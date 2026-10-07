#!/usr/bin/env python3
"""Run the SRS generation agent workflow from repository artifacts.

This script operationalizes `.github/agents/srs_gen_spec.agent.md` by:
- validating required inputs
- generating SRS markdown
- generating SRS traceability CSV
- generating Stage SRS report
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
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Set, Tuple

from workflow_routing import (
    apply_docx_authored_requirement_formatting,
    apply_docx_common_spec_formatting,
    GENERATED_SPEC_VERSION,
    cascade_retained_context,
    csv_cell_text,
    normalize_authored_requirement_blocks,
    organize_descriptive_topics,
    DESCRIPTIVE_MODE_TOPIC_SPECS,
    DESCRIPTIVE_POWER_TOPIC_SPECS,
    DESCRIPTIVE_SYSTEM_TOPIC_SPECS,
    SRS_SYSTEM_OVERVIEW_HEADINGS,
    assemble_descriptive_summary,
    compose_srs_system_overview,
    compose_srs_support_content,
    SRS_INTRODUCTORY_SECTIONS,
    write_descriptive_audit,
    read_retained_rows,
    source_parent_title,
    runtime_user_name,
    document_author_name,
    document_version_for_snapshot,
    document_version_history_markdown,
)
from approved_snapshot_resolver import resolve_complete_authoritative_input
from canonical_store import connect, read_stage2_descriptive_evidence
from allocation_ledger import refresh_ledger
from validate_downstream_coherence import (
    canonical_human_label,
    downstream_contract_fingerprint,
    resolve_downstream_contract,
    snapshot_architecture_context,
    srs_catalog_from_context,
    validate as validate_downstream_coherence,
)
from low_power_descriptive import (
    architecture_records_from_function_rows,
    assemble_low_power_descriptive,
    filter_configured_descriptive_exclusions,
    render_low_power_topics,
    write_low_power_audit,
)
from generate_architecture_sysml import approved_block_names
from stage1_descriptive_evidence import extract_stage1_descriptive_evidence
from spec_document_contract import shared_category_conventions_markdown


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
]

SRS_LATEX_AGENT_SCRIPT = "scripts/run_srs_md_to_latex_agent.py"
DOCX_REFERENCE_TEMPLATE = "templates/MPT_IPOS_template.docx"
FUNCTION_STOP_WORDS = {
    "a", "and", "are", "as", "at", "by", "for", "from", "in", "into",
    "of", "on", "or", "the", "to", "with",
}
SOURCE_REQUIREMENT_IDS: Set[str] = set()


POWER_FOCUS_TERMS = (
    "power",
    "supply",
    "voltage",
    "brown-out",
    "reverse-polarity",
    "polarity",
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
    derivation_kind: str = ""
    evidence_type: str = ""
    notes: str = ""
    source_section_owner: str = ""


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\n")


def _resolve_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


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
        return "The system shall satisfy this requirement based on available source artifacts."

    low = text.lower()
    if " shall " in low or low.startswith("shall "):
        return text

    if text.endswith("."):
        text = text[:-1]
    return f"The system shall satisfy the following behavior: {text}."


def _page_number_from_source(source: str) -> str:
    match = re.search(r"\(page\s+(\d+)\)", source or "", flags=re.IGNORECASE)
    return match.group(1) if match else ""


def _ocr_page_lines(ocr_dir: Path, source: str) -> List[str]:
    page = _page_number_from_source(source)
    if not page:
        return []
    candidates = sorted(ocr_dir.glob(f"*_p{int(page):03d}.txt")) + sorted(ocr_dir.glob(f"*_p{int(page)}.txt"))
    if not candidates:
        return []
    return candidates[0].read_text(encoding="utf-8").splitlines()


def _ocr_page_and_continuation_lines(ocr_dir: Path, source: str) -> List[str]:
    page = _page_number_from_source(source)
    if not page:
        return []

    out: List[str] = []
    for page_number in (int(page), int(page) + 1):
        candidates = sorted(ocr_dir.glob(f"*_p{page_number:03d}.txt")) + sorted(ocr_dir.glob(f"*_p{page_number}.txt"))
        if candidates:
            out.extend(candidates[0].read_text(encoding="utf-8").splitlines())
    return out


def _requirement_ocr_fragments(req_id: str, source: str, ocr_dir: Path) -> List[str]:
    lines = _ocr_page_lines(ocr_dir, source)
    if not lines:
        return []

    fragments: List[str] = []
    in_requirement = False
    req_pattern_text = re.escape(req_id).replace(r"\_", r"_\s*")
    req_pattern = re.compile(rf"\[?{req_pattern_text}\]?\s*(?:Requirement|Assumption)?\s*:?(.*)$", flags=re.IGNORECASE)
    next_req_pattern = re.compile(
        r"^\s*\[?[A-Z][A-Z0-9_-]*_\d+[A-Z0-9_-]*\]?\s*(?:Requirement|Assumption)?\s*:?(?:\s+|$)",
        flags=re.IGNORECASE,
    )
    next_section_pattern = re.compile(r"^\s*\d+(?:\.\d+)+\.\s+\S+")
    for line in lines:
        text = line.strip()
        if not text:
            continue
        if not in_requirement:
            match = req_pattern.match(text)
            if not match:
                continue
            in_requirement = True
            tail = match.group(1).strip()
            if tail:
                fragments.append(tail)
            continue
        if text.startswith("[End]") or text.startswith("[END]") or text.lower().startswith("table "):
            break
        if next_req_pattern.match(text) or next_section_pattern.match(text):
            break
        fragments.append(text)
    return fragments


def _join_wrapped_signal_fragments(fragments: List[str]) -> str:
    out = ""
    for fragment in fragments:
        text = fragment.strip()
        if not text:
            continue
        if not out:
            out = text
        elif out.endswith("_") or text.startswith((".", "_")):
            out += text
        else:
            out += text if re.search(r"[A-Za-z0-9_]$", out) and re.match(r"^[a-z][a-z0-9_]*\.", text) else f" {text}"
    return out.strip()


def _normalize_signal_token_spacing(text: str) -> str:
    normalized = text or ""
    normalized = re.sub(
        r"\b([A-Za-z])\s+_\s*([A-Za-z][A-Za-z0-9_]*)",
        r"\1_\2",
        normalized,
    )
    normalized = re.sub(r"(?<=[A-Za-z0-9])_\s+(?=[A-Za-z0-9])", "_", normalized)
    return normalized


def _clock_table_qualifiers(text: str) -> str:
    frequency_matches = re.findall(r"\b\d+(?:\.\d+)?\s*(?:MHz|kHz)\b", text, flags=re.IGNORECASE)
    frequency = frequency_matches[-1] if frequency_matches else ""
    statement_match = re.search(
        r"\bwith\s+clock\s+gating\s+(.+?)(?=\s*\.\s*$)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if statement_match:
        gating = statement_match.group(1).strip()
    elif re.search(r"\bwithout\s+clock\s+gating\b", text, flags=re.IGNORECASE):
        gating = "No"
    else:
        gating = "No" if re.search(r"\bNo\b", text, flags=re.IGNORECASE) else ""
    no_values = len(re.findall(r"\bNo\b", text, flags=re.IGNORECASE))
    delay = "No" if no_values >= 2 else ""
    qualifiers = []
    if delay:
        qualifiers.append(f"Delay: {delay}")
    if gating:
        qualifiers.append(f"Clock gating: {gating}")
    if frequency:
        qualifiers.append(f"F max: {frequency}")
    return (", " + "; ".join(qualifiers)) if qualifiers else ""


def _table_row_context(req_id: str, source: str, notes: str, ocr_dir: Path) -> str:
    lines = _ocr_page_and_continuation_lines(ocr_dir, source)
    if not lines:
        return ""
    line_match = re.search(r"lines\[(\d+)", notes or "")
    start = int(line_match.group(1)) if line_match else 0
    normalized_id = re.sub(r"\s+", "", req_id).lower()
    for index in range(max(0, start - 3), len(lines)):
        window = lines[index:index + 3]
        if normalized_id in re.sub(r"\s+", "", " ".join(window)).lower():
            row = lines[index:index + 10]
            return " ".join(item.strip() for item in row if item.strip())
    return ""


def _table_caption_reference(req_id: str, source: str, notes: str, ocr_dir: Path) -> str:
    lines = _ocr_page_and_continuation_lines(ocr_dir, source)
    if not lines:
        return ""
    line_match = re.search(r"lines\[(\d+)", notes or "")
    start = int(line_match.group(1)) if line_match else 0
    normalized_id = re.sub(r"\s+", "", req_id).lower()
    id_index = -1
    for index in range(max(0, start - 3), len(lines)):
        if normalized_id in re.sub(r"\s+", "", lines[index]).lower():
            id_index = index
            break
    if id_index < 0:
        return ""
    following_lines = [line.strip() for line in lines[id_index + 1:id_index + 5] if line.strip()]
    if not following_lines:
        return ""
    header_tokens = re.findall(r"\b[A-Z][A-Z0-9_]{1,}\b", following_lines[0])
    if re.search(r"\bshall\b", following_lines[0], flags=re.IGNORECASE) or len(header_tokens) < 3:
        return ""
    for line in lines[id_index + 1:]:
        text = re.sub(r"\s+", " ", line).strip()
        if not text:
            continue
        caption = re.match(r"^(Table\s+\d+\s*[:.]\s*.+?)\s*(?:\[End\]|\[END\])?$", text, flags=re.IGNORECASE)
        if caption:
            return caption.group(1).rstrip(" .") + "."
        if re.match(r"^\[?[A-Z][A-Z0-9_]*\]?\s+Requirement\b", text, flags=re.IGNORECASE):
            break
    return ""


def _derive_reset_clock_statement(req_id: str, source: str, statement: str, notes: str, ocr_dir: Path) -> str:
    fragments = _requirement_ocr_fragments(req_id, source, ocr_dir)
    row_context = _table_row_context(req_id, source, notes, ocr_dir)
    has_clock_evidence = bool(re.search(r"\b(?:frequency|clock_gating)=", notes or "", flags=re.IGNORECASE))
    qualifier_input = " ".join(fragments) + " " + row_context + " " + source + " " + statement
    qualifier_text = _clock_table_qualifiers(qualifier_input) if has_clock_evidence else ""
    if len(fragments) >= 3:
        first_root_match = re.match(r"\s*([A-Za-z_]\w*)\.", fragments[0])
        if first_root_match:
            root = first_root_match.group(1)
            split_at = next(
                (index for index, fragment in enumerate(fragments[1:], start=1)
                 if fragment.lstrip().startswith(root + ".")),
                -1,
            )
            if split_at > 0:
                source_signal = re.sub(r"\s+", "", "".join(fragments[:split_at]))
                destination_signal = re.sub(r"\s+", "", "".join(fragments[split_at:]))
                if source_signal and destination_signal:
                    return f"The {source_signal} signal shall be connected to the {destination_signal} signal{qualifier_text}."
    source_paths = re.findall(r"\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+\b", f"{source} {statement}")
    unique_paths = list(dict.fromkeys(source_paths))
    if len(unique_paths) >= 2:
        return f"The {unique_paths[0]} signal shall be connected to the {unique_paths[1]} signal{qualifier_text}."
    if len(fragments) < 3:
        return ""

    normalized_text = re.sub(r"\s*_\s*", "_", " ".join(fragments))
    paths = re.findall(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+", normalized_text)
    if len(paths) >= 2 and paths[0] != paths[1]:
        return f"The {paths[0]} signal shall be connected to the {paths[1]} signal{qualifier_text}."

    first_path = re.match(r"^([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+)", fragments[0].strip())
    if not first_path:
        return ""
    root = first_path.group(1).split(".", 1)[0]
    split_at = -1
    for idx, fragment in enumerate(fragments[1:], start=1):
        if fragment.strip().startswith(root):
            split_at = idx
            break
    if split_at < 1:
        return ""

    source_signal = _join_wrapped_signal_fragments(fragments[:split_at]).replace(" ", "")
    destination_signal = _join_wrapped_signal_fragments(fragments[split_at:]).replace(" ", "")
    if not source_signal or not destination_signal or source_signal == destination_signal:
        return ""
    return f"The {source_signal} signal shall be connected to the {destination_signal} signal{qualifier_text}."


def _normalize_source_statement(row: Dict[str, str], req_id: str, summary_csv: Path) -> str:
    statement = _normalize_signal_token_spacing(row.get("requirement_statement", ""))
    statement = re.sub(r"\[\s*Covers\s*:\s*[^\]]+\]\s*", "", statement, flags=re.IGNORECASE)
    source = row.get("source", "")
    notes = row.get("notes", "")
    ocr_dir = summary_csv.parent / "ocr_extracts"

    metadata = " ".join((source, notes, statement)).lower()
    if "table_line_info" in metadata:
        caption_reference = _table_caption_reference(req_id, source, notes, ocr_dir)
        if caption_reference:
            return caption_reference

    structural_paths = re.findall(r"\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+\b", metadata)
    if "table_line_info" in metadata and (
        re.search(r"\b(?:reset|clock|mhz|khz)\b", metadata)
        or len(set(structural_paths)) >= 2
    ):
        derived = _derive_reset_clock_statement(req_id, source, statement, notes, ocr_dir)
        if derived:
            return derived

    return statement


def _verification_method(req_type: str, domain: str) -> str:
    t = (req_type or "").strip().lower()
    if t in {"timing", "electrical", "performance"}:
        return "analysis+test"
    if t in {"interface", "protocol"}:
        return "inspection+test"
    if t in {"mode-behavior", "functional"}:
        return "test"
    if t in {"configuration"}:
        return "inspection+test"
    if domain == "XDN":
        return "analysis+test"
    return "test"


def _acceptance_criteria(row: Dict[str, str]) -> str:
    condition = (row.get("value_range_condition") or "").strip()
    if condition:
        return f"Measured result satisfies: {condition}."
    return "Requirement behavior is observed in nominal and boundary test conditions."


def _is_non_normative_table_row(row: Dict[str, str], statement: str) -> bool:
    raw_statement = row.get("requirement_statement", "")
    evidence = " ".join(row.get(field, "") for field in ("source", "notes", "derivation_kind", "evidence_type"))
    if (
        re.search(r"\b(?:pad\s+mux|bist|scan|debug|dft)\b", evidence, re.IGNORECASE)
        and re.search(r"\bshall\b", raw_statement, re.IGNORECASE)
    ):
        return False
    if (
        "table_line_info" in evidence
        and re.search(r"\b\d+\s*(?:k?hz|mhz)\b", evidence, re.IGNORECASE)
        and re.search(r"\b(?:signal|clock|reset)\b|\bu_[a-z0-9_]+\b", raw_statement, re.IGNORECASE)
    ):
        return False
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


def _is_introductory_architecture_record(record: Tuple[str, str, str]) -> bool:
    return bool(re.search(
        r"\b(?:revision|version)\s+history\b|\bhistory\s+table\b|\bintroduction\b|"
        r"\bdocument\s+control\b|\breference\s+documents?\b|"
        r"\b(?:added|changed|updated)\b.*\b\d{1,2}/\d{1,2}/\d{4}\b",
        " ".join(record),
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

    SOURCE_REQUIREMENT_IDS = {
        (row.get("source_req_id") or row.get("id") or "").strip()
        for row in rows
        if (row.get("source_req_id") or row.get("id") or "").strip()
    }
    requirements: List[Requirement] = []
    for row in rows:
        req_id = (row.get("source_req_id") or row.get("id") or "").strip()
        statement = _enforce_normative(_normalize_source_statement(row, req_id, summary_csv))
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
                derivation_kind=row.get("derivation_kind", ""),
                evidence_type=row.get("evidence_type", ""),
                notes=row.get("notes", ""),
                source_section_owner=row.get("source_section_owner", ""),
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


def _read_csv_rows(path: Path) -> List[Dict[str, str]]:
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


def _mode_source_rows(repo_root: Path, block_names: List[str]) -> List[Dict[str, str]]:
    """Extract ON/OFF operating-mode rows from source table text generically.

    The source table is identified by rows ending in a requirement-like ID. Its
    column names are matched to the current block inventory by token overlap, so
    projects may use aliases such as FIFO_CTRL for a FIFO block.
    """
    ocr_dir = repo_root / "artifacts/stage1_requirements/ocr_extracts"
    if not ocr_dir.exists():
        return []

    source_id_re = re.compile(r"\b[A-Za-z][A-Za-z0-9]*(?:[_-][A-Za-z0-9]+)+\b")
    state_re = re.compile(r"\b(on|off)\b", re.IGNORECASE)
    rows: List[Dict[str, str]] = []
    for path in sorted(ocr_dir.glob("*.txt")):
        text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8", errors="ignore"))
        header_match = re.search(r"([^.!?]{0,180})\bReq_ID\b", text, re.IGNORECASE)
        if not header_match:
            continue
        header = header_match.group(1)
        header_tokens = re.findall(r"[A-Za-z][A-Za-z0-9_/-]*", header)
        source_ids = list(source_id_re.finditer(text))
        for index, match in enumerate(source_ids):
            source_id = match.group(0)
            if not re.search(r"(?:^|_)\d+$", source_id):
                continue
            segment_start = source_ids[index - 1].end() if index else header_match.end()
            segment = text[segment_start:match.start()]
            states = list(state_re.finditer(segment))
            if len(states) < 2:
                continue
            column_count = min(len(states), len(block_names))
            if column_count < 2:
                continue
            selected = states[-column_count:]
            mode = segment[:selected[0].start()].strip(" -:;,.()")
            mode = re.sub(r"\b(?:table|operating|modes?|digital|blocks?|status|different)\b", " ", mode, flags=re.IGNORECASE)
            mode = re.sub(r"\s+", " ", mode).strip()
            if not mode or len(mode) > 80:
                continue

            column_positions: List[Tuple[int, str]] = []
            for block in block_names:
                block_tokens = [token for token in re.findall(r"[a-z0-9]+", block.lower()) if len(token) > 2]
                positions = [header.lower().find(token) for token in block_tokens if header.lower().find(token) >= 0]
                if positions:
                    column_positions.append((min(positions), block))
            column_positions.sort()
            if len(column_positions) != column_count:
                continue
            for column_index, (_position, block) in enumerate(column_positions):
                state = selected[column_index].group(1).upper()
                before = segment[:selected[column_index].start()]
                optional = bool(re.search(r"\boptionally\b", before[-24:], re.IGNORECASE))
                rows.append(
                    {
                        "mode": mode,
                        "block": block,
                        "state": state,
                        "source_req_id": source_id if column_index == 0 else "",
                        "evidence": f"{path.relative_to(repo_root).as_posix()} ({'optional source state' if optional else 'source state'})",
                    }
                )
    if not rows:
        return []
    modes = []
    for row in rows:
        if row["mode"] not in modes:
            modes.append(row["mode"])
    source_mode_ids = {
        mode: next((row["source_req_id"] for row in rows if row["mode"] == mode and row["source_req_id"]), "")
        for mode in modes
    }
    for row in rows:
        row["source_req_id"] = source_mode_ids.get(row["mode"], "")
    return rows


def _complete_mode_rows(mode_rows: List[Dict[str, str]], block_names: List[str]) -> List[Dict[str, str]]:
    """Add one derived ON state for inventory blocks absent from a source mode table."""
    completed = list(mode_rows)
    existing = {(row["mode"], row["block"]) for row in completed}
    modes: List[str] = []
    for row in completed:
        if row["mode"] not in modes:
            modes.append(row["mode"])
    for mode in modes:
        mode_slug = re.sub(r"[^a-z0-9]+", "-", mode.lower()).strip("-")
        for block in block_names:
            if (mode, block) in existing:
                continue
            block_slug = re.sub(r"[^a-z0-9]+", "-", block.lower()).strip("-")
            completed.append(
                {
                    "mode": mode,
                    "block": block,
                    "state": "ON",
                    "source_req_id": f"MODE-{mode_slug}-{block_slug}",
                    "evidence": "derived default: source mode table does not identify this block as clock-gated",
                }
            )
    return completed


def _filter_mode_rows_to_srs_allocations(
    mode_rows: List[Dict[str, str]],
    allocations: Dict[str, Dict[str, str]],
) -> List[Dict[str, str]]:
    return [
        row
        for row in mode_rows
        if allocations.get(row.get("source_req_id", ""), {}).get("owning_target") == "SRS"
    ]


def _require_block_functions(block_inventory_rows: List[Dict[str, str]]) -> None:
    missing = [
        (row.get("Block") or "<unnamed block>").strip()
        for row in block_inventory_rows
        if (row.get("Block") or "").strip() and not (row.get("Function") or "").strip()
    ]
    if missing:
        raise ValueError(
            "block_inventory.csv requires a non-empty Function for every block: "
            + ", ".join(missing)
        )


def _infer_project_identifier(requirements: List[Requirement]) -> str:
    """Infer current project identifier from Stage 1 source requirement IDs.

    Source requirement families may contain a project token between the domain and numeric suffix.
    Falls back to empty string when no stable project token is found.
    """
    token_counts: Dict[str, int] = defaultdict(int)
    token_pattern = re.compile(r"^[A-Za-z0-9]+_([A-Za-z][A-Za-z0-9]+)_\d+(?:$|_)")
    for req in requirements:
        req_id = (req.source_req_id or "").strip()
        if not req_id:
            continue
        match = token_pattern.match(req_id)
        if not match:
            continue
        token = match.group(1).upper()
        if token in {"SYS", "ANA", "DIG", "XDN"}:
            continue
        token_counts[token] += 1

    if not token_counts:
        return ""

    return max(token_counts.items(), key=lambda item: item[1])[0]


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


def _classify_block_category(block: Dict[str, str], owner_types: Dict[str, Dict[str, int]]) -> str:
    bundle = block.get("Function", "")
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


def _split_blocks(mapped_blocks: str) -> List[str]:
    return [canonical_human_label(token) for token in (mapped_blocks or "").split(";") if token.strip()]


def _canonical_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def _resolve_block_name(raw_name: str, block_functions: Dict[str, str]) -> str:
    name = (raw_name or "").strip()
    if not name:
        return ""

    normalized_inventory = {_canonical_token(block): block for block in block_functions}
    key = _canonical_token(name)
    if key in normalized_inventory:
        return normalized_inventory[key]

    lowered = name.lower()
    for block in block_functions:
        block_low = block.lower()
        if block_low in lowered or lowered in block_low:
            return block

    raw_terms = _function_terms(name)
    if raw_terms:
        ranked: List[Tuple[int, str]] = []
        for block, function in block_functions.items():
            overlap = raw_terms & _function_terms(f"{block} {function}")
            if overlap:
                ranked.append((len(overlap), block))
        if ranked:
            ranked.sort(key=lambda item: (-item[0], item[1]))
            return ranked[0][1]
    return ""


def _resolve_matrix_block_name(raw_name: str, block_functions: Dict[str, str]) -> str:
    name = (raw_name or "").strip()
    if not name:
        return ""

    normalized_inventory = {_canonical_token(block): block for block in block_functions}
    key = _canonical_token(name)
    if key in normalized_inventory:
        return normalized_inventory[key]

    lowered = name.lower()
    for block in block_functions:
        block_low = block.lower()
        if lowered in block_low:
            return block
    return name


def _pick_block_by_terms(block_functions: Dict[str, str], terms: Tuple[str, ...]) -> str:
    ranked: List[Tuple[int, str]] = []
    for block, function in block_functions.items():
        text = f"{block} {function}".lower()
        score = sum(1 for term in terms if term in text)
        if score > 0:
            ranked.append((score, block))
    if not ranked:
        return ""
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return ranked[0][1]


SOURCE_STOP_WORDS = {
    "section", "paragraph", "page", "requirements", "requirement", "peculiar",
    "integration", "document", "table", "figure", "spec", "specification",
    "mode", "modes", "functional", "digital", "analog", "system",
}


def _source_terms(source: str) -> Set[str]:
    terms = set(re.findall(r"[a-z][a-z0-9_\-]+", (source or "").lower()))
    return {
        term
        for term in terms
        if term not in SOURCE_STOP_WORDS and len(term) > 2
    }


def _source_priority_owner(source: str, block_functions: Dict[str, str]) -> str:
    source_terms = _source_terms(source)
    if not source_terms:
        return ""

    ranked: List[Tuple[int, int, str]] = []
    for block, function in block_functions.items():
        block_terms = _function_terms(f"{block} {function}")
        overlap = source_terms & block_terms
        if not overlap:
            continue
        ranked.append((len(overlap), len(block_terms), block))

    if not ranked:
        return ""

    ranked.sort(key=lambda item: (-item[0], -item[1], item[2]))
    return ranked[0][2]


def _is_reset_clock_table_requirement(requirement: Requirement) -> bool:
    derivation = " ".join(
        (requirement.derivation_kind, requirement.evidence_type, requirement.notes)
    ).lower()
    source_and_statement = " ".join((requirement.source, requirement.statement)).lower()
    if "reset_table_connection" in derivation or "clock_table_connection" in derivation:
        return True
    if "table_line_info" not in derivation:
        return False
    return bool(
        re.search(r"\b\d+\s*(?:k?hz|mhz)\b", source_and_statement)
        and re.search(r"\b(?:signal|clock|reset)\b", source_and_statement)
    )


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


def _reset_clock_owner(block_functions: Dict[str, str]) -> str:
    ranked: List[Tuple[int, str]] = []
    for block, function in block_functions.items():
        text = f"{block} {function}".lower()
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


def _evidence_block_names(
    requirement: Requirement,
    req_to_block: Dict[str, str],
    block_names: List[str],
) -> List[str]:
    names = [item.strip() for item in re.split(r"[,;]", req_to_block.get(requirement.source_req_id, "")) if item.strip()]
    statement = requirement.statement.casefold()
    for block_name in block_names:
        if block_name.casefold() in statement and block_name not in names:
            names.append(block_name)
    return names


def _timing_evidence_bullets(
    requirements: List[Requirement],
    req_to_block: Dict[str, str],
    block_names: List[str],
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
        blocks = _evidence_block_names(requirement, req_to_block, block_names)
        block_text = ", ".join(blocks) if blocks else "the involved source and destination blocks"
        prefix = ", ".join(topics).capitalize() if topics else "Timing behavior"
        response = "the receiving block shall consume synchronized indications" if "synchron" in lower or "clock domain" in lower else "the involved blocks shall apply the approved condition and response"
        bullets.append(f"- {prefix} applies to {block_text}; {response}. (Covers: {requirement.source_req_id})")
    return bullets


def _data_path_evidence_bullets(
    requirements: List[Requirement],
    req_to_block: Dict[str, str],
    block_names: List[str],
) -> List[str]:
    bullets: List[str] = []
    for requirement in requirements:
        lower = requirement.statement.casefold()
        topics = []
        if "overflow" in lower:
            topics.append("overflow")
        if "underflow" in lower:
            topics.append("underflow")
        if "backpressure" in lower:
            topics.append("backpressure")
        if "throughput" in lower or "rate" in lower:
            topics.append("throughput/data rate")
        if "fifo" in lower or "buffer" in lower or "queue" in lower:
            topics.append("buffering")
        blocks = _evidence_block_names(requirement, req_to_block, block_names)
        block_text = ", ".join(blocks) if blocks else "the producing and consuming blocks"
        prefix = ", ".join(topics).capitalize() if topics else "Data-path behavior"
        bullets.append(f"- {prefix} applies to {block_text}; the producing, buffering, and consuming blocks shall define the condition and response. (Covers: {requirement.source_req_id})")
    return bullets


def _interrupt_owner(block_functions: Dict[str, str]) -> str:
    ranked: List[Tuple[int, str]] = []
    for block, function in block_functions.items():
        text = f"{block} {function}".lower()
        score = sum(1 for term in ("processor", "cpu", "microcontroller", "controller", "interrupt", "irq") if term in text)
        if score:
            ranked.append((score, block))

    if not ranked:
        return ""
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return ranked[0][1]


def _matrix_owner_by_requirement(
    interaction_rows: List[Dict[str, str]],
    block_functions: Dict[str, str],
) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for row in interaction_rows:
        req_ids = [item.strip() for item in (row.get("Requirement IDs") or "").split(";") if item.strip()]
        if not req_ids:
            continue
        from_block = _resolve_matrix_block_name(row.get("From block", ""), block_functions)
        if not from_block:
            continue
        for req_id in req_ids:
            out[req_id] = from_block
    return out


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


def _is_boot_routine_operation_requirement(requirement: Requirement) -> bool:
    return _has_explicit_source_parent(requirement.source) and bool(
        re.search(
            r"\b(?:otp\s+)?boot\s+(?:operation|routine)\b",
            requirement.statement or "",
            flags=re.IGNORECASE,
        )
    )


def _dedicated_owner_candidates(
    requirement: Requirement,
    req_to_block: Dict[str, str],
    block_functions: Dict[str, str],
) -> List[str]:
    explicit = [
        name
        for name in _split_blocks(req_to_block.get(requirement.source_req_id, ""))
        if name in block_functions and name != "Unassigned"
    ]
    if explicit:
        return explicit
    return []


def _user_specific_group_label(source: str) -> str:
    """Derive a human-readable subgroup label from Stage 1 source metadata."""
    src = (source or "").strip()
    if not src:
        return "Unclear context"

    primary = src.split(", paragraph", 1)[0].strip()
    primary = re.sub(r"\s*\(page\s*\d+\)\s*$", "", primary, flags=re.IGNORECASE).strip()

    # Prefer the text after the section identifier, keeping original wording.
    match = re.match(r"^Section\s+[0-9A-Za-z_.-]+\s+(.*)$", primary, flags=re.IGNORECASE)
    if match:
        label = match.group(1).strip(" -:\t")
        if label:
            return label

    if primary:
        return primary
    return "Unclear context"


def _non_block_context_label(source: str, context_sources: Optional[List[str]] = None) -> str:
    """Group non-block requirements under their source paragraph name."""
    direct = source_parent_title(source)
    if re.search(r"\(under\s+Section\s+", source or "", flags=re.IGNORECASE):
        return direct
    if re.match(
        r"^Section\s+[0-9A-Za-z_.-]+\s+.+?(?:,\s*paragraph|\s*\(page\s+\d+\)|$)",
        source or "",
        flags=re.IGNORECASE,
    ):
        return direct
    page_match = re.search(r"\(page\s+(\d+)\)", source or "", flags=re.IGNORECASE)
    page = int(page_match.group(1)) if page_match else None
    if context_sources and page is not None:
        candidates: List[Tuple[int, str]] = []
        for candidate_source in context_sources:
            candidate_page_match = re.search(
                r"\(page\s+(\d+)\)", candidate_source or "", flags=re.IGNORECASE
            )
            if not candidate_page_match:
                continue
            candidate_page = int(candidate_page_match.group(1))
            if candidate_page > page or page - candidate_page > 1:
                continue
            if not re.search(r"\(under\s+Section\s+", candidate_source, flags=re.IGNORECASE):
                continue
            candidates.append((candidate_page, source_parent_title(candidate_source)))
        if candidates:
            return sorted(candidates, key=lambda item: item[0])[-1][1]
    return direct


def _cascade_non_block_context_rows(
    rows: List[Dict[str, str]],
    requirements: List[Requirement],
    req_to_block: Dict[str, str],
) -> List[Dict[str, str]]:
    """Carry an explicit source parent through child user-action paragraphs."""
    statements_by_id = {
        item.source_req_id: item.statement.lstrip("-• ")
        for item in requirements
    }
    return cascade_retained_context(rows, statements_by_id, req_to_block)


DEDICATED_SOURCE_TERMS = (
    "bist", "scan", "debug", "dft", "test mode", "test", "power-up",
    "power up", "power-down", "power down", "boot", "configuration", "pad mux",
)


def _dedicated_source_label(requirement: Requirement) -> str:
    source = (requirement.source or "").strip()
    source_lower = source.lower()
    statement = requirement.statement or ""
    statement_lower = statement.lower()
    if not source:
        return ""
    if _is_boot_routine_operation_requirement(requirement):
        return ""
    otp_boot_match = re.search(r"\b(?:otp\s+)?boot\s+routine\b", statement_lower)
    if otp_boot_match:
        return statement[otp_boot_match.start():otp_boot_match.end()].strip()
    if not any(term in source_lower for term in DEDICATED_SOURCE_TERMS):
        return ""
    parent_match = re.search(
        r"\bunder\s+Section\s+[0-9A-Za-z_.-]+\s+(.+?)(?:,\s*paragraph|\s*\(page\s*\d+\)|$)",
        source,
        flags=re.IGNORECASE,
    )
    if parent_match:
        return parent_match.group(1).strip(" .-:()\t")
    if "pad mux" in source_lower:
        return "PAD Mux"
    primary = source.split(", paragraph", 1)[0].strip()
    primary = re.sub(r"\s*\(page\s*\d+\)\s*$", "", primary, flags=re.IGNORECASE).strip()
    match = re.match(r"^Section\s+[0-9A-Za-z_.-]+\s+(.*)$", primary, flags=re.IGNORECASE)
    return (match.group(1) if match else primary).strip(" -:\t") or primary


def _read_snapshot_srs_allocations(
    repo_root: Path,
    *,
    project_id: str,
    snapshot_id: str,
    requirement_ids: set[str],
) -> dict[str, dict[str, str]]:
    connection = connect(repo_root)
    try:
        rows = connection.execute(
            """SELECT req_id, snapshot_id, owning_target, spec_level, coverage_status
                 FROM requirement_allocations
                WHERE project_id = ? AND snapshot_id = ?
                ORDER BY req_id""",
            (project_id, snapshot_id),
        ).fetchall()
    finally:
        connection.close()
    if not rows:
        raise RuntimeError(
            f"SRS placement requires non-empty allocation rows for selected snapshot {snapshot_id}."
        )
    allocations: dict[str, dict[str, str]] = {}
    for row in rows:
        req_id = str(row["req_id"] or "").strip()
        if not req_id or req_id in allocations:
            raise RuntimeError(
                f"SRS placement allocation data is missing or duplicated for requirement {req_id or '<empty>'}."
            )
        allocations[req_id] = {key: str(row[key] or "").strip() for key in row.keys()}
    if set(allocations) != requirement_ids:
        missing = sorted(requirement_ids - set(allocations))
        extra = sorted(set(allocations) - requirement_ids)
        raise RuntimeError(
            f"SRS placement allocation rows do not match selected snapshot {snapshot_id}: "
            f"missing={missing[:10]}, extra={extra[:10]}"
        )
    invalid = sorted(req_id for req_id, row in allocations.items() if not row["owning_target"])
    if invalid:
        raise RuntimeError(
            "SRS placement allocation rows have no authoritative owning_target: "
            + ", ".join(invalid[:10])
        )
    return allocations


def _is_srs_allocated(requirement: Requirement, allocations: dict[str, dict[str, str]]) -> bool:
    """Select SRS content from policy-authorized propagation targets.

    The owning target identifies the level that authors a requirement; it does
    not, by itself, describe every level that must carry its upstream context.
    Use the snapshot's required and contextual target sets so this decision is
    independent of project-specific ID namespaces and block names.
    """
    allocation = allocations[requirement.source_req_id]
    targets = {
        value.strip()
        for field in ("required_downstream_targets", "allowed_contextual_targets")
        for value in allocation.get(field, "").split(";")
        if value.strip()
    }
    return allocation.get("owning_target", "").strip() == "SRS"


def _deduplicate_authored_requirement_blocks(lines: List[str]) -> List[str]:
    """Keep the first authored block for each SRS ID while preserving distinct evidence."""
    header = re.compile(r"^\*\*\[(SRS-REQ-\d{3})\] Requirement:\*\*$")
    emitted: set[str] = set()
    result: List[str] = []
    index = 0
    while index < len(lines):
        match = header.match(lines[index].strip())
        if not match:
            result.append(lines[index])
            index += 1
            continue
        end = index + 1
        while end < len(lines) and not header.match(lines[end].strip()):
            end += 1
        if match.group(1) not in emitted:
            emitted.add(match.group(1))
            result.extend(lines[index:end])
        index = end
    return result


def _block_navigation_target(anchor: str, rendered: bool, label: str = "Jump") -> str:
    if not rendered:
        return "N/A"
    return f"[{label}](#{anchor})"


def _source_body_lines(requirement: Requirement) -> List[str]:
    payload = _statement_payload(requirement.statement).strip()
    payload = re.sub(r"\s+•\s*", "\n- ", payload)
    payload = re.sub(r"(?<!^)\s+(?=\d+(?:\.\d+)+\s+[A-Z])", "\n", payload)
    payload = re.sub(r":\s+(?=-\s+)", ":\n", payload)
    lines = payload.splitlines() or [payload]
    rendered: List[str] = []
    numbered_subsection_active = False
    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        if cleaned.startswith("• "):
            cleaned = "- " + cleaned[2:].strip()
        is_section_heading = bool(re.match(r"^\d+(?:\.\d+)+\s+[^:]+:\s*$", cleaned))
        is_list_item = not is_section_heading and bool(
            re.match(r"^(?:[-*+]\s+|\d+(?:\.\d+)+[.:]?\s+|\d+[.)]\s+)", cleaned)
        )
        if is_section_heading:
            if rendered and rendered[-1].strip():
                rendered.append("")
            rendered.append(cleaned)
            numbered_subsection_active = True
            continue
        if is_list_item:
            if rendered and rendered[-1].strip() and not re.match(
                r"^(?:[-*+]\s+|\d+(?:\.\d+)+[.:]?\s+|\d+[.)]\s+)",
                rendered[-1].strip(),
            ):
                rendered.append("")
            rendered.append(f"    {cleaned}" if numbered_subsection_active else cleaned)
        elif rendered and rendered[-1].lstrip().startswith(("- ", "* ", "+ ")):
            rendered[-1] = rendered[-1].rstrip() + " " + cleaned
        else:
            rendered.append(cleaned)
    return rendered or [payload]


def _function_terms(text: str) -> Set[str]:
    terms = set(re.findall(r"[a-z][a-z0-9]+", (text or "").lower()))
    return {
        term[:-1] if term.endswith("s") and len(term) > 4 else term
        for term in terms
        if term not in FUNCTION_STOP_WORDS and len(term) > 2
    }


def _function_supports_requirement(requirement: Requirement, function: str) -> bool:
    return bool(
        _function_terms(_statement_payload(requirement.statement))
        & _function_terms(function)
    )


def _map_requirements_to_blocks(
    requirements: List[Requirement],
    req_to_block: Dict[str, str],
    block_functions: Dict[str, str],
    matrix_requirement_ids: Set[str],
) -> Tuple[Dict[str, List[Requirement]], List[Requirement]]:
    by_block: Dict[str, List[Requirement]] = defaultdict(list)
    unmapped: List[Requirement] = []
    reset_clock_owner = _reset_clock_owner(block_functions)
    interrupt_owner = _interrupt_owner(block_functions)

    for req in requirements:
        if req.source_req_id in matrix_requirement_ids:
            continue

        if _dedicated_source_label(req):
            supported_blocks = _dedicated_owner_candidates(req, req_to_block, block_functions)
            mapped_blocks = [
                name
                for name in _split_blocks(req_to_block.get(req.source_req_id, ""))
                if name in block_functions and name != "Unassigned"
            ]
            matched_blocks = mapped_blocks or supported_blocks
            if not matched_blocks:
                unmapped.append(req)
                continue

        if req.source_section_owner in block_functions:
            matched_blocks = [req.source_section_owner]
        elif reset_clock_owner and _is_reset_clock_table_requirement(req):
            matched_blocks = [reset_clock_owner]
        elif interrupt_owner and _is_interrupt_table_requirement(req):
            matched_blocks = [interrupt_owner]
        else:
            mapped_blocks = _split_blocks(req_to_block.get(req.source_req_id, ""))
            explicit_blocks = [
                name
                for name in mapped_blocks
                if name in block_functions and name != "Unassigned"
            ]
            matched_blocks = explicit_blocks or [
                name
                for name in mapped_blocks
                if name in block_functions and name != "Unassigned"
                and _function_supports_requirement(req, block_functions[name])
            ]
        if matched_blocks:
            for block_name in matched_blocks:
                by_block[block_name].append(req)
        else:
            unmapped.append(req)

    return by_block, unmapped


def _statement_payload(text: str) -> str:
    t = (text or "").strip()
    low = t.lower()
    prefix = "the system shall satisfy the following behavior:"
    if low.startswith(prefix):
        t = t[len(prefix):].strip()
    # Remove both bracketed and plain leading requirement labels before rendering authored prose.
    t = re.sub(r"^\s*\[[^\]]+\]\s*(?:Requirement\s*:\s*)?", "", t, flags=re.IGNORECASE)
    if SOURCE_REQUIREMENT_IDS:
        source_id_pattern = "|".join(
            re.escape(source_id)
            for source_id in sorted(SOURCE_REQUIREMENT_IDS, key=len, reverse=True)
        )
        t = re.sub(rf"\b(?:{source_id_pattern})\b\s*:?", "", t)
    return _normalize_block_references(t.strip())


def _reset_clock_payload(requirement: Requirement) -> str:
    payload = _statement_payload(requirement.statement).rstrip(".")
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


def _split_source_list(payload: str) -> Tuple[str, List[str]]:
    normalized = re.sub(r"\s*•\s*", "\n• ", payload)
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


def _atomic_block_statement(block_name: str, requirement: Requirement) -> str:
    payload = (
        _reset_clock_payload(requirement)
        if _is_reset_clock_table_requirement(requirement)
        else _statement_payload(requirement.statement).rstrip(".")
    )
    if payload:
        lead, list_items = _split_source_list(payload)
        rendered = [f"The {block_name} block shall implement: {lead}."]
        if list_items:
            rendered.append("")
            for item in list_items:
                if re.match(r"^\d+(?:\.\d+)+\s+", item) and rendered[-1].strip():
                    rendered.append("")
                rendered.append(item)
        return "\n".join(rendered)
    return f"The {block_name} block shall implement: behavior defined by mapped upstream requirement evidence."


def _extract_requirement_label_and_clean_statement(statement: str) -> Tuple[str, str]:
    """Return `(label, cleaned_statement)` for tagged requirement prefixes.

    The tag family is discovered from the active source artifacts.
    """
    text = (statement or "").strip()
    if not text:
        return "", ""

    norm_prefix = re.compile(r"^\s*the system shall satisfy the following behavior:\s*", re.IGNORECASE)
    text_wo_norm = norm_prefix.sub("", text, count=1).strip()

    pattern = re.compile(
        r"^\s*(\[[^\]]+\]|(?:[A-Za-z]{2,}[A-Za-z0-9]*_[A-Za-z0-9_]*\d+|(?:SYS|ANA|DIG|XDN)-RQ-\d+))\s*"
        r"(?:requirement\s*)?:\s*",
        re.IGNORECASE,
    )
    match = pattern.match(text_wo_norm)
    if not match:
        return "", text

    label = match.group(1).strip()
    cleaned = pattern.sub("", text_wo_norm, count=1).strip()
    return label, cleaned


def _normalized_req_token(text: str) -> str:
    """Normalize requirement tokens for equivalence checks.

    Removes non-alphanumeric characters and lowercases so formatting variants
    compare equal.
    """
    return re.sub(r"[^a-zA-Z0-9]", "", (text or "")).lower()


def _block_summary_sentence(block_name: str, requirements: List[Requirement]) -> str:
    payloads: List[str] = []
    seen: Set[str] = set()
    for req in requirements:
        text = _statement_payload(req.statement).strip().rstrip(".")
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        payloads.append(text)

    if not payloads:
        return (
            f"The {block_name} block coordinates its declared interfaces and shall implement "
            "mapped system behavior defined by upstream requirement evidence."
        )

    highlights = payloads[:3]
    return (
        f"The {block_name} block coordinates its declared interfaces and shall implement system behavior including: "
        + "; ".join(highlights)
        + "."
    )


def _read_function_decomposition(path: Path) -> List[Tuple[str, str, str]]:
    if not path.exists():
        return []
    out: List[Tuple[str, str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        if "Top function" in line or "---" in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= 3:
            out.append((parts[0], parts[1], parts[2]))
    return out


def _extract_crosscheck_decision(path: Path) -> str:
    if not path.exists():
        return "unknown"
    text = path.read_text(encoding="utf-8")
    match = re.search(r"Decision:\s*([a-zA-Z\-]+)", text)
    if not match:
        return "unknown"
    return match.group(1).strip().lower()


def _to_text(value: object) -> str:
    """Normalize arbitrary values to a single text line for markdown rendering."""
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
    if re.match(r"^\d+(?:\.\d+)+\s+", text):
        return False
    if re.match(r"^\[SRS-REQ-\d{3}\]\s+Requirement:\s*$", text):
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
    """Insert a blank line before each independent Markdown paragraph.

    This improves paragraph spacing persistence in markdown-to-docx conversion
    without changing templates.
    """
    if not lines:
        return lines

    out: List[str] = []
    for idx, line in enumerate(lines):
        text = _to_text(line).strip()
        is_list_item = bool(re.match(r"^(?:[-*+]\s+|\d+(?:\.\d+)+[.:]?\s+|\d+[.)]\s+|•\s+)", text))
        previous_text = _to_text(out[-1]).strip() if out else ""
        previous_is_list_item = bool(re.match(r"^(?:[-*+]\s+|\d+(?:\.\d+)+[.:]?\s+|\d+[.)]\s+|•\s+)", previous_text))
        if text and is_list_item and out and previous_text and not previous_is_list_item:
            out.append("")
            previous_text = ""
        if text and out and (is_list_item or _is_prose_paragraph_line(text)):
            previous = _to_text(out[-1]).strip()
            if previous and not (is_list_item and previous_is_list_item) and (
                _is_prose_paragraph_line(previous)
                or previous.startswith(("#", "Covers:", "Outputs:", "Inputs:", "General functional description:"))
            ):
                out.append("")
        out.append(line)

    return out


def _insert_visible_paragraph_spacers(lines: List[str]) -> List[str]:
    """Insert explicit spacer paragraphs between prose blocks.

    Markdown blank lines can be visually collapsed by some renderers and DOCX styles.
    Adding a non-breaking-space paragraph keeps a visible vertical gap after conversion.
    """
    if not lines:
        return lines

    out: List[str] = []
    idx = 0
    n = len(lines)
    while idx < n:
        line = lines[idx]
        if _to_text(line).strip() != "":
            out.append(line)
            idx += 1
            continue

        blank_start = idx
        while idx < n and _to_text(lines[idx]).strip() == "":
            idx += 1
        blank_end = idx  # first non-blank after run or n

        prev_idx = blank_start - 1
        while prev_idx >= 0 and _to_text(lines[prev_idx]).strip() == "":
            prev_idx -= 1
        next_idx = blank_end
        while next_idx < n and _to_text(lines[next_idx]).strip() == "":
            next_idx += 1

        prev_line = lines[prev_idx] if prev_idx >= 0 else ""
        next_line = lines[next_idx] if next_idx < n else ""
        next_is_requirement = bool(re.match(r"^\[SRS-REQ-\d{3}\]\s+Requirement:\s*$", _to_text(next_line).strip()))
        needs_spacer = (
            (_is_prose_paragraph_line(prev_line) and (
                next_line.lstrip().startswith("#") or _is_prose_paragraph_line(next_line)
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
    """Keep Requirement ID blocks visually separated for rendered outputs."""
    out: List[str] = []
    for line in lines:
        if re.match(r"^\[SRS-REQ-\d{3}\]\s+Requirement:\s*$", _to_text(line).strip()):
            if out and _to_text(out[-1]).strip():
                out.append("")
        if re.match(r"^\s*Covers:\s*\S+\s*$", _to_text(line).strip()):
            if out and _to_text(out[-1]).strip():
                out.append("")
        if re.match(r"^\[SRS-REQ-\d{3}\]\s+Requirement:\s*$", _to_text(line).strip()):
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
    return normalize_authored_requirement_blocks(lines, ("SRS",))


def _ensure_subparagraph_heading_spacing(lines: List[str]) -> List[str]:
    """Insert visible spacing before numbered sub-paragraph headings."""
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
    """Ensure markdown table blocks are isolated for stable DOCX rendering."""
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
    """Return ordered heading metadata as (level, title, anchor, section_number)."""
    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
    used: Dict[str, int] = defaultdict(int)
    used_anchors: Set[str] = set()
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
        base = _heading_anchor_slug(title)

        anchor_base = explicit_id_match.group(1) if explicit_id_match else base
        used[anchor_base] += 1
        anchor = anchor_base if used[anchor_base] == 1 else f"{anchor_base}-{used[anchor_base] - 1}"
        while anchor in used_anchors:
            used[anchor_base] += 1
            anchor = f"{anchor_base}-{used[anchor_base] - 1}"
        used_anchors.add(anchor)
        section_number = ""
        token_match = re.match(r"^(\d+(?:\.\d+)*)\.?", title)
        if token_match:
            section_number = token_match.group(1)

        registry.append((level, title, anchor, section_number))

    return registry


def _heading_anchor_slug(text: str) -> str:
    base = re.sub(r"[^a-z0-9\s-]", "", (text or "").lower())
    return re.sub(r"\s+", "-", base).strip("-") or "section"


def _apply_heading_registry_anchors(lines: List[str], registry: List[Tuple[int, str, str, str]]) -> List[str]:
    """Keep emitted heading attributes aligned with the deduplicated registry."""
    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
    anchored_heading_re = re.compile(r"\s*\{#[a-zA-Z0-9_-]+\}\s*$")
    registry_index = 0
    normalized: List[str] = []

    for line in lines:
        if not heading_re.match(_to_text(line)):
            normalized.append(line)
            continue
        anchor = registry[registry_index][2]
        registry_index += 1
        if anchored_heading_re.search(line):
            normalized.append(anchored_heading_re.sub(f" {{#{anchor}}}", line))
        else:
            normalized.append(f"{line.rstrip()} {{#{anchor}}}")

    return normalized


def _resolve_final_heading_anchor(
    target: str,
    registry: List[Tuple[int, str, str, str]],
) -> str | None:
    normalized_target = target.strip().lstrip("#").casefold()
    for _level, _title, anchor, _section_number in registry:
        if anchor.casefold() == normalized_target:
            return anchor
    for _level, title, anchor, _section_number in registry:
        if _heading_anchor_slug(title).casefold() == normalized_target:
            return anchor
    return None


def _rewrite_internal_links(
    lines: List[str],
    registry: List[Tuple[int, str, str, str]],
) -> tuple[List[str], int, int]:
    """Bind internal links to final anchors, replacing unresolved targets with N/A."""
    link_re = re.compile(r"\[([^\]]+)\]\(#([^)]+)\)")
    resolved_count = 0
    non_link_count = 0
    rewritten: List[str] = []
    for line in lines:
        def replace(match: re.Match[str]) -> str:
            nonlocal resolved_count, non_link_count
            anchor = _resolve_final_heading_anchor(match.group(2), registry)
            if anchor is None:
                non_link_count += 1
                return "N/A"
            resolved_count += 1
            return f"[{match.group(1)}](#{anchor})"

        rewritten.append(link_re.sub(replace, line))
    return rewritten, resolved_count, non_link_count


def _structured_srs_low_power_records(repo_root: Path, function_rows: List[Tuple[str, str, str]]) -> List[Mapping[str, object]]:
    records = read_stage2_descriptive_evidence(repo_root)
    if records:
        return records
    return architecture_records_from_function_rows(function_rows)


def _power_sequence_summary(records: List[Mapping[str, object]]) -> List[str]:
    """Summarize entry, exit, and wake-up behavior from approved domain evidence."""
    power_records = [
        record for record in records
        if str(record.get("evidence_kind") or record.get("record_type") or "").casefold() == "power_domain"
        or "power-domain" in str(record.get("source") or "").casefold()
    ]
    always_on = []
    switchable = []
    otp_supply = False
    for record in power_records:
        statement = str(record.get("statement") or "")
        domain_match = re.match(r"\s*([^:]+):", statement)
        domain_name = domain_match.group(1).strip() if domain_match else "the domain"
        if re.search(r"\balways[- ]on\b", statement, re.IGNORECASE):
            always_on.append(domain_name)
        if re.search(r"\bswitchable\b", statement, re.IGNORECASE):
            switchable.append(domain_name)
        if "otp memory" in statement.casefold() and "program" in statement.casefold():
            otp_supply = True

    summary: List[str] = []
    if always_on:
        summary.append(
            "Entry / power-up: Always-on domains remain active under hardware control and are described as never powered down."
        )
    if otp_supply:
        summary.append(
            "The always-on OTP supply remains available for OTP programming operations."
        )
    if switchable:
        if not always_on:
            summary.append(
                "Entry / power-up: The switchable domain is software-controlled; the approved domain description does not specify its power-up timing."
            )
        summary.append(
            "Exit / power-down: The switchable domain may be powered down while idle, with the source assigning its control to software."
        )
        summary.append(
            "Wake-up / restore: The available evidence identifies software as the controller for returning the switchable domain to active use; no retention, state-restore, or wake-up timing is specified in the approved domain descriptions."
        )
    return summary


def _render_srs_low_power_section(
    lines: List[str],
    records: List[Mapping[str, object]],
    *,
    repo_root: Path,
) -> None:
    grouped, _audit = assemble_low_power_descriptive(records, repo_root=repo_root, profile="srs")
    lines.extend(render_low_power_topics(grouped))
    for topic in ("Entry, exit, wake-up, and restore", "Sequencing and domain control"):
        if topic not in grouped:
            lines.append(f"#### {topic}")
            if topic == "Entry, exit, wake-up, and restore":
                sequence_summary = _power_sequence_summary(records)
                lines.extend(f"- {entry}" for entry in sequence_summary)
                if not sequence_summary:
                    lines.append("- needed clarification from user")
            else:
                lines.append("- needed clarification from user")
            lines.append("")


def _build_srs_ids(requirements: List[Requirement]) -> Dict[str, str]:
    authored_counter = 0
    out: Dict[str, str] = {}

    for req in requirements:
        authored_counter += 1
        out[req.source_req_id] = f"SRS-REQ-{authored_counter:03d}"
    return out


def _connection_matrix_srs_ids(
    interaction_rows: List[Dict[str, str]],
    srs_id_map: Dict[str, str],
) -> Dict[str, str]:
    """Assign matrix IDs without colliding with Stage 1-authored SRS IDs."""
    out: Dict[str, str] = {}
    used_ids = set(srs_id_map.values())
    authored_counter = max(
        (int(req_id.rsplit("-", 1)[1]) for req_id in used_ids),
        default=0,
    )
    for row in interaction_rows:
        requirement_ids = (row.get("Requirement IDs") or "").strip()
        if not requirement_ids or not row.get("From block") or not row.get("To block"):
            continue
        for requirement_id in [item.strip() for item in requirement_ids.split(";") if item.strip()]:
            if requirement_id in out:
                continue
            if requirement_id in srs_id_map:
                out[requirement_id] = srs_id_map[requirement_id]
                continue
            authored_counter += 1
            authored_id = f"SRS-REQ-{authored_counter:03d}"
            out[requirement_id] = authored_id
            used_ids.add(authored_id)
    return out


def _write_traceability_csv(
    output_path: Path,
    requirements: List[Requirement],
    srs_id_map: Dict[str, str],
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
                "srs_req_id",
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
                    srs_id_map[req.source_req_id],
                    req.source_req_id,
                    req.domain,
                    req.statement,
                    owning_block,
                    "artifacts/stage1_requirements/requirements_summary.csv",
                    _verification_method(req.requirement_type, req.domain),
                    _acceptance_criteria({"value_range_condition": req.value_range_condition}),
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


def _append_matrix_only_traceability_rows(
    output_path: Path,
    interaction_rows: List[Dict[str, str]],
    connection_matrix_srs_ids: Dict[str, str],
    stage1_source_ids: Set[str],
    allocation_by_source: Dict[str, Dict[str, str]],
    snapshot_id: str,
) -> int:
    """Record matrix-only source IDs that are authored directly in the SRS."""
    rows_written = 0
    with output_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        for row in interaction_rows:
            from_block = (row.get("From block") or "").strip()
            to_block = (row.get("To block") or "").strip()
            for source_req_id in (item.strip() for item in (row.get("Requirement IDs") or "").split(";")):
                if not source_req_id or source_req_id in stage1_source_ids:
                    continue
                allocation = allocation_by_source.get(source_req_id, {})
                if allocation.get("owning_target") != "SRS":
                    continue
                srs_req_id = connection_matrix_srs_ids.get(source_req_id)
                if not srs_req_id:
                    continue
                writer.writerow(
                    [
                        srs_req_id,
                        source_req_id,
                        "XDN",
                        f"The {from_block} block shall be connected to the {to_block} block.",
                        from_block or "Unassigned",
                        "artifacts/stage2_mirco_arc/interaction_matrix.csv",
                        "inspection+test",
                        "Connection is present and operates as specified.",
                        "draft",
                        "source=Stage 2 connection matrix",
                        snapshot_id,
                        allocation.get("allocation_class", ""),
                        allocation.get("owning_target", ""),
                        allocation.get("lineage_mode", ""),
                        allocation.get("source_origin_req_ids", ""),
                        allocation.get("hierarchy_parent_req_ids", ""),
                        allocation.get("owning_domain", ""),
                    ]
                )
                rows_written += 1
    return rows_written


def _append_mode_traceability_rows(
    output_path: Path,
    mode_rows: List[Dict[str, str]],
    srs_id_map: Dict[str, str],
    existing_source_ids: Set[str],
    allocation_by_source: Dict[str, Dict[str, str]],
    snapshot_id: str,
) -> int:
    rows_written = 0
    emitted: Set[str] = set()
    with output_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        for row in mode_rows:
            source_req_id = row.get("source_req_id", "").strip()
            if not source_req_id or source_req_id in emitted or source_req_id in existing_source_ids:
                continue
            allocation = allocation_by_source.get(source_req_id, {})
            if allocation.get("owning_target") != "SRS" or source_req_id not in srs_id_map:
                continue
            emitted.add(source_req_id)
            writer.writerow(
                [
                    srs_id_map[source_req_id],
                    source_req_id,
                    "SYS",
                    f"In {row['mode']} mode, the {row['block']} block shall be {row['state']}",
                    row["block"],
                    row.get("evidence", ""),
                    "inspection+test",
                    f"The {row['block']} block state is {row['state']} in the {row['mode']} operating mode.",
                    "draft",
                    "operating mode state table",
                    snapshot_id,
                    allocation.get("allocation_class", ""),
                    allocation.get("owning_target", ""),
                    allocation.get("lineage_mode", ""),
                    allocation.get("source_origin_req_ids", ""),
                    allocation.get("hierarchy_parent_req_ids", ""),
                    allocation.get("owning_domain", ""),
                ]
            )
            rows_written += 1
    return rows_written


def _write_srs_markdown(
    output_path: Path,
    template_path: Path,
    source_spec: str,
    project_name: str,
    document_author: str,
    requirements: List[Requirement],
    srs_id_map: Dict[str, str],
    req_to_block: Dict[str, str],
    block_inventory_rows: List[Dict[str, str]],
    interface_rows: List[Dict[str, str]],
    source_port_rows: List[Dict[str, str]],
    interaction_rows: List[Dict[str, str]],
    connection_matrix_srs_ids: Dict[str, str],
    function_rows: List[Tuple[str, str, str]],
    descriptive_records: List[Mapping[str, object]],
    block_requirements: Dict[str, List[Requirement]],
    unmapped_requirements: List[Requirement],
    user_specific_requirements: List[Requirement],
    non_block_context_rows: List[Dict[str, str]],
    crosscheck_decision: str,
    missing_inputs: List[Path],
    mode_rows: List[Dict[str, str]],
    approved_srs_source_ids: Set[str],
    snapshot_id: str,
    contract_fingerprint: str,
    document_version: str,
    catalog_entries: Optional[List[Dict[str, str]]] = None,
    catalog_findings: Optional[List[str]] = None,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    render_block_functions = {
        (row.get("Block") or "").strip(): (row.get("Function") or "").strip()
        for row in block_inventory_rows
        if (row.get("Block") or "").strip()
    }
    render_reset_clock_owner = _reset_clock_owner(render_block_functions)
    retained_source_ids = {
        row.get("Requirement ID", "").strip()
        for row in non_block_context_rows
        if row.get("Requirement ID", "").strip()
    }

    template_text = template_path.read_text(encoding="utf-8")
    marker_toc = "__AUTO_TOC__"
    marker_nav = "__AUTO_NAV_TABLES__"
    marker_tot = "__AUTO_TABLE_OF_TABLES__"

    def _parse_template_sections(raw: str) -> List[Tuple[int, str, List[str]]]:
        lines_in = raw.splitlines()
        start_idx = -1
        end_idx = len(lines_in)

        for idx, line in enumerate(lines_in):
            if line.strip().lower() == "## srs document format":
                start_idx = idx + 1
                break

        if start_idx < 0:
            return []

        for idx in range(start_idx, len(lines_in)):
            line = lines_in[idx].strip().lower()
            if line.startswith("## required csv output format"):
                end_idx = idx
                break

        scoped = lines_in[start_idx:end_idx]
        sections: List[Tuple[int, str, List[str]]] = []
        current_level = 0
        current_title = ""
        current_body: List[str] = []

        heading_re = re.compile(r"^(#{2,6})\s+(.+?)\s*$")
        numbered_re = re.compile(r"^\d+(?:\.\d+)*\.")

        for line in scoped:
            match = heading_re.match(line)
            if match:
                title = match.group(2).strip()
                if numbered_re.match(title):
                    if current_title:
                        sections.append((current_level, current_title, current_body))
                    current_level = len(match.group(1))
                    current_title = title
                    current_body = []
                    continue

            if current_title:
                current_body.append(line)

        if current_title:
            sections.append((current_level, current_title, current_body))
        return sections

    def _anchor_slug(text: str) -> str:
        return _heading_anchor_slug(text)

    def _section_number(title: str) -> str:
        token = title.split()[0]
        return token.rstrip(".")

    def _normalized_heading_level(title: str, fallback_level: int) -> int:
        token_match = re.match(r"^(\d+(?:\.\d+)*)\.?", title)
        if not token_match:
            return min(6, max(2, fallback_level))
        depth = len(token_match.group(1).split("."))
        return min(6, max(2, depth + 1))

    def _append_section_with_template_body(lines_out: List[str], level: int, title: str, body: List[str]) -> None:
        heading_level = _normalized_heading_level(title, level)
        lines_out.append(f"{'#' * heading_level} {title} {{#{_anchor_slug(title)}}}")
        if body:
            body_text = [_to_text(item) for item in body]
            while body_text and not body_text[0].strip():
                body_text = body_text[1:]
            while body_text and not body_text[-1].strip():
                body_text = body_text[:-1]
            lines_out.extend(body_text)
        lines_out.append("")

    template_sections = _parse_template_sections(template_text)
    if not template_sections:
        raise ValueError("SRS template is missing a parsable 'SRS document format' numbered section scaffold")

    grouped: Dict[str, List[Requirement]] = defaultdict(list)
    for req in requirements:
        grouped[req.domain].append(req)

    domain_title = {
        "SYS": "System",
        "ANA": "Analog",
        "DIG": "Digital",
        "XDN": "Cross-domain",
    }

    support_sections, support_audit = compose_srs_support_content(
        project_name, snapshot_id, catalog_entries or [], catalog_findings or [],
        _structured_srs_low_power_records(_resolve_repo_root(), function_rows),
    )
    output_path.with_name("descriptive_srs_content_audit.json").write_text(
        json.dumps(support_audit, indent=2, ensure_ascii=True) + "\n", encoding="utf-8",
    )
    block_category = {
        entry["block"]: entry["category"] for entry in (catalog_entries or [])
    }
    analog_blocks = [
        block_name
        for block_name, category in block_category.items()
        if category in {BLOCK_CLASS_ANALOG, BLOCK_CLASS_POWER}
    ]
    digital_blocks = [
        block_name
        for block_name, category in block_category.items()
        if category == BLOCK_CLASS_DIGITAL
    ]
    def _interface_rows_for_block(block_name: str) -> List[Dict[str, str]]:
        block_terms = set(re.findall(r"[a-z0-9]+", block_name.lower()))
        return [
            row
            for row in interface_rows
            if block_terms
            and block_terms.intersection(set(re.findall(r"[a-z0-9]+", (row.get("Owner", "") or "").lower())))
        ]

    def _render_interface_catalog_table(rows: List[Dict[str, str]]) -> List[str]:
        if not rows:
            return []
        rendered = [
            "Interface catalog evidence:",
            "| Interface | Direction | Type | Owner | Purpose |",
            "|---|---|---|---|---|",
        ]
        for row in rows:
            values = [
                row.get("Interface", ""),
                row.get("Direction", ""),
                row.get("Type", ""),
                row.get("Owner", ""),
                row.get("Purpose", "").replace("|", "\\|"),
            ]
            rendered.append("| " + " | ".join(values) + " |")
        return rendered

    def _is_power_domain_record(record: Mapping[str, object]) -> bool:
        evidence_kind = str(record.get("evidence_kind") or record.get("record_type") or "").casefold()
        statement = str(record.get("statement") or "").casefold()
        source = str(record.get("source") or "").casefold()
        return (
            evidence_kind == "power_domain"
            or "power-domain" in source
            or "included block(s):" in statement
            or "power domain architecture" in statement
            or "power domain (pd)" in statement
            or statement.startswith("retention domain:")
            or "always-on domain" in statement
            or "domain that is always powered" in statement
        )

    def _non_power_architecture_records(records: List[Mapping[str, object]]) -> List[Mapping[str, object]]:
        return [record for record in records if not _is_power_domain_record(record)]
    interaction_summary = [
        f"{r.get('From block', '')} -> {r.get('To block', '')} via {r.get('Signal/control', '')} (trigger: {r.get('Trigger', '')})"
        for r in interaction_rows
        if r.get("From block", "") and r.get("To block", "")
    ]
    connection_matrix_requirements = [
        r for r in interaction_rows
        if r.get("Requirement IDs", "")
        and r.get("From block", "")
        and r.get("To block", "")
        and any(
            source_req_id.strip() in approved_srs_source_ids
            for source_req_id in (r.get("Requirement IDs") or "").split(";")
            if source_req_id.strip()
        )
    ]

    system_count = len(grouped.get("SYS", []))
    analog_count = len(grouped.get("ANA", []))
    digital_count = len(grouped.get("DIG", []))
    cross_count = len(grouped.get("XDN", []))

    block_index_entries: List[Tuple[int, str, int, int]] = []
    rendered_block_sections = False
    preview_section_counter = 1
    preview_emitted_source_ids: Set[str] = set()
    for row in block_inventory_rows:
        block = (row.get("Block") or "").strip()
        if not block:
            continue
        reqs = [
            req
            for req in block_requirements.get(block, [])
            if req.source_req_id not in preview_emitted_source_ids
        ]
        if not reqs:
            continue
        preview_emitted_source_ids.update(req.source_req_id for req in reqs)
        req_numbers = [int(srs_id_map[req.source_req_id].rsplit("-", 1)[1]) for req in reqs]
        start_id = min(req_numbers)
        end_id = max(req_numbers)
        block_index_entries.append((preview_section_counter, block, start_id, end_id))
        preview_section_counter += 1

    lines: List[str] = []
    lines.append("# System Requirements Specification {#system-requirements-specification}")
    lines.append("")
    lines.append(f"## {project_name} {{#project-name}}")
    lines.append("")
    lines.append(f"Author: {document_author}")
    lines.append("")
    lines.append(f"Date: {today}")
    lines.append(f"Snapshot ID: {snapshot_id}")
    lines.append(f"Downstream contract fingerprint: {contract_fingerprint}")
    lines.append(f"Source specification: {source_spec}")
    lines.append("")

    domain_order = ["SYS", "ANA", "DIG", "XDN"]
    mapped_source_ids: Set[str] = set()
    for req_list in block_requirements.values():
        for req in req_list:
            mapped_source_ids.add(req.source_req_id)
    mapped_source_ids.update(connection_matrix_srs_ids.keys())
    non_block_source_ids = {
        row.get("Requirement ID", "").strip()
        for row in non_block_context_rows
        if row.get("Requirement ID", "").strip()
    }

    for level, title, body in template_sections:
        sec_num = _section_number(title)
        if sec_num in {"3.2", "3.3", "3.4", "3.5", "3.6", "3.7"}:
            continue
        if sec_num.startswith("9."):
            continue
        if sec_num == "8.4" or sec_num.startswith("8.4."):
            continue

        # Artifact-synthesized sections replace template directive text.
        if not approved_srs_source_ids or sec_num in SRS_INTRODUCTORY_SECTIONS or sec_num in {"3.1", "3.3", "4.1", "5.1", "5.5", "6.3", "6.4"}:
            _append_section_with_template_body(lines, level, title, [])
        else:
            _append_section_with_template_body(lines, level, title, body)

        if sec_num == "0.1":
            lines.append(marker_toc)
            lines.append("")

        elif sec_num in SRS_INTRODUCTORY_SECTIONS:
            for paragraph in support_sections[sec_num]:
                lines.extend([paragraph, ""])

        elif sec_num == "2.5":
            lines.extend(shared_category_conventions_markdown())

        elif sec_num == "0.2":
            lines.append("#### Table 3. Section navigation index {#table-3-section-navigation-index}")
            lines.append("| Section | Paragraph anchor | Internal link | Page (rendered PDF) |")
            lines.append("|---|---|---|---|")
            lines.append(marker_nav)
            lines.append("")

            lines.append("#### Table 4. Block navigation index {#table-4-block-navigation-index}")
            lines.append("| Block | Paragraph anchor | Internal link | Requirement IDs |")
            lines.append("|---|---|---|---|")
            if block_index_entries:
                for sec_idx, block, req_start, req_end in block_index_entries:
                    anchor = _anchor_slug(f"9.{sec_idx} {block}")
                    req_range = (
                        f"SRS-REQ-{req_start:03d}"
                        if req_start == req_end
                        else f"SRS-REQ-{req_start:03d} to SRS-REQ-{req_end:03d}"
                    )
                    lines.append(f"| {block} | 9.{sec_idx} | {_block_navigation_target(anchor, rendered_block_sections)} | {req_range} |")
            else:
                lines.append("| N/A | N/A | N/A | N/A |")
            lines.append("")

            lines.append("#### Table 5. Requirement paragraph index by block {#table-5-requirement-paragraph-index-by-block}")
            lines.append("| Requirement group | Paragraph anchor | Internal link | Page (rendered PDF) |")
            lines.append("|---|---|---|---|")
            if block_index_entries:
                for sec_idx, block, req_start, req_end in block_index_entries:
                    anchor = _anchor_slug(f"9.{sec_idx} {block}")
                    req_range = (
                        f"SRS-REQ-{req_start:03d}"
                        if req_start == req_end
                        else f"SRS-REQ-{req_start:03d} to SRS-REQ-{req_end:03d}"
                    )
                    lines.append(f"| {req_range} | 9.{sec_idx} | {_block_navigation_target(anchor, rendered_block_sections, block)} | Auto |")
            else:
                lines.append("| N/A | N/A | N/A | N/A |")
            lines.append("")

        elif sec_num == "0.3":
            lines.append("#### Table 1. Version history {#table-1-version-history}")
            lines.extend(document_version_history_markdown(
                output_path, snapshot_id, document_version, today,
                f"Snapshot {snapshot_id} SRS baseline generated from Stage 1 and Stage 2 artifacts", document_author,
            ))
            lines.append("")

            lines.append("#### Table 2. Reference documents {#table-2-reference-documents}")
            lines.append("| Doc name | Version | Author |")
            lines.append("|---|---|---|")
            lines.append(f"| artifacts/stage1_requirements/requirements_summary.csv | {GENERATED_SPEC_VERSION} | Requirements Extraction Agent |")
            lines.append(f"| artifacts/stage2_mirco_arc/micro_architecture_report.md | {GENERATED_SPEC_VERSION} | Micro-Architectural Analysis Agent |")
            lines.append(f"| artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv | {GENERATED_SPEC_VERSION} | Micro-Architectural Analysis Agent |")
            lines.append(f"| artifacts/stage2_mirco_arc/block_inventory.csv | {GENERATED_SPEC_VERSION} | Micro-Architectural Analysis Agent |")
            lines.append(f"| artifacts/stage2_mirco_arc/interface_catalog.csv | {GENERATED_SPEC_VERSION} | Micro-Architectural Analysis Agent |")
            lines.append(f"| artifacts/stage2_mirco_arc/interaction_matrix.csv | {GENERATED_SPEC_VERSION} | Micro-Architectural Analysis Agent |")
            lines.append(f"| templates/SRS_gen_AI_template_prompt.md | {GENERATED_SPEC_VERSION} | Project template maintainers |")
            lines.append("")

            lines.append("#### Table 6. Category convention {#table-6-category-convention}")
            lines.append("| Category | Naming rule / prefix | Scope | Notes / example |")
            lines.append("|---|---|---|---|")
            lines.append("| System authored requirement | SRS-REQ-xxx | Project-specific SRS atomic entries | Covers one upstream requirement per row |")
            lines.append("| Source system requirement | SYS-RQ-xxx or source_req_id | Upstream Stage 1 requirement catalog | Referenced through Covers linkage |")
            lines.append("| Source analog requirement | ANA-RQ-xxx or source_req_id | Upstream Stage 1 requirement catalog | Referenced through Covers linkage |")
            lines.append("| Source digital requirement | DIG-RQ-xxx or source_req_id | Upstream Stage 1 requirement catalog | Referenced through Covers linkage |")
            lines.append("| Cross-domain requirement | XDN-RQ-xxx or source_req_id | Upstream Stage 1 requirement catalog | Referenced through Covers linkage |")
            lines.append("")

        elif sec_num == "0.4":
            lines.append("| Table | Title | Link |")
            lines.append("|---|---|---|")
            lines.append(marker_tot)
            lines.append("")

        elif sec_num == "3.1":
            overview_audit: List[Dict[str, str]] = []
            overview_sections = compose_srs_system_overview(
                descriptive_records,
                mode_rows=mode_rows,
                interface_rows=[{
                    **row,
                    "source": f"artifacts/stage2_mirco_arc/interface_catalog.csv:row {index}",
                    "scope": "architecture",
                } for index, row in enumerate(interface_rows, start=2)],
                power_records=[
                    *_structured_srs_low_power_records(_resolve_repo_root(), function_rows),
                    *descriptive_records,
                ],
                block_names=list(render_block_functions),
                audit_rows=overview_audit,
            )
            audit_path = output_path.with_name("descriptive_system_overview_audit.csv")
            with audit_path.open("w", encoding="utf-8", newline="") as audit_handle:
                audit_writer = csv.DictWriter(audit_handle, fieldnames=[
                    "section", "statement", "source", "scope", "rendered_summary", "decision", "reason",
                    "profile", "fact_id", "fact_json", "contributor_ids",
                    "profile_version", "profile_fingerprint", "projection_adapter",
                    "source_record_id", "normalized_record_json", "unit_id", "semantic_unit_json",
                ])
                audit_writer.writeheader()
                audit_writer.writerows(overview_audit)
            for heading in SRS_SYSTEM_OVERVIEW_HEADINGS:
                if not heading.startswith("3.1 "):
                    lines.extend([f"### {heading}", ""])
                if heading.startswith("3.6 ") and support_sections["3.6"]:
                    for item in overview_sections[heading]:
                        if not item.startswith("- **Clock and reset**"):
                            for sentence in item.split("\n")[1:]:
                                lines.extend([sentence.removeprefix("  - "), ""])
                    lines.extend(["", "| Domain | Type | Control | Functional Role | Power Conditions |",
                                  "|---|---|---|---|---|", *support_sections["3.6"], ""])
                    lines.extend(item for item in overview_sections[heading] if item.startswith("- **Clock and reset**"))
                else:
                    lines.extend(overview_sections[heading])
                lines.append("")

        elif sec_num == "4.1":
            lines.extend(support_sections["4.1"] or ["No analog block catalog entries have a resolved classification in the selected architecture context."])
            lines.append("")

        elif sec_num == "5.1":
            lines.extend(support_sections["5.1"] or ["No digital block catalog entries have a resolved classification in the selected architecture context."])
            lines.append("")

        elif sec_num == "6.1":
            if interaction_summary:
                lines.append("Cross-domain orchestration shall be implemented through interaction paths:")
                lines.append("")
                for interaction_path in interaction_summary[:8]:
                    lines.append(f"- {interaction_path}")
            else:
                lines.append("Cross-domain interactions shall be derived from Stage 2 micro-architecture interaction matrix evidence.")
            if connection_matrix_requirements:
                lines.append("")
                lines.append("### Connection Matrix Requirements")
                lines.append("")
                lines.append("Each populated source-to-destination connection-matrix cell shall be implemented as follows:")
                lines.append("")
                for row in connection_matrix_requirements:
                    from_block = _resolve_matrix_block_name(row.get("From block", ""), {
                        (item.get("Block") or "").strip(): (item.get("Function") or "").strip()
                        for item in block_inventory_rows
                        if (item.get("Block") or "").strip()
                    }) or (row.get("From block", "") or "").strip()
                    to_block = _resolve_matrix_block_name(row.get("To block", ""), {
                        (item.get("Block") or "").strip(): (item.get("Function") or "").strip()
                        for item in block_inventory_rows
                        if (item.get("Block") or "").strip()
                    }) or (row.get("To block", "") or "").strip()
                    for source_req_id in (item.strip() for item in (row.get("Requirement IDs") or "").split(";")):
                        if source_req_id not in approved_srs_source_ids:
                            continue
                        matrix_id = connection_matrix_srs_ids.get(source_req_id, "SRS-REQ-000")
                        lines.append(f"[{matrix_id}] Requirement:")
                        lines.append(
                            f"The {from_block} block shall be connected to the {to_block} block."
                        )
                        lines.append(f"Covers: {source_req_id}")
                        lines.append("")
            lines.append("")

        elif sec_num == "6.3":
            timing_requirements = [
                req for req in requirements
                if re.search(r"\b(?:clock\s+domain|synchron(?:ize|ized|ization)|clock\s+gating|gated|irq|interrupt|latency|response\s+time|recovery)\b", req.statement, re.IGNORECASE)
            ]
            if timing_requirements:
                lines.append("#### Timing, clock-domain, and interrupt summary")
                lines.extend(_timing_evidence_bullets(timing_requirements, req_to_block, list(render_block_functions)))
            lines.append("")

        elif sec_num == "5.5":
            timing_requirements = [
                req for req in requirements
                if re.search(r"\b(?:clock\s+domain|synchron(?:ize|ized|ization)|clock\s+gating|gated|irq|interrupt|latency|response\s+time|recovery)\b", req.statement, re.IGNORECASE)
            ]
            if timing_requirements:
                lines.append("")
                lines.append("#### Timing and synchronization summary")
                lines.extend(_timing_evidence_bullets(timing_requirements, req_to_block, list(render_block_functions)))
            lines.append("")

        elif sec_num == "5.6":
            lines.append("Digital data-path requirements shall state the conditions for full, empty, overflow, underflow, throughput limits, and backpressure, including the involved blocks and required response.")
            data_path_requirements = [
                req for req in requirements
                if re.search(r"\b(?:fifo|buffer|queue|overflow|underflow|full|empty|depth|throughput|backpressure|data\s+path)\b", req.statement, re.IGNORECASE)
            ]
            if data_path_requirements:
                lines.append("")
                lines.append("Data-path conditions and involved blocks:")
                lines.extend(_data_path_evidence_bullets(data_path_requirements, req_to_block, list(render_block_functions)))
                lines.extend([
                    "- Overflow: when a write arrives while storage is full, the producing and buffering blocks shall define whether the write is blocked, flagged, or otherwise handled without silent data loss.",
                    "- Underflow: when a read is requested while storage is empty, the consuming and buffering blocks shall define the returned status/data and recovery behavior.",
                    "- Throughput and backpressure: when the offered data rate exceeds the available transfer capacity, the producer, buffer, and consumer shall define flow control and recovery behavior.",
                ])
            else:
                architecture_data_path = [
                    interaction_path
                    for interaction_path in interaction_summary
                    if re.search(r"\b(?:fifo|buffer|queue|overflow|underflow|full|empty|depth|throughput|backpressure)\b", interaction_path, re.IGNORECASE)
                ]
                if architecture_data_path:
                    lines.append("Data-path conditions and involved blocks:")
                    lines.extend(f"- {item}" for item in architecture_data_path[:8])
                    lines.extend([
                        "- Overflow: when a write arrives while storage is full, the producing and buffering blocks shall define whether the write is blocked, flagged, or otherwise handled without silent data loss.",
                        "- Underflow: when a read is requested while storage is empty, the consuming and buffering blocks shall define the returned status/data and recovery behavior.",
                        "- Throughput and backpressure: when the offered data rate exceeds the available transfer capacity, the producer, buffer, and consumer shall define flow control and recovery behavior.",
                    ])
                else:
                    lines.append("- No approved buffering, FIFO, overflow, or underflow evidence was identified.")
            lines.append("")

        elif sec_num == "6.4":
            power_grouped, _power_audit = assemble_low_power_descriptive(
                _structured_srs_low_power_records(_resolve_repo_root(), function_rows),
                repo_root=_resolve_repo_root(),
                profile="srs",
            )
            lines.append("Supply-domain functions and operating conditions are described in [section 3.6](#36-power-clock-and-reset-overview).")
            lines.append("")
            lines.extend(render_low_power_topics({topic: entries for topic, entries in power_grouped.items()
                                                 if topic != "Power-domain architecture"}))
            lines.append("")

        elif sec_num == "8.3":
            dedicated_groups: Dict[str, List[Requirement]] = defaultdict(list)
            non_block_source_ids = {
                row.get("Requirement ID", "").strip()
                for row in non_block_context_rows
                if row.get("Requirement ID", "").strip()
            }
            for req in requirements:
                label = _dedicated_source_label(req)
                if (
                    label
                    and req.source_req_id not in non_block_source_ids
                    and req_to_block.get(req.source_req_id, "Unassigned") == "Unassigned"
                ):
                    dedicated_groups[label].append(req)
            boot_requirements = [
                req for req in requirements
                if _is_boot_routine_operation_requirement(req)
                and req.source_req_id not in non_block_source_ids
            ]
            if boot_requirements:
                dedicated_groups["ADSP Peculiar Requirements - Boot routine/operation"] = boot_requirements
            if dedicated_groups:
                lines.append("#### Dedicated source sections")
                lines.append("")
                for dedicated_index, group_name in enumerate(sorted(dedicated_groups), start=1):
                    paragraph_number = f"8.3.{dedicated_index}"
                    lines.append(f"##### {paragraph_number} {group_name} {{#{_anchor_slug(group_name)}}}")
                    lines.append("")
                    for req in sorted(dedicated_groups[group_name], key=lambda item: srs_id_map.get(item.source_req_id, item.source_req_id)):
                        srs_id = srs_id_map[req.source_req_id]
                        lines.append(f"[{srs_id}] Requirement:")
                        lines.extend(_source_body_lines(req))
                        lines.append(f"Covers: {req.source_req_id}")
                        lines.append("")
            for domain in domain_order:
                items = [
                    req
                    for req in grouped.get(domain, [])
                    if req.source_req_id not in mapped_source_ids
                    and req.source_req_id not in non_block_source_ids
                    and not _dedicated_source_label(req)
                ]
                lines.append(f"#### {domain_title[domain]} requirements")
                if not items:
                    lines.append("- No residual unmapped requirements for this domain (mapped items are captured in project-specific sub-block requirement paragraphs).")
                    lines.append("")
                    continue
                for req in items:
                    srs_id = srs_id_map[req.source_req_id]
                    lines.append(f"[{srs_id}] Requirement:")
                    lines.append(_statement_payload(req.statement))
                    lines.append(f"Covers: {req.source_req_id}")
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
                        key=lambda item: srs_id_map.get(item.source_req_id, item.source_req_id),
                    ):
                        srs_id = srs_id_map[req.source_req_id]
                        lines.append(f"[{srs_id}] Requirement:")
                        lines.append(_statement_payload(req.statement))
                        lines.append(f"Covers: {req.source_req_id}")
                        lines.append("")

        elif sec_num == "9":
            lines.append("This section summarizes system-level functions and digital/analog interactions. Block-specific requirements, source I/O tables, ports, pins, clocks, and resets are owned by DRS or ARS and the corresponding IPOS specifications.")
            lines.append("")
            if False and block_inventory_rows:
                lines.append(
                    "Block-level digital summaries and source I/O lists are owned by the DRS at the digital architecture level. Detailed block requirements are maintained in the owning Digital or Analog IPOS specification."
                )
                lines.append("")
                for section_index, block, _req_start, _req_end in []:
                    lines.append(f"### 9.{section_index} {block}")
                    lines.append("")
                    lines.append(
                        f"General functional description: {render_block_functions.get(block, '')}"
                    )
                    lines.append("")
                    for requirement in block_requirements.get(block, []):
                        srs_id = srs_id_map[requirement.source_req_id]
                        lines.append(f"**[{srs_id}] Requirement:**")
                        lines.append("")
                        lines.extend(_atomic_block_statement(block, requirement).splitlines())
                        lines.append(f"Covers: {requirement.source_req_id}")
                        lines.append("")
                source_io_tables = _read_csv_rows(
                    _resolve_repo_root() / "artifacts/stage2_mirco_arc/source_io_table_coverage.csv"
                )
                source_io_ports = _read_csv_rows(
                    _resolve_repo_root() / "artifacts/stage2_mirco_arc/source_port_catalog.csv"
                )
                if False and source_io_tables:
                    lines.append("#### Source I/O context")
                    lines.append("")
                    for table in source_io_tables:
                        table_title = (table.get("Table title") or "").strip()
                        if not table_title:
                            continue
                        lines.append(f"##### {table_title}")
                        lines.append("")
                        lines.append("| Port name | Direction | Type / details | Owner |")
                        lines.append("|---|---|---|---|")
                        table_ports = [
                            port
                            for port in source_io_ports
                            if (port.get("Table title") or "").strip() == table_title
                        ]
                        if not table_ports:
                            lines.append("| N/A | N/A | N/A | N/A |")
                        else:
                            for port in table_ports:
                                values = [
                                    port.get("Port name", ""),
                                    port.get("Direction", ""),
                                    port.get("Type / details", "").replace("|", "\\|"),
                                    port.get("Owner", ""),
                                ]
                                lines.append("| " + " | ".join(values) + " |")
                        lines.append("")
                any_block = False
                for row in block_inventory_rows:
                    block = (row.get("Block") or "").strip()
                    if not block:
                        continue

                    any_block = True
                    lines.append(f"- {block}: see the corresponding DRS block paragraph and owning IPOS specification.")

                if not any_block:
                    lines.append("- No block-level mappings available in the current input set.")
                    lines.append("")

    non_block_context_rows = _cascade_non_block_context_rows(
        non_block_context_rows,
        requirements,
        req_to_block,
    )
    if non_block_context_rows:
        lines.append("## 8.4 Source Function Context {#84-source-function-context}")
        lines.append("")
        grouped_context: Dict[str, List[Dict[str, str]]] = defaultdict(list)
        emitted_context_elsewhere = {
            req.source_req_id
            for req in user_specific_requirements
        }
        emitted_context_elsewhere.update(
            req.source_req_id
            for req in requirements
            if _dedicated_source_label(req)
            and req.source_req_id not in {
                row.get("Requirement ID", "").strip()
                for row in non_block_context_rows
                if row.get("Requirement ID", "").strip()
            }
        )
        context_sources = [
            item.get("Non-Block Function Context") or ""
            for item in non_block_context_rows
        ]
        for row in non_block_context_rows:
            source_req_id = row.get("Requirement ID", "").strip()
            if source_req_id not in non_block_source_ids:
                continue
            requirement = next(
                (item for item in requirements if item.source_req_id == source_req_id),
                None,
            )
            reviewed_context = row.get("Non-Block Function Context") or row.get("Source Paragraph") or ""
            authoritative_source = reviewed_context or (requirement.source if requirement is not None else "")
            grouped_context[
                _non_block_context_label(
                    authoritative_source or row.get("Non-Block Function Context") or "",
                    context_sources,
                )
            ].append(row)
        for context_index, (context, rows) in enumerate(sorted(grouped_context.items()), start=1):
            paragraph_number = f"8.4.{context_index}"
            lines.append(f"### {paragraph_number} {context} {{#{_anchor_slug(paragraph_number + ' ' + context)}}}")
            lines.append("")
            for row in rows:
                source_req_id = row.get("Requirement ID", "").strip()
                if source_req_id not in non_block_source_ids:
                    continue
                requirement = next(
                    (item for item in requirements if item.source_req_id == source_req_id),
                    None,
                )
                if source_req_id in emitted_context_elsewhere:
                    continue
                if requirement is not None:
                    lines.append(f"[{srs_id_map[source_req_id]}] Requirement:")
                    lines.extend(_source_body_lines(requirement))
                    lines.append(f"Covers: {source_req_id}")
                else:
                    lines.append(row.get("Requirement Statement") or "No preserved requirement statement.")
                source_paragraph = requirement.source if requirement is not None else (
                    row.get("Source Paragraph") or "Unknown"
                )
                lines.append(f"Source paragraph: {source_paragraph}")
                lines.append("")

    lines.append("## Assumptions and TBD {#assumptions-and-tbd}")
    lines.append("- ASSUME-001: Verification environments include controllable stimulus for all listed operating modes.")
    lines.append("- TBD-001: Unassigned requirements in traceability matrix need architectural owner review.")
    if crosscheck_decision == "no-go":
        lines.append("- TBD-002: Stage 2 micro-architecture crosscheck currently reports no-go; unresolved coverage items require closure.")
    lines.append("")

    lines.append("## 10. Missing Inputs {#10-missing-inputs}")
    if missing_inputs:
        for p in missing_inputs:
            try:
                rel = p.relative_to(_resolve_repo_root()).as_posix()
            except ValueError:
                rel = str(p)
            lines.append(f"- {rel}")
    else:
        lines.append("- None")
    lines.append("")

    if support_audit["review_findings"]:
        lines.extend(["### 10.1 Descriptive content review findings", ""])
        lines.extend("- " + finding for finding in support_audit["review_findings"])
        lines.append("")

    lines = _deduplicate_authored_requirement_blocks(lines)
    heading_registry = _build_heading_registry(lines)
    lines = _apply_heading_registry_anchors(lines, heading_registry)
    lines, _resolved_navigation_links, _intentional_non_links = _rewrite_internal_links(lines, heading_registry)
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
    toc_entries = [
        (title, section_number, anchor)
        for level, title, anchor, section_number in navigation_registry
        if (level == 2 and not section_number)
        or title == "0. Document Navigation"
        or (section_number and not section_number.startswith("0."))
    ]
    nav_entries = [
        (title, section_number, anchor)
        for _level, title, anchor, section_number in navigation_registry
        if section_number and not section_number.startswith("0.")
    ]
    table_entries = [
        (title, anchor)
        for _level, title, anchor, _num in heading_registry
        if re.match(r"^Table\s+\d+\.\s+", title)
    ]

    lines_rendered: List[str] = []
    for line in lines:
        if line == marker_toc:
            for item_title, section_number, anchor in toc_entries:
                indent = "  " * max(0, len(section_number.split(".")) - 1)
                lines_rendered.append(f"{indent}- [{item_title}](#{anchor})")
            continue

        if line == marker_nav:
            for nav_title, paragraph, anchor in nav_entries:
                lines_rendered.append(f"| {nav_title} | {paragraph} | [Jump](#{anchor}) | Auto |")
            non_block_source_ids = {
                row.get("Requirement ID", "").strip()
                for row in non_block_context_rows
                if row.get("Requirement ID", "").strip()
            }
            for group_name in sorted(
                {
                    _dedicated_source_label(req)
                    for req in requirements
                    if _dedicated_source_label(req)
                    and req.source_req_id not in non_block_source_ids
                    and req_to_block.get(req.source_req_id, "Unassigned") == "Unassigned"
                }
            ):
                anchor = _anchor_slug(group_name)
                lines_rendered.append(f"| {group_name} | dedicated | [Jump](#{anchor}) | Auto |")
            continue

        if line == marker_tot:
            for idx, (table_title, anchor) in enumerate(table_entries, start=1):
                short_title = re.sub(r"^Table\s+\d+\.\s*", "", table_title).strip()
                lines_rendered.append(f"| Table {idx} | {short_title} | [Go to Table {idx}](#{anchor}) |")
            continue

        lines_rendered.append(line)

    lines_rendered, _resolved_navigation_links, _intentional_non_links = _rewrite_internal_links(
        lines_rendered,
        heading_registry,
    )
    lines_rendered = [line for item in lines_rendered for line in _to_text(item).replace("•", "-").split("\n")]
    lines_rendered = _ensure_blank_line_between_paragraphs(lines_rendered)
    lines_rendered = _ensure_requirement_block_spacing(lines_rendered)
    lines_rendered = _ensure_subparagraph_heading_spacing(lines_rendered)
    lines_rendered = _ensure_table_block_spacing(lines_rendered)
    lines_rendered = _insert_visible_paragraph_spacers(lines_rendered)
    normalized_lines: List[str] = []
    for line in lines_rendered:
        stripped = line.strip()
        is_list_item = bool(re.match(r"^(?:[-*+]\s+|\d+(?:\.\d+)+[.:]?\s+|\d+[.)]\s+)", stripped))
        previous = normalized_lines[-1].strip() if normalized_lines else ""
        previous_is_list_item = bool(re.match(r"^(?:[-*+]\s+|\d+(?:\.\d+)+[.:]?\s+|\d+[.)]\s+)", previous))
        if is_list_item and previous and not previous_is_list_item:
            normalized_lines.append("")
        normalized_lines.append(line)
    lines_rendered = _terminate_authored_requirement_blocks(normalized_lines)
    lines_rendered = _deduplicate_authored_requirement_blocks(lines_rendered)
    final_registry = _build_heading_registry(lines_rendered)
    lines_rendered, _resolved_navigation_links, _intentional_non_links = _rewrite_internal_links(
        lines_rendered,
        final_registry,
    )
    rendered_text = "\n".join(lines_rendered) + "\n"
    rendered_text = re.sub(r"(?m)^([^\n]+:)\n(\d+(?:\.\d+)+[.:]?\s+)", r"\1\n\n\2", rendered_text)
    output_path.write_text(rendered_text, encoding="utf-8")


def _write_stage_report(
    output_path: Path,
    present_inputs: List[Path],
    missing_inputs: List[Path],
    requirements: List[Requirement],
    unmapped_requirements: List[Requirement],
    full_traceability_count: int,
    unassigned_count: int,
    crosscheck_decision: str,
    *,
    valid_empty: bool = False,
) -> str:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    counts = defaultdict(int)
    for req in requirements:
        counts[req.domain] += 1

    status = "pass" if valid_empty or requirements or full_traceability_count > 0 else "fail"
    blocking_issues: List[str] = []

    if not valid_empty and not requirements and full_traceability_count == 0:
        blocking_issues.append("No requirements were loaded from requirements_summary.csv")
    if missing_inputs:
        blocking_issues.append(f"Missing required input artifacts: {len(missing_inputs)}")
    if crosscheck_decision == "no-go":
        blocking_issues.append("Stage 2 micro-architecture crosscheck decision is no-go")
    if blocking_issues:
        status = "fail"

    lines: List[str] = [
        "# Stage SRS Report",
        "",
        f"Date: {today}",
        "",
        f"SRS generation status: {status}",
        "",
        "## Input artifact coverage summary",
        f"- Present inputs: {len(present_inputs)}",
        f"- Missing inputs: {len(missing_inputs)}",
        "",
        "## Count of generated SRS requirements by domain",
        f"- SYS: {counts['SYS']}",
        f"- ANA: {counts['ANA']}",
        f"- DIG: {counts['DIG']}",
        f"- XDN: {counts['XDN']}",
        "",
        "## Count of requirements with full traceability",
        f"- Fully mapped to owning block: {full_traceability_count}",
        f"- Unassigned owning block: {unassigned_count}",
        f"- Unmapped to known block inventory: {len(unmapped_requirements)}",
        "",
        "## Open TBD/assumptions list",
        *(
            [
                "- ASSUME-001: Verification environments include controllable stimulus for all listed operating modes.",
                "- TBD-001: Unassigned requirements in traceability matrix need architectural owner review.",
            ]
            if not valid_empty
            else ["- None"]
        ),
        f"- Stage 2 micro-architecture crosscheck decision: {crosscheck_decision}",
        "",
        "## Blocking issues list",
    ]

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
        raise RuntimeError(f"SRS md->docx conversion failed with exit code {rc}")
    apply_docx_authored_requirement_formatting(output_docx_path, ("SRS",))
    apply_docx_common_spec_formatting(output_docx_path)
    _validate_docx_end_markers(markdown_path, output_docx_path)


def _validate_docx_end_markers(markdown_path: Path, docx_path: Path) -> None:
    expected = len(re.findall(r"^[ \t]*\[End\][ \t]*$", markdown_path.read_text(encoding="utf-8"), flags=re.M | re.I))
    with zipfile.ZipFile(docx_path) as archive:
        document_xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
    if document_xml.lower().count("[end]") < expected:
        raise RuntimeError("SRS DOCX does not preserve all visible [End] requirement terminators")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run SRS generation agent workflow")
    parser.add_argument(
        "--agent-file",
        default=".github/agents/srs_gen_spec.agent.md",
        help="Path to agent definition markdown",
    )
    parser.add_argument(
        "--template-file",
        default="templates/SRS_gen_AI_template_prompt.md",
        help="Path to SRS generation template markdown",
    )
    parser.add_argument(
        "--requirements-summary",
        help="Deprecated compatibility option; resolver snapshot is authoritative",
    )
    parser.add_argument(
        "--req-block-trace",
        default="artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv",
        help="Requirement to block traceability CSV",
    )
    parser.add_argument(
        "--block-inventory",
        default="artifacts/stage2_mirco_arc/block_inventory.csv",
        help="Block inventory CSV",
    )
    parser.add_argument(
        "--interface-catalog",
        default="artifacts/stage2_mirco_arc/interface_catalog.csv",
        help="Interface catalog CSV",
    )
    parser.add_argument(
        "--interaction-matrix",
        default="artifacts/stage2_mirco_arc/interaction_matrix.csv",
        help="Interaction matrix CSV",
    )
    parser.add_argument(
        "--function-decomposition",
        default="artifacts/stage2_mirco_arc/function_decomposition.md",
        help="Function decomposition markdown",
    )
    parser.add_argument(
        "--architecture-crosscheck",
        default="artifacts/stage2_mirco_arc/architecture_crosscheck_report.md",
        help="Architecture crosscheck report markdown",
    )
    parser.add_argument(
        "--out-srs-md",
        default="artifacts/stage3_srs/system_requirements_specification.md",
        help="Output SRS markdown path",
    )
    parser.add_argument(
        "--out-traceability-csv",
        default="artifacts/stage3_srs/srs_traceability_matrix.csv",
        help="Output SRS traceability CSV path",
    )
    parser.add_argument(
        "--out-stage-report",
        default="artifacts/orchestrator/stage_srs_report.md",
        help="Output Stage SRS report path",
    )
    parser.add_argument(
        "--out-srs-docx",
        default="artifacts/stage3_srs/system_requirements_specification.docx",
        help="Output SRS DOCX path",
    )
    parser.add_argument(
        "--docx-reference-template",
        default=DOCX_REFERENCE_TEMPLATE,
        help="DOCX reference template path for pandoc conversion",
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
        print("SRS agent run: FAIL (Stage 2+ source-spec independence guard failed)")
        _append_log(repo_root, script_name, f"FAIL stage2_plus_guard_exit={guard_rc}")
        return guard_rc

    agent_file = (repo_root / args.agent_file).resolve()
    template_file = (repo_root / args.template_file).resolve()
    context = json.loads((repo_root / "config" / "project_context.json").read_text(encoding="utf-8"))
    requirement_input, selection = resolve_complete_authoritative_input(
        repo_root,
        "3",
        project_id=str(context.get("project_name") or repo_root.name),
        snapshot_id=args.snapshot_id,
    )
    downstream_contract = resolve_downstream_contract(repo_root, requirement_input.snapshot_id)
    coherence = validate_downstream_coherence(repo_root, requirement_input.snapshot_id)
    if not args.regenerate_downstream and coherence["decision"] != "PASS":
        raise RuntimeError(f"Downstream snapshot coherence blocked SRS generation: {coherence['finding_count']} findings")
    _append_log(repo_root, script_name, f"AUTHORITATIVE_SNAPSHOT snapshot_id={selection['selected_snapshot_id']} mode={selection['selection_mode']} user={runtime_user_name()}")
    refresh_ledger(repo_root, snapshot_id=requirement_input.snapshot_id, source_rows=requirement_input.rows)
    summary_csv = requirement_input.source_path
    req_block_trace_csv = (repo_root / args.req_block_trace).resolve()
    block_inventory_csv = (repo_root / args.block_inventory).resolve()
    interface_catalog_csv = (repo_root / args.interface_catalog).resolve()
    interaction_matrix_csv = (repo_root / args.interaction_matrix).resolve()
    function_decomposition_md = (repo_root / args.function_decomposition).resolve()
    architecture_crosscheck_md = (repo_root / args.architecture_crosscheck).resolve()

    out_srs_md = (repo_root / args.out_srs_md).resolve()
    out_srs_docx = (repo_root / args.out_srs_docx).resolve()
    out_traceability_csv = (repo_root / args.out_traceability_csv).resolve()
    out_stage_report = (repo_root / args.out_stage_report).resolve()
    document_version = document_version_for_snapshot(out_srs_md, requirement_input.snapshot_id)
    docx_reference_template = (
        (repo_root / args.docx_reference_template).resolve()
        if args.docx_reference_template
        else None
    )

    if docx_reference_template and docx_reference_template.exists():
        print(f"SRS agent run: INFO (format reference template: {docx_reference_template})")
        _append_log(repo_root, script_name, f"INFO docx_reference_template={docx_reference_template}")
    elif docx_reference_template:
        print(f"SRS agent run: WARN (reference template not found: {docx_reference_template})")
        _append_log(repo_root, script_name, f"WARN missing_docx_reference_template={docx_reference_template}")

    present_inputs, missing_inputs = _check_inputs(repo_root)

    if not agent_file.exists():
        print(f"SRS agent run: FAIL (missing agent file: {agent_file})")
        _append_log(repo_root, script_name, f"FAIL missing_agent={agent_file}")
        return 1

    if not summary_csv.exists():
        print(f"SRS agent run: FAIL (missing requirements summary: {summary_csv})")
        _append_log(repo_root, script_name, f"FAIL missing_summary={summary_csv}")
        return 1

    if not template_file.exists():
        print(f"SRS agent run: FAIL (missing prompt template: {template_file})")
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
        requirements = _read_requirements(summary_csv, requirement_input.rows)
        all_requirement_ids = {requirement.source_req_id for requirement in requirements}
        allocations = {
            source_id: downstream_contract.allocation(source_id)
            for source_id in all_requirement_ids
        }
        non_block_context_rows = _read_non_block_context_rows(
            repo_root / "artifacts/stage2_mirco_arc/unmapped_requirement_routing.csv",
            all_requirement_ids,
        )
        retained_context_ids = {
            row.get("Requirement ID", "").strip()
            for row in non_block_context_rows
            if row.get("Requirement ID", "").strip()
        }
        requirements = [
            requirement
            for requirement in requirements
            if _is_srs_allocated(requirement, allocations)
        ]
        req_to_block = _read_req_to_block(req_block_trace_csv)
        block_inventory_rows = _read_csv_rows(block_inventory_csv)
        _require_block_functions(block_inventory_rows)
        catalog_entries, catalog_findings = srs_catalog_from_context(
            block_inventory_rows, downstream_contract, snapshot_architecture_context(repo_root, downstream_contract),
        )
        inventory_block_names = [
            (row.get("Block") or "").strip()
            for row in block_inventory_rows
            if (row.get("Block") or "").strip()
        ]
        approved_names = approved_block_names(repo_root / "artifacts/stage1_specs/approved_block_list.xlsx")
        approved_tokens = {_canonical_token(name) for name in approved_names}
        block_names = [
            name
            for name in inventory_block_names
            if not approved_tokens or _canonical_token(name) in approved_tokens
        ]
        mode_rows = _filter_mode_rows_to_srs_allocations(
            _complete_mode_rows(_mode_source_rows(repo_root, block_names), block_names),
            allocations,
        )
        allocation_by_source = {
            requirement.source_req_id: allocations[requirement.source_req_id]
            for requirement in requirements
            if requirement.source_req_id in allocations
        }
        interface_rows = _read_csv_rows(interface_catalog_csv)
        source_port_rows = _read_csv_rows(repo_root / "artifacts/stage2_mirco_arc/source_port_catalog.csv")
        interaction_rows = _read_csv_rows(interaction_matrix_csv)
        function_rows = _read_function_decomposition(function_decomposition_md)
        matrix_requirement_ids: Set[str] = set()
        non_block_context_rows = _read_non_block_context_rows(
            repo_root / "artifacts/stage2_mirco_arc/unmapped_requirement_routing.csv",
            {requirement.source_req_id for requirement in requirements},
        )
        source_parent_requirements = [
            requirement
            for requirement in requirements
            if requirement.source_req_id not in matrix_requirement_ids
            and _has_explicit_source_parent(requirement.source)
            and _is_user_facing_requirement(requirement.statement)
            and not _is_reset_clock_table_requirement(requirement)
            and not _dedicated_source_label(requirement)
            and req_to_block.get(requirement.source_req_id, "Unassigned") == "Unassigned"
        ]
        retained_context_ids = {
            row.get("Requirement ID", "").strip()
            for row in non_block_context_rows
            if row.get("Requirement ID", "").strip()
        }
        for requirement in source_parent_requirements:
            if requirement.source_req_id in retained_context_ids:
                continue
            non_block_context_rows.append(
                {
                    "Requirement ID": requirement.source_req_id,
                    "Non-Block Function Context": requirement.source,
                    "Source Paragraph": requirement.source,
                    "Requirement Statement": requirement.statement,
                    "Routing Status": "retained_as_non_block_function_context",
                }
            )
        crosscheck_decision = _extract_crosscheck_decision(architecture_crosscheck_md)
        srs_id_map = _build_srs_ids(requirements)
        connection_matrix_srs_ids = _connection_matrix_srs_ids(interaction_rows, srs_id_map)
        used_srs_ids = set(srs_id_map.values()) | set(connection_matrix_srs_ids.values())
        next_mode_number = max(
            (int(value.rsplit("-", 1)[1]) for value in used_srs_ids if value.startswith("SRS-REQ-")),
            default=0,
        )
        for mode_row in mode_rows:
            source_req_id = mode_row["source_req_id"]
            if source_req_id in srs_id_map or source_req_id in connection_matrix_srs_ids:
                continue
            next_mode_number += 1
            srs_id_map[source_req_id] = f"SRS-REQ-{next_mode_number:03d}"
        matrix_requirement_ids = set(connection_matrix_srs_ids)
        source_parent_requirements = [
            requirement
            for requirement in requirements
            if requirement.source_req_id not in matrix_requirement_ids
            and _has_explicit_source_parent(requirement.source)
            and _is_user_facing_requirement(requirement.statement)
            and not _is_reset_clock_table_requirement(requirement)
            and not _dedicated_source_label(requirement)
            and req_to_block.get(requirement.source_req_id, "Unassigned") == "Unassigned"
        ]
        block_functions = {
            (row.get("Block") or "").strip(): (row.get("Function") or "").strip()
            for row in block_inventory_rows
            if (row.get("Block") or "").strip()
        }
        matrix_owner_by_req = _matrix_owner_by_requirement(interaction_rows, block_functions)
        reset_clock_owner = _reset_clock_owner(block_functions)
        interrupt_owner = _interrupt_owner(block_functions)
        retained_source_ids = {
            row.get("Requirement ID", "").strip()
            for row in non_block_context_rows
            if row.get("Requirement ID", "").strip()
        }
        non_block_source_ids = set(retained_source_ids)

        user_specific_requirements = [
            req
            for req in requirements
            if req.source_req_id not in matrix_requirement_ids
            and req.source_req_id not in non_block_source_ids
            and not _dedicated_source_label(req)
            and _is_user_facing_requirement(req.statement)
            and req_to_block.get(req.source_req_id, "") == "Unassigned"
        ]

        block_requirements, unmapped_requirements = _map_requirements_to_blocks(
            requirements,
            req_to_block,
            block_functions,
            matrix_requirement_ids,
        )
        for block_name, mapped_requirements in list(block_requirements.items()):
            retained_requirements = [
                requirement
                for requirement in mapped_requirements
                if requirement.source_req_id not in non_block_source_ids
            ]
            unmapped_requirements.extend(
                requirement
                for requirement in mapped_requirements
                if requirement.source_req_id in non_block_source_ids
            )
            block_requirements[block_name] = retained_requirements
        full_traceability_count, unassigned_count = _write_traceability_csv(
            out_traceability_csv, requirements, srs_id_map, req_to_block,
            allocation_by_source, requirement_input.snapshot_id
        )
        full_traceability_count += _append_matrix_only_traceability_rows(
            out_traceability_csv,
            interaction_rows,
            connection_matrix_srs_ids,
            {requirement.source_req_id for requirement in requirements},
            allocation_by_source,
            requirement_input.snapshot_id,
        )
        full_traceability_count += _append_mode_traceability_rows(
            out_traceability_csv,
            mode_rows,
            srs_id_map,
            {requirement.source_req_id for requirement in requirements},
            allocation_by_source,
            requirement_input.snapshot_id,
        )
        architecture_records = architecture_records_from_function_rows(function_rows)
        stage1_descriptive_records = extract_stage1_descriptive_evidence(
            repo_root / "artifacts/stage1_requirements/ocr_extracts/index.csv",
            block_names=block_names,
        )
        descriptive_records = filter_configured_descriptive_exclusions(
            [*stage1_descriptive_records, *architecture_records],
            repo_root=repo_root,
        )
        write_descriptive_audit(
            out_srs_md.with_name("descriptive_summary_audit.csv"),
            assemble_descriptive_summary(
                descriptive_records,
                DESCRIPTIVE_SYSTEM_TOPIC_SPECS,
                max_items_per_topic=max(len(descriptive_records), 1),
            ),
            section="System Main Functions",
        )
        write_descriptive_audit(
            out_srs_md.with_name("descriptive_operating_modes_audit.csv"),
            assemble_descriptive_summary(
                descriptive_records,
                DESCRIPTIVE_MODE_TOPIC_SPECS,
                include_general=False,
                max_items_per_topic=max(len(descriptive_records), 1),
            ),
            section="Operating Modes",
        )
        write_descriptive_audit(
            out_srs_md.with_name("descriptive_power_states_audit.csv"),
            assemble_descriptive_summary(
                descriptive_records,
                DESCRIPTIVE_POWER_TOPIC_SPECS,
                include_general=False,
                max_items_per_topic=max(len(descriptive_records), 1),
            ),
            section="Power States",
        )
        low_power_grouped, low_power_audit = assemble_low_power_descriptive(
            architecture_records,
            repo_root=repo_root,
            profile="srs",
        )
        write_low_power_audit(out_srs_md.with_name("descriptive_low_power_audit.csv"), low_power_audit)
        _write_srs_markdown(
            out_srs_md,
            template_file,
            source_spec,
            str(project_context.get("project_name") or "Project"),
            document_author_name(),
            requirements,
            srs_id_map,
            req_to_block,
            block_inventory_rows,
            interface_rows,
            source_port_rows,
            interaction_rows,
            connection_matrix_srs_ids,
            function_rows,
            descriptive_records,
            block_requirements,
            unmapped_requirements,
            user_specific_requirements,
            non_block_context_rows,
            crosscheck_decision,
            missing_inputs,
            mode_rows,
            {
                source_id
                for source_id, allocation in allocations.items()
                if allocation.get("owning_target", "").strip() == "SRS"
            },
            requirement_input.snapshot_id,
            downstream_contract_fingerprint(downstream_contract),
            document_version,
            catalog_entries=catalog_entries,
            catalog_findings=catalog_findings,
        )
        docx_generated = False
        if shutil.which("pandoc") is None:
            raise RuntimeError("pandoc is required for SRS DOCX generation but is not available on PATH")
        if docx_reference_template is not None and not docx_reference_template.exists():
            raise FileNotFoundError(f"Missing DOCX reference template: {docx_reference_template}")
        _convert_markdown_to_docx(out_srs_md, out_srs_docx, docx_reference_template, repo_root)
        docx_generated = True
        status = _write_stage_report(
            out_stage_report,
            present_inputs,
            missing_inputs,
            requirements,
            unmapped_requirements,
            full_traceability_count,
            unassigned_count,
            crosscheck_decision,
            valid_empty=not downstream_contract.source_ids_for_target("SRS"),
        )

        latex_cmd = [sys.executable, SRS_LATEX_AGENT_SCRIPT]
        latex_rc = subprocess.run(latex_cmd, cwd=repo_root).returncode
        if latex_rc != 0:
            raise RuntimeError(f"SRS md->latex conversion failed with exit code {latex_rc}")

        srs_crosscheck_cmd = [
            sys.executable,
            "scripts/run_srs_crosscheck_agent.py",
            "--snapshot-id",
            requirement_input.snapshot_id,
        ]
        srs_crosscheck_rc = subprocess.run(srs_crosscheck_cmd, cwd=repo_root).returncode
        if srs_crosscheck_rc != 0:
            raise RuntimeError(f"SRS crosscheck failed with exit code {srs_crosscheck_rc}")

        srs_latex_crosscheck_cmd = [sys.executable, "scripts/run_srs_latex_crosscheck_agent.py"]
        srs_latex_crosscheck_rc = subprocess.run(srs_latex_crosscheck_cmd, cwd=repo_root).returncode
        if srs_latex_crosscheck_rc != 0:
            raise RuntimeError(f"SRS LaTeX crosscheck failed with exit code {srs_latex_crosscheck_rc}")
    except Exception as exc:
        print(f"SRS agent run: FAIL ({exc})")
        print(traceback.format_exc())
        _append_log(repo_root, script_name, f"FAIL error={exc}")
        return 1

    print("SRS agent run: PASS")
    print(f"- Agent definition: {agent_file}")
    print(f"- Prompt template: {template_file}")
    print(f"- SRS markdown: {out_srs_md}")
    if docx_generated:
        print(f"- SRS DOCX: {out_srs_docx}")
    else:
        print("- SRS DOCX: not generated")
    print(f"- Traceability CSV: {out_traceability_csv}")
    print(f"- Combined LaTeX: {(repo_root / 'artifacts/stage3_srs/stage2_srs_combined.tex').resolve()}")
    print(f"- Stage report: {out_stage_report}")
    print(f"- Input coverage: present={len(present_inputs)} missing={len(missing_inputs)}")
    print(f"- Requirements generated: {len(requirements)}")
    print(f"- Traceability mapped: {full_traceability_count} (unassigned={unassigned_count})")
    print(f"- Stage 2 micro-architecture crosscheck decision: {crosscheck_decision}")
    print(f"- Stage status: {status}")

    _append_log(
        repo_root,
        script_name,
        (
            "PASS "
            f"requirements={len(requirements)} full_traceability={full_traceability_count} "
            f"unassigned={unassigned_count} missing_inputs={len(missing_inputs)} status={status}"
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

