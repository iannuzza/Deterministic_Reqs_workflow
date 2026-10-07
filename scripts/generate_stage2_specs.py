#!/usr/bin/env python3
"""Generate Stage 2 specification baseline artifacts from Stage 1 requirements.

Outputs:
- artifacts/stage1_specs/specs.md
- artifacts/stage1_specs/traceability_seed.csv
- artifacts/orchestrator/stage_02_report.md
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
from repo_paths import portable_repo_path, resolve_repo_path
import re
import subprocess
import sys
from collections import Counter, defaultdict
from typing import Dict, List, Set
from openpyxl import Workbook, load_workbook
from mapping_review_sync import sync_mapping_workbook_to_csv
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Alignment, Font, PatternFill, Protection
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter
from workflow_routing import source_parent_title
from requirement_corpus import authoritative_corpus_path
from canonical_store import connect


PROJECT_CONTEXT = Path("config/project_context.json")


def _configured_path(repo_root: Path, context: Dict[str, object], key: str, default: str) -> Path:
    return resolve_repo_path(repo_root, str(context.get(key, default)))


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\n")


def _read_requirements(summary_csv: Path) -> List[Dict[str, str]]:
    if not summary_csv.exists():
        raise FileNotFoundError(f"Stage 1 requirements summary not found: {summary_csv}")

    with summary_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [{k: (v or "").strip() for k, v in row.items()} for row in reader]

    if not rows:
        raise ValueError("Stage 1 requirements summary is empty")

    for required in ("id", "requirement_statement", "source", "requirement_type"):
        if required not in (reader.fieldnames or []):
            raise ValueError(f"Missing required column in summary CSV: {required}")

    return rows


def _read_csv_optional(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def _read_source_matrix_edges(path: Path) -> Dict[str, List[str]]:
    """Read exact source connection endpoints keyed by source requirement ID."""
    edges: Dict[str, List[str]] = defaultdict(list)
    for row in _read_csv_optional(path):
        req_id = (row.get("source_req_id") or "").strip()
        if not req_id:
            continue
        for field in ("from_block", "to_block"):
            block = (row.get(field) or "").strip()
            if block and block not in edges[req_id]:
                edges[req_id].append(block)
    return dict(edges)


def _read_previous_blocks_by_requirement(path: Path) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for row in _read_csv_optional(path):
        requirement_id = (
            row.get("Requirement ID")
            or row.get("source_req_id")
            or row.get("requirement_id")
            or row.get("canonical_id")
            or ""
        ).strip()
        block = (
            row.get("Block(s)")
            or row.get("block")
            or row.get("Block")
            or row.get("approved_block")
            or ""
        ).strip()
        if requirement_id and block:
            result[requirement_id] = block
    return result


def _is_concrete_profile_entity(block_name: str, metadata: object) -> bool:
    if not block_name or block_name == "Unassigned":
        return False
    return not (
        isinstance(metadata, dict)
        and str(metadata.get("entity_kind") or "").strip().lower()
        not in {"", "concrete_block"}
    )


def _cascade_previous_concrete_owners(
    preview_owner_ids: Dict[str, List[str]],
    previous_blocks_by_requirement: Dict[str, str],
    block_defs: Dict[str, object],
) -> int:
    cascaded = 0
    for req_id, previous_owner in previous_blocks_by_requirement.items():
        if not _is_concrete_profile_entity(previous_owner, block_defs.get(previous_owner)):
            continue
        current_owners = [owner for owner, req_ids in preview_owner_ids.items() if req_id in req_ids]
        if current_owners == [previous_owner]:
            continue
        for owner in current_owners:
            preview_owner_ids[owner] = [item for item in preview_owner_ids[owner] if item != req_id]
        if req_id not in preview_owner_ids[previous_owner]:
            preview_owner_ids[previous_owner].append(req_id)
        cascaded += 1
    return cascaded


def _ensure_previous_concrete_owner_defs(
    block_defs: Dict[str, object],
    previous_blocks_by_requirement: Dict[str, str],
) -> int:
    added = 0
    for previous_owner in sorted(set(previous_blocks_by_requirement.values()), key=str.lower):
        if not previous_owner or previous_owner == "Unassigned" or previous_owner in block_defs:
            continue
        block_defs[previous_owner] = {
            "function": "Concrete owner inherited from the approved upstream traceability artifact; review can refine this block description.",
            "inputs": "User review required: confirm source-backed inputs.",
            "outputs": "User review required: confirm source-backed outputs.",
            "candidate_requirement_count": sum(1 for owner in previous_blocks_by_requirement.values() if owner == previous_owner),
            "candidate_relations": {},
        }
        added += 1
    return added


def _sha256_file(path: Path) -> str:
    if not path.exists():
        return "missing"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _draft_review_sha256(draft: Dict[str, object]) -> str:
    stable = json.loads(json.dumps(draft, sort_keys=True))
    approval = stable.get("approval", {})
    if isinstance(approval, dict):
        approval["status"] = ""
        approval["approved_by"] = ""
        approval["approved_at"] = ""
        approval["reviewer_notes"] = ""
        approval["reviewed_draft_profile_sha256"] = ""
        approval["reviewed_mapping_preview_csv_sha256"] = ""
    review_package = stable.get("review_package", {})
    if isinstance(review_package, dict):
        review_package["draft_profile_sha256"] = ""
    encoded = json.dumps(stable, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _normalized_req_id(row: Dict[str, str]) -> str:
    return (row.get("source_req_id") or row.get("id") or "").strip()


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def _tokenize_text(text: str) -> List[str]:
    return [token for token in re.split(r"[^a-z0-9_\-]+", text.lower()) if token]


def _infer_supplementary_owner(row: Dict[str, str], block_defs: Dict[str, object]) -> str:
    """Infer an owner from a tagged supplementary ID when source metadata is absent."""
    if (row.get("source_section_owner") or "").strip():
        return (row.get("source_section_owner") or "").strip()
    req_id = (row.get("source_req_id") or row.get("id") or "").strip().lower()
    if not (row.get("source_spec") or "").strip():
        return ""
    normalized_id = re.sub(r"[^a-z0-9]+", "", req_id)
    candidates = [
        block_name
        for block_name in block_defs
        if block_name != "Unassigned"
        and re.sub(r"[^a-z0-9]+", "", block_name.lower()) in normalized_id
    ]
    return max(candidates, key=len, default="")


def _infer_block_classification(
    row: Dict[str, str], block_name: str, block_defs: Dict[str, object]
) -> str:
    """Classify a mapped supplementary requirement from configured block evidence."""
    current = (row.get("category") or "").strip().title()
    if current in {"Analog", "Digital", "System"}:
        return current
    definition = block_defs.get(block_name, {})
    if isinstance(definition, dict):
        configured = str(definition.get("classification") or "").strip().title()
        if configured in {"Analog", "Digital", "System"}:
            return configured
        evidence = " ".join(str(definition.get(key) or "") for key in ("function", "inputs", "outputs"))
    else:
        evidence = ""
    evidence = f"{evidence} {row.get('requirement_statement', '')}".lower()
    analog_terms = {"analog", "afe", "sensor", "transducer", "bias", "amplifier", "adc", "dac"}
    digital_terms = {"digital", "register", "state", "control", "logic", "bus", "fifo", "timer", "irq", "firmware", "routing"}
    analog_score = sum(evidence.count(term) for term in analog_terms)
    digital_score = sum(evidence.count(term) for term in digital_terms)
    if analog_score or digital_score:
        return "Analog" if analog_score > digital_score else "Digital"
    return "System"


def _read_profile_block_defs(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    block_defs = data.get("block_defs", {}) if isinstance(data, dict) else {}
    return block_defs if isinstance(block_defs, dict) else {}


def _read_profile_source_section_aliases(path: Path) -> Dict[str, List[str]]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    aliases = data.get("source_section_aliases", {}) if isinstance(data, dict) else {}
    if not isinstance(aliases, dict):
        return {}
    return {
        str(block): [str(alias) for alias in values if isinstance(alias, str)]
        for block, values in aliases.items()
        if isinstance(values, list)
    }


def _is_generic_source_paragraph(row: Dict[str, str], block_defs: Dict[str, object]) -> bool:
    source = (row.get("source") or "").strip().lower()
    if not source:
        return True

    block_terms = [block_name for block_name in block_defs if block_name != "Unassigned"]
    source_key = re.sub(r"[^a-z0-9]+", "", source)
    source_section_owner = (row.get("source_section_owner") or "").strip()
    dedicated_source_terms = (
        "bist", "scan", "debug", "dft", "test mode", "adc test", "pad mux",
        "power-up", "power up", "power-down", "power down", "boot", "configuration",
    )
    if source_section_owner in block_defs and source_section_owner != "Unassigned":
        parent_title = source_parent_title(source).lower()
        parent_key = re.sub(r"[^a-z0-9]+", "", parent_title)
        owner_key = re.sub(r"[^a-z0-9]+", "", source_section_owner.lower())
        if owner_key and owner_key in parent_key:
            return False
        parent_tokens = set(_tokenize_text(parent_title))
        owner_tokens = set(_tokenize_text(source_section_owner))
        if owner_tokens and owner_tokens.issubset(parent_tokens):
            return False
        if "(under section" in source and parent_title != "other source function context":
            return True
    if "(under section" in source and any(term in source for term in dedicated_source_terms):
        return True
    return not any(
        len(re.sub(r"[^a-z0-9]+", "", term.lower())) >= 3
        and re.sub(r"[^a-z0-9]+", "", term.lower()) in source_key
        for term in block_terms
    )


def _preview_blocks_for_requirement(
    row: Dict[str, str],
    candidate_blocks: List[str],
    profile_block_defs: Dict[str, object],
    source_section_aliases: Dict[str, List[str]] | None = None,
    source_matrix_edges: Dict[str, List[str]] | None = None,
) -> List[str]:
    if not profile_block_defs:
        return candidate_blocks or ["Unassigned"]
    source = (row.get("source") or "").strip().lower()
    req_id = _normalized_req_id(row)
    matrix_context = " ".join(
        [source, (row.get("requirement_statement") or "").strip().lower()]
    )
    if req_id in (source_matrix_edges or {}) or "connection matrix" in matrix_context or "xbar" in matrix_context:
        # Matrix ownership is represented by the exact interaction edge, not
        # by assigning a multi-endpoint requirement to one review block.
        return ["Unassigned"]
    dedicated_source_terms = (
        "bist", "scan", "debug", "dft", "test mode", "adc test", "pad mux",
        "power-up", "power up", "power-down", "power down", "boot", "configuration",
    )

    # Dedicated test/DFT paragraphs describe a procedure affecting a block;
    # they do not establish ownership of that affected block. Keep them as
    # source context until the reviewer assigns a hierarchy owner.
    if (
        "(under section" in source
        and any(term in source for term in ("adc test", "digital dft"))
    ):
        return [source_parent_title(row.get("source") or "")]

    concrete_profile_blocks = {
        name for name, metadata in profile_block_defs.items()
        if _is_concrete_profile_entity(name, metadata)
    }
    owner = (row.get("source_section_owner") or "").strip()
    if owner in concrete_profile_blocks:
        return [owner]

    source_section_aliases = source_section_aliases or {}
    target_match = re.search(r"\[to:\s*([^\]]+)\]", row.get("requirement_statement", ""), flags=re.IGNORECASE)
    if target_match:
        target = re.sub(r"[^a-z0-9]+", "", target_match.group(1).lower())
        target_matches = [
            block_name
            for block_name, aliases in source_section_aliases.items()
            if block_name in concrete_profile_blocks
            and any(re.sub(r"[^a-z0-9]+", "", alias.lower()) == target for alias in aliases)
        ]
        if len(target_matches) == 1:
            return target_matches
    source_alias_matches = [
        block_name
        for block_name, aliases in source_section_aliases.items()
        if block_name in concrete_profile_blocks
        and any(alias.strip().lower() in source for alias in aliases if alias.strip())
    ]
    if len(source_alias_matches) == 1:
        return source_alias_matches

    filtered = [block for block in candidate_blocks if block in concrete_profile_blocks]
    if filtered:
        return sorted(set(filtered))

    if "(under section" in source and any(term in source for term in dedicated_source_terms):
        return [source_parent_title(row.get("source") or "")]

    if _is_generic_source_paragraph(row, profile_block_defs):
        return [source_parent_title(row.get("source") or "")]

    return ["Unassigned"]


def _issue_is_extraction_completeness(text: str) -> bool:
    low = text.lower()
    return (
        "text, table, and figure extraction completeness" in low
        or "extraction completeness" in low
        or "table extraction completeness" in low
        or "figure extraction completeness" in low
    )


def _parse_semantic_issues(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    issues: List[Dict[str, str]] = []
    severity = ""
    issue_index = 1
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        heading = re.match(r"^##\s+(Critical|Major|Minor)\s*$", line, flags=re.IGNORECASE)
        if heading:
            severity = heading.group(1).lower()
            continue
        if line.startswith("## "):
            severity = ""
            continue
        if not severity or not line.startswith("- "):
            continue
        text = line[2:].strip()
        if not text or text.lower() == "none" or _issue_is_extraction_completeness(text):
            continue
        req_match = re.match(r"([A-Za-z0-9_\-]+):\s*(.*)", text)
        issues.append(
            {
                "issue_id": f"SEM-{issue_index:03d}",
                "severity": severity,
                "requirement_id": req_match.group(1) if req_match else "",
                "description": req_match.group(2) if req_match else text,
                "required_for_approval": "yes" if severity in {"critical", "major"} else "no",
                "disposition": "pending" if severity in {"critical", "major"} else "informational",
                "rationale": "",
            }
        )
        issue_index += 1
    return issues


def _write_csv(path: Path, header: List[str], rows: List[List[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def _join_unique(values: List[str]) -> str:
    unique: List[str] = []
    seen = set()
    for value in values:
        clean = _normalize_text(value)
        if clean and clean not in seen:
            seen.add(clean)
            unique.append(clean)
    return "; ".join(unique)


def _brief_evidence(values: List[str], limit: int = 3) -> str:
    return _join_unique(values[:limit])


def _read_supplementary_review(repo_root: Path, approved_classifications: Dict[str, str] | None = None) -> Dict[str, Dict[str, str]]:
    """Load the newest supplementary review decision for each source requirement."""
    candidates = sorted(
        (path for path in (repo_root / "artifacts/source_ingestion").glob("*/comparison_results.csv")),
        key=lambda path: path.stat().st_mtime,
    )
    decisions: Dict[str, Dict[str, str]] = {}
    for path in candidates:
        for row in _read_csv_optional(path):
            source_id = (row.get("source_req_id") or "").strip()
            if source_id:
                decisions[source_id] = {
                    "source_review_decision": (row.get("review_decision") or "").strip().lower(),
                    "source_classification": (row.get("classification") or (approved_classifications or {}).get(source_id, "")).strip().lower(),
                    "supplementary_staged_id": (row.get("staged_id") or "").strip(),
                    "supplementary_source_spec": (row.get("source_spec") or "").strip(),
                    "supplementary_source_page": (row.get("source_page") or "").strip(),
                    "supplementary_source_chunk_id": (row.get("source_chunk_id") or "").strip(),
                }
    return decisions


def _approved_classifications(repo_root: Path) -> Dict[str, str]:
    """Load approved canonical classifications; staged CSV categories are not authority."""
    context_path = repo_root / "config/project_context.json"
    context = json.loads(context_path.read_text(encoding="utf-8")) if context_path.exists() else {}
    project_id = str(context.get("project_name") or repo_root.name)
    connection = connect(repo_root)
    try:
        rows = connection.execute(
            """SELECT cr.source_req_id, crr.approved_classification
                 FROM canonical_requirements cr
                 JOIN canonical_requirement_revisions crr ON crr.revision_id = cr.current_revision_id
                WHERE cr.project_id = ? AND crr.lifecycle_state = 'approved'
                  AND crr.approved_classification IS NOT NULL""",
            (project_id,),
        ).fetchall()
        return {str(row[0]).strip(): str(row[1]).strip() for row in rows if row[0] and row[1]}
    finally:
        connection.close()


def _write_mapping_preview(
    path: Path,
    block_defs: Dict[str, object],
    preview_owner_ids: Dict[str, List[str]],
    requirements_by_id: Dict[str, Dict[str, str]],
    previous_blocks_by_requirement: Dict[str, str],
    supplementary_review: Dict[str, Dict[str, str]],
    approved_classifications: Dict[str, str],
    source_section_aliases: Dict[str, List[str]],
) -> None:
    rows: List[List[str]] = []
    for block_name in sorted(preview_owner_ids, key=str.lower):
        req_ids = sorted(set(preview_owner_ids[block_name]))
        meta = block_defs.get(block_name, {})
        is_source_context = block_name not in block_defs or block_name == "Unassigned"
        function_text = meta.get("function", "") if isinstance(meta, dict) else ""
        inputs = meta.get("inputs", "") if isinstance(meta, dict) else ""
        outputs = meta.get("outputs", "") if isinstance(meta, dict) else ""
        if is_source_context:
            function_text = f"Source parent paragraph context: {block_name}"
            inputs = "N/A"
            outputs = "N/A"
        for req_id in req_ids:
            row = requirements_by_id.get(req_id, {})
            statement = _normalize_text(row.get("requirement_statement", ""))
            source = _normalize_text(row.get("source", ""))
            review_meta = supplementary_review.get(req_id, {})
            classification = (
                review_meta.get("source_classification")
                or approved_classifications.get(req_id)
                or _infer_block_classification(row, block_name, block_defs)
            ).strip().title()
            approved_classification = (
                approved_classifications.get(req_id)
                or _infer_block_classification(row, block_name, block_defs)
            ).strip().title()
            if approved_classification not in {"Analog", "Digital", "System"}:
                approved_classification = "System"
            if is_source_context:
                paragraph = (
                    f"Retain {req_id} under source parent paragraph '{block_name}' pending reviewer block ownership decision: "
                    f"{statement}"
                )
            else:
                paragraph = (
                    f"The {block_name} block shall implement the source-backed behavior described by {req_id}: "
                    f"{statement}"
                )
            unresolved_source_paragraph = block_name.strip().lower() == "unresolved source paragraph"
            previous_owner = previous_blocks_by_requirement.get(req_id, "").strip()
            preserve_previous_review = (
                not is_source_context
                and previous_owner in block_defs
                and previous_owner != "Unassigned"
                and not unresolved_source_paragraph
            )
            target_match = re.search(r"\[to:\s*([^\]]+)\]", statement, flags=re.IGNORECASE)
            explicit_target_approval = False
            if target_match and not is_source_context and not unresolved_source_paragraph:
                target = re.sub(r"[^a-z0-9]+", "", target_match.group(1).lower())
                explicit_target_approval = any(
                    block_name == candidate
                    and any(re.sub(r"[^a-z0-9]+", "", alias.lower()) == target for alias in aliases)
                    for candidate, aliases in source_section_aliases.items()
                    if candidate in block_defs and candidate != "Unassigned"
                )
            source_alias_approval = False
            if not is_source_context and not unresolved_source_paragraph:
                source_text = re.sub(r"[^a-z0-9]+", "", source.lower())
                source_alias_approval = any(
                    block_name == candidate
                    and re.sub(r"[^a-z0-9]+", "", alias.lower()) in source_text
                    for candidate, aliases in source_section_aliases.items()
                    if candidate in block_defs and candidate != "Unassigned"
                    for alias in aliases
                    if alias.strip()
                )
            review_decision = "pending_review"
            rows.append(
                [
                    "" if unresolved_source_paragraph else block_name,
                    req_id,
                    statement,
                    source,
                    function_text,
                    inputs,
                    outputs,
                    paragraph,
                    classification,
                    approved_classification,
                    review_decision,
                    "" if (unresolved_source_paragraph or is_source_context) else block_name,
                    "",
                    "",
                    "",
                    "normal_hierarchical",
                    req_id,
                    "",
                    "",
                    classification,
                    "",
                    row.get("canonical_id") or row.get("id") or req_id,
                    review_meta.get("source_review_decision", ""),
                    review_meta.get("source_classification", ""),
                    review_meta.get("supplementary_staged_id", ""),
                    review_meta.get("supplementary_source_spec", ""),
                    review_meta.get("supplementary_source_page", ""),
                    review_meta.get("supplementary_source_chunk_id", ""),
                ]
            )
    _write_csv(
        path,
        [
            "candidate_block",
            "requirement_id",
            "requirement_statement",
            "source",
            "function_preview",
            "inputs_preview",
            "outputs_preview",
            "generated_block_paragraph_preview",
            "candidate_classification",
            "approved_classification",
            "review_decision",
            "approved_block",
            "allocation_class",
            "owning_target",
            "allocation_rationale",
            "lineage_mode",
            "source_origin_req_ids",
            "hierarchy_parent_req_ids",
            "lineage_candidate_parent_req_ids",
            "owning_domain",
            "reviewer_notes",
            "canonical_requirement_id",
            "source_review_decision",
            "source_classification",
            "supplementary_staged_id",
            "supplementary_source_spec",
            "supplementary_source_page",
            "supplementary_source_chunk_id",
        ],
        rows,
    )


def _read_existing_mapping_metadata(path: Path) -> Dict[str, Dict[str, str]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return {
            (row.get("requirement_id") or "").strip(): row
            for row in csv.DictReader(handle)
            if (row.get("requirement_id") or "").strip()
        }


def _prefill_mapping_allocations(
    path: Path,
    existing: Dict[str, Dict[str, str]],
    profile_block_defs: Dict[str, object],
) -> tuple[int, int]:
    """Apply deterministic allocation defaults while leaving review decisions user-controlled."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    filled = 0
    review = 0
    for row in rows:
        req_id = (row.get("requirement_id") or "").strip()
        prior = existing.get(req_id, {})
        prior_block = (prior.get("approved_block") or "").strip()
        prior_block_is_concrete = (
            not prior_block
            or prior_block.casefold() in {"system", "digital", "analog", "unassigned"}
            or (
                _is_concrete_profile_entity(prior_block, profile_block_defs.get(prior_block))
            )
        )
        for field in (
            "approved_classification",
            "approved_block",
            "allocation_class",
            "owning_target",
            "allocation_rationale",
            "lineage_mode",
            "source_origin_req_ids",
            "hierarchy_parent_req_ids",
            "lineage_candidate_parent_req_ids",
            "owning_domain",
            "reviewer_notes",
        ):
            if (
                prior_block_is_concrete
                and not (row.get(field) or "").strip()
                and (prior.get(field) or "").strip()
            ):
                row[field] = prior[field]
        prior_decision = (prior.get("review_decision") or "").strip() if prior_block_is_concrete else "pending_review"
        if prior_decision:
            row["review_decision"] = prior_decision
        elif (row.get("review_decision") or "").strip().casefold() in {"", "pending"}:
            row["review_decision"] = "pending_review"
        source = (row.get("source") or "").casefold()
        block = (row.get("approved_block") or "").strip()
        classification = (row.get("approved_classification") or "").casefold()
        decision = ""
        rationale = ""
        if "xbar connection matrix" in source:
            decision = "top_digital_architecture"
            rationale = "Digital source-to-destination connection contract between architectural blocks; owned by DRS."
        elif classification == "digital" and block:
            concrete_block = _is_concrete_profile_entity(block, profile_block_defs)
            if concrete_block and any(term in source for term in ("time slot", "select channel", "select division", "configure adc", "general config", "ppg frames", "select operative mode", "check data", "soft reset")):
                decision = "block_local_digital"
                rationale = "Requirement defines implementation behavior local to the approved digital block; owned by Digital IPOS."
            elif "peculiar requirements" in source and concrete_block:
                decision = "block_local_digital"
                rationale = "Requirement is explicitly defined in the approved block-specific requirements section; owned by Digital IPOS."
            elif concrete_block and any(term in source for term in ("boot phase", "otp boot routine")):
                decision = "block_local_digital"
                rationale = "Requirement defines OTP block implementation behavior; owned by Digital IPOS."
            elif any(term in source for term in ("clocks and reset", "16 mhz", "32 khz", "64 khz")):
                decision = "top_digital_architecture"
                rationale = "Shared clock/reset coordination across architectural blocks; owned by DRS."
        if decision:
            target = "Digital IPOS" if decision == "block_local_digital" else "DRS"
            changed = False
            if not (row.get("allocation_class") or "").strip():
                row["allocation_class"] = decision
                changed = True
            if not (row.get("owning_target") or "").strip():
                row["owning_target"] = target
                changed = True
            if not (row.get("allocation_rationale") or "").strip():
                row["allocation_rationale"] = rationale
                changed = True
            if not (row.get("lineage_mode") or "").strip():
                row["lineage_mode"] = "normal_hierarchical"
                changed = True
            if changed:
                filled += 1
        else:
            review += 1
            if not (row.get("allocation_rationale") or "").strip():
                row["allocation_rationale"] = "REVIEW_REQUIRED: explicit user allocation decision required."
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return filled, review


