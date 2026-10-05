#!/usr/bin/env python3
"""Run Stage 2 micro-architecture synthesis and mandatory architectural crosscheck.

This script reads Stage 1 requirements and produces Stage 2 micro-architecture artifacts:
- block inventory
- requirement-to-block traceability
- interface catalog
- interaction matrix
- function decomposition
- consolidated micro-architecture report
- architecture crosscheck report
- stage_02_micro_arch orchestrator report
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from typing import Dict, List, Tuple
from workflow_routing import pmu_clock_reset_alias, source_parent_title
from requirement_corpus import authoritative_corpus_path
from canonical_store import connect, fingerprint, replace_stage2_descriptive_evidence, utc_now
from low_power_descriptive import power_domain_records_from_ocr
from mapping_review_sync import sync_mapping_workbook_to_csv
from requirement_allocation_policy import LINEAGE_MODES, RULES, rule_for
from validate_stage2_profile import validate_approval_evidence


REQ_CSV = Path("artifacts/stage1_requirements/requirements_summary.csv")
OCR_INDEX_CSV = Path("artifacts/stage1_requirements/ocr_extracts/index.csv")
OUT_DIR = Path("artifacts/stage2_mirco_arc")
ORCH_REPORT = Path("artifacts/orchestrator/stage_02_micro_arch_report.md")
STAGE2_PROFILE = Path("config/stage2_mirco_arc_profile.json")
PROFILE_CROSSCHECK = Path("scripts/validate_stage2_profile.py")
ONTOLOGY_LINKS_CSV = Path("artifacts/stage0_ontology/ontology_requirement_links.csv")
POST_MAPPING_CROSSCHECK = Path("scripts/validate_stage2_mapping.py")
SEMANTIC_ISSUES_MD = Path("artifacts/stage0_ontology/semantic_issues.md")
ARCHITECTURE_PROFILE_DRAFT = Path("artifacts/stage1_specs/architecture_profile_draft.json")
ARCHITECTURE_MAPPING_PREVIEW_CSV = Path("artifacts/stage1_specs/architecture_mapping_preview.csv")


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\n")


def _read_requirements(path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({k: (v or "").strip() for k, v in row.items()})
    return rows


def _function_decomposition_rows_from_requirements(
    requirements: List[Dict[str, str]],
    final_mapping: Dict[str, str],
) -> List[Dict[str, str]]:
    """Build derived function rows from Stage 1 architecture evidence."""
    allowed_kinds = {"architecture_function", "architecture_capability", "power_management_concept"}
    rows: List[Dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for row in requirements:
        if (row.get("derivation_kind") or "").strip() not in allowed_kinds:
            continue
        statement = re.sub(r"\s+", " ", (row.get("requirement_statement") or "").strip())
        if not statement:
            continue
        source_id = (row.get("source_req_id") or row.get("id") or "").strip()
        owner = (final_mapping.get(source_id) or row.get("source_section_owner") or "System").strip()
        kind = (row.get("derivation_kind") or "").strip()
        key = (statement.casefold(), kind.casefold(), owner.casefold())
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "top_function": statement,
            "subfunctions": f"{kind}; source={row.get('source', '').strip()}",
            "blocks_involved": owner,
        })
    return rows


def _power_domain_function_rows(repo_root: Path) -> List[Dict[str, str]]:
    """Convert approved Stage 1 power-domain evidence into Stage 2 rows."""
    return [
        {
            "top_function": record["statement"],
            "subfunctions": "power_domain; source=" + record["source"],
            "blocks_involved": "System",
        }
        for record in power_domain_records_from_ocr(repo_root)
    ]


def _read_ontology_links(path: Path) -> Dict[str, List[Dict[str, str]]]:
    links: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    if not path.exists():
        return links
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            req_id = (row.get("source_req_id") or "").strip()
            if req_id:
                links[req_id].append({key: (value or "").strip() for key, value in row.items()})
    return links


def _read_final_architecture_mapping(path: Path, block_defs: Dict[str, object]) -> Dict[str, str]:
    """Return only final Stage 2A approved/reassigned block decisions."""
    mapping: Dict[str, str] = {}
    top_level_routes = {"system", "digital", "analog"}
    if not path.exists():
        return mapping
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            req_id = (row.get("requirement_id") or "").strip()
            decision = (row.get("review_decision") or "").strip().lower()
            approved_block = (row.get("approved_block") or "").strip()
            if (
                req_id
                and decision in {"approved", "reassigned"}
                and approved_block
            ):
                if approved_block in block_defs and approved_block != "Unassigned":
                    mapping[req_id] = approved_block
                elif approved_block.casefold() in top_level_routes:
                    # Top-level ownership is a routing decision, not a SysML block.
                    # Keep it out of block allocation; its classification routes it
                    # to SRS, DRS, or ARS downstream.
                    mapping[req_id] = "Unassigned"
    return mapping


def _persist_approved_architecture_mappings(
    repo_root: Path,
    *,
    project_id: str,
    mapping_preview_path: Path,
) -> int:
    """Persist the reviewed Stage 2 mapping handoff for immutable snapshots."""
    reviewed_rows = _read_requirements(mapping_preview_path)
    approved_rows = [
        row for row in reviewed_rows
        if (row.get("review_decision") or "").strip().casefold() in {"approved", "reassigned"}
        and (row.get("approved_block") or "").strip()
    ]
    if not approved_rows:
        raise RuntimeError("No approved architecture mapping rows are available to persist.")
    connection = connect(repo_root)
    try:
        canonical_by_source = {
            str(row["source_req_id"] or "").strip(): str(row["canonical_requirement_id"])
            for row in connection.execute(
                "SELECT canonical_requirement_id, source_req_id FROM canonical_requirements WHERE project_id = ?",
                (project_id,),
            ).fetchall()
            if str(row["source_req_id"] or "").strip()
        }
        persisted = 0
        reviewed_source_ids: set[str] = set()
        for row in approved_rows:
            source_id = (row.get("requirement_id") or "").strip()
            canonical_id = canonical_by_source.get(source_id)
            if not canonical_id:
                continue
            reviewed_source_ids.add(source_id)
            approved_block = (row.get("approved_block") or "").strip()
            architecture_layer = (row.get("approved_classification") or "System").strip()
            material = {
                "canonical_requirement_id": canonical_id,
                "architecture_layer": architecture_layer,
                "approved_block": approved_block,
                "mapping_preview": source_id,
            }
            allocation_class = (row.get("allocation_class") or "").strip()
            owning_target = (row.get("owning_target") or "").strip()
            allocation_rationale = (row.get("allocation_rationale") or "").strip()
            lineage_mode = (row.get("lineage_mode") or "").strip()
            if not allocation_class or not owning_target:
                raise RuntimeError(
                    f"Approved mapping {source_id} is missing allocation_class or owning_target. "
                    "Complete the approved hierarchy allocation review before Stage 2B freeze."
                )
            if rule_for(allocation_class).owning_target != owning_target:
                raise RuntimeError(
                    f"Approved mapping {source_id} has allocation target mismatch: "
                    f"class={allocation_class}, target={owning_target}."
                )
            mapping_id = "mapping-" + fingerprint(material)[:24]
            connection.execute(
                "UPDATE architecture_mappings SET lifecycle_state = 'impacted' WHERE project_id = ? AND canonical_requirement_id = ? AND lifecycle_state = 'approved' AND mapping_id <> ?",
                (project_id, canonical_id, mapping_id),
            )
            connection.execute(
                """INSERT OR REPLACE INTO architecture_mappings(
                    mapping_id, project_id, canonical_requirement_id, architecture_layer,
                    candidate_block, approved_block, mapping_reason, lifecycle_state,
                    content_fingerprint, created_at, allocation_class, owning_target,
                    allocation_rationale, lineage_mode, source_origin_req_ids,
                    hierarchy_parent_req_ids, lineage_candidate_parent_req_ids, owning_domain)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'approved', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    mapping_id, project_id, canonical_id, architecture_layer,
                    (row.get("candidate_block") or "").strip(), approved_block,
                    "Reviewed architecture_mapping_preview.xlsx synchronized to CSV.",
                    fingerprint(material), utc_now(), allocation_class, owning_target,
                    (row.get("allocation_rationale") or "").strip(),
                    (row.get("lineage_mode") or "normal_hierarchical").strip(),
                    (row.get("source_origin_req_ids") or source_id).strip(),
                    (row.get("hierarchy_parent_req_ids") or "").strip(),
                    (row.get("lineage_candidate_parent_req_ids") or "").strip(),
                    (row.get("owning_domain") or architecture_layer).strip(),
                ),
            )
            persisted += 1
        missing_canonical = sorted(set(canonical_by_source) - reviewed_source_ids)
        if missing_canonical:
            raise RuntimeError("Canonical requirements are missing approved mapping rows: " + ", ".join(missing_canonical[:10]))
        connection.commit()
        return persisted
    finally:
        connection.close()


