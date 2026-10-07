#!/usr/bin/env python3
"""Run the ARS generation agent workflow from repository artifacts.

This script operationalizes `.github/agents/ars_gen_spec.agent.md` by:
- validating required inputs
- generating ARS markdown
- generating ARS traceability CSV
- generating Stage ARS report
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import tempfile
import traceback
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import subprocess
import sys

from workflow_routing import (
    apply_docx_authored_requirement_formatting,
    apply_docx_common_spec_formatting,
    GENERATED_SPEC_VERSION,
    csv_cell_text,
    normalize_authored_requirement_blocks,
    organize_descriptive_topics,
    DESCRIPTIVE_ANALOG_TOPIC_SPECS,
    assemble_descriptive_summary,
    write_descriptive_audit,
    read_retained_rows,
    source_parent_title,
    runtime_user_name,
    document_author_name,
    document_version_for_snapshot,
    document_version_history_markdown,
)
from approved_snapshot_resolver import resolve_complete_authoritative_input
from traceability_rules import is_direct_upstream_source_id
from allocation_ledger import refresh_ledger
from validate_downstream_coherence import (
    canonical_human_label,
    resolve_downstream_contract,
    validate as validate_downstream_coherence,
)
from low_power_descriptive import assemble_low_power_descriptive, render_low_power_topics, write_low_power_audit


REQUIRED_INPUTS = [
    "artifacts/stage1_requirements/requirements_summary.csv",
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


ANALOG_FOCUS_TERMS = (
    "analog",
    "temperature",
    "sensor",
    "adc",
    "hysteresis",
    "setpoint",
    "relay",
    "ambient",
    "remote",
    "sampling",
    "conversion",
    "voltage",
    "power",
    "brown-out",
    "calibration",
    "noise",
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
    "a", "and", "are", "as", "at", "by", "for", "from", "in", "into",
    "of", "on", "or", "the", "to", "with",
}

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


@dataclass
class BlockInfo:
    name: str
    function: str
    inputs: str
    outputs: str
    linked_requirements: str


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
        return "The analog subsystem shall satisfy this requirement based on available source artifacts."

    low = text.lower()
    if " shall " in low or low.startswith("shall "):
        return text

    if text.endswith("."):
        text = text[:-1]
    return f"The analog subsystem shall satisfy the following behavior: {text}."


def _verification_method(req_type: str, domain: str) -> str:
    t = (req_type or "").strip().lower()
    if t in {"timing", "electrical", "performance"}:
        return "analysis+test"
    if t in {"interface", "protocol"}:
        return "inspection+test"
    if t in {"configuration", "mode-behavior"}:
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
        return True
    return not has_normative_marker


def _read_requirements(summary_csv: Path, input_rows: Optional[tuple[Dict[str, str], ...]] = None) -> List[Requirement]:
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
    requirements: List[Requirement] = []
    for row in rows:
        req_id = (row.get("source_req_id") or row.get("id") or "").strip()
        if req_id.upper() in excluded_ids:
            continue
        statement = _enforce_normative(row.get("requirement_statement", ""))
        if _is_non_normative_table_row(row, statement):
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


def _require_srs_upstream_map(requirements: List[Requirement], srs_upstream_map: Dict[str, str]) -> None:
    missing = sorted({
        req.source_req_id
        for req in requirements
        if not _direct_upstream_id(req.source_req_id)
        and req.source_req_id not in srs_upstream_map
    })
    if missing:
        preview = ", ".join(missing[:20])
        raise ValueError(
            "Missing SRS upstream mapping for ARS Covers (source_req_id -> SRS-REQ-xxx): " + preview
        )


def _direct_upstream_id(source_req_id: str) -> bool:
    """Allow supplementary-source requirements to remain upstream of ARS."""
    return is_direct_upstream_source_id(source_req_id)


def _upstream_id(source_req_id: str, srs_upstream_map: Dict[str, str]) -> str:
    if _direct_upstream_id(source_req_id):
        return source_req_id
    return srs_upstream_map[source_req_id]


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


def _connection_matrix_upstream_ids(
    interaction_rows: List[Dict[str, str]],
) -> Dict[str, str]:
    """Map populated connection-matrix source IDs to authored SRS matrix IDs."""
    out: Dict[str, str] = {}
    matrix_counter = 1
    for row in interaction_rows:
        requirement_ids = (row.get("Requirement IDs") or "").strip()
        if not requirement_ids or not row.get("From block") or not row.get("To block"):
            continue
        upstream_id = f"SRS-REQ-{matrix_counter:03d}"
        for requirement_id in [item.strip() for item in requirement_ids.split(";") if item.strip()]:
            out[requirement_id] = upstream_id
        matrix_counter += 1
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
    if re.match(r"^\[ARS-REQ-\d{3}\]\s+Requirement:\s*$", text):
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
    for idx, line in enumerate(lines):
        out.append(line)
        if idx >= len(lines) - 1:
            continue
        next_line = lines[idx + 1]
        current_text = _to_text(line).strip()
        next_text = _to_text(next_line).strip()
        current_is_list_item = bool(re.match(r"^(?:[-*+]\s+|\d+[.)]\s+|•\s+)", current_text))
        next_is_list_item = bool(re.match(r"^(?:[-*+]\s+|\d+[.)]\s+|•\s+)", next_text))
        if (next_is_list_item and not current_is_list_item and current_text) or (
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
    while idx < n:
        line = lines[idx]
        if _to_text(line).strip() != "":
            out.append(line)
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
        next_is_requirement = bool(re.match(r"^\[ARS-REQ-\d{3}\]\s+Requirement:\s*$", _to_text(next_line).strip()))
        needs_spacer = (
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
        if re.match(r"^\[ARS-REQ-\d{3}\]\s+Requirement:\s*$", _to_text(line).strip()):
            if out and _to_text(out[-1]).strip():
                out.append("")
        if re.match(r"^\s*Covers:\s*\S+\s*$", _to_text(line).strip()):
            if out and _to_text(out[-1]).strip():
                out.append("")
        if re.match(r"^\[ARS-REQ-\d{3}\]\s+Requirement:\s*$", _to_text(line).strip()):
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
    return normalize_authored_requirement_blocks(lines, ("ARS",))


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


def _inventory_analog_blocks(blocks: List[BlockInfo], interface_rows: List[Dict[str, str]]) -> Set[str]:
    owner_types = _interface_types_by_owner(interface_rows)
    out: Set[str] = set()
    for block in blocks:
        category = _classify_block_category(block, owner_types)
        if category in {BLOCK_CLASS_ANALOG, BLOCK_CLASS_POWER}:
            out.add(block.name)
    return out


def _analog_focus_score(text: str) -> int:
    t = _statement_payload(text)
    return sum(1 for token in ANALOG_FOCUS_TERMS if token in t)


def _digital_system_score(text: str) -> int:
    t = _statement_payload(text)
    return sum(1 for token in DIGITAL_SYSTEM_TERMS if token in t)


def _statement_payload(text: str) -> str:
    t = (text or "").strip()
    low = t.lower()
    prefix = "the analog subsystem shall satisfy the following behavior:"
    if low.startswith(prefix):
        t = t[len(prefix):].strip()
    t = re.sub(r"\[[A-Za-z][A-Za-z0-9_]*\s*\d+\]\s*(?:Requirement\s*:\s*)?", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\b[A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]*\s*\d+\b", "", t).strip()
    return _normalize_block_references(re.sub(r"\s+", " ", t))


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


DEDICATED_SOURCE_TERMS = (
    "bist", "scan", "debug", "dft", "test mode", "test", "power-up",
    "power up", "power-down", "power down", "boot", "configuration", "pad mux",
)


def _dedicated_source_label(requirement: Requirement) -> str:
    source = (requirement.source or "").strip()
    source_lower = source.lower()
    if not source:
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
    marker = re.compile(r"(?:^|\s)(?P<mark>•|\d+(?:\.\d+)+|(?:\d+|[a-z])[.)])\s+(?=[A-Za-z])")
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
    lead, items = _split_source_list(payload)
    return [lead] + items if items else [payload]


def _is_analog_relevant(req: Requirement, req_to_block: Dict[str, str], analog_blocks: Set[str]) -> bool:
    # The Stage 1 classification is authoritative: incidental analog-domain
    # wording must not route a Digital requirement into the ARS.
    if req.domain == "DIG":
        return False

    analog_score = _analog_focus_score(req.statement)
    digital_score = _digital_system_score(req.statement)
    if _dedicated_source_label(req):
        return analog_score >= 1 and analog_score >= digital_score
    if req.domain == "ANA":
        return True

    if req.domain == "XDN":
        return analog_score >= max(1, digital_score)

    if req.domain in {"DIG", "SYS"}:
        return False

    mapped = req_to_block.get(req.source_req_id, "")
    if not mapped:
        return False
    tokens = [t.strip() for t in mapped.split(";") if t.strip()]
    has_analog_owner = any(token in analog_blocks for token in tokens)
    if not has_analog_owner:
        return False

    # System-domain requirements are allowed only when analog evidence is at least balanced.
    if req.domain == "SYS":
        return analog_score >= 1 and analog_score >= digital_score

    if analog_score == 0 and digital_score > 0:
        return False
    if digital_score > analog_score:
        return False

    for token in tokens:
        if token in analog_blocks:
            return True
    return False


def _snapshot_ars_targets(requirement_input) -> Dict[str, str]:
    """Map source IDs to the approved snapshot owning target."""
    targets: Dict[str, str] = {}
    for row in requirement_input.rows:
        source_id = str(row.get("source_req_id") or row.get("id") or "").strip()
        canonical_id = str(row.get("canonical_id") or "").strip()
        if not source_id:
            continue
        metadata = requirement_input.allocation.get(canonical_id) or requirement_input.allocation.get(source_id) or {}
        targets[source_id] = str(metadata.get("owning_target") or "").strip()
    return targets


def _split_blocks(mapped_blocks: str) -> List[str]:
    return [canonical_human_label(token) for token in (mapped_blocks or "").split(";") if token.strip()]


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
    if "derived-from-structure" not in metadata and "structural_table_derivation" not in metadata:
        return False
    return "reset" in metadata or "clock" in metadata


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


def _map_requirements_to_analog_blocks(
    requirements: List[Requirement],
    req_to_block: Dict[str, str],
    analog_blocks: Set[str],
) -> Tuple[Dict[str, List[Requirement]], List[Requirement]]:
    by_block: Dict[str, List[Requirement]] = defaultdict(list)
    unmapped: List[Requirement] = []

    for req in requirements:
        if _dedicated_source_label(req):
            unmapped.append(req)
            continue
        mapped_blocks = _split_blocks(req_to_block.get(req.source_req_id, ""))
        matched_blocks = [name for name in mapped_blocks if name in analog_blocks]

        if matched_blocks:
            for block_name in matched_blocks:
                by_block[block_name].append(req)
        else:
            unmapped.append(req)

    return by_block, unmapped


def _describe_block_functionality_from_requirements(requirements: List[Requirement]) -> str:
    if not requirements:
        return "This block has no mapped analog-relevant requirement evidence in the current input set."

    payloads = [_statement_payload(req.statement).rstrip(".") for req in requirements]
    unique_payloads: List[str] = []
    for text in payloads:
        if text and text not in unique_payloads:
            unique_payloads.append(text)

    highlights = unique_payloads[:3]
    if not highlights:
        return "This block implements analog behavior defined by mapped upstream requirements."
    return "This block shall implement mapped analog behavior including: " + "; ".join(highlights) + "."


def _atomic_block_statement(block_name: str, requirement: Requirement) -> str:
    payload = _statement_payload(requirement.statement).rstrip(".")
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


def _build_ars_id_map(requirements: List[Requirement]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for authored_counter, req in enumerate(requirements, start=1):
        out[req.source_req_id] = f"ARS-REQ-{authored_counter:03d}"
    return out


def _write_traceability_csv(
    output_path: Path,
    requirements: List[Requirement],
    ars_id_map: Dict[str, str],
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
                "ars_req_id",
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
                    ars_id_map[req.source_req_id],
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


def _write_ars_markdown(
    output_path: Path,
    source_spec: str,
    project_name: str,
    document_author: str,
    snapshot_id: str,
    document_version: str,
    requirements: List[Requirement],
    ars_id_map: Dict[str, str],
    req_to_block: Dict[str, str],
    block_inventory: List[BlockInfo],
    interface_rows: List[Dict[str, str]],
    source_port_rows: List[Dict[str, str]],
    block_requirements: Dict[str, List[Requirement]],
    unmapped_requirements: List[Requirement],
    non_block_context_rows: List[Dict[str, str]],
    crosscheck_decision: str,
    missing_inputs: List[Path],
    connection_matrix_upstream: Dict[str, str],
    srs_upstream_map: Dict[str, str],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    grouped: Dict[str, List[Requirement]] = defaultdict(list)
    for req in requirements:
        grouped[req.domain].append(req)

    analog_blocks = _inventory_analog_blocks(block_inventory, interface_rows)
    analog_block_rows = [
        b for b in block_inventory if b.name in analog_blocks and block_requirements.get(b.name, [])
    ]
    analog_summary_block_rows = [b for b in block_inventory if b.name in analog_blocks]
    analog_summary_records = [
        {"statement": block.function, "source": f"block inventory: {block.name}"}
        for block in analog_summary_block_rows
        if block.function
    ]
    analog_summary_records.extend(
        {
            "statement": row.get("Non-Block Function Context") or row.get("Source Paragraph") or "",
            "source": row.get("Source Paragraph") or row.get("Requirement ID") or "",
        }
        for row in non_block_context_rows
    )

    def _anchor_slug(text: str) -> str:
        slug = re.sub(r"[^a-z0-9\s-]", "", text.lower())
        slug = re.sub(r"\s+", "-", slug).strip("-")
        return slug

    block_index_entries: List[Tuple[int, str, int, int]] = []
    preview_req_counter = 1
    preview_section_counter = 1
    for block in analog_block_rows:
        reqs = block_requirements.get(block.name, [])
        req_count = len(reqs)
        start_id = preview_req_counter
        end_id = preview_req_counter + req_count - 1
        block_index_entries.append((preview_section_counter, block.name, start_id, end_id))
        preview_req_counter = end_id + 1
        preview_section_counter += 1

    lines: List[str] = []
    lines.append("# Analog Requirements Specification")
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
    lines.append("")
    lines.append("#### Table 3. Section navigation index")
    lines.append("| Section | Paragraph anchor | Internal link | Page (rendered PDF) |")
    lines.append("|---|---|---|---|")
    lines.append(marker_nav)
    lines.append("")

    lines.append("#### Table 4. Analog block navigation index")
    lines.append("| Block | Paragraph anchor | Internal link | Requirement IDs |")
    lines.append("|---|---|---|---|")
    if block_index_entries:
        for sec_idx, block, req_start, req_end in block_index_entries:
            anchor = _anchor_slug(f"7.{sec_idx} {block}")
            req_range = f"ARS-REQ-{req_start:03d}" if req_start == req_end else f"ARS-REQ-{req_start:03d} to ARS-REQ-{req_end:03d}"
            lines.append(f"| {block} | 7.{sec_idx} | [Jump](#{anchor}) | {req_range} |")
    else:
        lines.append("| N/A | N/A | N/A | N/A |")
    lines.append("")

    lines.append("#### Table 5. Requirement paragraph index by block")
    lines.append("| Requirement group | Paragraph anchor | Internal link | Page (rendered PDF) |")
    lines.append("|---|---|---|---|")
    if block_index_entries:
        for sec_idx, block, req_start, req_end in block_index_entries:
            anchor = _anchor_slug(f"7.{sec_idx} {block}")
            req_range = f"ARS-REQ-{req_start:03d}" if req_start == req_end else f"ARS-REQ-{req_start:03d} to ARS-REQ-{req_end:03d}"
            lines.append(f"| {req_range} | 7.{sec_idx} | [{block}](#{anchor}) | Auto |")
    else:
        lines.append("| N/A | N/A | N/A | N/A |")
    lines.append("")

    lines.append("### 0.3 Document control")
    lines.append("")
    lines.append("#### Table 1. Version history")
    lines.extend(document_version_history_markdown(
        output_path, snapshot_id, document_version, today,
        f"Snapshot {snapshot_id} ARS baseline generated from Stage 1 and Stage 2 artifacts", document_author,
    ))
    lines.append("")

    lines.append("#### Table 2. Reference documents")
    lines.append("| Doc name | Version | Author |")
    lines.append("|---|---|---|")
    lines.append(f"| artifacts/stage3_srs/system_requirements_specification.md | {GENERATED_SPEC_VERSION} | SRS Gen Spec Agent |")
    lines.append(f"| artifacts/stage1_requirements/requirements_summary.csv | {GENERATED_SPEC_VERSION} | Requirements Extraction Agent |")
    lines.append(f"| artifacts/stage2_mirco_arc/micro_architecture_report.md | {GENERATED_SPEC_VERSION} | Micro-Architectural Analysis Agent |")
    lines.append(f"| artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv | {GENERATED_SPEC_VERSION} | Micro-Architectural Analysis Agent |")
    lines.append(f"| templates/ARS_gen_AI_template_prompt.md | {GENERATED_SPEC_VERSION} | Project template maintainers |")
    lines.append("")

    lines.append("#### Table 6. Category convention")
    lines.append("| Category | Naming rule / prefix | Scope | Notes / example |")
    lines.append("|---|---|---|---|")
    lines.append("| Analog authored requirement | ARS-REQ-xxx | Project-specific ARS atomic entries | Covers one upstream requirement per row |")
    lines.append("| Source analog/system/cross-domain requirement | source_req_id | Stage 1 source requirement catalog | Linked to authored SRS upstream ID |")
    lines.append("| ARS upstream reference in Covers | SRS-REQ-xxx | Authored SRS requirement catalog | Required for every ARS authored requirement |")
    lines.append("")

    lines.append("### 0.4 Table of tables")
    lines.append("| Table | Title | Link |")
    lines.append("|---|---|---|")
    lines.append("| Table 1 | Version history | [Go to Table 1](#table-1-version-history) |")
    lines.append("| Table 2 | Reference documents | [Go to Table 2](#table-2-reference-documents) |")
    lines.append("| Table 3 | Section navigation index | [Go to Table 3](#table-3-section-navigation-index) |")
    lines.append("| Table 4 | Analog block navigation index | [Go to Table 4](#table-4-analog-block-navigation-index) |")
    lines.append("| Table 5 | Requirement paragraph index by block | [Go to Table 5](#table-5-requirement-paragraph-index-by-block) |")
    lines.append("| Table 6 | Category convention | [Go to Table 6](#table-6-category-convention) |")
    lines.append("")

    lines.append("## 1. Introduction")
    lines.append("")
    lines.append("### 1.1 Purpose")
    lines.append("This document defines verifiable analog requirements derived from Stage 1 and micro-architecture artifacts.")
    lines.append("")
    lines.append("### 1.2 Scope")
    lines.append("This ARS covers analog subsystem behavior, analog interfaces, cross-domain dependencies, and verification hooks.")
    lines.append("")
    lines.append("### 1.3 Intended audience")
    lines.append("Architecture, analog design, validation, and verification stakeholders.")
    lines.append("")
    lines.append("### 1.4 References")
    lines.append("Reference documents are listed in [Table 2. Reference documents](#table-2-reference-documents).")
    lines.append("")

    lines.append("## 2. Definitions and terminology")
    lines.append("- Analog terminology follows source requirements and micro-architecture artifacts.")
    lines.append("")

    lines.append("## 3. System context for analog behavior")
    lines.append("- System context is summarized to scope analog requirements and mixed-signal interfaces.")
    lines.append("")
    lines.append("### 3.1 Analog Main Functions")
    lines.append("")
    analog_topics = DESCRIPTIVE_ANALOG_TOPIC_SPECS
    analog_summary = organize_descriptive_topics(analog_summary_records, analog_topics)
    if analog_summary:
        for topic, entries in analog_summary.items():
            lines.append(f"#### {topic}")
            lines.extend(f"- {entry}" for entry in entries)
            lines.append("")
    else:
        lines.append("No descriptive analog functions were identified in the approved architecture context.")
        lines.append("")
    low_power_grouped, _low_power_audit = assemble_low_power_descriptive(
        [dict(record, scope="block_local", domain="analog_or_mixed") for record in analog_summary_records],
        repo_root=_resolve_repo_root(),
        profile="ars",
    )
    lines.extend(render_low_power_topics(low_power_grouped))

    lines.append("## 4. Analog requirements")
    lines.append("")
    lines.append("General analog requirements that are not mapped to any included analog block are listed below.")
    residual_requirements = [req for req in unmapped_requirements if not _dedicated_source_label(req)]
    if residual_requirements:
        unmapped_ids = ", ".join(req.source_req_id for req in residual_requirements)
        lines.append(f"Unmapped analog-relevant requirements: {unmapped_ids}.")
    else:
        lines.append("All non-dedicated analog-relevant requirements are mapped to at least one analog block section.")
    lines.append("")

    lines.append("### 4.1 Analog block list")
    if analog_block_rows:
        lines.append("Analog-related implementation shall include blocks: " + ", ".join(b.name for b in analog_block_rows) + ".")
    else:
        lines.append("Analog block list shall be derived from block inventory evidence.")
    lines.append("")

    lines.append("### 4.2 Analog I/O characteristics")
    analog_if = [
        r for r in interface_rows
        if "analog" in (r.get("Type") or "").lower() or "sensor" in (r.get("Interface") or "").lower()
    ]
    if analog_if:
        lines.append("Relevant analog interfaces include " + "; ".join((r.get("Interface") or "") for r in analog_if[:10]) + ".")
    else:
        lines.append("Analog I/O characteristics shall be verified from interface catalog evidence.")
    lines.append("Applicable source context tables include PMU I/O List and Sensor Hub I/O List; detailed port definitions remain in the owning Analog IPOS specification.")
    for table_title in ("PMU I/O List", "Sensor Hub I/O List"):
        port_names = [
            row.get("Port name", "").strip()
            for row in source_port_rows
            if row.get("Table title", "").strip() == table_title
            and row.get("Ownership status", "").strip().lower() == "approved"
            and row.get("Port name", "").strip()
        ]
        if port_names:
            lines.append(f"Source context ports for {table_title}: " + ", ".join(port_names) + ".")
    lines.append("Detailed analog block inputs, outputs, ports, and source I/O tables are maintained only in the owning Analog IPOS specification.")
    lines.append("")

    lines.append("### 4.3 Sampling and conversion")
    lines.append("Sampling, conversion, and resolution behavior shall satisfy timing and accuracy constraints from source requirements.")
    lines.append("")

    lines.append("### 4.4 Analog operating modes")
    lines.append("Analog operating behavior shall remain consistent across manual, schedule, off, and fault-degraded scenarios.")
    lines.append("")

    lines.append("### 4.5 Analog calibration and test requirements")
    lines.append("Calibration and observability requirements shall be defined for offset/gain handling and verification access.")
    lines.append("")

    lines.append("### 4.6 Analog performance requirements")
    lines.append("Performance requirements shall cover noise, accuracy, range, drift, and response constraints.")
    lines.append("")

    lines.append("## 5. Validation and qualification requirements")
    lines.append("- Verification shall combine inspection, analysis, and test with measurable acceptance criteria.")
    lines.append("")

    lines.append("## 6. Requirement identification and traceability")
    lines.append("### 6.1 Numbering convention")
    lines.append("ARS IDs use domain-prefixed numbering: ANA-RQ-### and XDN-RQ-###. Newly authored requirements in project-specific sub-block requirement paragraphs use ARS-REQ-###.")
    lines.append("")
    lines.append("### 6.2 Traceability contract")
    lines.append("ARS requirement catalog entries include statement only; full traceability details are maintained in artifacts/stage4_ars/ars_traceability_matrix.csv.")
    lines.append("")

    lines.append("### 6.3 Requirement catalog")
    lines.append("")
    mapped_source_ids: Set[str] = set()
    for req_list in block_requirements.values():
        for req in req_list:
            mapped_source_ids.add(req.source_req_id)
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
            for req in sorted(dedicated_groups[group_name], key=lambda item: ars_id_map.get(item.source_req_id, item.source_req_id)):
                lines.append(f"[{ars_id_map[req.source_req_id]}] Requirement:")
                lines.extend(_source_body_lines(req))
                lines.append(f"Covers: {srs_upstream_map.get(req.source_req_id, 'SRS-REQ-000')}")
                lines.append("")

    for domain in ["ANA", "XDN"]:
        items = [
            req
            for req in grouped.get(domain, [])
            if req.source_req_id not in mapped_source_ids
            and req.source_req_id not in context_source_ids
            and req.source_req_id not in user_specific_ids
            and not _dedicated_source_label(req)
        ]
        title = "Analog" if domain == "ANA" else "Cross-domain"
        lines.append(f"#### {title} requirements")
        if not items:
            lines.append("- No residual unmapped requirements for this domain (mapped items are captured in project-specific analog sub-block requirement paragraphs).")
            lines.append("")
            continue
        for req in items:
            lines.append(f"[{ars_id_map[req.source_req_id]}] Requirement:")
            lines.append(req.statement)
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
                key=lambda item: ars_id_map.get(item.source_req_id, item.source_req_id),
            ):
                lines.append(f"[{ars_id_map[req.source_req_id]}] Requirement:")
                lines.append(req.statement)
                lines.append(f"Covers: {_upstream_id(req.source_req_id, srs_upstream_map)}")
                lines.append("")

    lines.append("## 7. Project-specific analog block sections")
    lines.append("")
    idx = 1
    emitted_source_ids: Set[str] = set()
    for block in analog_block_rows:
        lines.append(f"### 7.{idx} {block.name}")
        reqs = block_requirements.get(block.name, [])
        reqs_sorted = [
            req
            for req in sorted(reqs, key=lambda item: ars_id_map.get(item.source_req_id, item.source_req_id))
            if req.source_req_id not in emitted_source_ids
        ]
        if not reqs_sorted:
            lines.pop()
            continue

        lines.append("General functional description: " + block.function)
        lines.append("")
        lines.append("Inputs: " + (block.inputs or "N/A"))
        lines.append("Outputs: " + (block.outputs or "N/A"))
        lines.append("")

        for req in reqs_sorted:
            emitted_source_ids.add(req.source_req_id)
            lines.append(f"[{ars_id_map[req.source_req_id]}] Requirement:")
            lines.extend(_atomic_block_statement(block.name, req).splitlines())
            lines.append(f"Covers: {_upstream_id(req.source_req_id, srs_upstream_map)}")
            lines.append("")
            lines.append("")

        lines.append("")
        idx += 1

    if non_block_context_rows:
        lines.append("## 6.4 Source Function Context {#64-source-function-context}")
        lines.append("")
        grouped_context: Dict[str, List[Dict[str, str]]] = defaultdict(list)
        for row in non_block_context_rows:
            grouped_context[row.get("Non-Block Function Context") or "Unresolved source paragraph"].append(row)
        for context_index, (context, rows) in enumerate(sorted(grouped_context.items()), start=1):
            paragraph_number = f"6.4.{context_index}"
            lines.append(f"### {paragraph_number} {context} {{#{_anchor_slug(paragraph_number + ' ' + context)}}}")
            lines.append("")
            for row in rows:
                source_req_id = (row.get("Requirement ID") or "").strip()
                requirement = requirements_by_source_id.get(source_req_id)
                if requirement is None or source_req_id not in ars_id_map:
                    continue
                lines.append(f"[{ars_id_map[source_req_id]}] Requirement:")
                lines.extend(_source_body_lines(requirement))
                lines.append(f"Covers: {_upstream_id(source_req_id, srs_upstream_map)}")
                lines.append(f"Source paragraph: {row.get('Source Paragraph') or 'Unknown'}")
                lines.append("")

    lines.append("## 8. Assumptions and TBD")
    lines.append("- ASSUME-001: Analog validation environments provide representative sensor and load stimulus.")
    lines.append("- TBD-001: Unassigned requirements in ARS traceability matrix require architectural owner review.")
    if crosscheck_decision == "no-go":
        lines.append("- TBD-002: Micro-architecture crosscheck is no-go; unresolved critical findings may affect ARS closure.")
    lines.append("")

    lines.append("## 9. Missing Inputs")
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
    anchors = {anchor for _level, _title, anchor, _num in heading_registry}

    def _replace_if_missing(fragment: str, fallback: str) -> str:
        return fallback if fragment not in anchors and fallback in anchors else fragment

    lines_rendered: List[str] = []
    link_re = re.compile(r"\]\(#([^)]+)\)")
    for line in lines:
        text = _to_text(line)
        def _fix_link(m: re.Match[str]) -> str:
            frag = m.group(1).strip().lower()
            fixed = _replace_if_missing(frag, frag)
            return f"](#{fixed})"
        text = link_re.sub(_fix_link, text)
        lines_rendered.append(text)

    lines_rendered = _ensure_blank_line_between_paragraphs(lines_rendered)
    lines_rendered = _ensure_requirement_block_spacing(lines_rendered)
    lines_rendered = _ensure_subparagraph_heading_spacing(lines_rendered)
    lines_rendered = _ensure_table_block_spacing(lines_rendered)
    lines_rendered = _insert_visible_paragraph_spacers(lines_rendered)
    lines_rendered = _terminate_authored_requirement_blocks(lines_rendered)
    output_path.write_text("\n".join(item.replace("•", "-").replace("●", "-") for item in lines_rendered) + "\n", encoding="utf-8")


def _write_stage_report(
    output_path: Path,
    present_inputs: List[Path],
    missing_inputs: List[Path],
    requirements: List[Requirement],
    unmapped_requirements: List[Requirement],
    full_traceability_count: int,
    unassigned_count: int,
    crosscheck_decision: str,
) -> str:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    counts = defaultdict(int)
    for req in requirements:
        counts[req.domain] += 1

    status = "pass"
    blocking_issues: List[str] = []

    if missing_inputs:
        blocking_issues.append(f"Missing required input artifacts: {len(missing_inputs)}")
    if crosscheck_decision == "no-go":
        blocking_issues.append("Micro-architecture crosscheck decision is no-go")
    if blocking_issues:
        status = "fail"

    lines: List[str] = [
        "# Stage ARS Report",
        "",
        f"Date: {today}",
        "",
        f"ARS generation status: {status}",
        "",
        "## Input artifact coverage summary",
        f"- Present inputs: {len(present_inputs)}",
        f"- Missing inputs: {len(missing_inputs)}",
        "",
        "## Count of generated ARS requirements by domain",
        f"- ANA: {counts['ANA']}",
        f"- XDN: {counts['XDN']}",
        "",
        "## Count of requirements with full traceability",
        f"- Fully mapped to owning block: {full_traceability_count}",
        f"- Unassigned owning block: {unassigned_count}",
        f"- Unmapped to included analog blocks: {len(unmapped_requirements)}",
        "",
        "## Open TBD/assumptions list",
        "- ASSUME-001: Analog validation environments provide representative sensor and load stimulus.",
        "- TBD-001: Unassigned requirements in ARS traceability matrix require architectural owner review.",
        f"- Stage 2 micro-architecture crosscheck decision: {crosscheck_decision}",
        "",
        "## Unmapped analog requirements",
    ]

    if unmapped_requirements:
        lines.extend([f"- {req.source_req_id}" for req in unmapped_requirements])
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
        raise RuntimeError(f"ARS md->docx conversion failed with exit code {rc}")
    apply_docx_authored_requirement_formatting(output_docx_path, ("ARS",))
    apply_docx_common_spec_formatting(output_docx_path)
    _validate_docx_end_markers(markdown_path, output_docx_path)


def _validate_docx_end_markers(markdown_path: Path, docx_path: Path) -> None:
    expected = len(re.findall(r"^[ \t]*\[End\][ \t]*$", markdown_path.read_text(encoding="utf-8"), flags=re.M | re.I))
    with zipfile.ZipFile(docx_path) as archive:
        document_xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
    if document_xml.lower().count("[end]") < expected:
        raise RuntimeError("ARS DOCX does not preserve all visible [End] requirement terminators")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run ARS generation agent workflow")
    parser.add_argument("--agent-file", default=".github/agents/ars_gen_spec.agent.md", help="Path to agent definition markdown")
    parser.add_argument("--template-file", default="templates/ARS_gen_AI_template_prompt.md", help="Path to ARS generation template markdown")
    parser.add_argument("--requirements-summary", help="Deprecated compatibility option; resolver snapshot is authoritative")
    parser.add_argument("--req-block-trace", default="artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv", help="Requirement to block traceability CSV")
    parser.add_argument("--block-inventory", default="artifacts/stage2_mirco_arc/block_inventory.csv", help="Block inventory CSV")
    parser.add_argument("--interface-catalog", default="artifacts/stage2_mirco_arc/interface_catalog.csv", help="Interface catalog CSV")
    parser.add_argument("--architecture-crosscheck", default="artifacts/stage2_mirco_arc/architecture_crosscheck_report.md", help="Architecture crosscheck report markdown")
    parser.add_argument("--srs-traceability", default="artifacts/stage3_srs/srs_traceability_matrix.csv", help="SRS traceability CSV (source_req_id -> srs_req_id)")
    parser.add_argument("--out-ars-md", default="artifacts/stage4_ars/analog_requirements_specification.md", help="Output ARS markdown path")
    parser.add_argument("--out-ars-docx", default="artifacts/stage4_ars/analog_requirements_specification.docx", help="Output ARS DOCX path")
    parser.add_argument("--out-traceability-csv", default="artifacts/stage4_ars/ars_traceability_matrix.csv", help="Output ARS traceability CSV path")
    parser.add_argument("--out-stage-report", default="artifacts/orchestrator/stage_ars_report.md", help="Output Stage ARS report path")
    parser.add_argument("--docx-reference-template", default=DOCX_REFERENCE_TEMPLATE, help="DOCX reference template path for pandoc conversion")
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
        print("ARS agent run: FAIL (Stage 2+ source-spec independence guard failed)")
        _append_log(repo_root, script_name, f"FAIL stage2_plus_guard_exit={guard_rc}")
        return guard_rc

    agent_file = (repo_root / args.agent_file).resolve()
    template_file = (repo_root / args.template_file).resolve()
    context = json.loads((repo_root / "config" / "project_context.json").read_text(encoding="utf-8"))
    requirement_input, selection = resolve_complete_authoritative_input(
        repo_root,
        "5",
        project_id=str(context.get("project_name") or repo_root.name),
        snapshot_id=args.snapshot_id,
    )
    downstream_contract = resolve_downstream_contract(repo_root, requirement_input.snapshot_id)
    coherence = validate_downstream_coherence(repo_root, requirement_input.snapshot_id)
    if not args.regenerate_downstream and coherence["decision"] != "PASS":
        raise RuntimeError(f"Downstream snapshot coherence blocked ARS generation: {coherence['finding_count']} findings")
    _append_log(repo_root, script_name, f"AUTHORITATIVE_SNAPSHOT snapshot_id={selection['selected_snapshot_id']} mode={selection['selection_mode']} user={runtime_user_name()}")
    summary_csv = requirement_input.source_path
    req_block_trace_csv = (repo_root / args.req_block_trace).resolve()
    block_inventory_csv = (repo_root / args.block_inventory).resolve()
    interface_catalog_csv = (repo_root / args.interface_catalog).resolve()
    architecture_crosscheck_md = (repo_root / args.architecture_crosscheck).resolve()
    srs_traceability_csv = (repo_root / args.srs_traceability).resolve()

    out_ars_md = (repo_root / args.out_ars_md).resolve()
    document_version = document_version_for_snapshot(out_ars_md, requirement_input.snapshot_id)
    out_ars_docx = (repo_root / args.out_ars_docx).resolve()
    out_traceability_csv = (repo_root / args.out_traceability_csv).resolve()
    out_stage_report = (repo_root / args.out_stage_report).resolve()
    docx_reference_template = (
        (repo_root / args.docx_reference_template).resolve()
        if args.docx_reference_template
        else None
    )

    if docx_reference_template and docx_reference_template.exists():
        print(f"ARS agent run: INFO (format reference template: {docx_reference_template})")
        _append_log(repo_root, script_name, f"INFO docx_reference_template={docx_reference_template}")
    elif docx_reference_template:
        print(f"ARS agent run: WARN (reference template not found: {docx_reference_template})")
        _append_log(repo_root, script_name, f"WARN missing_docx_reference_template={docx_reference_template}")

    present_inputs, missing_inputs = _check_inputs(repo_root)

    if not agent_file.exists():
        print(f"ARS agent run: FAIL (missing agent file: {agent_file})")
        _append_log(repo_root, script_name, f"FAIL missing_agent={agent_file}")
        return 1

    if not summary_csv.exists():
        print(f"ARS agent run: FAIL (missing requirements summary: {summary_csv})")
        _append_log(repo_root, script_name, f"FAIL missing_summary={summary_csv}")
        return 1

    if not template_file.exists():
        print(f"ARS agent run: FAIL (missing prompt template: {template_file})")
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
        refresh_ledger(repo_root, snapshot_id=requirement_input.snapshot_id, source_rows=requirement_input.rows)
        snapshot_targets = {
            source_id: downstream_contract.target(source_id)
            for source_id in {
                str(row.get("source_req_id") or row.get("id") or "").strip()
                for row in requirement_input.rows
                if str(row.get("source_req_id") or row.get("id") or "").strip()
            }
        }
        missing_targets = sorted(
            requirement.source_req_id
            for requirement in all_requirements
            if not snapshot_targets.get(requirement.source_req_id)
        )
        if missing_targets:
            raise ValueError(
                "Approved snapshot allocation is missing owning_target for ARS inputs: "
                + ", ".join(missing_targets[:10])
            )
        req_to_block = _read_req_to_block(req_block_trace_csv)
        srs_upstream_map = _read_srs_upstream_map(srs_traceability_csv)
        block_inventory = _read_block_inventory(block_inventory_csv)
        _require_block_functions(block_inventory)
        interface_rows = _read_interface_rows(interface_catalog_csv)
        interaction_rows = _read_interface_rows((repo_root / "artifacts/stage2_mirco_arc/interaction_matrix.csv").resolve())
        connection_matrix_upstream = _connection_matrix_upstream_ids(interaction_rows)
        crosscheck_decision = _extract_crosscheck_decision(architecture_crosscheck_md)
        non_block_context_rows = _read_non_block_context_rows(
            repo_root / "artifacts/stage2_mirco_arc/unmapped_requirement_routing.csv",
            {requirement.source_req_id for requirement in all_requirements},
        )
        non_block_source_ids = {
            row.get("Requirement ID", "").strip()
            for row in non_block_context_rows
            if row.get("Requirement ID", "").strip()
        }

        analog_blocks = _inventory_analog_blocks(block_inventory, interface_rows)
        selected_requirements = [
            r for r in all_requirements
            if snapshot_targets.get(r.source_req_id) == "ARS"
        ]

        normalized_requirements: List[Requirement] = []
        for r in selected_requirements:
            dom = "ANA" if r.domain == "ANA" else "XDN"
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

        _require_srs_upstream_map(normalized_requirements, srs_upstream_map)

        allocation_by_source = {
            requirement.source_req_id: downstream_contract.allocation(requirement.source_req_id)
            for requirement in normalized_requirements
        }

        normalized_req_to_block = {
            requirement.source_req_id: (
                (requirement_input.allocation.get(
                    next(row.get("canonical_id", "") for row in requirement_input.rows
                         if row.get("source_req_id", "") == requirement.source_req_id),
                    {}) or {}
                ).get("approved_block", "").strip()
                or "Unassigned"
            )
            for requirement in normalized_requirements
        }

        block_requirements, unmapped_requirements = _map_requirements_to_analog_blocks(
            normalized_requirements,
            normalized_req_to_block,
            analog_blocks,
        )
        ars_id_map = _build_ars_id_map(normalized_requirements)
        full_traceability_count, unassigned_count = _write_traceability_csv(
            out_traceability_csv, normalized_requirements, ars_id_map, normalized_req_to_block,
            allocation_by_source, requirement_input.snapshot_id
        )
        descriptive_records = [
            {"statement": block.function, "source": f"block inventory: {block.name}"}
            for block in block_inventory
            if block.function and block.name in analog_blocks
        ]
        descriptive_records.extend(
            {
                "statement": row.get("Non-Block Function Context") or row.get("Source Paragraph") or "",
                "source": row.get("Source Paragraph") or row.get("Requirement ID") or "",
            }
            for row in non_block_context_rows
        )
        write_descriptive_audit(
            out_ars_md.with_name("descriptive_summary_audit.csv"),
            assemble_descriptive_summary(descriptive_records, DESCRIPTIVE_ANALOG_TOPIC_SPECS),
            section="Analog Main Functions",
        )
        low_power_grouped, low_power_audit = assemble_low_power_descriptive(
            [dict(record, scope="block_local", domain="analog_or_mixed") for record in descriptive_records],
            repo_root=repo_root,
            profile="ars",
        )
        write_low_power_audit(out_ars_md.with_name("descriptive_low_power_audit.csv"), low_power_audit)
        _write_ars_markdown(
            out_ars_md,
            source_spec,
            str(project_context.get("project_name") or "Project"),
            document_author_name(),
            requirement_input.snapshot_id,
            document_version,
            normalized_requirements,
            ars_id_map,
            normalized_req_to_block,
            block_inventory,
            interface_rows,
            _read_interface_rows((repo_root / "artifacts/stage2_mirco_arc/source_port_catalog.csv").resolve()),
            block_requirements,
            unmapped_requirements,
            non_block_context_rows,
            crosscheck_decision,
            missing_inputs,
            connection_matrix_upstream,
            srs_upstream_map,
        )
        docx_generated = False
        if shutil.which("pandoc") is None:
            raise RuntimeError("pandoc is required for ARS DOCX generation but is not available on PATH")
        if docx_reference_template is not None and not docx_reference_template.exists():
            raise FileNotFoundError(f"Missing DOCX reference template: {docx_reference_template}")
        _convert_markdown_to_docx(out_ars_md, out_ars_docx, docx_reference_template, repo_root)
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
        )

        ars_crosscheck_cmd = [sys.executable, "scripts/run_ars_crosscheck_agent.py"]
        ars_crosscheck_rc = subprocess.run(ars_crosscheck_cmd, cwd=repo_root).returncode
        if ars_crosscheck_rc != 0:
            raise RuntimeError(f"ARS crosscheck failed with exit code {ars_crosscheck_rc}")
    except Exception as exc:
        print(f"ARS agent run: FAIL ({exc})")
        print(traceback.format_exc())
        _append_log(repo_root, script_name, f"FAIL error={exc}")
        return 1

    print("ARS agent run: PASS")
    print(f"- Agent definition: {agent_file}")
    print(f"- Prompt template: {template_file}")
    print(f"- ARS markdown: {out_ars_md}")
    if docx_generated:
        print(f"- ARS DOCX: {out_ars_docx}")
    else:
        print("- ARS DOCX: not generated")
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
