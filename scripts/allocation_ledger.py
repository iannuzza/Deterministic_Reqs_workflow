"""Deterministic allocation-ledger adapter shared by stages and reports."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Iterable

from approved_snapshot_resolver import resolve_complete_authoritative_input
from requirement_allocation_policy import (
    BLOCK_LOCAL_ANALOG,
    BLOCK_LOCAL_DIGITAL,
    DESCRIPTIVE_ONLY,
    SYSTEM_LEVEL,
    TOP_ANALOG_ARCHITECTURE,
    TOP_DIGITAL_ARCHITECTURE,
    allocation_row,
    persist_allocation_ledger,
    requires_hierarchy_parent,
    rule_for,
    validate_allocation_rows,
    write_allocation_ledger,
)

LOCAL_TERMS = {
    "local_clock_reset", "local_register_access", "local_fifo_buffering",
    "local_interrupt_event_status", "local_timing_protocol", "local_mode_state",
    "exact_io_port_definition",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _blocks(mapping: str) -> list[str]:
    return [item.strip() for item in re.split(r"\s*[;,]\s*", mapping or "") if item.strip() and item.strip().casefold() != "unassigned"]


def _topic(statement: str) -> str:
    text = (statement or "").casefold()
    tests = (
        ("exact_io_port_definition", ("port", "pin", "i/o list", "io list")),
        ("local_register_access", ("register", "regmap", "address", "write-protect")),
        ("local_fifo_buffering", ("fifo", "buffer", "watermark", "overflow", "underflow")),
        ("local_interrupt_event_status", ("interrupt", "irq", "event", "status flag")),
        ("local_clock_reset", ("clock", "reset", "por", "reset release")),
        ("local_timing_protocol", ("latency", "throughput", "protocol", "timing", "frequency")),
        ("local_mode_state", ("state machine", "state transition", "operating mode")),
        ("system_power_wakeup", ("power domain", "wake-up", "wakeup", "retention", "isolation")),
    )
    for name, terms in tests:
        if any(term in text for term in terms):
            return name
    return ""


def _classify(row: dict[str, str], owner: str, domain: str) -> tuple[str, str, str]:
    statement = row.get("requirement_statement") or row.get("statement") or ""
    topic = _topic(statement)
    lower = statement.casefold()
    if domain.casefold() in {"ana", "analog", "analog_or_system"}:
        return TOP_ANALOG_ARCHITECTURE, "ARS", topic
    if domain.casefold() in {"dig", "digital", "digital_or_system"}:
        return TOP_DIGITAL_ARCHITECTURE, "DRS", topic
    if any(term in lower for term in ("descriptive", "context only")):
        return DESCRIPTIVE_ONLY, "", topic
    return SYSTEM_LEVEL, "SRS", topic


def build_source_ledger(
    source_rows: Iterable[dict[str, str]],
    mapping_rows: Iterable[dict[str, str]],
    *,
    snapshot_id: str,
    source_type: str = "primary",
    allocation_rows: Iterable[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    mapping = {
        (row.get("Requirement ID") or row.get("source_req_id") or "").strip(): _blocks(row.get("Block(s)") or row.get("Block") or row.get("approved_block") or "")
        for row in mapping_rows
    }
    allocation = {
        (row.get("source_req_id") or row.get("req_id") or "").strip(): row
        for row in (allocation_rows or [])
    }
    if not allocation:
        raise ValueError("Ledger materialization requires authoritative allocation metadata.")
    result: list[dict[str, str]] = []
    for source in source_rows:
        req_id = (source.get("source_req_id") or source.get("id") or "").strip()
        if not req_id:
            continue
        domain = (
            source.get("domain")
            or source.get("category")
            or source.get("approved_classification")
            or ""
        )
        approved = allocation.get(req_id)
        if approved is None:
            raise ValueError(f"Missing authoritative allocation metadata for {req_id}.")
        requirement_class = (approved.get("allocation_class") or "").strip()
        owning_target = (approved.get("owning_target") or "").strip()
        if not requirement_class or not owning_target:
            raise ValueError(f"Incomplete authoritative allocation metadata for {req_id}.")
        if rule_for(requirement_class).owning_target != owning_target:
            raise ValueError(
                f"Allocation target mismatch for {req_id}: class={requirement_class}, target={owning_target}."
            )
        lineage_mode = (approved.get("lineage_mode") or "").strip()
        parent_ids = (approved.get("hierarchy_parent_req_ids") or "").strip()
        if requires_hierarchy_parent(requirement_class, lineage_mode) and not parent_ids:
            raise ValueError(f"Lower-level hierarchical allocation is missing a real parent requirement ID for {req_id}.")
        owner = (approved.get("approved_block") or "").strip()
        statement = source.get("requirement_statement") or source.get("statement") or ""
        topic = _topic(statement)
        result.append(allocation_row(
            req_id=req_id,
            source_type=source_type,
            spec_level=owning_target,
            requirement_class=requirement_class,
            owning_block=owner,
            actual_targets=(),
            rendered_in_specs=(),
            snapshot_id=snapshot_id,
            topic_family=topic,
            abstraction_level="block_local" if "block_local" in requirement_class else "architecture",
            nearest_parent_req_id=(approved.get("hierarchy_parent_req_ids") or "").strip(),
            candidate_parent_req_ids=(approved.get("lineage_candidate_parent_req_ids") or "").strip(),
            source_origin_ids=tuple(item.strip() for item in (approved.get("source_origin_req_ids") or req_id).split(";") if item.strip()),
            owning_domain=(approved.get("owning_domain") or domain).strip(),
            lineage_mode=lineage_mode,
            policy_rationale=(approved.get("allocation_rationale") or "").strip(),
        ))
    return result


def _project_id(repo_root: Path) -> str:
    context_path = repo_root / "config/project_context.json"
    if not context_path.exists():
        return repo_root.name
    context = json.loads(context_path.read_text(encoding="utf-8"))
    return str(context.get("project_name") or repo_root.name)


def refresh_ledger(repo_root: Path, *, snapshot_id: str, source_rows: Iterable[dict[str, str]] | None = None, source_type: str = "primary") -> Path:
    """Materialize from the approved snapshot boundary, never from a CSV fallback."""
    requirement_input, selection = resolve_complete_authoritative_input(
        repo_root,
        "allocation-ledger",
        project_id=_project_id(repo_root),
        snapshot_id=snapshot_id,
    )
    approved_rows = [dict(row) for row in requirement_input.rows]
    if not approved_rows:
        raise ValueError(f"Approved snapshot {snapshot_id} resolved to zero requirements.")
    if not requirement_input.mapping:
        raise ValueError(f"Approved snapshot {snapshot_id} has no approved architecture mappings.")
    if source_rows is not None:
        supplied_ids = {(row.get("source_req_id") or row.get("canonical_id") or row.get("id") or "").strip() for row in source_rows}
        approved_ids = {(row.get("source_req_id") or row.get("canonical_id") or row.get("id") or "").strip() for row in approved_rows}
        if (supplied_ids - {""}) != (approved_ids - {""}):
            raise ValueError("Ledger source rows do not match the approved snapshot requirement set.")
    canonical_to_source = {
        str(row.get("canonical_id") or "").strip(): str(row.get("source_req_id") or "").strip()
        for row in approved_rows
        if str(row.get("canonical_id") or "").strip() and str(row.get("source_req_id") or "").strip()
    }
    mapping_rows = [
        {"Requirement ID": canonical_to_source.get(key, key), "approved_block": value}
        for key, value in requirement_input.mapping.items()
    ]
    allocation_rows = []
    for canonical_id, metadata in requirement_input.allocation.items():
        source_id = canonical_to_source.get(canonical_id, "")
        if source_id:
            allocation_rows.append({"source_req_id": source_id, **metadata})
    rows = build_source_ledger(
        approved_rows,
        mapping_rows,
        snapshot_id=requirement_input.snapshot_id,
        source_type=source_type,
        allocation_rows=allocation_rows,
    )
    findings = validate_allocation_rows(rows)
    if findings:
        raise ValueError("Invalid authoritative allocation metadata: " + "; ".join(findings[:10]))
    if not rows:
        raise ValueError(f"Approved snapshot {requirement_input.snapshot_id} produced zero allocation rows.")
    path = repo_root / "artifacts/traceability_reports/requirement_allocation_ledger.csv"
    write_allocation_ledger(path, rows)
    persist_allocation_ledger(repo_root, project_id=_project_id(repo_root), rows=rows, snapshot_id=requirement_input.snapshot_id)
    manifest = {
        "materialized": True,
        "source_type": source_type,
        "row_count": len(rows),
        "source_path": str(requirement_input.source_path),
        "snapshot_id": requirement_input.snapshot_id,
        "selection": selection,
        "snapshot_hash": requirement_input.snapshot_hash,
        "corpus_hash": requirement_input.corpus_hash,
        "source_type_counts": {source_type: len(rows)},
        "spec_level_counts": {level: sum(row.get("spec_level") == level for row in rows) for level in sorted({row.get("spec_level", "") for row in rows})},
    }
    manifest_path = repo_root / "artifacts/traceability_reports/requirement_allocation_materialization.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