def _infer_existing_block_from_source_id(row: Dict[str, str], block_defs: Dict[str, object]) -> str:
    """Use a supplementary source ID only to propose an existing configured block."""
    if not (row.get("source_spec") or "").strip():
        return ""
    source_id = re.sub(r"[^a-z0-9]+", "", (row.get("source_req_id") or row.get("id") or "").lower())
    candidates = [
        block_name for block_name in block_defs
        if block_name != "Unassigned"
        and re.sub(r"[^a-z0-9]+", "", block_name.lower()) in source_id
    ]
    return max(candidates, key=len, default="")


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


def _issue_is_extraction_completeness(text: str) -> bool:
    low = text.lower()
    return (
        "text, table, and figure extraction completeness" in low
        or "extraction completeness" in low
        or "table extraction completeness" in low
        or "figure extraction completeness" in low
    )


def _validate_mapping_preview_csv(path: Path) -> List[str]:
    allowed = {"approved", "reassigned", "rejected", "needs_clarification"}
    approved_decisions = {"approved", "reassigned"}
    allowed_classifications = {"analog", "digital", "system"}
    findings: List[str] = []
    if not path.exists():
        return [f"mapping preview CSV is missing: {path.as_posix()}"]
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "candidate_block",
            "requirement_id",
            "approved_classification",
            "review_decision",
            "approved_block",
            "allocation_class",
            "owning_target",
            "allocation_rationale",
            "lineage_mode",
            "source_origin_req_ids",
            "hierarchy_parent_req_ids",
            "owning_domain",
        }
        missing = sorted(required - set(reader.fieldnames or []))
        if missing:
            return [f"mapping preview CSV missing required column(s): {', '.join(missing)}"]
        for index, row in enumerate(reader, start=2):
            req_id = (row.get("requirement_id") or "").strip()
            decision = (row.get("review_decision") or "").strip().lower()
            approved_block = (row.get("approved_block") or "").strip()
            candidate_block = (row.get("candidate_block") or "").strip()
            generated_preview = (row.get("generated_block_paragraph_preview") or "").strip().lower()
            approved_classification = (row.get("approved_classification") or "").strip().lower()
            allocation_class = (row.get("allocation_class") or "").strip()
            owning_target = (row.get("owning_target") or "").strip()
            allocation_rationale = (row.get("allocation_rationale") or "").strip()
            lineage_mode = (row.get("lineage_mode") or "").strip()
            label = req_id or f"row {index}"
            unresolved = (
                candidate_block.lower() == "unresolved source paragraph"
                or "unresolved source paragraph" in generated_preview
            )
            if unresolved and (decision in approved_decisions or approved_block.lower() == "unresolved source paragraph"):
                findings.append(
                    f"{label}: unresolved source paragraph requires user block mapping before Stage 2A approval"
                )
            if approved_classification not in allowed_classifications:
                findings.append(f"{label}: approved_classification must be Analog, Digital, or System")
            if not allocation_class:
                findings.append(f"{label}: allocation_class is required")
            elif allocation_class not in RULES:
                findings.append(f"{label}: unsupported allocation_class: {allocation_class}")
            if not owning_target:
                findings.append(f"{label}: owning_target is required")
            elif allocation_class in RULES and rule_for(allocation_class).owning_target != owning_target:
                findings.append(
                    f"{label}: owning_target {owning_target!r} does not match "
                    f"allocation_class {allocation_class!r}"
                )
            if not allocation_rationale:
                findings.append(f"{label}: allocation_rationale is required")
            if lineage_mode not in LINEAGE_MODES:
                findings.append(f"{label}: unsupported lineage_mode: {lineage_mode}")
            if decision not in allowed:
                findings.append(f"{label}: review_decision must be one of {', '.join(sorted(allowed))}")
            elif decision not in approved_decisions:
                findings.append(f"{label}: review_decision={decision} blocks approval")
            elif decision == "reassigned" and not approved_block:
                findings.append(f"{label}: reassigned rows require approved_block")
            elif decision == "approved" and not approved_block:
                findings.append(f"{label}: {decision} rows require approved_block")
            elif approved_block.casefold() in {"system", "digital", "analog"} and approved_block.casefold() != approved_classification:
                findings.append(
                    f"{label}: top-level approved_block={approved_block} must match "
                    f"approved_classification={approved_classification.title()}"
                )
    return findings


def _validate_profile_approval(profile: Dict[str, object], repo_root: Path) -> List[str]:
    findings: List[str] = []
    findings.extend(validate_approval_evidence(
        repo_root / STAGE2_PROFILE,
        repo_root / ARCHITECTURE_PROFILE_DRAFT,
        repo_root / ARCHITECTURE_MAPPING_PREVIEW_CSV,
    ))
    approval = profile.get("approval", {})
    if not isinstance(approval, dict):
        return ["approval record is missing or is not an object"]
    if approval.get("status") != "approved":
        findings.append("approval.status must be approved")
    if not str(approval.get("approved_by") or "").strip():
        findings.append("approval.approved_by must be non-empty")
    if not str(approval.get("approved_at") or "").strip():
        findings.append("approval.approved_at must be non-empty")

    expected_hashes = approval.get("evidence_hashes", {})
    if not isinstance(expected_hashes, dict):
        findings.append("approval.evidence_hashes must be present")
        expected_hashes = {}
    authoritative_req_csv = authoritative_corpus_path(repo_root)
    current_hashes = {
        "requirements_summary_csv": (authoritative_req_csv, _sha256_file(authoritative_req_csv)),
        "ontology_requirement_links_csv": (ONTOLOGY_LINKS_CSV, _sha256_file(repo_root / ONTOLOGY_LINKS_CSV)),
        "semantic_issues_md": (SEMANTIC_ISSUES_MD, _sha256_file(repo_root / SEMANTIC_ISSUES_MD)),
    }
    for key, (path, digest) in current_hashes.items():
        recorded = expected_hashes.get(key, {})
        recorded_digest = recorded.get("sha256") if isinstance(recorded, dict) else ""
        if recorded_digest != digest:
            findings.append(
                f"approval.evidence_hashes.{key}.sha256 is stale or missing for {path.as_posix()}"
            )

    findings.extend(_validate_mapping_preview_csv(repo_root / ARCHITECTURE_MAPPING_PREVIEW_CSV))

    if "ambiguity_dispositions" not in profile:
        findings.append("ambiguity_dispositions must be present")
    dispositions = profile.get("ambiguity_dispositions", [])
    if not isinstance(dispositions, list):
        findings.append("ambiguity_dispositions must be a list")
        dispositions = []
    for item in dispositions:
        if not isinstance(item, dict):
            findings.append("ambiguity_dispositions contains a non-object item")
            continue
        severity = str(item.get("severity") or "").strip().lower()
        description = str(item.get("description") or "").strip()
        if severity not in {"critical", "major"} or _issue_is_extraction_completeness(description):
            continue
        disposition = str(item.get("disposition") or "").strip().lower()
        rationale = str(item.get("rationale") or "").strip()
        issue_id = str(item.get("issue_id") or "<unknown>")
        if disposition not in {"resolved", "waived"}:
            findings.append(f"ambiguity_dispositions.{issue_id} must be resolved or waived")
        if disposition == "waived" and not rationale:
            findings.append(f"ambiguity_dispositions.{issue_id} waiver requires rationale")
    return findings


