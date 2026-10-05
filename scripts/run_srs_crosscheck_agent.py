#!/usr/bin/env python3
"""Run SRS crosscheck for Stage 3 SRS outputs."""

from __future__ import annotations

import csv
import json
import re
import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path
from traceability_content_checks import (
    check_authored_markdown_content,
    check_source_traceability_content,
    read_source_requirements,
)
from workflow_routing import is_reset_clock_table_row
from approved_snapshot_resolver import resolve_authoritative_input, resolve_complete_authoritative_input
from canonical_store import connect
from source_io_coverage import check_source_coverage
from validate_downstream_coherence import resolve_downstream_contract


REQUIRED = [
    "artifacts/stage3_srs/system_requirements_specification.md",
    "artifacts/stage3_srs/srs_traceability_matrix.csv",
    "artifacts/orchestrator/stage_srs_report.md",
    "artifacts/stage1_requirements/requirements_summary.csv",
    "artifacts/stage2_mirco_arc/block_inventory.csv",
    "artifacts/stage2_mirco_arc/interaction_matrix.csv",
    "artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv",
]


FUNCTION_STOP_WORDS = {
    "a", "and", "are", "as", "at", "by", "for", "from", "in", "into",
    "of", "on", "or", "the", "to", "with",
}


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\\n")


def _count_rows(csv_path: Path) -> int:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return sum(1 for _ in reader)


def _approved_snapshot_source_catalog(repo_root: Path, summary_path: Path) -> dict[str, dict[str, str]]:
    """Extend primary Stage 1 evidence with the immutable snapshot's approved rows."""
    source_rows = read_source_requirements(summary_path)
    try:
        context = json.loads((repo_root / "config/project_context.json").read_text(encoding="utf-8"))
        snapshot = resolve_authoritative_input(
            repo_root,
            "3",
            project_id=str(context.get("project_name") or repo_root.name),
            use_latest_approved=True,
        )
        for row in snapshot.rows:
            source_id = (row.get("source_req_id") or row.get("id") or "").strip()
            if source_id:
                source_rows[source_id] = {key: str(value or "") for key, value in row.items()}
    except Exception:
        pass
    return source_rows


def _validate_srs_allocation_scope(
    repo_root: Path,
    *,
    project_id: str,
    snapshot_id: str,
    snapshot_ids: set[str],
    trace_source_ids: list[str],
) -> list[str]:
    """Validate SRS-owned coverage against the selected snapshot allocation partition."""
    connection = connect(repo_root)
    try:
        rows = connection.execute(
            """SELECT req_id, owning_target
                 FROM requirement_allocations
                WHERE project_id = ? AND snapshot_id = ?
                ORDER BY req_id""",
            (project_id, snapshot_id),
        ).fetchall()
    finally:
        connection.close()
    if not rows:
        return [f"Allocation materialization has zero rows for selected snapshot {snapshot_id}"]
    allocation_ids = [str(row["req_id"] or "").strip() for row in rows]
    findings: list[str] = []
    if any(not req_id for req_id in allocation_ids):
        findings.append("Allocation materialization contains an empty requirement ID")
    if len(allocation_ids) != len(set(allocation_ids)):
        findings.append("Allocation materialization contains duplicate requirement IDs")
    if set(allocation_ids) != snapshot_ids:
        findings.append(
            "Allocation materialization does not match selected snapshot: "
            f"missing={sorted(snapshot_ids - set(allocation_ids))[:10]}, "
            f"extra={sorted(set(allocation_ids) - snapshot_ids)[:10]}"
        )
    allowed_targets = {"SRS", "DRS", "ARS", "Digital IPOS", "Analog IPOS", "none"}
    invalid_targets = sorted({str(row["owning_target"] or "").strip() for row in rows} - allowed_targets)
    if invalid_targets:
        findings.append("Allocation materialization contains invalid owning targets: " + ", ".join(invalid_targets))
    srs_ids = {
        str(row["req_id"]).strip()
        for row in rows
        if str(row["owning_target"] or "").strip() == "SRS"
    }
    trace_counts = Counter(req_id for req_id in trace_source_ids if req_id)
    missing_srs = sorted(req_id for req_id in srs_ids if trace_counts[req_id] != 1)
    if missing_srs:
        findings.append(
            "SRS-owned allocation requirements must appear exactly once in SRS traceability: "
            + ", ".join(missing_srs[:20])
        )
    manifest_path = repo_root / "artifacts/traceability_reports/requirement_allocation_materialization.json"
    if not manifest_path.exists():
        findings.append("Allocation materialization manifest is missing")
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if str(manifest.get("snapshot_id") or "") != snapshot_id:
            findings.append("Allocation materialization manifest snapshot does not match selected snapshot")
        if int(manifest.get("row_count") or 0) != len(snapshot_ids):
            findings.append("Allocation materialization manifest row count does not match selected snapshot")
    return findings


