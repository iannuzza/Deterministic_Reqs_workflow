#!/usr/bin/env python3
"""Freeze the approved Stage 2 architecture mapping for downstream generation."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import warnings
from datetime import datetime, timezone
from pathlib import Path

from canonical_store import connect, fingerprint, utc_now
from requirement_corpus import authoritative_corpus_path, write_approved_snapshot
from snapshot_manager import create_approved_snapshot
from pre_freeze_coverage import validate_pre_freeze_coverage
from pre_freeze_coherence_gate import evaluate as evaluate_pre_freeze_gate
from validate_stage2_profile import validate_approval_evidence


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _register_approved_profiles(repo_root: Path, project_id: str, reviewer: str) -> None:
    """Persist the configurations explicitly approved by the snapshot reviewer."""
    profiles = {
        "vocabulary": repo_root / "config/domain_vocabulary.json",
        "taxonomy": repo_root / "config/ontology_role_taxonomy.json",
        "architecture": repo_root / "config/stage2_mirco_arc_profile.json",
    }
    connection = connect(repo_root)
    try:
        for kind, path in profiles.items():
            if not path.exists():
                raise RuntimeError(f"Required {kind} profile is missing: {path}")
            payload = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise RuntimeError(f"Required {kind} profile is not a JSON object: {path}")
            content_fingerprint = fingerprint(payload)
            profile_revision_id = f"profile-{kind}-{content_fingerprint[:24]}"
            connection.execute(
                """INSERT OR IGNORE INTO profile_revisions(
                    profile_revision_id, project_id, profile_kind, profile_name, revision_number,
                    profile_payload_json, content_fingerprint, lifecycle_state, approval_state,
                    approved_by, approved_at, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'approved', 'approved', ?, ?, ?)""",
                (
                    profile_revision_id,
                    project_id,
                    kind,
                    path.name,
                    content_fingerprint[:12],
                    json.dumps(payload, sort_keys=True),
                    content_fingerprint,
                    reviewer,
                    utc_now(),
                    utc_now(),
                ),
            )
        connection.commit()
    finally:
        connection.close()


def freeze(repo_root: Path, reviewer: str) -> Path:
    context_path = repo_root / "config/project_context.json"
    context = json.loads(context_path.read_text(encoding="utf-8")) if context_path.exists() else {}
    project_id = str(context.get("project_name") or repo_root.name)
    retrieval_path = repo_root / str(context.get("retrieval_config_path") or "config/retrieval_config.json")
    retrieval_payload = json.loads(retrieval_path.read_text(encoding="utf-8")) if retrieval_path.exists() else {}
    gate = evaluate_pre_freeze_gate(repo_root, repo_root / "artifacts/validation/source_to_stage2b_coherence.json")
    if gate["decision"] != "GO_ON":
        raise RuntimeError(f"Pre-freeze coherence gate blocked Stage 2B freeze: {gate['decision']}")
    approval_findings = validate_approval_evidence(
        repo_root / "config/stage2_mirco_arc_profile.json",
        repo_root / "artifacts/stage1_specs/architecture_profile_draft.json",
        repo_root / "artifacts/stage1_specs/architecture_mapping_preview.csv",
    )
    if approval_findings:
        raise RuntimeError("Stage 2A approval evidence is stale or incomplete: " + "; ".join(approval_findings))
    coverage = validate_pre_freeze_coverage(repo_root, project_id=project_id)
    _register_approved_profiles(repo_root, project_id, reviewer)
    connection = connect(repo_root)
    try:
        revision_rows = connection.execute("SELECT current_revision_id FROM canonical_requirements WHERE project_id = ? AND current_revision_id IS NOT NULL ORDER BY canonical_requirement_id", (project_id,)).fetchall()
        mapping_rows = connection.execute("SELECT mapping_id FROM architecture_mappings WHERE project_id = ? AND lifecycle_state = 'approved' ORDER BY mapping_id", (project_id,)).fetchall()
    finally:
        connection.close()
    if not revision_rows:
        raise RuntimeError("No canonical requirement revisions are available for snapshot creation.")
    snapshot_id = create_approved_snapshot(
        repo_root,
        project_id=project_id,
        canonical_revision_ids=[row[0] for row in revision_rows],
        mapping_ids=[row[0] for row in mapping_rows],
        approved_by=reviewer,
        retrieval={"version": str(retrieval_payload.get("version") or "1"), "hash": fingerprint(retrieval_payload)},
        semantic_enabled=bool(retrieval_payload.get("semantic_enabled", False)),
        semantic_fallback_enabled=bool(retrieval_payload.get("semantic_fallback_enabled", False)),
    )
    print(json.dumps({"snapshot_id": snapshot_id, "project_id": project_id, "canonical_revisions": len(revision_rows), "approved_mappings": len(mapping_rows), "pre_freeze_coverage": coverage["status"]}, indent=2))
    return repo_root / "data/canonical/canonical_store.sqlite"


def freeze_legacy_export(repo_root: Path, reviewer: str, *, legacy: bool = False) -> Path:
    """Compatibility-only file snapshot; never used by authoritative consumers."""
    if not legacy:
        raise RuntimeError("freeze_legacy_export is non-authoritative compatibility behavior; pass legacy=True explicitly.")
    warnings.warn(
        "freeze_legacy_export(..., legacy=True) writes compatibility artifacts only; it does not create an authoritative snapshot.",
        DeprecationWarning,
        stacklevel=2,
    )
    profile_path = repo_root / "config/stage2_mirco_arc_profile.json"
    mapping_path = repo_root / "artifacts/stage1_specs/architecture_mapping_preview.csv"
    if not profile_path.exists() or not mapping_path.exists():
        raise RuntimeError("Stage 2B requires the Stage 2 approval profile and mapping preview.")
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    approval = profile.get("approval", {})
    if approval.get("status") != "approved":
        raise RuntimeError("Stage 2B requires an approved Stage 2 architecture mapping.")
    mapping_hash = _sha256(mapping_path)
    if approval.get("reviewed_mapping_preview_csv_sha256") != mapping_hash:
        raise RuntimeError("Stage 2B mapping preview hash is stale.")

    corpus_rows = _read(authoritative_corpus_path(repo_root))
    mapping_rows = _read(mapping_path)
    by_id = {
        (row.get("source_req_id") or row.get("id") or "").strip(): row
        for row in corpus_rows
    }
    frozen = []
    for mapping in mapping_rows:
        source_id = (mapping.get("source_req_id") or mapping.get("id") or "").strip()
        if not source_id or source_id not in by_id:
            raise RuntimeError(f"Approved mapping references unknown requirement: {source_id}")
        decision = (mapping.get("review_decision") or "").strip().lower()
        if decision not in {"approved", "reassigned"}:
            raise RuntimeError(f"Requirement {source_id} is not approved for Stage 2B.")
        row = dict(by_id[source_id])
        row.update({key: value for key, value in mapping.items() if value})
        row["snapshot_source_req_id"] = source_id
        frozen.append(row)

    snapshot_id = "stage2b_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    snapshot = write_approved_snapshot(
        repo_root,
        frozen,
        snapshot_id=snapshot_id,
        approved_by=reviewer,
        mapping_preview_hash=mapping_hash,
    )
    print(json.dumps({"snapshot": str(snapshot), "rows": len(frozen), "snapshot_id": snapshot_id}, indent=2))
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze the approved Stage 2B architecture mapping.")
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()
    freeze(Path(__file__).resolve().parents[1], args.reviewer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())