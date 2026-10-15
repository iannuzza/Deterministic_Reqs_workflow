"""Strict resolver for approved canonical profile revisions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from canonical_store import connect, fingerprint

REQUIRED_PROFILE_KINDS = frozenset({"vocabulary", "taxonomy", "architecture"})


class ProfileResolutionError(RuntimeError):
    pass


def resolve_snapshot_profile(repo_root: Path, snapshot: dict, *, kind: str = "architecture") -> dict:
    """Resolve the exact approved profile revision captured by a snapshot."""
    if kind not in REQUIRED_PROFILE_KINDS:
        raise ProfileResolutionError("Unknown snapshot profile kind: " + kind)
    metadata = json.loads(snapshot.get("metadata_json") or "{}")
    expected = metadata.get("profiles", {}).get(kind)
    if not expected:
        raise ProfileResolutionError("Snapshot is missing its " + kind + " profile hash")
    connection = connect(repo_root)
    try:
        rows = connection.execute(
            """SELECT * FROM profile_revisions
               WHERE project_id = ? AND profile_kind = ? AND content_fingerprint = ?
                 AND lifecycle_state = 'approved' AND approval_state = 'approved'""",
            (snapshot["project_id"], kind, expected),
        ).fetchall()
        if not rows:
            raise ProfileResolutionError("Snapshot-bound approved profile is missing: " + kind)
        payloads = [json.loads(row["profile_payload_json"]) for row in rows]
        if any(not isinstance(payload, dict) or fingerprint(payload) != expected for payload in payloads):
            raise ProfileResolutionError("Snapshot-bound profile fingerprint mismatch: " + kind)
        return payloads[0]
    finally:
        connection.close()


def resolve_approved_profiles(repo_root: Path, *, project_id: str, profile_kinds: Iterable[str] = REQUIRED_PROFILE_KINDS) -> dict[str, dict]:
    requested = tuple(sorted(set(profile_kinds)))
    unknown = set(requested) - REQUIRED_PROFILE_KINDS
    if unknown:
        raise ProfileResolutionError(f"Unknown profile kinds: {sorted(unknown)}")
    connection = connect(repo_root)
    try:
        result = {}
        for kind in requested:
            row = connection.execute(
                """SELECT * FROM profile_revisions
                   WHERE project_id = ? AND profile_kind = ?
                     AND lifecycle_state = 'approved' AND approval_state = 'approved'
                   ORDER BY approved_at DESC, revision_number DESC, profile_revision_id DESC LIMIT 1""",
                (project_id, kind),
            ).fetchone()
            if row is None:
                raise ProfileResolutionError(f"No approved {kind} profile for project {project_id}.")
            try:
                payload = json.loads(row["profile_payload_json"])
            except json.JSONDecodeError as exc:
                raise ProfileResolutionError(f"Approved {kind} profile is not valid JSON.") from exc
            if not isinstance(payload, dict) or not row["content_fingerprint"]:
                raise ProfileResolutionError(f"Approved {kind} profile is incomplete.")
            result[kind] = {**dict(row), "payload": payload}
        return result
    finally:
        connection.close()
