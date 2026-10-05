"""Project-agnostic requirement allocation and traceability policy.

The policy is deliberately deterministic. Generators may choose source evidence,
but they must use these classes and target rules when allocating or reporting it.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


SYSTEM_LEVEL = "system_level"
TOP_DIGITAL_ARCHITECTURE = "top_digital_architecture"
TOP_ANALOG_ARCHITECTURE = "top_analog_architecture"
BLOCK_LOCAL_DIGITAL = "block_local_digital"
BLOCK_LOCAL_ANALOG = "block_local_analog"
DESCRIPTIVE_ONLY = "descriptive_only"

ACCOUNTING_STATUSES = frozenset({
    "covered", "under_covered", "over_propagated", "misallocated", "orphaned",
    "approved_exclusion", "unassigned_review",
})
LINEAGE_MODES = frozenset({
    "normal_hierarchical", "direct_source_to_ipos", "direct_supplementary_to_ipos",
    "split_lineage",
})

TOPIC_POLICIES = {
    "local_clock_reset": ("Digital IPOS",),
    "local_register_access": ("Digital IPOS",),
    "local_fifo_buffering": ("Digital IPOS",),
    "local_interrupt_event_status": ("Digital IPOS",),
    "local_timing_protocol": ("Digital IPOS", "Analog IPOS"),
    "local_mode_state": ("Digital IPOS", "Analog IPOS"),
    "exact_io_port_definition": ("Digital IPOS", "Analog IPOS"),
    "shared_clock_reset_power_coordination": ("DRS", "ARS"),
    "shared_interconnect_resource": ("DRS",),
    "analog_partition_bias_supply": ("ARS",),
    "system_power_wakeup": ("SRS",),
}


@dataclass(frozen=True)
class AllocationRule:
    requirement_class: str
    owning_target: str
    required_downstream_targets: tuple[str, ...]
    contextual_targets: tuple[str, ...]
    forbidden_targets: tuple[str, ...]
    direct_ipos_allowed: bool


RULES: dict[str, AllocationRule] = {
    SYSTEM_LEVEL: AllocationRule(SYSTEM_LEVEL, "SRS", ("SRS",), (), ("DRS", "ARS", "Digital IPOS", "Analog IPOS"), False),
    TOP_DIGITAL_ARCHITECTURE: AllocationRule(TOP_DIGITAL_ARCHITECTURE, "DRS", ("DRS",), ("SRS",), ("Digital IPOS",), False),
    TOP_ANALOG_ARCHITECTURE: AllocationRule(TOP_ANALOG_ARCHITECTURE, "ARS", ("ARS",), ("SRS",), ("Analog IPOS",), False),
    BLOCK_LOCAL_DIGITAL: AllocationRule(BLOCK_LOCAL_DIGITAL, "Digital IPOS", ("Digital IPOS",), (), ("SRS", "DRS"), True),
    BLOCK_LOCAL_ANALOG: AllocationRule(BLOCK_LOCAL_ANALOG, "Analog IPOS", ("Analog IPOS",), (), ("SRS", "ARS"), True),
    DESCRIPTIVE_ONLY: AllocationRule(DESCRIPTIVE_ONLY, "none", (), (), ("SRS", "DRS", "ARS", "Digital IPOS", "Analog IPOS"), False),
}


def rule_for(requirement_class: str) -> AllocationRule:
    """Return a rule, treating unknown classifications as review-required."""
    return RULES.get(requirement_class, AllocationRule(
        requirement_class, "review", (), (), (), False,
    ))


def requires_hierarchy_parent(requirement_class: str, lineage_mode: str) -> bool:
    """Return whether approved lineage explicitly requires another requirement parent.

    ``normal_hierarchical`` describes ordinary source-to-level placement and does
    not, by itself, prove a requirement-to-requirement parent relation.
    """
    return requirement_class in {BLOCK_LOCAL_DIGITAL, BLOCK_LOCAL_ANALOG} and lineage_mode == "split_lineage"


def is_approved_top_level_without_parent(row: Mapping[str, object]) -> bool:
    """Identify an approved SRS/DRS/ARS placement where a parent is not applicable."""
    decision = str(row.get("review_decision") or "").strip().casefold()
    allocation_class = str(row.get("allocation_class") or "").strip()
    owning_target = str(row.get("owning_target") or "").strip()
    lineage_mode = str(row.get("lineage_mode") or "").strip()
    return (
        decision == "approved"
        and allocation_class in {SYSTEM_LEVEL, TOP_DIGITAL_ARCHITECTURE, TOP_ANALOG_ARCHITECTURE}
        and owning_target in {"SRS", "DRS", "ARS"}
        and lineage_mode == "normal_hierarchical"
        and not str(row.get("hierarchy_parent_req_ids") or "").strip()
    )


def topic_policy(topic_family: str) -> tuple[str, ...]:
    """Return the only levels allowed to own a topic family."""
    return TOPIC_POLICIES.get(topic_family, ())


def direct_ipos_is_eligible(
    requirement_class: str, *, source_type: str, approved: bool, in_scope: bool,
    owning_block: str, mixed_requirement: bool, meaningful_intermediate: bool,
    lineage_preserved: bool,
) -> bool:
    """Gate direct IPOS allocation using explicit evidence, not source type or ID heuristics."""
    rule = rule_for(requirement_class)
    return bool(
        approved and in_scope and owning_block and rule.direct_ipos_allowed
        and not mixed_requirement and not meaningful_intermediate and lineage_preserved
        # Source type is provenance only and never controls placement.
    )


def nearest_parent(requirement_class: str, available: Iterable[str]) -> str:
    """Select the nearest rendered parent for one generated child."""
    present = {value for value in available if value}
    if requirement_class == BLOCK_LOCAL_DIGITAL:
        for candidate in ("DRS", "SRS"):
            if candidate in present:
                return candidate
    if requirement_class == BLOCK_LOCAL_ANALOG:
        for candidate in ("ARS", "SRS"):
            if candidate in present:
                return candidate
    for candidate in ("SRS", "Source", "Supplementary Source"):
        if candidate in present:
            return candidate
    return ""


def accounting_status(requirement_class: str, actual_targets: Iterable[str], *, approved_exclusion: bool = False) -> str:
    """Account for target coverage without requiring every class at every level."""
    if approved_exclusion:
        return "approved_exclusion"
    rule = rule_for(requirement_class)
    actual = set(actual_targets)
    if not rule.required_downstream_targets:
        return "covered" if not actual else "over_propagated"
    if not actual:
        return "orphaned"
    if set(rule.required_downstream_targets).issubset(actual):
        return "covered"
    if actual & (set(rule.required_downstream_targets) | set(rule.contextual_targets)):
        return "under_covered"
    return "misallocated"


def allocation_row(
    *, req_id: str, source_type: str, spec_level: str, requirement_class: str,
    source_origin_ids: Iterable[str] = (), owning_block: str = "", owning_domain: str = "",
    actual_targets: Iterable[str] = (), rendered_in_specs: Iterable[str] = (),
    nearest_parent_req_id: str = "", direct_source_to_ipos: bool = False,
    candidate_parent_req_ids: str = "",
    snapshot_id: str = "", topic_family: str = "", abstraction_level: str = "",
    split_parent_req_id: str = "", approved: bool = True, in_scope: bool = True,
    mixed_requirement: bool = False, meaningful_intermediate: bool = False,
    lineage_preserved: bool = True, lineage_mode: str = "normal_hierarchical",
    policy_rationale: str = "",
) -> dict[str, str]:
    """Create the canonical tabular representation used by reports and GUI."""
    actual = tuple(dict.fromkeys(value for value in actual_targets if value))
    rendered = tuple(dict.fromkeys(value for value in rendered_in_specs if value))
    status = accounting_status(requirement_class, actual, approved_exclusion=not approved)
    if direct_source_to_ipos and not direct_ipos_is_eligible(
        requirement_class, source_type=source_type, approved=approved, in_scope=in_scope,
        owning_block=owning_block, mixed_requirement=mixed_requirement,
        meaningful_intermediate=meaningful_intermediate, lineage_preserved=lineage_preserved,
    ):
        status = "misallocated"
    if lineage_mode not in LINEAGE_MODES:
        raise ValueError(f"Unsupported lineage mode: {lineage_mode}")
    rationale = policy_rationale or (
        f"{requirement_class} owns {rule_for(requirement_class).owning_target}; "
        f"topic policy allows {', '.join(topic_policy(topic_family)) or 'review'}"
    )
    return {
        "req_id": req_id,
        "source_type": source_type,
        "spec_level": spec_level,
        "immediate_parent_req_ids": nearest_parent_req_id,
        "lineage_candidate_parent_req_ids": candidate_parent_req_ids,
        "source_origin_req_ids": ";".join(source_origin_ids),
        "owning_block": owning_block,
        "owning_domain": owning_domain,
        "hierarchy_or_coverage_class": requirement_class,
        "owning_target": rule_for(requirement_class).owning_target,
        "valid_downstream_targets": ";".join(dict.fromkeys(
            rule_for(requirement_class).required_downstream_targets
            + rule_for(requirement_class).contextual_targets
        )),
        "allowed_contextual_targets": ";".join(rule_for(requirement_class).contextual_targets),
        "forbidden_upward_targets": ";".join(rule_for(requirement_class).forbidden_targets),
        "required_downstream_targets": ";".join(rule_for(requirement_class).required_downstream_targets),
        "actual_downstream_targets": ";".join(actual),
        "rendered_in_specs": ";".join(rendered),
        "direct_source_to_ipos": "true" if direct_source_to_ipos else "false",
        "snapshot_id": snapshot_id,
        "coverage_status": status,
        "lineage_mode": lineage_mode,
        "abstraction_level": abstraction_level,
        "integration_or_block_local": "block_local" if "block_local" in requirement_class else "integration",
        "scope": owning_domain or "system",
        "topic_family": topic_family,
        "split_parent_req_id": split_parent_req_id,
        "approved": "true" if approved else "false",
        "policy_rationale": rationale,
    }


LEDGER_FIELDS = tuple(allocation_row(req_id="", source_type="", spec_level="", requirement_class=""))


def write_allocation_ledger(path: Path, rows: Iterable[Mapping[str, object]]) -> Path:
    """Write a deterministic CSV ledger for reports, validation, and GUI use."""
    materialized = [{field: str(row.get(field, "") or "") for field in LEDGER_FIELDS} for row in rows]
    materialized.sort(key=lambda row: (row["source_type"], row["req_id"], row["spec_level"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(LEDGER_FIELDS))
        writer.writeheader()
        writer.writerows(materialized)
    return path


def validate_allocation_rows(rows: Iterable[Mapping[str, object]]) -> list[str]:
    """Validate policy fields shared by generators, gates, reports, and GUI."""
    findings: list[str] = []
    for row in rows:
        req_id = str(row.get("req_id") or "")
        requirement_class = str(row.get("hierarchy_or_coverage_class") or "")
        rule = rule_for(requirement_class)
        actual = {value for value in str(row.get("actual_downstream_targets") or "").split(";") if value}
        forbidden = set(rule.forbidden_targets)
        leaked = actual & forbidden
        if leaked:
            findings.append(f"{req_id}: forbidden upward targets: {', '.join(sorted(leaked))}")
        lineage_mode = str(row.get("lineage_mode") or "")
        if lineage_mode not in LINEAGE_MODES:
            findings.append(f"{req_id}: invalid lineage mode: {lineage_mode}")
        status = str(row.get("coverage_status") or "")
        if status not in ACCOUNTING_STATUSES:
            findings.append(f"{req_id}: invalid coverage status: {status}")
        if row.get("direct_source_to_ipos") == "true" and lineage_mode not in {
            "direct_source_to_ipos", "direct_supplementary_to_ipos",
        }:
            findings.append(f"{req_id}: direct IPOS flag has non-direct lineage mode")
    return findings


def persist_allocation_ledger(
    repo_root: Path, *, project_id: str, rows: Iterable[Mapping[str, object]], snapshot_id: str,
) -> int:
    """Persist approved allocation rows in the canonical local SQLite model."""
    from canonical_store import connect, fingerprint, utc_now

    materialized = [{field: str(row.get(field, "") or "") for field in LEDGER_FIELDS} for row in rows]
    connection = connect(repo_root)
    try:
        count = 0
        for row in materialized:
            allocation_id = "allocation-" + fingerprint({"snapshot_id": snapshot_id, "req_id": row["req_id"], "spec_level": row["spec_level"]})[:24]
            connection.execute(
                """INSERT OR REPLACE INTO requirement_allocations(
                    allocation_id, project_id, req_id, source_type, source_origin_req_ids,
                    spec_level, owning_target, owning_block, owning_domain, requirement_class,
                    topic_family, abstraction_level, immediate_parent_req_ids, split_parent_req_id,
                    lineage_candidate_parent_req_ids,
                    valid_downstream_targets, required_downstream_targets, actual_downstream_targets,
                    rendered_in_specs, lineage_mode, coverage_status, direct_source_to_ipos,
                    policy_rationale, snapshot_id, approval_state, metadata_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                    allocation_id, project_id, row["req_id"], row["source_type"], row["source_origin_req_ids"],
                    row["spec_level"], row["owning_target"], row["owning_block"], row["owning_domain"],
                    row["hierarchy_or_coverage_class"], row["topic_family"], row["abstraction_level"],
                    row["immediate_parent_req_ids"], row["split_parent_req_id"], row["lineage_candidate_parent_req_ids"], row["valid_downstream_targets"],
                    row["required_downstream_targets"], row["actual_downstream_targets"], row["rendered_in_specs"],
                    row["lineage_mode"], row["coverage_status"], 1 if row["direct_source_to_ipos"] == "true" else 0,
                    row["policy_rationale"], snapshot_id, row["approved"], "{}", utc_now(),
                ),
            )
            count += 1
        connection.commit()
        return count
    finally:
        connection.close()
