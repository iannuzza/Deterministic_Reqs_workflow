#!/usr/bin/env python3
"""Validate deterministic IPOS traceability and frozen-snapshot provenance."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

from approved_snapshot_resolver import resolve_complete_authoritative_input
from validate_downstream_coherence import resolve_downstream_contract
from generate_architecture_sysml import model_file_name
from generate_ipos_specs import _block_inventory_record, _block_markdown_name, _inventory_blocks, approved_snapshot_candidate_rows
from workflow_routing import (
    IPOS_LOCAL_ANALOG_TOPIC_SPECS,
    IPOS_LOCAL_DIGITAL_TOPIC_SPECS,
    validate_ipos_docx_layout,
    validate_ipos_descriptive_output,
    validate_spec_internal_links,
    build_ipos_functional_input,
    build_ipos_normalized_records,
)
from spec_document_contract import validate_materialization_chain
from allocation_ledger import read_csv
from requirement_allocation_policy import validate_allocation_rows


CONFIG = {
    "digital": ("6", "IPOS-DIG-REQ", "DRS", "artifacts/stage6_digital_ipos"),
    "analog": ("7", "IPOS-ANA-REQ", "ARS", "artifacts/stage7_analog_ipos"),
}


def _block_slug(block_name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", block_name.casefold()).strip("-")
    return slug or "unnamed-block"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=tuple(CONFIG), required=True)
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--snapshot-id")
    selector.add_argument("--use-latest-approved", action="store_true")
    parser.add_argument("--block", help="Validate descriptive materialization for one approved block only")
    args = parser.parse_args()
    stage, _prefix, upstream_name, output_dir = CONFIG[args.kind]
    topic_specs = IPOS_LOCAL_DIGITAL_TOPIC_SPECS if args.kind == "digital" else IPOS_LOCAL_ANALOG_TOPIC_SPECS
    root = Path(__file__).resolve().parents[1]
    try:
        context = json.loads((root / "config/project_context.json").read_text(encoding="utf-8"))
        snapshot, selection = resolve_complete_authoritative_input(
            root,
            stage,
            project_id=str(context.get("project_name") or root.name),
            snapshot_id=args.snapshot_id,
        )
        if not selection.get("selected_snapshot_id"):
            raise RuntimeError("Complete selector returned no selected snapshot ID.")
        trace_path = root / output_dir / "ipos_traceability_matrix.csv"
        if not trace_path.exists():
            raise RuntimeError("IPOS aggregate traceability artifact is missing.")
        with trace_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        block_root = root / output_dir / "blocks"
        block_dirs = sorted(path for path in block_root.iterdir() if path.is_dir()) if block_root.exists() else []
        mapped_block_names = {
            row.get("mapped_block", "").strip()
            for row in rows
            if row.get("mapped_block", "").strip()
            and row.get("mapped_block", "").strip() != "Unassigned"
        }
        inventory_blocks = set(_inventory_blocks(root, args.kind))
        invalid_mapped_blocks = sorted(mapped_block_names - inventory_blocks, key=str.casefold)
        if invalid_mapped_blocks:
            raise RuntimeError(
                f"{args.kind.capitalize()} IPOS traceability maps requirements outside the applicable "
                "concrete inventory scope: " + ", ".join(invalid_mapped_blocks)
            )
        expected_blocks = {_block_slug(name) for name in mapped_block_names}
        actual_blocks = {path.name for path in block_dirs}
        missing_blocks = sorted(expected_blocks - actual_blocks)
        unexpected_blocks = sorted(actual_blocks - expected_blocks)
        if missing_blocks:
            raise RuntimeError(
                f"{args.kind.capitalize()} IPOS block output directories are missing: "
                + ", ".join(missing_blocks)
            )
        if unexpected_blocks:
            raise RuntimeError(
                f"{args.kind.capitalize()} IPOS contains directories outside block_inventory.csv: "
                + ", ".join(unexpected_blocks)
            )
        sysml_root = root / "artifacts/stage2_mirco_arc/sysml/blocks"
        missing_sysml = sorted(
            model_file_name(name)
            for name in mapped_block_names
            if not (sysml_root / model_file_name(name)).is_file()
        )
        if missing_sysml:
            raise RuntimeError(
                f"{args.kind.capitalize()} IPOS is missing corresponding SysML block models: "
                + ", ".join(missing_sysml)
            )
        validation_block_dirs = block_dirs
        if args.block:
            selected_block = next(
                (name for name in _inventory_blocks(root, args.kind) if _block_slug(name) == _block_slug(args.block)),
                None,
            )
            if not selected_block:
                raise RuntimeError(f"Requested IPOS validation block is not approved in block_inventory.csv: {args.block}")
            validation_block_dirs = [path for path in block_dirs if path.name == _block_slug(selected_block)]
            if not validation_block_dirs:
                raise RuntimeError(f"Requested IPOS validation block is not materialized: {selected_block}")
        for block_dir in validation_block_dirs:
            concrete_block = next(
                (name for name in _inventory_blocks(root, args.kind) if _block_slug(name) == block_dir.name),
                block_dir.name,
            )
            markdown_path = block_dir / _block_markdown_name(args.kind, concrete_block)
            docx_path = block_dir / f"{args.kind}_ipos_{_block_slug(concrete_block)}.docx"
            if not markdown_path.exists() or not docx_path.exists():
                raise RuntimeError(f"{args.kind.capitalize()} IPOS artifacts are missing for block directory: {block_dir.name}")
            link_findings = validate_spec_internal_links(markdown_path, docx_path)
            if link_findings:
                raise RuntimeError("IPOS internal-link findings: " + "; ".join(link_findings[:10]))
            layout_findings = validate_ipos_docx_layout(docx_path)
            if layout_findings:
                raise RuntimeError("IPOS shared-layout findings: " + "; ".join(layout_findings[:10]))
            functional_input = build_ipos_functional_input(
                concrete_block,
                _block_inventory_record(root, concrete_block),
                [row for row in rows if row.get("mapped_block") == concrete_block],
                domain=args.kind,
                materialized=True,
                provenance=("approved snapshot", "artifacts/stage2_mirco_arc/block_inventory.csv"),
                candidate_requirement_rows=approved_snapshot_candidate_rows(snapshot, resolve_downstream_contract(root, snapshot.snapshot_id)),
            )
            descriptive_findings = validate_ipos_descriptive_output(
                markdown_path,
                block_dir / "descriptive_summary_audit.csv",
                concrete_block,
                [row.get("requirement_statement", "") for row in rows if row.get("mapped_block") == concrete_block],
                [row.get("source_req_id", "") for row in rows if row.get("mapped_block") == concrete_block],
                topic_specs,
                functional_input,
            )
            descriptive_findings.extend(validate_materialization_chain(
                block_dir / "materialization_audit.json",
                "IPOS",
                build_ipos_normalized_records(functional_input),
                markdown_path,
                docx_path,
            ))
            if descriptive_findings:
                raise RuntimeError("IPOS descriptive-output findings: " + "; ".join(descriptive_findings[:10]))
        if any(row.get("snapshot_id") != snapshot.snapshot_id for row in rows):
            raise RuntimeError("IPOS traceability contains a stale snapshot ID.")
        if any(not row.get("covers_upstream_req_id") for row in rows):
            raise RuntimeError(f"IPOS rows missing {upstream_name} Covers links.")
        ledger_path = root / "artifacts/traceability_reports/requirement_allocation_ledger.csv"
        if not ledger_path.exists():
            raise RuntimeError("Central allocation ledger is missing.")
        ledger_rows = read_csv(ledger_path)
        if any(row.get("snapshot_id") != snapshot.snapshot_id for row in ledger_rows):
            raise RuntimeError("Central allocation ledger is tied to a different snapshot.")
        findings = validate_allocation_rows(ledger_rows)
        if findings:
            raise RuntimeError("Central allocation policy findings: " + "; ".join(findings[:10]))
    except Exception as exc:
        print(f"IPOS {args.kind} gate: FAIL: {exc}")
        return 1
    validated_scope = f", descriptive block={selected_block}" if args.block else ""
    print(f"IPOS {args.kind} gate: PASS ({len(rows)} requirements, {len(expected_blocks)} blocks{validated_scope})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