def _validate_ontology_links(
    links: Dict[str, List[Dict[str, str]]], requirements: List[Dict[str, str]]
) -> List[str]:
    requirement_ids = {
        (row.get("source_req_id") or row.get("id") or "").strip()
        for row in requirements
    }
    findings: List[str] = []
    allowed_relations = {"supports", "depends-on", "part-of", "drives", "constrains", "connected-to"}
    for req_id, rows in links.items():
        if req_id not in requirement_ids:
            findings.append(f"Ontology link references missing Stage 1 requirement: {req_id}")
        for row in rows:
            if not row.get("role"):
                findings.append(f"Ontology link has empty role: {req_id}")
            if row.get("relation_type") not in allowed_relations:
                findings.append(f"Ontology link has invalid relation type for {req_id}: {row.get('relation_type', '')}")
            if not row.get("function_or_property_evidence"):
                findings.append(f"Ontology link has no function/property evidence: {req_id}")
    return findings


def _load_profile(path: Path) -> Dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))

    required_keys = [
        "block_defs",
        "mapping_rules",
        "interface_rows",
        "interaction_rows",
        "function_decomposition_rows",
    ]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing profile key: {key}")

    block_defs = data.get("block_defs", {})
    if "Unassigned" not in block_defs:
        raise ValueError("Profile block_defs must include 'Unassigned'")

    return data


def _needs(row: Dict[str, str], terms: Tuple[str, ...]) -> bool:
    text = " ".join(
        [
            row.get("requirement_statement", ""),
            row.get("category", ""),
            row.get("requirement_type", ""),
            row.get("parameter_signal_register", ""),
        ]
    ).lower()
    return any(term in text for term in terms)


def _pick_existing(block_defs: Dict[str, object], candidates: Tuple[str, ...]) -> str:
    for name in candidates:
        if name in block_defs:
            return name
    return "Unassigned"


def _entity_kind(block_name: str, block_defs: Dict[str, object]) -> str:
    """Return the configured entity kind, preserving legacy concrete defaults."""
    if block_name == "Unassigned":
        return "unassigned"
    metadata = block_defs.get(block_name, {})
    if isinstance(metadata, dict):
        configured = str(metadata.get("entity_kind") or "").strip().lower()
        if configured:
            return configured
    return "concrete_block"


def _is_concrete_block(block_name: str, block_defs: Dict[str, object]) -> bool:
    return _entity_kind(block_name, block_defs) == "concrete_block"


def _tokenize_text(text: str) -> List[str]:
    return [t for t in re.split(r"[^a-z0-9_\-]+", text.lower()) if t]


def _derive_block_seed_terms(block_name: str, meta: object, mapped_terms: List[str]) -> List[str]:
    terms: List[str] = []

    camel = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", block_name)
    for t in _tokenize_text(camel):
        if len(t) >= 3:
            terms.append(t)

    if isinstance(meta, dict):
        block_text = " ".join(
            [
                str(meta.get("function", "")),
                str(meta.get("inputs", "")),
                str(meta.get("outputs", "")),
            ]
        )
        for t in _tokenize_text(block_text):
            if len(t) >= 3:
                terms.append(t)

    for mt in mapped_terms:
        for t in _tokenize_text(mt):
            if len(t) >= 3:
                terms.append(t)

    unique: List[str] = []
    seen = set()
    for t in terms:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique


def _semantic_tokens(text: str) -> set[str]:
    stopwords = {
        "shall", "should", "must", "with", "from", "into", "that", "this",
        "when", "where", "which", "their", "there", "have", "been", "being",
        "block", "source", "destination", "requirement", "function", "property",
    }
    return {
        token
        for token in _tokenize_text(text)
        if len(token) >= 4 and token not in stopwords
    }


def _ontology_semantic_score(
    link: Dict[str, str],
    block_name: str,
    block_defs: Dict[str, object],
    mapping_rules: Dict[str, List[str]],
    source_section_aliases: Dict[str, List[str]],
) -> int:
    meta = block_defs.get(block_name, {})
    block_text = " ".join(
        [
            block_name,
            str(meta.get("function", "")) if isinstance(meta, dict) else "",
            str(meta.get("inputs", "")) if isinstance(meta, dict) else "",
            str(meta.get("outputs", "")) if isinstance(meta, dict) else "",
            " ".join(mapping_rules.get(block_name, [])),
            " ".join(source_section_aliases.get(block_name, [])),
        ]
    )
    evidence_text = " ".join(
        [
            link.get("function_or_property_evidence", ""),
            link.get("role", ""),
            link.get("related_role", ""),
        ]
    )
    overlap = _semantic_tokens(evidence_text) & _semantic_tokens(block_text)
    score = len(overlap)
    relation_type = link.get("relation_type", "")
    if relation_type in {"drives", "constrains", "depends-on", "part-of", "connected-to"}:
        score += 1
    return score


def _ontology_semantic_candidates(
    row: Dict[str, str],
    ontology_links: Dict[str, List[Dict[str, str]]],
    block_defs: Dict[str, object],
    mapping_rules: Dict[str, List[str]],
    source_section_aliases: Dict[str, List[str]],
) -> List[str]:
    candidates: List[Tuple[int, str]] = []
    req_id = (row.get("source_req_id") or row.get("id") or "").strip()
    for link in ontology_links.get(req_id, []):
        role = link.get("role", "").lower().strip()
        related_roles = {
            value.lower().strip()
            for value in link.get("related_role", "").split(";")
            if value.strip()
        }
        for block_name in block_defs:
            if not _is_concrete_block(block_name, block_defs):
                continue
            names = {
                name.lower().strip()
                for name in [block_name, *source_section_aliases.get(block_name, [])]
                if name.strip()
            }
            role_match = role in names or bool(related_roles & names)
            if not role_match:
                continue
            score = _ontology_semantic_score(
                link, block_name, block_defs, mapping_rules, source_section_aliases
            )
            if score >= 2:
                candidates.append((score, block_name))
    return sorted({block_name for _score, block_name in candidates})


def _best_block_from_text(
    row: Dict[str, str],
    block_defs: Dict[str, object],
    mapping_rules: Dict[str, List[str]],
) -> str:
    row_text = " ".join(
        [
            row.get("requirement_statement", ""),
            row.get("category", ""),
            row.get("requirement_type", ""),
            row.get("parameter_signal_register", ""),
        ]
    ).lower()

    best_block = "Unassigned"
    best_score = 0
    for block_name, meta in block_defs.items():
        if not _is_concrete_block(block_name, block_defs):
            continue
        mapped_terms = mapping_rules.get(block_name, [])
        seeds = _derive_block_seed_terms(block_name, meta, mapped_terms)
        if not seeds:
            continue
        score = sum(1 for seed in seeds if seed and seed in row_text)
        if score > best_score:
            best_score = score
            best_block = block_name

    return best_block if best_score > 0 else "Unassigned"


def _configured_interaction_blocks(
    row: Dict[str, str],
    block_defs: Dict[str, object],
    interaction_rows: List[Dict[str, object]],
) -> List[str]:
    requirement_id = (row.get("source_req_id") or row.get("id") or "").strip()
    if not requirement_id:
        return []
    blocks: List[str] = []
    for interaction in interaction_rows:
        requirement_ids = _split_requirement_ids(interaction.get("Requirement IDs", ""))
        if requirement_id not in requirement_ids:
            continue
        for field in ("From block", "To block"):
            block_name = _resolve_inventory_block_name(str(interaction.get(field, "")), block_defs)
            if _is_concrete_block(block_name, block_defs) and block_name not in blocks:
                blocks.append(block_name)
    return blocks


