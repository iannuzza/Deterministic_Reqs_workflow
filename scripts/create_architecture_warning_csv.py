#!/usr/bin/env python3
"""Create a diagnostic CSV for current Architecture Map placement warnings."""

from __future__ import annotations

import csv
from pathlib import Path

from requirement_allocation_policy import requires_hierarchy_parent


WARNING_FIELDS = [
    "warning",
    "requirement_id",
    "review_decision",
    "approved_classification",
    "approved_block",
    "allocation_class",
    "owning_target",
    "allocation_rationale",
    "lineage_mode",
    "source_origin_req_ids",
    "hierarchy_parent_req_ids",
    "owning_domain",
    "reviewer_notes",
]


def create(repo_root: Path) -> Path:
    mapping_path = repo_root / "artifacts/stage1_specs/architecture_mapping_preview.csv"
    output_path = repo_root / "artifacts/stage1_specs/architecture_mapping_warnings.csv"
    with mapping_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    warnings = [
        row for row in rows
        if (row.get("review_decision") or "").strip().casefold() in {"approved", "reassigned"}
        and requires_hierarchy_parent(
            (row.get("allocation_class") or "").strip(),
            (row.get("lineage_mode") or "").strip(),
        )
        and not (row.get("hierarchy_parent_req_ids") or "").strip()
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=WARNING_FIELDS)
        writer.writeheader()
        for row in sorted(warnings, key=lambda item: item.get("requirement_id") or ""):
            writer.writerow({
                "warning": "BLOCKER: hierarchy_parent_req_ids missing; do not infer from approved_block or source type.",
                **{field: row.get(field, "") for field in WARNING_FIELDS[1:]},
            })
    return output_path


if __name__ == "__main__":
    print(create(Path(__file__).resolve().parents[1]))
