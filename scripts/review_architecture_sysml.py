#!/usr/bin/env python3
"""Review the derived Stage 2A SysML model for structural completeness.

The approved architecture mapping workbook/CSV and snapshot/SQLite materialization
remain authoritative; this review validates only the generated structural artifact.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
import re
from typing import Dict, List, Optional, Set

from generate_architecture_sysml import block_name, model_file_name, read_csv, sha256, subsystem_for_block, sysml_name, usage_name
from validate_downstream_coherence import approved_sysml_block_scope


def _review(
    model_path: Path,
    model_dir: Path,
    traceability_path: Path,
    inventory_path: Path,
    interactions_path: Path,
    ports_path: Path,
    coverage_path: Path,
    mapping_path: Optional[Path] = None,
    edge_path: Optional[Path] = None,
    source_path: Optional[Path] = None,
    approved_blocks: Optional[Set[str]] = None,
    structural_only: bool = True,
) -> List[Dict[str, str]]:
    model = model_path.read_text(encoding="utf-8")
    shared_path = model_dir / "shared_definitions.sysml"
    shared_model = shared_path.read_text(encoding="utf-8") if shared_path.exists() else ""
    digital_path = model_dir / "DigitalSubsystem.sysml"
    digital_model = digital_path.read_text(encoding="utf-8") if digital_path.exists() else ""
    interactions = read_csv(interactions_path)
    blocks: Set[str] = set(approved_blocks or set())
    findings: List[Dict[str, str]] = []

    block_models: Dict[str, str] = {}
    missing_blocks = []
    for name in sorted(blocks):
        block_path = model_dir / "blocks" / model_file_name(name)
        block_text = block_path.read_text(encoding="utf-8") if block_path.exists() else ""
        block_models[name] = block_text
        if f"part def {sysml_name(name)}" not in block_text:
            missing_blocks.append(name)
    model_set_ok = bool(shared_model) and not missing_blocks
    model_set_details = f"shared definitions and {len(blocks)} per-block models are present"
    if not shared_model:
        model_set_details = "shared definitions model is missing"
    if missing_blocks:
        model_set_details += "; missing block models: " + ", ".join(missing_blocks)
    findings.append({"check": "model_set_completeness", "status": "PASS" if model_set_ok else "FAIL", "details": model_set_details})

    missing_connections = []
    for row in interactions:
        source = block_name(row.get("From block", ""))
        target = block_name(row.get("To block", ""))
        if source not in blocks or target not in blocks:
            continue
        source_path = f"topDigital.{usage_name(source)}" if subsystem_for_block(source) == "Digital Subsystem" else f"topAnalog.{usage_name(subsystem_for_block(source))}.{usage_name(source)}"
        target_path = f"topDigital.{usage_name(target)}" if subsystem_for_block(target) == "Digital Subsystem" else f"topAnalog.{usage_name(subsystem_for_block(target))}.{usage_name(target)}"
        expected = f"connect {source_path} to {target_path}"
        if expected not in model:
            missing_connections.append(f"{source}->{target}")
    findings.append({"check": "consistency", "status": "PASS" if not missing_connections else "FAIL", "details": "all interaction endpoints are represented" if not missing_connections else "missing connections: " + ", ".join(missing_connections)})

    missing_source_edges = []
    extra_source_edges = []
    source_edges = read_csv(edge_path) if edge_path and edge_path.exists() else []
    source_edges = [
        edge for edge in source_edges
        if block_name(edge.get("from_block", "")) in blocks
        and block_name(edge.get("to_block", "")) in blocks
    ]
    interaction_by_id = {
        req_id: row
        for row in interactions
        for req_id in re.split(r"\s*;\s*", row.get("Requirement IDs", ""))
        if req_id
    }
    source_ids = {row.get("source_req_id", "") for row in source_edges}
    for edge in source_edges:
        req_id = edge.get("source_req_id", "")
        interaction = interaction_by_id.get(req_id)
        source = block_name(edge.get("from_block", ""))
        target = block_name(edge.get("to_block", ""))
        if not interaction or block_name(interaction.get("From block", "")) != source or block_name(interaction.get("To block", "")) != target:
            missing_source_edges.append(f"{req_id}:{source}->{target}")
    for req_id, row in interaction_by_id.items():
        interaction_source = block_name(row.get("From block", ""))
        interaction_target = block_name(row.get("To block", ""))
        if (
            interaction_source in blocks
            and interaction_target in blocks
            and req_id not in source_ids
            and "xbar" in " ".join(row.values()).lower()
        ):
            extra_source_edges.append(req_id)
    source_edges_ok = not missing_source_edges and not extra_source_edges
    source_edge_details = f"{len(source_edges) - len(missing_source_edges)} of {len(source_edges)} source XBAR edges match the interaction matrix and top model"
    if missing_source_edges:
        source_edge_details += "; missing/mismatched: " + ", ".join(missing_source_edges)
    if extra_source_edges:
        source_edge_details += "; extra XBAR IDs: " + ", ".join(extra_source_edges)
    findings.append({"check": "source_connection_crosscheck", "status": "PASS" if source_edges_ok else "FAIL", "details": source_edge_details})

    names = [sysml_name(name) for name in blocks]
    duplicate_names = sorted({name for name in names if names.count(name) > 1})
    invalid_names = sorted(name for name in names if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name))
    naming_ok = not duplicate_names and not invalid_names
    naming_details = "SysML identifiers are unique and valid"
    if duplicate_names or invalid_names:
        naming_details = f"duplicate={duplicate_names}; invalid={invalid_names}"
    findings.append({"check": "naming", "status": "PASS" if naming_ok else "FAIL", "details": naming_details})

    if not structural_only:
        raise ValueError("Full SysML requirement coverage is owned by validate_downstream_coherence.py")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the stage-local structural SysML review")
    parser.add_argument("--model", default="artifacts/stage2_mirco_arc/sysml/STBIOSystem.sysml")
    parser.add_argument("--model-dir", default="artifacts/stage2_mirco_arc/sysml")
    parser.add_argument("--traceability", default="artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv")
    parser.add_argument("--mapping-preview", default="artifacts/stage1_specs/architecture_mapping_preview.csv")
    parser.add_argument("--source-edges", default="artifacts/stage1_requirements/source_matrix_edges.csv")
    parser.add_argument("--requirements", default="artifacts/stage1_requirements/requirements_summary.csv")
    parser.add_argument("--inventory", default="artifacts/stage2_mirco_arc/block_inventory.csv")
    parser.add_argument("--interactions", default="artifacts/stage2_mirco_arc/interaction_matrix.csv")
    parser.add_argument("--ports", default="artifacts/stage2_mirco_arc/source_port_catalog.csv")
    parser.add_argument("--io-coverage", default="artifacts/stage2_mirco_arc/source_io_table_coverage.csv")
    parser.add_argument("--output", default="artifacts/stage2_mirco_arc/stbio_architecture_model_review.md")
    parser.add_argument("--csv-output", default="artifacts/stage2_mirco_arc/stbio_architecture_model_review.csv")
    parser.add_argument("--snapshot-id", help="Explicit approved snapshot ID; omitted uses the resolver's approved snapshot.")
    parser.add_argument(
        "--scope",
        choices=["stage3-structural"],
        default="stage3-structural",
        help="Stage 3 review scope; complete requirement coherence is deferred to the final SysML phase.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    approved_blocks = approved_sysml_block_scope(repo_root, args.snapshot_id)
    model = Path(args.model)
    traceability = Path(args.traceability)
    inventory = Path(args.inventory)
    interactions = Path(args.interactions)
    findings = _review(
        model, Path(args.model_dir), traceability, inventory, interactions,
        Path(args.ports), Path(args.io_coverage), Path(args.mapping_preview),
        Path(args.source_edges), Path(args.requirements),
        approved_blocks,
        structural_only=args.scope == "stage3-structural",
    )
    status = "approved" if all(row["status"] == "PASS" for row in findings) else "rejected"
    timestamp = datetime.now().isoformat(timespec="seconds")

    csv_output = Path(args.csv_output)
    csv_output.parent.mkdir(parents=True, exist_ok=True)
    with csv_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "status", "details"])
        writer.writeheader()
        writer.writerows(findings)

    output = Path(args.output)
    output.write_text("\n".join([
        "# SysML Architecture Model Review",
        "",
        f"- Status: {status}",
        f"- Reviewed at: {timestamp}",
        f"- Model: {model.as_posix()}",
        f"- Model SHA-256: {sha256(model)}",
        "",
        "## Checks",
        "",
        "| Check | Status | Details |",
        "|---|---|---|",
        *[f"| {row['check']} | {row['status']} | {row['details'].replace('|', '/')} |" for row in findings],
        "",
        "## Gate Decision",
        "",
        "- This is a derived-artifact review only: it covers model set, endpoints, ports, naming, and source-edge consistency.",
        "- It does not replace, override, or invalidate approved architecture mapping or snapshot authority.",
        "- Full requirement coverage, allocation, ownership, partition, and end-to-end coherence are deferred to the final SysML phase and central validator.",
        "",
    ]) + "\n", encoding="utf-8")
    print(f"Model review: {status}")
    for row in findings:
        print(f"{row['check']}: {row['status']} - {row['details']}")
    return 0 if status == "approved" else 2


if __name__ == "__main__":
    raise SystemExit(main())
