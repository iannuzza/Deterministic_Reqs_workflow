"""Deterministic approval rules for supplementary requirement categories."""

from __future__ import annotations

from dataclasses import dataclass

CATEGORIES = frozenset({"new", "duplication", "refines", "conflict", "removed"})
SEMANTIC_CATEGORIES = frozenset({"new", "refines", "conflict", "removed"})


@dataclass(frozen=True)
class CategoryDecision:
    category: str
    approval_required: bool
    merge_allowed: bool
    reason: str


def validate_category(category: str) -> None:
    if category not in CATEGORIES:
        raise ValueError(f"Unknown merge category: {category}")


def evaluate_category(category: str, *, approved: bool = False, replaces_approved_mapping: bool = False) -> CategoryDecision:
    validate_category(category)
    if category == "conflict":
        return CategoryDecision(category, True, False, "conflicting text for the same source requirement ID requires explicit approval")
    if category == "removed":
        return CategoryDecision(category, True, False, "removal preserves lineage and requires an approved rationale")
    if category in SEMANTIC_CATEGORIES:
        return CategoryDecision(category, True, approved and not replaces_approved_mapping, "semantic category change requires approval")
    if replaces_approved_mapping:
        return CategoryDecision(category, True, False, "duplication cannot silently replace an approved mapping")
    return CategoryDecision(category, False, True, "non-semantic duplicate is mergeable without category approval")


def can_merge(category: str, *, review_decision: str, replaces_approved_mapping: bool = False) -> CategoryDecision:
    approved = review_decision.strip().lower() == "approved"
    decision = evaluate_category(category, approved=approved, replaces_approved_mapping=replaces_approved_mapping)
    if decision.approval_required and not approved:
        return CategoryDecision(category, True, False, decision.reason)
    return decision
