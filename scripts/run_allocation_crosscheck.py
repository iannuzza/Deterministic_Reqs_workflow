"""Final deterministic allocation and downward-coverage crosscheck."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from allocation_ledger import read_csv
from approved_snapshot_resolver import resolve_complete_authoritative_input
from requirement_allocation_policy import accounting_status, validate_allocation_rows, write_allocation_ledger

MATRICES = {
    "SRS": "artifacts/stage3_srs/srs_traceability_matrix.csv",
    "DRS": "artifacts/stage5_drs/drs_traceability_matrix.csv",
    "ARS": "artifacts/stage4_ars/ars_traceability_matrix.csv",
    "Digital IPOS": "artifacts/stage6_digital_ipos/ipos_traceability_matrix.csv",
    "Analog IPOS": "artifacts/stage7_analog_ipos/ipos_traceability_matrix.csv",
}


def validate_materialization_manifest(manifest: dict, rows: list[dict[str, str]]) -> None:
    """Validate that a ledger manifest proves the rows belong to this run."""
    if not manifest.get("materialized"):
        raise RuntimeError("Allocation ledger materialization is not marked complete.")
    selection = manifest.get("selection") or {}
    selected_snapshot_id = str(selection.get("selected_snapshot_id") or "")
    if not selected_snapshot_id:
        raise RuntimeError("Allocation materialization has no selected authoritative snapshot.")
    accepted = {
        str(item.get("snapshot_id"))
        for item in selection.get("attempted_snapshots", [])
        if item.get("accepted")
    }
    if selected_snapshot_id not in accepted:
        raise RuntimeError("Allocation materialization selected snapshot is not recorded as accepted.")
    if not rows:
        raise RuntimeError("Allocation crosscheck cannot pass with zero ledger rows.")
    if int(manifest.get("row_count", -1)) != len(rows):
        raise RuntimeError("Allocation materialization row count does not match the ledger.")
    if any(row.get("snapshot_id") != selected_snapshot_id for row in rows):
        raise RuntimeError("Allocation ledger rows do not match the selected authoritative snapshot.")


def _actual_targets(rows: list[dict[str, str]]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for row in rows:
        req_id = (row.get("req_id") or "").strip()
        targets = {value.strip() for value in (row.get("actual_downstream_targets") or "").split(";") if value.strip()}
        if req_id:
            result[req_id] = targets
    return result


def run(repo_root: Path) -> tuple[Path, Path]:
    ledger_path = repo_root / "artifacts/traceability_reports/requirement_allocation_ledger.csv"
    manifest_path = repo_root / "artifacts/traceability_reports/requirement_allocation_materialization.json"
    if not manifest_path.exists():
        raise RuntimeError("Allocation crosscheck requires a ledger materialization manifest.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = read_csv(ledger_path)
    validate_materialization_manifest(manifest, rows)
    selected_snapshot_id = str((manifest.get("selection") or {}).get("selected_snapshot_id"))
    context_path = repo_root / "config/project_context.json"
    context = json.loads(context_path.read_text(encoding="utf-8")) if context_path.exists() else {}
    resolved, _selection = resolve_complete_authoritative_input(
        repo_root,
        "crosscheck",
        project_id=str(context.get("project_name") or repo_root.name),
        snapshot_id=selected_snapshot_id,
    )
    if resolved.snapshot_id != selected_snapshot_id:
        raise RuntimeError("Crosscheck resolver returned a different snapshot than the materialization manifest.")
    actual = _actual_targets(rows)
    for row in rows:
        targets = actual.get(row.get("req_id", ""), set())
        row["actual_downstream_targets"] = ";".join(sorted(targets))
        row["coverage_status"] = accounting_status(row.get("hierarchy_or_coverage_class", ""), targets)
        rendered = sorted(targets)
        row["rendered_in_specs"] = ";".join(rendered)
        if row.get("lineage_mode") == "normal_hierarchical":
            if row.get("source_type") == "supplementary" and any("IPOS" in target for target in targets):
                row["lineage_mode"] = "direct_supplementary_to_ipos"
            elif any("IPOS" in target for target in targets) and not any(target in targets for target in ("DRS", "ARS")):
                row["lineage_mode"] = "direct_source_to_ipos"
    findings = validate_allocation_rows(rows)
    report_dir = repo_root / "artifacts/traceability_reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    write_allocation_ledger(ledger_path, rows)
    summary = {
        "approved_primary_requirements": sum(row.get("source_type") == "primary" for row in rows),
        "approved_supplementary_requirements": sum(row.get("source_type") == "supplementary" for row in rows),
        "by_class": dict(Counter(row.get("hierarchy_or_coverage_class", "") for row in rows)),
        "by_topic_family": dict(Counter(row.get("topic_family", "") for row in rows)),
        "by_scope": dict(Counter(row.get("scope", "") for row in rows)),
        "by_block": dict(Counter(row.get("owning_block", "") or "Unassigned" for row in rows)),
        "by_domain": dict(Counter(row.get("owning_domain", "") for row in rows)),
        "by_coverage_status": dict(Counter(row.get("coverage_status", "") for row in rows)),
        "by_lineage_mode": dict(Counter(row.get("lineage_mode", "") for row in rows)),
        "required_target_counts": dict(Counter(row.get("required_downstream_targets", "") for row in rows)),
        "actual_target_counts": dict(Counter(row.get("actual_downstream_targets", "") for row in rows)),
        "findings": findings,
        "row_count": len(rows),
        "materialization": manifest,
    }
    json_path = report_dir / "allocation_crosscheck_report.json"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    md_path = report_dir / "allocation_crosscheck_report.md"
    lines = ["# Allocation Crosscheck Report", "", "## Summary", ""]
    for key, value in summary.items():
        if isinstance(value, dict):
            lines.append(f"- {key}: {json.dumps(value, sort_keys=True)}")
        elif key != "findings":
            lines.append(f"- {key}: {value}")
    lines.extend(["", "## Findings", ""])
    lines.extend(f"- {finding}" for finding in findings) if findings else lines.append("- None")
    lines.extend(["", "## Associations", "", "- Source requirement -> rendered descendants, immediate parents, source origins, target sets, and owners are available in `requirement_allocation_ledger.csv`."])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    outputs = run(root)
    print("\n".join(str(path) for path in outputs))
