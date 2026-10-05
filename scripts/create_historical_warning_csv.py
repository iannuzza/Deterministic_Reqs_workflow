#!/usr/bin/env python3
"""Export historical pre-S2B warning details to a diagnostic CSV."""

from __future__ import annotations

import csv
import json
from pathlib import Path


FIELDS = [
    "severity",
    "phase1_severity",
    "category",
    "warning_scope",
    "warning_explanation",
    "why_phase1_warning",
    "missing_context_in_original_finding",
    "message",
    "path",
    "historical_batch_id",
    "historical_batch_timestamp",
    "source_spec",
    "source_kind",
    "source_req_ids",
    "source_req_id_note",
    "active_batch_path",
    "current_authority_effect",
    "future_validation_effect",
    "root_cause",
    "cleanup_action",
    "status",
    "workflow_triage",
]


def source_req_ids(batch_path: Path) -> str:
    requirements_path = batch_path / "normalized_requirements.csv"
    if not requirements_path.is_file():
        return ""
    with requirements_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        identifiers = sorted({
            str(row.get("source_req_id") or "").strip()
            for row in reader
            if str(row.get("source_req_id") or "").strip()
        })
    return ";".join(identifiers)


def create(repo_root: Path) -> Path:
    phase1_path = repo_root / "artifacts/validation/source_to_stage2b_coherence.json"
    remediation_path = repo_root / "artifacts/validation/pre_freeze_warning_remediation.json"
    output_path = repo_root / "artifacts/stage1_specs/historical_ingestion_warnings.csv"
    phase1 = json.loads(phase1_path.read_text(encoding="utf-8"))
    remediation = json.loads(remediation_path.read_text(encoding="utf-8"))
    cleanup = remediation.get("historical_warning_cleanup", {})
    by_path = {}
    for group in cleanup.get("groups", []):
        for path in group.get("paths", []):
            by_path[path] = group
    rows = []
    for finding in phase1.get("findings", []):
        if finding.get("category") != "stale_state":
            continue
        path = str(finding.get("path") or "")
        group = by_path.get(path, {})
        batch_path = Path(path)
        batch_id = batch_path.name
        batch_timestamp = batch_id.removeprefix("ipos_main_ctrl_")
        requirement_ids = source_req_ids(batch_path)
        explanation = (
            f"Historical ingestion batch {batch_id} is retained for audit but is not the "
            f"active batch; the active batch is selected separately."
        )
        rows.append({
            "severity": group.get("severity", "LOW"),
            "phase1_severity": finding.get("severity", "WARNING"),
            "category": finding.get("category", ""),
            "warning_scope": "batch-level workflow state, not a requirement defect",
            "warning_explanation": explanation,
            "why_phase1_warning": (
                "Phase 1 found an older ingestion candidate beside the active batch. "
                "It used WARNING because stale candidates can add noise or create future "
                "active-batch selection ambiguity until their authority is explicitly classified."
            ),
            "missing_context_in_original_finding": (
                "The raw finding did not identify the active batch, current authority effect, "
                "historical reason, cleanup action, workflow triage, or available source requirement IDs."
            ),
            "message": finding.get("message", ""),
            "path": path,
            "historical_batch_id": batch_id,
            "historical_batch_timestamp": batch_timestamp,
            "source_spec": group.get("source_spec", ""),
            "source_kind": group.get("source_kind", ""),
            "source_req_ids": requirement_ids,
            "source_req_id_note": (
                "IDs found in this historical batch; the warning itself is batch-level."
                if requirement_ids
                else "No source requirement ID is attached to this batch-level warning."
            ),
            "active_batch_path": cleanup.get("active_batch_path", ""),
            "current_authority_effect": group.get("current_authority_effect", ""),
            "future_validation_effect": group.get("future_validation_effect", ""),
            "root_cause": group.get("root_cause", ""),
            "cleanup_action": group.get("action", ""),
            "status": "historical_non_authoritative",
            "workflow_triage": "INFO_ONLY; preserved for audit and excluded from current authority",
        })
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: row["path"]))
    return output_path


if __name__ == "__main__":
    print(create(Path(__file__).resolve().parents[1]))
