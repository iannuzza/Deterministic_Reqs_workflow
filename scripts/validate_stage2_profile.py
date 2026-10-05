#!/usr/bin/env python3
"""Validate Stage 2A profile mappings against Stage 1 source evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


def _ids(value: str) -> list[str]:
    return [item.strip().upper() for item in (value or "").split(";") if item.strip()]


def _read_ids(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {
            (row.get("source_req_id") or row.get("id") or "").strip().upper()
            for row in csv.DictReader(handle)
            if (row.get("source_req_id") or row.get("id") or "").strip()
        }


def _draft_review_sha256(draft: dict) -> str:
    stable = json.loads(json.dumps(draft, sort_keys=True))
    approval = stable.get("approval", {})
    if isinstance(approval, dict):
        for field in (
            "status", "approved_by", "approved_at", "reviewer_notes",
            "reviewed_draft_profile_sha256", "reviewed_mapping_preview_csv_sha256",
        ):
            approval[field] = ""
    review_package = stable.get("review_package", {})
    if isinstance(review_package, dict):
        review_package["draft_profile_sha256"] = ""
    encoded = json.dumps(stable, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_approval_evidence(profile_path: Path, draft_path: Path, mapping_path: Path) -> list[str]:
    """Validate the shared S2A approval contract consumed by S2B freeze."""
    findings: list[str] = []
    try:
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [f"Approved Stage 2A profile is missing or invalid: {profile_path}"]
    approval = profile.get("approval", {})
    if not isinstance(approval, dict) or str(approval.get("status") or "").casefold() != "approved":
        findings.append("Stage 2A approval status is not approved")
        return findings
    if not str(approval.get("approved_by") or "").strip():
        findings.append("Stage 2A approval is missing approved_by")
    recorded_mapping_hash = str(approval.get("reviewed_mapping_preview_csv_sha256") or "")
    if not mapping_path.exists():
        findings.append(f"Approved Stage 2A mapping CSV is missing: {mapping_path}")
    elif not recorded_mapping_hash:
        findings.append("Stage 2A approval is missing reviewed_mapping_preview_csv_sha256")
    elif recorded_mapping_hash != _sha256_file(mapping_path):
        findings.append("Stage 2A approval mapping hash does not match the current mapping CSV")
    try:
        draft = json.loads(draft_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        findings.append(f"Stage 2A profile draft is missing or invalid: {draft_path}")
        return findings
    recorded_draft_hash = str(approval.get("reviewed_draft_profile_sha256") or "")
    if not recorded_draft_hash:
        findings.append("Stage 2A approval is missing reviewed_draft_profile_sha256")
    elif recorded_draft_hash != _draft_review_sha256(draft):
        findings.append("Stage 2A approval draft hash does not match the current profile draft")
    return findings


def validate(profile_path: Path, source_edges_path: Path, requirements_path: Path) -> list[str]:
    findings: list[str] = []
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    block_defs = profile.get("block_defs", {})
    rows = profile.get("interaction_rows", [])
    source_edges: dict[str, tuple[str, str]] = {}
    source_endpoint_ids: dict[tuple[str, str], str] = {}
    with source_edges_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            req_id = (row.get("source_req_id") or "").strip().upper()
            if not req_id:
                findings.append("Source matrix evidence contains a row without source_req_id")
                continue
            if req_id in source_edges:
                findings.append(f"Source matrix evidence duplicates source_req_id: {req_id}")
            source_edges[req_id] = ((row.get("from_block") or "").strip(), (row.get("to_block") or "").strip())
            endpoint = source_edges[req_id]
            if not endpoint[0] or not endpoint[1]:
                findings.append(f"Source matrix evidence has an empty endpoint for {req_id}")
            previous_id = source_endpoint_ids.get(endpoint)
            if previous_id and previous_id != req_id:
                findings.append(
                    f"Source matrix evidence repeats destination cell {endpoint[0]}->{endpoint[1]}: "
                    f"{previous_id}, {req_id}"
                )
            source_endpoint_ids[endpoint] = req_id

    stage1_ids = _read_ids(requirements_path)
    profile_edges: dict[str, tuple[str, str]] = {}
    profile_endpoint_ids: dict[tuple[str, str], str] = {}
    for index, row in enumerate(rows, start=1):
        from_block = str(row.get("From block", "")).strip()
        to_block = str(row.get("To block", "")).strip()
        if not from_block or not to_block:
            findings.append(f"Profile interaction row {index} has an empty endpoint")
        for req_id in _ids(str(row.get("Requirement IDs", ""))):
            if req_id not in stage1_ids:
                findings.append(f"Profile matrix ID is absent from Stage 1: {req_id}")
            if req_id in profile_edges:
                findings.append(f"Profile matrix ID is assigned more than once: {req_id}")
            profile_edges[req_id] = (from_block, to_block)
            endpoint = profile_edges[req_id]
            previous_id = profile_endpoint_ids.get(endpoint)
            if previous_id and previous_id != req_id:
                findings.append(
                    f"Profile matrix repeats destination cell {from_block}->{to_block}: "
                    f"{previous_id}, {req_id}"
                )
            profile_endpoint_ids[endpoint] = req_id
            expected = source_edges.get(req_id)
            if expected is None:
                findings.append(f"Profile matrix ID has no source evidence: {req_id}")
            elif expected != (from_block, to_block):
                findings.append(
                    f"Profile mapping differs from source matrix for {req_id}: "
                    f"profile={from_block}->{to_block}, source={expected[0]}->{expected[1]}"
                )

    for req_id in sorted(set(source_edges) - set(profile_edges)):
        findings.append(f"Source matrix ID is missing from profile: {req_id}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Stage 2A profile against source matrix evidence")
    parser.add_argument("--profile", default="config/stage2_mirco_arc_profile.json")
    parser.add_argument("--source-edges", default="artifacts/stage1_requirements/source_matrix_edges.csv")
    parser.add_argument("--requirements", default="artifacts/stage1_requirements/requirements_summary.csv")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    findings = validate(*(root / Path(value) for value in (args.profile, args.source_edges, args.requirements)))
    if findings:
        print("Stage 2A profile crosscheck: FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("Stage 2A profile crosscheck: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())