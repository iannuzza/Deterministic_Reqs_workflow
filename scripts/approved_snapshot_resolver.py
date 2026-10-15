"""Mandatory approved snapshot boundary for authoritative consumers."""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
from typing import Any

from approved_profile_resolver import resolve_approved_profiles, resolve_snapshot_profile
from requirement_corpus import RequirementInput, load_sqlite_snapshot_input
from snapshot_manager import resolve_approved_snapshot


class ApprovedResolverError(RuntimeError):
    pass


def _project_id(repo_root: Path) -> str:
    context_path = repo_root / "config/project_context.json"
    if not context_path.exists():
        return repo_root.name
    import json
    context = json.loads(context_path.read_text(encoding="utf-8"))
    return str(context.get("project_name") or repo_root.name)


def _complete_input(requirement_input: RequirementInput) -> tuple[bool, str]:
    rows = list(requirement_input.rows)
    ids = [str(row.get("canonical_id") or row.get("source_req_id") or row.get("id") or "").strip() for row in rows]
    if not rows:
        return False, "resolved requirement set is empty"
    if any(not value for value in ids):
        return False, "resolved requirement set contains an empty requirement ID"
    if len(set(ids)) != len(ids):
        return False, "resolved requirement set contains duplicate requirement IDs"
    if not requirement_input.mapping:
        return False, "approved mapping set is empty"
    missing = sorted(set(ids) - set(requirement_input.mapping))
    if missing:
        return False, f"requirements missing approved mappings: {', '.join(missing[:5])}"
    return True, "complete approved canonical requirements and mappings"


def resolve_complete_authoritative_input(
    repo_root: Path,
    stage: str,
    *,
    project_id: str,
    snapshot_id: str | None = None,
) -> tuple[RequirementInput, dict[str, Any]]:
    """Resolve one complete approved snapshot, recording deterministic selection.

    An explicit ``snapshot_id`` is never replaced. Without one, this function
    validates only the newest approved candidate by ``approved_at``, then
    descending snapshot ID. It never falls back to historical snapshots.
    """
    from canonical_store import connect

    attempted: list[dict[str, str]] = []
    if snapshot_id:
        try:
            requirement_input = resolve_authoritative_input(
                repo_root, stage, project_id=project_id, snapshot_id=snapshot_id,
            )
        except Exception as exc:
            raise ApprovedResolverError(f"Requested snapshot {snapshot_id} rejected: {exc}") from exc
        complete, reason = _complete_input(requirement_input)
        if not complete:
            raise ApprovedResolverError(f"Requested snapshot {snapshot_id} rejected: {reason}")
        return requirement_input, {
            "selection_mode": "explicit",
            "selected_snapshot_id": requirement_input.snapshot_id,
            "attempted_snapshots": [{"snapshot_id": snapshot_id, "accepted": True, "reason": reason}],
            "completeness_criteria": "approved status; project match; non-empty canonical and mapping sets; one approved mapping per requirement; resolver hash validation",
        }

    connection = connect(repo_root)
    try:
        candidates = connection.execute(
            "SELECT snapshot_id, approved_at FROM snapshots WHERE project_id = ? AND status = 'approved' ORDER BY approved_at DESC, snapshot_id DESC LIMIT 1",
            (project_id,),
        ).fetchall()
    finally:
        connection.close()
    valid: list[tuple[str, str, RequirementInput]] = []
    candidates = sorted(candidates, key=lambda row: (str(row["approved_at"] or ""), str(row["snapshot_id"])), reverse=True)[:1]
    for candidate in candidates:
        candidate_id = str(candidate["snapshot_id"])
        try:
            candidate_input = resolve_authoritative_input(repo_root, stage, project_id=project_id, snapshot_id=candidate_id)
            complete, reason = _complete_input(candidate_input)
        except Exception as exc:
            complete, reason, candidate_input = False, str(exc), None
        attempted.append({"snapshot_id": candidate_id, "accepted": complete, "reason": reason})
        if complete and candidate_input is not None:
            valid.append((str(candidate["approved_at"] or ""), candidate_id, candidate_input))
    if not valid:
        reasons = "; ".join(f"{item['snapshot_id']}: {item['reason']}" for item in attempted)
        raise ApprovedResolverError(f"No complete approved snapshot is available. Checked: {reasons or 'none'}")
    approved_at, selected_id, selected_input = sorted(valid, key=lambda item: (item[0], item[1]), reverse=True)[0]
    return selected_input, {
        "selection_mode": "deterministic_complete_candidate",
        "selected_snapshot_id": selected_id,
        "selected_approved_at": approved_at,
        "attempted_snapshots": attempted,
        "completeness_criteria": "approved status; project match; non-empty canonical and mapping sets; one approved mapping per requirement; resolver hash validation",
    }


