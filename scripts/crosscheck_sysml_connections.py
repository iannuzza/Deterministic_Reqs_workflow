#!/usr/bin/env python3
"""Crosscheck generated SysML block connections against Stage 2 source artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path

from generate_architecture_sysml import (
    block_name,
    model_file_name,
    read_csv,
    subsystem_for_block,
    sysml_name,
    usage_name,
)


def _top_path(block: str) -> str:
    if subsystem_for_block(block) == "Digital Subsystem":
        return f"topDigital.{usage_name(block)}"
    return f"topAnalog.{usage_name(subsystem_for_block(block))}.{usage_name(block)}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Crosscheck generated SysML block connections")
    parser.add_argument("--model", default="artifacts/stage2_mirco_arc/sysml/STBIOSystem.sysml")
    parser.add_argument("--blocks", default="artifacts/stage2_mirco_arc/sysml/blocks")
    parser.add_argument("--digital-subsystem", default="artifacts/stage2_mirco_arc/sysml/DigitalSubsystem.sysml")
    parser.add_argument("--interactions", default="artifacts/stage2_mirco_arc/interaction_matrix.csv")
    parser.add_argument("--source-edges", default="artifacts/stage1_requirements/source_matrix_edges.csv")
    parser.add_argument("--output", default="artifacts/stage2_mirco_arc/sysml_connection_crosscheck_report.md")
    args = parser.parse_args()

    model_path = Path(args.model)
    block_dir = Path(args.blocks)
    model = model_path.read_text(encoding="utf-8")
    interactions = read_csv(Path(args.interactions))
    source_edges = read_csv(Path(args.source_edges))
    source_edge_ids = {row.get("source_req_id", "") for row in source_edges}

    generated_block_names = {
        block_name(name)
        for row in interactions
        for name in (row.get("From block", ""), row.get("To block", ""))
        if (block_dir / model_file_name(block_name(name))).exists()
    }
    block_names = set()
    for row in interactions:
        block_names.add(block_name(row.get("From block", "")))
        block_names.add(block_name(row.get("To block", "")))
    block_names = {name for name in block_names if name in generated_block_names}

    missing_files = [
        block
        for block in sorted(block_names)
        if not (block_dir / model_file_name(block)).exists()
    ]
    connections_missing_from_top = []
    source_edge_mismatches = []
    matched_source_edges = 0
    interaction_ids = set()
    for row in interactions:
        source = block_name(row.get("From block", ""))
        target = block_name(row.get("To block", ""))
        if source not in block_names or target not in block_names:
            continue
        expected = f"connect {_top_path(source)} to {_top_path(target)}"
        if expected not in model:
            connections_missing_from_top.append(f"{source} -> {target}")
        for requirement_id in row.get("Requirement IDs", "").split(";"):
            requirement_id = requirement_id.strip()
            if requirement_id:
                interaction_ids.add(requirement_id)

    for row in source_edges:
        requirement_id = row.get("source_req_id", "")
        source = block_name(row.get("from_block", ""))
        target = block_name(row.get("to_block", ""))
        if source not in block_names or target not in block_names:
            continue
        expected = f"connect {_top_path(source)} to {_top_path(target)}"
        if (
            requirement_id not in interaction_ids
            or source not in block_names
            or target not in block_names
            or expected not in model
        ):
            source_edge_mismatches.append(f"{requirement_id}: {source} -> {target}")
        else:
            matched_source_edges += 1

    digital_path = Path(args.digital_subsystem)
    digital_model = digital_path.read_text(encoding="utf-8") if digital_path.exists() else ""
    digital_blocks = [
        block for block in sorted(block_names)
        if subsystem_for_block(block) == "Digital Subsystem"
    ]
    missing_from_digital = [
        block for block in digital_blocks
        if f"part {usage_name(block)} : {sysml_name(block)};" not in digital_model
    ]

    status = not missing_files and not connections_missing_from_top and not source_edge_mismatches and not missing_from_digital
    report_lines = [
        "# SysML Block Connection Crosscheck Report",
        "",
        f"- Status: {'PASS' if status else 'FAIL'}",
        f"- Model: {model_path.as_posix()}",
        "",
        "## Block File Coverage",
        "",
        f"- Interaction endpoint blocks: {len(block_names)}",
        f"- Missing block files: {', '.join(missing_files) if missing_files else 'None'}",
        f"- Digital hierarchy file: {digital_path.as_posix()}",
        f"- Digital hierarchy members checked: {len(digital_blocks)}",
        f"- Missing digital hierarchy members: {', '.join(missing_from_digital) if missing_from_digital else 'None'}",
        "",
        "## Connection Coverage",
        "",
        f"- Interaction matrix connections: {len(interactions)}",
        f"- Connections missing from hierarchical top: {', '.join(connections_missing_from_top) if connections_missing_from_top else 'None'}",
        f"- Source XBAR edges matched: {matched_source_edges} of {len(source_edges)}",
        f"- Source edge mismatches: {', '.join(source_edge_mismatches) if source_edge_mismatches else 'None'}",
        "",
        "## Conclusion",
        "",
        "- Every interaction endpoint has a generated block file and every source connection is represented in the hierarchical SysML top." if status else "- One or more generated SysML block or connection checks failed; see the findings above.",
        "",
    ]
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"SysML connection crosscheck: {'PASS' if status else 'FAIL'}")
    print(f"Report: {output_path.as_posix()}")
    return 0 if status else 1


if __name__ == "__main__":
    raise SystemExit(main())