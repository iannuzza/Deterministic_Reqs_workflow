"""Mandatory approved snapshot boundary for authoritative consumers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from approved_profile_resolver import resolve_approved_profiles
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
    explicitly evaluates all approved local candidates and selects the newest
    complete candidate by ``approved_at``, then descending snapshot ID.
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
            "SELECT snapshot_id, approved_at FROM snapshots WHERE project_id = ? AND status = 'approved' ORDER BY approved_at DESC, snapshot_id DESC",
            (project_id,),
        ).fetchall()
    finally:
        connection.close()
    valid: list[tuple[str, str, RequirementInput]] = []
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