def _write_mapping_preview_markdown(csv_path: Path) -> None:
    """Render the human-readable preview from the authoritative review CSV."""
    rows = _read_csv_optional(csv_path)
    grouped: Dict[str, List[str]] = defaultdict(list)
    for row in rows:
        candidate = (row.get("candidate_block") or "Unassigned").strip() or "Unassigned"
        requirement_id = (row.get("requirement_id") or "").strip()
        if requirement_id:
            grouped[candidate].append(requirement_id)
    lines = [
        "# Architecture Mapping Preview",
        "",
        "This report is derived from `architecture_mapping_preview.csv`; review decisions remain authoritative in the CSV/workbook.",
        "",
        "| Candidate block/context | Requirement count | Requirement IDs |",
        "| --- | ---: | --- |",
    ]
    for candidate in sorted(grouped, key=str.casefold):
        requirement_ids = sorted(set(grouped[candidate]))
        lines.append(f"| {candidate} | {len(requirement_ids)} | {', '.join(requirement_ids)} |")
    csv_path.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_mapping_workbook(csv_path: Path) -> Path:
    """Create the editable workbook paired with the authoritative review CSV."""
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    workbook = Workbook()
    workbook.calculation.fullCalcOnLoad = True
    workbook.calculation.forceFullCalc = True
    workbook.calculation.calcMode = "auto"
    worksheet = workbook.active
    worksheet.title = "Architecture Mapping Review"
    worksheet.protection.sheet = False
    for row in rows:
        worksheet.append(row)
    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions
    header_fill = PatternFill("solid", fgColor="1F4E78")
    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    headers = [str(cell.value or "").strip() for cell in worksheet[1]]
    editable_fields = {
        "approved_classification",
        "review_decision",
        "approved_block",
        "allocation_class",
        "owning_target",
        "allocation_rationale",
        "lineage_mode",
        "source_origin_req_ids",
        "hierarchy_parent_req_ids",
        "lineage_candidate_parent_req_ids",
        "owning_domain",
        "reviewer_notes",
    }
    approved_fill = PatternFill("solid", fgColor="C6EFCE")
    pending_fill = PatternFill("solid", fgColor="FFC7CE")
    decision_column_letter = get_column_letter(headers.index("review_decision") + 1) if "review_decision" in headers else ""
    for row in worksheet.iter_rows(min_row=2):
        row_decision = str(row[headers.index("review_decision")].value or "").strip().casefold() if "review_decision" in headers else ""
        row_fill = approved_fill if row_decision == "approved" else pending_fill
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if cell.column <= len(headers) and headers[cell.column - 1] in editable_fields:
                cell.fill = row_fill
                cell.protection = Protection(locked=False)
    row_valid_formula = None
    if all(field in headers for field in (
        "approved_classification",
        "approved_block",
        "review_decision",
        "allocation_class",
        "owning_target",
        "allocation_rationale",
        "lineage_mode",
    )):
        classification_column = get_column_letter(headers.index("approved_classification") + 1)
        block_column = get_column_letter(headers.index("approved_block") + 1)
        allocation_column = get_column_letter(headers.index("allocation_class") + 1)
        target_column = get_column_letter(headers.index("owning_target") + 1)
        rationale_column = get_column_letter(headers.index("allocation_rationale") + 1)
        lineage_column = get_column_letter(headers.index("lineage_mode") + 1)
        approved_formula = (
            f'AND(${decision_column_letter}2="approved",'
            f'OR(${classification_column}2="Analog",${classification_column}2="Digital",${classification_column}2="System"),'
            f'${block_column}2<>"",'
            f'OR(${allocation_column}2="system_level",${allocation_column}2="top_digital_architecture",'
            f'${allocation_column}2="top_analog_architecture",${allocation_column}2="block_local_digital",'
            f'${allocation_column}2="block_local_analog",${allocation_column}2="descriptive_only"),'
            f'OR(AND(${allocation_column}2="system_level",${target_column}2="SRS"),'
            f'AND(${allocation_column}2="top_digital_architecture",${target_column}2="DRS"),'
            f'AND(${allocation_column}2="top_analog_architecture",${target_column}2="ARS"),'
            f'AND(${allocation_column}2="block_local_digital",${target_column}2="Digital IPOS"),'
            f'AND(${allocation_column}2="block_local_analog",${target_column}2="Analog IPOS"),'
            f'AND(${allocation_column}2="descriptive_only",${target_column}2="none")),'
            f'${rationale_column}2<>"",LEFT(${rationale_column}2,16)<>"REVIEW_REQUIRED:",'
            f'${lineage_column}2<>"",'
            f'NOT(AND(OR(${block_column}2="System",${block_column}2="Digital",${block_column}2="Analog"),'
            f'${block_column}2<>${classification_column}2)))'
        )
        not_approved_formula = f'NOT({approved_formula})'
        for field_name in editable_fields:
            field_column = get_column_letter(headers.index(field_name) + 1)
            field_range = f"{field_column}2:{field_column}{worksheet.max_row}"
            worksheet.conditional_formatting.add(
                field_range,
                FormulaRule(formula=[approved_formula], fill=approved_fill, stopIfTrue=True),
            )
            worksheet.conditional_formatting.add(
                field_range,
                FormulaRule(formula=[not_approved_formula], fill=pending_fill),
            )
    for column in worksheet.columns:
        width = min(max(len(str(cell.value or "")) for cell in column) + 2, 60)
        worksheet.column_dimensions[get_column_letter(column[0].column)].width = max(width, 12)
    worksheet.row_dimensions[1].height = 30

    approved_blocks = []
    approved_block_list = csv_path.parents[0] / "approved_block_list.xlsx"
    if approved_block_list.exists():
        reference_workbook = load_workbook(approved_block_list, read_only=True, data_only=True)
        try:
            reference_sheet = reference_workbook.active
            for row in reference_sheet.iter_rows(min_row=2, values_only=True):
                block_name = str(row[0] or "").strip() if row else ""
                if block_name and block_name.casefold() not in {"unassigned", "needs_clarification"}:
                    approved_blocks.append(block_name)
        finally:
            reference_workbook.close()
    approved_blocks = sorted(set(approved_blocks), key=str.casefold)
    choices = workbook.create_sheet("Approved Block Choices")
    choices.append([
        "approved_block choices",
        "approved_classification choices",
        "allocation_class choices",
        "owning_target choices",
        "allocation_rationale choices",
        "lineage_mode choices",
        "review_decision choices",
    ])
    for top_level in ("System", "Digital", "Analog"):
        choices.append([top_level])
    for block_name in approved_blocks:
        choices.append([block_name])
    choices.sheet_state = "hidden"
    classifications = ("System", "Digital", "Analog")
    for row_index, classification in enumerate(classifications, start=2):
        choices.cell(row=row_index, column=2, value=classification)

    allocation_classes = (
        "system_level",
        "top_digital_architecture",
        "top_analog_architecture",
        "block_local_digital",
        "block_local_analog",
        "descriptive_only",
    )
    owning_targets = (
        "SRS",
        "DRS",
        "ARS",
        "Digital IPOS",
        "Analog IPOS",
        "none",
    )
    rationale_templates = (
        "System-level behavior; owned by SRS.",
        "Top-level digital architecture or inter-block digital coordination; owned by DRS.",
        "Top-level analog or mixed-signal architecture; owned by ARS.",
        "Digital behavior local to the approved block; owned by Digital IPOS.",
        "Analog behavior local to the approved block; owned by Analog IPOS.",
        "Descriptive content only; no implementation target.",
    )
    lineage_modes = (
        "normal_hierarchical",
        "direct_source_to_ipos",
        "direct_supplementary_to_ipos",
        "split_lineage",
    )
    review_decisions = (
        "pending_review",
        "approved",
        "reassigned",
        "rejected",
        "needs_clarification",
    )
    for row_index, value in enumerate(allocation_classes, start=2):
        choices.cell(row=row_index, column=3, value=value)
    for row_index, value in enumerate(owning_targets, start=2):
        choices.cell(row=row_index, column=4, value=value)
    for row_index, value in enumerate(rationale_templates, start=2):
        choices.cell(row=row_index, column=5, value=value)
    for row_index, value in enumerate(lineage_modes, start=2):
        choices.cell(row=row_index, column=6, value=value)
    for row_index, value in enumerate(review_decisions, start=2):
        choices.cell(row=row_index, column=7, value=value)

    baseline = workbook.create_sheet("Review Baseline")
    baseline_headers = headers
    baseline.append(baseline_headers)
    baseline_rows = {}
    for row_index, source_row in enumerate(rows[1:], start=2):
        record = dict(zip(headers, source_row))
        requirement_id = str(record.get("requirement_id") or "").strip()
        baseline_rows[requirement_id] = row_index
        baseline.append([record.get(field_name, "") for field_name in baseline_headers])
    baseline.sheet_state = "hidden"
    if "approved_block" in headers:
        block_column = get_column_letter(headers.index("approved_block") + 1)
        last_choice_row = max(4, len(approved_blocks) + 4)
        validation = DataValidation(
            type="list",
            formula1=f"'Approved Block Choices'!$A$2:$A${last_choice_row}",
            allow_blank=True,
        )
        validation.errorTitle = "Invalid approved block"
        validation.error = (
            "Select an approved real block or a top-level route (System, Digital, Analog). "
            "Do not enter source labels, interfaces, ports, or unapproved context labels."
        )
        validation.errorStyle = "stop"
        validation.promptTitle = "Approved block"
        validation.prompt = "Choose a real approved block or System, Digital, or Analog."
        validation.showErrorMessage = True
        validation.showInputMessage = True
        worksheet.add_data_validation(validation)
        validation.add(f"{block_column}2:{block_column}{worksheet.max_row}")
    if "approved_classification" in headers:
        classification_column = get_column_letter(headers.index("approved_classification") + 1)
        classification_validation = DataValidation(
            type="list",
            formula1="'Approved Block Choices'!$B$2:$B$4",
            allow_blank=False,
        )
        classification_validation.errorTitle = "Invalid classification"
        classification_validation.error = "Choose System, Digital, or Analog from the list."
        classification_validation.errorStyle = "stop"
        classification_validation.promptTitle = "Approved classification"
        classification_validation.prompt = "Choose System, Digital, or Analog."
        classification_validation.showErrorMessage = True
        classification_validation.showInputMessage = True
        worksheet.add_data_validation(classification_validation)
        classification_validation.add(f"{classification_column}2:{classification_column}{worksheet.max_row}")
    allocation_validation_specs = {
        "allocation_class": ("C", len(allocation_classes), "Allocation class", "Choose the class that best describes where this requirement belongs."),
        "owning_target": ("D", len(owning_targets), "Owning target", "Choose the target required by the selected allocation class."),
        "allocation_rationale": ("E", len(rationale_templates), "Allocation rationale", "Choose a rationale template, then refine it if needed."),
        "lineage_mode": ("F", len(lineage_modes), "Lineage mode", "Choose normal hierarchy unless the requirement is explicitly direct or split."),
    }
    for field_name, (choice_column, choice_count, prompt_title, prompt_text) in allocation_validation_specs.items():
        if field_name not in headers:
            continue
        field_column = get_column_letter(headers.index(field_name) + 1)
        allocation_validation = DataValidation(
            type="list",
            formula1=f"'Approved Block Choices'!${choice_column}$2:${choice_column}${choice_count + 1}",
            allow_blank=False,
        )
        allocation_validation.errorTitle = f"Invalid {field_name}"
        allocation_validation.error = "Choose a value from the drop-down list. The owning target must match the allocation class."
        allocation_validation.errorStyle = "stop"
        allocation_validation.promptTitle = prompt_title
        allocation_validation.prompt = prompt_text
        allocation_validation.showErrorMessage = True
        allocation_validation.showInputMessage = True
        worksheet.add_data_validation(allocation_validation)
        allocation_validation.add(f"{field_column}2:{field_column}{worksheet.max_row}")
    if "review_decision" in headers:
        decision_column = headers.index("review_decision") + 1
        decision_validation = DataValidation(
            type="list",
            formula1=f"'Approved Block Choices'!$G$2:$G${len(review_decisions) + 1}",
            allow_blank=False,
        )
        decision_validation.errorTitle = "Invalid review decision"
        decision_validation.error = "Choose an explicit review decision from the list."
        decision_validation.errorStyle = "stop"
        decision_validation.promptTitle = "Review decision"
        decision_validation.prompt = "Select approved or reassigned only after the full row is valid."
        decision_validation.showErrorMessage = True
        decision_validation.showInputMessage = True
        worksheet.add_data_validation(decision_validation)
        decision_validation.add(f"{decision_column_letter}2:{decision_column_letter}{worksheet.max_row}")
    workbook_path = csv_path.with_suffix(".xlsx")
    try:
        workbook.save(workbook_path)
        return workbook_path
    except PermissionError:
        raise PermissionError(
            f"Cannot update the architecture mapping workbook because it is open or locked: {workbook_path}. "
            "Save and close that workbook in Excel, then run Stage 2 again."
        )


