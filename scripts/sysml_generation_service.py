"""Approved-snapshot boundary for derived SysML generation."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterable, Mapping

from audit_log import record_event
from approved_snapshot_resolver import resolve_authoritative_input
from validate_downstream_coherence import canonical_human_label, human_label_key


class SysMLCompletenessError(RuntimeError):
    """Raised when generated SysML omits approved requirements in scope."""


def validate_snapshot_requirement_coverage(
    snapshot,
    requirements: Iterable[Mapping[str, str]],
    requirements_by_block: Mapping[str, Iterable[Mapping[str, str]]],
    *,
    partial_export: bool = False,
) -> dict[str, object]:
    """Verify that every approved mapped requirement is emitted under its block."""
    emitted_by_block = {
        human_label_key(block): {
            str(row.get("source_req_id") or row.get("canonical_id") or "").strip()
            for row in rows
            if str(row.get("source_req_id") or row.get("canonical_id") or "").strip()
        }
        for block, rows in requirements_by_block.items()
    }
    system_emitted = {
        str(row.get("source_req_id") or row.get("canonical_id") or "").strip()
        for row in requirements
        if str(row.get("source_req_id") or row.get("canonical_id") or "").strip()
    }
    links = getattr(snapshot, "source_links", {}) or {}
    expected_by_block: dict[str, set[str]] = {}
    for row in getattr(snapshot, "rows", ()):
        canonical_id = str(row.get("canonical_id") or "").strip()
        source_id = str(row.get("source_req_id") or "").strip()
        identifiers = {item for item in (canonical_id, source_id, *links.get(canonical_id, ())) if item}
        mapping_value = str((getattr(snapshot, "mapping", {}) or {}).get(canonical_id, ""))
        owners = [item.strip() for item in mapping_value.replace(",", ";").split(";") if item.strip() and item.strip() != "Unassigned"]
        for owner in owners or ["__system__"]:
            owner_key = owner if owner == "__system__" else human_label_key(owner)
            expected_by_block.setdefault(owner_key, set()).update(identifiers)

    missing: dict[str, list[str]] = {}
    digital_subsystem_key = human_label_key("Digital Subsystem")
    for block, identifiers in expected_by_block.items():
        if block == "__system__":
            continue
        emitted = emitted_by_block.get(block, set())
        if block == digital_subsystem_key:
            emitted = emitted | system_emitted
        present = {item for item in identifiers if item in emitted}
        if not present:
            missing[canonical_human_label(block)] = sorted(identifiers)
    result = {"expected_by_block": expected_by_block, "emitted_by_block": emitted_by_block, "missing_by_block": missing, "partial_export": partial_export}
    if missing and not partial_export:
        details = "; ".join(f"{block}: {', '.join(values)}" for block, values in sorted(missing.items()))
        raise SysMLCompletenessError(f"Approved snapshot requirements are missing from SysML block output: {details}")
    return result


def require_sysml_snapshot(repo_root: Path, *, project_id: str, snapshot_id: str | None, use_latest_approved: bool):
    return resolve_authoritative_input(repo_root, "sysml", project_id=project_id, snapshot_id=snapshot_id, use_latest_approved=use_latest_approved)


def generate_sysml_from_snapshot(
    repo_root: Path,
    *,
    project_id: str,
    snapshot_id: str | None,
    use_latest_approved: bool,
    output_path: Path,
    generator: Callable[[object, Path], None],
) -> Path:
    snapshot = require_sysml_snapshot(repo_root, project_id=project_id, snapshot_id=snapshot_id, use_latest_approved=use_latest_approved)
    generator(snapshot, output_path)
    record_event(repo_root, event_type="sysml_generated", entity_type="sysml", entity_id=str(output_path), actor="system", message="SysML generated from approved immutable snapshot", project_id=project_id, payload={"snapshot_id": snapshot.snapshot_id, "output_path": str(output_path)})
    return output_path
