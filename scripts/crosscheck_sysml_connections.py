#!/usr/bin/env python3
"""Crosscheck generated SysML block connections against Stage 2 source artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_downstream_coherence import resolve_sysml_materialization_scope
from sysml_relations import validate_serialized_relations


def main() -> int:
    parser = argparse.ArgumentParser(description="Crosscheck all three SysML relation classes through the central contract")
    parser.add_argument("--snapshot-id", required=True)
    parser.add_argument("--model")
    parser.add_argument("--blocks")
    parser.add_argument("--digital-subsystem")
    parser.add_argument("--interactions")
    parser.add_argument("--source-edges")
    parser.add_argument("--output", default="artifacts/stage2_mirco_arc/sysml_connection_crosscheck_report.md")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    scope = resolve_sysml_materialization_scope(root, args.snapshot_id).require_valid()
    for address, expected in ((args.model, scope.system_path), (args.blocks, scope.system_path.parent / "blocks"),
                              (args.digital_subsystem, scope.digital_path),
                              (args.interactions, root / "artifacts/stage2_mirco_arc/interaction_matrix.csv"),
                              (args.source_edges, root / "artifacts/stage1_requirements/source_matrix_edges.csv")):
        if address and Path(address).resolve() != expected.resolve():
            raise ValueError("SYSML_RELATION_CROSSCHECK_ADDRESS_MISMATCH")
    report = validate_serialized_relations(scope, scope.relation_inventory)
    status = "FAIL" if report["findings"] else "PASS"
    lines = ["# Central SysML Relation Crosscheck", "", "Snapshot: " + scope.snapshot_id,
             "Serialization integrity: " + status,
             "Resolved representation parity is not a complete-connectivity claim.", "",
             "## Per-View Coverage", "", "```json", json.dumps(report["views"], indent=2), "```", "",
             "## Integrity Findings", "", *("- " + value for value in report["findings"]), "",
             "## Central Gaps", "", "```json", json.dumps(report["gaps"], indent=2), "```", ""]
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print("SysML relation crosscheck: " + status + "; central gaps: " + str(len(report["gaps"])))
    print("Report: " + output.as_posix())
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())