def _is_single_upstream_id(covers_value: str) -> bool:
    value = (covers_value or "").strip()
    if not value or value.lower() == "none":
        return False
    if ";" in value or "," in value:
        return False
    return re.match(r"^[A-Z0-9_\-]+$", value) is not None


def _function_terms(text: str) -> set[str]:
    terms = set(re.findall(r"[a-z][a-z0-9]+", (text or "").lower()))
    return {
        term[:-1] if term.endswith("s") and len(term) > 4 else term
        for term in terms
        if term not in FUNCTION_STOP_WORDS and len(term) > 2
    }


def _normalize_block_heading_name(value: str) -> str:
    return re.sub(r"\s*\{#[a-zA-Z0-9_-]+\}\s*$", "", (value or "")).strip()


def _read_block_inventory(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return {
            (row.get("Block") or "").strip(): (row.get("Function") or "").strip()
            for row in reader
            if (row.get("Block") or "").strip()
        }


def _read_matrix_requirement_ids(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        ids: set[str] = set()
        for row in reader:
            ids.update(item.strip() for item in (row.get("Requirement IDs") or "").split(";") if item.strip())
        return ids


def _read_stage2_owners(path: Path) -> dict[str, set[str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        owners: dict[str, set[str]] = {}
        for row in csv.DictReader(handle):
            source_id = (row.get("Requirement ID") or row.get("source_req_id") or "").strip()
            if not source_id:
                continue
            owners[source_id] = {
                item.strip()
                for item in (
                    row.get("Block(s)")
                    or row.get("Mapped Block")
                    or row.get("owning_block")
                    or ""
                ).split(";")
                if item.strip()
            }
            owners[source_id].discard("Unassigned")
        return owners


def _check_stage2_ownership_contract(
    trace_rows: list[dict[str, str]],
    stage2_owners: dict[str, set[str]],
    matrix_ids: set[str],
    source_section_owners: dict[str, str],
    reset_clock_ids: set[str],
    interrupt_ids: set[str],
    functions: dict[str, str],
) -> list[str]:
    findings: list[str] = []
    reset_clock_owner = _reset_clock_owner(functions)
    interrupt_owner = _interrupt_owner(functions)
    for row in trace_rows:
        source_id = row.get("source_req_id", "").strip()
        if not source_id or source_id in matrix_ids or source_id not in stage2_owners:
            continue
        expected = stage2_owners[source_id]
        actual = {
            item.strip()
            for item in row.get("owning_block", "").split(";")
            if item.strip()
        }
        actual.discard("Unassigned")
        if expected != actual:
            findings.append(
                f"SRS owner differs from authoritative Stage 2A mapping: {source_id} "
                f"(stage2={'; '.join(sorted(expected)) or 'Unassigned'}, "
                f"srs={'; '.join(sorted(actual)) or 'Unassigned'})"
            )
    return findings


def _check_function_contract(
    raw_text: str,
    trace_rows: list[dict[str, str]],
    functions: dict[str, str],
    matrix_ids: set[str],
    source_section_owners: dict[str, str],
    reset_clock_table_ids: set[str],
    interrupt_table_ids: set[str],
) -> list[str]:
    findings: list[str] = []
    reset_clock_owner = _reset_clock_owner(functions)
    interrupt_owner = _interrupt_owner(functions)
    for block_name, function in functions.items():
        if not function:
            findings.append(f"Inventory block has empty Function: {block_name}")

    project_section = re.search(
        r"##\s+\d+\.\s+Project-specific block sections(.*?)(\n##\s+\d+\.|\n##\s+Assumptions|\n##\s+Missing|\Z)",
        raw_text,
        flags=re.S,
    )
    if project_section:
        blocks = re.split(r"(?=^###\s+\d+\.\d+\s+)", project_section.group(1), flags=re.M)
        for block_text in blocks:
            header = re.search(r"^###\s+\d+\.\d+\s+(.+?)\s*$", block_text, flags=re.M)
            if not header:
                continue
            block_name = _normalize_block_heading_name(header.group(1))
            description = re.search(r"^General functional description:\s*(.*?)\s*$", block_text, flags=re.M)
            expected = functions.get(block_name)
            if expected is None:
                findings.append(f"Generated SRS block is absent from block inventory: {block_name}")
            elif not description or description.group(1) != expected:
                findings.append(f"SRS Function description mismatch for block: {block_name}")

    for row in trace_rows:
        source_id = row.get("source_req_id", "")
        if source_id in matrix_ids:
            continue
        requirement_terms = _function_terms(row.get("requirement_statement", ""))
        for owner in [item for item in row.get("owning_block", "").split(";") if item.strip()]:
            owner = owner.strip()
            if owner.lower() == "unassigned":
                continue
            if owner not in functions:
                findings.append(f"SRS traceability owner is absent from block inventory: {owner}")
    return findings


def _has_markdown_table_with_columns(raw_text: str, required_terms: list[str]) -> bool:
    for line in raw_text.splitlines():
        if "|" not in line:
            continue
        low = line.lower()
        if all(term in low for term in required_terms):
            return True
    return False


def _slugify_heading(title: str) -> str:
    base = re.sub(r"[^a-z0-9\s-]", "", (title or "").lower())
    base = re.sub(r"\s+", "-", base).strip("-")
    return base or "section"


def _collect_heading_anchors(raw_text: str) -> tuple[set[str], dict[str, int]]:
    heading_re = re.compile(r"^(#{2,6})\s+(.+?)\s*$", flags=re.M)
    seen: dict[str, int] = {}
    anchors: set[str] = set()
    anchor_counts: dict[str, int] = {}

    for _hashes, raw_title in heading_re.findall(raw_text):
        explicit_id_match = re.search(r"\s*\{#([a-zA-Z0-9_-]+)\}\s*$", raw_title)
        title = re.sub(r"\s*\{#[a-zA-Z0-9_-]+\}\s*$", "", raw_title).strip()
        base = _slugify_heading(title)

        if explicit_id_match:
            anchor = explicit_id_match.group(1).strip().lower()
        else:
            next_count = seen.get(base, 0) + 1
            seen[base] = next_count
            anchor = base if next_count == 1 else f"{base}-{next_count - 1}"
        anchor_counts[anchor] = anchor_counts.get(anchor, 0) + 1
        anchors.add(anchor)

    return anchors, anchor_counts


def _read_source_section_owners(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {
            (row.get("source_req_id") or row.get("id") or "").strip(): (row.get("source_section_owner") or "").strip()
            for row in csv.DictReader(handle)
            if (row.get("source_req_id") or row.get("id") or "").strip()
            and (row.get("source_section_owner") or "").strip()
        }


def _read_reset_clock_table_requirement_ids(path: Path) -> set[str]:
    out: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            req_id = (row.get("source_req_id") or row.get("id") or "").strip()
            if req_id and is_reset_clock_table_row(row):
                out.add(req_id)
    return out


def _read_interrupt_table_requirement_ids(path: Path) -> set[str]:
    out: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            req_id = (row.get("source_req_id") or row.get("id") or "").strip()
            metadata = " ".join(
                (
                    row.get("derivation_kind") or "",
                    row.get("evidence_type") or "",
                    row.get("notes") or "",
                )
            ).lower()
            if req_id and "interrupt_table_connection" in metadata and "derived-from-structure" in metadata:
                out.add(req_id)
    return out


def _reset_clock_owner(functions: dict[str, str]) -> str:
    for block in functions:
        if block.strip().lower() == "pmu":
            return block

    ranked: list[tuple[int, str]] = []
    for block, function in functions.items():
        text = f"{block} {function}".lower()
        if "clock" not in text and "reset" not in text:
            continue
        score = sum(
            1
            for term in ("pmu", "power", "clock", "reset", "por", "ldo", "sequence", "sequencing", "release", "ready")
            if term in text
        )
        if score:
            ranked.append((score, block))

    if not ranked:
        return ""
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return ranked[0][1]


def _interrupt_owner(functions: dict[str, str]) -> str:
    ranked: list[tuple[int, str]] = []
    for block, function in functions.items():
        text = f"{block} {function}".lower()
        score = sum(1 for term in ("processor", "cpu", "microcontroller", "controller", "interrupt", "irq") if term in text)
        if score:
            ranked.append((score, block))
    if not ranked:
        return ""
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return ranked[0][1]


def _collect_internal_link_fragments(raw_text: str) -> list[str]:
    fragments = re.findall(r"\[[^\]]+\]\(#([^)]+)\)", raw_text)
    return [frag.strip().lower() for frag in fragments if frag.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run SRS crosscheck for Stage 3 SRS outputs.")
    parser.add_argument("--snapshot-id", help="Approved snapshot ID used to generate the SRS outputs")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    missing = [rel for rel in REQUIRED if not (repo_root / rel).exists()]
    srs_md = repo_root / "artifacts/stage3_srs/system_requirements_specification.md"
    trace_csv = repo_root / "artifacts/stage3_srs/srs_traceability_matrix.csv"

    status = "pass"
    findings: list[str] = []

    if missing:
        status = "fail"
        findings.append("Missing required artifacts: " + ", ".join(missing))

    trace_rows = _count_rows(trace_csv) if trace_csv.exists() else 0
    downstream_contract = resolve_downstream_contract(repo_root, args.snapshot_id)
    approved_srs_empty = not downstream_contract.source_ids_for_target("SRS")
    if trace_csv.exists() and trace_rows == 0 and not approved_srs_empty:
        status = "fail"
        findings.append("SRS traceability matrix has zero rows")

    trace_details: list[dict[str, str]] = []
    if trace_csv.exists():
        with trace_csv.open("r", encoding="utf-8", newline="") as handle:
            trace_details = [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]
    trace_ids = [row.get("srs_req_id", "") for row in trace_details]
    if any(not re.fullmatch(r"SRS-REQ-\d{3}", req_id) for req_id in trace_ids):
        status = "fail"
        findings.append("SRS traceability contains an invalid authored ID namespace")
    if len(trace_ids) != len(set(trace_ids)):
        status = "fail"
        findings.append("SRS traceability contains duplicate SRS-REQ IDs")
    context = json.loads((repo_root / "config/project_context.json").read_text(encoding="utf-8"))
    project_id = str(context.get("project_name") or repo_root.name)
    try:
        selected_input, selected_record = resolve_complete_authoritative_input(
            repo_root, "3", project_id=project_id, snapshot_id=downstream_contract.snapshot_id
        )
        selected_ids = {
            (row.get("source_req_id") or row.get("canonical_id") or row.get("id") or "").strip()
            for row in selected_input.rows
            if (row.get("source_req_id") or row.get("canonical_id") or row.get("id") or "").strip()
        }
        allocation_findings = _validate_srs_allocation_scope(
            repo_root,
            project_id=project_id,
            snapshot_id=str(selected_record["selected_snapshot_id"]),
            snapshot_ids=selected_ids,
            trace_source_ids=[row.get("source_req_id", "").strip() for row in trace_details],
        )
        if allocation_findings:
            status = "fail"
            findings.extend(allocation_findings)
    except Exception as exc:
        status = "fail"
        findings.append(f"Selected snapshot allocation validation failed: {exc}")
    inventory_path = repo_root / "artifacts/stage2_mirco_arc/block_inventory.csv"
    matrix_path = repo_root / "artifacts/stage2_mirco_arc/interaction_matrix.csv"
    stage2_trace_path = repo_root / "artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv"
    summary_path = repo_root / "artifacts/stage1_requirements/requirements_summary.csv"
    if inventory_path.exists() and matrix_path.exists() and summary_path.exists() and stage2_trace_path.exists():
        source_catalog = _approved_snapshot_source_catalog(repo_root, summary_path)
        mode_trace_ids = {
            (row.get("source_req_id") or "").strip()
            for row in trace_details
            if (row.get("notes") or "").strip() == "operating mode state table"
            and (row.get("source_req_id") or "").strip()
        }
        for row in trace_details:
            source_id = (row.get("source_req_id") or "").strip()
            if source_id in mode_trace_ids and source_id not in source_catalog:
                source_catalog[source_id] = {
                    "requirement_statement": row.get("requirement_statement") or "",
                    "source": row.get("source_artifact") or "",
                }
        matrix_ids = _read_matrix_requirement_ids(matrix_path)
        ownership_findings = _check_stage2_ownership_contract(
            trace_details,
            _read_stage2_owners(stage2_trace_path),
            matrix_ids,
            _read_source_section_owners(summary_path),
            _read_reset_clock_table_requirement_ids(summary_path),
            _read_interrupt_table_requirement_ids(summary_path),
            _read_block_inventory(inventory_path),
        )
        if ownership_findings:
            status = "fail"
            findings.extend(ownership_findings[:20])
        source_content_findings = check_source_traceability_content(
            trace_details,
            source_catalog,
            matrix_ids
            | _read_reset_clock_table_requirement_ids(summary_path)
            | _read_interrupt_table_requirement_ids(summary_path),
            "srs_req_id",
            "SRS",
        )
        if source_content_findings:
            status = "fail"
            findings.extend(source_content_findings[:20])
        authored_content_findings = check_authored_markdown_content(
            srs_md.read_text(encoding="utf-8") if srs_md.exists() else "",
            trace_details,
            source_catalog,
            _read_matrix_requirement_ids(matrix_path)
            | _read_reset_clock_table_requirement_ids(summary_path)
            | _read_interrupt_table_requirement_ids(summary_path),
            "srs_req_id",
            "SRS",
        )
        if authored_content_findings:
            status = "fail"
            findings.extend(authored_content_findings[:20])
        function_findings = _check_function_contract(
            srs_md.read_text(encoding="utf-8") if srs_md.exists() else "",
            trace_details,
            _read_block_inventory(inventory_path),
            _read_matrix_requirement_ids(matrix_path),
            _read_source_section_owners(summary_path),
            _read_reset_clock_table_requirement_ids(summary_path),
            _read_interrupt_table_requirement_ids(summary_path),
        )
        if function_findings:
            status = "fail"
            findings.extend(function_findings[:20])

    if srs_md.exists():
        raw_text = srs_md.read_text(encoding="utf-8")
        text = raw_text.lower()
        if "0. document navigation" not in text:
            status = "fail"
            findings.append("SRS is missing the required '0. Document Navigation' section")
        if "table of contents" not in text:
            status = "fail"
            findings.append("SRS is missing a table of contents section")
        if "internal index" not in text:
            status = "fail"
            findings.append("SRS is missing an internal index section")
        if "document control" not in text:
            status = "fail"
            findings.append("SRS is missing a document control section")
        if "table of tables" not in text:
            status = "fail"
            findings.append("SRS is missing a table of tables section")
        if "category convention" not in text:
            status = "fail"
            findings.append("SRS is missing a Category Convention section/table")
        else:
            if not _has_markdown_table_with_columns(raw_text, ["category", "scope"]):
                status = "fail"
                findings.append("SRS Category Convention table is missing required columns (at least Category and Scope)")

        if " shall " not in text and "shall" not in text:
            findings.append("SRS appears to lack normative 'shall' wording")
        if "linked requirements" in text:
            status = "fail"
            findings.append("SRS markdown contains deprecated 'Linked requirements' wording; expected 'Covers'")

        unresolved_directives = [
            "Summarize high-level system behavior derived from requirements and micro-architecture artifacts.",
            "Describe current-project high-level behavior using only current Stage 1 and Stage 2A artifacts; do not reuse wording or identifiers from other projects.",
            "This section is generated from current Stage 1 and Stage 2A artifacts.",
        ]
        if any(directive in raw_text for directive in unresolved_directives):
            status = "fail"
            findings.append("SRS markdown contains unresolved template directive text in narrative sections")

        forbidden_html_patterns = [r"<a\b"]
        for pattern in forbidden_html_patterns:
            if re.search(pattern, raw_text, flags=re.I):
                status = "fail"
                findings.append("SRS markdown contains forbidden raw HTML anchors that break DOCX-safe linking")
                break

        heading_anchors, heading_base_counts = _collect_heading_anchors(raw_text)
        internal_fragments = _collect_internal_link_fragments(raw_text)
        unresolved = sorted({frag for frag in internal_fragments if frag not in heading_anchors})
        if unresolved:
            status = "fail"
            findings.append(
                "SRS contains unresolved internal link fragments: " + ", ".join(unresolved[:15])
            )

        duplicate_heading_targets = sorted(base for base, count in heading_base_counts.items() if count > 1)
        if duplicate_heading_targets:
            status = "fail"
            findings.append(
                "SRS contains duplicate heading targets (anchor base reused): "
                + ", ".join(duplicate_heading_targets[:15])
            )

        authored_ids = re.findall(r"^\s*\*\*\[(SRS-REQ-\d{3})\]\s+Requirement:\*\*\s*$", raw_text, flags=re.M)
        structural_only_trace = bool(trace_details) and all(
            (row.get("notes") or "").strip() in {
                "operating mode state table",
                "source=Stage 2 connection matrix",
            }
            for row in trace_details
        )
        if not approved_srs_empty and not authored_ids and not structural_only_trace:
            status = "fail"
            findings.append("Project-specific block sections are missing [SRS-REQ-xxx] Requirement: headers")
        if re.search(r"^\s*(?:-\s*)?Requirement ID:\s*SRS-REQ-\d{3}\b", raw_text, flags=re.M):
            status = "fail"
            findings.append("SRS markdown uses deprecated 'Requirement ID: SRS-REQ-xxx' format; expected '[SRS-REQ-xxx] Requirement:'")
        if re.search(r"^\s*####\s+SRS-REQ-\d{3}\b", raw_text, flags=re.M):
            status = "fail"
            findings.append("SRS markdown uses deprecated '#### SRS-REQ-xxx' heading format; expected '[SRS-REQ-xxx] Requirement:'")
        if re.search(
            r"^\s*####\s+SRS-REQ-\d{3}[^\n]*\n\s*-\s*Statement:\s*",
            raw_text,
            flags=re.M,
        ):
            status = "fail"
            findings.append("SRS markdown uses deprecated '- Statement:' authored field under SRS-REQ headings")
        if len(authored_ids) != len(set(authored_ids)):
            status = "fail"
            findings.append("SRS markdown contains duplicate SRS-REQ IDs")
        if not approved_srs_empty and set(authored_ids) - set(trace_ids):
            status = "fail"
            findings.append("SRS markdown contains authored IDs absent from SRS traceability")
        authored_blocks = re.findall(
            r"^\s*\*\*\[(SRS-REQ-\d{3})\]\s+Requirement:\*\*\s*\n(.*?)(?=^\s*\*\*\[SRS-REQ-\d{3}\]\s+Requirement:\*\*\s*$|\Z)",
            raw_text,
            flags=re.M | re.S,
        )
        for _req_id, block in authored_blocks:
            statement_text = re.split(r"^\s*(?:-\s*)?Covers:\s*", block, maxsplit=1, flags=re.M)[0]
            if re.search(r"\b(?:DDS_[A-Z0-9_]+|(?:SYS|ANA|DIG|XDN)-RQ-\d+)\b", statement_text):
                status = "fail"
                findings.append("SRS authored statement contains an upstream requirement ID outside Covers")
                break
            if re.search(r"DCC\s+IP\s+00\s+25nA\s+01\s+50nA", statement_text):
                status = "fail"
                findings.append("SRS authored statement contains an unrewritten DCC table fragment")
                break

        project_section = re.search(
            r"##\s+\d+\.\s+Project-specific block sections(.*?)(\n##\s+\d+\.|\n##\s+Assumptions|\n##\s+Missing|\Z)",
            raw_text,
            flags=re.S,
        )
        if project_section:
            summary_only = (
                "Block-specific requirements, source I/O tables, ports, pins, clocks, and resets are owned by DRS or ARS"
                in project_section.group(1)
            )
            req_ids = re.findall(r"^\s*\*\*\[(SRS-REQ-\d{3})\]\s+Requirement:\*\*\s*$", project_section.group(1), flags=re.M)
            if not req_ids and not summary_only:
                status = "fail"
                findings.append("Project-specific sub-block requirement paragraphs have no atomic SRS-REQ entries")
            elif req_ids and len(req_ids) != len(set(req_ids)):
                status = "fail"
                findings.append("Project-specific sub-block requirement paragraphs contain duplicate SRS-REQ IDs")

            if not summary_only:
                blocks = re.split(r"(?=^###\s+\d+\.\d+\s+)", project_section.group(1), flags=re.M)
                for block_text in blocks:
                    if not block_text.strip().startswith("###"):
                        continue
                    local_req_ids = re.findall(r"^\s*\*\*\[(SRS-REQ-\d{3})\]\s+Requirement:\*\*\s*$", block_text, flags=re.M)
                    local_covers = re.findall(r"^\s*(?:-\s*)?Covers:\s*(.+?)\s*$", block_text, flags=re.M)
                    local_statements = re.findall(r"^\s*(The\s+.+?\s+block\s+shall\s+implement:\s*.+?)\s*$", block_text, flags=re.M)
                    if re.search(r"^\s*(?:-\s*)?Statement:\s*", block_text, flags=re.M):
                        status = "fail"
                        findings.append("SRS authored entries must not use the legacy 'Statement:' field")

                    if not local_req_ids:
                        status = "fail"
                        findings.append("A project-specific sub-block paragraph has no atomic SRS-REQ entries")
                        continue
                    if len(local_req_ids) != len(local_covers):
                        status = "fail"
                        findings.append("A project-specific sub-block paragraph has mismatched Requirement ID and Covers counts")
                    if len(local_req_ids) != len(local_statements):
                        status = "fail"
                        findings.append("A project-specific sub-block paragraph has mismatched Requirement ID and Statement counts")

                    for covers_value in local_covers:
                        if not _is_single_upstream_id(covers_value):
                            status = "fail"
                            findings.append("Atomic Covers entry must contain exactly one upstream requirement ID")
                            break

                    for statement in local_statements:
                        if "the following atomic functionality" in statement.lower():
                            status = "fail"
                            findings.append("Project-specific sub-block requirement statement uses deprecated filler phrase 'the following atomic functionality'")
                            break
                        if re.search(r"\b(?:DDS_[A-Z0-9_]+|(?:SYS|ANA|DIG|XDN)-RQ-\d+)\b", statement):
                            status = "fail"
                            findings.append("SRS authored statement must not contain an upstream requirement ID")
                            break

    io_findings, io_report = check_source_coverage(
        repo_root,
        "srs",
        repo_root / "artifacts/stage3_srs/system_requirements_specification.md",
        repo_root / "artifacts/stage3_srs/system_requirements_specification.docx",
        source_rows=list(source_catalog.values()),
        report_name="stage_srs_source_structural_coverage_report.md",
    )
    if io_findings:
        status = "fail"
        findings.extend(io_findings[:20])
    out = repo_root / "artifacts/orchestrator/stage_srs_crosscheck_report.md"
    lines = [
        "# Stage SRS Crosscheck Report",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        f"Status: {status}",
        "",
        "## Summary",
        f"- Traceability rows: {trace_rows}",
        f"- Source structural coverage: {io_report.relative_to(repo_root).as_posix()}",
        "",
        "## Findings",
    ]
    if findings:
        lines.extend([f"- {f}" for f in findings])
    else:
        lines.append("- None")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\\n".join(lines) + "\\n", encoding="utf-8")

    if status != "pass":
        print(f"SRS crosscheck: FAIL ({out})")
        _append_log(repo_root, script_name, "FAIL")
        return 1

    print(f"SRS crosscheck: PASS ({out})")
    _append_log(repo_root, script_name, f"PASS rows={trace_rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