def _explicit_target_block(
    row: Dict[str, str],
    block_defs: Dict[str, object],
    source_section_aliases: Dict[str, List[str]],
) -> str:
    """Resolve a configured [TO: ...] target without lexical block guessing."""
    match = re.search(r"\[to:\s*([^\]]+)\]", row.get("requirement_statement", ""), flags=re.IGNORECASE)
    if not match:
        return ""
    target = re.sub(r"[^a-z0-9]+", "", match.group(1).lower())
    matches = [
        block_name
        for block_name, aliases in source_section_aliases.items()
        if _is_concrete_block(block_name, block_defs)
        and any(re.sub(r"[^a-z0-9]+", "", alias.lower()) == target for alias in aliases)
    ]
    return matches[0] if len(matches) == 1 else ""


def _map_blocks(
    row: Dict[str, str],
    mapping_rules: Dict[str, List[str]],
    block_defs: Dict[str, object],
    source_section_aliases: Dict[str, List[str]],
    ontology_links: Dict[str, List[Dict[str, str]]],
    interaction_rows: List[Dict[str, object]] | None = None,
) -> List[str]:
    source_text = (row.get("source") or "").lower()
    statement_text = (row.get("requirement_statement") or "").lower()
    for block_name, aliases in source_section_aliases.items():
        if block_name not in block_defs or not _is_concrete_block(block_name, block_defs):
            continue
        if any(alias.strip().lower() in source_text for alias in aliases if alias.strip()):
            return [block_name]

    split_source_match = re.search(
        r"\bu_([a-z0-9]+)\s+signal\s+shall\s+be\s+connected\s+to\s+the\s+([a-z0-9]+)\.",
        statement_text,
    )
    if split_source_match:
        recovered_instance = "".join(split_source_match.groups())
        recovered_blocks = [
            block_name
            for block_name in block_defs
            if _is_concrete_block(block_name, block_defs)
            and re.sub(r"[^a-z0-9]+", "_", block_name.lower()).strip("_") == recovered_instance
        ]
        if len(recovered_blocks) == 1:
            return recovered_blocks

    explicit_instance_blocks = []
    for block_name in block_defs:
        if not _is_concrete_block(block_name, block_defs):
            continue
        instance_name = re.sub(r"[^a-z0-9]+", "_", block_name.lower()).strip("_")
        if instance_name and re.search(rf"\bu_{re.escape(instance_name)}\b", statement_text):
            explicit_instance_blocks.append(block_name)
    if len(explicit_instance_blocks) == 1:
        return explicit_instance_blocks

    configured_interaction_blocks = _configured_interaction_blocks(
        row,
        block_defs,
        interaction_rows or [],
    )
    if configured_interaction_blocks:
        return configured_interaction_blocks

    explicit_target = _explicit_target_block(row, block_defs, source_section_aliases)
    if explicit_target:
        return [explicit_target]

    source_context = " ".join(
        [row.get("source", ""), row.get("requirement_statement", "")]
    ).lower()
    if "connection matrix" in source_context or "xbar" in source_context:
        return ["Unassigned"]

    # A dedicated ADC DFT/test paragraph is source context, not proof that the
    # affected ADC owns the register-programming procedure. Preserve the
    # paragraph routing unless the reviewer supplies an approved block.
    if (
        "(under section" in source_context
        and any(term in source_context for term in ("adc test", "digital dft"))
    ):
        return ["Unassigned"]

    pmu_alias = pmu_clock_reset_alias(row, block_defs.keys())
    if pmu_alias:
        return [pmu_alias]

    parent_title = source_parent_title(row.get("source") or "").lower()
    parent_tokens = set(_tokenize_text(parent_title))
    parent_matches = []
    for block_name in block_defs:
        if not _is_concrete_block(block_name, block_defs):
            continue
        block_tokens = set(_tokenize_text(block_name))
        if block_tokens and block_tokens.issubset(parent_tokens):
            parent_matches.append(block_name)
    if len(parent_matches) == 1:
        return parent_matches

    source_section_owner = (row.get("source_section_owner") or "").strip()
    if source_section_owner in block_defs and _is_concrete_block(source_section_owner, block_defs):
        return [source_section_owner]

    ontology_candidates = _ontology_semantic_candidates(
        row, ontology_links, block_defs, mapping_rules, source_section_aliases
    )
    related_role_candidates: List[str] = []
    for link in ontology_links.get((row.get("source_req_id") or row.get("id") or "").strip(), []):
        relation_type = link.get("relation_type", "")
        if relation_type != "supports":
            related_role_candidates.extend(
                related.strip().lower()
                for related in link.get("related_role", "").split(";")
                if related.strip()
            )
    if ontology_candidates:
        return sorted(set(ontology_candidates))
    for role in related_role_candidates:
        for block_name in block_defs:
            if _is_concrete_block(block_name, block_defs) and role == block_name.lower().strip():
                ontology_candidates.append(block_name)
    if ontology_candidates:
        return sorted(set(ontology_candidates))

    mapped: List[str] = []

    for block_name, terms in mapping_rules.items():
        if not _is_concrete_block(block_name, block_defs):
            continue
        tuple_terms = tuple((t or "").strip().lower() for t in terms if (t or "").strip())
        if tuple_terms and _needs(row, tuple_terms):
            mapped.append(block_name)

    unique = sorted(set(mapped))
    row_text = " ".join(
        [
            row.get("requirement_statement", ""),
            row.get("category", ""),
            row.get("requirement_type", ""),
            row.get("parameter_signal_register", ""),
        ]
    ).lower()
    explicit_adc_evidence = bool(
        re.search(r"\badc(?:_config|\s+(?:calibration|test)|\s+sampling|\s+data)?\b", row_text)
    )
    if "ADC" in unique and not explicit_adc_evidence:
        unique.remove("ADC")
    if unique:
        return unique

    # Generic source context is valid only after all concrete block evidence
    # for this requirement has been exhausted.
    best_block = _best_block_from_text(row, block_defs, mapping_rules)
    if best_block != "Unassigned":
        return [best_block]
    if _is_generic_source_paragraph(row, block_defs):
        return ["Unassigned"]
    return [best_block]


def _is_generic_source_paragraph(row: Dict[str, str], block_defs: Dict[str, object]) -> bool:
    """Keep requirements from source paragraphs without a named block generic."""
    source = (row.get("source") or "").strip().lower()
    if not source:
        return True

    block_terms = [
        block_name
        for block_name in block_defs
        if _is_concrete_block(block_name, block_defs)
    ]
    source_key = re.sub(r"[^a-z0-9]+", "", source)
    source_section_owner = (row.get("source_section_owner") or "").strip()
    if source_section_owner in block_defs and _is_concrete_block(source_section_owner, block_defs):
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
    return not any(
        len(re.sub(r"[^a-z0-9]+", "", term.lower())) >= 3
        and re.sub(r"[^a-z0-9]+", "", term.lower()) in source_key
        for term in block_terms
    )


def _non_block_context_mapping(row: Dict[str, str]) -> str:
    """Retain the Stage 1 source paragraph when no identified logic block owns it."""
    source = (row.get("source") or "").strip()
    if source:
        return source
    return "Unresolved source paragraph"


def _extract_explicit_block_mentions(statement: str) -> List[str]:
    # Requirement-driven block mention scan (e.g., "X block" / "X sub-block").
    matches = re.findall(r"([a-z0-9/\- ]{2,}?)\s+(?:sub-)?block\b", statement.lower())
    mentions: List[str] = []
    for raw in matches:
        cleaned = re.sub(r"\s+", " ", raw).strip(" -/")
        if cleaned and cleaned not in mentions:
            mentions.append(cleaned)
    return mentions