def _priority(req_type: str) -> str:
    t = (req_type or "").strip().lower()
    if t in {"safety", "timing"}:
        return "high"
    if t in {"interface", "electrical"}:
        return "medium"
    return "medium"


def _write_traceability_seed(path: Path, requirements: List[Dict[str, str]], seed_limit: int) -> int:
    rows = requirements if seed_limit <= 0 else requirements[:seed_limit]

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "req_id",
            "requirement_title",
            "acceptance_test_id",
            "assertion_id",
            "priority",
            "status",
            "notes",
        ])

        for row in rows:
            req_id = row.get("id", "")
            statement = row.get("requirement_statement", "")
            title = statement if len(statement) <= 120 else statement[:117] + "..."
            assertion_id = "ASSERT_" + "".join(ch if ch.isalnum() else "_" for ch in req_id) + "_01"
            writer.writerow(
                [
                    req_id,
                    title,
                    f"AT-{req_id}",
                    assertion_id,
                    _priority(row.get("requirement_type", "")),
                    "draft",
                    f"source={row.get('source', '')}",
                ]
            )

    return len(rows)


def _write_specs_md(path: Path, requirements: List[Dict[str, str]], include_limit: int) -> int:
    rows = requirements if include_limit <= 0 else requirements[:include_limit]
    today = datetime.now().strftime("%Y-%m-%d")

    lines: List[str] = []
    lines.append("# Requirements Baseline")
    lines.append("")
    lines.append(f"Date: {today}")
    lines.append("")
    lines.append("## Scope")
    lines.append("- Stage 2 formalization baseline generated from Stage 1 requirements summary.")
    lines.append("")

    lines.append("## Requirements")
    for row in rows:
        lines.append(f"- {row.get('id', '')}: {row.get('requirement_statement', '')}")
    lines.append("")

    lines.append("## Acceptance Tests (Given-When-Then)")
    for row in rows:
        req_id = row.get("id", "")
        lines.append(
            f"- AT-{req_id}: Given nominal setup, when scenario for {req_id} is exercised, then expected behavior is observed."
        )
    lines.append("")

    lines.append("## Assertions")
    for row in rows:
        req_id = row.get("id", "")
        assertion_id = "ASSERT_" + "".join(ch if ch.isalnum() else "_" for ch in req_id) + "_01"
        lines.append(f"- {assertion_id}: trigger({req_id}) -> expected({req_id})")
    lines.append("")

    lines.append("## Open Ambiguities")
    lines.append("- Full Stage 2 review pending for requirements beyond this generated baseline.")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(rows)


