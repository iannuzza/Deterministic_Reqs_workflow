"""Project-configurable traceability and upstream-reference rules."""

from __future__ import annotations

import re
from pathlib import Path


_ID_RE = re.compile(r"^[A-Z][A-Z0-9_-]*$")
def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _source_name(value: str) -> str:
    return Path((value or "").replace("\\", "/")).name.casefold()


def is_direct_upstream_source_id(value: str) -> bool:
    """Classify supplementary IDs by their reference to an approved device block."""
    candidate = (value or "").strip()
    if not candidate:
        return False
    inventory_path = _repo_root() / "artifacts" / "stage2_mirco_arc" / "block_inventory.csv"
    try:
        import csv
        candidate_tokens = re.findall(r"[a-z0-9]+", candidate.casefold())
        with inventory_path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                block = (row.get("Block") or "").strip()
                entity_kind = (row.get("Entity kind") or "concrete_block").strip().casefold()
                if not block or block.casefold() == "unassigned" or entity_kind != "concrete_block":
                    continue
                block_tokens = re.findall(r"[a-z0-9]+", block.casefold())
                width = len(block_tokens)
                if width and any(candidate_tokens[index:index + width] == block_tokens for index in range(len(candidate_tokens) - width + 1)):
                    return True
    except OSError:
        return False
    return False


def is_valid_upstream_reference(value: str) -> bool:
    """Validate one Covers reference without coupling it to a project ID namespace."""
    candidate = (value or "").strip()
    if not candidate or candidate.lower() == "none" or ";" in candidate or "," in candidate:
        return False
    return bool(_ID_RE.fullmatch(candidate)) and (
        bool(re.fullmatch(r"SRS-REQ-\d+", candidate, re.IGNORECASE))
        or is_direct_upstream_source_id(candidate)
    )


def is_srs_requirement_id(value: str) -> bool:
    return bool(re.fullmatch(r"SRS-REQ-\d+", (value or "").strip(), re.IGNORECASE))
