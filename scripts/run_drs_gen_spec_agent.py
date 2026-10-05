#!/usr/bin/env python3
"""Run the DRS generation agent workflow from repository artifacts.

This script operationalizes `.github/agents/drs_gen_spec.agent.md` by:
- validating required inputs
- generating DRS markdown
- generating DRS traceability CSV
- generating Stage DRS report
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
import zipfile
from xml.etree import ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from workflow_routing import (
    apply_docx_authored_requirement_formatting,
    apply_docx_common_spec_formatting,
    GENERATED_SPEC_VERSION,
    csv_cell_text,
    normalize_authored_requirement_blocks,
    organize_descriptive_topics,
    DESCRIPTIVE_DIGITAL_TOPIC_SPECS,
    assemble_descriptive_summary,
    write_descriptive_audit,
    assess_top_digital_coverage,
    write_top_digital_coverage_audit,
    read_retained_rows,
    source_parent_title,
    runtime_user_name,
    document_author_name,
    document_version_for_snapshot,
    apply_shared_spec_markdown_formatting,
    compose_technical_block_purpose,
    project_architecture_interactions,
    project_architecture_interfaces,
    summarize_architecture_interactions,
    validate_drs_block_descriptions,
    compose_drs_interaction_summary,
    compose_drs_clock_summary,
    compose_drs_role_summary,
    drs_section_prose_findings,
)
from approved_snapshot_resolver import resolve_complete_authoritative_input
from requirement_corpus import load_sqlite_snapshot_input
from traceability_rules import is_direct_upstream_source_id
from allocation_ledger import refresh_ledger
from spec_document_contract import (
    DRS_TEMPLATE, load_drs_contract, drs_conventions_markdown,
    arrange_drs_contract_lines, validate_drs_document_contract, drs_contract_metadata,
)
from validate_downstream_coherence import (
    canonical_human_label,
    resolve_downstream_contract,
    validate as validate_downstream_coherence,
)
from low_power_descriptive import (
    assemble_low_power_descriptive,
    is_drs_top_level_record,
    power_domain_records_from_ocr,
    read_selected_low_power_audit,
    render_low_power_topics,
    write_low_power_audit,
)
from stage1_descriptive_evidence import extract_stage1_descriptive_evidence


REQUIRED_INPUTS = [
    "artifacts/stage1_requirements/requirements_rag_crosscheck.md",
    "artifacts/stage1_requirements/ocr_extracts/index.csv",
    "artifacts/stage2_mirco_arc/micro_architecture_report.md",
    "artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv",
    "artifacts/stage2_mirco_arc/unmapped_requirement_routing.csv",
    "artifacts/stage2_mirco_arc/block_inventory.csv",
    "artifacts/stage2_mirco_arc/interface_catalog.csv",
    "artifacts/stage2_mirco_arc/interaction_matrix.csv",
    "artifacts/stage2_mirco_arc/architecture_crosscheck_report.md",
    "artifacts/stage3_srs/srs_traceability_matrix.csv",
]

DOCX_REFERENCE_TEMPLATE = "templates/MPT_IPOS_template.docx"


SOURCE_INTERFACE_TABLE_TERMS = (
    "i/o list",
    "io list",
    "port list",
    "pin list",
    "clock list",
    "reset list",
    "interface list",
)
REGISTER_TABLE_RE = re.compile(
    r"\b(?:register\s*(?:name|address|map|offset|access|reset|description|value)|"
    r"register\s+table|reg(?:ister)?map)\b",
    re.IGNORECASE,
)

DIGITAL_INTERFACE_TABLE_TERMS = (
    "i2c",
    "spi",
    "ahb",
    "axi",
    "apb",
    "uart",
    "jtag",
)


POWER_FOCUS_TERMS = (
    "power",
    "supply",
    "voltage",
    "brown-out",
    "reverse-polarity",
    "polarity",
)


DIGITAL_SYSTEM_TERMS = (
    "uart",
    "host",
    "external host",
    "command",
    "firmware",
    "led",
    "button",
    "event log",
    "state machine",
    "serial",
    "protocol",
    "telemetry",
    "nvm",
    "memory",
    "register",
    "interrupt",
    "fifo",
    "clock",
    "reset",
    "mode",
)


ANALOG_FOCUS_TERMS = (
    "analog",
    "temperature",
    "sensor",
    "adc",
    "hysteresis",
    "setpoint",
    "relay",
    "ambient",
    "sampling",
    "conversion",
    "voltage",
    "calibration",
    "noise",
)


BLOCK_ANALOG_TERMS = (
    "analog",
    "sensor",
    "temperature",
    "adc",
    "conversion",
    "sampling",
    "hysteresis",
    "relay",
    "voltage",
    "power",
    "brown-out",
    "noise",
    "calibration",
)


BLOCK_DIGITAL_TERMS = (
    "control",
    "dsp",
    "uart",
    "host",
    "firmware",
    "command",
    "protocol",
    "gpio",
    "led",
    "button",
    "event",
    "schedule",
    "mode",
    "state machine",
    "telemetry",
    "nvm",
    "memory",
    "register",
    "interrupt",
    "fifo",
    "test",
    "debug",
)


DIGITAL_ARCHITECTURE_TERMS = (
    "i2c", "spi", "ahb", "axi", "apb", "uart", "jtag", "serial",
    "protocol", "bus", "processor", "cpu", "microprocessor", "core", "digital",
)

BLOCK_CLASS_ANALOG = "analog_or_mixed"
BLOCK_CLASS_POWER = "power_or_supply"
BLOCK_CLASS_DIGITAL = "digital_or_system"
FUNCTION_STOP_WORDS = {
    "a",
    "and",
    "are",
    "as",
    "at",
    "by",
    "for",
    "from",
    "in",
    "into",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}
SOURCE_REQUIREMENT_IDS: Set[str] = set()
DESCRIPTIVE_SIGNAL_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:i|o|ca|ta|u)_[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)?\b"
    r"|\bPUMP_[A-Za-z0-9_]+\b|\bH9A_MEM_OTP_+\b|\blevel_shifter_sel\b",
    re.IGNORECASE,
)


def _descriptive_text(text: str) -> str:
    """Keep architecture prose at block/resource level, not signal level."""
    cleaned = DESCRIPTIVE_SIGNAL_RE.sub("", text or "")
    cleaned = re.sub(r"\s+([,.;:)])", r"\1", cleaned)
    cleaned = re.sub(r"([(])\s+", r"\1", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    return cleaned.strip()


def _shared_resource_access_records(records: List[Dict[str, str]]) -> List[str]:
    """Select top-level source descriptions of shared-resource access behavior."""
    resource_terms = ("memory", "register", "regmap", "fifo", "bus", "interconnect")
    access_terms = ("access", "arbitrat", "shared", "common", "master", "slave", "transaction")
    selected: List[str] = []
    for record in records:
        statement = record.get("statement", "")
        searchable = statement.casefold()
        if any(term in searchable for term in resource_terms) and any(term in searchable for term in access_terms):
            cleaned = _descriptive_text(statement)
            if cleaned and cleaned not in selected:
                selected.append(cleaned)
    return selected

def _normalize_block_references(text: str) -> str:
    """Preserve source wording; ownership is resolved from runtime inventory evidence."""
    return text


@dataclass
class Requirement:
    source_req_id: str
    domain: str
    statement: str
    source: str
    requirement_type: str
    value_range_condition: str
    source_section_owner: str = ""
    derivation_kind: str = ""
    evidence_type: str = ""
    notes: str = ""


@dataclass
class BlockInfo:
    name: str
    function: str
    inputs: str
    outputs: str
    linked_requirements: str
    entity_kind: str = ""


def _resolve_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\n")


def _check_inputs(repo_root: Path) -> Tuple[List[Path], List[Path]]:
    present: List[Path] = []
    missing: List[Path] = []
    for rel in REQUIRED_INPUTS:
        p = (repo_root / rel).resolve()
        if p.exists():
            present.append(p)
        else:
            missing.append(p)
    return present, missing


def _csv_cell_text(value: object) -> str:
    """Normalize CSV cell values to text, including list-valued overflow fields."""
    return csv_cell_text(value)


def _read_non_block_context_rows(path: Path, requirement_ids: Set[str]) -> List[Dict[str, str]]:
    return read_retained_rows(path, requirement_ids)


def _resolve_source_spec_from_stage1_index(path: Path, repo_root: Path) -> str:
    if not path.exists():
        return "unknown"
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                source = _csv_cell_text(row.get("source_file")).strip()
                if source:
                    src = Path(source)
                    local_candidate = repo_root / "specs" / src.name
                    if local_candidate.exists():
                        return local_candidate.as_posix()
                    return source.replace("\\", "/")
    except Exception:
        return "unknown"
    return "unknown"


def _domain_from_row(row: Dict[str, str], req_id: str) -> str:
    category = (row.get("category") or "").strip().lower()
    if category == "analog":
        return "ANA"
    if category == "digital":
        return "DIG"
    if category == "system":
        return "SYS"

    up = req_id.upper()
    if up.startswith("REQ_ANA") or up.startswith("CONF_ANA"):
        return "ANA"
    if up.startswith("REQ_DIG") or up.startswith("CONF_DIG"):
        return "DIG"
    if up.startswith("REQ_SYS") or up.startswith("CONF_SYS"):
        return "SYS"
    return "XDN"


def _enforce_normative(statement: str) -> str:
    text = (statement or "").strip()
    if not text:
        return "The digital subsystem shall satisfy this requirement based on available source artifacts."

    low = text.lower()
    if " shall " in low or low.startswith("shall "):
        return text

    if text.endswith("."):
        text = text[:-1]
    return f"The digital subsystem shall satisfy the following behavior: {text}."


def _verification_method(req_type: str, domain: str) -> str:
    t = (req_type or "").strip().lower()
    if t in {"timing", "performance"}:
        return "analysis+test"
    if t in {"electrical"}:
        return "analysis"
    if t in {"interface", "protocol", "configuration"}:
        return "inspection+test"
    if domain == "XDN":
        return "analysis+test"
    return "test"


def _acceptance_criteria(value_range_condition: str) -> str:
    condition = (value_range_condition or "").strip()
    if condition:
        return f"Measured result satisfies: {condition}."
    return "Requirement behavior is observed in nominal and boundary test conditions."


def _excluded_source_req_ids(summary_csv: Path) -> Set[str]:
    config_path = summary_csv.parents[2] / "config" / "project_context.json"
    if not config_path.exists():
        return set()
    try:
        with config_path.open("r", encoding="utf-8") as handle:
            config = json.load(handle)
    except (OSError, ValueError):
        return set()
    values = config.get("requirement_id_rules", {}).get("excluded_source_req_ids", [])
    return {str(value).strip().upper() for value in values if str(value).strip()}


def _is_non_normative_table_row(row: Dict[str, str], statement: str) -> bool:
    raw_statement = row.get("requirement_statement", "")
    evidence = " ".join(row.get(field, "") for field in ("source", "notes", "derivation_kind", "evidence_type"))
    has_normative_marker = bool(
        re.search(r"\b(?:requirement|shall|must|required|connected|set\s+to)\b", raw_statement, re.IGNORECASE)
    )
    encoded_value_pairs = re.findall(r"\b[01]{2,}\s+\d+(?:\.\d+)?\s*[A-Za-z]+\b", raw_statement)
    if len(encoded_value_pairs) >= 2 and not has_normative_marker:
        return True
    if not re.search(
        r"table_line_info|table_context|\btable\s+\d+\s*:|operating\s+modes?\s+table|"
        r"state\s+table|configuration\s+summary|timing\s+summary",
        evidence,
        re.IGNORECASE,
    ):
        return False
    if re.search(r"recovery_mode=header_split", evidence, re.IGNORECASE) and not re.search(r"\bRequirement\s*:", raw_statement, re.IGNORECASE):
        return text


        return True
    return not has_normative_marker


def _is_introductory_source_row(row: Dict[str, str]) -> bool:
    """Exclude document-history and introductory source tables from specifications."""
    context = " ".join(
        row.get(field, "")
        for field in ("source", "notes", "derivation_kind", "evidence_type", "requirement_statement")
    )
    return bool(re.search(
        r"\b(?:revision|version)\s+history\b|\bhistory\s+table\b|\btable\s+of\s+contents\b|"
        r"\bintroduction(?:\s+table)?\b|\bdocument\s+control\b|\breference\s+documents?\b|"
        r"\babbreviations?\b|\blist\s+of\s+(?:figures|tables)\b",
        context,
        re.IGNORECASE,
    ))


def _read_requirements(summary_csv: Path, input_rows: Optional[tuple[Dict[str, str], ...]] = None) -> List[Requirement]:
    global SOURCE_REQUIREMENT_IDS
    if input_rows is None:
        with summary_csv.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = []
            for row in reader:
                cleaned: Dict[str, str] = {}
                for k, v in row.items():
                    if k is None:
                        continue
                    cleaned[k] = _csv_cell_text(v).strip()
                rows.append(cleaned)
    else:
        rows = []
        for snapshot_row in input_rows:
            row = dict(snapshot_row)
            source_req_id = (row.get("source_req_id") or row.get("id") or "").strip()
            row["id"] = row.get("id") or source_req_id
            row["source_req_id"] = source_req_id
            row["category"] = row.get("category") or row.get("approved_classification") or "System"
            row.setdefault("source", "")
            row.setdefault("requirement_type", "")
            row.setdefault("notes", "")
            rows.append(row)

    if not rows:
        raise ValueError("requirements_summary.csv is empty")

    required_cols = {"id", "requirement_statement", "source", "requirement_type"}
    missing = [c for c in required_cols if c not in set(rows[0])]
    if missing:
        raise ValueError(f"requirements_summary.csv missing required columns: {', '.join(missing)}")

    excluded_ids = _excluded_source_req_ids(summary_csv)
    SOURCE_REQUIREMENT_IDS = {
        (row.get("source_req_id") or row.get("id") or "").strip()
        for row in rows
        if (row.get("source_req_id") or row.get("id") or "").strip()
    }
    requirements: List[Requirement] = []
    for row in rows:
        req_id = (row.get("source_req_id") or row.get("id") or "").strip()
        if req_id.upper() in excluded_ids:
            continue
        statement = _enforce_normative(row.get("requirement_statement", ""))
        if _is_introductory_source_row(row) or _is_non_normative_table_row(row, statement):
            continue
        requirements.append(
            Requirement(
                source_req_id=req_id,
                domain=_domain_from_row(row, req_id),
                statement=statement,
                source=row.get("source", ""),
                requirement_type=row.get("requirement_type", ""),
                value_range_condition=row.get("value_range_condition", ""),
                source_section_owner=row.get("source_section_owner", ""),
                derivation_kind=row.get("derivation_kind", ""),
                evidence_type=row.get("evidence_type", ""),
                notes=row.get("notes", ""),
            )
        )
    return requirements


def _read_req_to_block(path: Path) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    if not path.exists():
        return mapping

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            req_id = _csv_cell_text(row.get("Requirement ID")).strip()
            blocks = _csv_cell_text(row.get("Block(s)")).strip()
            if req_id:
                mapping[req_id] = blocks or "Unassigned"
    return mapping


def _read_srs_upstream_map(path: Path) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    if not path.exists():
        return mapping
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            source_req_id = _csv_cell_text(row.get("source_req_id")).strip()
            srs_req_id = _csv_cell_text(row.get("srs_req_id")).strip()
            if source_req_id and re.fullmatch(r"SRS-REQ-\d{3}", srs_req_id):
                mapping[source_req_id] = srs_req_id
    return mapping


def _read_srs_statements(path: Path) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    if not path.exists():
        return mapping
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            source_req_id = _csv_cell_text(row.get("source_req_id")).strip()
            statement = _csv_cell_text(row.get("requirement_statement")).strip()
            if source_req_id and statement:
                mapping[source_req_id] = statement
    return mapping


def _require_srs_upstream_map(requirements: List[Requirement], srs_upstream_map: Dict[str, str]) -> None:
    return None


def _direct_upstream_id(source_req_id: str) -> bool:
    """Allow supplementary-source requirements to remain upstream of DRS."""
    return is_direct_upstream_source_id(source_req_id)


def _upstream_id(source_req_id: str, srs_upstream_map: Dict[str, str]) -> str:
    return srs_upstream_map.get(source_req_id, source_req_id)


def _read_block_inventory(path: Path) -> List[BlockInfo]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        out: List[BlockInfo] = []
        for row in reader:
            out.append(
                BlockInfo(
                    name=_csv_cell_text(row.get("Block")).strip(),
                    function=_csv_cell_text(row.get("Function")).strip(),
                    inputs=_csv_cell_text(row.get("Inputs")).strip(),
                    outputs=_csv_cell_text(row.get("Outputs")).strip(),
                    linked_requirements=_csv_cell_text(row.get("Linked requirements")).strip(),
                    entity_kind=_csv_cell_text(row.get("Entity kind")).strip(),
                )
            )
        return [b for b in out if b.name]


def _require_block_functions(block_inventory: List[BlockInfo]) -> None:
    missing = [block.name for block in block_inventory if not block.function]
    if missing:
        raise ValueError(
            "block_inventory.csv requires a non-empty Function for every block: "
            + ", ".join(missing)
        )


def _read_interface_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: List[Dict[str, str]] = []
        for row in reader:
            cleaned: Dict[str, str] = {}
            for k, v in row.items():
                if k is None:
                    continue
                cleaned[k] = _csv_cell_text(v).strip()
            rows.append(cleaned)
        return rows


def _read_interaction_rows(path: Path) -> List[Dict[str, str]]:
    return _read_interface_rows(path)


def _top_digital_coverage_records(
    interaction_rows: List[Dict[str, str]],
    interface_rows: List[Dict[str, str]],
    non_block_context_rows: List[Dict[str, str]],
    architecture_rows: Optional[List[Dict[str, str]]] = None,
) -> List[Dict[str, str]]:
    """Build only approved integration evidence for the top-digital assessor."""
    records: List[Dict[str, str]] = []
    for row in interaction_rows:
        source = row.get("From block", "").strip()
        destination = row.get("To block", "").strip()
        if not source or not destination:
            continue
        details = "; ".join(
            value for value in (
                row.get("Signal/control", "").strip(),
                row.get("Trigger", "").strip(),
                row.get("Notes", "").strip(),
            ) if value
        )
        records.append({
            "statement": f"Interaction: {source} -> {destination}" + (f" ({details})" if details else ""),
            "source": "artifacts/stage2_mirco_arc/interaction_matrix.csv",
            "scope": "integration",
        })
    for row in interface_rows:
        interface = row.get("Interface", "").strip()
        owner = row.get("Owner", "").strip()
        purpose = row.get("Purpose", "").strip()
        if not interface or not owner or not purpose:
            continue
        records.append({
            "statement": f"Approved interface {interface} owned by {owner}: {purpose}",
            "source": "artifacts/stage2_mirco_arc/interface_catalog.csv",
            "scope": "integration",
        })
    for row in non_block_context_rows:
        statement = (row.get("Non-Block Function Context") or row.get("Source Paragraph") or "").strip()
        source = (row.get("Source Paragraph") or row.get("Requirement ID") or "").strip()
        if statement:
            records.append({
                "statement": statement,
                "source": source,
                "scope": "top_digital",
            })
    records.extend(architecture_rows or [])
    return [record for record in records if is_drs_top_level_record(record)]

def _source_architecture_capability_records(summary_csv: Path) -> List[Dict[str, str]]:
    """Promote explicit Stage 1 system capabilities into top-level descriptive context."""
    overview_terms = (
        "aim of this document", "main features", "single die", "analog front end",
        "mixed-signal", "system-on-chip", "soc", "sensor interface", "power domain",
        "clock", "reset", "data path", "host interface", "embedded processor",
    )
    with summary_csv.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [
            {key: _csv_cell_text(value).strip() for key, value in row.items() if key is not None}
            for row in reader
        ]
    return [
        {
            "statement": row.get("requirement_statement", "").strip(),
            "source": row.get("source", "").strip(),
            "scope": "top_digital",
            "record_type": "architecture_capability",
            "source_req_id": row.get("id", "").strip(),
        }
        for row in rows
        if row.get("derivation_kind", "") == "architecture_capability"
        and row.get("requirement_statement", "").strip()
        and not re.search(r"\b(?:shall|must|required to)\b", row.get("requirement_statement", ""), re.I)
        and any(term in row.get("requirement_statement", "").casefold() for term in overview_terms)
        and re.search(r"\b(?:overview|introduction)\b", row.get("source", ""), re.I)
    ]


def _stage1_overview_descriptive_records(
    index_path: Path,
    digital_blocks: List[BlockInfo],
) -> Tuple[List[Dict[str, str]], Dict[str, List[Dict[str, str]]]]:
    """Adapt shared Stage 1 evidence to the DRS top-level/block scopes."""
    shared_records = extract_stage1_descriptive_evidence(
        index_path,
        block_names=[block.name for block in digital_blocks],
    )
    top_level = [
        {**record, "scope": "top_digital"}
        for record in shared_records
        if record.get("scope") == "system"
    ]
    by_block: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for record in shared_records:
        if record.get("scope") != "block_local":
            continue
        block_name = record.get("mapped_block", "")
        by_block[block_name].append({**record, "scope": "block_local_digital"})
    return top_level, dict(by_block)
    paragraphs: List[Dict[str, object]] = []
    active = False
    current: List[Tuple[int, int, str]] = []

    def flush() -> None:
        if not current:
            return
        statement = " ".join(re.sub(r"\s+", " ", text).strip() for _page, _line, text in current)
        statement = re.sub(r"\s+", " ", statement).strip()
        if statement:
            paragraphs.append({
                "statement": statement,
                "locations": [(page, line) for page, line, _text in current],
            })
        current.clear()

    for page, line_number, raw_line in source_lines:
        line = raw_line.strip()
        top_heading = re.match(r"^\s*\d+\.\s+(.+?)\s*$", line)
        if top_heading and re.search(r"\.{2,}|\s\d+\s*$", top_heading.group(1)):
            top_heading = None
        if top_heading:
            flush()
            title = top_heading.group(1)
            if re.search(r"\boverview\b", title, re.I):
                active = True
                continue
            if active:
                break
        if not active:
            continue
        if re.match(r"^\[[A-Z][A-Z0-9_-]*\]\s+(?:Definition|Assumption|Comment|Requirement)\b", line, re.I):
            flush()
            break
        if not line or re.fullmatch(r"\d{1,3}", line):
            flush()
            continue
        if re.match(r"^(?:Figure|Table)\s+\d+\b", line, re.I):
            flush()
            continue
        current.append((page, line_number, line))
    flush()

    merged: List[Dict[str, object]] = []
    for paragraph in paragraphs:
        statement = str(paragraph["statement"])
        if merged and not re.search(r"[.!?:;]\s*$", str(merged[-1]["statement"])) and statement[:1].islower():
            merged[-1]["statement"] = f"{merged[-1]['statement']} {statement}"
            merged[-1]["locations"].extend(paragraph["locations"])
        else:
            merged.append(paragraph)

    sentences: List[Dict[str, object]] = []
    for paragraph in merged:
        parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9•])", str(paragraph["statement"]))
        for part in parts:
            statement = part.strip()
            if not statement:
                continue
            if sentences and not re.search(r"[.!?]\s*$", str(sentences[-1]["statement"])) and statement[:1].islower():
                sentences[-1]["statement"] = f"{sentences[-1]['statement']} {statement}"
                sentences[-1]["locations"].extend(paragraph["locations"])
            else:
                sentences.append({"statement": statement, "locations": list(paragraph["locations"])})

    digital_terms = re.compile(
        r"\b(?:digital|processor|processing|signal processing|host|bus|fifo|sensor hub|"
        r"programmable|metadata|interconnect|memory|register|i2c|spi|ahb)\b",
        re.I,
    )
    top_level: List[Dict[str, str]] = []
    by_block: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    fifo_data_heading = re.compile(
        r"The internal and external data that can be collected in FIFO are:\s*(.+)", re.I
    )
    for paragraph in merged:
        source_evidence = str(paragraph["statement"])
        match = fifo_data_heading.search(source_evidence)
        if not match:
            continue
        bullet_text = match.group(1).split("All the data are stored inside", 1)[0]
        items = [re.sub(r"\s+", " ", item).strip(" .") for item in re.findall(r"•\s*([^•]+)", bullet_text)]
        items = [item for item in items if item]
        if len(items) < 3:
            continue
        items = [
            re.sub(r"^GSR\s*&\s*6 channels PPG$", "GSR and six PPG channels", item, flags=re.I)
            for item in items
        ]
        items = [
            re.sub(
                r"^up to 4 external sensors\s*\(expressed on 12 bytes each\)$",
                "up to four external sensors represented in 12 bytes each",
                item,
                flags=re.I,
            )
            for item in items
        ]
        first_page, first_line = paragraph["locations"][0]
        last_page, last_line = paragraph["locations"][-1]
        source = (
            f"Stage 1 OCR page {first_page}, lines {first_line}-{last_line}"
            if first_page == last_page else
            f"Stage 1 OCR page {first_page}, line {first_line}, through page {last_page}, line {last_line}"
        )
        top_level.append({
            "statement": "The FIFO data path carries " + ", ".join(items[:-1]) + f", and {items[-1]}.",
            "source": source,
            "source_evidence": source_evidence,
            "scope": "top_digital",
            "record_type": "architecture_capability",
            "evidence_kind": "architecture",
        })
    for paragraph in sentences:
        statement = str(paragraph["statement"])
        explicit_owners = []
        for block in digital_blocks:
            block_name = r"[-_\s]+".join(
                re.escape(token) for token in re.split(r"[-_\s]+", block.name) if token
            )
            subject_patterns = (
                rf"^\s*(?:the\s+)?(?:(?:advanced|digital|embedded|programmable|smart)\s+)*{block_name}\b",
                rf"^\s*(?:the\s+)?main\s+(?:purpose|benefits|function(?:s)?|role)\s+of\s+(?:the\s+)?{block_name}\b",
            )
            if any(re.search(pattern, statement, re.I) for pattern in subject_patterns):
                explicit_owners.append(block.name)
        if (
            len(statement) < 45
            or not re.search(r"[.!?]\s*$", statement)
            or re.search(r"\b(?:shall|must|required to)\b|\[(?:DDS|REQ|CONF)_", statement, re.I)
            or "•" in statement
            or re.search(r"\bsub[- ]fifo\b.*\bdepth\b|\bdepth\b.*\bsub[- ]fifo\b", statement, re.I)
            or not digital_terms.search(statement) and not explicit_owners
        ):
            continue
        locations = paragraph["locations"]
        first_page, first_line = locations[0]
        last_page, last_line = locations[-1]
        location = (
            f"Stage 1 OCR page {first_page}, lines {first_line}-{last_line}"
            if first_page == last_page else
            f"Stage 1 OCR page {first_page}, line {first_line}, through page {last_page}, line {last_line}"
        )
        record = {
            "statement": statement,
            "source": location,
            "scope": "top_digital",
            "record_type": "architecture_capability",
            "evidence_kind": "architecture",
        }
        if len(explicit_owners) == 1:
            record["scope"] = "block_local_digital"
            record["mapped_block"] = explicit_owners[0]
            by_block[explicit_owners[0]].append(record)
        else:
            top_level.append(record)
    return top_level, dict(by_block)

def _ocr_extract_lines(index_path: Path) -> List[Tuple[int, int, str]]:
    extracts_dir = index_path.parent
    if not extracts_dir.exists():
        return []

    rows: List[Tuple[int, int, str]] = []
    for path in sorted(extracts_dir.glob("*.txt")):
        page_match = re.search(r"_p(\d+)\.txt$", path.name)
        page = int(page_match.group(1)) if page_match else 0
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for line_no, line in enumerate(lines, start=1):
            rows.append((page, line_no, line.rstrip()))
    return rows


def _numbered_heading_title(line: str) -> str:
    match = re.match(r"^\s*(\d+(?:\.\d+)*)\.\s+(.+?)\s*$", line or "")
    return match.group(2).strip() if match else ""


def _source_interface_table_title(line: str) -> str:
    text = re.sub(r"\s+", " ", (line or "").strip())
    low = text.lower()
    if not any(term in low for term in SOURCE_INTERFACE_TABLE_TERMS):
        return ""
    if REGISTER_TABLE_RE.search(text):
        return ""
    if "..." in text or re.search(r"\.\s*\.\s*\.", text):
        return ""
    if re.search(r"\b(figure|memory map|memory mapping|connectivity check|revision history|abbreviation)\b", low):
        return ""
    return text.strip(" .")


def _source_table_block_name(title: str, context: str, block_inventory: List[BlockInfo]) -> str:
    ignored = {"list", "table", "port", "pin", "clock", "reset", "interface", "input", "output", "top", "controller"}

    def choose(evidence: str) -> str:
        evidence_terms = _function_terms(evidence)
        evidence_terms = {term for term in evidence_terms if term not in ignored}
        if not evidence_terms:
            return ""

        ranked: List[Tuple[int, int, str]] = []
        for block in block_inventory:
            block_terms = _function_terms(block.name)
            overlap = evidence_terms & block_terms
            if overlap:
                ranked.append((len(overlap), len(block_terms), block.name))

        if not ranked:
            return ""
        ranked.sort(key=lambda item: (-item[0], item[1], item[2]))
        return ranked[0][2]

    title_terms = {term for term in _function_terms(title) if term not in ignored}
    if not title_terms:
        return ""

    title_match = choose(title)
    if title_match:
        return title_match

    evidence_terms = _function_terms(context)
    if not evidence_terms:
        return ""

    return choose(context)


def _exclude_non_requirement_snippet(lines: List[str]) -> List[str]:
    """Keep raw source excerpts requirements-only after their first tagged non-requirement."""
    normalized = [re.sub(r"\s+", " ", line.strip()) for line in lines]
    for index, line in enumerate(normalized):
        non_requirement = re.match(
            r"^\[[A-Z][A-Z0-9_\-]*\]\s+(?:Definition|Assumption|Comment)\s*:",
            line,
            re.IGNORECASE,
        )
        if not non_requirement:
            continue
        return lines[:index]
    return lines


def _source_interface_tables_by_block(repo_root: Path, block_inventory: List[BlockInfo]) -> Dict[str, List[Tuple[str, str, str]]]:
    rows = _ocr_extract_lines((repo_root / "artifacts/stage1_requirements/ocr_extracts/index.csv").resolve())
    if not rows:
        return {}

    section_stack: List[str] = []
    table_hits: List[Tuple[int, str, str]] = []
    for idx, (_page, _line_no, line) in enumerate(rows):
        heading = _numbered_heading_title(line)
        if heading:
            section_stack.append(heading)
            section_stack = section_stack[-8:]
        title = _source_interface_table_title(line)
        if title:
            table_hits.append((idx, title, " ".join(section_stack)))

    by_block: Dict[str, List[Tuple[str, str, str]]] = defaultdict(list)
    seen: Set[Tuple[str, str]] = set()
    for idx, title, context in table_hits:
        start = idx
        while start > 0 and idx - start < 60:
            prev = rows[start - 1][2].strip()
            if start < idx and (_source_interface_table_title(prev) or re.match(r"^\s*\d+(?:\.\d+)*\.\s+", prev) or prev.lower().startswith("figure ")):
                break
            start -= 1

        end = idx + 1
        while end < len(rows) and end - idx < 180:
            current = rows[end][2].strip()
            if end > idx + 5 and (_source_interface_table_title(current) or re.match(r"^\s*\d+(?:\.\d+)*\.\s+", current) or current.lower().startswith("figure ")):
                break
            end += 1

        snippet_lines = [line for _page, _line_no, line in rows[start:end] if line.strip()]
        filtered_snippet_lines: List[str] = []
        seen_table_title = False
        for line in snippet_lines:
            text = line.strip()
            if _source_interface_table_title(text):
                seen_table_title = True
            if seen_table_title and (
                re.match(r"^\[[A-Z][A-Z0-9_\-]*\]\s+Requirement:?\s*$", text)
                or re.search(r"\bPeculiar Requirements\b", text, flags=re.I)
            ):
                break
            filtered_snippet_lines.append(line)
        snippet_lines = _exclude_non_requirement_snippet(filtered_snippet_lines)
        snippet = "\n".join(snippet_lines).strip()
        if not snippet:
            continue

        block_name = _source_table_block_name(title, context, block_inventory)
        if not block_name:
            continue

        page = rows[idx][0]
        provenance = f"source table from OCR extract page {page}"
        key = (block_name, title)
        if key in seen:
            continue
        seen.add(key)
        by_block[block_name].append((title, provenance, snippet))

    return by_block


def _render_source_interface_table(table_text: str) -> List[str]:
    """Render reliable OCR interface and parameter rows as Markdown tables."""
    raw_lines = [re.sub(r"\s+", " ", line.strip()) for line in table_text.splitlines() if line.strip()]
    header_re = re.compile(
        r"(?:Port name\s+Directio(?:n)?|Pin Name\s+Function|Generic name\s+Type\s+Value)", re.I
    )
    header_indexes = [index for index, line in enumerate(raw_lines) if header_re.search(line)]
    rendered_tables: List[List[str]] = []
    for header_index in header_indexes:
        header = raw_lines[header_index].lower()
        is_parameter = "generic name" in header or "parameter" in header
        end = len(raw_lines)
        for index in range(header_index + 1, len(raw_lines)):
            if index != header_index + 1 and (header_re.search(raw_lines[index]) or re.match(r"^Table\s+\d+", raw_lines[index], re.I)):
                end = index
                break
        is_pin_table = "pin name" in header and "function" in header
        if is_pin_table:
            table = ["| Pin name | Function |", "|---|---|"]
        elif is_parameter:
            table = ["| Parameter | Value / Type | Details |", "|---|---|---|"]
        else:
            table = ["| Port name | Direction | Type / Function | TOP CONNECTION / Details |", "|---|---|---|---|"]
        row_count = 0
        pin_name = ""
        pin_details: List[str] = []

        def flush_pin() -> None:
            nonlocal pin_name, pin_details, row_count
            if pin_name and pin_details:
                details = " ".join(pin_details).replace("|", "\\|")
                escaped_name = pin_name.replace("|", "\\|")
                table.append(f"| {escaped_name} | {details} |")
                row_count += 1
            pin_name = ""
            pin_details = []

        for line in raw_lines[header_index + 1 : end]:
            if re.match(r"^(?:Table\s+\d+|\d+(?:\.\d+)+\s+|Figure\s+)", line, re.I):
                break
            tokens = line.split()
            if is_pin_table:
                if line.lower() in {"[end]", "[end]."}:
                    break
                pin_token = tokens[0] if tokens else ""
                is_pin_name = bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9_<>:/-]*", pin_token)) and (
                    pin_token.upper() == pin_token or "<" in pin_token or "_" in pin_token
                )
                if is_pin_name:
                    flush_pin()
                    pin_name = pin_token
                    pin_details = tokens[1:]
                elif pin_name:
                    pin_details.append(line)
            elif is_parameter:
                if len(tokens) < 2 or tokens[0].lower() in {"generic", "name", "type", "value"}:
                    continue
                name = tokens[0].replace("|", "\\|")
                value = " ".join(tokens[1:]).replace("|", "\\|")
                table.append(f"| {name} | {value} | |")
            else:
                if len(tokens) < 2:
                    continue
                direction_index = next(
                    (index for index, token in enumerate(tokens[1:], start=1)
                     if token.lower() in {"input", "output", "inout", "bidirectional"}),
                    None,
                )
                if direction_index is None:
                    continue
                name = " ".join(tokens[:direction_index]).replace("|", "\\|")
                direction = tokens[direction_index]
                details = " ".join(tokens[direction_index + 1 :]).replace("|", "\\|")
                table.append(f"| {name} | {direction} | {details} | |")
            row_count += 1
        if is_pin_table:
            flush_pin()
        if row_count >= (1 if is_parameter else 2):
            if rendered_tables:
                rendered_tables.append([""])
            rendered_tables.append(table)
    return [line for table in rendered_tables for line in table]


def _render_approved_port_table(rows: List[Dict[str, str]]) -> List[str]:
    """Render approved owner-scoped source ports without losing catalog details."""
    if not rows:
        return []
    lines = ["| Port name | Direction | Type / details | Source page |", "|---|---|---|---|"]
    seen: Set[Tuple[str, str, str, str]] = set()
    for row in rows:
        fields = tuple(row.get(key, "").strip().replace("|", "\\|").replace("\n", " ")
                       for key in ("Port name", "Direction", "Type / details", "Source page"))
        if not fields[0] or fields in seen:
            continue
        seen.add(fields)
        lines.append("| " + " | ".join(fields) + " |")
    return lines if seen else []


def _connection_matrix_upstream_ids(
    interaction_rows: List[Dict[str, str]],
) -> Dict[str, Tuple[str, str]]:
    """Map source cell IDs to the authored SRS matrix ID and exact edge statement."""
    out: Dict[str, Tuple[str, str]] = {}
    matrix_counter = 1
    for row in interaction_rows:
        requirement_ids = (row.get("Requirement IDs") or "").strip()
        source_block = _normalize_block_references((row.get("From block") or "").strip())
        destination_block = _normalize_block_references((row.get("To block") or "").strip())
        if not requirement_ids or not source_block or not destination_block:
            continue
        upstream_id = f"SRS-REQ-{matrix_counter:03d}"
        statement = f"The {source_block} block shall be connected to the {destination_block} block."
        for requirement_id in [item.strip() for item in requirement_ids.split(";") if item.strip()]:
            out[requirement_id] = (upstream_id, statement)
        matrix_counter += 1
    return out


def _connection_matrix_source_owners(interaction_rows: List[Dict[str, str]]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for row in interaction_rows:
        source_block = _normalize_block_references((row.get("From block") or "").strip())
        requirement_ids = (row.get("Requirement IDs") or "").strip()
        if not source_block or not requirement_ids:
            continue
        for requirement_id in [item.strip() for item in requirement_ids.split(";") if item.strip()]:
            out[requirement_id] = source_block
    return out


def _interface_types_by_owner(interface_rows: List[Dict[str, str]]) -> Dict[str, Dict[str, int]]:
    owner_types: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in interface_rows:
        owner = (row.get("Owner") or "").strip()
        iface_type = (row.get("Type") or "").strip().lower()
        if owner and iface_type:
            owner_types[owner][iface_type] += 1
    return owner_types


def _linked_domain_counts(linked_requirements: str) -> Dict[str, int]:
    counts = {"ana": 0, "dig": 0, "sys": 0}
    for token in [t.strip().upper() for t in (linked_requirements or "").split(";") if t.strip()]:
        if "ANA-RQ" in token or "CONF_ANA" in token:
            counts["ana"] += 1
        elif "DIG-RQ" in token or "CONF_DIG" in token:
            counts["dig"] += 1
        elif "SYS-RQ" in token or "CONF_SYS" in token:
            counts["sys"] += 1
    return counts


def _text_score(text: str, terms: Tuple[str, ...]) -> int:
    t = (text or "").lower()
    return sum(1 for token in terms if token in t)


def _classify_block_category(block: BlockInfo, owner_types: Dict[str, Dict[str, int]]) -> str:
    bundle = block.function
    if _text_score(bundle, DIGITAL_ARCHITECTURE_TERMS) > 0:
        return BLOCK_CLASS_DIGITAL
    if "convert" in bundle.lower() and _text_score(bundle, ("adc", "analog")) > 0:
        return BLOCK_CLASS_ANALOG
    analog_score = _text_score(bundle, BLOCK_ANALOG_TERMS)
    power_score = _text_score(bundle, POWER_FOCUS_TERMS)
    digital_score = _text_score(bundle, BLOCK_DIGITAL_TERMS)

    if power_score > 0 and power_score >= digital_score:
        return BLOCK_CLASS_POWER
    if analog_score > digital_score:
        return BLOCK_CLASS_ANALOG

    return BLOCK_CLASS_DIGITAL


def _extract_crosscheck_decision(path: Path) -> str:
    if not path.exists():
        return "unknown"
    text = path.read_text(encoding="utf-8")
    match = re.search(r"Decision:\s*([a-zA-Z\-]+)", text)
    if not match:
        return "unknown"
    return match.group(1).strip().lower()


def _to_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(_to_text(item) for item in value)
    return str(value)


def _is_prose_paragraph_line(line: str) -> bool:
    text = _to_text(line).strip()
    if not text:
        return False
    if text.startswith(("#", "|", "-", "*", ">", "```", "<")):
        return False
    if re.match(r"^\d+\.\s+", text):
        return False
    if re.match(r"^\[DRS-REQ-\d{3}\]\s+Requirement:\s*$", text):
        return False

    field_prefixes = (
        "Statement:",
        "Covers:",
        "Inputs:",
        "Outputs:",
        "General functional description:",
    )
    if any(text.startswith(prefix) for prefix in field_prefixes):
        return False
    return True


def _ensure_blank_line_between_paragraphs(lines: List[str]) -> List[str]:
    if not lines:
        return lines
    out: List[str] = []
    in_requirement = False
    for idx, line in enumerate(lines):
        text = _to_text(line).strip()
        if re.match(r"^\[DRS-REQ-\d{3}\]\s+Requirement:\s*$", text):
            in_requirement = True
        out.append(line)
        if text.startswith("Covers:"):
            in_requirement = False
            continue
        if idx >= len(lines) - 1:
            continue
        next_line = lines[idx + 1]
        current_is_list_item = bool(re.match(r"^(?:[-*+]\s+|\d+[.)]\s+|•\s+)", text))
        next_text = _to_text(next_line).strip()
        next_is_list_item = bool(re.match(r"^(?:[-*+]\s+|\d+[.)]\s+|•\s+)", next_text))
        if in_requirement and not (next_is_list_item and text and not current_is_list_item):
            continue
        if (next_is_list_item and text and not current_is_list_item) or (
            _is_prose_paragraph_line(line) and _is_prose_paragraph_line(next_line)
        ):
            out.append("")
    return out


def _insert_visible_paragraph_spacers(lines: List[str]) -> List[str]:
    if not lines:
        return lines

    out: List[str] = []
    idx = 0
    n = len(lines)
    in_requirement = False
    in_fenced_block = False
    while idx < n:
        line = lines[idx]
        text = _to_text(line).strip()
        is_fence = text.startswith("```")
        if re.match(r"^\[DRS-REQ-\d{3}\]\s+Requirement:\s*$", text):
            in_requirement = True
        if text != "":
            out.append(line)
            if text.startswith("Covers:"):
                in_requirement = False
            if is_fence:
                in_fenced_block = not in_fenced_block
            idx += 1
            continue

        blank_start = idx
        while idx < n and _to_text(lines[idx]).strip() == "":
            idx += 1
        blank_end = idx

        prev_idx = blank_start - 1
        while prev_idx >= 0 and _to_text(lines[prev_idx]).strip() == "":
            prev_idx -= 1
        next_idx = blank_end
        while next_idx < n and _to_text(lines[next_idx]).strip() == "":
            next_idx += 1

        prev_line = lines[prev_idx] if prev_idx >= 0 else ""
        next_line = lines[next_idx] if next_idx < n else ""
        next_is_requirement = bool(re.match(r"^\[DRS-REQ-\d{3}\]\s+Requirement:\s*$", _to_text(next_line).strip()))
        needs_spacer = not in_fenced_block and not in_requirement and (
            (_is_prose_paragraph_line(prev_line) and (
                _to_text(next_line).lstrip().startswith("#") or _is_prose_paragraph_line(next_line)
            ))
            or (
                prev_line.strip().startswith(("Covers:", "Source paragraph:"))
                and next_is_requirement
            )
        )

        out.append("")
        if needs_spacer and (not out or out[-1] != "<p>&nbsp;</p>"):
            out.append("<p>&nbsp;</p>")
            out.append("")
    return out


def _ensure_requirement_block_spacing(lines: List[str]) -> List[str]:
    out: List[str] = []
    for line in lines:
        if re.match(r"^\[DRS-REQ-\d{3}\]\s+Requirement:\s*$", _to_text(line).strip()):
            if out and _to_text(out[-1]).strip():
                out.append("")
        if re.match(r"^\s*Covers:\s*\S+\s*$", _to_text(line).strip()):
            if out and _to_text(out[-1]).strip():
                out.append("")
        if re.match(r"^\[DRS-REQ-\d{3}\]\s+Requirement:\s*$", _to_text(line).strip()):
            while out and not _to_text(out[-1]).strip():
                out.pop()
            if out:
                out.extend(["", ""])
            out.append(line)
            out.append("")
            continue
        out.append(line)
    return out


def _terminate_authored_requirement_blocks(lines: List[str]) -> List[str]:
    return normalize_authored_requirement_blocks(lines, ("DRS",))


def _ensure_subparagraph_heading_spacing(lines: List[str]) -> List[str]:
    out: List[str] = []
    sub_heading_re = re.compile(r"^#{4,6}\s+\d+(?:\.\d+){1,}\.?.*")
    for line in lines:
        if sub_heading_re.match(_to_text(line).strip()):
            while out and not _to_text(out[-1]).strip():
                out.pop()
            if out and _to_text(out[-1]).strip() != "<p>&nbsp;</p>":
                out.extend(["", "<p>&nbsp;</p>", ""])
            out.append(line)
            continue
        out.append(line)
    return out


def _ensure_table_block_spacing(lines: List[str]) -> List[str]:
    out: List[str] = []

    def _is_table_row(text: str) -> bool:
        t = _to_text(text).strip()
        return t.startswith("|") and t.endswith("|") and len(t) >= 2

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if not _is_table_row(line):
            out.append(line)
            i += 1
            continue

        while out and _to_text(out[-1]).strip() == "":
            out.pop()
        if out:
            out.append("")

        while i < n and _is_table_row(lines[i]):
            out.append(lines[i])
            i += 1

        while i < n and _to_text(lines[i]).strip() == "":
            i += 1

        if i < n:
            out.extend(["", "<p>&nbsp;</p>", ""])

    return out


def _build_heading_registry(lines: List[str]) -> List[Tuple[int, str, str, str]]:
    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
    used: Dict[str, int] = defaultdict(int)
    registry: List[Tuple[int, str, str, str]] = []

    for line in lines:
        line_text = _to_text(line)
        match = heading_re.match(line_text)
        if not match:
            continue

        level = len(match.group(1))
        raw_title = match.group(2).strip()
        explicit_id_match = re.search(r"\s*\{#([a-zA-Z0-9_-]+)\}\s*$", raw_title)
        title = re.sub(r"\s*\{#[a-zA-Z0-9_-]+\}\s*$", "", raw_title).strip()
        base = re.sub(r"[^a-z0-9\s-]", "", title.lower())
        base = re.sub(r"\s+", "-", base).strip("-") or "section"

        if explicit_id_match:
            anchor = explicit_id_match.group(1)
        else:
            used[base] += 1
            anchor = base if used[base] == 1 else f"{base}-{used[base] - 1}"

        section_number = ""
        token_match = re.match(r"^(\d+(?:\.\d+)*)\.?,?", title)
        if token_match:
            section_number = token_match.group(1)

        registry.append((level, title, anchor, section_number))

    return registry


def _apply_explicit_heading_ids(lines: List[str]) -> List[str]:
    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
    used: Dict[str, int] = defaultdict(int)
    out: List[str] = []

    for line in lines:
        text = _to_text(line)
        match = heading_re.match(text)
        if not match:
            out.append(text)
            continue

        hashes = match.group(1)
        raw_title = match.group(2).strip()
        if re.search(r"\s*\{#[a-zA-Z0-9_-]+\}\s*$", raw_title):
            out.append(text)
            continue

        title = raw_title
        base = re.sub(r"[^a-z0-9\s-]", "", title.lower())
        base = re.sub(r"\s+", "-", base).strip("-") or "section"
        used[base] += 1
        anchor = base if used[base] == 1 else f"{base}-{used[base] - 1}"
        out.append(f"{hashes} {title} {{#{anchor}}}")

    return out


def _inventory_digital_blocks(blocks: List[BlockInfo], interface_rows: List[Dict[str, str]]) -> Set[str]:
    owner_types = _interface_types_by_owner(interface_rows)
    out: Set[str] = set()
    for block in blocks:
        category = _classify_block_category(block, owner_types)
        # DRS includes digital logic plus power/clock support blocks.
        if category in {BLOCK_CLASS_DIGITAL, BLOCK_CLASS_POWER}:
            out.add(block.name)
    return out


def _drs_descriptive_blocks(
    block_inventory: List[BlockInfo],
    interface_rows: List[Dict[str, str]],
    source_interface_tables: Dict[str, List[Tuple[str, str, str]]],
) -> List[BlockInfo]:
    """Select only approved concrete digital blocks from existing DRS evidence."""
    digital_blocks = _inventory_digital_blocks(block_inventory, interface_rows)
    owner_types = _interface_types_by_owner(interface_rows)
    for block in block_inventory:
        titles = [title.lower() for title, _, _ in source_interface_tables.get(block.name, [])]
        has_digital_table = any(term in title for title in titles for term in DIGITAL_INTERFACE_TABLE_TERMS)
        if block.name in source_interface_tables and (
            _classify_block_category(block, owner_types) != BLOCK_CLASS_ANALOG or has_digital_table
        ):
            digital_blocks.add(block.name)
    return [block for block in block_inventory
            if block.name in digital_blocks and block.entity_kind.casefold() == "concrete_block"]


def _append_drs_block_description_audit(path: Path, blocks: List[BlockInfo]) -> None:
    with path.open("r", encoding="utf-8", newline="") as handle:
        fieldnames = next(csv.reader(handle))
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        for order, block in enumerate(blocks, start=1):
            writer.writerow({
                "section": "DRS digital block descriptions",
                "input_order": str(order),
                "output_order": str(order),
                "decision": "retained",
                "topic": "Digital block purpose",
                "scope": "block_local_digital",
                "scope_decision": "approved_concrete_block",
                "mapped_block": block.name,
                "domain": "digital",
                "statement": compose_technical_block_purpose(block.name, block.function),
                "source": "artifacts/stage2_mirco_arc/block_inventory.csv",
                "source_evidence": block.function,
                "functional_evidence": block.function,
            })


DRS_INTRO_TOPICS = (
    ("4.2 Arbitration, control, and shared resources", r"control|mode|state|interrupt|status|configuration|xbar|fifo|memory|register"),
    ("4.3 Register and configuration requirements", r"register|configuration"),
    ("4.4 Interface and communication requirements", r"spi|i2c|ahb|bus|host|protocol"),
    ("4.5 Data-path and buffering requirements", r"fifo|buffer|sample|data|watermark|overrun|empty"),
    ("4.6 Digital performance requirements", r"clock|reset|latency|timing|startup"),
)


DRS_NARRATIVE_ROLE_TERMS = {
    "Power and clock islands": ("clock", "por", "power mode"),
    "Buses and interconnects": ("i2c", "spi", "ahb"),
    "Arbitration and control": ("mutually exclusive", "write-protection", "register access"),
    "Shared digital resources": ("fifo storage", "mapped", "memory access"),
    "Digital processing blocks": ("signal elaboration", "dsp elaboration", "signal processing"),
    "Arbitration, control, and shared resources": ("mutually exclusive", "fifo storage", "memory access", "mapped", "control"),
    "4.2 Arbitration, control, and shared resources": ("mutually exclusive", "fifo storage", "memory access", "mapped", "control"),
    "4.3 Register and configuration requirements": ("mapped", "write-protection", "configuration"),
    "4.4 Interface and communication requirements": ("i2c", "spi", "ahb"),
    "4.5 Data-path and buffering requirements": ("fifo storage", "fifo multi-mode", "data formatting"),
    "4.6 Digital performance requirements": ("clock", "por", "clock-ready"),
    "7. Interfaces and mixed-signal interactions": ("analog domain", "adc", "i2c", "spi", "ahb", "pad"),
}


def _drs_topic_narrative(topic: str, blocks: List[BlockInfo]) -> str:
    terms = DRS_NARRATIVE_ROLE_TERMS.get(topic, ())
    ranked = sorted(
        (block for block in blocks if not re.search(r"\b(?:represent|described by .* evidence)\b", block.function, re.I)),
        key=lambda block: -sum(term in block.function.casefold() for term in terms),
    )
    selected = [block for block in ranked if any(term in block.function.casefold() for term in terms)][:2]
    return compose_drs_role_summary([(block.name, block.function) for block in selected], terms) or "need clarification"


def _drs_section_interaction_summary(rows: List[Tuple[str, str, str]]) -> str:
    return compose_drs_interaction_summary(rows)


def _drs_source_capability_sentence(statement: str) -> str:
    text = " ".join(statement.split()).strip()
    match = re.fullmatch(
        r"Aim of this document is to explain main features of the (.+?), electronic interface[s]? of (.+)",
        text.rstrip("."),
        re.I,
    )
    if match:
        return f"The {match[1]} integrates electronic interfaces for {match[2].rstrip('.')}."
    text = re.sub(r"^Aim of this document is to explain\s+", "", text, flags=re.I)
    return text[:1].upper() + text[1:] if text else ""


def _drs_top_level_overview(
    rows: List[Tuple[str, str, str]],
    source_capabilities: List[str] | None = None,
) -> str:
    """Summarize approved Digital Top capability families without block detail."""
    families = (
        ("data", ("sample", "data", "stream", "fifo", "sensor"),
         "supports digital acquisition, data movement, and buffering across the recorded integration paths"),
        ("control", ("configuration", "register", "mode", "control", "status", "interrupt"),
         "supports configuration, control, status, and interrupt interactions"),
        ("interfaces", ("spi", "i2c", "ahb", "bus", "protocol", "host"),
         "provides the recorded serial, bus, and host-facing integration paths"),
        ("power", ("power/clock", "power mode", "reset", "clock"),
         "coordinates the recorded power, clock, and operating-mode interactions"),
    )
    capabilities = [
        description for _name, terms, description in families
        if any(any(term in exchange.casefold() for term in terms) for _source, _target, exchange in rows)
    ]
    if not capabilities:
        return "The approved Digital Top overview is not sufficiently specified by the available architecture evidence."
    capability_text = capabilities[0] if len(capabilities) == 1 else "; ".join(capabilities[:-1]) + "; and " + capabilities[-1]
    source_text = " ".join(
        sentence for sentence in (_drs_source_capability_sentence(item) for item in (source_capabilities or []))
        if sentence
    )
    overview = "The Digital Top is the digital integration layer for the recorded top-level interfaces. It " + capability_text + ". The source material does not define a separate application role."
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", (source_text + " " + overview).strip())
    paragraphs = [" ".join(sentences[index:index + 2]) for index in range(0, len(sentences), 2)]
    return "\n\n".join(paragraphs)


def _drs_clock_section_summary(paths: List[Tuple[str, str, str, str, str]]) -> str:
    return compose_drs_clock_summary(paths)


def _drs_processing_summary(blocks: List[BlockInfo], interactions: List[Tuple[str, str, str]]) -> str:
    role = _drs_topic_narrative("Digital processing blocks", blocks)
    relationships = _drs_section_interaction_summary(interactions)
    if role == "need clarification":
        return relationships + " Processing behavior: need clarification."
    return role + " " + relationships


DRS_SHARED_FACETS = (
    ("Shared-resource ownership", ("fifo storage", "mutually exclusive", "shared resource")),
    ("Register and memory access coordination", ("register", "memory access", "mapped", "ahb")),
    ("Flow control and backpressure", ("backpressure", "flow control", "stall", "ready/valid")),
    ("Synchronization", ("synchronization mechanism", "clock-domain crossing", "reset-domain crossing")),
    ("Reset and boot coordination", ("boot", "reset", "por")),
    ("Latency and bandwidth", ("latency", "bandwidth", "throughput")),
    ("Power and clock interaction", ("clock", "power mode", "power/clock")),
)


def _drs_shared_facet_rows(blocks: List[BlockInfo], interactions: List[Tuple[str, str, str]]) -> List[Tuple[str, str]]:
    rows = []
    rendered_sentences: Set[str] = set()
    for facet, terms in DRS_SHARED_FACETS:
        owners = [(block.name, block.function)
              for block in blocks if any(term in block.function.casefold() for term in terms)
              and not re.search(r"\b(?:represent|described by .* evidence)\b", block.function, re.I)]
        exchanges = [row for row in interactions if any(term in row[2].casefold() for term in terms)]
        detail = compose_drs_role_summary(owners, terms)
        if exchanges:
            detail += " " + _drs_section_interaction_summary(exchanges)
        sentences = re.split(r"(?<=\.)\s+", detail.strip()) if detail.strip() else []
        distinct = [sentence for sentence in sentences if sentence not in rendered_sentences]
        if distinct:
            detail = " ".join(distinct)
        rendered_sentences.update(sentences)
        detail = detail.strip() or "need clarification"
        if facet == "Register and memory access coordination" and (owners or exchanges):
            detail += " Concurrent-access ordering policy: need clarification."
        rows.append((facet, detail))
    return rows


def _drs_rendered_prose_findings(markdown: str, document: ET.Element | None = None) -> List[str]:
    sections = {"1.2", "3", "3.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "7"}
    findings = []

    def inspect(paragraphs: List[Tuple[bool, str]], artifact: str) -> None:
        active = ""
        for is_heading, text in paragraphs:
            if is_heading:
                number = re.match(r"^(\d+(?:\.\d+)*)\.?\s+", text)
                if number:
                    active = number.group(1)
                continue
            if active in sections:
                findings.extend(f"drs_section_prose:{artifact}:{active}:{finding}"
                                for finding in drs_section_prose_findings(text))

    paragraphs = []
    for line in markdown.splitlines():
        if not line.strip() or line.startswith(("|", "<")):
            continue
        heading = re.match(r"^#{1,6}\s+(.+)", line)
        text = heading.group(1).replace("**", "") if heading else line
        paragraphs.append((bool(heading), text))
    inspect(paragraphs, "markdown")
    if document is not None:
        word = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        body = document.find(word + "body")
        docx_paragraphs = []
        if body is not None:
            for paragraph in body.findall(word + "p"):
                text = "".join(node.text or "" for node in paragraph.iter(word + "t"))
                style = paragraph.find(word + "pPr/" + word + "pStyle")
                is_heading = style is not None and style.get(word + "val", "").casefold().startswith("heading")
                docx_paragraphs.append((is_heading, text))
        inspect(docx_paragraphs, "docx")
    return list(dict.fromkeys(findings))


def _drs_power_clock_routes(clock_paths: List[Tuple[str, str, str, str, str]], blocks: List[BlockInfo]) -> List[Tuple[str, str, str, str, str]]:
    clock_owners = [block.name for block in blocks if "clock" in block.function.casefold()]
    return [path for path in clock_paths if path[1] != "need clarification"
            and any(f"u_{owner.casefold().replace(' ', '_')}." in path[1].casefold() for owner in clock_owners)]


def _drs_power_reset_outputs(port_rows: List[Dict[str, str]], blocks: List[BlockInfo]) -> List[Tuple[str, str, str, str]]:
    clock_owners = {block.name for block in blocks if "clock" in block.function.casefold()}
    return [(row["Owner"], row["Port name"], row["Type / details"], row["Source page"])
            for row in port_rows if row.get("Ownership status") == "approved"
            and row.get("Owner") in clock_owners and row.get("Direction") == "output"
            and row.get("Port name", "").casefold().startswith("resetn_")
            and "reset" in row.get("Type / details", "").casefold() and row.get("Source page")]


def _drs_intro_rows(entries: List[str], block_names: Set[str] | None = None) -> Dict[str, List[Tuple[str, str, str]]]:
    interactions = project_architecture_interactions(entries)
    rows = {
        topic: [row for row in interactions if re.search(pattern, row[2], re.I)]
        for topic, pattern in DRS_INTRO_TOPICS
    }
    rows["3. Top Level Overview"] = interactions
    if block_names is not None:
        rows["7. Interfaces and mixed-signal interactions"] = [
            row for row in interactions if row[0] not in block_names or row[1] not in block_names
        ]
    return rows


def _drs_power_domain_rows(records: List[Dict[str, str]]) -> List[Tuple[str, str, str, str]]:
    rows: List[Tuple[str, str, str, str]] = []
    for record in records:
        if record.get("evidence_kind") != "power_domain":
            continue
        statement = record.get("statement", "")
        name = re.match(r"^([A-Z][A-Z0-9_]+):", statement)
        domain_type = re.search(r"Domain type: ([^.]+)\.", statement)
        control = re.search(r"Control mode: ([^.]+)\.", statement)
        function = re.search(r"(?:^|•)\s*Function: (.+?)(?=\s*•|$)", statement)
        if name and domain_type and control and function:
            rows.append((name.group(1), domain_type.group(1).strip(), control.group(1).strip(), function.group(1).strip().rstrip(".")))
    return rows


def _drs_domain_function_sentence(name: str, function: str) -> str:
    supply = re.match(r"power supply to (.+)", function, re.I)
    if supply:
        return f"{name} supplies power to {supply.group(1)}."
    if re.match(r"(?:ensures|powers|supplies|provides|maintains|controls|retains|manages|routes|supports|enables|delivers|stores|sequences|holds|isolates|coordinates)\b", function, re.I):
        return f"{name} {function[:1].lower() + function[1:]}{'' if function.endswith('.') else '.'}"
    return f"{name} has the documented function: {function}{'' if function.endswith('.') else '.'}"


def _drs_block_relationships(block_name: str, interactions: List[Tuple[str, str, str]]) -> str:
    relationships = []
    for source, target, exchange in interactions:
        if source == block_name:
            relationships.append(f"to {target} ({exchange})")
        elif target == block_name:
            relationships.append(f"from {source} ({exchange})")
    return "; ".join(relationships) if relationships else "Detailed integration relationship: need clarification."


def _drs_function_summary(
    block: BlockInfo,
    requirement_statements: List[str],
    stage1_descriptions: Optional[List[Dict[str, str]]] = None,
) -> str:
    stage1_text = " ".join(
        record.get("statement", "").strip()
        for record in stage1_descriptions or []
        if record.get("statement", "").strip()
    )
    if not re.search(r"\b(?:represent|described by .* evidence)\b", block.function, re.I):
        summary = compose_technical_block_purpose(block.name, block.function)
        return f"{summary} {stage1_text}".strip() if stage1_text else summary
    wake_up = re.compile(rf"\bto wake up the {re.escape(block.name)}\b.*\btrigger an interrupt\b", re.I)
    if any(wake_up.search(statement) for statement in requirement_statements):
        wake_summary = f"An interrupt triggers {block.name} wake-up."
        return f"{wake_summary} {stage1_text}".strip() if stage1_text else f"{wake_summary} Local processing function: need clarification."
    if stage1_text:
        return stage1_text
    return f"The local processing function of {block.name}: need clarification."
def _append_drs_block_description_audit(
    path: Path,
    blocks: List[BlockInfo],
    stage1_descriptions: Optional[Dict[str, List[Dict[str, str]]]] = None,
) -> None:
    with path.open("r", encoding="utf-8", newline="") as handle:
        fieldnames = next(csv.reader(handle))
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        for order, block in enumerate(blocks, start=1):
            writer.writerow({
                "section": "DRS digital block descriptions",
                "input_order": str(order),
                "output_order": str(order),
                "decision": "retained",
                "topic": "Digital block purpose",
                "scope": "block_local_digital",
                "scope_decision": "approved_concrete_block",
                "mapped_block": block.name,
                "domain": "digital",
                "statement": compose_technical_block_purpose(block.name, block.function),
                "source": "artifacts/stage2_mirco_arc/block_inventory.csv",
                "source_evidence": block.function,
                "functional_evidence": block.function,
            })
        for block_name, records in (stage1_descriptions or {}).items():
            for record in records:
                writer.writerow({
                    "section": "DRS Stage 1 source descriptions",
                    "input_order": "",
                    "output_order": "",
                    "decision": "retained",
                    "reason": "complete Stage 1 overview description",
                    "topic": "Digital block purpose",
                    "scope": "block_local_digital",
                    "scope_decision": "explicit source subject",
                    "mapped_block": block_name,
                    "domain": "digital",
                    "statement": record.get("statement", ""),
                    "source": record.get("source", ""),
                    "source_evidence": record.get("statement", ""),
                    "functional_evidence": record.get("statement", ""),
                })


def _append_drs_stage1_overview_audit(path: Path, records: List[Dict[str, str]]) -> None:
    if not records:
        return
    with path.open("r", encoding="utf-8", newline="") as handle:
        fieldnames = next(csv.reader(handle))
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        for order, record in enumerate(records, start=1):
            source_text = record.get("statement", "").strip()
            writer.writerow({
                "section": "DRS Stage 1 overview descriptions",
                "input_order": str(order),
                "output_order": str(order),
                "decision": "retained",
                "reason": "source-backed descriptive overview",
                "topic": "Top Level Overview",
                "scope": "top_digital",
                "scope_decision": "approved snapshot scope",
                "domain": "digital",
                "statement": _drs_source_capability_sentence(source_text),
                "source": record.get("source", ""),
                "source_evidence": record.get("source_evidence", source_text),
                "functional_evidence": source_text,
            })


def _drs_has_synchronization_evidence(requirement_statements: List[str]) -> bool:
    return any(re.search(r"\b(?:clock[- ]domain crossing|reset[- ]domain crossing|synchroniz\w*|interrupt latency|response time)\b", statement, re.I)
               for statement in requirement_statements)


def _drs_clock_path_rows(snapshot_rows: List[Dict[str, str]]) -> List[Tuple[str, str, str, str, str]]:
    paths = []
    pattern = re.compile(
        r"^The (\S+) signal shall be connected to the (\S+) signal, "
        r"with frequency ([\d.]+\s*(?:MHz|kHz|Hz)) and (with|without) clock gating(?:\s+(.*?))?\.\s*$", re.I,
    )
    for row in snapshot_rows:
        if row.get("approved_classification") != "Digital" or row.get("lifecycle_state") != "approved":
            continue
        match = pattern.match(row.get("requirement_statement", ""))
        if match and row.get("source_req_id"):
            source, target, frequency, gating, control = match.groups()
            if re.search(r"(?:^|\.)u\.", source) or re.search(r"(?:^|\.)u\.", target):
                source = target = "need clarification"
            if gating == "with":
                control = (control or "").strip()
                gating_text = f"Gated; control expression: {control}" if control else "Gated; control expression: need clarification"
                if control and re.search(r"\b[A-Za-z_]\w*\s+[A-Za-z_]\w*\.", control):
                    gating_text += "; signal spelling: need clarification"
            else:
                gating_text = "Not gated"
            paths.append((row["source_req_id"], source, target, frequency,
                          gating_text))
    return paths


def _drs_clock_path_markdown_row(path: Tuple[str, str, str, str, str]) -> str:
    return "| " + " | ".join((*path[:4], path[4].replace("|", r"\|"))) + " |"


def _drs_sync_connection_rows(snapshot_rows: List[Dict[str, str]], port_rows: List[Dict[str, str]]) -> List[Tuple[str, str, str]]:
    connections = []
    approved_ports = [row for row in port_rows if row.get("Ownership status") == "approved"]
    for row in snapshot_rows:
        statement = row.get("requirement_statement", "")
        if (row.get("approved_classification") != "Digital" or row.get("lifecycle_state") != "approved"
                or not row.get("source_req_id") or "shall be connected to" not in statement):
            continue
        normalized_statement = re.sub(r"\s+", "", statement)
        target_text = statement.split("shall be connected to", 1)[1]
        normalized_target = re.sub(r"\s+", "", target_text)
        if not re.search(r"(?:rstn|resetn|clk)_sync", normalized_target, re.I):
            continue
        sources = [port for port in approved_ports if port.get("Direction") == "output"
                   and "reset" in port.get("Port name", "").casefold()
                   and port.get("Port name", "") in normalized_statement
                   and port.get("Owner")]
        targets = [port for port in approved_ports if port.get("Direction") == "input"
                   and "_sync" in port.get("Port name", "").casefold()
                   and port.get("Port name", "") in normalized_target
                   and port.get("Owner")]
        source = f"{sources[0]['Owner']}.{sources[0]['Port name']}" if len(sources) == 1 else "need clarification"
        target = f"{targets[0]['Owner']}.{targets[0]['Port name']}" if len(targets) == 1 else "need clarification"
        connections.append((row["source_req_id"], source, target))
    return connections


def _append_drs_intro_audit(path: Path, records: List[Dict[str, str]], block_names: Set[str]) -> None:
    rows = _drs_intro_rows([record.get("statement", "") for record in records], block_names)
    with path.open("r", encoding="utf-8", newline="") as handle:
        fieldnames = next(csv.reader(handle))
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        for topic, interactions in rows.items():
            for order, (source, target, exchange) in enumerate(interactions, start=1):
                evidence = next((record for record in records if
                    (source, target, exchange) in project_architecture_interactions([record.get("statement", "")])
                ), {})
                writer.writerow({
                    "section": "DRS introductory architecture", "topic": topic,
                    "input_order": str(order), "output_order": str(order), "decision": "retained",
                    "statement": f"{source} -> {target}: {exchange}",
                    "source": evidence.get("source", ""),
                    "source_evidence": evidence.get("statement", ""),
                    "scope": "top_digital",
                })
def validate_drs_descriptive_artifacts(repo_root: Path) -> List[str]:
    """Apply the shared descriptive contract to existing DRS artifacts."""
    markdown_path = repo_root / "artifacts/stage5_drs/digital_requirements_specification.md"
    audit_path = markdown_path.with_name("descriptive_summary_audit.csv")
    docx_path = markdown_path.with_suffix(".docx")
    if not markdown_path.exists() or not audit_path.exists() or not docx_path.exists():
        return ["DRS descriptive Markdown, audit, or DOCX is missing"]
    block_inventory = _read_block_inventory(repo_root / "artifacts/stage2_mirco_arc/block_inventory.csv")
    interface_rows = _read_interface_rows(repo_root / "artifacts/stage2_mirco_arc/interface_catalog.csv")
    tables = _source_interface_tables_by_block(repo_root, block_inventory)
    blocks = _drs_descriptive_blocks(block_inventory, interface_rows, tables)
    port_rows = _read_interface_rows(repo_root / "artifacts/stage2_mirco_arc/source_port_catalog.csv")
    with audit_path.open("r", encoding="utf-8", newline="") as handle:
        audit_rows = list(csv.DictReader(handle))
    findings = validate_drs_block_descriptions(
        markdown_path.read_text(encoding="utf-8"),
        [{"name": block.name, "function": block.function} for block in blocks],
        audit_rows, port_rows, docx_path,
    )
    matrix_records = _top_digital_coverage_records(
        _read_interaction_rows(repo_root / "artifacts/stage2_mirco_arc/interaction_matrix.csv"), [], [], []
    )
    expected = _drs_intro_rows([record.get("statement", "") for record in matrix_records],
                               {block.name for block in blocks})
    markdown = markdown_path.read_text(encoding="utf-8")
    intro_audit = [row for row in audit_rows if row.get("section") == "DRS introductory architecture"]
    docx_rows: Set[Tuple[str, str, str]] = set()
    docx_tables: List[List[str]] = []
    docx_text = ""
    try:
        with zipfile.ZipFile(docx_path) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))
        word = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        docx_text = " ".join(text.text or "" for text in document.iter(word + "t"))
        findings.extend(_drs_rendered_prose_findings(markdown, document))
        for table in document.iter(word + "tbl"):
            for table_row in table.iter(word + "tr"):
                cells = ["".join(text.text or "" for text in cell.iter(word + "t")).strip()
                         for cell in table_row.iter(word + "tc")]
                if len(cells) >= 3:
                    docx_rows.add(tuple(cells[:3]))
                    docx_tables.append(cells)
    except (OSError, KeyError, ValueError, ET.ParseError, zipfile.BadZipFile):
        findings.append("drs_intro_docx_unreadable")
    power_audit_path = markdown_path.with_name("descriptive_low_power_audit.csv")
    if power_audit_path.exists():
        with power_audit_path.open("r", encoding="utf-8", newline="") as handle:
            power_audit = list(csv.DictReader(handle))
    else:
        power_audit = []
        findings.append("drs_power_domain_audit_missing")
    power_rows = _drs_power_domain_rows([
        {"evidence_kind": "power_domain", "statement": row.get("statement", "")}
        for row in power_audit if row.get("decision") == "selected"
        and row.get("query_seed") == "structured power-domain evidence"
    ])
    if power_domain_records_from_ocr(repo_root) and not power_rows:
        findings.append("drs_power_domain_evidence_missing")
    if power_rows:
        if "| Domain | Type | Control | Function |" not in markdown or ["Domain", "Type", "Control", "Function"] not in docx_tables:
            findings.append("drs_power_domain_table_missing")
        for name, domain_type, control, function in power_rows:
            if f"| {name} | {domain_type} | {control} | {function} |" not in markdown or [name, domain_type, control, function] not in docx_tables:
                findings.append(f"drs_power_domain_row_missing:{name}")
    block_section = re.search(r"(?ms)^### (?:\*\*)?4\.1 Digital block list[^\n]*\n(.*?)(?=^### (?:\*\*)?4\.2 )", markdown)
    functions_section = re.search(r"(?ms)^### (?:\*\*)?3\.1 Digital Main Functions[^\n]*\n(.*?)(?=^## (?:\*\*)?4\.)", markdown)
    if functions_section and re.search(r"(?m)^.*:\s*[•-]\s+", functions_section.group(1)):
        findings.append("drs_low_power_fragment_in_functions")
    if functions_section:
        named_headings = re.findall(r"(?m)^####\s+(?:\*\*)?([^*{\n]+?)(?:\*\*)?\s*(?:\{#[^}]+\})?\s*$", functions_section.group(1))
        for name in named_headings:
            if name.strip() in {block.name for block in blocks}:
                continue
            if name.strip() not in {topic for topic, _ in DESCRIPTIVE_DIGITAL_TOPIC_SPECS} | {
                "Arbitration, control, and shared resources", "Power-domain architecture", "Low-power state behavior", "Entry, exit, wake-up, and restore",
                "Sequencing and domain control", "Low-power responsibility",
            }:
                findings.append(f"drs_unapproved_function_subparagraph:{name.strip()}")
    if blocks and (not block_section or "| Block | Role | Architectural relationship |" not in block_section.group(1) or ["Block", "Role", "Architectural relationship"] not in docx_tables):
        findings.append("drs_block_roles_table_missing")
    with (repo_root / "artifacts/stage5_drs/drs_traceability_matrix.csv").open("r", encoding="utf-8", newline="") as handle:
        drs_statements = [row.get("requirement_statement", "") for row in csv.DictReader(handle)]
    _stage1_overview_records, stage1_block_descriptions = _stage1_overview_descriptive_records(
        repo_root / "artifacts/stage1_requirements/ocr_extracts/index.csv",
        blocks,
    )
    for block in blocks:
        purpose = _drs_function_summary(
            block,
            drs_statements,
            stage1_block_descriptions.get(block.name, []),
        )
        relationship = _drs_block_relationships(block.name, expected["3. Top Level Overview"])
        block_heading = (re.search(rf"(?m)^####\s+(?:\*\*)?{re.escape(block.name)}(?:\*\*)?\s*(?:\{{#[^}}]+\}})?\s*$", functions_section.group(1))
                         if functions_section else None)
        block_body = functions_section.group(1)[block_heading.end():].split("\n#### ", 1)[0] if block_heading else ""
        if stage1_block_descriptions.get(block.name):
            evidence_present = block.name in block_body and block.name in docx_text
            if not evidence_present:
                findings.append(f"drs_digital_function_missing:{block.name}")
        role = (_drs_function_summary(block, drs_statements)
            if re.search(r"\b(?:represent|described by .* evidence)\b", block.function, re.I)
            else block.function)
        if not block_section or f"| {block.name} | {role} | {relationship} |" not in block_section.group(1) or [block.name, role, relationship] not in docx_tables:
            findings.append(f"drs_block_role_or_relationship_missing:{block.name}")
    selected_topics = organize_descriptive_topics(matrix_records, DESCRIPTIVE_DIGITAL_TOPIC_SPECS)
    combined_entries = list(dict.fromkeys(
        selected_topics.get("Arbitration and control", [])
        + _shared_resource_access_records(matrix_records)
        + selected_topics.get("Shared digital resources", [])))
    snapshot_id_match = re.search(r"(?m)^Snapshot ID: (\S+)$", markdown)
    snapshot_clock_paths = (_drs_clock_path_rows(load_sqlite_snapshot_input(
        repo_root, "DRS", snapshot_id=snapshot_id_match.group(1)).rows)
        if snapshot_id_match else [])
    for topic in DRS_NARRATIVE_ROLE_TERMS:
        if topic.startswith(("4.", "7.")) or topic in {"Arbitration and control", "Shared digital resources"}:
            continue
        heading = re.search(rf"(?m)^####\s+(?:\*\*)?{re.escape(topic)}(?:\*\*)?\s*(?:\{{#[^}}]+\}})?\s*$", functions_section.group(1)) if functions_section else None
        body = functions_section.group(1)[heading.end():].split("\n#### ", 1)[0] if heading else ""
        narrative = (_drs_section_interaction_summary(project_architecture_interactions(selected_topics[topic]))
                     if topic in selected_topics else None)
        if topic == "Arbitration, control, and shared resources":
            narrative = _drs_section_interaction_summary(project_architecture_interactions(combined_entries))
        if topic == "Power and clock islands":
            narrative = _drs_clock_section_summary(_drs_power_clock_routes(snapshot_clock_paths, blocks))
        if topic == "Digital processing blocks" and narrative:
            narrative = _drs_processing_summary(blocks, project_architecture_interactions(selected_topics[topic]))
        if topic == "Sequencing and domain control":
            narrative = _drs_clock_section_summary(_drs_power_clock_routes(snapshot_clock_paths, blocks))
        if narrative is None:
            continue
        if narrative not in body or narrative not in docx_text:
            findings.append(f"drs_digital_topic_narrative_missing:{topic}")
    if functions_section and "Priority between simultaneous resource requesters: need clarification." not in functions_section.group(1):
        findings.append("drs_arbitration_boundary_missing")
    shared_section = re.search(r"(?ms)^### (?:\*\*)?4\.2 Arbitration, control, and shared resources[^\n]*\n(.*?)(?=^### (?:\*\*)?4\.3 )", markdown)
    shared_narrative = _drs_section_interaction_summary(expected[DRS_INTRO_TOPICS[0][0]])
    if not shared_section or shared_narrative not in shared_section.group(1) or shared_narrative not in docx_text:
        findings.append("drs_shared_section_summary_missing")
    shared_rows = _drs_shared_facet_rows(blocks, expected[DRS_INTRO_TOPICS[0][0]])
    for facet, evidence in shared_rows:
        statement = f"{facet}: {evidence}"
        if not shared_section or statement not in shared_section.group(1) or statement not in docx_text:
            findings.append(f"drs_shared_facet_missing:{facet}")
    performance_section = re.search(r"(?ms)^### (?:\*\*)?4\.6 Digital performance requirements[^\n]*\n(.*?)(?=^### (?:\*\*)?4\.7 )", markdown)
    reset_outputs = _drs_power_reset_outputs(port_rows, blocks)
    if reset_outputs:
        if not performance_section or "| Power/clock owner | Reset output | Approved description | Source page |" not in performance_section.group(1):
            findings.append("drs_power_reset_outputs_missing")
        for output in reset_outputs:
            if not performance_section or "| " + " | ".join(output) + " |" not in performance_section.group(1) or list(output) not in docx_tables:
                findings.append(f"drs_power_reset_output_missing:{output[1]}")
    timing_section = re.search(r"(?ms)^### (?:\*\*)?4\.7 Clock and synchronization across domains[^\n]*\n(.*?)(?=^## (?:\*\*)?5\.)", markdown)
    snapshot_match = re.search(r"(?m)^Snapshot ID: (\S+)$", markdown)
    if snapshot_match:
        snapshot_rows = load_sqlite_snapshot_input(repo_root, "DRS", snapshot_id=snapshot_match.group(1)).rows
        clock_paths = _drs_clock_path_rows(snapshot_rows)
        clock_narrative = _drs_clock_section_summary(clock_paths)
        if (not timing_section or clock_narrative not in timing_section.group(1)
            or clock_narrative not in docx_text):
            findings.append("drs_clock_section_summary_missing")
        pmu_routes = _drs_power_clock_routes(clock_paths, blocks)
        if pmu_routes:
            if not performance_section or "| Source requirement | Source clock | Destination clock | Frequency | Clock gating |" not in performance_section.group(1):
                findings.append("drs_power_clock_table_missing")
            for path in pmu_routes:
                if not performance_section or _drs_clock_path_markdown_row(path) not in performance_section.group(1) or list(path) not in docx_tables:
                    findings.append(f"drs_power_clock_route_missing:{path[0]}")
        elif not performance_section or "Power/clock destination coverage: need clarification." not in performance_section.group(1):
            findings.append("drs_power_clock_coverage_missing")
        unresolved_routes = [path[0] for path in clock_paths if path[1] == "need clarification"]
        if unresolved_routes:
            boundary = "Clock-path endpoints requiring clarification: " + ", ".join(unresolved_routes) + "."
            if not performance_section or boundary not in performance_section.group(1) or boundary not in docx_text:
                findings.append("drs_power_clock_endpoint_boundary_missing")
        for source_id, source, target in _drs_sync_connection_rows(snapshot_rows, port_rows):
            if not any(source.startswith(block.name + ".") for block in blocks if "clock" in block.function.casefold()):
                continue
            statement = f"Reset connection {source_id}: {source} -> {target}; release/synchronization behavior: need clarification."
            if not performance_section or statement not in performance_section.group(1) or statement not in docx_text:
                findings.append(f"drs_power_reset_route_missing:{source_id}")
        if clock_paths:
            header = "| Source requirement | Source clock | Destination clock | Frequency | Clock gating |"
            if not timing_section or header not in timing_section.group(1) or ["Source requirement", "Source clock", "Destination clock", "Frequency", "Clock gating"] not in docx_tables:
                findings.append("drs_clock_path_table_missing")
            for path in clock_paths:
                if not timing_section or _drs_clock_path_markdown_row(path) not in timing_section.group(1) or list(path) not in docx_tables:
                    findings.append(f"drs_clock_path_missing:{path[0]}")
        elif not timing_section or "Clock distribution paths and clock-gating behavior: need clarification." not in timing_section.group(1):
            findings.append("drs_clock_path_boundary_missing")
        for source_id, source, target in _drs_sync_connection_rows(snapshot_rows, port_rows):
            boundary = (f"Reset/synchronization-labelled connection {source_id}: {source} -> {target}; "
                        "synchronization implementation: need clarification.")
            if not timing_section or boundary not in timing_section.group(1) or boundary not in docx_text:
                findings.append(f"drs_sync_connection_boundary_missing:{source_id}")
    else:
        findings.append("drs_clock_path_snapshot_missing")
    if not timing_section or (not _drs_has_synchronization_evidence(drs_statements)
                              and "Clock-domain crossing, reset-domain crossing, and measured interrupt response time: need clarification." not in timing_section.group(1)):
        findings.append("drs_synchronization_boundary_missing")
    if "This DRS covers digital subsystem behavior" in markdown or "System context is summarized to scope" in markdown:
        findings.append("drs_intro_generic_placeholder")
    for topic, rows in expected.items():
        heading = re.search(rf"(?m)^#{{2,3}}\s+(?:\*\*)?{re.escape(topic)}(?:\*\*)?\s*(?:\{{#[^}}]+\}})?\s*$", markdown)
        if not heading:
            findings.append(f"missing_drs_intro_section:{topic}")
            continue
        body = markdown[heading.end():]
        next_heading = re.search(r"(?m)^#{2,3}\s+", body)
        body = body[:next_heading.start()] if next_heading else body
        context_only = topic == "3. Top Level Overview"
        narrative = (_drs_clock_section_summary(_drs_power_clock_routes(snapshot_clock_paths, blocks))
                 if topic == DRS_INTRO_TOPICS[4][0] else
                 _drs_top_level_overview(rows) if topic == "3. Top Level Overview"
                 or topic in {item[0] for item in DRS_INTRO_TOPICS[:4]}
                     else _drs_section_interaction_summary(rows) if topic.startswith("7.")
                     else summarize_architecture_interactions(rows))
        has_interaction_table = context_only or topic == DRS_INTRO_TOPICS[4][0] or "| Source | Destination | Architectural exchange |" in body
        if topic == "3. Top Level Overview":
            if not body.strip():
                findings.append(f"drs_intro_overview_missing:{topic}")
        elif rows and ((topic != DRS_INTRO_TOPICS[0][0] and narrative not in body and not has_interaction_table) or not has_interaction_table):
            findings.append(f"drs_intro_summary_or_table_missing:{topic}")
        if rows and docx_text and topic != DRS_INTRO_TOPICS[0][0] and topic != "3. Top Level Overview" and not has_interaction_table and narrative not in docx_text:
            findings.append(f"drs_intro_summary_missing_from_docx:{topic}")
        for order, (source, target, exchange) in enumerate(rows, start=1):
            if not context_only and topic != DRS_INTRO_TOPICS[4][0] and f"| {source} | {target} | {exchange} |" not in body:
                findings.append(f"drs_intro_interaction_missing:{topic}:{order}")
            if not context_only and topic != DRS_INTRO_TOPICS[4][0] and docx_text and (source, target, exchange) not in docx_rows:
                findings.append(f"drs_intro_interaction_missing_from_docx:{topic}:{order}")
            matching = [row for row in intro_audit if row.get("topic") == topic and row.get("output_order") == str(order)]
            evidence = next((record for record in matrix_records if
                (source, target, exchange) in project_architecture_interactions([record.get("statement", "")])
            ), {})
            if (len(matching) != 1 or matching[0].get("statement") != f"{source} -> {target}: {exchange}"
                or matching[0].get("source") != evidence.get("source")
                or matching[0].get("source_evidence") != evidence.get("statement")):
                findings.append(f"drs_intro_provenance_mismatch:{topic}:{order}")
        if len([row for row in intro_audit if row.get("topic") == topic]) != len(rows):
            findings.append(f"drs_intro_audit_count_mismatch:{topic}")
    if re.search(r"(?m)^- Interaction:|Digital control behavior shall define|Register map behavior shall define|Performance requirements shall cover", markdown):
        findings.append("drs_intro_generic_or_raw_interaction")
    return findings


def _digital_focus_score(text: str) -> int:
    t = _statement_payload(text).lower()
    return sum(1 for token in DIGITAL_SYSTEM_TERMS if token in t)


def _analog_focus_score(text: str) -> int:
    t = _statement_payload(text).lower()
    return sum(1 for token in ANALOG_FOCUS_TERMS if token in t)


def _statement_payload(text: str) -> str:
    t = (text or "").strip()
    low = t.lower()
    prefix = "the digital subsystem shall satisfy the following behavior:"
    if low.startswith(prefix):
        t = t[len(prefix):].strip()
    t = re.sub(
        r"^\s*\[[A-Za-z][A-Za-z0-9_]*\d+\]\s+Requirement\s*:?\s*",
        "",
        t,
        flags=re.IGNORECASE,
    )
    t = re.sub(r"\s*\[[A-Za-z][A-Za-z0-9_]*\d+\]", "", t)
    if SOURCE_REQUIREMENT_IDS:
        source_id_pattern = "|".join(
            re.escape(source_id)
            for source_id in sorted(SOURCE_REQUIREMENT_IDS, key=len, reverse=True)
        )
        t = re.sub(rf"\b(?:{source_id_pattern})\b\s*:?", "", t)
    return _normalize_block_references(re.sub(r"\s+", " ", t.strip()))


def _reset_clock_payload(requirement: Requirement) -> str:
    authored_payload = _statement_payload(requirement.statement)
    if re.search(r"\b(?:Delay|Clock gating|F max):", authored_payload, flags=re.IGNORECASE):
        return authored_payload
    source_paths = re.findall(
        r"\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+\b",
        f"{requirement.source} {requirement.statement}",
    )
    unique_paths = list(dict.fromkeys(source_paths))
    if len(unique_paths) >= 2:
        payload = _statement_payload(requirement.statement)
        qualifiers = re.findall(r",\s*(?:with frequency|without clock gating|with clock gating)[^.]*", payload, flags=re.IGNORECASE)
        suffix = "".join(qualifiers)
        return f"The {unique_paths[0]} signal shall be connected to the {unique_paths[1]} signal{suffix}."
    payload = _statement_payload(requirement.statement)
    normalized_payload = re.sub(r"\s*_\s*", "_", payload)
    paths = re.findall(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+", normalized_payload)
    if len(paths) >= 2 and paths[0] != paths[1]:
        return f"The {paths[0]} signal shall be connected to the {paths[1]} signal."
    if re.search(r"\bwith(?:out)?\s+clock\s+gating\b", payload, flags=re.IGNORECASE):
        return payload

    payload = re.sub(
        r"\s+and\s+shall\s+have\s+a\s+frequency\s+of\s+(.+)$",
        r", with frequency \1",
        payload,
        flags=re.IGNORECASE,
    )
    match = re.match(r"^The\s+signal\s+(.+?)\s+shall\s+be\s+connected\s+to\s+(.+)$", payload, flags=re.IGNORECASE)
    if match:
        source_signal = match.group(1).strip()
        target_signal = match.group(2).strip().rstrip(".")
        return f"The {source_signal} signal shall be connected to the {target_signal} signal"
    return payload


def _is_user_facing_requirement(statement: str) -> bool:
    low = (statement or "").lower()
    return (
        "the user shall" in low
        or "user shall" in low
        or "external i2c/spi" in low
        or "external i2c" in low
        or "external spi" in low
    )


def _has_explicit_source_parent(source: str) -> bool:
    return bool(re.search(r"\(under\s+Section\s+", source or "", flags=re.IGNORECASE))


def _user_specific_group_label(source: str) -> str:
    """Derive a human-readable subgroup label from Stage 1 source metadata."""
    src = (source or "").strip()
    if not src:
        return "Unclear context"

    primary = src.split(", paragraph", 1)[0].strip()
    primary = re.sub(r"\s*\(page\s*\d+\)\s*$", "", primary, flags=re.IGNORECASE).strip()

    match = re.match(r"^Section\s+[0-9A-Za-z_.-]+\s+(.*)$", primary, flags=re.IGNORECASE)
    if match:
        label = match.group(1).strip(" -:\t")
        if label:
            return label

    if primary:
        return primary
    return "Unclear context"


def _non_block_context_label(source: str) -> str:
    """Group non-block requirements under their source paragraph name."""
    return source_parent_title(source)


def _display_non_block_source(row: Dict[str, str]) -> str:
    source_paragraph = (row.get("Source Paragraph") or "").strip()
    list_item_label = re.match(
        r"^Section\s+\d+\s+(?P<label>.+?\s+routine),\s+paragraph\s+\d+\s+\(page\s+\d+\)$",
        source_paragraph,
        flags=re.IGNORECASE,
    )
    if list_item_label and "(under section" not in source_paragraph.lower():
        return "Unheaded source context; OCR numbered-list label is not a source paragraph"
    return source_paragraph or "Unknown"


DEDICATED_SOURCE_TERMS = (
    "bist", "scan", "debug", "dft", "test mode", "test", "power-up",
    "power up", "power-down", "power down", "boot", "configuration", "pad mux",
)


def _dedicated_source_label(requirement: Requirement) -> str:
    source = (requirement.source or "").strip()
    source_lower = source.lower()
    if not source:
        return ""
    if not _has_explicit_source_parent(source):
        return ""
    if not any(term in source_lower for term in DEDICATED_SOURCE_TERMS):
        return ""
    parent_match = re.search(
        r"\bunder\s+Section\s+[0-9A-Za-z_.-]+\s+(.+?)(?:,\s*paragraph|\s*\(page\s*\d+\)|$)",
        source,
        flags=re.IGNORECASE,
    )
    if parent_match:
        return parent_match.group(1).strip(" .-:()\t")
    if "pad mux" in source.lower():
        return "PAD Mux"
    primary = source.split(", paragraph", 1)[0].strip()
    match = re.match(r"^Section\s+[0-9A-Za-z_.-]+\s+(.*)$", primary, flags=re.IGNORECASE)
    return (match.group(1) if match else primary).strip(" -:\t") or primary


def _split_source_list(payload: str) -> Tuple[str, List[str]]:
    normalized = re.sub(r"\s*[•●]\s*", "\n• ", payload)
    marker = re.compile(r"(?:^|\s)(?P<mark>•)\s+(?=[A-Za-z])")
    matches = list(marker.finditer(normalized))
    if not matches:
        return normalized.strip(), []
    lead = normalized[:matches[0].start()].strip()
    items: List[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(normalized)
        item = normalized[match.start():end].strip()
        if item:
            if item.startswith("• "):
                item = "- " + item[2:]
            items.append(item)
    return lead, items


def _source_body_lines(requirement: Requirement) -> List[str]:
    payload = _statement_payload(requirement.statement).strip()
    payload = re.sub(r"\s+•\s*", "\n- ", payload)
    payload = re.sub(r"(?<!^)\s+(?=\d+(?:\.\d+)+\s+[A-Z])", "\n", payload)
    payload = re.sub(r":\s+(?=-\s+)", ":\n", payload)
    rendered: List[str] = []
    for line in payload.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        is_heading = bool(re.match(r"^\d+(?:\.\d+)+\s+[^:]+:\s*$", cleaned))
        is_item = cleaned.startswith(("- ", "* ", "+ "))
        if is_heading:
            if rendered and rendered[-1].strip():
                rendered.append("")
            rendered.append(cleaned)
        elif is_item:
            if rendered and rendered[-1].strip() and not rendered[-1].startswith(("- ", "* ", "+ ")):
                rendered.append("")
            rendered.append(cleaned)
        elif rendered and rendered[-1].startswith(("- ", "* ", "+ ")):
            rendered[-1] = rendered[-1].rstrip() + " " + cleaned
        else:
            rendered.append(cleaned)
    return rendered or [payload]


def _is_digital_relevant(
    req: Requirement,
    req_to_block: Dict[str, str],
    digital_blocks: Set[str],
    allocations: Optional[Dict[str, Dict[str, str]]] = None,
) -> bool:
    if allocations is not None and req.source_req_id in allocations:
        allocation = allocations[req.source_req_id]
        targets = {
            value.strip()
            for field in ("required_downstream_targets", "allowed_contextual_targets")
            for value in allocation.get(field, "").split(";")
            if value.strip()
        }
        owning_target = allocation.get("owning_target", "").strip()
        if owning_target and owning_target != "DRS" and "DRS" not in targets:
            return False
    if _dedicated_source_label(req):
        return True
    mapped = req_to_block.get(req.source_req_id, "")
    tokens = [t.strip() for t in mapped.split(";") if t.strip()]
    has_digital_owner = any(token in digital_blocks for token in tokens)

    digital_score = _digital_focus_score(req.statement)
    analog_score = _analog_focus_score(req.statement)

    # Explicit top-level classification is authoritative: System belongs to SRS,
    # Analog belongs to ARS, and only Digital belongs to DRS.
    if req.domain == "DIG":
        if has_digital_owner:
            return True
        return digital_score >= analog_score

    if req.domain in {"SYS", "ANA"}:
        return False

    if req.domain == "XDN":
        if has_digital_owner:
            return True
        return digital_score >= max(1, analog_score)

    if req.domain == "ANA":
        return has_digital_owner and digital_score >= 1 and digital_score >= analog_score

    # Unknown domain is admitted only with explicit digital ownership.
    return has_digital_owner


def _split_blocks(mapped_blocks: str) -> List[str]:
    return [canonical_human_label(token) for token in (mapped_blocks or "").split(";") if token.strip()]


def _function_terms(text: str) -> Set[str]:
    terms = set(re.findall(r"[a-z][a-z0-9]+", (text or "").lower()))
    return {
        term[:-1] if term.endswith("s") and len(term) > 4 else term
        for term in terms
        if term not in FUNCTION_STOP_WORDS and len(term) > 2
    }


def _function_supports_requirement(requirement: Requirement, block: BlockInfo) -> bool:
    requirement_terms = _function_terms(_statement_payload(requirement.statement))
    function_terms = _function_terms(block.function)
    return bool(requirement_terms & function_terms)


def _is_reset_clock_table_requirement(requirement: Requirement) -> bool:
    metadata = " ".join(
        (
            requirement.derivation_kind,
            requirement.evidence_type,
            requirement.notes,
            requirement.source,
            requirement.statement,
        )
    ).lower()
    if (
        "derived-from-structure" not in metadata
        and "structural_table_derivation" not in metadata
        and "table_line_info" not in metadata
    ):
        return False
    if "reset" in metadata or "clock" in metadata:
        return True
    structural_paths = re.findall(r"\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+\b", metadata)
    return "table_line_info" in metadata and len(set(structural_paths)) >= 2


def _is_interrupt_table_requirement(requirement: Requirement) -> bool:
    metadata = " ".join(
        (
            requirement.derivation_kind,
            requirement.evidence_type,
            requirement.notes,
            requirement.source,
            requirement.statement,
        )
    ).lower()
    return "interrupt_table_connection" in metadata and "derived-from-structure" in metadata


def _reset_clock_owner(block_by_name: Dict[str, BlockInfo]) -> str:
    ranked: List[Tuple[int, str]] = []
    for block, info in block_by_name.items():
        text = f"{block} {info.function}".lower()
        if "clock" not in text and "reset" not in text:
            continue
        score = sum(
            1
            for term in ("pmu", "power", "clock", "reset", "por", "ldo", "sequence", "sequencing", "release", "ready")
            if term in text
        )
        if score:
            ranked.append((score, block))

    if not ranked:
        return ""
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return ranked[0][1]


def _interrupt_owner(block_by_name: Dict[str, BlockInfo]) -> str:
    ranked: List[Tuple[int, str]] = []
    for block, info in block_by_name.items():
        text = f"{block} {info.function}".lower()
        score = sum(1 for term in ("processor", "cpu", "microcontroller", "controller", "interrupt", "irq") if term in text)
        if score:
            ranked.append((score, block))

    if not ranked:
        return ""
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return ranked[0][1]


def _resolve_digital_owners(
    requirement: Requirement,
    mapped_blocks: str,
    block_by_name: Dict[str, BlockInfo],
    digital_blocks: Set[str],
) -> List[str]:
    explicit_blocks = [
        name
        for name in _split_blocks(mapped_blocks)
        if name in digital_blocks
        and name != "Unassigned"
        and name in block_by_name
    ]
    return explicit_blocks or [
        name
        for name in _split_blocks(mapped_blocks)
        if name in digital_blocks
        and name != "Unassigned"
        and name in block_by_name
        and _function_supports_requirement(requirement, block_by_name[name])
    ]


def _map_requirements_to_digital_blocks(
    requirements: List[Requirement],
    req_to_block: Dict[str, str],
    block_by_name: Dict[str, BlockInfo],
    digital_blocks: Set[str],
    matrix_source_owners: Dict[str, str],
) -> Tuple[Dict[str, List[Requirement]], List[Requirement]]:
    by_block: Dict[str, List[Requirement]] = defaultdict(list)
    unmapped: List[Requirement] = []
    reset_clock_owner = _reset_clock_owner(block_by_name)
    interrupt_owner = _interrupt_owner(block_by_name)

    for req in requirements:
        if _dedicated_source_label(req):
            unmapped.append(req)
            continue
        matrix_owner = matrix_source_owners.get(req.source_req_id, "")
        if matrix_owner and matrix_owner in digital_blocks and matrix_owner in block_by_name:
            matched_blocks = [matrix_owner]
        elif req.source_section_owner in digital_blocks and req.source_section_owner in block_by_name:
            matched_blocks = [req.source_section_owner]
        elif reset_clock_owner and _is_reset_clock_table_requirement(req) and reset_clock_owner in digital_blocks:
            matched_blocks = [reset_clock_owner]
        elif interrupt_owner and _is_interrupt_table_requirement(req) and interrupt_owner in digital_blocks:
            matched_blocks = [interrupt_owner]
        else:
            matched_blocks = _resolve_digital_owners(
                req,
                req_to_block.get(req.source_req_id, ""),
                block_by_name,
                digital_blocks,
            )

        if matched_blocks:
            for block_name in matched_blocks:
                by_block[block_name].append(req)
        else:
            unmapped.append(req)

    return by_block, unmapped


def _atomic_block_statement(
    block_name: str,
    requirement: Requirement,
    source_requirement_ids: Set[str],
) -> str:
    payload = (
        _reset_clock_payload(requirement)
        if _is_reset_clock_table_requirement(requirement)
        else _statement_payload(requirement.statement)
    )
    source_ids_pattern = "|".join(
        re.escape(source_id)
        for source_id in sorted(source_requirement_ids, key=len, reverse=True)
        if source_id
    )
    if source_ids_pattern:
        payload = re.sub(rf"\b(?:{source_ids_pattern})\b", "", payload).strip()
    if payload:
        lead, list_items = _split_source_list(payload.rstrip("."))
        rendered = [f"The {block_name} block shall implement: {lead}."]
        if list_items:
            rendered.append("")
            for item in list_items:
                if re.match(r"^\d+(?:\.\d+)+\s+", item) and rendered[-1].strip():
                    rendered.append("")
                rendered.append(item)
        return "\n".join(rendered)
    return f"The {block_name} block shall implement: behavior defined by mapped upstream requirement evidence."


def _connection_matrix_statement(
    block_name: str,
    requirement: Requirement,
    connection_matrix_upstream: Dict[str, Tuple[str, str]],
    source_requirement_ids: Set[str],
) -> str:
    if requirement.source_req_id in connection_matrix_upstream:
        edge_statement = connection_matrix_upstream[requirement.source_req_id][1]
        destination = edge_statement.rsplit(" to ", 1)[-1].rstrip(".")
        return f"The {block_name} block shall implement: connection to {destination}."
    return _atomic_block_statement(block_name, requirement, source_requirement_ids)


def _condition_owner_names(requirement: Requirement, block_requirements: Dict[str, List[Requirement]]) -> List[str]:
    return [
        block_name
        for block_name, mapped_requirements in block_requirements.items()
        if any(item.source_req_id == requirement.source_req_id for item in mapped_requirements)
    ]


def _detailed_timing_bullets(
    requirements: List[Requirement],
    block_requirements: Dict[str, List[Requirement]],
    srs_upstream_map: Dict[str, str],
) -> List[str]:
    bullets: List[str] = []
    for requirement in requirements:
        lower = requirement.statement.casefold()
        topics = []
        if "synchron" in lower or "clock domain" in lower:
            topics.append("clock-domain synchronization")
        if "gating" in lower or "gated" in lower:
            topics.append("clock gating")
        if "reset" in lower or "recovery" in lower:
            topics.append("reset/recovery")
        if "irq" in lower or "interrupt" in lower or "latency" in lower:
            topics.append("interrupt response/latency")
        owners = ", ".join(_condition_owner_names(requirement, block_requirements)) or "the source and destination blocks"
        topic = ", ".join(topics).capitalize() if topics else "Timing behavior"
        bullets.append(
            f"- {topic} applies to {owners}; the involved blocks shall apply the approved condition and response. "
            f"Covers: {_upstream_id(requirement.source_req_id, srs_upstream_map)}"
        )
    return bullets


def _detailed_data_path_bullets(
    requirements: List[Requirement],
    block_requirements: Dict[str, List[Requirement]],
    srs_upstream_map: Dict[str, str],
) -> List[str]:
    bullets: List[str] = []
    for requirement in requirements:
        lower = requirement.statement.casefold()
        topics = []
        evidence_topics = []
        if "overflow" in lower:
            evidence_topics.append("overflow")
        if "underflow" in lower:
            evidence_topics.append("underflow")
        if "backpressure" in lower:
            evidence_topics.append("backpressure")
        if "throughput" in lower or "rate" in lower:
            evidence_topics.append("throughput/data rate")
        if "fifo" in lower or "buffer" in lower or "queue" in lower:
            evidence_topics.append("buffering")
        owners = ", ".join(_condition_owner_names(requirement, block_requirements)) or "the producing and consuming blocks"
        topic = ", ".join(dict.fromkeys(evidence_topics)).capitalize() if evidence_topics else "Data-path behavior"
        statement = _descriptive_text(requirement.statement)
        bullets.append(
            f"- {topic}: {statement} Involved blocks: {owners}. "
            f"Covers: {_upstream_id(requirement.source_req_id, srs_upstream_map)}"
        )
    return bullets


def _build_drs_id_map(requirements: List[Requirement]) -> Dict[str, str]:
    authored_counter = 0
    out: Dict[str, str] = {}
    for req in requirements:
        authored_counter += 1
        out[req.source_req_id] = f"DRS-REQ-{authored_counter:03d}"
    return out


def _write_traceability_csv(
    output_path: Path,
    requirements: List[Requirement],
    drs_id_map: Dict[str, str],
    req_to_block: Dict[str, str],
    allocation_by_source: Dict[str, Dict[str, str]],
    snapshot_id: str,
) -> Tuple[int, int]:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    full_traceability = 0
    unassigned = 0

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "drs_req_id",
                "source_req_id",
                "domain",
                "requirement_statement",
                "owning_block",
                "source_artifact",
                "verification_method",
                "acceptance_criteria",
                "status",
                "notes",
                "snapshot_id",
                "allocation_class",
                "owning_target",
                "lineage_mode",
                "source_origin_req_ids",
                "hierarchy_parent_req_ids",
                "owning_domain",
            ]
        )

        for req in requirements:
            owning_block = req_to_block.get(req.source_req_id, "Unassigned")
            if owning_block == "Unassigned":
                unassigned += 1
            else:
                full_traceability += 1

            writer.writerow(
                [
                    drs_id_map[req.source_req_id],
                    req.source_req_id,
                    req.domain,
                    req.statement,
                    owning_block,
                    "artifacts/stage1_requirements/requirements_summary.csv",
                    _verification_method(req.requirement_type, req.domain),
                    _acceptance_criteria(req.value_range_condition),
                    "draft",
                    f"source={req.source}",
                    snapshot_id,
                    allocation_by_source[req.source_req_id].get("allocation_class", ""),
                    allocation_by_source[req.source_req_id].get("owning_target", ""),
                    allocation_by_source[req.source_req_id].get("lineage_mode", ""),
                    allocation_by_source[req.source_req_id].get("source_origin_req_ids", ""),
                    allocation_by_source[req.source_req_id].get("hierarchy_parent_req_ids", ""),
                    allocation_by_source[req.source_req_id].get("owning_domain", ""),
                ]
            )

    return full_traceability, unassigned


def _write_drs_markdown(
    output_path: Path,
    source_spec: str,
    project_name: str,
    document_author: str,
    snapshot_id: str,
    document_version: str,
    requirements: List[Requirement],
    drs_id_map: Dict[str, str],
    block_inventory: List[BlockInfo],
    stage1_block_descriptions: Dict[str, List[Dict[str, str]]],
    interface_rows: List[Dict[str, str]],
    source_interface_tables: Dict[str, List[Tuple[str, str, str]]],
    source_port_rows: List[Dict[str, str]],
    block_requirements: Dict[str, List[Requirement]],
    unmapped_requirements: List[Requirement],
    top_digital_records: List[Dict[str, str]],
    non_block_context_rows: List[Dict[str, str]],
    crosscheck_decision: str,
    missing_inputs: List[Path],
    requirements_only_mode: bool,
    connection_matrix_upstream: Dict[str, Tuple[str, str]],
    source_requirement_ids: Set[str],
    srs_upstream_map: Dict[str, str],
    clock_path_rows: List[Tuple[str, str, str, str, str]],
    sync_connection_rows: List[Tuple[str, str, str]],
    document_contract: dict,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    def _anchor_slug(text: str) -> str:
        slug = re.sub(r"[^a-z0-9\s-]", "", text.lower())
        return re.sub(r"\s+", "-", slug).strip("-") or "dedicated-source-section"

    grouped: Dict[str, List[Requirement]] = defaultdict(list)
    for req in requirements:
        grouped[req.domain].append(req)

    digital_block_rows = _drs_descriptive_blocks(block_inventory, interface_rows, source_interface_tables)
    digital_summary_records = [
        record
        for record in top_digital_records
        if record.get("evidence_kind", "").casefold() != "power_domain"
        and record.get("record_type", "").casefold() != "power_domain"
        and "power-domain" not in record.get("source", "").casefold()
        and "included block(s):" not in record.get("statement", "").casefold()
    ]
    source_capabilities = [
        record["statement"] for record in digital_summary_records
        if record.get("record_type") == "architecture_capability"
    ]
    architecture_entries = [record.get("statement", "") for record in digital_summary_records]
    architecture_interactions = project_architecture_interactions(architecture_entries)
    intro_rows = _drs_intro_rows(architecture_entries)

    def append_interaction_context(rows: List[Tuple[str, str, str]], *, include_summary: bool = True) -> None:
        if not rows:
            return
        if include_summary:
            lines.append(summarize_architecture_interactions(rows))
            lines.append("")
        lines.append("| Source | Destination | Architectural exchange |")
        lines.append("|---|---|---|")
        for source, target, exchange in rows:
            lines.append(f"| {source} | {target} | {exchange} |")
        lines.append("")

    lines: List[str] = []
    lines.append("# Digital Requirements Specification")
    lines.append("")
    lines.append(f"## {project_name}")
    lines.append("")
    lines.append(f"Author: {document_author}")
    lines.append("")
    lines.append(f"Date: {today}")
    lines.append(f"Snapshot ID: {snapshot_id}")
    lines.append(f"Source specification: {source_spec}")
    lines.append("")
    lines.append("## 0. Document Navigation")
    lines.append("")
    lines.append("### 0.1 Table of contents")
    marker_toc = "__AUTO_TOC__"
    marker_nav = "__AUTO_NAV__"
    lines.append(marker_toc)
    lines.append("")

    lines.append("### 0.2 Internal index for paragraphs and pages")
    lines.append("#### Table 3. Section navigation index")
    lines.append("| Section | Paragraph anchor | Internal link | Page (rendered PDF) |")
    lines.append("|---|---|---|---|")
    lines.append(marker_nav)
    lines.append("")

    lines.append("### 0.3 Document control")
    lines.append("#### Table 1. Version history")
    lines.append("| Version | Date | Description | Author |")
    lines.append("|---|---|---|---|")
    lines.append(f"| {document_version} | {today} | Snapshot {snapshot_id} DRS baseline generated from Stage 1 and Stage 2 artifacts | {document_author} |")
    lines.append("")

    lines.append("#### Table 2. Reference documents")
    lines.append("| Doc name | Version | Author |")
    lines.append("|---|---|---|")
    if not requirements_only_mode:
        lines.append(f"| artifacts/stage4_ars/analog_requirements_specification.md | {GENERATED_SPEC_VERSION} | ARS Gen Spec Agent |")
    lines.append(f"| artifacts/stage1_requirements/requirements_summary.csv | {GENERATED_SPEC_VERSION} | Requirements Extraction Agent |")
    lines.append(f"| artifacts/stage2_mirco_arc/micro_architecture_report.md | {GENERATED_SPEC_VERSION} | Micro-Architectural Analysis Agent |")
    lines.append(f"| artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv | {GENERATED_SPEC_VERSION} | Micro-Architectural Analysis Agent |")
    lines.append(f"| templates/DRS_gen_AI_template_prompt.md | {GENERATED_SPEC_VERSION} | Project template maintainers |")
    lines.append("")

    lines.append("#### Table 6. Category convention")
    lines.append("| Category | Naming rule / prefix | Scope | Notes / example |")
    lines.append("|---|---|---|---|")
    lines.append("| Digital authored requirement | DRS-REQ-xxx | Project-specific DRS atomic entries | Covers one upstream requirement per row |")
    lines.append("| Source digital/system/cross-domain requirement | source_req_id | Stage 1 source requirement catalog | Linked to authored SRS upstream ID |")
    lines.append("| DRS upstream reference in Covers | SRS-REQ-xxx | Authored SRS requirement catalog | Required for every DRS authored requirement |")
    lines.append("")

    lines.append("### 0.4 Table of tables")
    lines.append("| Table | Title | Link |")
    lines.append("|---|---|---|")
    lines.append("| Table 1 | Version history | [Go to Table 1](#table-1-version-history) |")
    lines.append("| Table 2 | Reference documents | [Go to Table 2](#table-2-reference-documents) |")
    lines.append("| Table 3 | Section navigation index | [Go to Table 3](#table-3-section-navigation-index) |")
    lines.append("| Table 6 | Category convention | [Go to Table 6](#table-6-category-convention) |")
    lines.append("")

    lines.append("## 1. Introduction")
    lines.append("")
    lines.append("### 1.1 Purpose")
    lines.append(f"This specification describes the digital integration of {', '.join(block.name for block in digital_block_rows)}." if digital_block_rows else "This specification records digital integration requirements.")
    lines.append("")
    lines.append("### 1.2 Scope")
    lines.append("This specification covers digital integration behavior and the relationships between the digital subsystem and its interfaces. Block-local implementation remains outside this integration scope.")
    lines.append("")
    lines.append("### 1.3 Intended audience")
    lines.append("System architects, digital design, firmware, validation, and verification stakeholders.")
    lines.append("")
    lines.append("### 1.4 References")
    lines.append("Reference files are listed in Table 2. Reference documents.")
    lines.append("")

    lines.append("## 2. Definitions and terminology")
    lines.append("Source and destination labels in the architecture tables retain their integration-evidence meanings; the block list distinguishes concrete digital blocks from other interaction endpoints.")
    lines.append("")
    lines.extend(drs_conventions_markdown(document_contract))

    lines.append("## 3. Top Level Overview")
    lines.append(_drs_top_level_overview(architecture_interactions, source_capabilities))
    lines.append("")
    lines.append("### 3.1 Digital Main Functions")
    lines.append("")
    for block in digital_block_rows:
        lines.append(f"#### {block.name}")
        lines.append(_drs_function_summary(
            block,
            [req.statement for req in requirements],
            stage1_block_descriptions.get(block.name, []),
        ))
        lines.append("")
    digital_topics = DESCRIPTIVE_DIGITAL_TOPIC_SPECS
    digital_summary = organize_descriptive_topics(digital_summary_records, digital_topics)
    shared_resource_entries = _shared_resource_access_records(digital_summary_records)
    if shared_resource_entries:
        arbitration_entries = digital_summary.setdefault("Arbitration and control", [])
        for entry in shared_resource_entries:
            if entry not in arbitration_entries:
                arbitration_entries.append(entry)
    combined_topic = "Arbitration, control, and shared resources"
    combined_entries = list(dict.fromkeys(digital_summary.get("Arbitration and control", []) + digital_summary.get("Shared digital resources", [])))
    if combined_entries:
        digital_summary = {
            (combined_topic if topic == "Arbitration and control" else topic): (combined_entries if topic == "Arbitration and control" else entries)
            for topic, entries in digital_summary.items() if topic != "Shared digital resources"
        }
    if digital_summary:
        for topic, entries in digital_summary.items():
            topic_rows = project_architecture_interactions(entries)
            if topic_rows:
                lines.append(f"#### {topic}")
                if topic == "Power and clock islands":
                    lines.append(_drs_clock_section_summary(_drs_power_clock_routes(clock_path_rows, digital_block_rows)))
                    lines.append(_drs_section_interaction_summary(topic_rows))
                else:
                    narrative = _drs_section_interaction_summary(topic_rows)
                    if topic == "Digital processing blocks":
                        narrative = _drs_processing_summary(digital_block_rows, topic_rows)
                    lines.append(narrative)
                if topic == combined_topic:
                    lines.append("Priority between simultaneous resource requesters: need clarification.")
                lines.append("")
                if topic != "Power and clock islands":
                    append_interaction_context(topic_rows, include_summary=False)
    else:
        lines.append("No descriptive digital functions were identified in the approved architecture context.")
        lines.append("")
    low_power_grouped, _low_power_audit = assemble_low_power_descriptive(
        top_digital_records,
        repo_root=_resolve_repo_root(),
        profile="drs",
    )
    power_domain_rows = _drs_power_domain_rows([
        record for record in top_digital_records
        if record.get("statement", "") in low_power_grouped.get("Power-domain architecture", [])
    ])
    for topic, entries in low_power_grouped.items():
        power_table_rendered = False
        if topic == "Power-domain architecture" and power_domain_rows:
            lines.append(f"#### {topic}")
            domain_groups: Dict[Tuple[str, str], List[str]] = defaultdict(list)
            for name, domain_type, control, _ in power_domain_rows:
                domain_groups[(domain_type, control)].append(name)
            for (domain_type, control), names in domain_groups.items():
                label = "domain" if len(names) == 1 else "domains"
                action = "supports" if len(names) == 1 else "support"
                lines.append(f"The {domain_type.lower()} {label} {', '.join(names)} {action} digital operation under {control} control. "
                             + " ".join(_drs_domain_function_sentence(name, function)
                                        for name, _, _, function in power_domain_rows if name in names))
            lines.append("")
            lines.append("| Domain | Type | Control | Function |")
            lines.append("|---|---|---|---|")
            for name, domain_type, control, function in power_domain_rows:
                lines.append(f"| {name} | {domain_type} | {control} | {function} |")
            lines.append("")
            entries = [entry for entry in entries if not any(entry.startswith(name + ":") for name, _, _, _ in power_domain_rows)]
            power_table_rendered = True
            if not entries:
                continue
        context = [_descriptive_text(entry) for entry in entries if _descriptive_text(entry)]
        context = [entry for entry in context if not entry.casefold().startswith("this document paragraph describes")
               and not re.search(r":\s*[•-]\s+", entry)]
        interaction_rows = project_architecture_interactions(context)
        interface_rows_for_topic = project_architecture_interfaces(context)
        other_context = [entry for entry in context if not project_architecture_interactions([entry])
                         and not project_architecture_interfaces([entry])]
        if not interaction_rows and not interface_rows_for_topic and not other_context:
            continue
        if not power_table_rendered:
            lines.append(f"#### {topic}")
        if interaction_rows:
            if topic == "Sequencing and domain control":
                role = _drs_topic_narrative("Power and clock islands", digital_block_rows)
                if role != "need clarification":
                    lines.append(role)
                lines.append(_drs_clock_section_summary(_drs_power_clock_routes(clock_path_rows, digital_block_rows)))
                lines.append(_drs_section_interaction_summary(interaction_rows))
                lines.append("Domain transition ordering and reset-release dependencies: need clarification.")
                lines.append("")
            else:
                lines.append(_drs_section_interaction_summary(interaction_rows))
                append_interaction_context(interaction_rows, include_summary=False)
        if interface_rows_for_topic:
            lines.append(" ".join(f"{owner} uses {interface} for {purpose[:1].lower() + purpose[1:]}."
                                  for interface, owner, purpose in interface_rows_for_topic))
            lines.append("| Interface | Owner | Function |")
            lines.append("|---|---|---|")
            for interface, owner, purpose in interface_rows_for_topic:
                lines.append(f"| {interface} | {owner} | {purpose} |")
            lines.append("")
        for entry in other_context:
            domain_description = re.fullmatch(r"(.+?): Domain that (.+)", entry)
            lines.append(f"The {domain_description.group(1)} is a domain that {domain_description.group(2)}" if domain_description else entry)
        lines.append("")

    lines.append("## 4. Digital requirements")
    lines.append("")
    lines.append("Digital integration paths and their authored requirements are distinguished below from block-local behavior.")
    if unmapped_requirements:
        lines.append("Residual digital-relevant requirements are captured in the requirement catalog with SRS upstream Covers links.")
    else:
        lines.append("All selected digital-relevant requirements are mapped to at least one digital block section.")
    lines.append("")

    lines.append("### 4.1 Digital block list")
    if digital_block_rows:
        lines.append("The digital blocks carry the following functions and architectural exchanges:")
        lines.append("")
        lines.append("| Block | Role | Architectural relationship |")
        lines.append("|---|---|---|")
        for block in digital_block_rows:
            role = (_drs_function_summary(block, [req.statement for req in requirements])
                    if re.search(r"\b(?:represent|described by .* evidence)\b", block.function, re.I) else block.function)
            lines.append(f"| {block.name} | {role} | {_drs_block_relationships(block.name, architecture_interactions)} |")
    else:
        lines.append("No digital blocks are included in this document.")
    lines.append("")

    lines.append("### 4.2 Arbitration, control, and shared resources")
    lines.append(_drs_section_interaction_summary(intro_rows[DRS_INTRO_TOPICS[0][0]]))
    facet_rows = _drs_shared_facet_rows(digital_block_rows, intro_rows[DRS_INTRO_TOPICS[0][0]])
    for facet, evidence in sorted(facet_rows, key=lambda row: row[1] == "need clarification"):
        lines.append(f"{facet}: {evidence}")
    lines.append("Priority between simultaneous resource requesters: need clarification.")
    lines.append("")
    append_interaction_context(intro_rows[DRS_INTRO_TOPICS[0][0]], include_summary=False)
    lines.append("")

    lines.append("### 4.3 Register and configuration requirements")
    lines.append(_drs_section_interaction_summary(intro_rows[DRS_INTRO_TOPICS[1][0]]))
    lines.append("")
    append_interaction_context(intro_rows[DRS_INTRO_TOPICS[1][0]], include_summary=False)
    lines.append("")

    lines.append("### 4.4 Interface and communication requirements")
    lines.append(_drs_section_interaction_summary(intro_rows[DRS_INTRO_TOPICS[2][0]]))
    lines.append("")
    append_interaction_context(intro_rows[DRS_INTRO_TOPICS[2][0]], include_summary=False)
    lines.append("")

    lines.append("### 4.5 Data-path and buffering requirements")
    lines.append(_drs_section_interaction_summary(intro_rows[DRS_INTRO_TOPICS[3][0]]))
    lines.append("")
    append_interaction_context(intro_rows[DRS_INTRO_TOPICS[3][0]], include_summary=False)
    lines.append("")

    lines.append("### 4.6 Digital performance requirements")
    lines.append(_drs_clock_section_summary(_drs_power_clock_routes(clock_path_rows, digital_block_rows)))
    lines.append("Measured latency and cross-domain synchronization behavior: need clarification.")
    lines.append("")
    power_clock_routes = _drs_power_clock_routes(clock_path_rows, digital_block_rows)
    if power_clock_routes:
        lines.append("Clock distribution:")
        lines.append("")
        lines.append("| Source requirement | Source clock | Destination clock | Frequency | Clock gating |")
        lines.append("|---|---|---|---|---|")
        for path in power_clock_routes:
            lines.append(_drs_clock_path_markdown_row(path))
        lines.append("")
    else:
        lines.append("Power/clock destination coverage: need clarification.")
    unresolved_routes = [path[0] for path in clock_path_rows if path[1] == "need clarification"]
    if unresolved_routes:
        lines.append("Clock-path endpoints requiring clarification: " + ", ".join(unresolved_routes) + ".")
    reset_outputs = _drs_power_reset_outputs(source_port_rows, digital_block_rows)
    if reset_outputs:
        lines.append("Reset outputs:")
        lines.append("")
        lines.append("| Power/clock owner | Reset output | Approved description | Source page |")
        lines.append("|---|---|---|---|")
        for owner, port, description, page in reset_outputs:
            lines.append(f"| {owner} | {port} | {description} | {page} |")
        lines.append("")
    else:
        lines.append("Reset-output destinations: need clarification.")
    for source_id, source, target in sync_connection_rows:
        if any(source.startswith(block.name + ".") for block in digital_block_rows if "clock" in block.function.casefold()):
            lines.append(f"Reset connection {source_id}: {source} -> {target}; release/synchronization behavior: need clarification.")
    lines.append("")

    timing_requirements = [
        req for req in requirements
        if re.search(r"\b(?:clock\s+domain|synchron(?:ize|ized|ization)|clock\s+gating|gated|irq|interrupt|latency|response\s+time|recovery)\b", req.statement, re.IGNORECASE)
    ]
    lines.append("### 4.7 Clock and synchronization across domains")
    lines.append(_drs_clock_section_summary(clock_path_rows))
    if clock_path_rows:
        lines.append("Clock distribution:")
        lines.append("")
        lines.append("| Source requirement | Source clock | Destination clock | Frequency | Clock gating |")
        lines.append("|---|---|---|---|---|")
        for path in clock_path_rows:
            lines.append(_drs_clock_path_markdown_row(path))
        lines.append("")
    else:
        lines.append("Clock distribution paths and clock-gating behavior: need clarification.")
    for source_id, source, target in sync_connection_rows:
        lines.append(f"Reset/synchronization-labelled connection {source_id}: {source} -> {target}; synchronization implementation: need clarification.")
    wake_up_requirements = [req for req in timing_requirements if re.search(r"\bwake up\b.*\binterrupt\b", req.statement, re.I)]
    wake_up_blocks = [block.name for block in digital_block_rows if any(
        re.search(rf"\bwake up the {re.escape(block.name)}\b", req.statement, re.I) for req in wake_up_requirements
    )]
    if wake_up_blocks:
        lines.append("Interrupt-triggered wake-up is specified for " + ", ".join(wake_up_blocks) + ".")
    if not _drs_has_synchronization_evidence([req.statement for req in requirements]):
        lines.append("Clock-domain crossing, reset-domain crossing, and measured interrupt response time: need clarification.")
    if timing_requirements:
        lines.append("")
        lines.append("| Timing focus | Source requirement | Upstream reference |")
        lines.append("|---|---|---|")
        for requirement in timing_requirements:
            statement = requirement.statement.casefold()
            focus = "Interrupt status or wake-up" if re.search(r"irq|interrupt", statement) else (
                "Clock or synchronization" if re.search(r"clock|synchron|gated", statement) else "Recovery or latency"
            )
            lines.append(f"| {focus} | {requirement.source_req_id} | {_upstream_id(requirement.source_req_id, srs_upstream_map)} |")
        lines.append("")
    lines.append("")

    lines.append("## 5. Validation and qualification requirements")
    lines.append("- Verification shall combine inspection, analysis, and test with measurable acceptance criteria.")
    lines.append("")

    lines.append("## 6. Requirement identification and traceability")
    lines.append("### 6.1 Numbering convention")
    lines.append("DRS authored requirements use DRS-REQ-### numbering. Source requirements retain their original IDs and are referenced through Covers linkage.")
    lines.append("")
    lines.append("### 6.2 Traceability contract")
    lines.append("DRS requirement catalog entries include statement only; full traceability details are maintained in artifacts/stage5_drs/drs_traceability_matrix.csv.")
    lines.append("")

    lines.append("### 6.3 Requirement catalog")
    lines.append("")
    emitted_source_ids: Set[str] = set()
    mapped_source_ids: Set[str] = set()
    for req_list in block_requirements.values():
        for req in req_list:
            mapped_source_ids.add(req.source_req_id)
    mapped_source_ids.update(connection_matrix_upstream)
    context_source_ids = {
        (row.get("Requirement ID") or "").strip()
        for row in non_block_context_rows
        if (row.get("Requirement ID") or "").strip()
    }
    requirements_by_source_id = {req.source_req_id: req for req in requirements}

    user_specific_requirements = [
        req
        for req in unmapped_requirements
        if req.source_req_id not in context_source_ids
        and not _dedicated_source_label(req)
        and _is_user_facing_requirement(req.statement)
    ]
    user_specific_ids = {req.source_req_id for req in user_specific_requirements}
    dedicated_groups: Dict[str, List[Requirement]] = defaultdict(list)
    for req in unmapped_requirements:
        label = _dedicated_source_label(req)
        if label and req.source_req_id not in context_source_ids:
            dedicated_groups[label].append(req)

    if dedicated_groups:
        lines.append("#### Dedicated source sections")
        lines.append("")
        for dedicated_index, group_name in enumerate(sorted(dedicated_groups), start=1):
            paragraph_number = f"6.3.{dedicated_index}"
            lines.append(f"##### {paragraph_number} {group_name} {{#{_anchor_slug(group_name)}}}")
            lines.append("")
            for req in sorted(dedicated_groups[group_name], key=lambda item: drs_id_map.get(item.source_req_id, item.source_req_id)):
                if req.source_req_id in emitted_source_ids:
                    continue
                emitted_source_ids.add(req.source_req_id)
                lines.append(f"[{drs_id_map[req.source_req_id]}] Requirement:")
                lines.extend(_source_body_lines(req))
                lines.append(f"Covers: {_upstream_id(req.source_req_id, srs_upstream_map)}")
                lines.append("")

    for domain in ["DIG", "XDN"]:
        items = [
            req
            for req in grouped.get(domain, [])
            if req.source_req_id not in mapped_source_ids
            and req.source_req_id not in context_source_ids
            and req.source_req_id not in user_specific_ids
            and not _dedicated_source_label(req)
            and req.source_req_id not in connection_matrix_upstream
            and not _is_reset_clock_table_requirement(req)
            and not _is_interrupt_table_requirement(req)
        ]
        title = "Digital" if domain == "DIG" else "Cross-domain"
        lines.append(f"#### {title} requirements")
        if not items:
            lines.append("- No residual unmapped requirements for this domain (mapped items are captured in project-specific sub-block requirement paragraphs).")
            lines.append("")
            continue
        for req in items:
            if req.source_req_id in emitted_source_ids:
                continue
            emitted_source_ids.add(req.source_req_id)
            lines.append(f"[{drs_id_map[req.source_req_id]}] Requirement:")
            lines.append(req.statement)
            lines.append(f"Covers: {_upstream_id(req.source_req_id, srs_upstream_map)}")
            lines.append("")

    lines.append("#### Use case, user specific")
    if not user_specific_requirements:
        lines.append("- None")
        lines.append("")
    else:
        grouped_user_specific: Dict[str, List[Requirement]] = defaultdict(list)
        for req in user_specific_requirements:
            grouped_user_specific[_user_specific_group_label(req.source)].append(req)

        for group_name in sorted(grouped_user_specific):
            lines.append(f"##### {group_name}")
            lines.append("")
            for req in sorted(
                grouped_user_specific[group_name],
                key=lambda item: drs_id_map.get(item.source_req_id, item.source_req_id),
            ):
                if req.source_req_id in emitted_source_ids:
                    continue
                emitted_source_ids.add(req.source_req_id)
                lines.append(f"[{drs_id_map[req.source_req_id]}] Requirement:")
                lines.extend(_source_body_lines(req))
                lines.append(f"Covers: {_upstream_id(req.source_req_id, srs_upstream_map)}")
                lines.append("")

    lines.append("## 7. Interfaces and mixed-signal interactions")
    boundary_rows = _drs_intro_rows(architecture_entries,
                                    {block.name for block in digital_block_rows})["7. Interfaces and mixed-signal interactions"]
    lines.append(_drs_section_interaction_summary(boundary_rows))
    lines.append("")
    append_interaction_context(boundary_rows, include_summary=False)
    lines.append("")

    lines.append("## 8. Assumptions and TBD")
    lines.append("- ASSUME-001: Firmware and verification environments provide deterministic digital stimulus and observability.")
    lines.append("- TBD-001: Unassigned requirements in DRS traceability matrix require architectural owner review.")
    if crosscheck_decision == "no-go":
        lines.append("- TBD-002: Micro-architecture crosscheck is no-go; unresolved critical findings may affect DRS closure.")
    lines.append("")

    lines.append("## 9. Top-level integration requirements")
    lines.append("")
    idx = 1
    authored_req_counter = 0
    top_level_requirements = [
        req
        for req in requirements
        if req.source_req_id in connection_matrix_upstream
        or _is_reset_clock_table_requirement(req)
        or _is_interrupt_table_requirement(req)
    ]
    if top_level_requirements:
        lines.append("Shared-resource, interface, clock/reset, interrupt, and interaction constraints are rendered here at integration scope. Detailed block-local behavior remains in Digital IPOS specifications.")
        lines.append("")
        for req in sorted(top_level_requirements, key=lambda item: drs_id_map.get(item.source_req_id, item.source_req_id)):
            if req.source_req_id in emitted_source_ids:
                continue
            emitted_source_ids.add(req.source_req_id)
            authored_req_counter += 1
            lines.append(f"[{drs_id_map[req.source_req_id]}] Requirement:")
            if req.source_req_id in connection_matrix_upstream:
                lines.append(connection_matrix_upstream[req.source_req_id][1])
            else:
                lines.extend(_source_body_lines(req))
            lines.append(f"Covers: {_upstream_id(req.source_req_id, srs_upstream_map)}")
            lines.append("")
    else:
        lines.append("No approved top-level integration requirements were identified in the current snapshot.")
        lines.append("")

    # The complete block-owned traceability matrix remains available to the
    # Digital IPOS generator, but block-local requirement bodies are not
    # rendered in the top-level DRS document.
    for block in digital_block_rows:
        rendered_source_titles: Set[str] = set()
        reqs = block_requirements.get(block.name, [])
        source_tables_for_block = source_interface_tables.get(block.name, [])
        source_ports_for_block = [
            row for row in source_port_rows
            if row.get("Owner") == block.name and row.get("Ownership status") == "approved"
        ]
        reqs_sorted = sorted(reqs, key=lambda item: drs_id_map.get(item.source_req_id, item.source_req_id))
        unique_upstream = {}
        for req in reqs_sorted:
            upstream = connection_matrix_upstream.get(req.source_req_id)
            if upstream and not upstream[1].startswith(f"The {block.name} block"):
                continue
            if req.source_req_id in emitted_source_ids:
                continue
            unique_upstream[upstream[0] if upstream else req.source_req_id] = req
        reqs_sorted = list(unique_upstream.values())
        lines.append(f"### 9.{idx} {block.name}")
        lines.append(compose_technical_block_purpose(block.name, block.function))
        lines.append("")

        for table_index, (title, provenance, table_text) in enumerate(source_tables_for_block, start=1):
            rendered_source_titles.add(title)
            lines.append(f"Source interface table {table_index}: {title}")
            lines.append(f"- {provenance}")
            rendered_table = _render_source_interface_table(table_text)
            table_base = title.split(":", 1)[-1].strip()
            table_ports = [row for row in source_ports_for_block if (
                row.get("Table title", "").strip() == title.strip()
                or row.get("Table title", "").strip() in title
                or title.strip() in row.get("Table title", "").strip()
                or row.get("Table title", "").strip() == table_base
            )]
            if rendered_table:
                lines.extend(rendered_table)
            elif table_ports:
                lines.extend(_render_approved_port_table(table_ports))
            else:
                lines.append(table_text)
            rendered_names = {
                cell.strip().replace("\\|", "|")
                for line in rendered_table if line.startswith("|")
                for cell in [line.split("|", 2)[1]]
            }
            missing_ports = [row for row in table_ports if row.get("Port name", "").strip() not in rendered_names]
            if rendered_table and missing_ports:
                lines.append("")
                lines.extend(_render_approved_port_table(missing_ports))
            lines.append("")

        for title in dict.fromkeys(row.get("Table title", "").strip() for row in source_ports_for_block):
            if not title or any(
                title == rendered_title or title in rendered_title or rendered_title in title
                for rendered_title in rendered_source_titles
            ):
                continue
            lines.append(f"Source interface table: {title}")
            lines.extend(_render_approved_port_table([
                row for row in source_ports_for_block if row.get("Table title", "").strip() == title
            ]))
            lines.append("")

        for req in reqs_sorted:
            authored_req_counter += 1
            emitted_source_ids.add(req.source_req_id)
            lines.append(f"[{drs_id_map[req.source_req_id]}] Requirement:")
            lines.extend(
                _connection_matrix_statement(
                    block.name,
                    req,
                    connection_matrix_upstream,
                    source_requirement_ids,
                ).splitlines()
            )
            upstream_id = _upstream_id(req.source_req_id, srs_upstream_map)
            lines.append(f"Covers: {upstream_id}")
            lines.append("")
            lines.append("")

        lines.append("")
        idx += 1

    if authored_req_counter == 0:
        lines.append("No additional block-local requirements are rendered in the top-level DRS.")
        lines.append("")

    if non_block_context_rows:
        lines.append("## 6.4 Source Function Context {#64-source-function-context}")
        lines.append("")
        grouped_context: Dict[str, List[Dict[str, str]]] = defaultdict(list)
        for row in non_block_context_rows:
            grouped_context[_non_block_context_label(row.get("Non-Block Function Context") or "")].append(row)
        for context_index, (context, rows) in enumerate(sorted(grouped_context.items()), start=1):
            paragraph_number = f"6.4.{context_index}"
            lines.append(f"### {paragraph_number} {context} {{#{_anchor_slug(paragraph_number + ' ' + context)}}}")
            lines.append("")
            for row in rows:
                source_req_id = (row.get("Requirement ID") or "").strip()
                requirement = requirements_by_source_id.get(source_req_id)
                if requirement is None or source_req_id not in drs_id_map:
                    continue
                if source_req_id in emitted_source_ids:
                    continue
                emitted_source_ids.add(source_req_id)
                lines.append(f"[{drs_id_map[source_req_id]}] Requirement:")
                lines.extend(_source_body_lines(requirement))
                lines.append(f"Covers: {_upstream_id(source_req_id, srs_upstream_map)}")
                lines.append(f"Source paragraph: {_display_non_block_source(row)}")
                lines.append("")

    lines.append("## 10. Missing Inputs")
    if missing_inputs:
        repo_root = _resolve_repo_root()
        for p in missing_inputs:
            try:
                rel = p.relative_to(repo_root).as_posix()
            except ValueError:
                rel = str(p)
            lines.append(f"- {rel}")
    else:
        lines.append("- None")
    lines.append("")

    lines = arrange_drs_contract_lines(lines, document_contract)
    lines = _apply_explicit_heading_ids(lines)
    heading_registry = _build_heading_registry(lines)
    first_numbered_index = next(
        (index for index, entry in enumerate(heading_registry) if entry[3]),
        len(heading_registry),
    )

    def _navigation_key(item: Tuple[int, Tuple[int, str, str, str]]) -> Tuple[int, Tuple[int, ...], int]:
        index, entry = item
        section_number = entry[3]
        if not section_number:
            return (0 if index < first_numbered_index else 2, (), index)
        return (1, tuple(int(part) for part in section_number.split(".")), index)

    navigation_registry = [
        entry
        for _index, entry in sorted(enumerate(heading_registry), key=_navigation_key)
    ]
    ordered_entries = [
        (title, section_number, anchor)
        for level, title, anchor, section_number in navigation_registry
        if (level == 2 and not section_number)
        or title == "0. Document Navigation"
        or (section_number and not section_number.startswith("0."))
    ]
    toc_lines = [
        f"{'  ' * max(0, len(number.split('.')) - 1)}- [{title}](#{anchor})"
        for title, number, anchor in ordered_entries
    ]
    nav_lines = [
        f"| {title} | {section_number or '0'} | [Jump](#{anchor}) | Auto |"
        for title, section_number, anchor in ordered_entries
    ]
    lines = [
        item
        for line in lines
        for item in (
            toc_lines if line == marker_toc else nav_lines if line == marker_nav else [line]
        )
    ]
    lines_rendered: List[str] = apply_shared_spec_markdown_formatting([_to_text(item) for item in lines])
    lines_rendered = _ensure_blank_line_between_paragraphs(lines_rendered)
    lines_rendered = _ensure_requirement_block_spacing(lines_rendered)
    lines_rendered = _ensure_subparagraph_heading_spacing(lines_rendered)
    lines_rendered = _ensure_table_block_spacing(lines_rendered)
    lines_rendered = _insert_visible_paragraph_spacers(lines_rendered)
    lines_rendered = _terminate_authored_requirement_blocks(lines_rendered)
    output_path.write_text("\n".join(lines_rendered) + "\n", encoding="utf-8")


def _write_stage_report(
    output_path: Path,
    present_inputs: List[Path],
    missing_inputs: List[Path],
    requirements: List[Requirement],
    unmapped_requirements: List[Requirement],
    full_traceability_count: int,
    unassigned_count: int,
    crosscheck_decision: str,
    requirements_only_mode: bool,
) -> str:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    counts = defaultdict(int)
    for req in requirements:
        counts[req.domain] += 1

    status = "pass" if requirements else "fail"
    blocking_issues: List[str] = []

    if not requirements:
        blocking_issues.append("No digital-relevant requirements were selected from requirements_summary.csv")
    if missing_inputs:
        blocking_issues.append(f"Missing required input artifacts: {len(missing_inputs)}")
    if crosscheck_decision == "no-go":
        blocking_issues.append("Micro-architecture crosscheck decision is no-go")
    if blocking_issues:
        status = "fail"

    lines: List[str] = [
        "# Stage DRS Report",
        "",
        f"Date: {today}",
        "",
        f"DRS generation status: {status}",
        f"DRS mode: {'requirements-only (Stage1 + Stage2A)' if requirements_only_mode else 'full inputs'}",
        "",
        "## Input artifact coverage summary",
        f"- Present inputs: {len(present_inputs)}",
        f"- Missing inputs: {len(missing_inputs)}",
        "",
        "## Count of generated DRS requirements by domain",
        f"- DIG: {counts['DIG']}",
        f"- XDN: {counts['XDN']}",
        "",
        "## Count of requirements with full traceability",
        f"- Fully mapped to owning block: {full_traceability_count}",
        f"- Unassigned owning block: {unassigned_count}",
        f"- Unmapped to included digital blocks: {len(unmapped_requirements)}",
        "",
        "## Open TBD/assumptions list",
        "- ASSUME-001: Firmware and verification environments provide deterministic digital stimulus and observability.",
        "- TBD-001: Unassigned requirements in DRS traceability matrix require architectural owner review.",
        f"- Stage 2 micro-architecture crosscheck decision: {crosscheck_decision}",
        "",
        "## Unmapped digital requirements",
    ]

    if unmapped_requirements:
        lines.extend(
            [f"- {req.source_req_id}" for req in unmapped_requirements if not _dedicated_source_label(req)]
            or ["- None (dedicated source-section requirements are listed under their preserved paragraphs)"]
        )
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Blocking issues list")

    if blocking_issues:
        for issue in blocking_issues:
            lines.append(f"- {issue}")
    else:
        lines.append("- None")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return status


def _convert_markdown_to_docx(
    markdown_path: Path,
    output_docx_path: Path,
    reference_template_path: Path | None,
    repo_root: Path,
) -> None:
    if shutil.which("pandoc") is None:
        raise RuntimeError("pandoc is not available on PATH")
    if not markdown_path.exists():
        raise FileNotFoundError(f"Missing markdown source for DOCX conversion: {markdown_path}")
    if reference_template_path is not None and not reference_template_path.exists():
        raise FileNotFoundError(f"Missing DOCX reference template: {reference_template_path}")

    output_docx_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "pandoc",
        str(markdown_path),
        "--from",
        "markdown+pipe_tables+header_attributes+raw_html",
        "--to",
        "docx",
        "-o",
        str(output_docx_path),
    ]
    if reference_template_path is not None:
        cmd[6:6] = ["--reference-doc", str(reference_template_path)]
    rc = subprocess.run(cmd, cwd=repo_root).returncode
    if rc != 0:
        raise RuntimeError(f"DRS md->docx conversion failed with exit code {rc}")
    _apply_docx_table_grid(output_docx_path)
    apply_docx_authored_requirement_formatting(output_docx_path, ("DRS",))
    apply_docx_common_spec_formatting(output_docx_path)
    _validate_docx_tables(output_docx_path)
    _validate_docx_end_markers(markdown_path, output_docx_path)


def _validate_docx_end_markers(markdown_path: Path, docx_path: Path) -> None:
    expected = len(re.findall(r"^[ \t]*\[End\][ \t]*$", markdown_path.read_text(encoding="utf-8"), flags=re.M | re.I))
    with zipfile.ZipFile(docx_path) as archive:
        document_xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
    if document_xml.lower().count("[end]") < expected:
        raise RuntimeError("DRS DOCX does not preserve all visible [End] requirement terminators")


def _apply_docx_table_grid(docx_path: Path) -> None:
    """Give generated Word tables visible borders while keeping them editable."""
    border_xml = (
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '</w:tblBorders>'
    )
    with zipfile.ZipFile(docx_path) as archive:
        members = {info.filename: archive.read(info.filename) for info in archive.infolist()}
    document_xml = members["word/document.xml"].decode("utf-8", errors="ignore")
    def add_borders(match: re.Match[str]) -> str:
        table_properties = match.group(0)
        if "<w:tblBorders" in table_properties:
            return table_properties
        return table_properties.replace("</w:tblPr>", border_xml + "</w:tblPr>")

    document_xml = re.sub(r"<w:tblPr(?:\s[^>]*)?>.*?</w:tblPr>", add_borders, document_xml, flags=re.DOTALL)
    members["word/document.xml"] = document_xml.encode("utf-8")
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with zipfile.ZipFile(temporary_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for filename, content in members.items():
                archive.writestr(filename, content)
        temporary_path.replace(docx_path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _validate_docx_tables(docx_path: Path) -> None:
    """Ensure Markdown pipe tables became editable Word tables, not plain text."""
    try:
        with zipfile.ZipFile(docx_path) as archive:
            document_xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
    except (OSError, KeyError, zipfile.BadZipFile) as exc:
        raise RuntimeError(f"Unable to inspect generated DOCX: {exc}") from exc

    table_count = len(re.findall(r"<w:tbl(?:\s|>)", document_xml))
    if table_count == 0:
        raise RuntimeError("Generated DOCX contains no editable Word tables")
    if "Sensor Hub I/O List" in document_xml and table_count < 1:
        raise RuntimeError("Sensor Hub I/O List was not converted to an editable Word table")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run DRS generation agent workflow")
    parser.add_argument("--agent-file", default=".github/agents/drs_gen_spec.agent.md", help="Path to agent definition markdown")
    parser.add_argument("--template-file", default="templates/DRS_gen_AI_template_prompt.md", help="Path to DRS generation template markdown")
    parser.add_argument("--requirements-summary", help="Deprecated compatibility option; resolver snapshot is authoritative")
    parser.add_argument("--req-block-trace", default="artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv", help="Requirement to block traceability CSV")
    parser.add_argument("--block-inventory", default="artifacts/stage2_mirco_arc/block_inventory.csv", help="Block inventory CSV")
    parser.add_argument("--interface-catalog", default="artifacts/stage2_mirco_arc/interface_catalog.csv", help="Interface catalog CSV")
    parser.add_argument("--architecture-crosscheck", default="artifacts/stage2_mirco_arc/architecture_crosscheck_report.md", help="Architecture crosscheck report markdown")
    parser.add_argument("--srs-traceability", default="artifacts/stage3_srs/srs_traceability_matrix.csv", help="SRS traceability CSV (source_req_id -> srs_req_id)")
    parser.add_argument("--out-drs-md", default="artifacts/stage5_drs/digital_requirements_specification.md", help="Output DRS markdown path")
    parser.add_argument("--out-drs-docx", default="artifacts/stage5_drs/digital_requirements_specification.docx", help="Output DRS DOCX path")
    parser.add_argument("--out-traceability-csv", default="artifacts/stage5_drs/drs_traceability_matrix.csv", help="Output DRS traceability CSV path")
    parser.add_argument("--out-stage-report", default="artifacts/orchestrator/stage_drs_report.md", help="Output Stage DRS report path")
    parser.add_argument("--docx-reference-template", default=DOCX_REFERENCE_TEMPLATE, help="DOCX reference template path for pandoc conversion")
    parser.add_argument(
        "--requirements-only",
        action="store_true",
        help="Generate DRS from Stage 1 + Stage 2A artifacts only and omit Stage 4 ARS references.",
    )
    parser.add_argument("--snapshot-id", help="Explicit approved canonical snapshot ID")
    parser.add_argument("--use-latest-approved", action="store_true", help="Explicitly select the latest approved snapshot")
    parser.add_argument("--regenerate-downstream", action="store_true", help="Regenerate from the explicit approved snapshot before coherence validation passes")
    args = parser.parse_args()
    if bool(args.snapshot_id) == bool(args.use_latest_approved):
        parser.error("Provide exactly one of --snapshot-id or --use-latest-approved")
    if args.regenerate_downstream and not args.snapshot_id:
        parser.error("--regenerate-downstream requires --snapshot-id")

    repo_root = _resolve_repo_root()
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    guard_cmd = [sys.executable, "scripts/guard_stage2_plus_spec_independence.py", "--quiet"]
    guard_rc = subprocess.run(guard_cmd, cwd=repo_root).returncode
    if guard_rc != 0:
        print("DRS agent run: FAIL (Stage 2+ source-spec independence guard failed)")
        _append_log(repo_root, script_name, f"FAIL stage2_plus_guard_exit={guard_rc}")
        return guard_rc

    agent_file = (repo_root / args.agent_file).resolve()
    template_file = (repo_root / args.template_file).resolve()
    try:
        document_contract = load_drs_contract(template_file)
        if template_file != (repo_root / DRS_TEMPLATE).resolve():
            raise ValueError("DRS pilot requires the authoritative repository template")
        for argument, expected in (
            (args.out_drs_md, "artifacts/stage5_drs/digital_requirements_specification.md"),
            (args.out_drs_docx, "artifacts/stage5_drs/digital_requirements_specification.docx"),
        ):
            if (repo_root / argument).resolve() != (repo_root / expected).resolve():
                raise ValueError("DRS pilot requires canonical output paths for shared validation")
        baseline = json.loads((repo_root / "artifacts/stage5_drs/drs_preservation_baseline.json").read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"DRS agent run: FAIL (document contract: {exc})")
        return 1
    context = json.loads((repo_root / "config" / "project_context.json").read_text(encoding="utf-8"))
    requirement_input, selection = resolve_complete_authoritative_input(
        repo_root,
        "4",
        project_id=str(context.get("project_name") or repo_root.name),
        snapshot_id=args.snapshot_id,
    )
    downstream_contract = resolve_downstream_contract(repo_root, requirement_input.snapshot_id)
    if baseline.get("snapshot_id") != requirement_input.snapshot_id:
        raise RuntimeError("DRS preservation baseline does not match the approved snapshot")
    coherence = validate_downstream_coherence(repo_root, requirement_input.snapshot_id)
    blocking = [finding for finding in coherence["findings"] if not (
        args.regenerate_downstream and finding.startswith(("DRS_CONTRACT:", "DRS: "))
    )]
    if blocking:
        raise RuntimeError(f"Downstream snapshot coherence blocked DRS generation: {coherence['finding_count']} findings")
    _append_log(repo_root, script_name, f"AUTHORITATIVE_SNAPSHOT snapshot_id={selection['selected_snapshot_id']} mode={selection['selection_mode']} user={runtime_user_name()}")
    summary_csv = requirement_input.source_path
    req_block_trace_csv = (repo_root / args.req_block_trace).resolve()
    block_inventory_csv = (repo_root / args.block_inventory).resolve()
    interface_catalog_csv = (repo_root / args.interface_catalog).resolve()
    architecture_crosscheck_md = (repo_root / args.architecture_crosscheck).resolve()
    srs_traceability_csv = (repo_root / args.srs_traceability).resolve()

    out_drs_md = (repo_root / args.out_drs_md).resolve()
    document_version = document_version_for_snapshot(out_drs_md, requirement_input.snapshot_id)
    out_drs_docx = (repo_root / args.out_drs_docx).resolve()
    out_traceability_csv = (repo_root / args.out_traceability_csv).resolve()
    out_stage_report = (repo_root / args.out_stage_report).resolve()
    docx_reference_template = (
        (repo_root / args.docx_reference_template).resolve()
        if args.docx_reference_template
        else None
    )

    if docx_reference_template and docx_reference_template.exists():
        print(f"DRS agent run: INFO (format reference template: {docx_reference_template})")
        _append_log(repo_root, script_name, f"INFO docx_reference_template={docx_reference_template}")
    elif docx_reference_template:
        print(f"DRS agent run: WARN (reference template not found: {docx_reference_template})")
        _append_log(repo_root, script_name, f"WARN missing_docx_reference_template={docx_reference_template}")

    present_inputs, missing_inputs = _check_inputs(repo_root)

    if not agent_file.exists():
        print(f"DRS agent run: FAIL (missing agent file: {agent_file})")
        _append_log(repo_root, script_name, f"FAIL missing_agent={agent_file}")
        return 1

    if not summary_csv.exists():
        print(f"DRS agent run: FAIL (missing requirements summary: {summary_csv})")
        _append_log(repo_root, script_name, f"FAIL missing_summary={summary_csv}")
        return 1

    if not template_file.exists():
        print(f"DRS agent run: FAIL (missing prompt template: {template_file})")
        _append_log(repo_root, script_name, f"FAIL missing_prompt_template={template_file}")
        return 1

    try:
        project_context_path = repo_root / "config/project_context.json"
        project_context = (
            json.loads(project_context_path.read_text(encoding="utf-8"))
            if project_context_path.exists()
            else {}
        )
        source_spec = _resolve_source_spec_from_stage1_index(
            (repo_root / "artifacts/stage1_requirements/ocr_extracts/index.csv").resolve(),
            repo_root,
        )
        all_requirements = _read_requirements(summary_csv, requirement_input.rows)
        source_architecture_capability_records = _source_architecture_capability_records(
            repo_root / "artifacts/stage1_requirements/requirements_summary.csv"
        )
        canonical_to_source = {
            str(row.get("canonical_id") or "").strip(): str(row.get("source_req_id") or "").strip()
            for row in requirement_input.rows
            if str(row.get("canonical_id") or "").strip() and str(row.get("source_req_id") or "").strip()
        }
        allocations_by_source = {
            source_id: downstream_contract.allocation(source_id)
            for source_id in canonical_to_source.values()
            if source_id
        }
        refresh_ledger(repo_root, snapshot_id=requirement_input.snapshot_id, source_rows=requirement_input.rows)
        req_to_block = _read_req_to_block(req_block_trace_csv)
        srs_upstream_map = _read_srs_upstream_map(srs_traceability_csv)
        srs_statements = _read_srs_statements(srs_traceability_csv)
        for requirement in all_requirements:
            if requirement.source_req_id in srs_statements:
                requirement.statement = srs_statements[requirement.source_req_id]
        block_inventory = _read_block_inventory(block_inventory_csv)
        _require_block_functions(block_inventory)
        block_by_name = {block.name: block for block in block_inventory}
        interface_rows = _read_interface_rows(interface_catalog_csv)
        source_port_rows = _read_interface_rows(repo_root / "artifacts/stage2_mirco_arc/source_port_catalog.csv")
        interaction_rows = _read_interaction_rows((repo_root / "artifacts/stage2_mirco_arc/interaction_matrix.csv").resolve())
        connection_matrix_upstream = _connection_matrix_upstream_ids(interaction_rows)
        connection_matrix_source_owners = _connection_matrix_source_owners(interaction_rows)
        crosscheck_decision = _extract_crosscheck_decision(architecture_crosscheck_md)
        source_interface_tables = _source_interface_tables_by_block(repo_root, block_inventory)
        non_block_context_rows = _read_non_block_context_rows(
            repo_root / "artifacts/stage2_mirco_arc/unmapped_requirement_routing.csv",
            {requirement.source_req_id for requirement in all_requirements},
        )
        non_block_source_ids = {
            row.get("Requirement ID", "").strip()
            for row in non_block_context_rows
            if row.get("Requirement ID", "").strip()
        }
        approved_architecture_rows = read_selected_low_power_audit(
            srs_traceability_csv.with_name("descriptive_low_power_audit.csv")
        )
        approved_architecture_rows.extend(source_architecture_capability_records)

        digital_blocks = _inventory_digital_blocks(block_inventory, interface_rows)
        stage1_overview_records, stage1_block_descriptions = _stage1_overview_descriptive_records(
            repo_root / "artifacts/stage1_requirements/ocr_extracts/index.csv",
            [block for block in block_inventory if block.name in digital_blocks],
        )
        approved_architecture_rows.extend(stage1_overview_records)
        req_to_block = {
            source_id: downstream_contract.concrete_owner(source_id, digital_blocks) or "Unassigned"
            for source_id in allocations_by_source
        }
        selected_requirements = [
            r for r in all_requirements
            if allocations_by_source.get(r.source_req_id, {}).get("owning_target") == "DRS"
        ]

        normalized_requirements: List[Requirement] = []
        for r in selected_requirements:
            dom = "DIG" if r.domain in {"DIG", "SYS"} else "XDN"
            normalized_requirements.append(
                Requirement(
                    source_req_id=r.source_req_id,
                    domain=dom,
                    statement=r.statement,
                    source=r.source,
                    requirement_type=r.requirement_type,
                    value_range_condition=r.value_range_condition,
                    derivation_kind=r.derivation_kind,
                    evidence_type=r.evidence_type,
                    notes=r.notes,
                )
            )

            _require_srs_upstream_map(normalized_requirements, srs_upstream_map)

        block_requirements, unmapped_requirements = _map_requirements_to_digital_blocks(
            normalized_requirements,
            req_to_block,
            block_by_name,
            digital_blocks,
            connection_matrix_source_owners,
        )
        for block_name, mapped_requirements in list(block_requirements.items()):
            block_requirements[block_name] = [
                requirement
                for requirement in mapped_requirements
                if requirement.source_req_id not in non_block_source_ids
            ]
            unmapped_requirements.extend(
                requirement
                for requirement in mapped_requirements
                if requirement.source_req_id in non_block_source_ids
            )
        drs_id_map = _build_drs_id_map(normalized_requirements)
        full_traceability_count, unassigned_count = _write_traceability_csv(
            out_traceability_csv, normalized_requirements, drs_id_map, req_to_block,
            allocations_by_source, requirement_input.snapshot_id
        )
        structured_power_records = power_domain_records_from_ocr(repo_root)
        descriptive_records = [
            record for record in structured_power_records
            if is_drs_top_level_record(record)
        ]
        descriptive_records.extend(_top_digital_coverage_records(
            interaction_rows,
            interface_rows,
            non_block_context_rows,
            approved_architecture_rows,
        ))
        write_descriptive_audit(
            out_drs_md.with_name("descriptive_summary_audit.csv"),
            assemble_descriptive_summary(
                [record for record in descriptive_records
                 if record.get("record_type", "").casefold() != "architecture_capability"],
                DESCRIPTIVE_DIGITAL_TOPIC_SPECS,
            ),
            section="Digital Main Functions",
        )
        low_power_grouped, low_power_audit = assemble_low_power_descriptive(
            descriptive_records,
            repo_root=repo_root,
            profile="drs",
        )
        write_low_power_audit(out_drs_md.with_name("descriptive_low_power_audit.csv"), low_power_audit)
        _coverage, coverage_audit = assess_top_digital_coverage(
            _top_digital_coverage_records(
                interaction_rows,
                interface_rows,
                non_block_context_rows,
                approved_architecture_rows,
            )
        )
        write_top_digital_coverage_audit(
            out_drs_md.with_name("top_digital_coverage_audit.csv"),
            coverage_audit,
        )
        _write_drs_markdown(
            out_drs_md,
            source_spec,
            str(project_context.get("project_name") or "Project"),
            document_author_name(),
            requirement_input.snapshot_id,
            document_version,
            normalized_requirements,
            drs_id_map,
            block_inventory,
            stage1_block_descriptions,
            interface_rows,
            source_interface_tables,
            source_port_rows,
            block_requirements,
            unmapped_requirements,
            descriptive_records,
            non_block_context_rows,
            crosscheck_decision,
            missing_inputs,
            args.requirements_only,
            connection_matrix_upstream,
            {requirement.source_req_id for requirement in all_requirements},
            srs_upstream_map,
            _drs_clock_path_rows(requirement_input.rows),
            _drs_sync_connection_rows(requirement_input.rows, source_port_rows),
            document_contract,
        )
        _append_drs_block_description_audit(
            out_drs_md.with_name("descriptive_summary_audit.csv"),
            _drs_descriptive_blocks(block_inventory, interface_rows, source_interface_tables),
            stage1_block_descriptions,
        )
        _append_drs_stage1_overview_audit(
            out_drs_md.with_name("descriptive_summary_audit.csv"),
            [*source_architecture_capability_records, *stage1_overview_records],
        )
        _append_drs_intro_audit(
            out_drs_md.with_name("descriptive_summary_audit.csv"), descriptive_records,
            {block.name for block in _drs_descriptive_blocks(block_inventory, interface_rows, source_interface_tables)},
        )
        docx_generated = False
        if shutil.which("pandoc") is None:
            raise RuntimeError("pandoc is required for DRS DOCX generation but is not available on PATH")
        if docx_reference_template is not None and not docx_reference_template.exists():
            raise FileNotFoundError(f"Missing DOCX reference template: {docx_reference_template}")
        _convert_markdown_to_docx(out_drs_md, out_drs_docx, docx_reference_template, repo_root)
        contract_findings = validate_drs_document_contract(repo_root, check_metadata=False)
        contract_findings.extend(validate_drs_descriptive_artifacts(repo_root))
        if contract_findings:
            raise RuntimeError("DRS contract failed: " + "\n".join(contract_findings))
        metadata = drs_contract_metadata(repo_root, document_contract)
        out_drs_md.with_name("drs_document_contract.json").write_text(
            json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        docx_generated = True
        status = _write_stage_report(
            out_stage_report,
            present_inputs,
            missing_inputs,
            normalized_requirements,
            unmapped_requirements,
            full_traceability_count,
            unassigned_count,
            crosscheck_decision,
            args.requirements_only,
        )

        with out_stage_report.open("a", encoding="utf-8") as handle:
            handle.write(f"\n## Executed DRS document contract\n\nVersion: {document_contract['version']}\n\nTemplate SHA-256: {document_contract['sha256']}\n\n")
            for rule in document_contract["mandatory_rules"]:
                handle.write(f"- {rule}: PASS\n")
        drs_crosscheck_cmd = [sys.executable, "scripts/run_drs_crosscheck_agent.py"]
        if args.snapshot_id:
            drs_crosscheck_cmd += ["--snapshot-id", args.snapshot_id]
        else:
            drs_crosscheck_cmd.append("--use-latest-approved")
        drs_crosscheck_rc = subprocess.run(drs_crosscheck_cmd, cwd=repo_root).returncode
        if drs_crosscheck_rc != 0:
            raise RuntimeError(f"DRS crosscheck failed with exit code {drs_crosscheck_rc}")
        final_coherence = validate_downstream_coherence(repo_root, requirement_input.snapshot_id)
        if final_coherence["decision"] != "PASS":
            raise RuntimeError("Final downstream coherence failed: " + "\n".join(final_coherence["findings"]))
    except Exception as exc:
        print(f"DRS agent run: FAIL ({exc})")
        print(traceback.format_exc())
        _append_log(repo_root, script_name, f"FAIL error={exc}")
        return 1

    print("DRS agent run: PASS")
    print(f"- Agent definition: {agent_file}")
    print(f"- Prompt template: {template_file}")
    print(f"- DRS markdown: {out_drs_md}")
    if docx_generated:
        print(f"- DRS DOCX: {out_drs_docx}")
    else:
        print("- DRS DOCX: not generated")
    print(f"- Traceability CSV: {out_traceability_csv}")
    print(f"- Stage report: {out_stage_report}")
    print(f"- Input coverage: present={len(present_inputs)} missing={len(missing_inputs)}")
    print(f"- Requirements generated: {len(normalized_requirements)}")
    print(f"- Traceability mapped: {full_traceability_count} (unassigned={unassigned_count})")
    print(f"- Micro-architecture crosscheck decision: {crosscheck_decision}")
    print(f"- Stage status: {status}")

    _append_log(
        repo_root,
        script_name,
        (
            "PASS "
            f"requirements={len(normalized_requirements)} full_traceability={full_traceability_count} "
            f"unassigned={unassigned_count} missing_inputs={len(missing_inputs)} status={status}"
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
