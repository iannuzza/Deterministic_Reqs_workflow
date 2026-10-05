#!/usr/bin/env python3
"""Run ARS crosscheck for Stage 4 ARS outputs."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from traceability_content_checks import (
    check_authored_markdown_content,
    check_source_traceability_content,
    read_source_requirements,
)
from workflow_routing import is_reset_clock_table_row
from approved_snapshot_resolver import resolve_authoritative_input
from traceability_rules import is_valid_upstream_reference
from source_io_coverage import check_source_coverage


REQUIRED = [
    "artifacts/stage4_ars/analog_requirements_specification.md",
    "artifacts/stage4_ars/ars_traceability_matrix.csv",
    "artifacts/orchestrator/stage_ars_report.md",
    "artifacts/stage1_requirements/requirements_summary.csv",
    "artifacts/stage2_mirco_arc/block_inventory.csv",
    "artifacts/stage2_mirco_arc/interface_catalog.csv",
    "artifacts/stage2_mirco_arc/interaction_matrix.csv",
]


FUNCTION_STOP_WORDS = {
    "a", "and", "are", "as", "at", "by", "for", "from", "in", "into",
    "of", "on", "or", "the", "to", "with",
}


def _approved_snapshot_source_catalog(repo_root: Path, summary_path: Path) -> dict[str, dict[str, str]]:
    source_rows = read_source_requirements(summary_path)
    try:
        context = json.loads((repo_root / "config/project_context.json").read_text(encoding="utf-8"))
        snapshot = resolve_authoritative_input(
            repo_root,
            "4",
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


ANALOG_FOCUS_TERMS = (
    "analog",
    "temperature",
    "sensor",
    "adc",
    "hysteresis",
    "setpoint",
    "relay",
    "ambient",
    "remote",
    "sampling",
    "conversion",
    "voltage",
    "power",
    "brown-out",
    "calibration",
    "noise",
)


POWER_FOCUS_TERMS = (
    "power",
    "supply",
    "voltage",
    "brown-out",
    "reverse-polarity",
    "polarity",
)


DIGITAL_SYSTEM_TERMS = (
    "uart",
    "host",
    "external host",
    "command",
    "firmware",
    "led",
    "button",
    "event log",
    "state machine",
    "serial",
    "protocol",
    "telemetry",
    "nvm",
    "memory",
)


BLOCK_ANALOG_TERMS = (
    "analog",
    "sensor",
    "temperature",
    "adc",
    "conversion",
    "sampling",
    "hysteresis",
    "relay",
    "voltage",
    "power",
    "brown-out",
    "noise",
    "calibration",
)


BLOCK_DIGITAL_TERMS = (
    "uart",
    "host",
    "firmware",
    "command",
    "protocol",
    "gpio",
    "led",
    "button",
    "event",
    "schedule",
    "mode",
    "state machine",
    "telemetry",
    "nvm",
    "memory",
)


DIGITAL_ARCHITECTURE_TERMS = (
    "i2c", "spi", "ahb", "axi", "apb", "uart", "jtag", "serial",
    "protocol", "bus", "processor", "cpu", "microprocessor", "core", "digital",
)

BLOCK_CLASS_ANALOG = "analog_or_mixed"
BLOCK_CLASS_POWER = "power_or_supply"
BLOCK_CLASS_DIGITAL = "digital_or_system"


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


def _read_trace_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


def _split_blocks(mapped_blocks: str) -> List[str]:
    return [token.strip() for token in (mapped_blocks or "").split(";") if token.strip()]


def _is_single_upstream_id(covers_value: str) -> bool:
    value = (covers_value or "").strip()
    if not value or value.lower() == "none":
        return False
    if ";" in value or "," in value:
        return False
    return is_valid_upstream_reference(value)


def _has_markdown_table_with_columns(raw_text: str, required_terms: list[str]) -> bool:
    for line in raw_text.splitlines():
        if "|" not in line:
            continue
        low = line.lower()
        if all(term in low for term in required_terms):
            return True
    return False


def _read_block_inventory(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


def _read_interface_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


def _function_terms(text: str) -> set[str]:
    terms = set(re.findall(r"[a-z][a-z0-9]+", (text or "").lower()))
    return {
        term[:-1] if term.endswith("s") and len(term) > 4 else term
        for term in terms
        if term not in FUNCTION_STOP_WORDS and len(term) > 2
    }


def _normalize_block_heading_name(value: str) -> str:
    return re.sub(r"\s*\{#[a-zA-Z0-9_-]+\}\s*$", "", (value or "")).strip()


def _read_matrix_requirement_ids(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        ids: set[str] = set()
        for row in reader:
            ids.update(item.strip() for item in (row.get("Requirement IDs") or "").split(";") if item.strip())
        return ids


def _read_reset_clock_table_requirement_ids(path: Path) -> set[str]:
    out: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            req_id = (row.get("source_req_id") or row.get("id") or "").strip()
            if req_id and is_reset_clock_table_row(row):
                out.add(req_id)
    return out


def _reset_clock_owner(block_functions: Dict[str, str]) -> str:
    for block in block_functions:
        if block.strip().lower() == "pmu":
            return block

    ranked: List[Tuple[int, str]] = []
    for block, function in block_functions.items():
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


def _check_function_contract(
    raw_text: str,
    trace_rows: List[Dict[str, str]],
    block_functions: Dict[str, str],
    matrix_ids: set[str],
    reset_clock_table_ids: set[str],
) -> List[str]:
    findings: List[str] = []
    reset_clock_owner = _reset_clock_owner(block_functions)
    for block_name, function in block_functions.items():
        if not function:
            findings.append(f"Inventory block has empty Function: {block_name}")

    project_section = re.search(
        r"##\s+\d+\.\s+Project-specific analog block sections(.*?)(\n##\s+\d+\.|\n##\s+Assumptions|\n##\s+Missing|\Z)",
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
            expected = block_functions.get(block_name)
            if expected is None:
                findings.append(f"Generated ARS block is absent from block inventory: {block_name}")
            elif not description or description.group(1) != expected:
                findings.append(f"ARS Function description mismatch for block: {block_name}")

    for row in trace_rows:
        source_id = row.get("source_req_id", "")
        if source_id in matrix_ids:
            continue
        if (row.get("domain") or "").strip().upper() == "DIG":
            findings.append(f"Digital-domain requirement must not be emitted in ARS: {source_id}")
        requirement_terms = _function_terms(row.get("requirement_statement", ""))
        for owner in [item.strip() for item in row.get("owning_block", "").split(";") if item.strip()]:
            if owner.lower() == "unassigned":
                continue
            if owner not in block_functions:
                findings.append(f"ARS traceability owner is absent from block inventory: {owner}")
            elif source_id in reset_clock_table_ids and owner == reset_clock_owner:
                continue
            elif not requirement_terms & _function_terms(block_functions[owner]):
                findings.append(f"ARS owner is not supported by inventory Function: {source_id} -> {owner}")
    return findings


def _interface_types_by_owner(interface_rows: List[Dict[str, str]]) -> Dict[str, Dict[str, int]]:
    owner_types: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in interface_rows:
        owner = (row.get("Owner") or "").strip()
        iface_type = (row.get("Type") or "").strip().lower()
        if owner and iface_type:
            owner_types[owner][iface_type] += 1
    return owner_types


def _linked_domain_counts(linked_requirements: str) -> Dict[str, int]:
    counts = {"ana": 0, "dig": 0, "sys": 0}
    for token in [t.strip().upper() for t in (linked_requirements or "").split(";") if t.strip()]:
        if "ANA-RQ" in token or "CONF_ANA" in token:
            counts["ana"] += 1
        elif "DIG-RQ" in token or "CONF_DIG" in token:
            counts["dig"] += 1
        elif "SYS-RQ" in token or "CONF_SYS" in token:
            counts["sys"] += 1
    return counts


def _text_score(text: str, terms: Tuple[str, ...]) -> int:
    t = (text or "").lower()
    return sum(1 for token in terms if token in t)


def _classify_block_category(block: Dict[str, str], owner_types: Dict[str, Dict[str, int]]) -> str:
    bundle = block.get("Function", "")
    if _text_score(bundle, DIGITAL_ARCHITECTURE_TERMS) > 0:
        return BLOCK_CLASS_DIGITAL
    analog_score = _text_score(bundle, BLOCK_ANALOG_TERMS)
    power_score = _text_score(bundle, POWER_FOCUS_TERMS)
    digital_score = _text_score(bundle, BLOCK_DIGITAL_TERMS)

    if power_score > 0 and power_score >= digital_score:
        return BLOCK_CLASS_POWER
    if analog_score >= digital_score:
        return BLOCK_CLASS_ANALOG

    return BLOCK_CLASS_DIGITAL


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    missing = [rel for rel in REQUIRED if not (repo_root / rel).exists()]
    ars_md = repo_root / "artifacts/stage4_ars/analog_requirements_specification.md"
    trace_csv = repo_root / "artifacts/stage4_ars/ars_traceability_matrix.csv"
    block_inventory_csv = repo_root / "artifacts/stage2_mirco_arc/block_inventory.csv"
    interface_catalog_csv = repo_root / "artifacts/stage2_mirco_arc/interface_catalog.csv"

    status = "pass"
    findings: list[str] = []

    if missing:
        status = "fail"
        findings.append("Missing required artifacts: " + ", ".join(missing))

    trace_rows = _count_rows(trace_csv) if trace_csv.exists() else 0

    trace_details = _read_trace_rows(trace_csv) if trace_csv.exists() else []
    trace_ids = [row.get("ars_req_id", "") for row in trace_details]
    if any(not re.fullmatch(r"ARS-REQ-\d{3}", req_id) for req_id in trace_ids):
        status = "fail"
        findings.append("ARS traceability contains an invalid authored ID namespace")
    if len(trace_ids) != len(set(trace_ids)):
        status = "fail"
        findings.append("ARS traceability contains duplicate ARS-REQ IDs")
    summary_path = repo_root / "artifacts/stage1_requirements/requirements_summary.csv"
    source_catalog = _approved_snapshot_source_catalog(repo_root, summary_path)
    block_rows = _read_block_inventory(block_inventory_csv) if block_inventory_csv.exists() else []
    interface_rows = _read_interface_rows(interface_catalog_csv) if interface_catalog_csv.exists() else []
    owner_types = _interface_types_by_owner(interface_rows)
    block_category = {
        (row.get("Block") or "").strip(): _classify_block_category(row, owner_types)
        for row in block_rows
        if (row.get("Block") or "").strip()
    }
    interaction_matrix_path = repo_root / "artifacts/stage2_mirco_arc/interaction_matrix.csv"
    if ars_md.exists() and interaction_matrix_path.exists():
        source_content_findings = check_source_traceability_content(
            trace_details,
            source_catalog,
            _read_matrix_requirement_ids(interaction_matrix_path)
            | _read_reset_clock_table_requirement_ids(summary_path),
            "ars_req_id",
            "ARS",
        )
        if source_content_findings:
            status = "fail"
            findings.extend(source_content_findings[:20])
        authored_content_findings = check_authored_markdown_content(
            ars_md.read_text(encoding="utf-8") if ars_md.exists() else "",
            trace_details,
            source_catalog,
            _read_matrix_requirement_ids(interaction_matrix_path)
            | _read_reset_clock_table_requirement_ids(summary_path),
            "ars_req_id",
            "ARS",
        )
        if authored_content_findings:
            status = "fail"
            findings.extend(authored_content_findings[:20])
        function_findings = _check_function_contract(
            ars_md.read_text(encoding="utf-8"),
            trace_details,
            {(row.get("Block") or "").strip(): (row.get("Function") or "").strip() for row in block_rows if (row.get("Block") or "").strip()},
            _read_matrix_requirement_ids(interaction_matrix_path),
            _read_reset_clock_table_requirement_ids(summary_path) if summary_path.exists() else set(),
        )
        if function_findings:
            status = "fail"
            findings.extend(function_findings[:20])
    analog_class_blocks = {
        block_name
        for block_name, category in block_category.items()
        if category in {BLOCK_CLASS_ANALOG, BLOCK_CLASS_POWER}
    }
    unmapped_trace_rows: List[Dict[str, str]] = []
    for row in trace_details:
        owning = row.get("owning_block", "")
        tokens = _split_blocks(owning)
        if not tokens or all(token.lower() == "unassigned" for token in tokens):
            continue
        has_analog_block = any(token in analog_class_blocks for token in tokens)
        if not has_analog_block:
            unmapped_trace_rows.append(row)

    if unmapped_trace_rows:
        status = "fail"
        findings.append(
            "Requirements not mapped to included analog blocks: "
            + ", ".join((r.get("source_req_id") or r.get("ars_req_id") or "unknown") for r in unmapped_trace_rows[:20])
        )

    if ars_md.exists():
        raw_text = ars_md.read_text(encoding="utf-8")
        text = raw_text.lower()
        if "0. document navigation" not in text:
            status = "fail"
            findings.append("ARS is missing the required '0. Document Navigation' section")
        if "table of contents" not in text:
            status = "fail"
            findings.append("ARS is missing a table of contents section")
        if "internal index" not in text:
            status = "fail"
            findings.append("ARS is missing an internal index section")
        if "document control" not in text:
            status = "fail"
            findings.append("ARS is missing a document control section")
        if "table of tables" not in text:
            status = "fail"
            findings.append("ARS is missing a table of tables section")
        if "category convention" not in text:
            status = "fail"
            findings.append("ARS is missing a Category Convention section/table")
        else:
            if not _has_markdown_table_with_columns(raw_text, ["category", "scope"]):
                status = "fail"
                findings.append("ARS Category Convention table is missing required columns (at least Category and Scope)")

        if "analog" not in text:
            findings.append("ARS appears to lack analog-focused narrative")

        authored_ids = re.findall(r"^\s*\*\*\[(ARS-REQ-\d{3})\]\s+Requirement:\*\*\s*$", raw_text, flags=re.M)
        if trace_rows and not authored_ids:
            status = "fail"
            findings.append("Project-specific analog block sections are missing [ARS-REQ-xxx] Requirement: headers")
        if re.search(r"^\s*(?:-\s*)?Requirement ID:\s*ARS-REQ-\d{3}\b", raw_text, flags=re.M):
            status = "fail"
            findings.append("ARS markdown uses deprecated 'Requirement ID: ARS-REQ-xxx' format; expected '[ARS-REQ-xxx] Requirement:'")
        if re.search(r"^\s*####\s+ARS-REQ-\d{3}\b", raw_text, flags=re.M):
            status = "fail"
            findings.append("ARS markdown uses deprecated '#### ARS-REQ-xxx' heading format; expected '[ARS-REQ-xxx] Requirement:'")
        if re.search(
            r"^\s*####\s+ARS-REQ-\d{3}[^\n]*\n\s*-\s*Statement:\s*",
            raw_text,
            flags=re.M,
        ):
            status = "fail"
            findings.append("ARS markdown uses deprecated '- Statement:' authored field under ARS-REQ headings")
        if len(authored_ids) != len(set(authored_ids)):
            status = "fail"
            findings.append("ARS markdown contains duplicate ARS-REQ IDs")
        if set(authored_ids) - set(trace_ids):
            status = "fail"
            findings.append("ARS markdown contains authored IDs absent from ARS traceability")

        if "linked requirements" in text:
            status = "fail"
            findings.append("ARS markdown contains deprecated 'Linked requirements' wording; expected 'Covers'")
        unresolved_directives = [
            "Summarize high-level system behavior derived from requirements and micro-architecture artifacts.",
            "Describe current-project high-level behavior using only current Stage 1 and Stage 2A artifacts; do not reuse wording or identifiers from other projects.",
            "This section is generated from current Stage 1 and Stage 2A artifacts.",
        ]
        if any(directive in raw_text for directive in unresolved_directives):
            status = "fail"
            findings.append("ARS markdown contains unresolved template directive text in narrative sections")
        if "mapped requirements by analog block" in text:
            status = "fail"
            findings.append(
                "ARS markdown contains redundant mapped-summary section; mapped items shall be captured atomically in project-specific analog sub-block requirement paragraphs"
            )

        project_section = re.search(
            r"##\s+\d+\.\s+Project-specific analog block sections(.*?)(\n##\s+\d+\.|\n##\s+Assumptions|\n##\s+Missing|\Z)",
            raw_text,
            flags=re.S,
        )
        if project_section:
            req_ids = re.findall(r"^\s*\*\*\[(ARS-REQ-\d{3})\]\s+Requirement:\*\*\s*$", project_section.group(1), flags=re.M)
            dedicated_section = re.search(r"^####\s+Dedicated source sections\b", raw_text, flags=re.M)
            dedicated_req_ids = re.findall(
                r"^\s*\*\*\[(ARS-REQ-\d{3})\]\s+Requirement:\*\*\s*$",
                raw_text[dedicated_section.start():] if dedicated_section else "",
                flags=re.M,
            )
            context_section = re.search(r"^##\s+6\.4\s+Source Function Context\b(.*?)(?=^##\s+|\Z)", raw_text, flags=re.M | re.S)
            context_req_ids = re.findall(
                r"^\s*\*\*\[(ARS-REQ-\d{3})\]\s+Requirement:\*\*\s*$",
                context_section.group(1) if context_section else "",
                flags=re.M,
            )
            if trace_rows and not req_ids and not dedicated_req_ids and not context_req_ids:
                status = "fail"
                findings.append("Project-specific analog sub-block requirement paragraphs have no atomic ARS-REQ entries")
            elif len(req_ids) != len(set(req_ids)):
                status = "fail"
                findings.append("Project-specific analog sub-block requirement paragraphs contain duplicate ARS-REQ IDs")

            blocks = re.split(r"(?=^###\s+\d+\.\d+\s+)" , project_section.group(1), flags=re.M)
            for block_text in blocks:
                if not block_text.strip().startswith("###"):
                    continue
                local_req_ids = re.findall(r"^\s*\*\*\[(ARS-REQ-\d{3})\]\s+Requirement:\*\*\s*$", block_text, flags=re.M)
                local_covers = re.findall(r"^\s*(?:-\s*)?Covers:\s*(.+?)\s*$", block_text, flags=re.M)
                local_statements = re.findall(r"^\s*(The\s+.+?\s+block\s+shall\s+implement:\s*.+?)\s*$", block_text, flags=re.M)
                if re.search(r"^\s*(?:-\s*)?Statement:\s*", block_text, flags=re.M):
                    status = "fail"
                    findings.append("ARS authored entries must not use the legacy 'Statement:' field")

                if not local_req_ids:
                    status = "fail"
                    findings.append("A project-specific analog sub-block paragraph has no atomic ARS-REQ entries")
                    continue
                if len(local_req_ids) != len(local_covers):
                    status = "fail"
                    findings.append("A project-specific analog sub-block paragraph has mismatched Requirement ID and Covers counts")
                if len(local_req_ids) != len(local_statements):
                    status = "fail"
                    findings.append("A project-specific analog sub-block paragraph has mismatched Requirement ID and Statement counts")

                for covers_value in local_covers:
                    if not _is_single_upstream_id(covers_value):
                        status = "fail"
                        findings.append("Atomic Covers entry must contain exactly one upstream SRS-REQ-xxx ID")
                        break

                for statement in local_statements:
                    if "the following atomic functionality" in statement.lower():
                        status = "fail"
                        findings.append("Project-specific analog sub-block requirement statement uses deprecated filler phrase 'the following atomic functionality'")
                        break
                    if re.search(r"\b(?:DDS_[A-Z0-9_]+|(?:SYS|ANA|DIG|XDN)-RQ-\d+)\b", statement):
                        status = "fail"
                        findings.append("ARS authored statement must not contain an upstream requirement ID")
                        break

            listed = re.findall(r"^###\s+\d+\.\d+\s+(.+?)\s*$", project_section.group(1), flags=re.M)
            for block_name in listed:
                category = block_category.get(block_name, "unknown")
                if category == BLOCK_CLASS_DIGITAL:
                    status = "fail"
                    findings.append(
                        f"Block in project-specific analog section is classified as digital/system by architecture data: {block_name}"
                    )

    io_findings, io_report = check_source_coverage(
        repo_root,
        "ars",
        ars_md,
        repo_root / "artifacts/stage4_ars/analog_requirements_specification.docx",
        source_rows=list(source_catalog.values()),
        stage_active=bool(trace_rows),
        report_name="stage_ars_source_structural_coverage_report.md",
    )
    if io_findings:
        status = "fail"
        findings.extend(io_findings[:20])
    out = repo_root / "artifacts/orchestrator/stage_ars_crosscheck_report.md"
    lines = [
        "# Stage ARS Crosscheck Report",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        f"Status: {status}",
        "",
        "## Summary",
        f"- Traceability rows: {trace_rows}",
        f"- Source structural coverage: {io_report.relative_to(repo_root).as_posix()}",
        f"- Unmapped to included analog blocks: {len(unmapped_trace_rows)}",
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
        print(f"ARS crosscheck: FAIL ({out})")
        _append_log(repo_root, script_name, "FAIL")
        return 1

    print(f"ARS crosscheck: PASS ({out})")
    _append_log(repo_root, script_name, f"PASS rows={trace_rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
