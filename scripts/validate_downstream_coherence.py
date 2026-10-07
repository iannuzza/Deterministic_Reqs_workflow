#!/usr/bin/env python3
"""Read-only downstream coherence validator.

Architectural authority comes only from approved mapping and snapshot materialization.
Stage 2 SysML is a derived structural artifact; its review is not an authority source
or a prerequisite for interpreting the downstream contract.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from approved_snapshot_resolver import resolve_complete_authoritative_input
from requirement_allocation_policy import requires_hierarchy_parent
from workflow_routing import (
    validate_document_author_fields,
    approved_snapshot_candidate_rows,
    IPOS_LOCAL_ANALOG_TOPIC_SPECS,
    IPOS_LOCAL_DIGITAL_TOPIC_SPECS,
    validate_ipos_descriptive_output,
    build_ipos_functional_input,
    build_ipos_normalized_records,
    extract_ipos_structural_function_name,
)
from spec_document_contract import validate_materialization_chain, validate_drs_document_contract

TRACE_ARTIFACTS = {
    "SRS": Path("artifacts/stage3_srs/srs_traceability_matrix.csv"),
    "ARS": Path("artifacts/stage4_ars/ars_traceability_matrix.csv"),
    "DRS": Path("artifacts/stage5_drs/drs_traceability_matrix.csv"),
    "Digital IPOS": Path("artifacts/stage6_digital_ipos/ipos_traceability_matrix.csv"),
    "Analog IPOS": Path("artifacts/stage7_analog_ipos/ipos_traceability_matrix.csv"),
}

REQUIRED_TRACE_FIELDS = (
    "snapshot_id",
    "allocation_class",
    "owning_target",
    "lineage_mode",
    "source_origin_req_ids",
    "hierarchy_parent_req_ids",
    "owning_domain",
)

GENERATOR_FILES = (
    "scripts/run_srs_gen_spec_agent.py",
    "scripts/run_ars_gen_spec_agent.py",
    "scripts/run_drs_gen_spec_agent.py",
    "scripts/generate_ipos_specs.py",
)

RUNTIME_USER_METADATA_RULE = (
    "The local process username may be used only for generated-document Author metadata "
    "and non-authoritative audit/log actor fields; it must never select or alter snapshot, "
    "allocation, ownership, partition, traceability, or explicit reviewer authority."
)

BLOCK_OVERVIEW_POLICY = (
    "Descriptive sections use natural technical prose and readable function summaries bounded by "
    "approved document-specific authority, with deterministic rendering and independent final-text "
    "and provenance validation. The DRS pilot covers only approved concrete digital blocks and "
    "their inventory functions; its complete approved block I/O remains tabular. SRS and ARS "
    "retain their existing output contracts until separately authorized."
)

INFERENCE_MARKERS = (
    "_infer_owner_from_source_id",
    "_infer_analog_blocks",
    "_infer_digital_blocks",
    "_normalize_req_to_analog_ownership",
)

APPROVED_LABEL_CANONICALS = {
    "adc": "ADC",
    "adsp": "ADSP",
    "bist": "BIST Controller",
    "bist controller": "BIST Controller",
    "digital": "Digital Subsystem",
    "digital subsystem": "Digital Subsystem",
    "i2c interface": "I2C interface",
    "i2c/spi ahb": "I2C_SPI_AHB",
    "i2c spi ahb": "I2C_SPI_AHB",
    "irq logic": "IRQ logic",
    "ispu debug": "ISPU debug",
    "main controller": "Main Controller",
    "pad mux": "Pad Mux",
    "pmu": "PMU",
    "regmap": "Regmap",
    "sensor hub": "Sensor-Hub",
    "smart fifo": "Smart FIFO",
    "fifo": "Smart FIFO",
}


def normalize_human_label(value: object) -> str:
    """Normalize only deterministic human-label spelling differences."""
    text = str(value or "").casefold().replace("-", " ").replace("_", " ")
    return " ".join(text.split())


def human_label_key(value: object) -> str:
    """Return the central semantic key for a human-readable label."""
    normalized = normalize_human_label(value)
    return normalize_human_label(APPROVED_LABEL_CANONICALS.get(normalized, normalized))


def canonical_human_label(value: object) -> str:
    """Return the approved display label without fuzzy or inferred matching."""
    normalized = normalize_human_label(value)
    return APPROVED_LABEL_CANONICALS.get(normalized, str(value or "").strip())


def ipos_authored_requirement_id(block_name: object, sequence: int) -> str:
    """Build the sole stable authored-ID format for Digital and Analog IPOS."""
    approved_block = canonical_human_label(block_name)
    block_token = re.sub(r"[^A-Z0-9]+", "-", approved_block.upper()).strip("-")
    if not block_token:
        raise DownstreamCoherenceError("IPOS authored requirement requires an approved concrete block name.")
    return f"IPOS-{block_token}-{sequence:03d}"


class DownstreamCoherenceError(RuntimeError):
    pass


class DownstreamContract:
    """The shared snapshot-bound contract consumed by downstream stages."""

    def __init__(self, requirement_input, selection: dict[str, Any]):
        self.requirement_input = requirement_input
        self.selection = selection
        self.snapshot_id = requirement_input.snapshot_id
        self.expected = _expected_allocations(requirement_input)

    def allocation(self, source_req_id: str) -> dict[str, str]:
        return self.expected.get((source_req_id or "").strip(), {})

    def target(self, source_req_id: str) -> str:
        return str(self.allocation(source_req_id).get("owning_target") or "").strip()

    def allocation_class(self, source_req_id: str) -> str:
        return str(self.allocation(source_req_id).get("allocation_class") or "").strip()

    def source_ids_for_target(self, target: str) -> set[str]:
        return {source_id for source_id in self.expected if self.target(source_id) == target}

    def metadata(self, source_req_id: str) -> dict[str, str]:
        allocation = self.allocation(source_req_id)
        return {field: str(allocation.get(field) or "").strip() for field in REQUIRED_TRACE_FIELDS}

    def concrete_owner(self, source_req_id: str, concrete_blocks: set[str]) -> str:
        """Return only an explicitly approved owner that exists in the inventory."""
        owner = str(self.allocation(source_req_id).get("approved_block") or "").strip()
        return owner if owner in concrete_blocks else ""

    def valid_empty(self, target: str, rows: list[dict[str, str]]) -> bool:
        return not self.source_ids_for_target(target) and not rows


def downstream_contract_fingerprint(contract: DownstreamContract) -> str:
    """Hash the operational allocation contract, excluding candidate lineage evidence."""
    payload = {
        source_id: {
            key: str(value or "").strip()
            for key, value in sorted(metadata.items())
            if key not in {"canonical_id", "lineage_candidate_parent_req_ids"}
        }
        for source_id, metadata in sorted(contract.expected.items())
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def resolve_downstream_contract(repo_root: Path, snapshot_id: str | None = None) -> DownstreamContract:
    requirement_input, selection = resolve_complete_authoritative_input(
        repo_root,
        "downstream-contract",
        project_id=_project_id(repo_root),
        snapshot_id=snapshot_id,
    )
    return DownstreamContract(requirement_input, selection)


def approved_sysml_block_scope(repo_root: Path, snapshot_id: str | None = None) -> set[str]:
    """Return concrete SysML blocks with approved IPOS requirement scope."""
    contract = resolve_downstream_contract(repo_root, snapshot_id)
    return {
        canonical_human_label(str(allocation.get("approved_block") or "").strip())
        for allocation in contract.expected.values()
        if str(allocation.get("owning_target") or "").strip() in {"Digital IPOS", "Analog IPOS"}
        and str(allocation.get("approved_block") or "").strip()
    }


def snapshot_architecture_context(repo_root: Path, contract: DownstreamContract) -> dict:
    from canonical_store import connect

    connection = connect(repo_root)
    try:
        snapshot = connection.execute("SELECT project_id, metadata_json FROM snapshots WHERE snapshot_id = ?",
                                      (contract.snapshot_id,)).fetchone()
        fingerprint = json.loads(snapshot["metadata_json"])["profiles"]["architecture"]
        rows = connection.execute(
            "SELECT * FROM profile_revisions WHERE project_id = ? AND profile_kind = ? "
            "AND content_fingerprint = ? AND approval_state = ? AND lifecycle_state = ?",
            (snapshot["project_id"], "architecture", fingerprint, "approved", "approved"),
        ).fetchall()
        if not rows:
            raise DownstreamCoherenceError("Snapshot-bound approved architecture profile is unavailable.")
        payloads = [json.loads(row["profile_payload_json"]) for row in rows]
        if any(payload != payloads[0] for payload in payloads):
            raise DownstreamCoherenceError("Snapshot-bound architecture profile is ambiguous.")
        return {"payload": payloads[0], "fingerprint": fingerprint}
    finally:
        connection.close()


def srs_catalog_from_context(inventory: list[dict[str, str]], contract: DownstreamContract,
                             context: dict) -> tuple[list[dict[str, str]], list[str]]:
    definitions = context["payload"].get("block_defs", {})
    entries: list[dict[str, str]] = []
    findings: list[str] = []
    categories = {"analog": "analog", "mixed signal": "analog", "digital": "digital",
                  "digital or system": "digital"}
    seen: set[str] = set()
    for row in inventory:
        block = str(row.get("Block") or "").strip()
        key = human_label_key(block)
        if not key:
            continue
        if key in seen:
            findings.append(f"SRS_CATALOG_DUPLICATE: {block}")
            continue
        seen.add(key)
        matches = [value for name, value in definitions.items() if human_label_key(name) == key]
        allocations = [(source_id, value) for source_id, value in contract.expected.items()
                       if human_label_key(value.get("approved_block")) == key]
        if not matches and not allocations:
            findings.append(f"SRS_CATALOG_APPROVAL_MISSING: {block}")
            continue
        if any(str(value.get("entity_kind") or "").casefold() in {"interface", "group", "subsystem"}
               for value in matches):
            continue
        classifications = {categories[normalize_human_label(value.get("classification"))]
                           for value in matches if normalize_human_label(value.get("classification")) in categories}
        classifications.update(categories[normalize_human_label(value.get("owning_domain"))]
                               for _, value in allocations if normalize_human_label(value.get("owning_domain")) in categories)
        functions = {str(value.get("function") or "").strip() for value in matches if value.get("function")}
        if len(classifications) != 1:
            findings.append(f"SRS_CATALOG_CLASSIFICATION_{'CONFLICT' if classifications else 'MISSING'}: {block}")
            continue
        if len(functions) != 1:
            findings.append(f"SRS_CATALOG_FUNCTION_{'CONFLICT' if functions else 'MISSING'}: {block}")
            continue
        entries.append({"block": block, "category": next(iter(classifications)), "function": next(iter(functions)),
                        "source": "snapshot architecture profile:" + context["fingerprint"],
                        "classification_sources": json.dumps([source_id for source_id, _ in allocations]),
                        "snapshot_id": contract.snapshot_id})
    return entries, findings


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]


def _project_id(repo_root: Path) -> str:
    context = repo_root / "config/project_context.json"
    if not context.exists():
        return repo_root.name
    payload = json.loads(context.read_text(encoding="utf-8"))
    return str(payload.get("project_name") or repo_root.name)


def _source_id(row: dict[str, str]) -> str:
    return (row.get("source_req_id") or row.get("req_id") or row.get("id") or "").strip()


def _expected_allocations(requirement_input) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for requirement in requirement_input.rows:
        canonical_id = str(requirement.get("canonical_id") or "").strip()
        source_id = _source_id(requirement)
        metadata = dict(requirement_input.allocation.get(canonical_id) or {})
        if source_id:
            metadata["canonical_id"] = canonical_id
            metadata["source_req_id"] = source_id
            result[source_id] = metadata
    return result


def _check_snapshot_and_allocations(repo_root: Path, snapshot_id: str, requirement_input) -> list[str]:
    findings: list[str] = []
    if requirement_input.snapshot_id != snapshot_id:
        findings.append(
            f"SNAPSHOT_SELECTOR_MISMATCH: resolver returned {requirement_input.snapshot_id}, expected {snapshot_id}"
        )
    expected = _expected_allocations(requirement_input)
    if not expected:
        findings.append("SNAPSHOT_ALLOCATION_EMPTY: explicit snapshot resolved without allocation metadata")
    for source_id, metadata in expected.items():
        required = ("allocation_class", "owning_target", "lineage_mode", "source_origin_req_ids", "owning_domain")
        missing = [field for field in required if not str(metadata.get(field) or "").strip()]
        if missing:
            findings.append(f"SNAPSHOT_METADATA_MISSING: {source_id}: {', '.join(missing)}")
        if requires_hierarchy_parent(
            str(metadata.get("allocation_class") or ""),
            str(metadata.get("lineage_mode") or ""),
        ) and not str(metadata.get("hierarchy_parent_req_ids") or "").strip():
            findings.append(f"SNAPSHOT_PARENT_MISSING: {source_id}: hierarchy_parent_req_ids")
    return findings


def _check_ledger(repo_root: Path, snapshot_id: str, expected: dict[str, dict[str, str]]) -> list[str]:
    findings: list[str] = []
    manifest_path = repo_root / "artifacts/traceability_reports/requirement_allocation_materialization.json"
    ledger_path = repo_root / "artifacts/traceability_reports/requirement_allocation_ledger.csv"
    if not manifest_path.exists() or not ledger_path.exists():
        return ["LEDGER_MISSING: allocation ledger or materialization manifest is missing"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"LEDGER_MANIFEST_INVALID: {exc}"]
    _, rows = _read_csv(ledger_path)
    manifest_snapshot = str(manifest.get("snapshot_id") or (manifest.get("selection") or {}).get("selected_snapshot_id") or "")
    if manifest_snapshot != snapshot_id:
        findings.append(
            f"LEDGER_STALE: materialization is {manifest_snapshot or '<missing>'}, explicit snapshot is {snapshot_id}"
        )
    if int(manifest.get("row_count") or -1) != len(rows):
        findings.append("LEDGER_ROW_COUNT_MISMATCH: manifest row_count does not match ledger")
    row_snapshot_ids = {str(row.get("snapshot_id") or "") for row in rows}
    if row_snapshot_ids != {snapshot_id}:
        findings.append(
            f"LEDGER_STALE_ROWS: ledger snapshot IDs are {sorted(row_snapshot_ids)}, expected only {snapshot_id}"
        )
    ledger_ids = {_source_id(row) for row in rows if _source_id(row)}
    expected_ids = set(expected)
    if ledger_ids != expected_ids:
        findings.append(
            f"LEDGER_REQUIREMENT_SET_MISMATCH: missing={len(expected_ids - ledger_ids)}, extra={len(ledger_ids - expected_ids)}"
        )
    for row in rows:
        source_id = _source_id(row)
        approved = expected.get(source_id)
        if approved is None:
            continue
        for field in ("allocation_class", "owning_target", "lineage_mode", "source_origin_req_ids", "owning_domain"):
            ledger_field = "hierarchy_or_coverage_class" if field == "allocation_class" else field
            if str(row.get(ledger_field) or "").strip() != str(approved.get(field) or "").strip():
                findings.append(f"LEDGER_METADATA_DRIFT: {source_id}: {field}")
    return findings


def _check_trace_artifact(
    stage: str,
    path: Path,
    rows: list[dict[str, str]],
    fields: list[str],
    snapshot_id: str,
    expected: dict[str, dict[str, str]],
) -> list[str]:
    findings: list[str] = []
    missing_fields = sorted(set(REQUIRED_TRACE_FIELDS) - set(fields))
    if missing_fields:
        findings.append(f"{stage}_TRACE_METADATA_MISSING: columns={','.join(missing_fields)}")
    source_ids = [_source_id(row) for row in rows if _source_id(row)]
    approved_ids = {
        source_id
        for source_id, allocation in expected.items()
        if str(allocation.get("owning_target") or "").strip() == stage
    }
    if not approved_ids and not rows:
        return findings
    if len(source_ids) != len(set(source_ids)):
        findings.append(f"{stage}_TRACE_DUPLICATE_SOURCE_IDS")
    expected_target = stage
    if stage in {"Digital IPOS", "Analog IPOS"}:
        expected_classes = {"block_local_digital"} if stage == "Digital IPOS" else {"block_local_analog"}
    else:
        expected_classes = {"system_level"} if stage == "SRS" else {"top_digital_architecture"} if stage == "DRS" else {"top_analog_architecture"}
    for row in rows:
        source_id = _source_id(row)
        if not source_id:
            findings.append(f"{stage}_TRACE_EMPTY_SOURCE_ID")
            continue
        approved = expected.get(source_id)
        if approved is None:
            findings.append(f"{stage}_TRACE_STALE_OR_UNKNOWN_SOURCE: {source_id}")
            continue
        if str(row.get("snapshot_id") or "").strip() != snapshot_id:
            findings.append(f"{stage}_TRACE_STALE_SNAPSHOT: {source_id}")
        if str(approved.get("owning_target") or "").strip() != expected_target:
            findings.append(
                f"{stage}_TARGET_MISMATCH: {source_id}: approved={approved.get('owning_target')}, expected={expected_target}"
            )
        if str(approved.get("allocation_class") or "").strip() not in expected_classes:
            findings.append(
                f"{stage}_PARTITION_MISMATCH: {source_id}: approved={approved.get('allocation_class')}"
            )
        for field in REQUIRED_TRACE_FIELDS:
            if field in fields and not str(row.get(field) or "").strip():
                if field != "hierarchy_parent_req_ids" or requires_hierarchy_parent(
                    str(approved.get("allocation_class") or ""),
                    str(approved.get("lineage_mode") or ""),
                ):
                    findings.append(f"{stage}_TRACE_METADATA_EMPTY: {source_id}: {field}")
    if stage == "DRS":
        expected_ids = {source_id for source_id, item in expected.items() if item.get("owning_target") == "DRS"}
        if set(source_ids) != expected_ids:
            findings.append(f"DRS_PARTITION_INCOMPLETE: missing={len(expected_ids - set(source_ids))}, extra={len(set(source_ids) - expected_ids)}")
    return findings


def _check_generator_inference(repo_root: Path) -> list[str]:
    findings: list[str] = []
    for relative in GENERATOR_FILES:
        path = repo_root / relative
        if not path.exists():
            findings.append(f"GENERATOR_MISSING: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in INFERENCE_MARKERS:
            if marker in text:
                lines = [str(index) for index, line in enumerate(text.splitlines(), 1) if marker in line]
                findings.append(f"GENERATOR_INFERENCE: {relative}: {marker}: lines={','.join(lines[:8])}")
    return findings


def _ipos_block_slug(block_name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", block_name.casefold()).strip("-") or "unnamed-block"


def approved_primary_source_name(repo_root: Path) -> str:
    """Return the primary source basename recorded by the Stage 1 OCR index."""
    index_path = repo_root / "artifacts/stage1_requirements/ocr_extracts/index.csv"
    if not index_path.exists():
        return ""
    _fields, rows = _read_csv(index_path)
    for row in rows:
        source_file = str(row.get("source_file") or "").strip()
        if source_file:
            return Path(source_file.replace("\\", "/")).name.casefold()
    return ""


def created_ipos_block_directories(repo_root: Path, stage: str) -> dict[str, Path]:
    """Return only IPOS block directories containing a generated document artifact."""
    if stage not in {"Digital IPOS", "Analog IPOS"}:
        raise ValueError(f"Unsupported IPOS stage: {stage}")
    output_root = repo_root / (
        "artifacts/stage6_digital_ipos" if stage == "Digital IPOS" else "artifacts/stage7_analog_ipos"
    )
    block_root = output_root / "blocks"
    if not block_root.exists():
        return {}
    return {
        path.name: path
        for path in sorted(block_root.iterdir(), key=lambda item: item.name.casefold())
        if path.is_dir() and (any(path.glob("*.md")) or any(path.glob("*.docx")))
    }


def approved_traceability_hierarchy(repo_root: Path) -> dict[str, object]:
    """Build the shared design/RM hierarchy from approved trace and mapping metadata."""
    ledger_rows = _read_csv(repo_root / "artifacts/traceability_reports/requirement_allocation_ledger.csv")[1]
    source_ids = {
        str(row.get("req_id") or row.get("source_req_id") or "").strip()
        for row in ledger_rows
        if str(row.get("req_id") or row.get("source_req_id") or "").strip()
    }
    matrix_paths = {
        "SRS": repo_root / TRACE_ARTIFACTS["SRS"],
        "ARS": repo_root / TRACE_ARTIFACTS["ARS"],
        "DRS": repo_root / TRACE_ARTIFACTS["DRS"],
        "Digital IPOS": repo_root / TRACE_ARTIFACTS["Digital IPOS"],
        "Analog IPOS": repo_root / TRACE_ARTIFACTS["Analog IPOS"],
    }
    supplementary_by_id: dict[str, str] = {}
    mapping_path = repo_root / "artifacts/stage1_specs/architecture_mapping_preview.csv"
    if mapping_path.exists():
        _fields, mapping_rows = _read_csv(mapping_path)
        for row in mapping_rows:
            req_id = str(row.get("requirement_id") or row.get("canonical_requirement_id") or "").strip()
            source = Path(str(row.get("supplementary_source_spec") or "").replace("\\", "/")).name
            if req_id and source and source.casefold() != approved_primary_source_name(repo_root):
                supplementary_by_id[req_id] = source

    def rows_for(path: Path) -> list[dict[str, str]]:
        return _read_csv(path)[1] if path.exists() else []

    def coverage_edges(label: str, rows: list[dict[str, str]]) -> list[str]:
        edges: list[str] = []
        for row in rows:
            upstream = str(
                row.get("covers_upstream_req_id")
                or row.get("source_req_id")
                or row.get("requirement_id")
                or ""
            ).strip()
            if not upstream:
                continue
            source = supplementary_by_id.get(upstream)
            target = f"supplementary source {source}" if source else f"approved source requirement {upstream}"
            edges.append(f"{label} -> {target} [{upstream}]")
        return list(dict.fromkeys(edges))

    def node(label: str, kind: str, artifact: str, rows: list[dict[str, str]], children: list[dict[str, object]] | None = None) -> dict[str, object]:
        coverage_ids = sorted({
            str(row.get("source_req_id") or row.get("requirement_id") or "").strip()
            for row in rows
            if str(row.get("source_req_id") or row.get("requirement_id") or "").strip()
        })
        edges = coverage_edges(label, rows)
        return {
            "label": label,
            "kind": kind,
            "artifact": artifact,
            "coverage_ids": coverage_ids,
            "covered": len(set(coverage_ids) & source_ids),
            "total": len(source_ids),
            "dependencies": "\n".join(edges),
            "coverage_edges": edges,
            "children": children or [],
        }

    root_rows = rows_for(matrix_paths["SRS"])
    analog_rows = rows_for(matrix_paths["ARS"])
    digital_rows = rows_for(matrix_paths["DRS"])
    analog_children: list[dict[str, object]] = [
        node("ARS - Analog Requirements Specification", "spec", matrix_paths["ARS"].relative_to(repo_root).as_posix(), analog_rows)
    ] if analog_rows else []
    digital_children: list[dict[str, object]] = [
        node("DRS - Digital Requirements Specification", "spec", matrix_paths["DRS"].relative_to(repo_root).as_posix(), digital_rows)
    ] if digital_rows else []

    for stage, parent_children, kind in (
        ("Digital IPOS", digital_children, "digital"),
        ("Analog IPOS", analog_children, "analog"),
    ):
        rows = rows_for(matrix_paths[stage])
        by_block: dict[str, list[dict[str, str]]] = {}
        block_order: list[str] = []
        for row in rows:
            block = canonical_human_label(row.get("mapped_block") or row.get("owning_block") or "")
            if not block:
                continue
            if block not in by_block:
                by_block[block] = []
                block_order.append(block)
            by_block[block].append(row)
        created = created_ipos_block_directories(repo_root, stage)
        for block in block_order:
            if not any(_ipos_block_slug(block) == _ipos_block_slug(name) for name in created):
                continue
            block_rows = by_block[block]
            parent_children.append(
                node(
                    f"{stage}: {block}",
                    "block",
                    next(path.relative_to(repo_root).as_posix() for name, path in created.items() if _ipos_block_slug(name) == _ipos_block_slug(block)),
                    block_rows,
                )
            )

    analog_subsystem = node(
        "Analog Subsystem",
        "design_level",
        "artifacts/stage2_mirco_arc/sysml/STBIOSystem.sysml",
        analog_rows,
        analog_children,
    )
    digital_subsystem = node(
        "Digital Subsystem",
        "design_level",
        "artifacts/stage2_mirco_arc/sysml/DigitalSubsystem.sysml",
        digital_rows,
        digital_children,
    )
    return node(
        "STBIOSystem",
        "design_root",
        "artifacts/stage2_mirco_arc/sysml/STBIOSystem.sysml",
        root_rows,
        [
            node("Top Analog Architecture", "design_level", "artifacts/stage2_mirco_arc/sysml/STBIOSystem.sysml", analog_rows, [analog_subsystem]),
            digital_subsystem,
        ],
    )


def _source_spec_node_metrics(
    source_ids: set[str],
    outgoing_edges: list[dict[str, object]],
) -> dict[str, object]:
    """Summarize approved downstream coverage against one source specification."""
    unique_source_ids = {value.strip() for value in source_ids if value.strip()}
    covered_source_ids: set[str] = set()
    downstream_coverage: list[dict[str, object]] = []
    for edge in outgoing_edges:
        statistics = edge.get("coverage") or {}
        if not isinstance(statistics, dict):
            continue
        edge_total = {
            str(value).strip()
            for value in statistics.get("total_unique_upstream_req_ids") or []
            if str(value).strip()
        } & unique_source_ids
        edge_covered = {
            str(value).strip()
            for value in statistics.get("covered_unique_upstream_req_ids") or []
            if str(value).strip()
        } & edge_total
        if not edge_total:
            continue
        covered_source_ids.update(edge_covered)
        downstream_coverage.append({
            "target": str(edge.get("target") or ""),
            "covered": len(edge_covered),
            "total": len(edge_total),
            "percentage": len(edge_covered) / len(edge_total) * 100.0,
        })
    return {
        "covered": len(covered_source_ids),
        "total": len(unique_source_ids),
        "percentage": len(covered_source_ids) / len(unique_source_ids) * 100.0 if unique_source_ids else 0.0,
        "downstream_coverage": downstream_coverage,
    }


def _approved_upstream_coverage(
    target_id: str,
    node_by_id: dict[str, dict[str, object]],
    edges: list[dict[str, object]],
) -> tuple[list[str], list[str], list[dict[str, object]]]:
    """Return one coverage entry per approved upstream specification relationship."""
    upstream_labels: list[str] = []
    upstream_statistics: list[str] = []
    upstream_metrics: list[dict[str, object]] = []
    seen_upstreams: set[str] = set()
    accepted_kinds = {
        "generated_document_covers",
        "approved_supplementary_covers",
        "approved_source_covers",
    }
    for edge in edges:
        if str(edge.get("target") or "") != target_id or str(edge.get("kind") or "") not in accepted_kinds:
            continue
        upstream_id = str(edge.get("source") or "")
        if not upstream_id or upstream_id in seen_upstreams:
            continue
        statistics = edge.get("coverage") or {}
        if not isinstance(statistics, dict):
            continue
        covered = int(statistics.get("covered") or 0)
        total = int(statistics.get("total") or 0)
        if covered <= 0 or total <= 0:
            continue
        seen_upstreams.add(upstream_id)
        upstream_label = str(node_by_id.get(upstream_id, {}).get("label") or upstream_id)
        percentage = float(statistics.get("percentage") or 0.0)
        upstream_labels.append(upstream_label)
        upstream_statistics.append(
            f"{upstream_label}: {covered} / {total} ({percentage:.1f}%)"
        )
        upstream_metrics.append({
            "upstream": upstream_label,
            "covered": covered,
            "total": total,
            "percentage": percentage,
        })
    return upstream_labels, upstream_statistics, upstream_metrics


def _source_spec_target_metrics(
    source_ids: set[str],
    target_rows: list[dict[str, str]],
) -> tuple[dict[str, object], dict[str, object]]:
    """Calculate reciprocal source-ID and target-requirement coverage for one target."""
    source_scope = {value.strip() for value in source_ids if value.strip()}
    target_scope: set[str] = set()
    source_covered: set[str] = set()
    target_covered: set[str] = set()
    target_id_fields = ("srs_req_id", "ars_req_id", "drs_req_id", "ipos_req_id", "requirement_id")
    for row in target_rows:
        target_id = next((str(row.get(field) or "").strip() for field in target_id_fields if str(row.get(field) or "").strip()), "")
        if target_id:
            target_scope.add(target_id)
        references = {
            str(row.get(field) or "").strip()
            for field in ("source_req_id", "covers_upstream_req_id")
        }
        for field in ("source_origin_req_ids", "hierarchy_parent_req_ids"):
            references.update(
                value.strip()
                for value in re.split(r"[;,]", str(row.get(field) or ""))
                if value.strip()
            )
        matches = (references - {""}) & source_scope
        if matches:
            source_covered.update(matches)
            if target_id:
                target_covered.add(target_id)
    source_statistics = {
        "covered_unique_source_req_ids": sorted(source_covered),
        "total_unique_source_req_ids": sorted(source_scope),
        "covered": len(source_covered),
        "total": len(source_scope),
        "percentage": len(source_covered) / len(source_scope) * 100.0 if source_scope else 0.0,
    }
    target_statistics = {
        "covered_unique_target_req_ids": sorted(target_covered),
        "total_unique_target_req_ids": sorted(target_scope),
        "covered": len(target_covered),
        "total": len(target_scope),
        "percentage": len(target_covered) / len(target_scope) * 100.0 if target_scope else 0.0,
    }
    return source_statistics, target_statistics


def _primary_to_supplementary_coverage(
    primary_node_id: str,
    supplementary_node_id: str,
    primary_source_name: str,
    relationship_edges: list[dict[str, object]],
) -> dict[str, object] | None:
    for edge in relationship_edges:
        if edge["source"] == primary_node_id and edge["target"] == supplementary_node_id:
            return {"upstream": primary_source_name, **edge["target_coverage"]}
    return None


def approved_generated_document_dependency_graph(repo_root: Path) -> dict[str, object]:
    """Return only generated-document Covers dependencies for the RM view.

    Architectural structure is intentionally excluded here.  SysML parsers own
    architecture edges; this contract owns the document dependency view.  Every
    edge coverage value is unique approved upstream requirement IDs covered by
    the derived document divided by all unique requirement IDs in that upstream.
    """
    matrix_paths = {
        "SRS": repo_root / TRACE_ARTIFACTS["SRS"],
        "ARS": repo_root / TRACE_ARTIFACTS["ARS"],
        "DRS": repo_root / TRACE_ARTIFACTS["DRS"],
        "Digital IPOS": repo_root / TRACE_ARTIFACTS["Digital IPOS"],
        "Analog IPOS": repo_root / TRACE_ARTIFACTS["Analog IPOS"],
    }

    def rows_for(stage: str) -> list[dict[str, str]]:
        return _read_csv(matrix_paths[stage])[1] if matrix_paths[stage].exists() else []

    def coverage(rows: list[dict[str, str]]) -> tuple[int, int]:
        ids = {
            str(row.get("source_req_id") or row.get("requirement_id") or "").strip()
            for row in rows
        }
        ids.discard("")
        ledger_ids = {
            str(row.get("req_id") or row.get("source_req_id") or "").strip()
            for row in _read_csv(repo_root / "artifacts/traceability_reports/requirement_allocation_ledger.csv")[1]
        }
        ledger_ids.discard("")
        return len(ids & ledger_ids), len(ledger_ids)

    nodes: list[dict[str, object]] = []
    edges: list[dict[str, object]] = []
    target_rows_by_node: dict[str, list[dict[str, str]]] = {}

    def add_node(
        node_id: str,
        label: str,
        kind: str,
        rows: list[dict[str, str]],
        upstream_blocks: list[str] | None = None,
        upstream_coverage: list[str] | None = None,
        document_qualification: str = "",
    ) -> None:
        covered, total = coverage(rows)
        nodes.append({
            "id": node_id,
            "label": label,
            "kind": kind,
            "document_qualification": document_qualification,
            "covered": covered,
            "total": total,
            "coverage_metric": "source_ledger_coverage",
            "coverage_label": "Source-ledger coverage",
            "upstream_blocks": list(upstream_blocks or []),
            "upstream_coverage": list(upstream_coverage or []),
        })

    stage_rows = {stage: rows_for(stage) for stage in matrix_paths}
    approved_contract = resolve_downstream_contract(repo_root)
    primary_source_name = approved_primary_source_name(repo_root)
    ledger_ids = {
        str(row.get("req_id") or row.get("source_req_id") or "").strip()
        for row in _read_csv(repo_root / "artifacts/traceability_reports/requirement_allocation_ledger.csv")[1]
    }
    ledger_ids.discard("")
    source_doc_ids = {primary_source_name: ledger_ids}
    supplementary_by_id: dict[str, str] = {}
    approved_supplementary_rows_by_name: dict[str, list[dict[str, str]]] = {}
    mapping_path = repo_root / "artifacts/stage1_specs/architecture_mapping_preview.csv"
    if mapping_path.exists():
        _fields, mapping_rows = _read_csv(mapping_path)
        primary_name = approved_primary_source_name(repo_root)
        for mapping_row in mapping_rows:
            requirement_id = str(
                mapping_row.get("requirement_id") or mapping_row.get("canonical_requirement_id") or ""
            ).strip()
            source_name = Path(str(mapping_row.get("supplementary_source_spec") or "").replace("\\", "/")).name
            if (
                requirement_id in approved_contract.expected
                and source_name
                and source_name.casefold() != primary_name
                and str(mapping_row.get("review_decision") or "").strip().casefold() == "approved"
            ):
                supplementary_by_id[requirement_id] = source_name
                approved_supplementary_rows_by_name.setdefault(source_name, []).append(mapping_row)

    generated_doc_ids = {
        "SRS": {str(row.get("srs_req_id") or "").strip() for row in stage_rows["SRS"] if row.get("srs_req_id")},
        "ARS": {str(row.get("ars_req_id") or "").strip() for row in stage_rows["ARS"] if row.get("ars_req_id")},
        "DRS": {str(row.get("drs_req_id") or "").strip() for row in stage_rows["DRS"] if row.get("drs_req_id")},
    }
    generated_doc_refs: dict[str, dict[str, str]] = {}
    for document_name, stage in (("SRS", "SRS"), ("ARS", "ARS"), ("DRS", "DRS")):
        generated_doc_refs[document_name] = {}
        for row in stage_rows[stage]:
            authored_id = str(
                row.get(f"{stage.lower()}_req_id") or row.get("requirement_id") or ""
            ).strip()
            source_id = str(row.get("source_req_id") or "").strip()
            if authored_id:
                generated_doc_refs[document_name][authored_id] = authored_id
            if source_id and authored_id:
                generated_doc_refs[document_name][source_id] = authored_id
    generated_document_covers: dict[str, list[str]] = {}
    for stage, document_name in (("Digital IPOS", "DRS"), ("Analog IPOS", "ARS")):
        document_path = repo_root / (
            "artifacts/stage6_digital_ipos/ipos_requirements_specification.md"
            if stage == "Digital IPOS"
            else "artifacts/stage7_analog_ipos/ipos_requirements_specification.md"
        )
        if document_path.exists():
            generated_document_covers[stage] = re.findall(
                r"^\s*Covers:\s*(\S+)\s*$",
                document_path.read_text(encoding="utf-8", errors="replace"),
                flags=re.MULTILINE,
            )
    supplementary_doc_ids: dict[str, set[str]] = {}
    if mapping_path.exists():
        for mapping_row in mapping_rows:
            requirement_id = str(
                mapping_row.get("requirement_id") or mapping_row.get("canonical_requirement_id") or ""
            ).strip()
            source_name = supplementary_by_id.get(requirement_id)
            if source_name and requirement_id:
                supplementary_doc_ids.setdefault(source_name, set()).add(requirement_id)

    def dependency_coverage(
        upstream_name: str,
        derived_rows: list[dict[str, str]],
        derived_upstream_ids: list[str] | None = None,
    ) -> dict[str, object]:
        upstream_ids = (
            generated_doc_ids.get(upstream_name)
            or supplementary_doc_ids.get(upstream_name, set())
            or source_doc_ids.get(upstream_name, set())
        )
        covered_ids: set[str] = set()
        references = derived_upstream_ids if derived_upstream_ids is not None else [
            str(row.get("covers_upstream_req_id") or row.get("source_req_id") or "").strip()
            for row in derived_rows
        ]
        for upstream_id in references:
            upstream_id = upstream_id.strip()
            if upstream_name in supplementary_doc_ids or upstream_name in source_doc_ids:
                if upstream_id in upstream_ids:
                    covered_ids.add(upstream_id)
                continue
            authored_upstream_id = generated_doc_refs.get(upstream_name, {}).get(upstream_id)
            if authored_upstream_id:
                covered_ids.add(authored_upstream_id)
        denominator = len(upstream_ids)
        return {
            "covered_unique_upstream_req_ids": sorted(covered_ids),
            "total_unique_upstream_req_ids": sorted(upstream_ids),
            "covered": len(covered_ids),
            "total": denominator,
            "percentage": len(covered_ids) / denominator * 100.0 if denominator else 0.0,
        }

    edge_statistics: list[dict[str, object]] = []

    def dependency_edge(
        source: str,
        target: str,
        kind: str,
        upstream_name: str,
        derived_rows: list[dict[str, str]],
        derived_upstream_ids: list[str] | None = None,
    ) -> dict[str, object]:
        statistics = dependency_coverage(upstream_name, derived_rows, derived_upstream_ids)
        edge_statistics.append({
            "upstream_node": source,
            "derived_node": target,
            "edge_type": kind,
            **statistics,
        })
        return {
            "source": source,
            "target": target,
            "kind": kind,
            "coverage": statistics,
            "statistics": edge_statistics[-1],
        }

    def upstream_coverage_details(rows: list[dict[str, str]]) -> list[str]:
        covered_ids: dict[str, set[str]] = {}
        for row in rows:
            upstream_id = str(row.get("covers_upstream_req_id") or row.get("source_req_id") or "").strip()
            if not upstream_id:
                continue
            source_name = supplementary_by_id.get(upstream_id)
            if source_name:
                covered_ids.setdefault(source_name, set()).add(upstream_id)
                continue
            for document_name, document_refs in generated_doc_refs.items():
                authored_upstream_id = document_refs.get(upstream_id)
                if authored_upstream_id:
                    covered_ids.setdefault(document_name, set()).add(authored_upstream_id)
                    break
        details: list[str] = []
        for document_name, ids in sorted(covered_ids.items(), key=lambda item: item[0].casefold()):
            denominator = len(
                generated_doc_ids.get(document_name)
                or supplementary_doc_ids.get(document_name, set())
                or source_doc_ids.get(document_name, set())
            )
            if denominator:
                details.append(f"{document_name}: {len(ids)} / {denominator} ({len(ids) / denominator * 100.0:.1f}%)")
        return details

    add_node(
        "SRS", "SRS - System Requirements Specification", "document", stage_rows["SRS"],
        document_qualification="System Requirements Specification (SRS)",
    )
    target_rows_by_node["SRS"] = stage_rows["SRS"]
    if stage_rows["ARS"]:
        add_node(
            "ARS", "ARS - Analog Requirements Specification", "document", stage_rows["ARS"], ["SRS"],
            document_qualification="Analog Requirements Specification (ARS)",
        )
        target_rows_by_node["ARS"] = stage_rows["ARS"]
    if stage_rows["DRS"]:
        add_node(
            "DRS", "DRS - Digital Requirements Specification", "document", stage_rows["DRS"], ["SRS"],
            document_qualification="Digital Requirements Specification (DRS)",
        )
        target_rows_by_node["DRS"] = stage_rows["DRS"]

    for stage, parent_id, label in (
        ("Digital IPOS", "DRS", "Digital IPOS"),
        ("Analog IPOS", "ARS", "Analog IPOS"),
    ):
        created = created_ipos_block_directories(repo_root, stage)
        if not created or not stage_rows[stage]:
            continue
        group_id = stage.replace(" ", "_")
        summary_statistics = dependency_coverage(
            parent_id,
            stage_rows[stage],
            generated_document_covers.get(stage),
        )
        edge_statistics.append({
            "upstream_node": parent_id,
            "derived_node": label,
            "edge_type": "generated_document_summary",
            "summary": True,
            **summary_statistics,
        })
        for block_name, block_path in sorted(created.items(), key=lambda item: item[0].casefold()):
            block_rows = [
                row for row in stage_rows[stage]
                if _ipos_block_slug(canonical_human_label(row.get("mapped_block") or row.get("owning_block") or ""))
                == _ipos_block_slug(block_name)
            ]
            block_id = f"{group_id}:{_ipos_block_slug(block_name)}"
            upstream_coverage = upstream_coverage_details(block_rows)
            approved_upstreams = [parent_id]
            approved_upstreams.extend(
                f"Supplementary specification: {supplementary_by_id[upstream_id]}"
                for upstream_id in sorted({
                    str(row.get("covers_upstream_req_id") or row.get("source_req_id") or "").strip()
                    for row in block_rows
                    if supplementary_by_id.get(str(row.get("covers_upstream_req_id") or row.get("source_req_id") or "").strip())
                })
            )
            add_node(
                block_id,
                f"{label}: {block_path.name}",
                "ipos_block",
                block_rows,
                list(dict.fromkeys(approved_upstreams)),
                upstream_coverage,
                document_qualification=f"{label} block",
            )
            target_rows_by_node[block_id] = block_rows
            edges.append(dependency_edge(parent_id, block_id, "generated_document_covers", parent_id, block_rows))

    node_ids = {str(node["id"]) for node in nodes}
    created_by_stage = {
        stage: created_ipos_block_directories(repo_root, stage)
        for stage in ("Digital IPOS", "Analog IPOS")
    }

    def direct_target(stage: str, row: dict[str, str]) -> str | None:
        if stage == "DRS":
            return "DRS" if "DRS" in node_ids else None
        if stage not in created_by_stage:
            return None
        block = canonical_human_label(row.get("mapped_block") or row.get("owning_block") or "")
        for block_name in created_by_stage[stage]:
            if _ipos_block_slug(block_name) == _ipos_block_slug(block):
                return f"{stage.replace(' ', '_')}:{_ipos_block_slug(block_name)}"
        return None

    direct_dependency_rows: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for stage in ("DRS", "Digital IPOS", "Analog IPOS"):
        for row in stage_rows[stage]:
            upstream_id = str(row.get("covers_upstream_req_id") or row.get("source_req_id") or "").strip()
            supplementary_name = supplementary_by_id.get(upstream_id)
            if not supplementary_name:
                continue
            authored_id = str(row.get("source_req_id") or row.get("requirement_id") or "").strip()
            allocation = approved_contract.expected.get(authored_id)
            if not allocation or str(row.get("snapshot_id") or "").strip() != approved_contract.snapshot_id:
                continue
            if not row.get("covers_upstream_req_id") and str(allocation.get("lineage_mode") or "") != "direct_supplementary_to_ipos":
                continue
            target_id = direct_target(stage, row)
            if not target_id:
                continue
            source_id = f"supplementary:{supplementary_name.casefold()}"
            if source_id not in node_ids:
                add_node(
                    source_id,
                    f"Supplementary specification: {supplementary_name}",
                    "supplementary_spec",
                    [],
                    document_qualification="Supplementary source specification",
                )
                node_ids.add(source_id)
            direct_dependency_rows.setdefault((source_id, target_id, supplementary_name), []).append(row)

    for (source_id, target_id, supplementary_name), derived_rows in direct_dependency_rows.items():
        edges.append(dependency_edge(source_id, target_id, "approved_supplementary_covers", supplementary_name, derived_rows))

    if "ARS" in {node["id"] for node in nodes} and stage_rows["SRS"]:
        edges.append(dependency_edge("SRS", "ARS", "generated_document_covers", "SRS", stage_rows["ARS"]))
    if "DRS" in {node["id"] for node in nodes} and stage_rows["SRS"]:
        edges.append(dependency_edge("SRS", "DRS", "generated_document_covers", "SRS", stage_rows["DRS"]))
    if "DRS" in {node["id"] for node in nodes} and stage_rows["DRS"]:
        edges.append(
            dependency_edge(
                f"source:{primary_source_name.casefold()}",
                "DRS",
                "approved_source_covers",
                primary_source_name,
                stage_rows["DRS"],
                [str(row.get("source_req_id") or "").strip() for row in stage_rows["DRS"]],
            )
        )

    primary_node_id = f"source:{primary_source_name.casefold()}"
    if ledger_ids:
        add_node(
            primary_node_id,
            f"Primary source specification: {primary_source_name}",
            "source_spec",
            [],
            document_qualification="Primary source specification",
        )

    source_ids_by_node = {
        primary_node_id: ledger_ids,
        **{
            f"supplementary:{name.casefold()}": ids
            for name, ids in supplementary_doc_ids.items()
        },
    }
    for source_name, source_ids in supplementary_doc_ids.items():
        source_node_id = f"supplementary:{source_name.casefold()}"
        if source_ids and source_node_id not in node_ids:
            add_node(
                source_node_id,
                f"Supplementary specification: {source_name}",
                "supplementary_spec",
                [],
                document_qualification="Supplementary source specification",
            )
            node_ids.add(source_node_id)

    source_spec_edges: list[dict[str, object]] = []
    source_spec_relationship_edges: list[dict[str, object]] = []
    source_node_metrics: dict[str, dict[str, object]] = {}
    source_specs = {
        primary_node_id: (primary_source_name, ledger_ids),
        **{
            f"supplementary:{name.casefold()}": (name, ids)
            for name, ids in supplementary_doc_ids.items()
        },
    }

    for target_node_id, (target_name, _target_ids) in source_specs.items():
        if target_node_id == primary_node_id:
            continue
        target_rows = approved_supplementary_rows_by_name.get(target_name, [])
        for source_node_id, (source_name, source_ids) in source_specs.items():
            if source_node_id == target_node_id or not source_ids:
                continue
            source_stat, target_stat = _source_spec_target_metrics(source_ids, target_rows)
            if not source_stat["covered"] or not target_stat["covered"]:
                continue
            source_spec_relationship_edges.append({
                "source": source_node_id,
                "target": target_node_id,
                "kind": "approved_source_spec_provenance",
                "source_specification": source_name,
                "target_specification": target_name,
                "source_coverage": source_stat,
                "target_coverage": target_stat,
            })
    for source_node_id, source_ids in source_ids_by_node.items():
        if not source_ids:
            continue
        aggregate_source_ids: set[str] = set()
        downstream_coverage: list[dict[str, object]] = []
        for target_node_id, target_rows in target_rows_by_node.items():
            source_stat, target_stat = _source_spec_target_metrics(source_ids, target_rows)
            matched_source_ids = set(source_stat["covered_unique_source_req_ids"])
            if not matched_source_ids or not target_stat["covered"]:
                continue
            target_node = next((node for node in nodes if node.get("id") == target_node_id), {})
            source_spec_edges.append({
                "source": source_node_id,
                "target": target_node_id,
                "kind": "source_spec_coverage",
                "source_specification": next((
                    name for name in (primary_source_name, *supplementary_doc_ids)
                    if source_node_id == f"source:{name.casefold()}" or source_node_id == f"supplementary:{name.casefold()}"
                ), ""),
                "target_specification": str(target_node.get("label") or target_node_id),
                "source_coverage": source_stat,
                "target_coverage": target_stat,
            })
            aggregate_source_ids.update(matched_source_ids)
            downstream_coverage.append({
                "target": target_node_id,
                "target_label": str(target_node.get("label") or target_node_id),
                **source_stat,
                "target_covered": target_stat["covered"],
                "target_total": target_stat["total"],
                "target_percentage": target_stat["percentage"],
            })
        source_node_metrics[source_node_id] = {
            "covered": len(aggregate_source_ids),
            "total": len(source_ids),
            "percentage": len(aggregate_source_ids) / len(source_ids) * 100.0,
            "downstream_coverage": downstream_coverage,
        }

    node_by_id = {str(node.get("id") or ""): node for node in nodes}
    metric_edges = [*edges, *(
        {
            "source": edge["source"],
            "target": edge["target"],
            "kind": "approved_source_covers",
            "coverage": edge["source_coverage"],
        }
        for edge in source_spec_edges
    )]
    for node in nodes:
        if node.get("kind") not in {"document", "ipos_block"}:
            continue
        target_id = str(node.get("id") or "")
        upstream_labels, upstream_statistics, upstream_metrics = _approved_upstream_coverage(target_id, node_by_id, metric_edges)
        node["upstream_blocks"] = upstream_labels
        node["upstream_coverage"] = upstream_statistics
        node["upstream_coverage_metrics"] = upstream_metrics

    for node in nodes:
        node_id = str(node.get("id") or "")
        if node.get("kind") not in {"source_spec", "supplementary_spec"}:
            continue
        node.update(source_node_metrics.get(node_id, {"covered": 0, "total": len(source_ids_by_node.get(node_id, set())), "percentage": 0.0, "downstream_coverage": []}))
        node["coverage_metric"] = "source_spec_coverage"
        node["coverage_label"] = "Source-spec coverage"
        if node.get("kind") == "supplementary_spec":
            coverage = _primary_to_supplementary_coverage(
                primary_node_id, node_id, primary_source_name, source_spec_relationship_edges
            )
            if coverage:
                node["upstream_coverage_metrics"] = [coverage]
                node["upstream_coverage"] = [
                    f"Primary coverage ({primary_source_name}): {coverage['covered']} / {coverage['total']} ({coverage['percentage']:.1f}%)"
                ]

    edges = [
        edge for edge in edges
        if int(((edge.get("coverage") or {}).get("covered")) or 0) > 0
        and int(((edge.get("coverage") or {}).get("total")) or 0) > 0
    ]
    edge_statistics = [
        statistic for statistic in edge_statistics
        if int(statistic.get("covered") or 0) > 0
        and int(statistic.get("total") or 0) > 0
    ]

    return {
        "nodes": nodes,
        "edges": edges,
        "edge_statistics": edge_statistics,
        "source_spec_edges": source_spec_edges,
        "source_spec_relationship_edges": source_spec_relationship_edges,
    }


def _check_ipos_descriptive_policy(
    repo_root: Path,
    contract: DownstreamContract,
    ipos_kind: str | None = None,
    ipos_block: str | None = None,
) -> list[str]:
    """Apply the shared descriptive policy as part of central coherence validation."""
    findings: list[str] = []
    _inventory_fields, inventory_rows = _read_csv(repo_root / "artifacts/stage2_mirco_arc/block_inventory.csv")
    inventory_by_block = {
        canonical_human_label(row.get("Block")): row
        for row in inventory_rows
        if row.get("Block", "").strip()
    }
    candidate_rows = approved_snapshot_candidate_rows(contract.requirement_input, contract)
    for stage, kind in (("Digital IPOS", "digital"), ("Analog IPOS", "analog")):
        if ipos_kind and kind != ipos_kind:
            continue
        matrix_path = TRACE_ARTIFACTS[stage]
        _fields, rows = _read_csv(repo_root / matrix_path)
        topic_specs = IPOS_LOCAL_DIGITAL_TOPIC_SPECS if kind == "digital" else IPOS_LOCAL_ANALOG_TOPIC_SPECS
        expected_blocks = {
            str(row.get("mapped_block") or row.get("owning_block") or "").strip()
            for row in rows
            if row.get("mapped_block") or row.get("owning_block")
        }
        for block_dir in created_ipos_block_directories(repo_root, stage).values():
            if ipos_block and _ipos_block_slug(ipos_block) != block_dir.name:
                continue
            block_name = next(
                (name for name in expected_blocks if _ipos_block_slug(name) == block_dir.name),
                block_dir.name,
            )
            markdown_path = next(block_dir.glob("*.md"), None)
            audit_path = block_dir / "descriptive_summary_audit.csv"
            if markdown_path is None:
                findings.append(f"{stage.upper().replace(' ', '_')}_DESCRIPTIVE_MARKDOWN_MISSING: {block_dir.name}")
                continue
            block_rows = [
                row for row in rows
                if _ipos_block_slug(canonical_human_label(row.get("mapped_block") or row.get("owning_block") or ""))
                == block_dir.name
            ]
            functional_input = build_ipos_functional_input(
                block_name,
                inventory_by_block.get(canonical_human_label(block_name), {}),
                block_rows,
                domain=kind,
                materialized=True,
                provenance=("approved snapshot", "artifacts/stage2_mirco_arc/block_inventory.csv"),
                candidate_requirement_rows=candidate_rows,
            )
            findings.extend(
                _check_prefix(
                    validate_ipos_descriptive_output(
                        markdown_path,
                        audit_path,
                        block_name,
                        [row.get("requirement_statement", "") for row in block_rows],
                        [row.get("source_req_id", "") for row in block_rows],
                        topic_specs,
                        functional_input,
                    ),
                    f"{stage}:{block_dir.name}: ",
                )
            )
            docx_path = next(block_dir.glob("*.docx"), None)
            if docx_path is None:
                findings.append(f"{stage}: {block_dir.name}: final DOCX is missing")
            else:
                findings.extend(_check_prefix(
                    validate_materialization_chain(
                        block_dir / "materialization_audit.json",
                        "IPOS",
                        build_ipos_normalized_records(functional_input),
                        markdown_path,
                        docx_path,
                    ),
                    f"{stage}:{block_dir.name}: ",
                ))
    return findings


def _check_ipos_cross_document_description_reuse(repo_root: Path) -> list[str]:
    """Reject repeated IPOS scope prose unless audit evidence is independently local."""
    findings: list[str] = []
    candidates: list[tuple[str, str, set[str]]] = []
    for stage in ("Digital IPOS", "Analog IPOS"):
        root = repo_root / ("artifacts/stage6_digital_ipos/blocks" if stage == "Digital IPOS" else "artifacts/stage7_analog_ipos/blocks")
        for block_dir in created_ipos_block_directories(repo_root, stage).values():
            markdown = next(block_dir.glob("*.md"), None)
            audit = block_dir / "descriptive_summary_audit.csv"
            if markdown is None or not audit.exists():
                continue
            text = markdown.read_text(encoding="utf-8", errors="replace")
            match = re.search(
                r"^###\s+(?:\*\*)?1\.2 Supported functions and scope(?:\*\*)?.*?(?=^###\s+|^##\s+|\Z)",
                text, flags=re.MULTILINE | re.DOTALL,
            )
            if not match:
                continue
            scope = re.sub(r"[^a-z0-9 ]+", " ", match.group(0).casefold())
            scope = re.sub(r"\b(?:the|local|scope|covers|approved|function|accepting|and|producing)\b", " ", scope)
            scope = re.sub(r"\s+", " ", scope).strip()
            with audit.open("r", encoding="utf-8", newline="") as handle:
                audit_rows = list(csv.DictReader(handle))
            evidence = {
                item.strip() for row in audit_rows if row.get("decision") == "selected"
                for item in (row.get("supporting_requirement_evidence_ids") or "").split(";") if item.strip()
            }
            candidates.append((f"{stage}:{block_dir.name}", scope, evidence))
    for index, (left_name, left_scope, left_evidence) in enumerate(candidates):
        for right_name, right_scope, right_evidence in candidates[index + 1:]:
            if left_scope and left_scope == right_scope and not (left_evidence and right_evidence and left_evidence.isdisjoint(right_evidence)):
                findings.append(
                    f"cross_block_text_reuse_without_distinct_evidence: {left_name} and {right_name}"
                )
    return findings


def _structural_function_key(value: object) -> str:
    """Normalize formatting variants while preserving literal source display text."""
    return re.sub(r"[^a-z0-9]+", "", str(value or "").casefold())


def _authoritative_ipos_structural_functions(
    contract: DownstreamContract,
) -> dict[tuple[str, str], dict[str, dict[str, object]]]:
    """Discover required structural functions only from approved allocated requirements."""
    expected_by_canonical_id = {
        str(metadata.get("canonical_id") or "").strip(): metadata
        for metadata in contract.expected.values()
    }
    discovered: dict[tuple[str, str], dict[str, dict[str, object]]] = {}
    for requirement in contract.requirement_input.rows:
        canonical_id = str(requirement.get("canonical_id") or "").strip()
        allocation = expected_by_canonical_id.get(canonical_id, {})
        target = str(allocation.get("owning_target") or "").strip()
        block = canonical_human_label(str(allocation.get("approved_block") or "").strip())
        if target not in {"Digital IPOS", "Analog IPOS"} or not block:
            continue
        statement = str(requirement.get("requirement_statement") or requirement.get("statement") or "").strip()
        entity = extract_ipos_structural_function_name(statement)
        entity_key = _structural_function_key(entity)
        if not entity_key:
            continue
        item = discovered.setdefault((target, _ipos_block_slug(block)), {}).setdefault(entity_key, {
            "display_name": entity,
            "source_req_ids": set(),
        })
        source_id = _source_id(requirement)
        if source_id:
            item["source_req_ids"].add(source_id)
    return discovered


def _check_approved_function_coverage(
    repo_root: Path,
    contract: DownstreamContract,
) -> tuple[list[str], dict[str, Any]]:
    """Require approved structural functions to be materialized in their generated IPOS scope."""
    findings: list[str] = []
    summary: dict[str, Any] = {"expected": 0, "present": 0, "missing": []}
    expected = _authoritative_ipos_structural_functions(contract)
    for stage, kind in (("Digital IPOS", "digital"), ("Analog IPOS", "analog")):
        output_root = repo_root / (
            "artifacts/stage6_digital_ipos/blocks" if kind == "digital" else "artifacts/stage7_analog_ipos/blocks"
        )
        for (_target, slug), functions in expected.items():
            if _target != stage:
                continue
            block_dir = output_root / slug
            markdown_path = next(block_dir.glob("*.md"), None)
            audit_path = block_dir / "descriptive_summary_audit.csv"
            markdown = markdown_path.read_text(encoding="utf-8", errors="replace") if markdown_path else ""
            audit_rows = _read_csv(audit_path)[1] if audit_path.exists() else []
            rendered_keys = {
                _structural_function_key(extract_ipos_structural_function_name(row.get("candidate_evidence_statement") or ""))
                for row in audit_rows
                if row.get("decision") == "accepted_candidate"
            }
            rendered_keys.discard("")
            normalized_markdown = _structural_function_key(markdown)
            for entity_key, item in functions.items():
                summary["expected"] += 1
                present = entity_key in rendered_keys or entity_key in normalized_markdown
                if present:
                    summary["present"] += 1
                    continue
                source_ids = "; ".join(sorted(item["source_req_ids"]))
                finding = (
                    f"APPROVED_FUNCTION_MISSING_FROM_GENERATED_SPEC: {stage}: {slug}: "
                    f"{item['display_name']}: {source_ids}"
                )
                findings.append(finding)
                summary["missing"].append(finding)
    return findings, summary


def _check_prefix(findings: list[str], prefix: str) -> list[str]:
    return [prefix + finding for finding in findings]


def _ipos_source_port_rows(path: Path) -> set[tuple[str, str]]:
    """Read rendered Source I/O port names and directions from Markdown or DOCX."""
    if path.suffix.casefold() == ".md":
        text = path.read_text(encoding="utf-8", errors="replace")
        return {
            (match.group(1).strip(), match.group(2).casefold())
            for match in re.finditer(
                r"^\|\s*([^|]+?)\s*\|\s*(input|output|inout|bidirectional)\s*\|",
                text,
                flags=re.IGNORECASE | re.MULTILINE,
            )
        }
    if path.suffix.casefold() != ".docx" or not path.exists():
        return set()
    try:
        with zipfile.ZipFile(path) as archive:
            root = ElementTree.fromstring(archive.read("word/document.xml"))
    except (KeyError, OSError, ElementTree.ParseError):
        return set()
    rows: list[list[str]] = []
    for table_row in root.iter():
        if not table_row.tag.endswith("}tr"):
            continue
        cells = []
        for cell in table_row.iter():
            if not cell.tag.endswith("}tc"):
                continue
            cells.append(" ".join(node.text or "" for node in cell.iter() if node.tag.endswith("}t")).strip())
        if cells:
            rows.append(cells)
    header_index = next(
        (
            index
            for index, row in enumerate(rows)
            if len(row) >= 2 and row[0].casefold() == "port name" and row[1].casefold() == "direction"
        ),
        None,
    )
    if header_index is None:
        return set()
    return {
        (row[0].strip(), row[1].casefold())
        for row in rows[header_index + 1:]
        if len(row) >= 2 and row[0].strip() and row[1].casefold() in {"input", "output", "inout", "bidirectional"}
    }


def _check_ipos_source_port_coverage(repo_root: Path) -> tuple[list[str], dict[str, Any]]:
    """Require approved source ports to survive into every generated IPOS block document."""
    catalog = _read_trace_rows(repo_root, "artifacts/stage2_mirco_arc/source_port_catalog.csv")
    expected_by_slug: dict[str, tuple[str, set[tuple[str, str]]]] = {}
    for row in catalog:
        if str(row.get("Ownership status") or "").casefold() != "approved":
            continue
        owner = canonical_human_label(row.get("Owner") or "")
        if not owner or owner in {"STBIOSystem", "Digital Subsystem"}:
            continue
        slug = _ipos_block_slug(owner)
        expected_by_slug.setdefault(slug, (owner, set()))[1].add(
            (str(row.get("Port name") or "").strip(), str(row.get("Direction") or "").casefold())
        )

    findings: list[str] = []
    summary: dict[str, Any] = {"blocks": {}, "expected_rows": 0, "checked_rows": 0}
    for stage in ("Digital IPOS", "Analog IPOS"):
        for slug, block_dir in created_ipos_block_directories(repo_root, stage).items():
            owner, expected = expected_by_slug.get(slug, (slug, set()))
            if not expected:
                continue
            summary["expected_rows"] += len(expected)
            block_summary = summary["blocks"].setdefault(f"{stage}:{owner}", {"expected": len(expected)})
            for suffix in (".md", ".docx"):
                candidates = [candidate for candidate in block_dir.glob(f"*{suffix}") if candidate.is_file()]
                if not candidates:
                    findings.append(f"IPOS_SOURCE_PORT_ARTIFACT_MISSING: {stage}: {owner}: {suffix}")
                    continue
                path = candidates[0]
                actual = _ipos_source_port_rows(path)
                summary["checked_rows"] += len(actual & expected)
                block_summary[suffix[1:] + "_rows"] = len(actual)
                for port_name, direction in sorted(expected - actual):
                    findings.append(f"IPOS_SOURCE_PORT_MISSING: {stage}: {owner}: {port_name}: {direction}: {path.name}")
                for port_name, direction in sorted(actual - expected):
                    findings.append(f"IPOS_SOURCE_PORT_UNAPPROVED: {stage}: {owner}: {port_name}: {direction}: {path.name}")
    return findings, summary


def _check_ipos_authored_requirement_format(
    repo_root: Path,
    stage: str,
    rows: list[dict[str, str]],
) -> list[str]:
    """Enforce the authoritative IPOS authored-block format in trace and Markdown output."""
    findings: list[str] = []
    kind = "digital" if stage == "Digital IPOS" else "analog"
    output_root = repo_root / ("artifacts/stage6_digital_ipos" if kind == "digital" else "artifacts/stage7_analog_ipos")
    rows_by_block: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        block_name = canonical_human_label(row.get("mapped_block") or "")
        rows_by_block.setdefault(block_name, []).append(row)

    expected_block_dirs = {_ipos_block_slug(block_name) for block_name in rows_by_block if block_name}
    block_root = output_root / "blocks"
    actual_block_dirs = set(created_ipos_block_directories(repo_root, stage))
    empty_block_dirs = {
        path.name for path in block_root.iterdir() if path.is_dir()
    } - actual_block_dirs if block_root.exists() else set()
    for block_dir in sorted(empty_block_dirs):
        findings.append(f"{stage}_IPOS_EMPTY_BLOCK_DOCUMENT: {block_dir}")
    for block_dir in sorted(actual_block_dirs - expected_block_dirs):
        findings.append(f"{stage}_IPOS_EMPTY_BLOCK_DOCUMENT: {block_dir}")

    for block_name, block_rows in rows_by_block.items():
        if not block_name:
            findings.append(f"{stage}_IPOS_BLOCK_NAME_MISSING")
            continue
        expected_by_id = {
            ipos_authored_requirement_id(block_name, sequence): row
            for sequence, row in enumerate(block_rows, 1)
        }
        actual_ids = [str(row.get("ipos_req_id") or "").strip() for row in block_rows]
        if actual_ids != list(expected_by_id):
            findings.append(f"{stage}_IPOS_ID_FORMAT_OR_SEQUENCE_INVALID: {block_name}")

        markdown_path = output_root / "blocks" / _ipos_block_slug(block_name) / f"{kind}_ipos_{_ipos_block_slug(block_name)}.md"
        if not markdown_path.exists():
            findings.append(f"{stage}_IPOS_MARKDOWN_MISSING: {markdown_path.relative_to(repo_root).as_posix()}")
            continue
        text = markdown_path.read_text(encoding="utf-8", errors="replace")
        section_match = re.search(r"^##\s+(?:\*\*)?3\. Block requirements(?:\*\*)?.*$", text, flags=re.M)
        if not section_match:
            findings.append(f"{stage}_IPOS_REQUIREMENTS_SECTION_MISSING: {block_name}")
            continue
        requirements_text = text[section_match.end():]
        blocks = re.findall(
            r"^####\s+(?:\*\*)?(IPOS-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3})(?:\*\*)?(?:\s+\{#[^}]+\})?\s*\n(.*?)(?=^####\s+|\Z)",
            requirements_text,
            flags=re.M | re.S,
        )
        rendered_by_id = {requirement_id: body.strip() for requirement_id, body in blocks}
        if len(rendered_by_id) != len(blocks) or set(rendered_by_id) != set(expected_by_id):
            findings.append(f"{stage}_IPOS_RENDERED_ID_SET_INVALID: {block_name}")
            continue
        for requirement_id, row in expected_by_id.items():
            statement = str(row.get("requirement_statement") or "").strip()
            covers = str(row.get("covers_upstream_req_id") or "").strip()
            expected_body = f"{statement}\n\nCovers: {covers}\n\n[End]"
            if rendered_by_id[requirement_id] != expected_body:
                findings.append(f"{stage}_IPOS_AUTHORED_BLOCK_FORMAT_INVALID: {requirement_id}")
    return findings


def _read_trace_rows(repo_root: Path, relative: str) -> list[dict[str, str]]:
    _fields, rows = _read_csv(repo_root / relative)
    return rows


def _extract_srs_source_ids(text: str) -> set[str]:
    """Extract explicit SRS source IDs from generated Stage 3 text."""
    ids: set[str] = set()
    for match in re.finditer(r"^\s*Covers:\s*([^\n]+)$", text, flags=re.M | re.I):
        ids.update(re.findall(r"\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+\b", match.group(1)))
    for match in re.finditer(r"\bsource_req_id\s*[=:]\s*[\"']?([A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+)", text, flags=re.I):
        ids.add(match.group(1))
    for match in re.finditer(r"\bsourceReqIds\s*=\s*([^|*/]+)", text, flags=re.I):
        ids.update(re.findall(r"\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+\b", match.group(1)))
    return ids


def _extract_srs_requirement_ids(text: str) -> set[str]:
    """Extract authored SRS IDs so stale rendered entries cannot escape checks."""
    ids: set[str] = set()
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            ids.update(match.upper() for match in re.findall(r"\bSRS-REQ-\d{3}\b", line, flags=re.I))
            continue
        match = re.match(
            r"^\s*(?:[-*+]\s+)?(?:#{1,6}\s+)?(?:\*\*)?\[(SRS-REQ-\d{3})\]\s+Requirement:",
            line,
            flags=re.I,
        )
        if match:
            ids.add(match.group(1).upper())
    return ids


def _read_docx_text(path: Path) -> str | None:
    """Read visible text from a DOCX package for central artifact checks."""
    try:
        with zipfile.ZipFile(path) as archive:
            root = ElementTree.fromstring(archive.read("word/document.xml"))
    except (KeyError, OSError, zipfile.BadZipFile, ElementTree.ParseError):
        return None
    lines = [
        " ".join(node.text or "" for node in paragraph.iter() if node.tag.endswith("}t"))
        for paragraph in root.iter()
        if paragraph.tag.endswith("}p")
    ]
    for table_row in root.iter():
        if not table_row.tag.endswith("}tr"):
            continue
        cells = [
            " ".join(node.text or "" for node in cell.iter() if node.tag.endswith("}t"))
            for cell in table_row.iter()
            if cell.tag.endswith("}tc")
        ]
        if cells:
            lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _check_srs_artifact_coherence(
    repo_root: Path,
    contract: DownstreamContract,
    expected: dict[str, dict[str, str]],
) -> list[str]:
    """Enforce freshness and exact partition coherence for all Stage 3 SRS outputs."""
    findings: list[str] = []
    approved_srs_ids = contract.source_ids_for_target("SRS")
    trace_path = repo_root / TRACE_ARTIFACTS["SRS"]
    trace_fields, trace_rows = _read_csv(trace_path)
    trace_ids = {_source_id(row) for row in trace_rows if _source_id(row)}
    expected_requirement_ids = {
        str(row.get("srs_req_id") or "").strip().upper()
        for row in trace_rows
        if str(row.get("srs_req_id") or "").strip()
    }
    if trace_ids != approved_srs_ids:
        findings.append(
            "SRS_PARTITION_SET_MISMATCH: "
            f"missing={len(approved_srs_ids - trace_ids)}, extra={len(trace_ids - approved_srs_ids)}"
        )

    stage3_root = repo_root / "artifacts/stage3_srs"
    artifact_ids: set[str] = set()
    artifact_requirement_ids: set[str] = set()
    snapshot_markers: set[str] = set()
    fingerprint_markers: set[str] = set()
    for path in sorted(stage3_root.iterdir()) if stage3_root.exists() else []:
        if not path.is_file() or path.suffix.casefold() not in {".md", ".csv", ".docx", ".tex", ".sysml"}:
            continue
        if path.name.startswith("~$"):
            continue
        if path.suffix.casefold() == ".docx":
            text = _read_docx_text(path)
            if text is None:
                findings.append(f"SRS_DOCX_UNREADABLE: {path.relative_to(repo_root).as_posix()}")
                continue
        else:
            text = path.read_text(encoding="utf-8", errors="ignore")
        artifact_ids.update(_extract_srs_source_ids(text))
        artifact_requirement_ids.update(_extract_srs_requirement_ids(text))
        snapshot_markers.update(re.findall(r"Snapshot ID:\s*([^\s]+)", text, flags=re.I))
        fingerprint_markers.update(re.findall(r"Downstream contract fingerprint:\s*([0-9a-f]{64})", text, flags=re.I))

    unsupported = artifact_ids - approved_srs_ids
    if unsupported:
        findings.append("SRS_STALE_UNSUPPORTED_IDS: " + ", ".join(sorted(unsupported)[:20]))
    if not approved_srs_ids and artifact_ids:
        findings.append("SRS_EMPTY_PARTITION_HAS_REQUIREMENT_CONTENT")
    if artifact_requirement_ids != expected_requirement_ids:
        findings.append(
            "SRS_RENDERED_REQUIREMENT_ID_SET_MISMATCH: "
            f"missing={len(expected_requirement_ids - artifact_requirement_ids)}, "
            f"extra={len(artifact_requirement_ids - expected_requirement_ids)}"
        )

    expected_fingerprint = downstream_contract_fingerprint(contract)
    if snapshot_markers and snapshot_markers != {contract.snapshot_id}:
        findings.append(f"SRS_STALE_SNAPSHOT_MARKERS: {sorted(snapshot_markers)}")
    if fingerprint_markers and fingerprint_markers != {expected_fingerprint}:
        findings.append("SRS_STALE_CONTRACT_FINGERPRINT")
    if not snapshot_markers or not fingerprint_markers:
        findings.append("SRS_FRESHNESS_MARKERS_MISSING")

    if not approved_srs_ids and any(trace_rows for _ in [0]):
        findings.append("SRS_EMPTY_PARTITION_TRACEABILITY_NOT_EMPTY")
    return findings


def _sysml_model_file_name(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", human_label_key(label)).strip("_") + ".sysml"


def _check_sysml_requirement_coverage(
    repo_root: Path,
    contract: DownstreamContract,
    expected: dict[str, dict[str, str]],
) -> list[str]:
    """Check emitted SysML requirement coverage against the selected contract."""
    findings: list[str] = []
    sysml_roots = [
        repo_root / "artifacts/stage2_mirco_arc/sysml",
        repo_root / "artifacts/stage3_srs",
    ]
    files = sorted({path for root in sysml_roots if root.exists() for path in root.rglob("*.sysml")})
    sysml_block_paths = {path for path in files if path.parent.name == "blocks"}
    compact = lambda value: re.sub(r"[^a-z0-9]", "", value.casefold())
    created_ipos_names = {
        compact(name)
        for stage in ("Digital IPOS", "Analog IPOS")
        for name in created_ipos_block_directories(repo_root, stage)
    }
    for path in sorted(sysml_block_paths):
        if compact(path.stem) not in created_ipos_names:
            findings.append(f"SYSML_STALE_IPOS_BLOCK_FILE: {path.relative_to(repo_root).as_posix()}")
    generated_sysml_names = {compact(path.stem) for path in sysml_block_paths}
    for ipos_name in sorted(created_ipos_names - generated_sysml_names):
        findings.append(f"SYSML_CREATED_IPOS_BLOCK_MISSING: {ipos_name}")
    expected_keys: set[tuple[str, str, str]] = set()
    owner_by_file = {
        _sysml_model_file_name(str(metadata.get("approved_block") or "")): human_label_key(str(metadata.get("approved_block") or ""))
        for metadata in expected.values()
        if str(metadata.get("owning_target") or "").strip() in {"Digital IPOS", "Analog IPOS"}
        and str(metadata.get("approved_block") or "").strip()
    }
    for source_id, metadata in expected.items():
        target = str(metadata.get("owning_target") or "").strip()
        if target not in {"SRS", "DRS", "Digital IPOS", "Analog IPOS"}:
            continue
        owner = human_label_key(str(metadata.get("approved_block") or "")) if target.endswith("IPOS") else ""
        expected_keys.add((source_id, target, owner))

    emitted: set[tuple[str, str, str]] = set()
    snapshots: set[str] = set()
    fingerprints: set[str] = set()
    for path in files:
        name = path.name
        if name == "STBIOSystem.sysml" or path.parent.name == "stage3_srs":
            target, owner = "SRS", ""
        elif name == "DigitalSubsystem.sysml":
            target, owner = "DRS", ""
        elif path.parent.name == "blocks":
            target = "Digital IPOS"
            owner = owner_by_file.get(name, "")
        else:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        snapshots.update(re.findall(r"^//\s*Snapshot ID:\s*([^\s]+)", text, flags=re.M | re.I))
        fingerprints.update(re.findall(r"^//\s*Downstream contract fingerprint:\s*([0-9a-f]{64})", text, flags=re.M | re.I))
        for source_id in re.findall(r'attribute\s+sourceReqId\s*=\s*"([A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+)"', text):
            emitted.add((source_id, target, owner))

    unsupported = emitted - expected_keys
    missing = expected_keys - emitted
    if unsupported:
        findings.append("SYSML_UNSUPPORTED_REQUIREMENT_COVERAGE: " + ", ".join(sorted(item[0] for item in unsupported)[:20]))
    if missing:
        findings.append("SYSML_MISSING_APPROVED_REQUIREMENT_COVERAGE: " + ", ".join(sorted(item[0] for item in missing)[:20]))
    expected_fingerprint = downstream_contract_fingerprint(contract)
    if snapshots != {contract.snapshot_id}:
        findings.append(f"SYSML_STALE_SNAPSHOT_MARKERS: {sorted(snapshots)}")
    if fingerprints != {expected_fingerprint}:
        findings.append("SYSML_STALE_CONTRACT_FINGERPRINT")
    return findings


def _check_sysml_artifacts(repo_root: Path, expected: dict[str, dict[str, str]]) -> tuple[list[str], dict[str, Any]]:
    """Check generated SysML against the approved downstream trace artifacts."""
    findings: list[str] = []
    summary: dict[str, Any] = {}

    targets = {
        "SRS": (repo_root / "artifacts/stage2_mirco_arc/sysml/STBIOSystem.sysml", "srs_req_id"),
        "DRS": (repo_root / "artifacts/stage2_mirco_arc/sysml/DigitalSubsystem.sysml", "drs_req_id"),
    }
    for target, (path, authored_field) in targets.items():
        rows = _read_trace_rows(
            repo_root,
            "artifacts/stage3_srs/srs_traceability_matrix.csv"
            if target == "SRS"
            else "artifacts/stage5_drs/drs_traceability_matrix.csv",
        )
        approved_ids = {
            source_id
            for source_id, allocation in expected.items()
            if str(allocation.get("owning_target") or "").strip() == target
        }
        summary[target] = {"path": path.relative_to(repo_root).as_posix(), "approved_count": len(approved_ids), "checked_count": len(rows)}
        if not path.exists():
            if approved_ids:
                findings.append(f"SYSML_{target}_MISSING: {path.relative_to(repo_root).as_posix()}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        missing_ids = []
        missing_descriptions = []
        for row in rows:
            source_id = _source_id(row)
            if source_id not in approved_ids:
                continue
            authored_id = str(row.get(authored_field) or "").strip()
            statement = str(row.get("requirement_statement") or "").strip()
            if authored_id and authored_id not in text and source_id not in text:
                missing_ids.append(source_id)
            if statement and statement not in text:
                missing_descriptions.append(source_id)
        if missing_ids:
            findings.append(f"SYSML_{target}_ID_MISSING: {', '.join(sorted(missing_ids)[:10])}")
        if missing_descriptions:
            findings.append(f"SYSML_{target}_DESCRIPTION_MISSING: {', '.join(sorted(missing_descriptions)[:10])}")

    ipos_summary = {}
    for ipos_stage, matrix_relative in (
        ("Digital IPOS", "artifacts/stage6_digital_ipos/ipos_traceability_matrix.csv"),
        ("Analog IPOS", "artifacts/stage7_analog_ipos/ipos_traceability_matrix.csv"),
    ):
        ipos_rows = _read_trace_rows(repo_root, matrix_relative)
        stage_summary = {"approved_count": len(ipos_rows), "blocks": {}}
        for row in ipos_rows:
            owner = canonical_human_label(row.get("mapped_block") or row.get("owning_block") or "")
            block_path = repo_root / "artifacts/stage2_mirco_arc/sysml/blocks" / _sysml_model_file_name(owner)
            block_summary = stage_summary["blocks"].setdefault(owner, {"path": block_path.relative_to(repo_root).as_posix(), "count": 0})
            block_summary["count"] += 1
            if not block_path.exists():
                findings.append(f"SYSML_{ipos_stage.upper().replace(' ', '_')}_BLOCK_MISSING: {owner}")
                continue
            text = block_path.read_text(encoding="utf-8", errors="replace")
            source_id = _source_id(row)
            statement = str(row.get("requirement_statement") or "").strip()
            if source_id not in text and not str(row.get("ipos_req_id") or "").strip() in text:
                findings.append(f"SYSML_{ipos_stage.upper().replace(' ', '_')}_ID_MISSING: {owner}: {source_id}")
            if statement and statement not in text:
                findings.append(f"SYSML_{ipos_stage.upper().replace(' ', '_')}_DESCRIPTION_MISSING: {owner}: {source_id}")
        ipos_summary[ipos_stage] = stage_summary

    port_rows = _read_trace_rows(repo_root, "artifacts/stage2_mirco_arc/source_port_catalog.csv")
    checked_ports = 0
    created_sysml_names = {
        re.sub(r"[^a-z0-9]", "", name.casefold())
        for stage in ("Digital IPOS", "Analog IPOS")
        for name in created_ipos_block_directories(repo_root, stage)
    }
    for row in port_rows:
        if str(row.get("Ownership status") or "").strip().casefold() != "approved":
            continue
        owner = canonical_human_label(row.get("Owner") or "")
        if owner == "STBIOSystem":
            path = repo_root / "artifacts/stage2_mirco_arc/sysml/STBIOSystem.sysml"
        elif owner == "Digital Subsystem":
            path = repo_root / "artifacts/stage2_mirco_arc/sysml/DigitalSubsystem.sysml"
        else:
            if re.sub(r"[^a-z0-9]", "", owner.casefold()) not in created_sysml_names:
                continue
            path = repo_root / "artifacts/stage2_mirco_arc/sysml/blocks" / _sysml_model_file_name(owner)
        checked_ports += 1
        if not path.exists():
            findings.append(f"SYSML_PORT_OWNER_FILE_MISSING: {owner}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        port_name = str(row.get("Port name") or "").strip()
        if port_name and f'attribute sourceName = "{port_name}"' not in text:
            findings.append(f"SYSML_PORT_MISSING: {owner}: {port_name}")
    summary["approved_port_rows_checked"] = checked_ports
    return findings, summary


def validate(
    repo_root: Path,
    snapshot_id: str | None = None,
    ipos_kind: str | None = None,
    ipos_block: str | None = None,
) -> dict[str, Any]:
    if bool(ipos_kind) != bool(ipos_block):
        raise ValueError("IPOS descriptive validation scope requires both kind and block.")
    project_id = _project_id(repo_root)
    contract = resolve_downstream_contract(repo_root, snapshot_id)
    requirement_input = contract.requirement_input
    selection = contract.selection
    selected_snapshot_id = contract.snapshot_id
    expected = contract.expected
    findings = _check_snapshot_and_allocations(repo_root, selected_snapshot_id, requirement_input)
    findings.extend(_check_ledger(repo_root, selected_snapshot_id, expected))
    findings.extend(_check_srs_artifact_coherence(repo_root, contract, expected))
    findings.extend(f"DRS_CONTRACT: {finding}" for finding in validate_drs_document_contract(repo_root))
    from run_drs_gen_spec_agent import validate_drs_descriptive_artifacts
    from stage1_descriptive_evidence import extract_stage1_descriptive_evidence, validate_stage1_descriptive_records
    from workflow_routing import validate_srs_system_overview
    stage1_index = repo_root / "artifacts/stage1_requirements/ocr_extracts/index.csv"
    if stage1_index.exists():
        findings.extend(
            f"STAGE1_DESCRIPTIVE: {finding}"
            for finding in validate_stage1_descriptive_records(
                extract_stage1_descriptive_evidence(stage1_index)
            )
        )
    findings.extend(
        f"SRS_OVERVIEW: {finding}"
        for finding in validate_srs_system_overview(
            repo_root / "artifacts/stage3_srs/system_requirements_specification.md"
        )
    )
    findings.extend(f"DRS: {finding}" for finding in validate_drs_descriptive_artifacts(repo_root))
    spec_documents = [
        repo_root / f"artifacts/{stage}/{filename}"
        for stage, filename in (
            ("stage3_srs", "system_requirements_specification.md"),
            ("stage4_ars", "analog_requirements_specification.md"),
            ("stage5_drs", "digital_requirements_specification.md"),
        )
    ]
    spec_documents.extend((repo_root / "artifacts/stage6_digital_ipos/blocks").glob("*/*.md"))
    spec_documents.extend((repo_root / "artifacts/stage7_analog_ipos/blocks").glob("*/*.md"))
    for markdown_path in spec_documents:
        findings.extend(validate_document_author_fields(markdown_path))
    findings.extend(_check_sysml_requirement_coverage(repo_root, contract, expected))
    artifact_summary: dict[str, dict[str, Any]] = {}
    for stage, relative in TRACE_ARTIFACTS.items():
        path = repo_root / relative
        fields, rows = _read_csv(path)
        expected_partition_count = sum(
            1 for allocation in expected.values()
            if str(allocation.get("owning_target") or "").strip() == stage
        )
        artifact_summary[stage] = {
            "path": relative.as_posix(),
            "exists": path.exists(),
            "row_count": len(rows),
            "fields": fields,
            "approved_partition_count": expected_partition_count,
            "valid_empty": bool(path.exists() and not rows and expected_partition_count == 0),
        }
        if not path.exists():
            findings.append(f"{stage}_TRACE_MISSING: {relative.as_posix()}")
        else:
            findings.extend(_check_trace_artifact(stage, path, rows, fields, selected_snapshot_id, expected))
            if stage in {"Digital IPOS", "Analog IPOS"}:
                findings.extend(_check_ipos_authored_requirement_format(repo_root, stage, rows))
    findings.extend(_check_generator_inference(repo_root))
    findings.extend(_check_ipos_descriptive_policy(repo_root, contract, ipos_kind, ipos_block))
    findings.extend(_check_ipos_cross_document_description_reuse(repo_root))
    function_coverage_findings, function_coverage_summary = _check_approved_function_coverage(repo_root, contract)
    findings.extend(function_coverage_findings)
    source_port_findings, source_port_summary = _check_ipos_source_port_coverage(repo_root)
    findings.extend(source_port_findings)
    sysml_findings, sysml_summary = _check_sysml_artifacts(repo_root, expected)
    findings.extend(sysml_findings)
    sysml_summary["ipos_source_port_coverage"] = source_port_summary
    return {
        "validator": "validate_downstream_coherence",
        "mode": "read_only_local_deterministic",
        "project_id": project_id,
        "explicit_snapshot_id": snapshot_id,
        "selected_snapshot_id": selected_snapshot_id,
        "selection_mode": "explicit_override" if snapshot_id else selection.get("selection_mode"),
        "ipos_descriptive_validation_scope": {
            "kind": ipos_kind or "all",
            "block": ipos_block or "all",
        },
        "snapshot_selection": selection,
        "approved_requirement_count": len(requirement_input.rows),
        "approved_allocation_count": len(expected),
        "artifacts": artifact_summary,
        "approved_function_coverage": function_coverage_summary,
        "sysml": sysml_summary,
        "finding_count": len(findings),
        "findings": findings,
        "decision": "PASS" if not findings else "BLOCK_DOWNSTREAM",
        "generation_allowed": not findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only downstream snapshot-to-output coherence validator")
    parser.add_argument("--snapshot-id", help="Optional diagnostic override; normal use selects the approved workflow snapshot.")
    parser.add_argument("--ipos-kind", choices=("digital", "analog"), help="Limit IPOS descriptive checks to the selected document kind.")
    parser.add_argument("--ipos-block", help="Limit IPOS descriptive checks to one approved concrete block.")
    args = parser.parse_args()
    if bool(args.ipos_kind) != bool(args.ipos_block):
        parser.error("--ipos-kind and --ipos-block must be provided together.")
    repo_root = Path(__file__).resolve().parents[1]
    try:
        result = validate(repo_root, args.snapshot_id, args.ipos_kind, args.ipos_block)
    except Exception as exc:
        result = {
            "validator": "validate_downstream_coherence",
            "mode": "read_only_local_deterministic",
            "explicit_snapshot_id": args.snapshot_id,
            "decision": "BLOCK_DOWNSTREAM",
            "generation_allowed": False,
            "finding_count": 1,
            "findings": [f"RESOLUTION_FAILURE: {exc}"],
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
