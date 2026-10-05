#!/usr/bin/env python3
"""Independently validate final Stage 2A requirement-to-block mappings."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, List

from requirement_corpus import authoritative_corpus_path


STOPWORDS = {
    "shall", "should", "must", "with", "from", "into", "that", "this", "when",
    "where", "which", "their", "there", "have", "been", "being", "block",
    "source", "destination", "requirement", "function", "property", "user",
}


def _tokens(value: str) -> set[str]:
    return {
        token
        for token in re.split(r"[^a-z0-9_\-]+", (value or "").lower())
        if len(token) >= 4 and token not in STOPWORDS
    }


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _split(value: str) -> List[str]:
    return [item.strip() for item in (value or "").split(";") if item.strip()]


def _infer_existing_block_from_source_id(row: Dict[str, str], inventory: Dict[str, Dict[str, str]]) -> str:
    if not (row.get("source_spec") or "").strip():
        return ""
    source_id = re.sub(r"[^a-z0-9]+", "", (row.get("source_req_id") or row.get("id") or "").lower())
    candidates = [
        block_name for block_name in inventory
        if block_name != "Unassigned"
        and re.sub(r"[^a-z0-9]+", "", block_name.lower()) in source_id
    ]
    return max(candidates, key=len, default="")


def _read_aliases(path: Path) -> Dict[str, List[str]]:
    try:
        profile = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    aliases = profile.get("source_section_aliases", {})
    return aliases if isinstance(aliases, dict) else {}


def _read_reviewed_assignments(path: Path) -> Dict[str, str]:
    """Return reviewer-owned block decisions from Architecture Map Review."""
    if not path.exists():
        return {}
    try:
        rows = _read_csv(path)
    except OSError:
        return {}
    return {
        (row.get("requirement_id") or "").strip(): (row.get("approved_block") or "").strip()
        for row in rows
        if (row.get("review_decision") or "").strip().lower() in {"approved", "reassigned"}
        and (row.get("requirement_id") or "").strip()
        and (row.get("approved_block") or "").strip()
    }


def _read_reviewed_top_level_routes(path: Path) -> set[str]:
    """Return approved rows intentionally routed without a concrete block."""
    if not path.exists():
        return set()
    try:
        rows = _read_csv(path)
    except OSError:
        return set()
    top_level_targets = {"srs", "drs", "ars"}
    return {
        (row.get("requirement_id") or "").strip()
        for row in rows
        if (row.get("review_decision") or "").strip().lower() in {"approved", "reassigned"}
        and not (row.get("approved_block") or "").strip()
        and (
            (row.get("owning_target") or "").strip().lower() in top_level_targets
            or (row.get("allocation_class") or "").strip().lower() in {
                "system_level", "top_digital_architecture", "top_analog_architecture"
            }
        )
    }


def _has_explicit_instance_reference(requirement_text: str, block_name: str, aliases: List[str] | None = None) -> bool:
    names = [block_name, *(aliases or [])]
    for name in names:
        if re.search(r"\[\s*TO\s*:\s*" + re.escape(name) + r"\s*\]", requirement_text or "", flags=re.IGNORECASE):
            return True
        instance_name = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
        if not instance_name:
            continue
        pattern = r"\bu_" + r"[_\s]*".join(re.escape(char) for char in instance_name) + r"\b"
        if re.search(pattern, requirement_text or "", flags=re.IGNORECASE):
            return True
    split_source_match = re.search(
        r"\bu_([a-z0-9]+)\s+signal\s+shall\s+be\s+connected\s+to\s+the\s+([a-z0-9]+)\.",
        requirement_text or "",
        flags=re.IGNORECASE,
    )
    return bool(split_source_match and any(
        "".join(split_source_match.groups()).lower()
        == re.sub(r"[^a-z0-9]+", "", name.lower())
        for name in names
    ))


def validate(
    traceability_path: Path,
    inventory_path: Path,
    requirements_path: Path,
    ontology_links_path: Path,
    interaction_path: Path,
    profile_path: Path,
    mapping_preview_path: Path,
) -> List[str]:
    findings: List[str] = []
    traceability = _read_csv(traceability_path)
    inventory_rows = _read_csv(inventory_path)
    requirements = _read_csv(requirements_path)
    ontology_links = _read_csv(ontology_links_path) if ontology_links_path.exists() else []
    interactions = _read_csv(interaction_path)
    aliases = _read_aliases(profile_path)
    reviewed_assignments = _read_reviewed_assignments(mapping_preview_path)
    reviewed_top_level_routes = _read_reviewed_top_level_routes(mapping_preview_path)

    inventory = {
        row.get("Block", ""): row
        for row in inventory_rows
        if row.get("Block", "")
    }
    requirement_map = {
        (row.get("source_req_id") or row.get("id") or "").strip(): row
        for row in requirements
        if (row.get("source_req_id") or row.get("id") or "").strip()
    }
    ontology_by_req: Dict[str, List[Dict[str, str]]] = {}
    for row in ontology_links:
        req_id = row.get("source_req_id", "")
        if req_id:
            ontology_by_req.setdefault(req_id, []).append(row)

    matrix_ids = {
        req_id
        for row in interactions
        for req_id in _split(row.get("Requirement IDs", ""))
    }
    seen: set[str] = set()
    for row in traceability:
        req_id = (row.get("Requirement ID") or "").strip()
        if not req_id:
            findings.append("Final mapping contains a row without Requirement ID")
            continue
        if req_id in seen:
            findings.append(f"Final mapping contains duplicate Requirement ID: {req_id}")
        seen.add(req_id)

        source_row = requirement_map.get(req_id)
        if source_row is None:
            findings.append(f"Final mapping references missing Stage 1 requirement: {req_id}")
            continue
        mapped_blocks = _split(row.get("Block(s)") or row.get("Mapped Block") or "")
        if not mapped_blocks:
            findings.append(f"Final mapping has no block or routing state: {req_id}")
            continue
        if req_id in reviewed_top_level_routes:
            continue
        if mapped_blocks == ["Unassigned"]:
            continue

        requirement_text = source_row.get("requirement_statement", "")
        links = ontology_by_req.get(req_id, [])
        for block_name in mapped_blocks:
            block = inventory.get(block_name)
            if block is None:
                findings.append(f"Final mapping assigns unknown inventory block: {req_id} -> {block_name}")
                continue
            function_text = " ".join(
                [block.get("Function", ""), block.get("Inputs", ""), block.get("Outputs", "")]
            )
            if not function_text.strip():
                findings.append(f"Assigned block has no function/input/output evidence: {req_id} -> {block_name}")
                continue

            # Matrix cells have their own exact source-row/column validation.
            if req_id in matrix_ids:
                continue

            source_owner = source_row.get("source_section_owner", "").strip()
            if not source_owner:
                source_owner = _infer_existing_block_from_source_id(source_row, inventory)
            block_aliases = aliases.get(block_name, [])
            source_context = source_row.get("source", "")
            if source_owner == block_name or any(
                alias.lower() in source_context.lower()
                for alias in block_aliases
                if alias.strip()
            ):
                continue
            if reviewed_assignments.get(req_id) == block_name:
                continue
            if _has_explicit_instance_reference(requirement_text, block_name, block_aliases):
                continue
            configured_names = {
                name.lower().strip()
                for name in [block_name, *aliases.get(block_name, [])]
                if name.strip()
            }
            if any(
                link.get("role", "").lower().strip() in configured_names
                for link in links
            ):
                continue

            evidence_text = " ".join(
                [
                    requirement_text,
                    " ".join(link.get("function_or_property_evidence", "") for link in links),
                ]
            )
            overlap = _tokens(evidence_text) & _tokens(function_text)
            if len(overlap) < 2:
                findings.append(
                    f"Final mapping lacks semantic function support: {req_id} -> {block_name} "
                    f"(overlap={len(overlap)})"
                )

    expected_ids = set(requirement_map)
    missing_ids = sorted(expected_ids - seen)
    for req_id in missing_ids:
        findings.append(f"Stage 1 requirement missing from final mapping: {req_id}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate final Stage 2A mappings against inventory and ontology evidence")
    parser.add_argument("--traceability", default="artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv")
    parser.add_argument("--inventory", default="artifacts/stage2_mirco_arc/block_inventory.csv")
    parser.add_argument(
        "--requirements",
        default=None,
        help="Optional compatibility override; otherwise use the authoritative corpus resolver.",
    )
    parser.add_argument("--ontology-links", default="artifacts/stage0_ontology/ontology_requirement_links.csv")
    parser.add_argument("--interactions", default="artifacts/stage2_mirco_arc/interaction_matrix.csv")
    parser.add_argument("--profile", default="config/stage2_mirco_arc_profile.json")
    parser.add_argument("--mapping-preview", default="artifacts/stage1_specs/architecture_mapping_preview.csv")
    parser.add_argument("--report", default="artifacts/stage2_mirco_arc/stage2_mapping_crosscheck_report.md")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    requirements_path = (
        root / Path(args.requirements)
        if args.requirements
        else authoritative_corpus_path(root)
    )
    paths = [root / Path(value) for value in (
        args.traceability, args.inventory, requirements_path, args.ontology_links, args.interactions
    )]
    report_path = root / Path(args.report)
    required = paths[:3] + [paths[4]]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        print("Stage 2A post-mapping semantic crosscheck: FAIL")
        for path in missing:
            print(f"- missing: {path}")
        report_path.write_text("# Stage 2A Post-Mapping Semantic Crosscheck\n\n- Status: FAIL\n", encoding="utf-8")
        return 1
    findings = validate(
        paths[0], paths[1], paths[2], paths[3], paths[4],
        root / Path(args.profile), root / Path(args.mapping_preview),
    )
    if findings:
        print("Stage 2A post-mapping semantic crosscheck: FAIL")
        for finding in findings:
            print(f"- {finding}")
        report_path.write_text(
            "# Stage 2A Post-Mapping Semantic Crosscheck\n\n- Status: FAIL\n\n"
            + "\n".join(f"- {finding}" for finding in findings)
            + "\n",
            encoding="utf-8",
        )
        return 1
    report_path.write_text(
        "# Stage 2A Post-Mapping Semantic Crosscheck\n\n"
        "- Status: PASS\n"
        "- Final requirement-to-block mappings have known inventory owners and semantic function/property support.\n",
        encoding="utf-8",
    )
    print("Stage 2A post-mapping semantic crosscheck: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
