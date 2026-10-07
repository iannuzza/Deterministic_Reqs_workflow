#!/usr/bin/env python3
"""Generate deterministic digital or analog IPOS requirements from a frozen snapshot."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import warnings
import re
from datetime import date, datetime
from pathlib import Path

from approved_snapshot_resolver import resolve_complete_authoritative_input
from workflow_routing import (
    approved_snapshot_candidate_rows,
    build_ipos_functional_input,
    build_ipos_normalized_records,
    build_ipos_semantic_units,
    compose_ipos_overview,
    write_ipos_descriptive_audit,
    apply_shared_spec_markdown_formatting,
    apply_unique_spec_heading_anchors,
    spec_anchor_slug,
    apply_docx_common_spec_formatting,
    GENERATED_SPEC_VERSION,
    apply_docx_authored_requirement_formatting,
    apply_docx_ipos_requirement_style_guard,
    document_author_name,
    document_version_for_snapshot,
    document_version_history_markdown,
)
from spec_document_contract import write_materialization_audit
from allocation_ledger import read_csv, refresh_ledger
from requirement_allocation_policy import BLOCK_LOCAL_ANALOG, BLOCK_LOCAL_DIGITAL
from validate_downstream_coherence import (
    ipos_authored_requirement_id,
    resolve_downstream_contract,
    validate as validate_downstream_coherence,
)


CONFIG = {
    "digital": {
        "upstream": "DRS",
        "prefix": "IPOS-DIG-REQ",
        "trace": "artifacts/stage5_drs/drs_traceability_matrix.csv",
        "output_dir": "artifacts/stage6_digital_ipos",
        "title": "Digital IPOS - {block_name}",
        "docx": "digital_ipos_requirements_specification.docx",
    },
    "analog": {
        "upstream": "ARS",
        "prefix": "IPOS-ANA-REQ",
        "trace": "artifacts/stage4_ars/ars_traceability_matrix.csv",
        "output_dir": "artifacts/stage7_analog_ipos",
        "title": "Analog IPOS - {block_name}",
        "docx": "analog_ipos_requirements_specification.docx",
    },
}

DOCX_REFERENCE_TEMPLATE = Path("templates/MPT_IPOS_template.docx")


DIGITAL_ARCHITECTURE_TERMS = (
    "i2c", "spi", "ahb", "axi", "apb", "uart", "jtag", "serial",
    "protocol", "bus", "processor", "cpu", "microprocessor", "core", "digital",
)
ANALOG_TERMS = (
    "analog", "sensor", "temperature", "adc", "conversion", "sampling",
    "hysteresis", "relay", "voltage", "noise", "calibration", "afe",
)
POWER_TERMS = ("power", "supply", "voltage", "brown-out", "polarity")
DIGITAL_TERMS = (
    "control", "dsp", "uart", "host", "firmware", "command", "protocol", "gpio",
    "led", "button", "event", "schedule", "mode", "state machine", "telemetry",
    "nvm", "memory", "register", "interrupt", "fifo", "test", "debug",
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise RuntimeError(f"Required upstream traceability artifact is missing: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _inventory_blocks(repo_root: Path, kind: str) -> list[str]:
    """Return all concrete inventory blocks applicable to one IPOS domain."""
    inventory_path = repo_root / "artifacts/stage2_mirco_arc/block_inventory.csv"
    if not inventory_path.exists():
        return []
    blocks: list[str] = []
    for row in _read_csv(inventory_path):
        name = row.get("Block", "").strip()
        entity_kind = row.get("Entity kind", "concrete_block").strip().casefold()
        function = row.get("Function", "").casefold()
        if not name or name.casefold() == "unassigned" or entity_kind != "concrete_block":
            continue
        analog_score = sum(term in function for term in ANALOG_TERMS)
        power_score = sum(term in function for term in POWER_TERMS)
        digital_score = sum(term in function for term in DIGITAL_TERMS)
        is_analog = (
            "convert" in function and ("adc" in function or "analog" in function)
        ) or (
            analog_score > digital_score and analog_score >= 2
        ) or (
            power_score > digital_score and power_score >= 2
        )
        if (kind == "analog" and is_analog) or (kind == "digital" and not is_analog):
            blocks.append(name)
    return sorted(dict.fromkeys(blocks), key=str.casefold)


def _digital_inventory_blocks(repo_root: Path) -> list[str]:
    return _inventory_blocks(repo_root, "digital")


def _analog_inventory_blocks(repo_root: Path) -> list[str]:
    return _inventory_blocks(repo_root, "analog")


def _block_slug(block_name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", block_name.casefold()).strip("-")
    return slug or "unnamed-block"


def _ipos_requirement_id(block_name: str, sequence: int) -> str:
    return ipos_authored_requirement_id(block_name, sequence)


def _block_docx_name(kind: str, block_name: str) -> str:
    return f"{kind}_ipos_{_block_slug(block_name)}.docx"


def _block_markdown_name(kind: str, block_name: str) -> str:
    return f"{kind}_ipos_{_block_slug(block_name)}.md"


def _block_inventory_record(repo_root: Path, block_name: str) -> dict[str, str]:
    path = repo_root / "artifacts/stage2_mirco_arc/block_inventory.csv"
    if not path.exists():
        return {}
    return next((row for row in _read_csv(path) if row.get("Block", "").strip() == block_name), {})


def _write_ipos_document(
    repo_root: Path,
    config: dict[str, str],
    kind: str,
    title: str,
    output_dir: Path,
    block_name: str,
    rows: list[dict[str, str]],
    snapshot_id: str,
    require_docx: bool = True,
    candidate_requirement_rows: list[dict[str, str]] | None = None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    source_port_path = repo_root / "artifacts/stage2_mirco_arc/source_port_catalog.csv"
    source_ports = []
    if source_port_path.exists():
        source_ports = [
            port
            for port in _read_csv(source_port_path)
            if port.get("Owner", "").strip() == block_name
            and port.get("Ownership status", "").strip().casefold() == "approved"
        ]

    inventory = _block_inventory_record(repo_root, block_name)
    functional_input = build_ipos_functional_input(
        block_name,
        inventory,
        rows,
        domain=kind,
        materialized=bool(rows),
        provenance=(
            "approved snapshot",
            "artifacts/stage2_mirco_arc/block_inventory.csv",
        ),
        candidate_requirement_rows=candidate_requirement_rows,
    )
    overview_sections, ipos_audit = compose_ipos_overview(
        functional_input,
    )
    write_ipos_descriptive_audit(output_dir / "descriptive_summary_audit.csv", ipos_audit)
    markdown_path = output_dir / _block_markdown_name(kind, block_name)
    document_version = document_version_for_snapshot(markdown_path, snapshot_id)
    document_author = document_author_name()
    lines = [
        f"# {title}",
        "",
        f"- Snapshot: `{snapshot_id}`",
        "",
        f"Author: {document_author}",
        "",
        "## 0. Document Navigation",
        "",
        "### 0.1 Table of contents",
        "- [1. Block overview](#1-block-overview)",
        "- [2. Source I/O](#2-source-io)",
        "- [3. Block requirements](#3-block-requirements)",
        "",
        "### 0.2 Document control",
        "#### Table 1. Version history",
        *document_version_history_markdown(
            markdown_path, snapshot_id, document_version, date.today().isoformat(),
            f"Snapshot {snapshot_id} {kind} IPOS block baseline", document_author,
        ),
        "",
        "### 0.3 Requirement navigation",
        "| Requirement | Internal link |",
        "|---|---|",
        *[
            f"| {row['ipos_req_id']} | [Go to requirement](#{spec_anchor_slug(row['ipos_req_id'])}) |"
            for row in rows
        ],
        "",
        "## 1. Block overview",
        "",
    ]
    lines.extend(["### 1.1 Functionality", ""])
    lines.extend(overview_sections["functionality"])
    lines.append("")
    lines.extend(["### 1.2 Supported functions and scope", ""])
    lines.extend(f"- {entry}" for entry in overview_sections["scope"])
    lines.append("")
    if overview_sections["internal_structure"]:
        lines.extend(["### 1.3 Internal structure", ""])
        lines.extend(f"- {entry}" for entry in overview_sections["internal_structure"])
        lines.append("")
    if overview_sections["internal_functions"]:
        lines.extend(["### 1.4 Internal blocks or functions", ""])
        lines.extend(f"- {entry}" for entry in overview_sections["internal_functions"])
        lines.append("")
    if overview_sections["general_architecture"]:
        lines.extend(["### 1.5 General architecture", ""])
        lines.extend(f"- {entry}" for entry in overview_sections["general_architecture"])
        lines.append("")
    lines.extend(["## 2. Source I/O", ""])
    if source_ports:
        lines.extend([
            "The following approved source I/O entries are owned by this block.",
            "",
            "| Port name | Direction | Type / details | Table | Source page |",
            "|---|---|---|---|---|",
        ])
        for port in source_ports:
            lines.append(
                "| " + " | ".join([
                    port.get("Port name", ""),
                    port.get("Direction", ""),
                    port.get("Type / details", "").replace("|", "\\|"),
                    port.get("Table title", ""),
                    port.get("Source page", ""),
                ]) + " |"
            )
    else:
        lines.append("No approved source I/O entries are assigned to this block in the current architecture snapshot.")
    lines.append("")
    if not rows:
        lines.extend([
            "## 3. Block requirements",
            "",
            "### 2.1 Scope status",
            "",
            "Not applicable: no approved upstream requirements are mapped to this block in the selected snapshot.",
            "",
        ])
    lines.extend(["## 3. Block requirements", ""])
    for row in rows:
        lines.extend([
            "",
            f"#### {row['ipos_req_id']}",
            row["requirement_statement"],
            "",
            f"Covers: {row['covers_upstream_req_id']}",
            "",
            "[End]",
            "",
        ])

    lines = apply_unique_spec_heading_anchors(
        apply_shared_spec_markdown_formatting(lines, preserve_authored_text=True)
    )
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    template_path = repo_root / DOCX_REFERENCE_TEMPLATE
    if not require_docx and not template_path.exists():
        return
    if not template_path.exists():
        raise RuntimeError(f"IPOS DOCX reference template is missing: {template_path}")
    if shutil.which("pandoc") is None:
        raise RuntimeError("pandoc is required for IPOS DOCX generation but is not available on PATH")
    docx_path = output_dir / config["docx"]
    _convert_ipos_markdown_to_docx(markdown_path, template_path, docx_path, repo_root)
    apply_docx_authored_requirement_formatting(docx_path, ("IPOS",))
    apply_docx_ipos_requirement_style_guard(docx_path)
    apply_docx_common_spec_formatting(docx_path)
    write_materialization_audit(
        output_dir / "materialization_audit.json",
        "IPOS",
        build_ipos_normalized_records(functional_input),
        build_ipos_semantic_units(functional_input, overview_sections, ipos_audit),
        markdown_path,
        docx_path,
    )


def _convert_ipos_markdown_to_docx(markdown_path: Path, template_path: Path, docx_path: Path, repo_root: Path) -> None:
    result = subprocess.run(
        [
            "pandoc",
            str(markdown_path),
            "--from",
            "markdown+pipe_tables+header_attributes+raw_html",
            "--to",
            "docx",
            "--reference-doc",
            str(template_path),
            "-o",
            str(docx_path),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        details = (result.stderr or result.stdout or "Pandoc returned no diagnostic output.").strip()
        lock_path = docx_path.with_name(f"~${docx_path.name[2:]}")
        lock_note = (
            f" Office lock detected at {lock_path}; close the document in Word and, "
            "if no Office process is using it, remove the stale lock before retrying."
            if lock_path.exists()
            else ""
        )
        raise RuntimeError(
            f"IPOS md->docx conversion failed with exit code {result.returncode}: "
            f"{details}{lock_note}"
        )


def generate(repo_root: Path, kind: str, *, snapshot_id: str | None = None, use_latest_approved: bool = False, legacy: bool = False, regenerate_downstream: bool = False, block: str | None = None) -> Path:
    config = CONFIG[kind]
    if legacy:
        raise ValueError("IPOS generation no longer permits legacy or fallback input paths.")
    if regenerate_downstream and not snapshot_id:
        raise ValueError("regenerate_downstream requires snapshot_id")
    if not snapshot_id and not use_latest_approved:
        raise ValueError("Authoritative IPOS generation requires snapshot_id or use_latest_approved.")
    context = json.loads((repo_root / "config" / "project_context.json").read_text(encoding="utf-8"))
    snapshot, selection = resolve_complete_authoritative_input(
        repo_root,
        "6" if kind == "digital" else "7",
        project_id=str(context.get("project_name") or repo_root.name),
        snapshot_id=snapshot_id,
    )
    downstream_contract = resolve_downstream_contract(repo_root, snapshot.snapshot_id)
    coherence = validate_downstream_coherence(repo_root, snapshot.snapshot_id)
    if not regenerate_downstream and coherence["decision"] != "PASS":
        raise RuntimeError(f"Downstream snapshot coherence blocked {kind} IPOS generation: {coherence['finding_count']} findings")
    (repo_root / "artifacts" / "traceability_reports").mkdir(parents=True, exist_ok=True)
    (repo_root / "artifacts" / "traceability_reports" / f"{kind}_ipos_snapshot_selection.json").write_text(
        json.dumps(selection, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    refresh_ledger(repo_root, snapshot_id=snapshot.snapshot_id, source_rows=snapshot.rows)
    source_ids = {
        (row.get("source_req_id") or row.get("id") or "").strip()
        for row in snapshot.rows
        if (row.get("source_req_id") or row.get("id") or "").strip()
    }
    canonical_by_source = {
        (row.get("source_req_id") or row.get("id") or "").strip(): row.get("canonical_id") or row.get("id") or ""
        for row in snapshot.rows
    }
    upstream_rows = _read_csv(repo_root / config["trace"])
    ledger_rows = read_csv(repo_root / "artifacts/traceability_reports/requirement_allocation_ledger.csv")
    source_by_id = {
        (row.get("source_req_id") or row.get("id") or "").strip(): row
        for row in snapshot.rows
        if (row.get("source_req_id") or row.get("id") or "").strip()
    }
    allocation_by_source = {
        str(row.get("source_req_id") or row.get("id") or "").strip(): downstream_contract.allocation(
            str(row.get("source_req_id") or row.get("id") or "").strip()
        )
        for row in snapshot.rows
        if str(row.get("source_req_id") or row.get("id") or "").strip()
    }
    records = []
    block_sequences: dict[str, int] = {}
    emitted_sources: set[str] = set()
    expected_class = BLOCK_LOCAL_DIGITAL if kind == "digital" else BLOCK_LOCAL_ANALOG
    for upstream in upstream_rows:
        upstream_id = (upstream.get(f"{config['upstream'].lower()}_req_id") or "").strip()
        source_id = (upstream.get("source_req_id") or "").strip()
        metadata = allocation_by_source.get(source_id, {})
        if (
            not upstream_id
            or not source_id
            or source_id not in source_ids
            or metadata.get("allocation_class") != expected_class
        ):
            continue
        mapped_block = (metadata.get("approved_block") or "Unassigned").strip()
        block_sequences[mapped_block] = block_sequences.get(mapped_block, 0) + 1
        emitted_sources.add(source_id)
        records.append({
            "ipos_req_id": _ipos_requirement_id(mapped_block, block_sequences[mapped_block]),
            "source_req_id": source_id,
            "canonical_id": canonical_by_source[source_id],
            "covers_upstream_req_id": upstream_id,
            "mapped_block": mapped_block,
            "requirement_statement": (upstream.get("requirement_statement") or "").strip(),
            "snapshot_id": snapshot.snapshot_id,
            "source_artifact": str(snapshot.source_path.relative_to(repo_root)).replace("\\", "/"),
            "allocation_class": metadata.get("allocation_class", ""),
            "owning_target": metadata.get("owning_target", ""),
            "lineage_mode": metadata.get("lineage_mode", ""),
            "source_origin_req_ids": metadata.get("source_origin_req_ids", ""),
            "hierarchy_parent_req_ids": metadata.get("hierarchy_parent_req_ids", ""),
            "owning_domain": metadata.get("owning_domain", ""),
        })

    # A block-local source requirement may legitimately bypass DRS/ARS. The
    # shared ledger is the only authority for this direct allocation decision.
    for ledger in ledger_rows:
        source_id = ledger.get("req_id", "").strip()
        if not source_id or source_id in emitted_sources or ledger.get("hierarchy_or_coverage_class") != expected_class:
            continue
        mapped_block = ledger.get("owning_block", "").strip()
        source = source_by_id.get(source_id, {})
        metadata = allocation_by_source.get(source_id, {})
        if not mapped_block or source_id not in source_ids:
            continue
        block_sequences[mapped_block] = block_sequences.get(mapped_block, 0) + 1
        records.append({
            "ipos_req_id": _ipos_requirement_id(mapped_block, block_sequences[mapped_block]),
            "source_req_id": source_id,
            "canonical_id": canonical_by_source[source_id],
            "covers_upstream_req_id": source_id,
            "mapped_block": mapped_block,
            "requirement_statement": (source.get("requirement_statement") or source.get("statement") or "").strip(),
            "snapshot_id": snapshot.snapshot_id,
            "source_artifact": str(snapshot.source_path.relative_to(repo_root)).replace("\\", "/"),
            "lineage_mode": metadata.get("lineage_mode", ""),
            "allocation_class": metadata.get("allocation_class", ""),
            "owning_target": metadata.get("owning_target", ""),
            "source_origin_req_ids": metadata.get("source_origin_req_ids", ""),
            "hierarchy_parent_req_ids": metadata.get("hierarchy_parent_req_ids", ""),
            "owning_domain": metadata.get("owning_domain", ""),
        })

    output_dir = repo_root / config["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    legacy_root_docx = output_dir / config["docx"]
    if not block and legacy_root_docx.exists():
        legacy_root_docx.unlink()
    block_root = output_dir / "blocks"
    block_root.mkdir(parents=True, exist_ok=True)
    trace_path = output_dir / "ipos_traceability_matrix.csv"
    fields = [
        "ipos_req_id", "source_req_id", "canonical_id", "covers_upstream_req_id",
        "mapped_block", "requirement_statement", "snapshot_id", "source_artifact", "allocation_class",
        "owning_target", "lineage_mode", "source_origin_req_ids", "hierarchy_parent_req_ids", "owning_domain",
    ]
    if not block:
        with trace_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(records)

    mapped_blocks = {
        row["mapped_block"] for row in records if row["mapped_block"] != "Unassigned"
    }
    inventory_blocks = set(_inventory_blocks(repo_root, kind))
    invalid_blocks = sorted(mapped_blocks - inventory_blocks, key=str.casefold)
    if invalid_blocks:
        raise RuntimeError(
            f"{kind.capitalize()} IPOS received block ownership outside the applicable "
            "concrete inventory scope: " + ", ".join(invalid_blocks)
        )
    # Materialize an IPOS document only when the selected snapshot maps at
    # least one approved block-local requirement to its concrete block.
    block_names = sorted(mapped_blocks, key=str.casefold)
    if block:
        selected_block = next((name for name in block_names if _block_slug(name) == _block_slug(block)), None)
        if not selected_block:
            raise RuntimeError(f"Requested IPOS generation block is not materialized by the approved snapshot: {block}")
        block_names = [selected_block]
    else:
        desired_block_dirs = {_block_slug(block_name) for block_name in block_names}
        for existing_dir in block_root.iterdir():
            if existing_dir.is_dir() and existing_dir.name not in desired_block_dirs:
                try:
                    shutil.rmtree(existing_dir)
                except OSError:
                    pass
    for index, block_name in enumerate(block_names, start=1):
        activity = f"Generate IPOS document {index}/{len(block_names)}: {block_name}"
        started_at = datetime.now().astimezone()
        print(
            f"[IPOS_ACTIVITY] START | {started_at.isoformat(timespec='seconds')} | {activity}",
            flush=True,
        )
        outcome = "failed"
        block_rows = [row for row in records if row["mapped_block"] == block_name]
        block_dir = output_dir / "blocks" / _block_slug(block_name)
        legacy_markdown = block_dir / "ipos_requirements_specification.md"
        if legacy_markdown.exists():
            legacy_markdown.unlink()
        block_config = dict(config)
        block_config["docx"] = _block_docx_name(kind, block_name)
        try:
            _write_ipos_document(
                repo_root,
                block_config,
                kind,
                config["title"].format(block_name=block_name),
                block_dir,
                block_name,
                block_rows,
                snapshot.snapshot_id,
                require_docx=not legacy,
                candidate_requirement_rows=approved_snapshot_candidate_rows(snapshot, downstream_contract),
            )
            outcome = "complete"
        finally:
            finished_at = datetime.now().astimezone()
            elapsed = str(finished_at - started_at).split(".", 1)[0]
            print(
                f"[IPOS_ACTIVITY] END | {finished_at.isoformat(timespec='seconds')} | "
                f"{activity} | {outcome} | elapsed={elapsed}",
                flush=True,
            )
    return trace_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic IPOS from an approved Stage 2B snapshot.")
    parser.add_argument("--kind", choices=tuple(CONFIG), required=True)
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--snapshot-id", help="Explicit approved canonical snapshot ID")
    selector.add_argument("--use-latest-approved", action="store_true", help="Explicitly select the latest approved snapshot")
    parser.add_argument("--regenerate-downstream", action="store_true", help="Regenerate from the explicit approved snapshot before coherence validation passes")
    parser.add_argument("--block", help="Regenerate one approved materialized IPOS block without modifying other IPOS artifacts")
    args = parser.parse_args()
    if args.regenerate_downstream and not args.snapshot_id:
        parser.error("--regenerate-downstream requires --snapshot-id")
    print(f"Generated {generate(Path(__file__).resolve().parents[1], args.kind, snapshot_id=args.snapshot_id, use_latest_approved=args.use_latest_approved, regenerate_downstream=args.regenerate_downstream, block=args.block)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