def resolve_authoritative_input(
    repo_root: Path,
    stage: str,
    *,
    project_id: str,
    snapshot_id: str | None = None,
    use_latest_approved: bool = False,
    required_profiles: tuple[str, ...] = ("vocabulary", "taxonomy", "architecture"),
) -> RequirementInput:
    try:
        snapshot = resolve_approved_snapshot(repo_root, snapshot_id=snapshot_id, use_latest_approved=use_latest_approved)
        resolve_approved_profiles(repo_root, project_id=project_id, profile_kinds=required_profiles)
        if snapshot["project_id"] != project_id:
            raise ApprovedResolverError("Snapshot project does not match requested project.")
        return load_sqlite_snapshot_input(repo_root, stage, snapshot_id=snapshot["snapshot_id"])
    except Exception as exc:
        if isinstance(exc, ApprovedResolverError):
            raise
        raise ApprovedResolverError(str(exc)) from exc


def validate_governed_source_context(profile: dict) -> list[str]:
    """Validate content membership inside the existing architecture profile."""
    context = profile.get("governed_source_context")
    if context is None:
        return []
    if not isinstance(context, dict) or context.get("version") != 1 or not isinstance(context.get("records"), list):
        return ["governed_source_context_invalid_schema"]
    findings = []
    identities = set()
    for record in context["records"]:
        if not isinstance(record, dict):
            findings.append("governed_source_context_invalid_record")
            continue
        identity = str(record.get("record_id") or "")
        text = str(record.get("statement") or "")
        if not identity or identity in identities:
            findings.append("governed_source_context_duplicate_or_missing_identity")
        identities.add(identity)
        if not text or hashlib.sha256(text.encode("utf-8")).hexdigest() != record.get("content_sha256"):
            findings.append("governed_source_context_text_hash_mismatch:" + identity)
        if record.get("evidence_kind") != "descriptive":
            findings.append("governed_source_context_unsupported_content_kind:" + identity)
        if record.get("review_decision") == "approved" and (
            not record.get("source_file") or not (record.get("source_revision_id") or record.get("source_revision"))):
            findings.append("governed_source_context_missing_source_revision:" + identity)
        try:
            spans = json.loads(record.get("source_spans_json") or "[]")
            if not spans or any(not isinstance(span, dict) or not span.get("text_file")
                                or not isinstance(span.get("page"), int) or span["page"] < 1
                                or not isinstance(span.get("line"), int) or span["line"] < 1
                                or not isinstance(span.get("artifact_sha256"), str)
                                or len(span["artifact_sha256"]) != 64
                                or any(character not in "0123456789abcdef" for character in span["artifact_sha256"])
                                for span in spans):
                findings.append("governed_source_context_invalid_source_spans:" + identity)
        except (ValueError, TypeError):
            findings.append("governed_source_context_invalid_source_spans:" + identity)
        decision = record.get("review_decision", "pending")
        if decision not in {"pending", "approved", "rejected"}:
            findings.append("governed_source_context_invalid_review_decision:" + identity)
        if decision == "approved":
            if not record.get("mapped_block") or record["mapped_block"] not in profile.get("block_defs", {}):
                findings.append("governed_source_context_unknown_owner:" + identity)
            if record.get("domain") not in {"digital", "analog", "mixed_signal", "system"}:
                findings.append("governed_source_context_invalid_domain:" + identity)
            if not str(record.get("review_rationale") or "").strip():
                findings.append("governed_source_context_missing_review_rationale:" + identity)
    return findings


def resolve_governed_descriptive_context(
    repo_root: Path, *, snapshot_id: str, project_id: str,
) -> tuple[dict, ...]:
    snapshot = resolve_approved_snapshot(repo_root, snapshot_id=snapshot_id)
    if snapshot["project_id"] != project_id:
        raise ApprovedResolverError("Governed source context project mismatch")
    profile = resolve_snapshot_profile(repo_root, snapshot)
    findings = validate_governed_source_context(profile)
    if findings:
        raise ApprovedResolverError("; ".join(findings))
    return tuple({**record, "snapshot_id": snapshot_id, "admission_state": "admitted"}
                 for record in profile.get("governed_source_context", {}).get("records", ())
                 if record.get("review_decision") == "approved")


def resolve_complete_snapshot_id(
    repo_root: Path,
    *,
    project_id: str,
    snapshot_id: str | None = None,
) -> str:
    """Return one validated snapshot ID for a multi-step downstream flow."""
    _, selection = resolve_complete_authoritative_input(
        repo_root,
        "srs",
        project_id=project_id,
        snapshot_id=snapshot_id,
    )
    selected_id = str(selection.get("selected_snapshot_id") or "")
    if not selected_id:
        raise ApprovedResolverError("Approved snapshot selection returned no snapshot ID")
    return selected_id