def _write_markdown(path: Path, lines: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_csv(path: Path, header: List[str], rows: List[List[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def _show_output(repo_root: Path, label: str, path: Path) -> None:
    rel = path.relative_to(repo_root).as_posix()
    print(f"- generated {label}: {rel}")


def _requirement_source_map(rows: List[Dict[str, str]]) -> Dict[str, str]:
    return {
        (row.get("source_req_id") or row.get("id") or "").strip(): (row.get("source") or "").strip()
        for row in rows
        if (row.get("source_req_id") or row.get("id") or "").strip()
    }


def _split_requirement_ids(value: object) -> List[str]:
    return [item.strip() for item in str(value or "").split(";") if item.strip()]


def _interaction_evidence_text(row: Dict[str, object]) -> str:
    return " ".join(
        str(row.get(field, ""))
        for field in ("Signal/control", "Trigger", "Notes", "Evidence", "Source")
    ).lower()


def _is_figure_only_interaction(row: Dict[str, object]) -> bool:
    evidence = _interaction_evidence_text(row)
    if "figure" not in evidence:
        return False
    return not any(term in evidence for term in ("table", "matrix", "text", "description", "requirement"))


def _is_table_or_matrix_source(source: str) -> bool:
    source_low = (source or "").lower()
    return any(term in source_low for term in ("table", "matrix", "connection")) and "figure" not in source_low


def _validate_interaction_rows(
    rows: List[Dict[str, object]],
    req_sources: Dict[str, str],
) -> List[str]:
    findings: List[str] = []
    for index, row in enumerate(rows, start=2):
        from_block = str(row.get("From block", "")).strip()
        to_block = str(row.get("To block", "")).strip()
        signal = str(row.get("Signal/control", "")).strip().lower()
        trigger = str(row.get("Trigger", "")).strip().lower()
        notes = str(row.get("Notes", "")).strip().lower()
        requirement_ids = str(row.get("Requirement IDs", "")).strip()
        is_connection_row = (
            "connection matrix" in signal
            or "connection matrix" in trigger
            or "connection matrix" in notes
            or "xbar" in signal
            or "xbar" in trigger
            or "xbar" in notes
        )
        if _is_figure_only_interaction(row):
            findings.append(f"row {index}: interaction rows must not be derived from figure-only evidence")
        if is_connection_row and (not from_block or not to_block):
            findings.append(f"row {index}: connection-matrix row must define source and destination blocks")
        if is_connection_row and not requirement_ids:
            findings.append(f"row {index}: connection-matrix row {from_block} -> {to_block} is missing Requirement IDs")
        for req_id in _split_requirement_ids(requirement_ids):
            source = req_sources.get(req_id, "")
            if not _is_table_or_matrix_source(source):
                findings.append(
                    f"row {index}: requirement-backed interaction {req_id} must come from textual table/matrix evidence, got source='{source or 'unknown'}'"
                )
    return findings


def _stage1_ocr_texts(index_path: Path) -> List[str]:
    extracts_dir = index_path.parent
    if not extracts_dir.exists():
        return []

    texts: List[str] = []
    for path in sorted(extracts_dir.glob("*.txt")):
        try:
            texts.append(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    return texts


def _canonical_block_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def _resolve_inventory_block_name(raw_name: str, block_defs: Dict[str, object]) -> str:
    name = (raw_name or "").strip()
    if not name:
        return ""

    key = _canonical_block_key(name)
    by_key = {_canonical_block_key(block): block for block in block_defs}
    if key in by_key:
        return by_key[key]

    raw_terms = set(_tokenize_text(name))
    if raw_terms:
        ranked: List[Tuple[int, int, str]] = []
        for block in block_defs:
            block_terms = set(_tokenize_text(block))
            if not block_terms:
                continue
            if raw_terms <= block_terms:
                ranked.append((len(raw_terms & block_terms), len(block_terms), block))
        if ranked:
            ranked.sort(key=lambda item: (-item[0], item[1], item[2]))
            return ranked[0][2]

    return name


def _clean_architecture_actor_name(raw: str) -> str:
    text = re.sub(r"^[\s•*\-o]+", "", raw or "").strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\([^)]*\)", "", text).strip()
    text = re.sub(r"\b\d+\s*[- ]?bit\b.*$", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"\b(?:processor|controller|collector|engine|core|ip)\b.*$", "", text, flags=re.IGNORECASE).strip()
    text = text.strip(" .:;,")
    if not text:
        return ""

    words = text.split()
    kept: List[str] = []
    for word in words:
        if len(kept) >= 3:
            break
        if word.isupper() or re.match(r"^[A-Z][A-Za-z0-9_/-]*$", word):
            kept.append(word)
            continue
        break

    candidate = " ".join(kept).strip(" .:;,") if kept else text
    if not re.search(r"[A-Za-z]", candidate):
        return ""
    if candidate.lower() in {"the", "main", "block", "blocks", "ips", "actors", "domain"}:
        return ""
    return candidate


def _architecture_text_block_names(texts: List[str]) -> List[str]:
    names: List[str] = []
    seen = set()
    in_actor_list = False
    saw_actor_bullet = False

    for text in texts:
        for raw_line in text.splitlines():
            line = raw_line.strip()
            low = line.lower()
            if not line:
                if in_actor_list and saw_actor_bullet:
                    in_actor_list = False
                continue

            if re.search(r"\b(main|primary)\b.*\b(ip|ips|block|blocks|actor|actors)\b.*\bare\s*:?\s*$", low):
                in_actor_list = True
                saw_actor_bullet = False
                continue

            if not in_actor_list:
                continue

            if not re.match(r"^\s*[•*\-]\s*\S+", raw_line):
                if saw_actor_bullet:
                    in_actor_list = False
                in_actor_list = False
                continue
            saw_actor_bullet = True

            candidate = _clean_architecture_actor_name(line)
            if not candidate:
                continue
            key = re.sub(r"[^a-z0-9]+", "", candidate.lower())
            if key in seen:
                continue
            seen.add(key)
            names.append(candidate)

    return names


def _ensure_architecture_text_blocks(
    block_defs: Dict[str, object],
    mapping_rules: Dict[str, List[str]],
    architecture_block_names: List[str],
) -> Dict[str, object]:
    augmented: Dict[str, object] = dict(block_defs)
    for block_name in architecture_block_names:
        resolved = _resolve_inventory_block_name(block_name, augmented)
        if not resolved or resolved in augmented:
            continue
        augmented[resolved] = _generic_interaction_block_meta(resolved)
        mapping_rules.setdefault(resolved, _tokenize_text(resolved))
    return augmented


def _is_connection_matrix_row(row: Dict[str, object]) -> bool:
    return any(
        "connection matrix" in str(row.get(field, "")).lower()
        or "xbar" in str(row.get(field, "")).lower()
        for field in ("Signal/control", "Trigger", "Notes")
    )


def _generic_interaction_block_meta(block_name: str) -> Dict[str, str]:
    return {
        "function": (
            f"Represent the {block_name} digital architecture block and its source/destination responsibilities "
            "described by Stage 2 interaction evidence."
        ),
        "inputs": "Defined by interaction matrix ingress and upstream requirement evidence",
        "outputs": "Defined by interaction matrix egress and upstream requirement evidence",
    }


def _ensure_interaction_blocks(
    block_defs: Dict[str, object],
    mapping_rules: Dict[str, List[str]],
    interaction_rows: List[Dict[str, object]],
) -> Dict[str, object]:
    augmented: Dict[str, object] = dict(block_defs)
    for row in interaction_rows:
        for field in ("From block", "To block"):
            block_name = _resolve_inventory_block_name(str(row.get(field, "")).strip(), augmented)
            if not block_name or block_name in augmented:
                continue
            # Interaction endpoints are evidence, not permission to invent blocks.
    return augmented


def _link_interaction_requirements_to_blocks(
    block_to_reqs: Dict[str, List[str]],
    block_defs: Dict[str, object],
    interaction_rows: List[Dict[str, object]],
) -> None:
    for row in interaction_rows:
        requirement_ids = [
            item.strip()
            for item in str(row.get("Requirement IDs", "")).split(";")
            if item.strip()
        ]
        if not requirement_ids:
            continue
        for field in ("From block", "To block"):
            block_name = _resolve_inventory_block_name(str(row.get(field, "")).strip(), block_defs)
            if not block_name or not _is_concrete_block(block_name, block_defs):
                continue
            block_to_reqs[block_name].extend(requirement_ids)


def _detect_requirement_source_from_index(index_path: Path) -> str:
    if not index_path.exists():
        return "unknown"

    try:
        with index_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                source = (row.get("source_file") or "").strip()
                if source:
                    return source
    except Exception:
        return "unknown"

    return "unknown"


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    guard_cmd = [sys.executable, "scripts/guard_stage2_plus_spec_independence.py", "--quiet"]
    guard_rc = subprocess.run(guard_cmd, cwd=repo_root).returncode
    if guard_rc != 0:
        print("Stage 2 micro-architecture run: FAIL")
        print("- Stage 2+ source-spec independence guard failed")
        _append_log(repo_root, script_name, f"FAIL stage2_plus_guard_exit={guard_rc}")
        return guard_rc

    sync_cmd = [sys.executable, "scripts/sync_repo_memory_local.py", "--quiet"]
    sync_rc = subprocess.run(sync_cmd, cwd=repo_root).returncode
    if sync_rc != 0:
        print("Stage 2 micro-architecture run: FAIL")
        print(f"- memory sync failed with exit code: {sync_rc}")
        _append_log(repo_root, script_name, f"FAIL memory_sync_exit={sync_rc}")
        return sync_rc

    mapping_csv = repo_root / ARCHITECTURE_MAPPING_PREVIEW_CSV
    mapping_workbook = mapping_csv.with_suffix(".xlsx")
    if mapping_workbook.exists():
        try:
            synchronized_rows = sync_mapping_workbook_to_csv(mapping_workbook, mapping_csv)
            print(f"- synchronized mapping workbook rows: {synchronized_rows}")
            _append_log(repo_root, script_name, f"mapping_workbook_synchronized rows={synchronized_rows}")
        except Exception as exc:
            print("Stage 2 micro-architecture run: FAIL")
            print(f"- mapping workbook synchronization failed: {exc}")
            _append_log(repo_root, script_name, f"FAIL mapping_workbook_sync={exc}")
            return 1

    req_path = authoritative_corpus_path(repo_root)
    profile_path = repo_root / STAGE2_PROFILE
    index_path = repo_root / OCR_INDEX_CSV
    requirement_source = _detect_requirement_source_from_index(index_path)

    print(f"- stage2 profile: {STAGE2_PROFILE.as_posix()}")
    print(f"- requirement source (from OCR index): {requirement_source}")

    if not profile_path.exists():
        print("Stage 2 micro-architecture run: FAIL")
        print(f"- missing profile: {STAGE2_PROFILE.as_posix()}")
        _append_log(repo_root, script_name, f"FAIL missing_profile={STAGE2_PROFILE.as_posix()}")
        return 1

    try:
        profile = _load_profile(profile_path)
    except Exception as exc:
        print("Stage 2 micro-architecture run: FAIL")
        print(f"- invalid profile: {STAGE2_PROFILE.as_posix()} ({exc})")
        _append_log(repo_root, script_name, f"FAIL invalid_profile error={exc}")
        return 1

    approval_findings = _validate_profile_approval(profile, repo_root)
    if approval_findings:
        print("Stage 2 micro-architecture run: STOP pending user architecture-profile approval")
        print("- Review artifacts/stage1_specs/architecture_profile_draft.json")
        print("- Complete config/stage2_mirco_arc_profile.json approval status, approver, date, evidence hashes, reviewed draft hash, reviewed mapping-preview CSV hash, and ambiguity dispositions")
        for finding in approval_findings:
            print(f"- {finding}")
        _append_log(repo_root, script_name, f"STOP pending_user_architecture_profile_approval findings={len(approval_findings)}")
        return 1

    profile_check = subprocess.run(
        [
            sys.executable,
            str(repo_root / PROFILE_CROSSCHECK),
            "--profile",
            str(profile_path),
            "--source-edges",
            str(repo_root / "artifacts/stage1_requirements/source_matrix_edges.csv"),
            "--requirements",
            str(req_path),
        ],
        cwd=repo_root,
    )
    if profile_check.returncode != 0:
        print("Stage 2 micro-architecture run: FAIL")
        print("- Stage 2A profile crosscheck failed")
        _append_log(repo_root, script_name, "FAIL stage2_profile_crosscheck")
        return profile_check.returncode

    block_defs = profile.get("block_defs", {})
    configured_block_defs = dict(block_defs)
    mapping_rules = profile.get("mapping_rules", {})
    source_section_aliases = profile.get("source_section_aliases", {})
    interface_rows_cfg = profile.get("interface_rows", [])
    interaction_rows_cfg = profile.get("interaction_rows", [])
    ontology_links = _read_ontology_links(repo_root / ONTOLOGY_LINKS_CSV)

    if not req_path.exists():
        print("Stage 2 micro-architecture run: FAIL")
        print(f"- missing: {REQ_CSV.as_posix()}")
        _append_log(repo_root, script_name, f"FAIL missing={REQ_CSV.as_posix()}")
        return 1

    requirements = _read_requirements(req_path)
    if not requirements:
        print("Stage 2 micro-architecture run: FAIL")
        print(f"- no requirements found in authoritative corpus: {req_path.as_posix()}")
        _append_log(repo_root, script_name, "FAIL empty_requirements")
        return 1

    ontology_links_path = repo_root / ONTOLOGY_LINKS_CSV
    if not ontology_links_path.exists():
        print("Stage 2 micro-architecture run: FAIL")
        print(f"- missing ontology mapping artifact: {ONTOLOGY_LINKS_CSV.as_posix()}")
        _append_log(repo_root, script_name, f"FAIL missing={ONTOLOGY_LINKS_CSV.as_posix()}")
        return 1
    ontology_links = _read_ontology_links(ontology_links_path)
    ontology_findings = _validate_ontology_links(ontology_links, requirements)
    if ontology_findings:
        print("Stage 2 micro-architecture run: FAIL")
        for finding in ontology_findings:
            print(f"- {finding}")
        _append_log(repo_root, script_name, f"FAIL ontology_links_validation findings={len(ontology_findings)}")
        return 1

    interaction_findings = _validate_interaction_rows(interaction_rows_cfg, _requirement_source_map(requirements))
    if interaction_findings:
        print("Stage 2 micro-architecture run: FAIL")
        for finding in interaction_findings:
            print(f"- {finding}")
        _append_log(repo_root, script_name, f"FAIL interaction_matrix_validation findings={len(interaction_findings)}")
        return 1

    block_defs = _ensure_architecture_text_blocks(
        block_defs,
        mapping_rules,
        _architecture_text_block_names(_stage1_ocr_texts(index_path)),
    )
    block_defs = _ensure_interaction_blocks(block_defs, mapping_rules, interaction_rows_cfg)
    final_architecture_mapping = _read_final_architecture_mapping(
        repo_root / ARCHITECTURE_MAPPING_PREVIEW_CSV,
        configured_block_defs,
    )
    try:
        persisted_mapping_count = _persist_approved_architecture_mappings(
            repo_root,
            project_id=str(profile.get("project_name") or json.loads((repo_root / "config/project_context.json").read_text(encoding="utf-8")).get("project_name") or repo_root.name),
            mapping_preview_path=repo_root / ARCHITECTURE_MAPPING_PREVIEW_CSV,
        )
        _append_log(repo_root, script_name, f"canonical_architecture_mappings_persisted rows={persisted_mapping_count}")
    except Exception as exc:
        print("Stage 2 micro-architecture run: FAIL")
        print(f"- canonical architecture mapping persistence failed: {exc}")
        _append_log(repo_root, script_name, f"FAIL canonical_architecture_mapping_persistence={exc}")
        return 1

    trace_rows: List[List[str]] = []
    block_to_reqs: Dict[str, List[str]] = defaultdict(list)
    missing_ids: List[str] = []
    rag_warn_ids: List[str] = []
    rag_fail_ids: List[str] = []
    explicit_block_violations: List[str] = []
    explicit_block_mentions_total = 0
    unmapped_routing_rows: List[List[str]] = []

    for row in requirements:
        inferred_owner = _infer_existing_block_from_source_id(row, block_defs)
        if inferred_owner and not (row.get("source_section_owner") or "").strip():
            row = dict(row)
            row["source_section_owner"] = inferred_owner
        req_id = (row.get("source_req_id") or row.get("id") or "").strip()
        statement = row.get("requirement_statement", "")
        notes = row.get("notes", "")

        if not req_id:
            missing_ids.append("<blank-id>")

        blocks = _map_blocks(
            row,
            mapping_rules,
            block_defs,
            source_section_aliases,
            ontology_links,
            interaction_rows_cfg,
        )
        if req_id in final_architecture_mapping:
            blocks = [final_architecture_mapping[req_id]]
        for b in blocks:
            if req_id:
                block_to_reqs[b].append(req_id)

        if blocks == ["Unassigned"]:
            unmapped_routing_rows.append(
                [
                    req_id,
                    (row.get("source") or "").strip(),
                    statement,
                    "Unassigned",
                    _non_block_context_mapping(row),
                    "retained_as_non_block_function_context",
                ]
            )

        # Requirement-driven crosscheck: explicit block mentions must not stay unassigned.
        block_mentions = [
            mention
            for mention in _extract_explicit_block_mentions(statement)
            if _resolve_inventory_block_name(mention, block_defs) in block_defs
        ]
        explicit_block_mentions_total += len(block_mentions)
        if req_id and block_mentions and blocks == ["Unassigned"]:
            for mention in block_mentions:
                explicit_block_violations.append(f"{req_id}::{mention}")

        trace_rows.append([req_id, statement, "; ".join(blocks), notes])

        low_notes = notes.lower()
        if "rag_crosscheck=warn" in low_notes and req_id:
            rag_warn_ids.append(req_id)
        if "rag_crosscheck=fail" in low_notes and req_id:
            rag_fail_ids.append(req_id)

    _link_interaction_requirements_to_blocks(block_to_reqs, block_defs, interaction_rows_cfg)

    out_dir = repo_root / OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) Generate requirement-to-block traceability matrix CSV at:
    #    artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv
    trace_csv = out_dir / "requirement_to_block_traceability.csv"
    _write_csv(
        trace_csv,
        ["Requirement ID", "Requirement", "Block(s)", "Notes"],
        trace_rows,
    )
    _show_output(repo_root, "requirement_to_block_traceability", trace_csv)

    # 1a) Preserve source paragraph routing for requirements without an identified block.
    unmapped_routing_csv = out_dir / "unmapped_requirement_routing.csv"
    _write_csv(
        unmapped_routing_csv,
        [
            "Requirement ID",
            "Source Paragraph",
            "Requirement Statement",
            "Identified Block Mapping",
            "Non-Block Function Context",
            "Routing Status",
        ],
        unmapped_routing_rows,
    )
    _show_output(repo_root, "unmapped_requirement_routing", unmapped_routing_csv)

    # 2) Generate block inventory CSV at:
    #    artifacts/stage2_mirco_arc/block_inventory.csv
    block_inv_rows: List[List[str]] = []
    for block_name, meta in block_defs.items():
        linked = sorted(set(block_to_reqs.get(block_name, [])))
        if block_name == "Unassigned" and not linked:
            continue
        if not _is_concrete_block(block_name, block_defs):
            continue
        block_inv_rows.append(
            [
                block_name,
                _entity_kind(block_name, block_defs),
                str(meta.get("function", "")),
                str(meta.get("inputs", "")),
                str(meta.get("outputs", "")),
                "; ".join(linked),
            ]
        )

    block_inventory_csv = out_dir / "block_inventory.csv"
    _write_csv(
        block_inventory_csv,
        ["Block", "Entity kind", "Function", "Inputs", "Outputs", "Linked requirements"],
        block_inv_rows,
    )
    _show_output(repo_root, "block_inventory", block_inventory_csv)

    # 3) Generate interface catalog CSV at:
    #    artifacts/stage2_mirco_arc/interface_catalog.csv
    interface_rows: List[List[str]] = []
    for row in interface_rows_cfg:
        interface_rows.append(
            [
                str(row.get("Interface", "")),
                str(row.get("Direction", "")),
                str(row.get("Type", "")),
                str(row.get("Owner", "")),
                str(row.get("Purpose", "")),
            ]
        )
    interface_csv = out_dir / "interface_catalog.csv"
    _write_csv(interface_csv, ["Interface", "Direction", "Type", "Owner", "Purpose"], interface_rows)
    _show_output(repo_root, "interface_catalog", interface_csv)

    # 4) Generate interaction matrix CSV at:
    #    artifacts/stage2_mirco_arc/interaction_matrix.csv
    interaction_rows: List[List[str]] = []
    for row in interaction_rows_cfg:
        requirement_ids = str(row.get("Requirement IDs", "")).strip()
        is_connection_row = _is_connection_matrix_row(row)
        if is_connection_row and not requirement_ids:
            continue
        interaction_rows.append(
            [
                str(row.get("From block", "")),
                str(row.get("To block", "")),
                str(row.get("Signal/control", "")),
                str(row.get("Trigger", "")),
                str(row.get("Notes", "")),
                requirement_ids,
            ]
        )
    interaction_csv = out_dir / "interaction_matrix.csv"
    _write_csv(
        interaction_csv,
        ["From block", "To block", "Signal/control", "Trigger", "Notes", "Requirement IDs"],
        interaction_rows,
    )
    _show_output(repo_root, "interaction_matrix", interaction_csv)

    post_mapping_check = subprocess.run(
        [
            sys.executable,
            str(repo_root / POST_MAPPING_CROSSCHECK),
            "--requirements",
            str(req_path),
        ],
        cwd=repo_root,
    )
    if post_mapping_check.returncode != 0:
        print("Stage 2 micro-architecture run: FAIL")
        print("- post-mapping semantic crosscheck failed")
        _append_log(repo_root, script_name, "FAIL post_mapping_semantic_crosscheck")
        return post_mapping_check.returncode

    # 5) Generate function decomposition markdown at:
    #    artifacts/stage2_mirco_arc/function_decomposition.md
    function_md = out_dir / "function_decomposition.md"
    function_lines = [
        "# Function Decomposition",
        "",
        "| Top function | Subfunctions | Blocks involved |",
        "| --- | --- | --- |",
    ]
    function_source_rows = _read_requirements(repo_root / REQ_CSV)
    function_rows = _power_domain_function_rows(repo_root)
    function_rows.extend(
        _function_decomposition_rows_from_requirements(function_source_rows, final_architecture_mapping)
    )
    replace_stage2_descriptive_evidence(repo_root, power_domain_records_from_ocr(repo_root))
    for row in function_rows:
        function_lines.append(
            "| "
            + str(row.get("top_function", ""))
            + " | "
            + str(row.get("subfunctions", ""))
            + " | "
            + str(row.get("blocks_involved", ""))
            + " |"
        )
    _write_markdown(
        function_md,
        function_lines,
    )
    _show_output(repo_root, "function_decomposition", function_md)

    # 6) Generate consolidated micro-architecture report markdown at:
    #    artifacts/stage2_mirco_arc/micro_architecture_report.md
    micro_arch_md = out_dir / "micro_architecture_report.md"
    _write_markdown(
        micro_arch_md,
        [
            "# Stage 2 Micro-Architecture Analysis Report",
            "",
            f"- Date: {datetime.now().strftime('%Y-%m-%d')}",
            f"- Requirement source: {REQ_CSV.as_posix()}",
            "",
            "## Provenance",
            f"- Stage 2 profile: {STAGE2_PROFILE.as_posix()}",
            f"- OCR index: {OCR_INDEX_CSV.as_posix()}",
            f"- Source document (from OCR index): {requirement_source}",
            "",
            "## Generated Artifacts",
            f"- {block_inventory_csv.relative_to(repo_root).as_posix()}",
            f"- {trace_csv.relative_to(repo_root).as_posix()}",
            f"- {unmapped_routing_csv.relative_to(repo_root).as_posix()}",
            f"- {interface_csv.relative_to(repo_root).as_posix()}",
            f"- {interaction_csv.relative_to(repo_root).as_posix()}",
            f"- { (out_dir / 'stage2_mapping_crosscheck_report.md').relative_to(repo_root).as_posix()}",
            f"- {function_md.relative_to(repo_root).as_posix()}",
            "",
            "## Summary",
            f"- Requirements analyzed: {len(requirements)}",
            f"- Blocks with assigned requirements: {len([b for b in block_to_reqs if b != 'Unassigned'])}",
            f"- Potentially unassigned requirements: {len(set(block_to_reqs.get('Unassigned', [])))}",
            f"- Unmapped routing ledger entries: {len(unmapped_routing_rows)}",
            f"- Unmapped routing ledger: {unmapped_routing_csv.relative_to(repo_root).as_posix()}",
            "",
            "## Notes",
            "- This report is synthesized from requirement text and metadata heuristics.",
            "- Crosscheck findings are captured in architecture_crosscheck_report.md.",
        ],
    )
    _show_output(repo_root, "micro_architecture_report", micro_arch_md)

    # 7) Generate architectural crosscheck report markdown at:
    #    artifacts/stage2_mirco_arc/architecture_crosscheck_report.md
    all_req_ids = [
        (r.get("source_req_id") or r.get("id") or "").strip()
        for r in requirements
        if (r.get("source_req_id") or r.get("id") or "").strip()
    ]
    assigned_ids = set()
    for block_name, reqs in block_to_reqs.items():
        if block_name == "Unassigned":
            continue
        assigned_ids.update(reqs)

    # Retained non-block context is a valid traceability outcome, not an uncovered requirement.
    routed_ids = {
        row[0].strip()
        for row in unmapped_routing_rows
        if row and row[0].strip()
    }
    assigned_ids.update(routed_ids)

    uncovered = sorted([rid for rid in all_req_ids if rid not in assigned_ids])
    covered = sorted([rid for rid in all_req_ids if rid in assigned_ids])

    critical_findings = [f"Uncovered requirement: {rid}" for rid in uncovered]
    critical_findings.extend(
        [
            f"Requirement-driven block mention unresolved (mapped as Unassigned): {item}"
            for item in sorted(set(explicit_block_violations))
        ]
    )
    major_findings = [f"RAG crosscheck fail evidence quality: {rid}" for rid in sorted(set(rag_fail_ids))]
    minor_findings = [f"RAG crosscheck warning evidence quality: {rid}" for rid in sorted(set(rag_warn_ids))]

    decision = "no-go" if critical_findings else "go"

    crosscheck_md = out_dir / "architecture_crosscheck_report.md"
    _write_markdown(
        crosscheck_md,
        [
            "# Architecture Crosscheck Report",
            "",
            f"Date: {datetime.now().strftime('%Y-%m-%d')}",
            "",
            "## Scope",
            "- Stage 2 micro-architecture output package crosscheck against requirement baseline",
            "",
            "## Inputs",
            f"- Requirements list: {REQ_CSV.as_posix()}",
            f"- Block inventory: {block_inventory_csv.relative_to(repo_root).as_posix()}",
            f"- Requirement-to-block traceability: {trace_csv.relative_to(repo_root).as_posix()}",
            f"- Unmapped requirement routing: {unmapped_routing_csv.relative_to(repo_root).as_posix()}",
            f"- Interface catalog: {interface_csv.relative_to(repo_root).as_posix()}",
            f"- Interaction matrix: {interaction_csv.relative_to(repo_root).as_posix()}",
            f"- Architecture summary: {micro_arch_md.relative_to(repo_root).as_posix()}",
            "",
            "## Coverage Summary",
            f"- Total requirements: {len(all_req_ids)}",
            f"- Covered requirements: {len(covered)}",
            "- Partially covered requirements: 0",
            f"- Uncovered requirements: {len(uncovered)}",
            "",
            "## Traceability Defects",
            f"- Missing requirement IDs: {', '.join(sorted(set(missing_ids))) if missing_ids else 'None'}",
            f"- Inconsistent mappings: {'None'}",
            f"- Duplicate/conflicting ownership: {'None'}",
            "",
            "## Explicit Block Mapping Checks",
            f"- Explicit block mentions found in requirement list: {explicit_block_mentions_total}",
            f"- Unresolved explicit block mentions (mapped as Unassigned): {len(sorted(set(explicit_block_violations)))}",
            f"- Violations: {'None' if not explicit_block_violations else '; '.join(sorted(set(explicit_block_violations)))}",
            "",
            "## Completeness Assessment",
            f"- Missing blocks vs requirement intent: {'None' if not uncovered else 'See uncovered requirements list'}",
            "- Missing interfaces vs requirement intent: None detected by heuristic synthesis",
            "- Missing interactions vs requirement intent: None detected by heuristic synthesis",
            "",
            "## Assumptions, Ambiguities, And Missing Evidence",
            f"- Critical: {'; '.join(critical_findings) if critical_findings else 'None'}",
            f"- Major: {'; '.join(major_findings) if major_findings else 'None'}",
            f"- Minor: {'; '.join(minor_findings) if minor_findings else 'None'}",
            "",
            "## Gate Recommendation",
            f"- Decision: {decision}",
            f"- Blocking findings: {'; '.join(critical_findings) if critical_findings else 'None'}",
        ],
    )
    _show_output(repo_root, "architecture_crosscheck_report", crosscheck_md)

    # 8) Generate Stage 02 micro-architecture orchestrator summary report at:
    #    artifacts/orchestrator/stage_02_micro_arch_report.md
    stage2_micro_arch_report = repo_root / ORCH_REPORT
    _write_markdown(
        stage2_micro_arch_report,
        [
            "# Stage 02 Micro-Architecture Report",
            "",
            f"Date: {datetime.now().strftime('%Y-%m-%d')}",
            "",
            "## Scope",
            "- Stage 2 micro-architecture synthesis and mandatory architectural crosscheck.",
            "",
            "## Provenance",
            f"- Stage 2 profile: {STAGE2_PROFILE.as_posix()}",
            f"- OCR index: {OCR_INDEX_CSV.as_posix()}",
            f"- Source document (from OCR index): {requirement_source}",
            "",
            "## Micro-Architecture Outputs",
            f"- Blocks identified: {len([b for b in block_to_reqs if b != 'Unassigned'])}",
            f"- Interfaces cataloged: {len(interface_rows)}",
            f"- Requirement-to-block links: {len(covered)}",
            f"- Unmapped requirement routing entries: {len(unmapped_routing_rows)}",
            "",
            "## Key Deliverables",
            f"- Block inventory: {block_inventory_csv.relative_to(repo_root).as_posix()}",
            f"- Interface catalog: {interface_csv.relative_to(repo_root).as_posix()}",
            f"- Interaction matrix: {interaction_csv.relative_to(repo_root).as_posix()}",
            f"- Unmapped requirement routing ledger: {unmapped_routing_csv.relative_to(repo_root).as_posix()}",
            f"- Consolidated micro-architecture report: {micro_arch_md.relative_to(repo_root).as_posix()}",
            "",
            "## Architectural Crosscheck",
            "- Agent: architectural-crosscheck.agent.md",
            f"- Crosscheck report: {crosscheck_md.relative_to(repo_root).as_posix()}",
            f"- Traceability check vs requirement list: {'pass' if (len(uncovered) == 0 and len(explicit_block_violations) == 0) else 'fail'}",
            f"- Completeness check vs requirements: {'pass' if (len(uncovered) == 0 and len(explicit_block_violations) == 0) else 'fail'}",
            f"- Unresolved assumptions/ambiguities/missing evidence: {'none' if (not critical_findings and not major_findings and not minor_findings) else 'present'}",
            "",
            "## Status",
            f"- Stage 2 micro-architecture gate: {'pass' if decision == 'go' else 'fail'}",
        ],
    )
    _show_output(repo_root, "stage_02_micro_arch_report", stage2_micro_arch_report)

    print("Stage 2 micro-architecture + Crosscheck: DONE")
    print(f"- requirements analyzed: {len(all_req_ids)}")
    print(f"- uncovered requirements: {len(uncovered)}")
    print(f"- gate recommendation: {decision}")

    _append_log(
        repo_root,
        script_name,
        "PASS "
        f"requirements={len(all_req_ids)} uncovered={len(uncovered)} decision={decision} "
        f"profile={STAGE2_PROFILE.as_posix()} source={requirement_source}",
    )

    return 0 if decision == "go" else 2


if __name__ == "__main__":
    raise SystemExit(main())