def _write_architecture_profile_draft(
    draft_path: Path,
    approval_request_path: Path,
    requirements: List[Dict[str, str]],
    ontology_links_path: Path,
    semantic_issues_path: Path,
    summary_csv: Path,
    profile_path: Path,
    prior_traceability_path: Path,
) -> None:
    """Create a reviewer-owned Stage 2A profile draft from Stage 0/1 evidence."""
    ontology_rows = _read_csv_optional(ontology_links_path)
    semantic_issues = _parse_semantic_issues(semantic_issues_path)
    profile_block_defs = _read_profile_block_defs(profile_path)
    profile_source_section_aliases = _read_profile_source_section_aliases(profile_path)
    source_matrix_edges = _read_source_matrix_edges(
        summary_csv.parent / "source_matrix_edges.csv"
    )
    for index, row in enumerate(requirements):
        inferred_owner = _infer_supplementary_owner(row, profile_block_defs)
        if inferred_owner:
            enriched = dict(row)
            enriched["source_section_owner"] = inferred_owner
            if not (enriched.get("category") or "").strip():
                enriched["category"] = _infer_block_classification(enriched, inferred_owner, profile_block_defs)
            requirements[index] = enriched
    links_by_req: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for link in ontology_rows:
        req_id = (link.get("source_req_id") or "").strip()
        if req_id:
            links_by_req[req_id].append(link)

    owner_ids: Dict[str, List[str]] = defaultdict(list)
    block_evidence: Dict[str, List[str]] = defaultdict(list)
    block_relations: Dict[str, Counter] = defaultdict(Counter)
    requirements_by_id = {_normalized_req_id(row): row for row in requirements if _normalized_req_id(row)}
    for row in requirements:
        owner = (row.get("source_section_owner") or "").strip()
        requirement_id = _normalized_req_id(row)
        if owner and owner.lower() != "unassigned" and requirement_id:
            owner_ids[owner].append(requirement_id)
            block_evidence[owner].append(row.get("requirement_statement", ""))

        for link in links_by_req.get(requirement_id, []):
            role = _normalize_text(link.get("role", ""))
            if role and role.lower() != "requirement":
                owner_ids[role].append(requirement_id)
                block_evidence[role].append(link.get("function_or_property_evidence", ""))
                block_relations[role][link.get("relation_type", "")] += 1
            for related_role in link.get("related_role", "").split(";"):
                related_role = _normalize_text(related_role)
                if related_role and related_role.lower() != "requirement":
                    owner_ids[related_role].append(requirement_id)
                    block_relations[related_role][f"related:{link.get('relation_type', '')}"] += 1

    normalized_req_rows: List[List[str]] = []
    trace_rows: List[List[str]] = []
    req_candidate_blocks: Dict[str, List[str]] = defaultdict(list)
    for row in requirements:
        req_id = _normalized_req_id(row)
        links = links_by_req.get(req_id, [])
        roles = _join_unique([link.get("role", "") for link in links])
        related_roles = _join_unique([link.get("related_role", "") for link in links])
        relation_types = _join_unique([link.get("relation_type", "") for link in links])
        evidence = _brief_evidence([link.get("function_or_property_evidence", "") for link in links])
        owner = (row.get("source_section_owner") or "").strip()
        candidates: List[str] = []
        if owner and owner.lower() != "unassigned":
            candidates.append(owner)
        candidates.extend([link.get("role", "") for link in links if link.get("role", "").lower() != "requirement"])
        for link in links:
            candidates.extend(
                [item.strip() for item in link.get("related_role", "").split(";") if item.strip().lower() != "requirement"]
            )
        req_candidate_blocks[req_id] = sorted(set(candidate for candidate in candidates if candidate))
        normalized_req_rows.append(
            [
                req_id,
                row.get("source_req_id", ""),
                row.get("id", ""),
                row.get("id_policy", ""),
                row.get("category", ""),
                row.get("requirement_type", ""),
                owner,
                row.get("source", ""),
                _normalize_text(row.get("requirement_statement", "")),
                roles,
                related_roles,
            ]
        )
        trace_rows.append(
            [
                req_id,
                owner,
                "; ".join(req_candidate_blocks[req_id]),
                roles,
                relation_types,
                evidence,
                "review_required" if req_candidate_blocks[req_id] else "needs_manual_block_assignment",
            ]
        )

    block_defs = {
        owner: {
            "function": _brief_evidence(block_evidence.get(owner, []), limit=2)
            or "User review required: define the source-backed architectural function.",
            "inputs": "User review required: confirm source-backed inputs.",
            "outputs": "User review required: confirm source-backed outputs.",
            "candidate_requirement_count": len(set(owner_ids[owner])),
            "candidate_relations": dict(block_relations.get(owner, Counter())),
        }
        for owner in sorted(owner_ids, key=str.lower)
    }
    block_defs["Unassigned"] = {
        "function": "Placeholder for requirements requiring manual architectural assignment.",
        "inputs": "N/A",
        "outputs": "N/A",
    }
    preview_block_defs = dict(block_defs)
    preview_block_defs.update(profile_block_defs)
    if "Unassigned" not in preview_block_defs:
        preview_block_defs["Unassigned"] = block_defs["Unassigned"]
    preview_owner_ids: Dict[str, List[str]] = defaultdict(list)
    for row in requirements:
        req_id = _normalized_req_id(row)
        if not req_id:
            continue
        for block_name in _preview_blocks_for_requirement(
            row,
            req_candidate_blocks.get(req_id, []),
            profile_block_defs,
            profile_source_section_aliases,
            source_matrix_edges,
        ):
            preview_owner_ids[block_name].append(req_id)
    source_hashes = {
        "requirements_summary_csv": {
            "path": portable_repo_path(summary_csv.parents[2], summary_csv),
            "sha256": _sha256_file(summary_csv),
        },
        "ontology_requirement_links_csv": {
            "path": portable_repo_path(summary_csv.parents[2], ontology_links_path),
            "sha256": _sha256_file(ontology_links_path),
        },
        "semantic_issues_md": {
            "path": portable_repo_path(summary_csv.parents[2], semantic_issues_path),
            "sha256": _sha256_file(semantic_issues_path),
        },
    }
    final_summary_dir = draft_path.parent
    mapping_preview_path = final_summary_dir / "architecture_mapping_preview.csv"
    mapping_workbook_path = mapping_preview_path.with_suffix(".xlsx")
    if mapping_workbook_path.exists() and mapping_preview_path.exists():
        sync_mapping_workbook_to_csv(mapping_workbook_path, mapping_preview_path)
    existing_mapping_metadata = _read_existing_mapping_metadata(mapping_preview_path)
    previous_blocks_by_requirement = _read_previous_blocks_by_requirement(prior_traceability_path)
    approved_classifications = _approved_classifications(summary_csv.parents[2])
    added_owner_defs = _ensure_previous_concrete_owner_defs(preview_block_defs, previous_blocks_by_requirement)
    if added_owner_defs:
        print(f"[INFO] Added {added_owner_defs} inherited concrete owner definition(s) to architecture mapping preview")
    cascaded_owner_count = _cascade_previous_concrete_owners(
        preview_owner_ids,
        previous_blocks_by_requirement,
        preview_block_defs,
    )
    if cascaded_owner_count:
        print(f"[INFO] Cascaded {cascaded_owner_count} existing concrete requirement owner(s) into architecture mapping preview")
    _write_mapping_preview(
        mapping_preview_path,
        preview_block_defs,
        preview_owner_ids,
        requirements_by_id,
        previous_blocks_by_requirement,
        _read_supplementary_review(summary_csv.parents[2], approved_classifications),
        approved_classifications,
        profile_source_section_aliases,
    )
    filled_count, review_count = _prefill_mapping_allocations(
        mapping_preview_path,
        existing_mapping_metadata,
        preview_block_defs,
    )
    print(f"[INFO] Allocation prefill: {filled_count} deterministic rows; {review_count} rows remain for user review")
    _write_mapping_preview_markdown(mapping_preview_path)
    workbook_path = _write_mapping_workbook(mapping_preview_path)
    if workbook_path != mapping_preview_path.with_suffix(".xlsx"):
        print(f"[WARN] Mapping review workbook was locked; wrote editable copy to {workbook_path.as_posix()}")
    mapping_preview_hash = _sha256_file(mapping_preview_path)
    draft = {
        "approval": {
            "status": "pending_user_approval",
            "approved_by": "",
            "approved_at": "",
            "reviewer_notes": "",
            "reviewed_draft_profile_sha256": "",
            "reviewed_mapping_preview_csv_sha256": "",
            "evidence_hashes": source_hashes,
        },
        "review_package": {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "source_artifact_hashes": source_hashes,
            "mapping_preview_csv": {
                "path": "artifacts/stage1_specs/architecture_mapping_preview.csv",
                "sha256": mapping_preview_hash,
            },
            "draft_profile_sha256": "computed_after_write",
            "required_approval_checks": [
                "approval.status is approved",
                "approved_by and approved_at are non-empty",
                "approval.evidence_hashes match current Stage 0/1 artifacts",
                "approval.reviewed_draft_profile_sha256 matches the current draft artifact",
                "approval.reviewed_mapping_preview_csv_sha256 matches the reviewed architecture mapping preview CSV",
                "critical and major ambiguity dispositions are resolved or waived with rationale",
            ],
            "non_enforced_checks": [
                "Text, table, and figure extraction completeness",
            ],
        },
        "block_defs": block_defs,
        "source_section_aliases": {},
        "mapping_rules": {
            owner: [owner.lower()]
            for owner in sorted(owner_ids, key=str.lower)
        },
        "interface_rows": [],
        "interaction_rows": [],
        "function_decomposition_rows": [],
        "normalized_requirements": [
            {
                "req_id": row[0],
                "source_req_id": row[1],
                "generated_id": row[2],
                "id_policy": row[3],
                "category": row[4],
                "requirement_type": row[5],
                "source_section_owner": row[6],
                "source": row[7],
                "normalized_statement": row[8],
                "ontology_roles": row[9],
                "ontology_related_roles": row[10],
                "candidate_blocks": req_candidate_blocks.get(row[0], []),
            }
            for row in normalized_req_rows
        ],
        "ambiguity_dispositions": semantic_issues,
        "review_evidence": {
            owner: sorted(set(requirement_ids))
            for owner, requirement_ids in sorted(owner_ids.items(), key=lambda item: item[0].lower())
        },
    }
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_hash = _draft_review_sha256(draft)
    draft["review_package"]["draft_profile_sha256"] = draft_hash
    draft_path.write_text(json.dumps(draft, indent=2) + "\n", encoding="utf-8")

    _write_csv(
        final_summary_dir / "architecture_profile_requirements_summary.csv",
        [
            "Requirement ID",
            "Source Req ID",
            "Generated ID",
            "ID Policy",
            "Category",
            "Requirement Type",
            "Source Section Owner",
            "Source",
            "Normalized Statement",
            "Ontology Roles",
            "Ontology Related Roles",
        ],
        normalized_req_rows,
    )
    block_summary_rows: List[List[str]] = []
    for owner in sorted(owner_ids, key=str.lower):
        block_summary_rows.append(
            [
                owner,
                str(len(set(owner_ids[owner]))),
                _join_unique(list(block_relations.get(owner, Counter()).keys())),
                block_defs.get(owner, {}).get("function", "") if isinstance(block_defs.get(owner), dict) else "",
                "; ".join(sorted(set(owner_ids[owner]))),
            ]
        )
    _write_csv(
        final_summary_dir / "architecture_profile_block_summary.csv",
        ["Candidate Block", "Requirement Count", "Relation Evidence", "Candidate Function Evidence", "Requirement IDs"],
        block_summary_rows,
    )
    _write_csv(
        final_summary_dir / "architecture_profile_traceability.csv",
        [
            "Requirement ID",
            "Source Section Owner",
            "Candidate Blocks",
            "Ontology Roles",
            "Relation Types",
            "Function/Property Evidence",
            "Review Status",
        ],
        trace_rows,
    )
    _write_csv(
        final_summary_dir / "architecture_profile_ambiguity_dispositions.csv",
        ["Issue ID", "Severity", "Requirement ID", "Description", "Required For Approval", "Disposition", "Rationale"],
        [
            [
                issue.get("issue_id", ""),
                issue.get("severity", ""),
                issue.get("requirement_id", ""),
                issue.get("description", ""),
                issue.get("required_for_approval", ""),
                issue.get("disposition", ""),
                issue.get("rationale", ""),
            ]
            for issue in semantic_issues
        ],
    )
    lines = [
        "# Architecture Profile Approval Request",
        "",
        "## Required User Action",
        "",
        "1. Review `architecture_profile_draft.json` against the source requirements and ontology artifacts.",
        "2. Review and edit `architecture_mapping_preview.csv` for preliminary requirement-ID-to-block assignments and generated block paragraph previews.",
        "3. Review the final summary tables and traceability outputs generated beside the draft.",
        "4. Define or correct real device blocks, functions, inputs, outputs, aliases, mapping rules, interaction rows, and preliminary requirement ownership.",
        "5. Resolve or waive every critical/major ambiguity disposition with rationale; minor issues are informational.",
        "6. Save the approved profile at the configured Stage 2 profile path.",
        "7. Set `approval.status` to `approved`, provide non-empty `approved_by` and `approved_at`, copy the current evidence hashes, set `approval.reviewed_draft_profile_sha256` to:",
        f"   `{draft_hash}`",
        "8. Set `approval.reviewed_mapping_preview_csv_sha256` to the hash of the reviewed CSV:",
        f"   `{mapping_preview_hash}`",
        "9. Run Stage 2A only after approval; it will stop when this approval record is incomplete, stale, or has unresolved critical/major ambiguity items.",
        "",
        "## Draft Evidence Summary",
        "",
        f"- Stage 1 requirements analyzed: {len(requirements)}",
        f"- Candidate architecture terms: {len(owner_ids)}",
        f"- Ontology link rows analyzed: {len(ontology_rows)}",
        f"- Ambiguity items requiring approval disposition: {sum(1 for issue in semantic_issues if issue.get('required_for_approval') == 'yes')}",
        "- Text, table, and figure extraction completeness: not enforced by this approval gate",
        "",
        "## Mapping CSV Review Decisions",
        "",
        "- `approved`: accept the candidate block and generated paragraph preview.",
        "- `approved`: use the confirmed or edited `approved_block` value.",
        "- `rejected`: reject this preliminary assignment; Stage 2A remains blocked.",
        "- Set `review_decision` explicitly in the workbook; block or classification edits never infer approval.",
        "- `pending_review`: generated default, not approved for downstream use.",
        "",
        "## Final Summary Tables / Traceability Outputs",
        "",
        "- `architecture_mapping_preview.csv`",
        "- `architecture_profile_requirements_summary.csv`",
        "- `architecture_profile_block_summary.csv`",
        "- `architecture_profile_traceability.csv`",
        "- `architecture_profile_ambiguity_dispositions.csv`",
        "",
        "## Evidence Hashes",
        "",
        f"- requirements_summary_csv: `{source_hashes['requirements_summary_csv']['sha256']}`",
        f"- ontology_requirement_links_csv: `{source_hashes['ontology_requirement_links_csv']['sha256']}`",
        f"- semantic_issues_md: `{source_hashes['semantic_issues_md']['sha256']}`",
        f"- mapping_preview_csv: `{mapping_preview_hash}`",
        f"- draft_profile_sha256: `{draft_hash}`",
    ]
    for owner in sorted(owner_ids, key=str.lower):
        lines.append(f"- {owner}: {len(set(owner_ids[owner]))} source requirements")
    approval_request_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_stage2_report(path: Path, total_requirements: int, seed_rows: int, spec_rows: int) -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "# Stage 02 Report",
        "",
        f"Date: {today}",
        "",
        "## Scope",
        "- Stage 2 specification formalization baseline generated from Stage 1 artifacts.",
        "",
        "## Specification Notes",
        f"- Requirement normalization status: baseline generated from {total_requirements} Stage 1 requirements.",
        f"- Acceptance test coverage: seed entries created for {seed_rows} requirements.",
        f"- Assertion coverage: assertion seeds created for {spec_rows} requirements.",
        "",
        "## Evidence",
        "- Specs baseline generated",
        "- Traceability seed generated",
        "- Architecture profile draft and approval request generated",
        "- Preliminary requirement-to-block mapping preview generated",
        "- Final architecture-profile requirements summary generated",
        "- Final architecture-profile block summary generated",
        "- Final architecture-profile traceability output generated",
        "- Final architecture-profile ambiguity disposition table generated",
        "",
        "## Status",
        "- Gate 2: pending validation",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Stage 2 baseline specs artifacts")
    parser.add_argument(
        "--summary-csv",
        help="Deprecated compatibility option; the integrated-corpus resolver is authoritative",
    )
    parser.add_argument(
        "--specs-md",
        default="artifacts/stage1_specs/specs.md",
        help="Output Stage 2 specs markdown path",
    )
    parser.add_argument(
        "--traceability-csv",
        default="artifacts/stage1_specs/traceability_seed.csv",
        help="Output Stage 2 traceability seed CSV path",
    )
    parser.add_argument(
        "--stage2-report",
        default="artifacts/orchestrator/stage_02_report.md",
        help="Output Stage 2 orchestrator report path",
    )
    parser.add_argument(
        "--architecture-profile-draft",
        default="artifacts/stage1_specs/architecture_profile_draft.json",
        help="Output draft architecture profile for user review and approval",
    )
    parser.add_argument(
        "--architecture-approval-request",
        default="artifacts/stage1_specs/architecture_profile_approval_request.md",
        help="Output user approval request for the draft architecture profile",
    )
    parser.add_argument(
        "--seed-limit",
        type=int,
        default=40,
        help="Max number of requirements to include in traceability seed (<=0 means all)",
    )
    parser.add_argument(
        "--spec-limit",
        type=int,
        default=20,
        help="Max number of requirements to include in specs.md examples (<=0 means all)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")
    context_path = repo_root / PROJECT_CONTEXT
    context = json.loads(context_path.read_text(encoding="utf-8")) if context_path.exists() else {}

    guard_cmd = [sys.executable, "scripts/guard_stage2_plus_spec_independence.py", "--quiet"]
    guard_rc = subprocess.run(guard_cmd, cwd=repo_root).returncode
    if guard_rc != 0:
        print("Stage 2 specs generation: FAIL (Stage 2+ source-spec independence guard failed)")
        _append_log(repo_root, script_name, f"FAIL stage2_plus_guard_exit={guard_rc}")
        return guard_rc

    summary_csv = authoritative_corpus_path(repo_root)
    specs_md = (repo_root / args.specs_md).resolve()
    traceability_csv = (repo_root / args.traceability_csv).resolve()
    stage2_report = (repo_root / args.stage2_report).resolve()
    architecture_profile_draft = (repo_root / args.architecture_profile_draft).resolve()
    architecture_approval_request = (repo_root / args.architecture_approval_request).resolve()
    ontology_links = _configured_path(
        repo_root, context, "ontology_links_path", "artifacts/ontology/ontology_requirement_links.csv"
    )
    semantic_issues = _configured_path(
        repo_root, context, "semantic_issues_path", "artifacts/ontology/semantic_issues.md"
    )
    profile_path = _configured_path(repo_root, context, "stage2_profile_path", "config/stage2_profile.json")
    prior_traceability_path = _configured_path(
        repo_root, context, "stage2_traceability_path", "artifacts/stage2/requirement_to_block_traceability.csv"
    )

    try:
        requirements = _read_requirements(summary_csv)
        seed_rows = _write_traceability_seed(traceability_csv, requirements, args.seed_limit)
        spec_rows = _write_specs_md(specs_md, requirements, args.spec_limit)
        _write_architecture_profile_draft(
            architecture_profile_draft,
            architecture_approval_request,
            requirements,
            ontology_links,
            semantic_issues,
            summary_csv,
            profile_path,
            prior_traceability_path,
        )
        _write_stage2_report(stage2_report, len(requirements), seed_rows, spec_rows)
    except Exception as exc:
        print(f"Stage 2 generation: FAIL ({exc})")
        _append_log(repo_root, script_name, f"FAIL error={exc}")
        return 1

    print("Stage 2 generation: PASS")
    print(f"- Source summary: {summary_csv}")
    print(f"- Specs: {specs_md}")
    print(f"- Traceability seed: {traceability_csv}")
    print(f"- Architecture profile draft: {architecture_profile_draft}")
    print(f"- User approval request: {architecture_approval_request}")
    print(f"- Architecture mapping preview: {architecture_profile_draft.parent / 'architecture_mapping_preview.csv'}")
    print(f"- Architecture requirements summary: {architecture_profile_draft.parent / 'architecture_profile_requirements_summary.csv'}")
    print(f"- Architecture block summary: {architecture_profile_draft.parent / 'architecture_profile_block_summary.csv'}")
    print(f"- Architecture traceability: {architecture_profile_draft.parent / 'architecture_profile_traceability.csv'}")
    print(f"- Architecture ambiguity dispositions: {architecture_profile_draft.parent / 'architecture_profile_ambiguity_dispositions.csv'}")
    print(f"- Stage report: {stage2_report}")
    print(f"- Requirements loaded: {len(requirements)}")
    print(f"- Seed rows written: {seed_rows}")
    print(f"- Specs entries written: {spec_rows}")

    _append_log(
        repo_root,
        script_name,
        (
            "PASS "
            f"requirements={len(requirements)} seed_rows={seed_rows} spec_rows={spec_rows} "
            f"specs={specs_md.as_posix()} traceability={traceability_csv.as_posix()} "
            f"report={stage2_report.as_posix()}"
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
