#!/usr/bin/env python3
"""Repeatable, read-only pre-freeze coherence and warning-triage gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


WARNING_CLASSES = {
    "INFO_ONLY",
    "HARDEN_LATER",
    "BLOCK_BEFORE_PHASE2",
    "BLOCK_BEFORE_STAGE2B_FREEZE",
    "BLOCK_BEFORE_DOWNSTREAM",
}


def authority_paths(repo_root: Path) -> list[Path]:
    return [
        repo_root / "artifacts/source_ingestion",
        repo_root / "artifacts/stage1_specs/architecture_mapping_preview.csv",
        repo_root / "artifacts/stage1_specs/architecture_mapping_preview.xlsx",
        repo_root / "config/stage2_mirco_arc_profile.json",
        repo_root / "data/canonical/canonical_store.sqlite",
    ]


def authority_fingerprint(repo_root: Path) -> str:
    digest = hashlib.sha256()
    for path in authority_paths(repo_root):
        if path.is_dir():
            entries = sorted(item for item in path.rglob("*") if item.is_file())
            for entry in entries:
                digest.update(entry.relative_to(repo_root).as_posix().encode())
                digest.update(entry.read_bytes())
        elif path.exists():
            digest.update(path.relative_to(repo_root).as_posix().encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def classify_warning(finding: dict[str, Any], historical_paths: set[str] | None = None) -> str:
    category = str(finding.get("category") or "")
    message = str(finding.get("message") or "").casefold()
    if category == "hierarchical_placement" and (
        "hierarchy_parent_req_ids" in message or "hierarchy-parent" in message
    ):
        return "BLOCK_BEFORE_STAGE2B_FREEZE"
    if category == "stale_state" and "approved snapshot" in message:
        return "BLOCK_BEFORE_STAGE2B_FREEZE"
    if category in {"id_chain", "revision", "merge_readiness", "canonical"}:
        return "BLOCK_BEFORE_PHASE2"
    if category in {"stage2b"}:
        return "BLOCK_BEFORE_STAGE2B_FREEZE"
    if category in {"stage2a"}:
        return "BLOCK_BEFORE_DOWNSTREAM"
    if category == "stale_state" and str(finding.get("path") or "") in (historical_paths or set()):
        return "INFO_ONLY"
    if category == "stale_state" and str(finding.get("severity") or "") == "INFO" and "historical" in message:
        return "INFO_ONLY"
    if category == "stale_state":
        return "HARDEN_LATER"
    return "INFO_ONLY"


def warning_analysis(finding: dict[str, Any]) -> dict[str, str]:
    """Return root cause and only safe automatic action for one warning."""
    category = str(finding.get("category") or "")
    message = str(finding.get("message") or "")
    if category == "stale_state" and "approved snapshot" in message.casefold():
        return {"root_cause": "stale approved snapshot authority", "automatic_action": "quarantine_snapshot"}
    if category == "hierarchical_placement":
        return {"root_cause": "lower-level hierarchy authority remains unresolved after approved-lineage candidate remediation", "automatic_action": "stop_at_approval_boundary"}
    return {"root_cause": "requires deterministic review", "automatic_action": "no_automatic_change"}


def gate_decision(classes: list[str], *, phase1_pass: bool, fingerprint_matches: bool) -> str:
    if not phase1_pass or not fingerprint_matches:
        return "STOP_BEFORE_PHASE2"
    if "BLOCK_BEFORE_PHASE2" in classes:
        return "STOP_BEFORE_PHASE2"
    if "BLOCK_BEFORE_STAGE2B_FREEZE" in classes:
        return "STOP_BEFORE_STAGE2B_FREEZE"
    if "BLOCK_BEFORE_DOWNSTREAM" in classes:
        return "GO_ON_WITH_DOWNSTREAM_BLOCKERS"
    return "GO_ON"


def evaluate(repo_root: Path, phase1_report_path: Path) -> dict[str, Any]:
    report = json.loads(phase1_report_path.read_text(encoding="utf-8")) if phase1_report_path.exists() else {}
    current_fingerprint = authority_fingerprint(repo_root)
    recorded_fingerprint = str(report.get("authority_fingerprint") or "")
    phase1_pass = report.get("result") == "PASS" and int(report.get("counts", {}).get("ERROR", 1)) == 0
    fingerprint_matches = bool(recorded_fingerprint) and recorded_fingerprint == current_fingerprint
    warnings = [
        item for item in report.get("findings", [])
        if item.get("severity") == "WARNING"
        or (item.get("severity") == "INFO" and item.get("category") == "stale_state")
    ]
    remediation_path = repo_root / "artifacts/validation/pre_freeze_warning_remediation.json"
    remediation = json.loads(remediation_path.read_text(encoding="utf-8")) if remediation_path.exists() else {}
    cleanup = remediation.get("historical_warning_cleanup", {})
    historical_paths = {
        path
        for group in cleanup.get("groups", [])
        for path in group.get("paths", [])
    }
    classified = [{**item, "triage_class": classify_warning(item, historical_paths), **warning_analysis(item)} for item in warnings]
    classes = [item["triage_class"] for item in classified]
    decision = gate_decision(classes, phase1_pass=phase1_pass, fingerprint_matches=fingerprint_matches)
    counts = {name: sum(item["triage_class"] == name for item in classified) for name in sorted(WARNING_CLASSES)}
    return {
        "gate": "pre_freeze_coherence_gate",
        "mode": "read_only_local_deterministic",
        "phase1_report": str(phase1_report_path),
        "phase1_pass": phase1_pass,
        "authority_fingerprint": current_fingerprint,
        "recorded_authority_fingerprint": recorded_fingerprint,
        "authority_fingerprint_matches": fingerprint_matches,
        "warning_counts": counts,
        "classified_warnings": classified,
        "remediation_exhausted": bool(remediation.get("remediation_exhausted")),
        "auto_resolved_hierarchy_parent_count": int(remediation.get("auto_resolved_count", 0)),
        "csv_authority_crosscheck": remediation.get("csv_authority_crosscheck", {}),
        "historical_warning_cleanup": cleanup,
        "suppressed_top_level_parent_warning_count": int(
            remediation.get("csv_authority_crosscheck", {}).get("counts", {}).get(
                "TOP_LEVEL_PARENT_WARNING_SUPPRESSED", 0
            )
        ),
        "decision": decision,
        "freeze_allowed": decision == "GO_ON",
        "downstream_allowed": decision == "GO_ON",
        "repeatable_after_authority_change": True,
        "next_step": "Resolve freeze blockers and rerun Phase 1 plus this gate." if decision != "GO_ON" else "Proceed only through the separately approved freeze boundary.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the read-only pre-freeze warning-triage gate")
    parser.add_argument("--phase1-report", default="artifacts/validation/source_to_stage2b_coherence.json")
    parser.add_argument("--report", default="artifacts/validation/pre_freeze_coherence_gate.json")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    phase1_path = repo_root / args.phase1_report
    result = evaluate(repo_root, phase1_path)
    report_path = repo_root / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Pre-freeze coherence gate: {result['decision']}")
    print(f"authority_fingerprint_matches={result['authority_fingerprint_matches']}")
    print(json.dumps(result["warning_counts"], sort_keys=True))
    return 0 if result["decision"] == "GO_ON" else 1


if __name__ == "__main__":
    raise SystemExit(main())
