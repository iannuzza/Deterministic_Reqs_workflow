#!/usr/bin/env python3
"""Generate Stage 1 requirement outputs from OCR extracts.

This script parses OCR page text files, detects normative statements,
and writes Stage 1 artifacts used by downstream gates.
"""

from __future__ import annotations

import argparse
import csv
import html as html_lib
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from repo_paths import portable_repo_path, resolve_repo_path
from typing import Dict, List, Optional, Tuple
from workflow_routing import source_parent_title

NORMATIVE_PATTERNS = [
    r"\bshall\b",
    r"\bmust\b",
    r"\bmandatory\b",
    r"\bis\s+required\b",
    r"\bare\s+required\b",
    r"\brequired\s+to\b",
    r"\bneeds?\s+to\b",
    r"\bshall\s+not\b",
    r"\bmust\s+not\b",
    r"\bnot\s+be\b",
    r"\bis\s+the\s+maximum\b",
    r"\bis\s+the\s+minimum\b",
    r"\bavailable\s+to\s+the\s+user\b",
    r"\btolerance\b",
    r"\bpass\s*/\s*fail\b",
    r"\bpass\s+criteria\b",
    r"\bfail\s+criteria\b",
    r"\bcompliance\s+criteria\b",
]

FUNCTIONAL_SUBJECT_PATTERN = re.compile(
    r"\b("
    r"device|sensor|sensing element|"
    r"firmware|microcontroller|processor|controller|host|application|"
    r"interface|digital interface|analog interface|spi|i2c|uart|register|fifo|"
    r"interrupt|clock|reset|calibration|temperature|voltage|supply|power|"
    r"mode|configuration|command|output|data"
    r")\b",
    flags=re.IGNORECASE,
)

FUNCTIONAL_VERB_PATTERN = re.compile(
    r"\b("
    r"measures?|controls?|drives?|supports?|provides?|uses?|maintains?|restores?|"
    r"computes?|switch(?:es|ed)?|remains?|operates?|compares?|detects?|marks?|"
    r"records?|responds?|generates?|allows?|process(?:es)?|signals?|forces?|"
    r"stores?|fills?|stops?|discards?|restarts?|reads?|writes?|acquires?|"
    r"places?|triggers?|enabled?|selected?|configured?|followed|leads?"
    r"extends?|includes?|is connected|is powered|is forced|is able|is selected|"
    r"is less than|is greater than|is at least|is within"
    r")\b",
    flags=re.IGNORECASE,
)

NON_REQUIREMENT_SENTENCE_PATTERN = re.compile(
    r"\b("
    r"this document|this section summarizes|specification is intended|does not cover|"
    r"preparation of test plans|support internal detailed specifications|these features allow"
    r")\b",
    flags=re.IGNORECASE,
)

DEFAULT_REQ_ID_PATTERN = r"[A-Z][A-Z0-9]*(?:\.\d+)*[A-Z0-9]*"
REQ_ID_PATTERN = DEFAULT_REQ_ID_PATTERN
TABLE_REQ_ID_PATTERN = DEFAULT_REQ_ID_PATTERN
REQ_ID_DEFINITION_RE = re.compile(rf"^\s*(?P<reqid>{REQ_ID_PATTERN})\s*:\s*(?P<body>.*)$")
REQ_ID_ONLY_RE = re.compile(rf"^\s*(?P<reqid>{REQ_ID_PATTERN})\s*$")
REQ_ID_INLINE_DEFINITION_RE = re.compile(rf"\b(?P<reqid>{REQ_ID_PATTERN})\s*:\s*")
SOURCE_REQ_ID_NOTE_RE = re.compile(rf"\bsource_req_id=(?P<reqid>{REQ_ID_PATTERN})\b")
TAGGED_SOURCE_MODE = False
TAG_REQUIREMENT_LABEL = "Requirement"
TAG_REQUIRES_LABEL = True
TAG_TERMINATOR = "[End]"
TABLE_CONTEXT_REQUIRED = True
ALLOW_COMPACT_IDS = False
NON_REQUIREMENT_ID_LABELS = {
    "definition",
    "description",
    "assumption",
    "note",
    "reference",
    "n/a",
}
TABLE_ID_COLUMNS_PRIORITY: List[str] = ["Spec ID", "Req_id", "ID"]
REQ_ID_TAGGED_START_RE = re.compile(rf"^\s*\[(?P<reqid>{REQ_ID_PATTERN})\]\s*{re.escape(TAG_REQUIREMENT_LABEL)}\s*:?\s*(?P<body>.*)$", re.IGNORECASE)
TAGGED_REQID_FALLBACK_RE = re.compile(rf"\[(?P<reqid>{REQ_ID_PATTERN})\]", re.IGNORECASE)
TABLE_REQID_RE = re.compile(rf"(?<![A-Za-z0-9_])(?P<reqid>{REQ_ID_PATTERN})(?![A-Za-z0-9_])", re.IGNORECASE)
REQ_ID_HEADER_FALLBACK_RE = re.compile(r"\b(?:req(?:uirement)?|spec)\s*[_\-\s]*id\b", re.IGNORECASE)
CUSTOM_REQ_ID_FAMILY_RE = re.compile(r"\b([A-Z]{2,}(?:_[A-Z0-9]+)+_\d{2,})\b", re.IGNORECASE)
SPEC_ID_SIMPLE_RE = re.compile(r"\b([A-Z]{1,4}\d{1,4}[A-Z]?)\b")
REQ_ID_TOKEN_RE = re.compile(r"\b([A-Z][A-Z0-9_]*\d+(?:[A-Z0-9_]|[.-]\d+)*)\b")

DEFAULT_ARCHITECTURE_ANALYSIS_RULES = {
    "power_concepts": [
        "power domain",
        "power island",
        "power mode",
        "power gating",
        "retention domain",
        "isolation domain",
        "low-power",
        "low power",
        "power-aware",
        "power aware",
        "power state",
        "power sequence",
        "power sequencing",
    ],
    "architecture_subject_terms": [
        "architecture", "block", "subsystem", "domain", "island", "controller",
        "unit", "manager", "interface", "path", "sequence", "mode", "function",
        "capability", "system",
    ],
    "capability_verbs": [
        "is", "are", "provide", "provides", "support", "supports", "include",
        "includes", "consists of", "comprise", "comprises", "responsible for",
        "used to", "enable", "enables", "implement", "implements", "control",
        "controls", "manage", "manages", "handle", "handles",
    ],
}
POWER_MANAGEMENT_CONCEPT_RE = re.compile(
    r"\b(?:power\s+(?:domain|island|mode|gating|management|manager|controller)|"
    r"retention\s+domain|isolation\s+domain|low[- ]power|power[- ]aware|"
    r"power\s+state|power\s+sequenc(?:e|ing))\b",
    flags=re.IGNORECASE,
)
ARCHITECTURE_SUBJECT_RE = re.compile(
    r"\b(?:architecture|block|subsystem|domain|island|controller|unit|manager|"
    r"interface|path|sequence|mode|function|capability|system)\b",
    flags=re.IGNORECASE,
)
ARCHITECTURE_CAPABILITY_RE = re.compile(
    r"\b(?:is|are|provides?|supports?|includes?|consists?\s+of|comprises?|"
    r"responsible\s+for|used\s+to|enables?|implements?|controls?|manages?|handles?)\b",
    flags=re.IGNORECASE,
)

DIGITAL_HINTS = [
    "i2c",
    "spi",
    "fifo",
    "stream mode",
    "bypass mode",
    "watermark",
    "drdy",
    "int1",
    "int2",
    "sda",
    "scl",
    "register",
    "ctrl",
    "bit",
    "serial",
    "interface",
    "chip select",
    "cs",
    "otp",
]

ANALOG_HINTS = [
    "voltage",
    "current",
    "noise",
    "offset",
    "gain",
    "bandwidth",
    "filter",
    "adc",
    "temperature",
    "analog",
    "drift",
]

BLOCK_FUNCTION_KEYWORDS = [
    ("fifo", "Digital", ["fifo", "buffer", "data"]),
    ("adc", "Analog", ["analog", "digital", "conversion", "adc"]),
    ("temperature sensor", "Analog", ["temperature", "sensor", "measurement"]),
    ("digital filtering", "Digital", ["filter", "digital", "bandwidth"]),
    ("control logic", "Digital", ["control", "logic", "mode", "state"]),
    ("interrupt generator", "Digital", ["interrupt", "int1", "int2", "drdy"]),
    ("i2c", "Digital", ["i2c", "serial", "interface"]),
    ("spi", "Digital", ["spi", "serial", "interface"]),
    ("mux", "Digital", ["mux", "select", "switch"]),
    ("reference", "Analog", ["reference", "signal", "bias"]),
    ("charge amp", "Analog", ["charge", "amplifier", "signal"]),
    ("phase generator", "Digital", ["phase", "clock", "generator"]),
    ("clock", "Digital", ["clock", "timing", "cycle"]),
    ("low-pass filter", "Analog", ["low-pass", "filter", "bandwidth"]),
    ("high-pass filter", "Analog", ["high-pass", "filter", "bandwidth"]),
]

TIMING_TABLE_HEADER_RE = re.compile(r"^Table\s+(?P<table_no>\d+)\.\s+(?P<title>.*timing values.*)$", re.IGNORECASE)
GENERIC_TABLE_HEADER_RE = re.compile(r"^Table\s+(?P<table_no>\d+)\.\s+(?P<title>.+)$", re.IGNORECASE)
TIMING_ROW_RE = re.compile(r"^(?P<symbol>[A-Za-z][A-Za-z0-9_]*(?:\([^)]+\))?)\s+(?P<rest>.+)$")
TIMING_ROW_BOUNDARY_RE = re.compile(r"^(Table\s+\d+\.|Figure\s+\d+\.|\d+(?:\.\d+){0,3}\.?\s+[A-Za-z])", re.IGNORECASE)
TIMING_UNIT_ONLY_RE = re.compile(r"^(ns|us|µs|ms|s|kHz|MHz|Hz)$", re.IGNORECASE)
TIMING_HEADER_LINE_RE = re.compile(r"^(Symbol|Parameter|Value|Unit|Min\.|Max\.|Min\s+Max\.|Subject to general operating)", re.IGNORECASE)
MEASUREMENT_HEADER_LINE_RE = re.compile(r"^(Symbol|Parameter|Value|Unit|Min\.|Max\.|Typ\.|Condition|Ratings|Notes)$", re.IGNORECASE)
FIGURE_BLOCK_CAPTION_RE = re.compile(r"^Figure\s+(?P<fig_no>\d+)\.\s+(?P<title>.*block\s+diagram.*)$", re.IGNORECASE)

ANALOG_MEASUREMENT_TITLE_HINT_RE = re.compile(
    r"(electrical\s+characteristics|mechanical\s+characteristics|temperature\s+sensor\s+characteristics|"
    r"absolute\s+maximum\s+ratings|measurement|sensitivity|noise|offset|supply|voltage|current)",
    re.IGNORECASE,
)
ANALOG_MEASUREMENT_ROW_HINT_RE = re.compile(
    r"(voltage|current|temperature|sensitivity|noise|offset|range|bandwidth|dps|g|mg|°c|ma|ua|v|hz|khz|mhz)",
    re.IGNORECASE,
)
NOISE_TABLE_SYMBOLS = {
    "SYMBOL",
    "PARAMETER",
    "VALUE",
    "UNIT",
    "MIN",
    "MAX",
    "TYP",
    "RATINGS",
    "CONDITION",
    "NOTES",
    "DS10938",
}



def _load_project_context(repo_root: Path) -> Dict[str, object]:
    config_path = repo_root / "config/project_context.json"
    if not config_path.exists():
        return {}
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _compile_architecture_rule_terms(terms: object) -> Optional[re.Pattern[str]]:
    if not isinstance(terms, list):
        return None
    normalized = [str(term).strip() for term in terms if str(term).strip()]
    if not normalized:
        return None
    return re.compile(
        r"\b(?:" + "|".join(re.escape(term) for term in sorted(normalized, key=len, reverse=True)) + r")\b",
        flags=re.IGNORECASE,
    )


def _init_architecture_analysis_rules(repo_root: Path) -> None:
    global POWER_MANAGEMENT_CONCEPT_RE
    global ARCHITECTURE_SUBJECT_RE
    global ARCHITECTURE_CAPABILITY_RE

    rules = dict(DEFAULT_ARCHITECTURE_ANALYSIS_RULES)
    taxonomy_path = repo_root / "config/ontology_role_taxonomy.json"
    try:
        taxonomy = json.loads(taxonomy_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        taxonomy = {}
    configured = taxonomy.get("architecture_analysis") if isinstance(taxonomy, dict) else None
    if isinstance(configured, dict):
        for key in rules:
            if isinstance(configured.get(key), list) and configured[key]:
                rules[key] = configured[key]

    POWER_MANAGEMENT_CONCEPT_RE = (
        _compile_architecture_rule_terms(rules["power_concepts"])
        or POWER_MANAGEMENT_CONCEPT_RE
    )
    ARCHITECTURE_SUBJECT_RE = (
        _compile_architecture_rule_terms(rules["architecture_subject_terms"])
        or ARCHITECTURE_SUBJECT_RE
    )
    ARCHITECTURE_CAPABILITY_RE = (
        _compile_architecture_rule_terms(rules["capability_verbs"])
        or ARCHITECTURE_CAPABILITY_RE
    )


def _compile_requirement_id_regexes(req_id_pattern: str, table_req_id_pattern: Optional[str] = None) -> None:
    global REQ_ID_PATTERN
    global REQ_ID_DEFINITION_RE
    global REQ_ID_ONLY_RE
    global REQ_ID_INLINE_DEFINITION_RE
    global SOURCE_REQ_ID_NOTE_RE
    global REQ_ID_TAGGED_START_RE
    global TAGGED_REQID_FALLBACK_RE
    global TABLE_REQID_RE
    global TABLE_REQ_ID_PATTERN

    REQ_ID_PATTERN = req_id_pattern
    TABLE_REQ_ID_PATTERN = table_req_id_pattern or req_id_pattern
    REQ_ID_DEFINITION_RE = re.compile(rf"^\s*(?P<reqid>{REQ_ID_PATTERN})\s*:\s*(?P<body>.*)$")
    REQ_ID_ONLY_RE = re.compile(rf"^\s*(?P<reqid>{REQ_ID_PATTERN})\s*$")
    REQ_ID_INLINE_DEFINITION_RE = re.compile(rf"\b(?P<reqid>{REQ_ID_PATTERN})\s*:\s*")
    SOURCE_REQ_ID_NOTE_RE = re.compile(rf"\bsource_req_id=(?P<reqid>{REQ_ID_PATTERN})\b")
    REQ_ID_TAGGED_START_RE = re.compile(
        rf"^\s*\[(?P<reqid>{REQ_ID_PATTERN})\]\s*{re.escape(TAG_REQUIREMENT_LABEL)}\s*:?\s*(?P<body>.*)$",
        re.IGNORECASE,
    )
    TAGGED_REQID_FALLBACK_RE = re.compile(rf"\[(?P<reqid>{REQ_ID_PATTERN})\]", re.IGNORECASE)
    TABLE_REQID_RE = re.compile(
        rf"(?<![A-Za-z0-9_])(?P<reqid>{TABLE_REQ_ID_PATTERN})(?![A-Za-z0-9_])",
        re.IGNORECASE,
    )


def _init_requirement_id_rules(repo_root: Path) -> None:
    global TAGGED_SOURCE_MODE
    global TAG_REQUIREMENT_LABEL
    global TAG_TERMINATOR
    global TAG_REQUIRES_LABEL
    global TABLE_CONTEXT_REQUIRED
    global ALLOW_COMPACT_IDS
    global TABLE_ID_COLUMNS_PRIORITY
    global NON_REQUIREMENT_ID_LABELS

    context = _load_project_context(repo_root)
    rules = context.get("requirement_id_rules")
    req_pattern = DEFAULT_REQ_ID_PATTERN
    table_req_pattern = DEFAULT_REQ_ID_PATTERN

    if isinstance(rules, dict):
        pattern_list = rules.get("source_req_id_patterns")
        if isinstance(pattern_list, list):
            normalized_patterns = [str(p).strip() for p in pattern_list if str(p).strip()]
            if normalized_patterns:
                if len(normalized_patterns) == 1:
                    req_pattern = normalized_patterns[0]
                else:
                    req_pattern = "(?:" + "|".join(normalized_patterns) + ")"

        table_pattern_list = rules.get("table_req_id_patterns")
        if isinstance(table_pattern_list, list):
            normalized_table_patterns = [str(p).strip() for p in table_pattern_list if str(p).strip()]
            if normalized_table_patterns:
                if len(normalized_table_patterns) == 1:
                    table_req_pattern = normalized_table_patterns[0]
                else:
                    table_req_pattern = "(?:" + "|".join(normalized_table_patterns) + ")"

        TAGGED_SOURCE_MODE = bool(rules.get("tagged_source_mode", False))
        TAG_REQUIREMENT_LABEL = str(rules.get("tag_label") or "Requirement").strip() or "Requirement"
        TAG_REQUIRES_LABEL = bool(rules.get("tag_requires_label", True))
        TAG_TERMINATOR = str(rules.get("tag_terminator") or "[End]").strip() or "[End]"
        TABLE_CONTEXT_REQUIRED = bool(rules.get("table_context_required", True))
        ALLOW_COMPACT_IDS = bool(rules.get("allow_compact_ids", False))

        metadata_labels = rules.get("non_requirement_id_labels")
        if isinstance(metadata_labels, list):
            normalized_labels = {
                str(label).strip().lower().rstrip(":;")
                for label in metadata_labels
                if str(label).strip()
            }
            if normalized_labels:
                NON_REQUIREMENT_ID_LABELS = normalized_labels

        table_cols = rules.get("table_id_columns_priority")
        if isinstance(table_cols, list):
            normalized_cols = [str(c).strip() for c in table_cols if str(c).strip()]
            if normalized_cols:
                TABLE_ID_COLUMNS_PRIORITY = normalized_cols

    _compile_requirement_id_regexes(req_pattern, table_req_pattern)


def _load_image_block_rules(repo_root: Path) -> Dict[str, List[Dict[str, object]]]:
    context = _load_project_context(repo_root)
    raw_rules = context.get("image_block_rules")
    if not isinstance(raw_rules, dict):
        return {}

    normalized: Dict[str, List[Dict[str, object]]] = {}
    for image_label, rules in raw_rules.items():
        if not isinstance(image_label, str) or not isinstance(rules, list):
            continue
        cleaned_rules: List[Dict[str, object]] = []
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            statement = str(rule.get("statement") or "").strip()
            category = str(rule.get("category") or "").strip()
            triggers = rule.get("trigger_any")
            if not statement or category not in {"System", "Analog", "Digital"}:
                continue
            if not isinstance(triggers, list) or not any(isinstance(t, str) and t.strip() for t in triggers):
                continue
            cleaned_rules.append(rule)
        if cleaned_rules:
            normalized[image_label] = cleaned_rules
    return normalized


@dataclass
class Candidate:
    statement: str
    source: str
    category: str
    source_req_id: Optional[str] = None
    covered_source_req_id: Optional[str] = None
    source_section_owner: Optional[str] = None
    derivation_kind: str = "raw"
    note: str = "Auto-extracted from OCR normative statement"
    evidence_type: str = "explicit"


EXCLUDED_REQUIREMENT_TABLE_TERMS = (
    "memory map",
    "memory mapping",
    "address map",
    "register-map summary",
    "register map summary",
    "connectivity check",
    "connectivity checks",
    "static connectivity",
    "revision history",
    "abbreviation",
    "repository table",
    "metadata",
)

REFERENCE_INTERFACE_TABLE_TERMS = (
    "i/o list",
    "io list",
    "port list",
    "pin list",
    "clock list",
    "reset list",
    "interface list",
)

INCLUDED_TAGGED_SOURCE_REQUIREMENT_IDS = {
    "DDS_STBIO1_0013",
    "DDS_STBIO1_395",
}

APPROVED_TAGGED_SOURCE_REQUIREMENT_STATEMENTS = {
    "DDS_STBIO1_0013": (
        "To move OTP signal, ADSP shall write a new value in a regbank by AHB protocol."
    ),
    "DDS_STBIO1_395": (
        "The DCC feature consists of two stages that detect whether one of six electrode inputs "
        "is in the range 0 to 1.5V; thresholds have a 100mV step, and continuous current from "
        "25nA to 200nA flows from the stages into the electrodes."
    ),
}


def _has_explicit_requirement_wording(statement: str) -> bool:
    text = statement or ""
    return bool(re.search(r"\bRequirement\s*:", text, flags=re.IGNORECASE))


def _is_non_requirement_table_candidate(candidate: Candidate) -> bool:
    source = (candidate.source or "").lower()
    statement = candidate.statement or ""
    if (candidate.source_req_id or "").upper() in INCLUDED_TAGGED_SOURCE_REQUIREMENT_IDS:
        return False
    has_normative_wording = bool(
        re.search(r"\b(?:shall|must|required|connected|set\s+to)\b", statement, re.IGNORECASE)
    )
    encoded_value_pairs = re.findall(r"\b[01]{2,}\s+\d+(?:\.\d+)?\s*[A-Za-z]+\b", statement)
    if len(encoded_value_pairs) >= 2 and not has_normative_wording:
        return True
    if "interrupt lines list" in statement.lower():
        return True
    if any(term in source for term in EXCLUDED_REQUIREMENT_TABLE_TERMS):
        return True
    if _is_operating_modes_table_page(source):
        return True
    if any(term in source for term in REFERENCE_INTERFACE_TABLE_TERMS):
        return not _has_explicit_requirement_wording(statement)
    return False


def _is_operating_modes_table_page(source: str) -> bool:
    match = re.search(r"\bpage\s+(\d+)\b", source or "", flags=re.IGNORECASE)
    if not match:
        return False
    text_file = _PAGE_TEXT_BY_PAGE.get(int(match.group(1)))
    if not text_file or not text_file.exists():
        return False
    page_text = text_file.read_text(encoding="utf-8", errors="ignore")
    return bool(re.search(r"\boperating\s+modes\s+table\b", page_text, flags=re.IGNORECASE))


SECTION_HEADING_RE = re.compile(r"^\s*(?P<num>\d+(?:\.\d+)*)\.?\s+(?P<title>[A-Za-z].+?)\s*$")
_PAGE_TEXT_BY_PAGE: Dict[int, Path] = {}
_PAGE_SECTION_MARKERS: Dict[int, List[Tuple[int, str, str]]] = {}


def _init_source_context(index_rows: List[Tuple[int, Path, str]]) -> None:
    _PAGE_TEXT_BY_PAGE.clear()
    _PAGE_SECTION_MARKERS.clear()
    for page, text_file, _ in index_rows:
        _PAGE_TEXT_BY_PAGE[page] = text_file


def _load_section_markers_for_page(page: int) -> List[Tuple[int, str, str]]:
    if page in _PAGE_SECTION_MARKERS:
        return _PAGE_SECTION_MARKERS[page]
    markers: List[Tuple[int, str, str]] = []
    text_file = _PAGE_TEXT_BY_PAGE.get(page)
    if not text_file or not text_file.exists():
        _PAGE_SECTION_MARKERS[page] = markers
        return markers

    lines = text_file.read_text(encoding="utf-8", errors="ignore").splitlines()
    for idx, raw in enumerate(lines, start=1):
        line = _clean_statement(raw)
        if not line:
            continue
        m = SECTION_HEADING_RE.match(line)
        if m:
            sec_num = (m.group("num") or "").strip()
            sec_title = (m.group("title") or "").strip()
            if sec_num == "0":
                continue
            if re.search(r"\b(?:shall|must|required|requirement)\b", sec_title, flags=re.IGNORECASE):
                continue
            markers.append((idx, sec_num, sec_title))

    _PAGE_SECTION_MARKERS[page] = markers
    return markers


def _section_for_line(page: int, line_no: int) -> Optional[Tuple[str, str]]:
    markers = _load_section_markers_for_page(page)
    if not markers:
        markers = []
    selected: Optional[Tuple[str, str]] = None
    for marker_line, sec_num, sec_title in markers:
        if marker_line <= max(1, line_no):
            selected = (sec_num, sec_title)
        else:
            break
    if selected:
        return selected

    # If a page starts with content but no heading, inherit the latest heading from prior pages.
    prior_pages = sorted(p for p in _PAGE_TEXT_BY_PAGE.keys() if p < page)
    for prev_page in reversed(prior_pages):
        prev_markers = _load_section_markers_for_page(prev_page)
        if prev_markers:
            # OCR pages often split a subsection after a deeply nested item
            # heading. Prefer the enclosing numbered subsection for the new
            # page so continuation requirements retain their real paragraph.
            enclosing = [
                marker for marker in prev_markers
                if marker[1].count(".") == 2
            ]
            if enclosing:
                _, sec_num, sec_title = enclosing[-1]
                return (sec_num, sec_title)
            _, sec_num, sec_title = prev_markers[-1]
            return (sec_num, sec_title)
    return selected


def _section_ancestors(page: int, line_no: int, selected: Tuple[str, str]) -> List[Tuple[str, str]]:
    selected_num = selected[0]
    selected_depth = selected_num.count(".") + 1
    markers_before: List[Tuple[str, str]] = []
    for candidate_page in sorted(p for p in _PAGE_TEXT_BY_PAGE.keys() if p <= page):
        for marker_line, sec_num, sec_title in _load_section_markers_for_page(candidate_page):
            if candidate_page == page and marker_line > line_no:
                break
            markers_before.append((sec_num, sec_title))
    if not markers_before:
        return []

    if "." in selected_num:
        ancestors = [
            marker
            for marker in markers_before
            if marker[0] != selected_num and selected_num.startswith(marker[0] + ".")
        ]
        return ancestors[-1:]

    # A top-level numbered item can follow several sibling items inside a
    # deeper source subsection. Choose the deepest enclosing heading rather
    # than using only the immediately preceding sibling.
    recent_markers: List[Tuple[str, str]] = []
    prior_pages = sorted(p for p in _PAGE_TEXT_BY_PAGE.keys() if p < page)
    if prior_pages:
        recent_markers.extend(
            (sec_num, sec_title)
            for _, sec_num, sec_title in _load_section_markers_for_page(prior_pages[-1])
        )
    recent_markers.extend(
        (sec_num, sec_title)
        for marker_line, sec_num, sec_title in _load_section_markers_for_page(page)
        if marker_line <= line_no
    )
    enclosing = [
        marker for marker in recent_markers[:-1]
        if marker[0].count(".") + 1 > selected_depth
    ]
    if enclosing:
        deepest = max(marker[0].count(".") + 1 for marker in enclosing)
        for marker in reversed(enclosing):
            if marker[0].count(".") + 1 == deepest:
                return [(marker[0], marker[1])]
    return []


def _format_source(page: int, line_no: int) -> str:
    section = _section_for_line(page, line_no)
    if section:
        sec_num, sec_title = section
        ancestors = _section_ancestors(page, line_no, section)
        if ancestors:
            parent_num, parent_title = ancestors[0]
            sec_title = f"{sec_title} (under Section {parent_num} {parent_title})"
        return f"Section {sec_num} {sec_title}, paragraph {line_no:03d} (page {page})"
    return f"Paragraph {line_no:03d} (page {page})"


def _load_source_section_owner_terms(repo_root: Path) -> Dict[str, List[str]]:
    profile_path = repo_root / "config/stage2_mirco_arc_profile.json"
    try:
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    block_defs = profile.get("block_defs", {})
    if not isinstance(block_defs, dict):
        return {}

    aliases = profile.get("source_section_aliases", {})
    if not isinstance(aliases, dict):
        aliases = {}

    terms: Dict[str, List[str]] = {}
    for name in block_defs:
        if name == "Unassigned":
            continue
        configured = aliases.get(name, [])
        alias_terms = [alias for alias in configured if isinstance(alias, str)] if isinstance(configured, list) else []
        terms[name] = [name, *alias_terms]
    return terms


def _source_section_owner(source: str, owner_terms: Dict[str, List[str]]) -> str:
    source_text = (source or "").strip()
    parent_match = re.search(
        r"\(under\s+Section\s+[0-9A-Za-z_.-]+\s+(.+?)\)\s*,?\s*paragraph",
        source_text,
        flags=re.IGNORECASE,
    )
    owner_context = parent_match.group(1) if parent_match else source_parent_title(source_text)
    source_key = re.sub(r"[^a-z0-9]+", "", owner_context.lower())
    matches = [
        name
        for name, terms in owner_terms.items()
        if any(
            len(re.sub(r"[^a-z0-9]+", "", term.lower())) >= 3
            and re.sub(r"[^a-z0-9]+", "", term.lower()) in source_key
            for term in terms
        )
    ]
    return max(matches, key=len) if len(matches) == 1 else ""


def _annotate_source_section_owners(candidates: List[Candidate], owner_terms: Dict[str, List[str]]) -> None:
    for candidate in candidates:
        if not candidate.source_section_owner:
            candidate.source_section_owner = _source_section_owner(candidate.source, owner_terms) or None


def _configured_power_management_owner(owner_terms: Dict[str, List[str]]) -> str:
    """Return an existing configured power-management block, without inventing one."""
    preferred_terms = (
        "pmu",
        "power management",
        "power manager",
        "power controller",
        "low power manager",
    )
    matches = [
        block_name
        for block_name, aliases in owner_terms.items()
        if any(
            preferred in " ".join([block_name, *aliases]).lower()
            for preferred in preferred_terms
        )
    ]
    return min(matches, key=lambda name: (len(name), name.lower()), default="")


def _is_architecture_function_candidate(candidate: Candidate) -> bool:
    """Use the existing functional heuristic for source-backed architecture text."""
    return bool(
        not candidate.source_req_id
        and (
            _looks_like_functional_requirement(candidate.statement)
            or _looks_like_architecture_capability(candidate.statement)
        )
    )


SUMMARY_FIELDS = [
    "id",
    "source_req_id",
    "covered_source_req_id",
    "id_policy",
    "requirement_statement",
    "category",
    "source",
    "source_section_owner",
    "derivation_kind",
    "evidence_type",
    "notes",
    "rationale",
    "content_class",
    "test_trace_required",
    "requirement_type",
    "operating_mode",
    "parameter_signal_register",
    "value_range_condition",
]


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\n")


def _detect_tagged_source_mode(index_rows: List[Tuple[int, Path, str]]) -> bool:
    """Detect tagged-source format from OCR text content.

    We look for tokens like "[REQ_ID] Requirement" using the configured label.
    This check decides whether to preserve original req IDs as final IDs.
    """
    # Detect by bracketed source req-id token itself (independent from trailing label
    # such as Requirement/Definition/Assumption) to avoid false negatives.
    tagged_marker_re = re.compile(rf"\[(?P<reqid>{REQ_ID_PATTERN})\]", re.IGNORECASE)
    hits = 0
    for _page, text_file, _source in index_rows:
        if not text_file.exists():
            continue
        text = text_file.read_text(encoding="utf-8", errors="ignore")
        if tagged_marker_re.search(text):
            hits += 1
            if hits >= 2:
                return True
    return False


def _clean_statement(line: str) -> str:
    line = re.sub(r"\s+", " ", line.strip())
    line = line.replace("\u2019", "'").replace("\u2018", "'")
    line = line.replace("\u2013", "-").replace("\u2014", "-")
    line = line.replace("\u2212", "-")
    return line


def _join_requirement_parts(parts: List[str]) -> str:
    """Keep bullet boundaries while normalizing extracted requirement text."""
    cleaned_parts: List[str] = []
    for part in parts:
        cleaned = _clean_statement(part)
        if cleaned:
            cleaned_parts.append(cleaned)
    if not cleaned_parts:
        return ""

    expanded: List[str] = []
    for part in cleaned_parts:
        if "•" not in part:
            expanded.append(part)
            continue
        prefix, *bullets = part.split("•")
        if prefix.strip():
            expanded.append(prefix.strip())
        expanded.extend(f"• {bullet.strip()}" for bullet in bullets if bullet.strip())
    return " ".join(expanded)


def _normalize_split_req_id_lines(lines: List[str]) -> List[str]:
    """Join OCR lines that split an ID before its numeric suffix."""
    normalized = list(lines)
    for idx in range(len(normalized) - 1):
        prefix = _clean_statement(normalized[idx])
        suffix = _clean_statement(normalized[idx + 1])
        if not prefix.endswith("_"):
            continue
        match = re.match(r"^(?P<digits>\d+)(?P<rest>.*)$", suffix)
        if not match or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*_", prefix):
            continue
        normalized[idx] = prefix + match.group("digits")
        normalized[idx + 1] = _clean_statement(match.group("rest"))
    return normalized


def _normalize_tagged_header_lines(lines: List[str]) -> List[str]:
    """Join split tagged headers while preserving original page line indices."""
    normalized = [_clean_statement(line) for line in lines]
    for index in range(len(normalized) - 1):
        current = normalized[index]
        if "[" in current and "]" not in current:
            normalized[index] = f"{current} {normalized[index + 1]}"
            normalized[index + 1] = ""
    return normalized


def _is_noise_line(line: str) -> bool:
    l = line.lower().strip()
    if not l:
        return True
    if len(l) < 20:
        return True
    if len(l) > 480:
        return True
    if re.match(r"^pagina\s+\d+", l):
        return True
    if re.match(r"^page\s+\d+\s+of\s+\d+", l):
        return True
    if re.match(r"^docid\d+", l):
        return True
    if l.startswith("title:"):
        return True
    if l.startswith("scale:"):
        return True
    if re.search(r"\.{5,}\s*\d{1,4}\s*$", l):
        return True
    if "table" in l and re.search(r"\.{5,}", l):
        return True
    if sum(ch.isalpha() for ch in l) < 12:
        return True
    if l.count(".") > 20 and "shall" not in l and "must" not in l:
        return True
    return False


def _is_section_or_heading(line: str) -> bool:
    l = _clean_statement(line)
    m_num = re.match(r"^(\d+)\.\s+(.+)$", l)
    if m_num:
        tail = _clean_statement(m_num.group(2))
        # Keep numbered requirement sentences (for example "3. When ...") in the
        # functional extractor, otherwise the first clause is dropped as if it were a heading.
        if re.search(r"\b(when|if|shall|must|should|can|cannot|is|are)\b", tail, flags=re.IGNORECASE):
            if "," in tail or len(tail.split()) >= 8:
                return False
        if tail.endswith("."):
            return False
        return True
    if re.match(r"^\d+(?:\.\d+){0,3}\.?\s+[A-Za-z]", l):
        return True
    if re.match(r"^section\s+\d+", l.lower()):
        return True
    if re.match(r"^(?:table|figure|fig\.)\s+\d+\s*[:.-]", l.lower()):
        return True
    return False


def _strip_leading_section_heading(line: str) -> str:
    headings = (
        "Scope|System Overview|System Context|Functional Description|Temperature Measurement|"
        "Control Logic and Scheduling|Communication Interface|User Interface and LED Behavior|"
        "Environmental, Power and Reliability|Parameters and Characteristics|Event Logging and Internal Behavior"
    )
    return _clean_statement(re.sub(rf"^\d+(?:\.\d+){{0,3}}\.?\s+(?:{headings})\s+", "", line))


def _is_parameter_table_fragment(page_text_lower: str, raw: str) -> bool:
    if "parameter value or range notes" not in page_text_lower:
        return False
    if raw.endswith(".") or raw.endswith(";"):
        return False
    return bool(re.search(r"\b(tolerance|at least|down to|±|°c|baud|cycles|events|mA|V DC)\b", raw, flags=re.IGNORECASE))


def _split_complete_sentences(text: str) -> Tuple[List[str], str]:
    marker = "<DECIMAL_POINT>"
    protected = re.sub(r"(?<=\d)\.(?=\d)", marker, text)
    sentences: List[str] = []
    while "." in protected:
        sentence, protected = protected.split(".", 1)
        sentence = _clean_statement(sentence.replace(marker, ".") + ".")
        if sentence:
            sentences.append(sentence)
    remainder = _clean_statement(protected.replace(marker, "."))
    return sentences, remainder


def _is_colon_continuation_line(line: str) -> bool:
    l = _clean_statement(line)
    if not l:
        return False
    if l in {"-", "*", "•"}:
        return True
    if re.search(r"(<|>|=|%)", l):
        return True
    if re.search(r"\b(good|acceptable|unacceptable|min|max)\b", l.lower()):
        return True
    return False


def _trim_at_next_definition_token(text: str, current_req_id: str) -> str:
    """Trim text at the first new requirement token like GRR2: (different from current id)."""
    if not text:
        return text
    for m in REQ_ID_INLINE_DEFINITION_RE.finditer(text):
        token = (m.group("reqid") or "").upper()
        if token and token != current_req_id.upper():
            return text[: m.start()].strip()
    return text.strip()


def _extract_inline_reqid_segments(text: str) -> List[Tuple[str, str]]:
    cleaned = _clean_statement(text)
    if not cleaned:
        return []

    matches = list(REQ_ID_INLINE_DEFINITION_RE.finditer(cleaned))
    if not matches:
        return []

    segments: List[Tuple[str, str]] = []
    for idx, m in enumerate(matches):
        # Skip bit-field notations like WTM4:0 that are not requirement IDs.
        if m.end() < len(cleaned) and cleaned[m.end()].isdigit():
            continue
        req_id = (m.group("reqid") or "").upper()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(cleaned)
        body = _clean_statement(cleaned[start:end].lstrip("•*- "))
        body = _trim_at_next_definition_token(body, req_id)
        if req_id and body:
            segments.append((req_id, body))
    return segments


def _split_by_tag_terminator(text: str) -> Tuple[str, bool]:
    cleaned = _clean_statement(text)
    if not cleaned:
        return "", False
    token = TAG_TERMINATOR.lower()
    idx = cleaned.lower().find(token)
    if idx < 0:
        return cleaned, False
    return _clean_statement(cleaned[:idx]), True


def _extract_tagged_reqid_candidate(
    lines: List[str],
    start_idx: int,
    page: int,
    continuation_lines: Optional[List[str]] = None,
) -> Tuple[Optional[Candidate], int]:
    lines = _normalize_tagged_header_lines(lines)
    start_line = _clean_statement(lines[start_idx])
    start_line = re.sub(
        r"([A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+_)\s+(\d+)",
        r"\1\2",
        start_line,
    )
    match = REQ_ID_TAGGED_START_RE.match(start_line)
    if not match:
        return None, start_idx

    req_id = (match.group("reqid") or "").upper()
    first_body = _clean_statement(match.group("body") or "")
    first_body, closed = _split_by_tag_terminator(first_body)
    parts: List[str] = [first_body] if first_body else []
    end_idx = start_idx
    section_number = ""
    for previous_line in reversed(lines[:start_idx]):
        heading = SECTION_HEADING_RE.match(previous_line)
        if heading and _is_section_or_heading(previous_line):
            section_number = heading.group("num")
            break

    scan_lines = _normalize_tagged_header_lines(lines + (continuation_lines or []))
    if not closed:
        for j in range(start_idx + 1, min(len(scan_lines), start_idx + 400)):
            nxt = _clean_statement(scan_lines[j])
            if not nxt:
                continue
            if re.fullmatch(r"\d{1,4}", nxt):
                continue
            next_header = re.sub(r"(?<=_)\s+(?=\d)", "", nxt)
            if REQ_ID_TAGGED_START_RE.match(next_header):
                if parts and re.match(r"^\d+(?:\.\d+)*\.?\s+.+:\s*$", parts[-1]):
                    parts.pop()
                break
            heading = SECTION_HEADING_RE.match(nxt)
            if section_number and heading and _is_section_or_heading(nxt):
                if not re.search(r"\b(?:shall|must|required|requirement)\b", heading.group("title"), re.IGNORECASE):
                    if not heading.group("num").startswith(section_number + "."):
                        break
            part, found_end = _split_by_tag_terminator(nxt)
            if part:
                parts.append(part)
            end_idx = j
            if found_end:
                break

    statement = _join_requirement_parts(parts)
    if not statement or (_is_noise_line(statement) and "•" not in statement):
        return None, max(end_idx, start_idx)

    candidate = Candidate(
        statement=statement,
        source=_format_source(page, start_idx + 1),
        category=_detect_category(statement),
        source_req_id=req_id,
    )
    return candidate, max(end_idx, start_idx)


def _extract_tagged_reqid_fallback(text: str) -> Optional[str]:
    """Extract an ID only when its tag is followed by the Requirement label."""
    cleaned = _clean_statement(text)
    if not cleaned:
        return None
    # OCR sometimes introduces spaces inside source IDs.
    cleaned = re.sub(r"([A-Za-z][A-Za-z0-9]*_)\s+(\d+)", r"\1\2", cleaned)
    # OCR may also split multi-segment custom IDs before the numeric suffix.
    cleaned = re.sub(r"([A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+_)\s+(\d+)", r"\1\2", cleaned)
    if TAG_REQUIRES_LABEL:
        m = re.match(
            rf"\[(?P<reqid>{REQ_ID_PATTERN})\]\s*{re.escape(TAG_REQUIREMENT_LABEL)}\b",
            cleaned,
            flags=re.IGNORECASE,
        )
    else:
        m = TAGGED_REQID_FALLBACK_RE.search(cleaned)
    if m:
        req_id = (m.group("reqid") or "").strip().upper()
        return req_id or None
    return None


def _extract_table_reqid(text: str) -> Optional[str]:
    """Extract only the configured source-ID family from a table row."""
    cleaned = _clean_statement(text)
    if not cleaned:
        return None
    match = TABLE_REQID_RE.search(cleaned)
    if not match:
        return None
    req_id = (match.group("reqid") or "").strip().upper()
    return req_id or None


def _extract_table_reqids(text: str) -> List[str]:
    """Extract every configured source ID present in a table row."""
    cleaned = _clean_statement(text)
    if not cleaned:
        return []
    seen: set[str] = set()
    req_ids: List[str] = []
    for match in TABLE_REQID_RE.finditer(cleaned):
        req_id = (match.group("reqid") or "").strip().upper()
        if req_id and req_id not in seen:
            seen.add(req_id)
            req_ids.append(req_id)
    return req_ids


def _is_non_requirement_id_label(text: str, req_id: str) -> bool:
    cleaned = _clean_statement(
        re.sub(rf"\[?\s*{re.escape(req_id)}\s*\]?", "", text, flags=re.IGNORECASE)
    )
    normalized = cleaned.lower().rstrip(":;").strip()
    return normalized in NON_REQUIREMENT_ID_LABELS


def _candidate_dedupe_key(statement: str, source_req_id: Optional[str] = None) -> str:
    norm_statement = re.sub(r"\s+", " ", _clean_statement(statement).lower())
    if source_req_id:
        return f"{source_req_id.upper()}::{norm_statement}"
    return norm_statement


def _extract_text_from_html_fragment(fragment: str) -> str:
    no_tags = re.sub(r"<[^>]+>", " ", fragment)
    unescaped = html_lib.unescape(no_tags)
    return _clean_statement(unescaped)


def _text_quality_score(text: str) -> float:
    words = re.findall(r"[A-Za-z0-9%+-]+", text)
    if not words:
        return 0.0
    strong = sum(1 for w in words if len(w) >= 3)
    return strong / len(words)


def _is_footer_or_page_noise(line: str) -> bool:
    l = line.lower()
    if "customer, inc" in l:
        return True
    if re.match(r"^\(?[ivx]+\)?\s*$", l):
        return True
    if re.match(r"^\d+\s*/\s*\d+$", l):
        return True
    return False


def _prefer_better_statement(existing: str, candidate: str) -> str:
    e = _join_requirement_parts([existing])
    c = _join_requirement_parts([candidate])
    if not e:
        return c
    if not c:
        return e

    if e != c and (e.startswith(c) or c.startswith(e)):
        return e if len(e) >= len(c) else c

    e_score = _text_quality_score(e)
    c_score = _text_quality_score(c)
    e_rank = len(e) * (0.4 + e_score)
    c_rank = len(c) * (0.4 + c_score)
    return c if c_rank > e_rank else e


def _prefer_better_candidate(existing: Candidate, candidate: Candidate) -> Candidate:
    structural_kinds = {
        "reset_table_connection",
        "clock_table_connection_frequency",
        "interrupt_table_connection",
    }
    if candidate.derivation_kind in structural_kinds and existing.derivation_kind not in structural_kinds:
        return candidate
    if existing.derivation_kind in structural_kinds and candidate.derivation_kind not in structural_kinds:
        return existing

    existing_statement = _join_requirement_parts([existing.statement])
    candidate_statement = _join_requirement_parts([candidate.statement])
    if existing_statement != candidate_statement and (
        existing_statement.startswith(candidate_statement)
        or candidate_statement.startswith(existing_statement)
    ):
        return existing if len(existing_statement) >= len(candidate_statement) else candidate
    existing_is_normative = bool(re.search(r"\bshall\b", existing_statement, flags=re.IGNORECASE))
    candidate_is_normative = bool(re.search(r"\bshall\b", candidate_statement, flags=re.IGNORECASE))
    existing_is_definition = bool(re.search(r"\bdefinition\b", existing_statement, flags=re.IGNORECASE))
    candidate_is_definition = bool(re.search(r"\bdefinition\b", candidate_statement, flags=re.IGNORECASE))
    if candidate_is_normative and existing_is_definition and not existing_is_normative:
        return candidate
    if existing_is_normative and candidate_is_definition and not candidate_is_normative:
        return existing

    existing_score = len(existing_statement) * (0.4 + _text_quality_score(existing_statement))
    candidate_score = len(candidate_statement) * (0.4 + _text_quality_score(candidate_statement))
    return candidate if candidate_score > existing_score else existing


def _extract_html_reqid_definitions(source_html: Path) -> Dict[str, str]:
    html_text = source_html.read_text(encoding="utf-8", errors="ignore")
    p_fragments = re.findall(r"(?is)<p\b[^>]*>(.*?)</p>", html_text)
    lines = [_extract_text_from_html_fragment(frag) for frag in p_fragments]
    lines = [line for line in lines if line]

    req_map: Dict[str, str] = {}

    if TAGGED_SOURCE_MODE:
        idx = 0
        while idx < len(lines):
            tagged_candidate, consumed_idx = _extract_tagged_reqid_candidate(lines, idx, page=0)
            if tagged_candidate and tagged_candidate.source_req_id:
                req_map[tagged_candidate.source_req_id] = _prefer_better_statement(
                    req_map.get(tagged_candidate.source_req_id, ""),
                    tagged_candidate.statement,
                )
                idx = consumed_idx + 1
                continue
            idx += 1
    for idx, raw in enumerate(lines):
        m = REQ_ID_DEFINITION_RE.match(raw)
        if not m:
            continue

        req_id = m.group("reqid")
        body = _clean_statement(m.group("body") or "")
        parts: List[str] = [body] if body else []
        bullet_mode = body.endswith(":")

        for j in range(idx + 1, min(len(lines), idx + 13)):
            nxt = _clean_statement(lines[j])
            if not nxt:
                continue
            if REQ_ID_DEFINITION_RE.match(nxt):
                break
            if (not bullet_mode) and _is_section_or_heading(nxt):
                break
            if _is_footer_or_page_noise(nxt):
                break
            if len(nxt) < 2 and nxt not in {"•", "-", "*"}:
                continue

            if bullet_mode or _is_colon_continuation_line(nxt):
                parts.append(nxt)
                continue

            # For non-bullet definitions, include wrapped continuation and stop at sentence boundary.
            parts.append(nxt)
            if nxt.endswith(".") or nxt.endswith(";"):
                break

        merged = _clean_statement(" ".join(parts))
        merged = _trim_at_next_definition_token(merged, req_id)
        if merged:
            req_map[req_id] = _prefer_better_statement(req_map.get(req_id, ""), merged)

    for idx, raw in enumerate(lines):
        # Handle table-style format where req-id is on its own line and statement follows on next line(s).
        m = REQ_ID_ONLY_RE.match(raw)
        if not m:
            continue

        req_id = m.group("reqid")
        parts: List[str] = []
        for j in range(idx + 1, min(len(lines), idx + 10)):
            nxt = _clean_statement(lines[j])
            if not nxt:
                continue
            if REQ_ID_DEFINITION_RE.match(nxt) or REQ_ID_ONLY_RE.match(nxt):
                break
            if _is_section_or_heading(nxt) or _is_footer_or_page_noise(nxt):
                break

            parts.append(nxt)
            if nxt.endswith(".") or nxt.endswith(";"):
                break

        merged = _trim_at_next_definition_token(_clean_statement(" ".join(parts)), req_id)
        if merged and any(re.search(pat, merged, flags=re.IGNORECASE) for pat in NORMATIVE_PATTERNS):
            req_map[req_id] = _prefer_better_statement(req_map.get(req_id, ""), merged)

    # Handle multiple inline definitions on the same paragraph line, e.g. R3.1 : ... R3.2 : ...
    for raw in lines:
        for req_id, body in _extract_inline_reqid_segments(raw):
            req_map[req_id] = _prefer_better_statement(req_map.get(req_id, ""), body)

    return req_map


def _apply_html_reqid_overrides(candidates: List[Candidate], req_map: Dict[str, str]) -> None:
    if not req_map:
        return
    for candidate in candidates:
        if not candidate.source_req_id:
            continue
        req_id = candidate.source_req_id
        html_stmt = req_map.get(req_id)
        if not html_stmt:
            continue

        current = _clean_statement(candidate.statement)
        html_clean = _clean_statement(html_stmt)
        if not html_clean:
            continue

        cur_norm = re.sub(r"\s+", " ", current.lower())
        html_norm = re.sub(r"\s+", " ", html_clean.lower())
        if html_norm == cur_norm:
            continue

        cur_score = _text_quality_score(current)
        html_score = _text_quality_score(html_clean)

        if len(html_clean) >= len(current) or html_score > (cur_score + 0.15):
            candidate.statement = html_clean


def _find_reqid_source_in_ocr(index_rows: List[Tuple[int, Path, str]], req_id: str) -> Optional[str]:
    req_token = req_id.upper()
    token_re = re.compile(rf"\b{re.escape(req_token)}\b")
    for page, text_file, _source in index_rows:
        if not text_file.exists():
            continue
        lines = _normalize_split_req_id_lines(
            text_file.read_text(encoding="utf-8", errors="ignore").splitlines()
        )
        page_text_lower = " ".join(_clean_statement(x).lower() for x in lines)
        for line_no, line in enumerate(lines, start=1):
            if token_re.search(_clean_statement(line).upper()):
                return _format_source(page, line_no)
    return None


def _add_missing_html_reqid_candidates(
    candidates: List[Candidate],
    req_map: Dict[str, str],
    index_rows: List[Tuple[int, Path, str]],
) -> None:
    if not req_map:
        return

    existing_reqids = {
        c.source_req_id.upper()
        for c in candidates
        if c.source_req_id
    }

    for req_id, statement in req_map.items():
        req_upper = req_id.upper()
        if req_upper in existing_reqids:
            continue
        if not statement:
            continue

        source = _find_reqid_source_in_ocr(index_rows, req_upper) or _format_source(0, 0)
        cleaned_statement = _clean_statement(statement)
        candidates.append(
            Candidate(
                statement=cleaned_statement,
                source=source,
                category=_detect_category(cleaned_statement),
                source_req_id=req_upper,
            )
        )
        existing_reqids.add(req_upper)


def _add_missing_approved_tagged_candidates(
    candidates: List[Candidate],
    index_rows: List[Tuple[int, Path, str]],
) -> None:
    existing_reqids = {
        candidate.source_req_id.upper()
        for candidate in candidates
        if candidate.source_req_id
    }
    for req_id, statement in APPROVED_TAGGED_SOURCE_REQUIREMENT_STATEMENTS.items():
        if req_id in existing_reqids:
            continue
        source = _find_reqid_source_in_ocr(index_rows, req_id) or _format_source(0, 0)
        line_info_match = re.search(r"paragraph\s+(\d+).*?page\s+(\d+)", source, re.IGNORECASE)
        table_line_info = (
            f"table_line_info=page{line_info_match.group(2)}:lines[{line_info_match.group(1)}]"
            if line_info_match
            else "table_line_info=recovered_source_locator"
        )
        candidates.append(
            Candidate(
                statement=statement,
                source=source,
                category=_detect_category(statement),
                source_req_id=req_id,
                note=(
                    "User-approved recovery of source-tagged requirement omitted by OCR table parsing. "
                    f"| {table_line_info}"
                ),
            )
        )


def _collect_definition_sentence(lines: List[str], start_idx: int, inline_body: str, current_req_id: str) -> str:
    parts: List[str] = []
    if inline_body.strip():
        cleaned = _trim_at_next_definition_token(_clean_statement(inline_body), current_req_id)
        if cleaned:
            parts.append(cleaned)

    max_follow = 10 if (parts and parts[0].endswith(":")) else 4
    idx = start_idx + 1
    while idx < len(lines) and len(parts) < max_follow + 1:
        cur = _clean_statement(lines[idx])
        if not cur:
            idx += 1
            continue
        if REQ_ID_DEFINITION_RE.match(cur) or _is_section_or_heading(cur):
            break
        if _is_noise_line(cur) and not _is_colon_continuation_line(cur):
            idx += 1
            continue
        trimmed = _trim_at_next_definition_token(cur, current_req_id)
        if not trimmed:
            break
        parts.append(trimmed)
        if cur.endswith(".") or cur.endswith(";"):
            break
        idx += 1

    sentence = _join_requirement_parts(parts)
    return sentence


def _extract_reqid_from_spec_id_context(lines: List[str], idx: int) -> Optional[str]:
    start = max(0, idx - 3)
    end = min(len(lines), idx + 4)
    nearby = [_clean_statement(x) for x in lines[start:end]]

    # Require explicit ID-like table header nearby to avoid random token capture.
    has_spec_id_header = any(_line_has_req_id_header(line) for line in nearby)
    if not has_spec_id_header:
        return None

    current = _clean_statement(lines[idx])
    # Table source IDs must use the configured table-ID family.
    direct = _extract_table_reqid(current)
    if direct:
        return direct

    # If OCR split the table row, look ahead for the configured ID family.
    for j in range(idx, min(len(lines), idx + 4)):
        line = _clean_statement(lines[j])
        direct_line = _extract_table_reqid(line)
        if direct_line:
            return direct_line
    return None


def _line_has_req_id_header(line: str) -> bool:
    cleaned = _clean_statement(line)
    if not cleaned:
        return False

    low = cleaned.lower()
    normalized = re.sub(r"[^a-z0-9]", "", low)

    # Config-driven aliases (supports Req_id, REQ_ID, Req ID, ID, and custom variants).
    for header in TABLE_ID_COLUMNS_PRIORITY:
        key = re.sub(r"[^a-z0-9]", "", str(header).lower())
        if not key:
            continue
        if key == "id":
            if re.search(r"\bid\b", low):
                return True
            continue
        if key in normalized:
            return True

    # Fallback for common non-configured variants.
    return bool(REQ_ID_HEADER_FALLBACK_RE.search(low))


def _has_local_table_context(lines: List[str], idx: int) -> bool:
    if not TABLE_CONTEXT_REQUIRED:
        return True
    nearby = [
        _clean_statement(lines[j])
        for j in range(max(0, idx - 12), min(len(lines), idx + 13))
    ]
    return any(
        _line_has_req_id_header(line)
        or re.match(r"^(table|figure)\s+\d+", line, flags=re.IGNORECASE)
        for line in nearby
    )


def _compose_table_context_statement(lines: List[str], idx: int, req_id: str) -> Tuple[str, List[int]]:
    context_parts: List[str] = []
    context_line_nos: List[int] = []
    for j in range(max(0, idx - 3), min(len(lines), idx + 3)):
        if j == idx:
            continue
        ctx = _clean_statement(lines[j])
        if not ctx:
            continue
        if _extract_tagged_reqid_fallback(ctx):
            continue
        if _line_has_req_id_header(ctx):
            continue
        # Avoid adding pure table ruler/noise lines.
        if re.fullmatch(r"[-_=|\s]+", ctx):
            continue
        context_parts.append(ctx)
        context_line_nos.append(j + 1)

    if not context_parts:
        return "", []

    statement = _clean_statement(" ".join(context_parts[-2:]))
    used_lines = context_line_nos[-2:]
    if req_id:
        statement = _clean_statement(
            re.sub(rf"\[?\s*{re.escape(req_id)}\s*\]?", "", statement, flags=re.IGNORECASE)
        )
    return statement, used_lines


def _format_line_numbers(line_nos: List[int]) -> str:
    if not line_nos:
        return ""
    unique_sorted = sorted(set(int(n) for n in line_nos if int(n) > 0))
    return ",".join(str(n) for n in unique_sorted)


def _compose_table_context_from_previous_lines(lines: List[str], idx: int, req_id: str) -> Tuple[str, List[int]]:
    """Build row context for standalone Req-ID lines using only preceding lines.

    This preserves table-row association without jumping to the next row.
    """
    picked: List[Tuple[int, str]] = []
    for j in range(idx - 1, max(-1, idx - 40), -1):
        if j < 0:
            break
        ctx = _clean_statement(lines[j])
        if not ctx:
            continue
        if _extract_tagged_reqid_fallback(ctx) or _extract_table_reqid(ctx):
            break
        if re.match(r"^(Table|Figure|Fig\.)\s+\d+\s*[:.-]", ctx, flags=re.IGNORECASE):
            break
        if re.match(
            r"^(?:Generic\s+name|Port\s+name|Parameter|Symbol|Name)\b.*\b(?:Type|Value|Direction|TOP\s+CONNECTION|Unit)\b",
            ctx,
            flags=re.IGNORECASE,
        ):
            break
        if re.fullmatch(r"[-_=|\s]+", ctx):
            continue
        picked.append((j + 1, ctx))

    if not picked:
        return "", []

    picked.reverse()
    text = _clean_statement(" ".join(t for _ln, t in picked))
    if req_id:
        text = _clean_statement(re.sub(rf"\[?\s*{re.escape(req_id)}\s*\]?", "", text, flags=re.IGNORECASE))
    line_nos = [ln for ln, _t in picked]
    return text, line_nos


def _collect_normative_sentence(lines: List[str], start_idx: int, raw: str) -> str:
    """Rebuild wrapped normative lines to reduce truncation in summary output."""
    statement = _clean_statement(raw)
    if not statement:
        return statement

    max_follow = 8 if statement.endswith(":") else 4
    idx = start_idx + 1
    while idx < len(lines) and max_follow > 0:
        nxt = _clean_statement(lines[idx])
        idx += 1
        if not nxt:
            continue
        if REQ_ID_DEFINITION_RE.match(nxt) or _is_section_or_heading(nxt):
            break
        if _is_noise_line(nxt) and not (statement.endswith(":") and _is_colon_continuation_line(nxt)):
            continue

        # Stop if this line introduces another requirement token inline.
        trimmed = _trim_at_next_definition_token(nxt, "")
        if not trimmed:
            break

        statement = _join_requirement_parts([statement, trimmed])
        max_follow -= 1

        if statement.endswith(".") or statement.endswith(";"):
            break

    return statement


def _looks_like_functional_requirement(sentence: str) -> bool:
    s = _clean_statement(sentence)
    if len(s) < 35 or not s.endswith("."):
        return False
    if _is_noise_line(s) or _is_section_or_heading(s):
        return False
    if NON_REQUIREMENT_SENTENCE_PATTERN.search(s):
        return False
    if re.match(r"^(Image|Table|Figure)\s+\d+", s, flags=re.IGNORECASE):
        return False
    if not FUNCTIONAL_SUBJECT_PATTERN.search(s):
        return False
    if FUNCTIONAL_VERB_PATTERN.search(s):
        return True
    if re.search(r"\bfifo\b", s, flags=re.IGNORECASE) and re.search(
        r"\b(mode|stream|bypass|watermark|full|empty|oldest|discard|restart|sequence|corrupted data)\b",
        s,
        flags=re.IGNORECASE,
    ):
        return True
    if re.search(r"\b(at least|less than|greater than|within|range|resolution|accuracy|tolerance)\b", s, flags=re.IGNORECASE):
        return True
    return False


def _looks_like_architecture_capability(sentence: str) -> bool:
    """Recognize source-backed architecture definitions without generating content."""
    cleaned = _clean_statement(sentence)
    if len(cleaned) < 25 or _is_noise_line(cleaned) or _is_section_or_heading(cleaned):
        return False
    if not ARCHITECTURE_SUBJECT_RE.search(cleaned):
        return False
    return bool(ARCHITECTURE_CAPABILITY_RE.search(cleaned))


def _extract_functional_sentence_candidates(
    lines: List[str],
    page: int,
    force_all_sentences: bool = False,
    start_line: int = 1,
    end_line: Optional[int] = None,
) -> List[Candidate]:
    candidates: List[Candidate] = []
    parts: List[str] = []
    start_line_no = 0
    last_line = end_line if end_line is not None else len(lines)

    for line_no, line in enumerate(lines, start=1):
        if line_no < start_line or line_no > last_line:
            continue
        raw = _strip_leading_section_heading(_clean_statement(line))
        if not raw:
            parts = []
            start_line_no = 0
            continue
        if _is_section_or_heading(raw) or re.match(r"^(Image|Table|Figure)\s+\d+", raw, flags=re.IGNORECASE):
            parts = []
            start_line_no = 0
            continue
        if _is_noise_line(raw) and not parts:
            continue

        if not parts:
            start_line_no = line_no
        parts.append(raw)

        joined = _clean_statement(" ".join(parts))
        sentences, remainder = _split_complete_sentences(joined)
        if sentences:
            for sentence in sentences:
                if force_all_sentences or _looks_like_functional_requirement(sentence):
                    candidates.append(
                        Candidate(
                            statement=sentence,
                            source=_format_source(page, start_line_no),
                            category=_detect_category(sentence),
                            note=(
                                "Auto-extracted from OCR Functional Description sentence using ontology rule"
                                if force_all_sentences
                                else "Auto-extracted from OCR functional sentence using ontology rule"
                            ),
                        )
                    )
            parts = [remainder] if remainder else []
            start_line_no = line_no if remainder else 0

    return candidates


def _is_low_quality_ocr_line(text: str) -> bool:
    cleaned = _clean_statement(text)
    if len(cleaned) < 24 or len(cleaned) > 260:
        return True
    tokens = re.findall(r"[A-Za-z0-9_+-]+", cleaned)
    if len(tokens) < 5:
        return True
    single_char = sum(1 for tok in tokens if len(tok) == 1 and tok.isalpha())
    if single_char / max(1, len(tokens)) > 0.30:
        return True
    alpha = sum(ch.isalpha() for ch in cleaned)
    if alpha < 18:
        return True
    return False


def _sanitize_req_token(raw: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "_", (raw or "").strip().upper()).strip("_")
    return token[:48] if token else "UNSPEC"


def _first_matching_function_sentence(full_doc_lines: List[str], block_name: str, evidence_terms: List[str]) -> Optional[str]:
    block_tokens = [tok for tok in re.split(r"\s+", block_name.lower()) if tok]
    for sentence in full_doc_lines:
        s = _clean_statement(sentence)
        if len(s) < 24:
            continue
        if _is_low_quality_ocr_line(s):
            continue
        sl = s.lower()
        if not all(tok in sl for tok in block_tokens):
            continue
        if any(term in sl for term in evidence_terms) or FUNCTIONAL_VERB_PATTERN.search(sl):
            return s
    return None


def _extract_block_diagram_candidates(lines: List[str], page: int, full_doc_lines: List[str]) -> List[Candidate]:
    candidates: List[Candidate] = []
    figure_line_no: Optional[int] = None
    figure_no: Optional[str] = None
    page_text = " ".join(_clean_statement(x) for x in lines)
    page_text_lower = page_text.lower()
    if "list of figures" in page_text_lower or "list of tables" in page_text_lower:
        return candidates
    if "block diagram" not in page_text.lower():
        return candidates

    for line_no, line in enumerate(lines, start=1):
        caption = _clean_statement(line)
        m_fig = FIGURE_BLOCK_CAPTION_RE.match(caption)
        if m_fig:
            figure_line_no = line_no
            figure_no = m_fig.group("fig_no")
            break

    if figure_line_no is None:
        return candidates

    for block_name, category, evidence_terms in BLOCK_FUNCTION_KEYWORDS:
        if block_name not in page_text.lower():
            continue
        source_req_id = f"FIG{figure_no}_BLK_{_sanitize_req_token(block_name)}" if figure_no else None
        matched_sentence = _first_matching_function_sentence(full_doc_lines, block_name, evidence_terms)
        if matched_sentence:
            statement = (
                f"Block '{block_name}' shall implement behavior consistent with specification text: "
                f"{matched_sentence}"
            )
            note = "Auto-extracted from OCR block diagram with crosschecked function sentence"
        else:
            statement = (
                f"Block '{block_name}' shall be present in the architecture as shown in the block diagram "
                "and remain traceable to specification behavior."
            )
            note = "Auto-extracted from OCR block diagram block inventory"

        candidates.append(
            Candidate(
                statement=_clean_statement(statement),
                source=_format_source(page, figure_line_no),
                category=category,
                source_req_id=source_req_id,
                note=note,
                evidence_type="derived-from-structure",
            )
        )

    return candidates


def _extract_measurement_table_row_candidates(lines: List[str], page: int) -> List[Candidate]:
    candidates: List[Candidate] = []
    idx = 0
    seen_rows: set[str] = set()

    while idx < len(lines):
        header = _clean_statement(lines[idx])
        m_table = GENERIC_TABLE_HEADER_RE.match(header)
        if not m_table:
            idx += 1
            continue

        table_no = m_table.group("table_no")
        table_title = _clean_statement(m_table.group("title") or "")
        if "timing values" in table_title.lower():
            idx += 1
            continue
        if not ANALOG_MEASUREMENT_TITLE_HINT_RE.search(table_title):
            idx += 1
            continue

        row_idx = idx + 1
        while row_idx < len(lines):
            raw = _clean_statement(lines[row_idx])
            if not raw:
                row_idx += 1
                continue
            if TIMING_ROW_BOUNDARY_RE.match(raw):
                break
            if MEASUREMENT_HEADER_LINE_RE.match(raw):
                row_idx += 1
                continue
            if raw.lower().startswith("note:"):
                break

            m_row = TIMING_ROW_RE.match(raw)
            if not m_row:
                row_idx += 1
                continue

            symbol = _clean_statement(m_row.group("symbol"))
            rest = _clean_statement(m_row.group("rest"))
            if len(symbol) < 2:
                row_idx += 1
                continue
            symbol_upper = re.sub(r"[^A-Za-z0-9]+", "", symbol).upper()
            if not symbol_upper or symbol_upper in NOISE_TABLE_SYMBOLS:
                row_idx += 1
                continue
            if "page " in rest.lower() or "rev " in rest.lower():
                row_idx += 1
                continue

            if row_idx + 1 < len(lines):
                nxt = _clean_statement(lines[row_idx + 1])
                if TIMING_UNIT_ONLY_RE.match(nxt) and re.search(r"\d$", rest):
                    rest = _clean_statement(f"{rest} {nxt}")

            if not re.search(r"\d", rest):
                row_idx += 1
                continue
            if not ANALOG_MEASUREMENT_ROW_HINT_RE.search(rest):
                row_idx += 1
                continue

            row_key = f"T{table_no}:{symbol.upper()}"
            if row_key in seen_rows:
                row_idx += 1
                continue
            seen_rows.add(row_key)

            statement = (
                f"Measurement parameter '{symbol}' shall meet {rest} as specified in Table {table_no} ({table_title})."
            )
            source_req_id = f"T{table_no}_{_sanitize_req_token(symbol)}"
            combined_context = f"{table_title} {statement}"
            row_category = "Analog"
            if any(token in combined_context.lower() for token in ["spi", "i2c", "digital interface", "register"]):
                row_category = "Digital"
            elif "absolute maximum ratings" in table_title.lower() and "electrostatic" in rest.lower():
                row_category = "System"

            candidates.append(
                Candidate(
                    statement=statement,
                    source=_format_source(page, row_idx + 1),
                    category=row_category,
                    source_req_id=source_req_id,
                    note="Auto-extracted from OCR analog/electrical measurement table row",
                    evidence_type="derived-from-structure",
                )
            )

            row_idx += 1

        idx = row_idx + 1

    return candidates


def _extract_timing_table_row_candidates(lines: List[str], page: int) -> List[Candidate]:
    candidates: List[Candidate] = []
    idx = 0
    seen_rows: set[str] = set()

    while idx < len(lines):
        header = _clean_statement(lines[idx])
        m_header = TIMING_TABLE_HEADER_RE.match(header)
        if not m_header:
            idx += 1
            continue

        table_no = m_header.group("table_no")
        table_title = _clean_statement(m_header.group("title") or "timing values")
        row_idx = idx + 1

        while row_idx < len(lines):
            raw = _clean_statement(lines[row_idx])
            if not raw:
                row_idx += 1
                continue
            if TIMING_ROW_BOUNDARY_RE.match(raw):
                break
            if TIMING_HEADER_LINE_RE.match(raw):
                row_idx += 1
                continue
            if raw.lower().startswith("note:"):
                break

            m_row = TIMING_ROW_RE.match(raw)
            if not m_row:
                row_idx += 1
                continue

            symbol = _clean_statement(m_row.group("symbol"))
            rest = _clean_statement(m_row.group("rest"))
            if len(symbol) < 2 or "(" not in symbol:
                row_idx += 1
                continue

            if row_idx + 1 < len(lines):
                nxt = _clean_statement(lines[row_idx + 1])
                if TIMING_UNIT_ONLY_RE.match(nxt) and re.search(r"\d$", rest):
                    rest = _clean_statement(f"{rest} {nxt}")

            rest = re.sub(r"\s+", " ", rest).strip()
            if not re.search(r"\d", rest):
                row_idx += 1
                continue

            row_key = f"{table_no}:{symbol.upper()}"
            if row_key in seen_rows:
                row_idx += 1
                continue
            seen_rows.add(row_key)

            statement = (
                f"Timing parameter '{symbol}' shall meet {rest} as specified in Table {table_no} ({table_title})."
            )
            candidates.append(
                Candidate(
                    statement=statement,
                    source=_format_source(page, row_idx + 1),
                    category="Digital",
                    note="Auto-extracted from OCR timing table row (one requirement per row)",
                    evidence_type="derived-from-structure",
                )
            )

            row_idx += 1

        idx = row_idx + 1

    return candidates


def _extract_image_candidates(
    lines: List[str],
    page: int,
    full_doc_text_lower: str,
    image_block_rules: Dict[str, List[Dict[str, object]]],
) -> List[Candidate]:
    candidates: List[Candidate] = []
    for line_no, line in enumerate(lines, start=1):
        caption = _clean_statement(line)
        if not re.match(r"^Image\s+\d+\s+[-–]\s+", caption, flags=re.IGNORECASE):
            continue

        caption_lower = caption.lower()
        if "system context" in caption_lower and "hardware block diagram" in caption_lower:
            image_id = re.match(r"^(Image\s+\d+)", caption, flags=re.IGNORECASE)
            label = image_id.group(1) if image_id else "Image"
            context_lines = lines[max(0, line_no - 6):line_no]
            context_text = _clean_statement(" ".join(_clean_statement(x) for x in context_lines))
            ctx = (context_text + " " + full_doc_text_lower).lower()

            image_statements: List[Tuple[str, str]] = []

            # Block-level candidates come from centralized project configuration.
            for rule in image_block_rules.get(label, []):
                statement_template = str(rule.get("statement") or "").strip()
                category = str(rule.get("category") or "").strip()
                trigger_any = rule.get("trigger_any")
                if not statement_template or category not in {"System", "Analog", "Digital"}:
                    continue
                if not isinstance(trigger_any, list):
                    continue
                normalized_triggers = [str(t).lower() for t in trigger_any if isinstance(t, str) and t.strip()]
                if not normalized_triggers:
                    continue
                if any(t in ctx for t in normalized_triggers):
                    image_statements.append((statement_template.format(image_label=label), category))

            # Connection/interface candidates from caption context
            if "ambient sensor" in ctx and "receives input" in ctx:
                image_statements.append(
                    (f"{label} indicates the device receives input from the ambient sensor.", "Analog")
                )
            if "remote sensor" in ctx and "receives input" in ctx:
                image_statements.append(
                    (f"{label} indicates the device receives input from the optional remote sensor when present.", "Digital")
                )
            if "drives" in ctx and "heating system" in ctx:
                image_statements.append(
                    (f"{label} indicates the device drives the external heating system interface.", "System")
                )
            if "external host" in ctx and "uart" in ctx:
                image_statements.append(
                    (f"{label} indicates the device communicates with the external host via UART.", "Digital")
                )

            seen_stmt: set[str] = set()
            for statement, category in image_statements:
                stmt_key = _clean_statement(statement).lower()
                if not stmt_key or stmt_key in seen_stmt:
                    continue
                seen_stmt.add(stmt_key)
                candidates.append(
                    Candidate(
                        statement=statement,
                        source=_format_source(page, line_no),
                        category=category,
                        note="Auto-extracted from OCR image/caption context (sub-block/interface) using ontology rule",
                        evidence_type="derived-from-structure",
                    )
                )
    return candidates


def _extract_table_spec_candidates(
    lines: List[str],
    idx: int,
    page: int,
    line_no: int,
    raw: str,
    has_spec_id_header: bool,
    has_table_header: bool,
) -> List[Candidate]:
    # Tagged requirement lines are handled by the dedicated tagged parser. Treating
    # them as table rows can incorrectly attach the preceding requirement text.
    if REQ_ID_TAGGED_START_RE.match(_clean_statement(raw)):
        return []
    if raw.endswith(".") or raw.endswith(";"):
        return []

    # First, prefer configured req-id pattern matches directly from table rows.
    explicit_req_id = _extract_table_reqid(raw)
    if not explicit_req_id:
        # OCR may split an ID prefix from its numeric suffix across lines.
        nxt = _clean_statement(lines[idx + 1]) if idx + 1 < len(lines) else ""
        prv = _clean_statement(lines[idx - 1]) if idx - 1 >= 0 else ""
        stitched_candidates = [
            _clean_statement(f"{raw} {nxt}"),
            _clean_statement(f"{prv} {raw}"),
        ]
        stitched_source_lines = [nxt, prv]
        for stitched, source_line in zip(stitched_candidates, stitched_source_lines):
            stitched_req_id = _extract_table_reqid(stitched)
            if (
                stitched_req_id
                and not _is_non_requirement_id_label(source_line, stitched_req_id)
                and not _is_non_requirement_id_label(stitched, stitched_req_id)
            ):
                explicit_req_id = stitched_req_id
                break
    if explicit_req_id:
        if _is_non_requirement_id_label(raw, explicit_req_id):
            return []
        # OCR can split table/figure headers from req-id rows across pages.
        # Accept explicit req-id rows when table OR req-id headers are present,
        # or when nearby context still indicates a table/figure region.
        if not _has_local_table_context(lines, idx):
            nearby = " ".join(
                _clean_statement(lines[j])
                for j in range(max(0, idx - 4), min(len(lines), idx + 3))
            )
            if not re.search(r"\b(table|figure)\s+\d+", nearby, flags=re.IGNORECASE):
                return []

        trace_lines = [line_no]
        statement = _clean_statement(
            re.sub(rf"\[?\s*{re.escape(explicit_req_id)}\s*\]?", "", raw, flags=re.IGNORECASE)
        )
        # If OCR line carries only the ID token, attach context from PREVIOUS lines only.
        # This keeps association with the same logical row and avoids switching to next row.
        if not statement:
            prev_statement, prev_lines = _compose_table_context_from_previous_lines(lines, idx, explicit_req_id)
            if prev_statement:
                statement = prev_statement
                trace_lines.extend(prev_lines)
            else:
                statement = f"Table row contains requirement ID {explicit_req_id}."

        if statement:
            trace_line_text = _format_line_numbers(trace_lines)
            return [
                Candidate(
                    statement=statement,
                    source=_format_source(page, line_no),
                    category=_detect_category(statement),
                    source_req_id=explicit_req_id,
                    note=(
                        "Auto-extracted from OCR table/figure req-id row"
                        + (f" | table_line_info=page{page}:lines[{trace_line_text}]" if trace_line_text else "")
                        + " | table_context_policy=same_line_only"
                    ),
                )
            ]

    # Compact IDs are opt-in and require an explicit ID header on the page.
    if not ALLOW_COMPACT_IDS or not has_spec_id_header:
        return []

    current_tokens = []
    for m in SPEC_ID_SIMPLE_RE.finditer(raw):
        token = (m.group(1) or "").upper()
        if token in {"ID", "SPEC", "TBD"}:
            continue
        # Ignore bit-field notations such as WTM4:0 or DR[1:0].
        tail = raw[m.end(): m.end() + 2]
        if re.match(r"^:\d", tail):
            continue
        # Keep table-style rows where token starts the line (possibly after a bullet).
        lead = raw[:m.start()].strip(" •-*\t")
        if lead:
            continue
        current_tokens.append(m)
    if not current_tokens:
        return []

    first_match = current_tokens[0]
    spec_req_id = first_match.group(1)
    body_start = first_match.end()
    body = _clean_statement(raw[body_start:])

    # Strict table-line policy: compact-ID fallback must stay on the same source line.
    if body:
        statement = _clean_statement(f"{spec_req_id} {body}")
    else:
        statement = f"Table row contains requirement ID {spec_req_id}."

    return [
        Candidate(
            statement=statement,
            source=_format_source(page, line_no),
            category=_detect_category(statement),
            source_req_id=spec_req_id,
            note=(
                f"Auto-extracted from OCR table row | table_line_info=page{page}:lines[{line_no}]"
                " | table_context_policy=same_line_only"
            ),
        )
    ]


def _extract_explicit_reqid_row_candidates(
    lines: List[str],
    page: int,
    page_has_spec_id_header: bool,
    page_has_table_header: bool,
) -> List[Candidate]:
    """Recover req-id rows from OCR table/figure layouts with broken headers."""
    candidates: List[Candidate] = []
    seen_reqids: set[str] = set()

    for idx, raw_line in enumerate(lines):
        raw = _clean_statement(raw_line)
        if not raw:
            continue
        if TAGGED_SOURCE_MODE and REQ_ID_TAGGED_START_RE.match(raw):
            continue

        nearby = " ".join(
            _clean_statement(lines[j])
            for j in range(max(0, idx - 4), min(len(lines), idx + 3))
        )
        has_table_context = (
            _has_local_table_context(lines, idx)
            or page_has_table_header
            or bool(re.search(r"\b(table|figure)\s+\d+", nearby, flags=re.IGNORECASE))
        )
        if not has_table_context:
            continue

        req_ids = _extract_table_reqids(raw)
        if not req_ids:
            nxt = _clean_statement(lines[idx + 1]) if idx + 1 < len(lines) else ""
            stitched = _clean_statement(f"{raw} {nxt}") if nxt else raw
            stitched_req_ids = _extract_table_reqids(stitched)
            # A standalone ID on the next line owns the complete row before it.
            # Defer to that ID line so wrapped cells are not finalized early.
            recent_lines = lines[max(0, idx - 8):idx]
            recent_context = " ".join(_clean_statement(previous_line) for previous_line in recent_lines)
            has_parameter_columns = any(
                re.match(
                    r"^(?:Generic\s+name|Port\s+name|Parameter|Symbol|Name)\b.*\b(?:Type|Value|Direction|TOP\s+CONNECTION|Unit)\b",
                    _clean_statement(previous_line),
                    flags=re.IGNORECASE,
                )
                for previous_line in recent_lines
            ) or bool(
                re.search(
                    r"\b(?:Generic\s+name|Port\s+name|Parameter|Symbol|Name)\b.*\b(?:Type|Value|Direction|TOP\s+CONNECTION|Unit)\b",
                    recent_context,
                    flags=re.IGNORECASE,
                )
            )
            if (
                stitched_req_ids
                and _extract_table_reqids(nxt)
                and not REQ_ID_TAGGED_START_RE.match(nxt)
                and (has_parameter_columns or page_has_table_header)
            ):
                continue
            req_ids = [
                req_id
                for req_id in stitched_req_ids
                if not _is_non_requirement_id_label(nxt, req_id)
                and not _is_non_requirement_id_label(stitched, req_id)
            ]

        req_ids = [req_id for req_id in req_ids if req_id not in seen_reqids]
        if not req_ids:
            continue

        statement = raw
        for req_id in req_ids:
            if _is_non_requirement_id_label(raw, req_id):
                req_ids = [candidate_id for candidate_id in req_ids if candidate_id != req_id]
        if not req_ids:
            continue
        for req_id in req_ids:
            statement = _clean_statement(
                re.sub(rf"\[?\s*{re.escape(req_id)}\s*\]?", "", statement, flags=re.IGNORECASE)
            )

        trace_lines = [idx + 1]
        if not statement or len(statement) < 12:
            prev_statement, prev_lines = _compose_table_context_from_previous_lines(lines, idx, req_id)
            if prev_statement:
                statement = prev_statement
                trace_lines.extend(prev_lines)

        if (not statement or len(statement) < 12) and idx + 1 < len(lines):
            nxt = _clean_statement(lines[idx + 1])
            if nxt and not _extract_table_reqid(nxt) and not _is_section_or_heading(nxt):
                statement = _clean_statement(f"{statement} {nxt}") if statement else nxt
                trace_lines.append(idx + 2)

        if idx > 0:
            previous_line = _clean_statement(lines[idx - 1])
            if (
                previous_line
                and previous_line not in statement
                and not _extract_table_reqid(previous_line)
                and not _line_has_req_id_header(previous_line)
            ):
                statement = _clean_statement(f"{statement} {previous_line}") if statement else previous_line
                trace_lines.append(idx)

        if not statement:
            statement = f"Table/figure row contains requirement ID {req_id}."

        trace_line_text = _format_line_numbers(trace_lines)
        for req_id in req_ids:
            candidates.append(
                Candidate(
                    statement=statement,
                    source=_format_source(page, idx + 1),
                    category=_detect_category(statement),
                    source_req_id=req_id,
                    note=(
                        "Auto-extracted from OCR explicit req-id row sweep"
                        + (f" | table_line_info=page{page}:lines[{trace_line_text}]" if trace_line_text else "")
                        + " | recovery_mode=header_split"
                    ),
                )
            )
            seen_reqids.add(req_id)

    return candidates


def _extract_reset_clock_table_candidates(
    lines: List[str],
    page: int,
    continuation_table_header: bool = False,
) -> List[Candidate]:
    """Derive normative connectivity/frequency requirements from reset/clock tables."""
    page_text = " ".join(_clean_statement(line) for line in lines).lower()
    is_reset = "reset scheme" in page_text or "reset table" in page_text
    is_clock = bool(re.search(r"\bclocks?\s+scheme\b", page_text)) or "clock table" in page_text
    is_functional_reset_summary = bool(
        re.search(r"functional\s+reset\s+summary", page_text, flags=re.IGNORECASE)
    )
    if continuation_table_header:
        is_reset = is_reset or "reset scheme is shown" in page_text
        is_clock = is_clock or bool(re.search(r"\b(?:16\s*mhz|32\s*khz|64\s*khz)\b", page_text))
    if not (is_reset or is_clock or is_functional_reset_summary):
        return []

    candidates: List[Candidate] = []
    for idx, raw_line in enumerate(lines):
        req_id = _extract_table_reqid(raw_line)
        if not req_id or not re.search(r"\d+$", req_id):
            continue
        has_table_columns = re.search(r"\b(req[_ ]?id|source)\b", page_text) and re.search(
            r"\b(destination|target)\b", page_text
        )
        if not has_table_columns and not continuation_table_header:
            continue

        row_parts: List[str] = []
        for row_idx in range(idx, min(len(lines), idx + 18)):
            part = _clean_statement(lines[row_idx])
            next_row_id = TABLE_REQID_RE.match(part)
            if row_idx != idx and next_row_id and (
                next_row_id.end() == len(part) or part[next_row_id.end()].isspace()
            ):
                break
            if row_idx != idx and re.match(r"^(?:Table|Figure|Section)\s+\d+", part, flags=re.IGNORECASE):
                break
            if part:
                row_parts.append(part)
        row_text = " ".join(row_parts)
        row_text = re.sub(rf"\b{re.escape(req_id)}\b", "", row_text, flags=re.IGNORECASE)
        row_text = _clean_statement(row_text)

        path_prefix_match = re.search(r"\s+1\s+", row_text)
        if path_prefix_match:
            path_prefix = re.sub(r"\s+", "", row_text[:path_prefix_match.start()])
            root_matches = list(re.finditer(r"(?:u_)?[A-Za-z][A-Za-z0-9_]*\.", path_prefix))
            if len(root_matches) >= 2:
                first_root = root_matches[0].group(0)
                second_root = next(
                    (match for match in root_matches[1:] if match.group(0) == first_root),
                    None,
                )
                if second_root:
                    row_text = (
                        path_prefix[:second_root.start()]
                        + " "
                        + path_prefix[second_root.start():]
                        + row_text[path_prefix_match.start():]
                    )

        # Table cells may wrap hierarchical paths across physical OCR lines.
        # Repeated hierarchy roots identify the source/target cell boundary;
        # fragments inside each cell are joined without introducing spaces.
        hierarchy_roots = list(re.finditer(r"\b([A-Za-z_]\w*)\.", row_text))
        if len(hierarchy_roots) >= 2:
            first_root = hierarchy_roots[0].group(1)
            second_root = next(
                (match for match in hierarchy_roots[1:] if match.group(1) == first_root),
                None,
            )
            if second_root:
                source_cell = re.sub(r"\s+", "", row_text[:second_root.start()])
                target_cell = row_text[second_root.start():]
                target_parts = re.split(
                    r"\s+(?:No|1|\d+\s*(?:MHz|kHz)|F\s*max|Frequency|Clock\s+gating)\b",
                    target_cell,
                    maxsplit=1,
                    flags=re.IGNORECASE,
                )[0]
                target_prefix = target_cell
                target_cell = re.sub(r"\s+", "", target_parts[0])
                qualifier_tail = target_prefix[len(target_parts[0]):]
                if source_cell and target_cell and "." in source_cell and "." in target_cell:
                    row_text = f"{source_cell} {target_cell}{qualifier_tail}"

        signal_markers = list(
            re.finditer(
                r"\b(?:u_)?[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)+\b",
                row_text,
            )
        )
        if len(signal_markers) < 2:
            continue
        source_signal = _clean_statement(row_text[signal_markers[0].start():signal_markers[1].start()])
        target_signal = _clean_statement(row_text[signal_markers[1].start():])
        target_cells = re.split(r"\s+(No|1)\s+", target_signal, maxsplit=1)
        target_signal = target_cells[0]
        leading_cell = target_cells[1] if len(target_cells) > 1 else ""
        trailing_cells = target_cells[2] if len(target_cells) > 2 else ""
        source_signal = re.sub(r"\s+", "", source_signal)
        target_signal = re.sub(r"\s+", "", target_signal)
        if not source_signal or not target_signal:
            continue

        frequency_match = re.search(
            r"(?:f\s*max|frequency)\s*[:=]?\s*([^,;]+)",
            row_text,
            flags=re.IGNORECASE,
        )
        if not frequency_match:
            frequency_matches = list(re.finditer(r"\b\d+\s*(?:MHz|kHz)\b", row_text, flags=re.IGNORECASE))
            frequency_match = frequency_matches[-1] if frequency_matches else None
        clock_gating_match = re.search(
            r"(?:clock\s+gating|clk\s+gating|gating)\s*[:=]?\s*([^,;]+)",
            row_text,
            flags=re.IGNORECASE,
        )
        clock_gating = ""
        if clock_gating_match:
            clock_gating = _clean_statement(clock_gating_match.group(1))
        elif leading_cell.lower() == "no":
            clock_gating = leading_cell
        elif trailing_cells and frequency_match:
            gating_match = re.search(
                r"(.+?)\s+No\s+\d+\s*(?:MHz|kHz)\b",
                trailing_cells,
                flags=re.IGNORECASE,
            )
            if gating_match:
                clock_gating = _clean_statement(gating_match.group(1))
        if not clock_gating:
            gating_match = re.search(
                r"\s+1\s+(.+?)\s+No\s+\d+\s*(?:MHz|kHz)\b",
                row_text,
                flags=re.IGNORECASE,
            )
            if gating_match:
                clock_gating = _clean_statement(gating_match.group(1))
        suffix_parts: List[str] = []
        note_parts = [
            "Derived from reset/clock table columns req_id, source, "
            "destination/target and optional F max/Frequency/clock gating"
        ]
        if is_clock and frequency_match:
            frequency = _clean_statement(
                frequency_match.group(1) if frequency_match.lastindex else frequency_match.group(0)
            )
            if frequency:
                suffix_parts.append(f"with frequency {frequency}")
                note_parts.append(f"frequency={frequency}")
        if clock_gating:
            if clock_gating.lower() == "no":
                suffix_parts.append("without clock gating")
                note_parts.append("clock_gating=No")
            else:
                suffix_parts.append(f"with clock gating {clock_gating}")
                note_parts.append(f"clock_gating={clock_gating}")

        suffix = f", {' and '.join(suffix_parts)}" if suffix_parts else ""
        statement = f"The {source_signal} signal shall be connected to the {target_signal} signal{suffix}."
        derivation_kind = "reset_table_connection"
        if is_clock and frequency_match:
            derivation_kind = "clock_table_connection_frequency"

        candidates.append(
            Candidate(
                statement=statement,
                source=_format_source(page, idx + 1),
                category="Digital",
                source_req_id=req_id,
                covered_source_req_id=req_id,
                derivation_kind=derivation_kind,
                note=(
                    " | ".join(note_parts)
                    + f" | table_line_info=page{page}:lines[{idx + 1}-{min(len(lines), idx + 18)}]"
                ),
                evidence_type="derived-from-structure",
            )
        )
    return candidates


def _line_starts_interrupt_row(text: str) -> bool:
    return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_]*\s+\d+(?::\d+)?\b", _clean_statement(text)))


def _extract_interrupt_table_candidates(lines: List[str], page: int) -> List[Candidate]:
    """Derive requirements from interrupt rows using only Interrupt/bit/Description columns."""
    page_text = " ".join(_clean_statement(line) for line in lines)
    if not re.search(r"\bInterrupt\s+bit\s+Description\b", page_text, flags=re.IGNORECASE):
        return []

    candidates: List[Candidate] = []
    for idx, raw_line in enumerate(lines):
        if not _line_starts_interrupt_row(raw_line):
            continue

        row_parts: List[str] = []
        for row_idx in range(idx, min(len(lines), idx + 4)):
            part = _clean_statement(lines[row_idx])
            if row_idx != idx and (part.lower().startswith("[end]") or REQ_ID_TAGGED_START_RE.match(part)):
                break
            if row_idx != idx and _line_starts_interrupt_row(part):
                break
            if part:
                row_parts.append(part)

        row_text = _clean_statement(" ".join(row_parts))
        req_id = _extract_table_reqid(row_text)
        if not req_id:
            continue
        row_text = re.sub(rf"\[?\b{re.escape(req_id)}\b\]?", "", row_text, flags=re.IGNORECASE)
        row_text = _clean_statement(row_text)

        match = re.match(
            r"^(?P<interrupt>[A-Za-z_][A-Za-z0-9_]*)\s+(?P<bit>\d+(?::\d+)?(?:\s+\d+)?)\s+(?P<description>.+)$",
            row_text,
        )
        if not match:
            continue

        interrupt_label = _clean_statement(match.group("interrupt"))
        bit_label = _clean_statement(match.group("bit"))
        description = _clean_statement(match.group("description"))
        if not interrupt_label or not bit_label or not description:
            continue

        statement = f"The {interrupt_label} interrupt shall be connected to {description} to bit {bit_label}."
        candidates.append(
            Candidate(
                statement=statement,
                source=_format_source(page, idx + 1),
                category="Digital",
                source_req_id=req_id,
                covered_source_req_id=req_id,
                derivation_kind="interrupt_table_connection",
                note=(
                    "Derived from interrupt table columns Interrupt, bit, Description"
                    f" | table_line_info=page{page}:lines[{idx + 1}-{min(len(lines), idx + len(row_parts))}]"
                ),
                evidence_type="derived-from-structure",
            )
        )
    return candidates


def _detect_category(statement: str) -> str:
    s = statement.lower()
    if re.search(r"\b(fifo|stream mode|bypass mode|watermark|drdy|int1|int2|register|ctrl_reg|out_[xyz]|i2c|spi|sda|scl|serial|sub\(7\)|sub\(6-0\))\b", s):
        return "Digital"
    if any(k in s for k in DIGITAL_HINTS):
        return "Digital"
    if any(k in s for k in ANALOG_HINTS):
        return "Analog"
    return "System"


def _category_prefix(category: str) -> str:
    if category == "System":
        return "SYS"
    if category == "Analog":
        return "ANA"
    return "DIG"


def _id_scheme_prefix(content_class: str) -> str:
    if content_class == "Definition":
        return "DEF_"
    if content_class == "Validation constraint":
        return "VAL_CONSTR_"
    if content_class == "Configuration":
        return "CONF_"
    if content_class == "Description":
        return "DES_"
    return "REQ_"


def _detect_requirement_type(statement: str) -> str:
    s = statement.lower()
    if re.search(r"\b(manual mode|schedule mode|off mode|automatic selection mode|state|initialization|idle|measurement state|control state|error state)\b", s):
        return "mode-behavior"
    if re.search(r"\b(uart|command|interface|host|response|baud|data bits|parity|stop bit)\b", s):
        return "interface"
    if re.search(r"\b(one second|milliseconds|ms|minute|response time|duration|period|time slot|current time)\b", s):
        return "timing"
    if re.search(r"\b(voltage|supply|current|dc|polarity|power|relay output current|brown-out)\b", s):
        return "electrical"
    if re.search(r"\b(setpoint|hysteresis|configuration|schedule|factory default|operating mode|parameter)\b", s):
        return "configuration"
    if re.search(r"\b(fault|safe|forced off|error|unrecoverable|protection|critical)\b", s):
        return "safety"
    if re.search(r"\b(temperature|accuracy|resolution|range|sensor|measurement|adc|analog-to-digital)\b", s):
        return "functional"
    return "other"


def _detect_content_class(requirement_type: str) -> str:
    if requirement_type == "configuration":
        return "Configuration"
    return "Requirement"


def _test_trace_required(content_class: str) -> str:
    if content_class in {"Requirement", "Configuration", "Validation constraint"}:
        return "yes"
    return "no"


def _detect_operating_mode(statement: str) -> str:
    modes = []
    s = statement.lower()
    for label in ["manual mode", "schedule mode", "off mode", "automatic selection mode", "initialization state", "idle state", "measurement state", "control state", "error state"]:
        if label in s:
            modes.append(label)
    return "; ".join(modes)


def _detect_parameter_signal_register(statement: str) -> str:
    table_match = re.search(r"Parameter '([^']+)'", statement)
    if table_match:
        return table_match.group(1)
    s = statement.lower()
    candidates = [
        ("UART", "uart"),
        ("relay output", "relay"),
        ("ambient sensor", "ambient sensor"),
        ("remote sensor", "remote sensor"),
        ("LED", "led"),
        ("push button", "button"),
        ("event log", "event log"),
        ("setpoint", "setpoint"),
        ("hysteresis", "hysteresis"),
        ("supply voltage", "supply"),
        ("control temperature", "control temperature"),
    ]
    found = [name for name, token in candidates if token in s]
    return "; ".join(dict.fromkeys(found))


def _detect_value_range_condition(statement: str) -> str:
    table_match = re.search(r"is specified as (.*?)(?:; note:|\.$)", statement)
    if table_match:
        return _clean_statement(table_match.group(1))

    patterns = [
        r"\b\d+(?:\.\d+)?\s*(?:degrees Celsius|°C|V DC|V|mA|baud|bits|events|hours|milliseconds|ms|seconds?|minute|minutes|%)\b",
        r"\bminus\s+\d+\s+degrees Celsius\b",
        r"\bplus or minus\s+\d+(?:\.\d+)?\s*(?:percent|degrees Celsius)\b",
        r"\bplus or minus\s+\d+(?:\.\d+)?\s*%\b",
        r"\b(?:at least|less than|greater than|less than or equal to|greater than or equal to|up to|down to|within)\s+[^.;,]+",
        r"\b\d+\s+to\s+\d+\s*°C\b",
        r"\b-\d+\s+to\s+\d+\s*°C\b",
        r"±\s*\d+(?:\.\d+)?\s*°C(?:\s*\([^)]*\))?",
    ]
    values: List[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, statement, flags=re.IGNORECASE):
            values.append(_clean_statement(match.group(0)))
    return "; ".join(dict.fromkeys(values))


def _build_rationale(candidate: Candidate, requirement_type: str) -> str:
    if "image/caption context" in candidate.note:
        return f"Image caption and adjacent PDF text indicate a {requirement_type} candidate from diagram context."
    if "table row value" in candidate.note:
        return f"Table row encodes a {requirement_type} constraint with auditable value/range data."
    if "functional sentence" in candidate.note:
        return f"Narrative sentence states device behavior classified as a {requirement_type} requirement."
    if candidate.source_req_id:
        return "Source requirement ID was preserved from the specification text."
    return f"Normative pattern or accepted requirement phrase indicates a {requirement_type} requirement."


def _read_index(index_csv: Path) -> List[Tuple[int, Path, str]]:
    repo_root = Path(__file__).resolve().parent.parent
    rows: List[Tuple[int, Path, str]] = []
    with index_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if (row.get("status") or "").strip() != "text-extracted":
                continue
            page = int(row["page"])
            text_file = resolve_repo_path(repo_root, row["text_file"])
            source_file = portable_repo_path(repo_root, row["source_file"])
            rows.append((page, text_file, source_file))
    rows.sort(key=lambda x: x[0])
    return rows


def _functional_description_bounds(index_rows: List[Tuple[int, Path, str]]) -> Dict[int, Tuple[int, Optional[int]]]:
    bounds: Dict[int, Tuple[int, Optional[int]]] = {}
    in_section = False

    has_reset_clock_table_header = False
    for page, text_file, _source in index_rows:
        if not text_file.exists():
            continue
        lines = text_file.read_text(encoding="utf-8", errors="ignore").splitlines()
        page_start: Optional[int] = 1 if in_section else None
        page_end: Optional[int] = None

        for line_no, line in enumerate(lines, start=1):
            raw = _clean_statement(line)
            if re.match(r"^\d+(?:\.\d+){0,3}\.?\s+Functional Description\b", raw, flags=re.IGNORECASE):
                in_section = True
                page_start = line_no + 1
                continue
            if in_section and re.match(r"^\d+(?:\.\d+){0,3}\.?\s+[A-Za-z]", raw) and not re.search(r"Functional Description\b", raw, flags=re.IGNORECASE):
                page_end = line_no - 1
                in_section = False
                break

        if page_start is not None:
            if page_start <= len(lines) and (page_end is None or page_end >= page_start):
                bounds[page] = (page_start, page_end)

    return bounds


def _collect_candidates(
    index_rows: List[Tuple[int, Path, str]],
    image_block_rules: Dict[str, List[Dict[str, object]]],
) -> List[Candidate]:
    combined_pattern = re.compile("|".join(NORMATIVE_PATTERNS), flags=re.IGNORECASE)
    seen: set[str] = set()
    candidate_index_by_reqid: Dict[str, int] = {}
    candidates: List[Candidate] = []
    functional_bounds = _functional_description_bounds(index_rows)
    full_doc_lines = [
        _clean_statement(x)
        for _p, tf, _s in index_rows
        if tf.exists()
        for x in tf.read_text(encoding="utf-8", errors="ignore").splitlines()
        if _clean_statement(x)
    ]
    full_doc_text = " ".join(full_doc_lines)
    full_doc_text_lower = " ".join(
        _clean_statement(x).lower()
        for _p, tf, _s in index_rows
        if tf.exists()
        for x in tf.read_text(encoding="utf-8", errors="ignore").splitlines()
    )

    page_lines_by_index: List[List[str]] = []
    for _page, text_file, _source in index_rows:
        if text_file.exists():
            page_lines_by_index.append(
                _normalize_split_req_id_lines(
                    text_file.read_text(encoding="utf-8", errors="ignore").splitlines()
                )
            )
        else:
            page_lines_by_index.append([])

    has_reset_clock_table_header = False
    for page_index, (page, text_file, _source) in enumerate(index_rows):
        if not text_file.exists():
            continue
        lines = page_lines_by_index[page_index]
        continuation_lines = [
            line
            for later_page_lines in page_lines_by_index[page_index + 1:]
            for line in later_page_lines
        ]
        page_text_lower = " ".join(_clean_statement(x).lower() for x in lines)
        continuation_table_header = has_reset_clock_table_header
        has_reset_clock_table_header = bool(
            re.search(r"\b(req[_ ]?id|source)\b", page_text_lower)
            and re.search(r"\b(destination|target)\b", page_text_lower)
            and re.search(r"\b(clock|reset)\b", page_text_lower)
        )
        page_has_spec_id_header = any(_line_has_req_id_header(x) for x in lines)
        page_has_table_header = bool(re.search(r"\btable\s+\d+", page_text_lower, flags=re.IGNORECASE))

        semantic_candidates = _extract_functional_sentence_candidates(lines, page)
        architecture_candidates = [
            candidate
            for candidate in _extract_functional_sentence_candidates(
                lines, page, force_all_sentences=True
            )
            if _looks_like_architecture_capability(candidate.statement)
            and not POWER_MANAGEMENT_CONCEPT_RE.search(candidate.statement)
        ]
        for candidate in architecture_candidates:
            candidate.derivation_kind = "architecture_capability"
            candidate.note = (
                "Auto-extracted from source-backed architecture capability or functional definition"
            )
            candidate.evidence_type = "explicit"
            if TAGGED_SOURCE_MODE:
                candidate.category = "System"
        semantic_candidates.extend(architecture_candidates)
        power_concept_candidates = [
            candidate
            for candidate in _extract_functional_sentence_candidates(
                lines, page, force_all_sentences=True
            )
            if POWER_MANAGEMENT_CONCEPT_RE.search(candidate.statement)
        ]
        for candidate in power_concept_candidates:
            candidate.derivation_kind = "power_management_concept"
            candidate.note = (
                "Auto-extracted from source-backed power-management architecture concept"
            )
            candidate.evidence_type = "explicit"
            if TAGGED_SOURCE_MODE:
                candidate.category = "System"
        semantic_candidates.extend(power_concept_candidates)
        if page in functional_bounds:
            start_line, end_line = functional_bounds[page]
            semantic_candidates.extend(
                _extract_functional_sentence_candidates(
                    lines,
                    page,
                    force_all_sentences=True,
                    start_line=start_line,
                    end_line=end_line,
                )
            )
        semantic_candidates.extend(_extract_timing_table_row_candidates(lines, page))
        semantic_candidates.extend(_extract_measurement_table_row_candidates(lines, page))
        semantic_candidates.extend(_extract_block_diagram_candidates(lines, page, full_doc_lines))
        semantic_candidates.extend(_extract_image_candidates(lines, page, full_doc_text_lower, image_block_rules))
        semantic_candidates.extend(_extract_interrupt_table_candidates(lines, page))
        semantic_candidates.extend(
            _extract_explicit_reqid_row_candidates(
                lines,
                page,
                page_has_spec_id_header,
                page_has_table_header,
            )
        )
        semantic_candidates.extend(
            _extract_reset_clock_table_candidates(lines, page, continuation_table_header)
        )

        for semantic_candidate in semantic_candidates:
            if TAGGED_SOURCE_MODE and not semantic_candidate.source_req_id:
                semantic_candidate.source_req_id = _extract_tagged_reqid_fallback(semantic_candidate.statement)
            if TAGGED_SOURCE_MODE and _is_architecture_function_candidate(semantic_candidate):
                semantic_candidate.derivation_kind = (
                    semantic_candidate.derivation_kind
                    if semantic_candidate.derivation_kind != "raw"
                    else "architecture_function"
                )
                semantic_candidate.category = "System"
                semantic_candidate.note = (
                    "Auto-extracted from source-backed main functionality description"
                )
            dedupe_key = _candidate_dedupe_key(semantic_candidate.statement, semantic_candidate.source_req_id)
            existing_index = candidate_index_by_reqid.get(semantic_candidate.source_req_id or "")
            if TAGGED_SOURCE_MODE and existing_index is not None:
                candidates[existing_index] = _prefer_better_candidate(
                    candidates[existing_index], semantic_candidate
                )
                continue
            if dedupe_key not in seen:
                seen.add(dedupe_key)
                if semantic_candidate.source_req_id:
                    candidate_index_by_reqid[semantic_candidate.source_req_id] = len(candidates)
                candidates.append(semantic_candidate)

        line_no = 1
        while line_no <= len(lines):
            idx = line_no - 1
            raw = _clean_statement(lines[idx])
            fallback_req_id = _extract_tagged_reqid_fallback(raw)

            tagged_candidate, consumed_idx = _extract_tagged_reqid_candidate(
                lines,
                idx,
                page,
                continuation_lines=continuation_lines,
            )
            if tagged_candidate:
                dedupe_key = _candidate_dedupe_key(tagged_candidate.statement, tagged_candidate.source_req_id)
                existing_index = candidate_index_by_reqid.get(tagged_candidate.source_req_id or "")
                if TAGGED_SOURCE_MODE and existing_index is not None:
                    candidates[existing_index] = _prefer_better_candidate(
                        candidates[existing_index], tagged_candidate
                    )
                    line_no = consumed_idx + 2
                    continue
                if dedupe_key not in seen:
                    seen.add(dedupe_key)
                    if tagged_candidate.source_req_id:
                        candidate_index_by_reqid[tagged_candidate.source_req_id] = len(candidates)
                    candidates.append(tagged_candidate)
                line_no = consumed_idx + 2
                continue

            if not TAGGED_SOURCE_MODE:
                for table_candidate in _extract_table_spec_candidates(
                    lines,
                    idx,
                    page,
                    line_no,
                    raw,
                    page_has_spec_id_header,
                    page_has_table_header,
                ):
                    dedupe_key = _candidate_dedupe_key(table_candidate.statement, table_candidate.source_req_id)
                    if dedupe_key not in seen:
                        seen.add(dedupe_key)
                        candidates.append(table_candidate)

            inline_defs = _extract_inline_reqid_segments(raw)
            if inline_defs:
                for idx_def, (source_req_id, body) in enumerate(inline_defs):
                    if idx_def == 0 and REQ_ID_DEFINITION_RE.match(raw):
                        statement = _collect_definition_sentence(lines, idx, body, source_req_id)
                    else:
                        statement = _clean_statement(body)

                    if not statement or _is_noise_line(statement):
                        continue

                    dedupe_key = _candidate_dedupe_key(statement, source_req_id)
                    if dedupe_key in seen:
                        continue

                    seen.add(dedupe_key)
                    cat = _detect_category(statement)
                    source = _format_source(page, line_no)
                    fallback_req_id = (
                        _extract_tagged_reqid_fallback(statement)
                        if TAGGED_SOURCE_MODE
                        else source_req_id
                    )
                    candidates.append(
                        Candidate(
                            statement=statement,
                            source=source,
                            category=cat,
                            source_req_id=fallback_req_id or source_req_id,
                        )
                    )
                line_no += 1
                continue

            if _is_noise_line(raw):
                line_no += 1
                continue
            if _is_parameter_table_fragment(page_text_lower, raw):
                line_no += 1
                continue
            if not combined_pattern.search(raw.lower()):
                line_no += 1
                continue

            rebuilt = _collect_normative_sentence(lines, line_no - 1, raw)
            if rebuilt:
                raw = rebuilt

            # Keep one copy per normalized statement to reduce duplicates from headers/footers.
            dedupe_key = _candidate_dedupe_key(raw)
            if dedupe_key in seen:
                # If this deduped statement contains a tagged requirement ID, enrich the
                # previously inserted candidate so final IDs preserve tagged source IDs.
                if fallback_req_id:
                    for existing_candidate in reversed(candidates):
                        if existing_candidate.source_req_id:
                            continue
                        existing_key = _candidate_dedupe_key(existing_candidate.statement)
                        if existing_key == dedupe_key:
                            existing_candidate.source_req_id = fallback_req_id
                            break
                line_no += 1
                continue
            seen.add(dedupe_key)

            cat = _detect_category(raw)
            source = _format_source(page, line_no)
            spec_req_id = _extract_reqid_from_spec_id_context(lines, idx)
            if fallback_req_id:
                spec_req_id = fallback_req_id
            candidates.append(Candidate(statement=raw, source=source, category=cat, source_req_id=spec_req_id))

            line_no += 1

    return candidates


def _write_summary_csv(path: Path, records: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=SUMMARY_FIELDS,
        )
        writer.writeheader()
        writer.writerows(records)


def _write_table_row_review(path: Path, request_path: Path, records: List[Dict[str, str]]) -> int:
    """Record table rows that require manual review instead of silent acceptance."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rows: List[List[str]] = []
    dangling_tokens = {
        "and", "or", "to", "of", "for", "in", "on", "at", "with", "from", "the", "a", "an"
    }
    for record in records:
        notes = record.get("notes", "")
        is_table_row = (
            "recovery_mode=header_split" in notes
            or record.get("derivation_kind", "") in {
                "reset_table_connection",
                "clock_table_connection_frequency",
                "interrupt_table_connection",
            }
        )
        if not is_table_row:
            continue
        statement = _clean_statement(record.get("requirement_statement", ""))
        derivation_kind = record.get("derivation_kind", "")
        if derivation_kind == "clock_table_connection_frequency":
            table_kind = "clock_reset_structural"
        elif derivation_kind == "reset_table_connection":
            table_kind = "clock_reset_structural"
        elif derivation_kind == "interrupt_table_connection":
            table_kind = "interrupt_structural"
        else:
            table_kind = "explicit_req_id_table_row"
        normalized = statement.lower().rstrip(".;").strip()
        reasons: List[str] = []
        if not statement:
            reasons.append("empty_row_statement")
        if normalized.endswith(":"):
            reasons.append("expected_last_value_missing")
        if normalized and normalized.split()[-1] in dangling_tokens:
            reasons.append("dangling_token")
        if re.search(r"\[DDS_STBIO1_\d+\]", statement):
            reasons.append("cross_row_source_id")
        status = "manual_review" if reasons else "accepted"
        rows.append([
            record.get("source_req_id", ""),
            table_kind,
            status,
            ";".join(reasons),
            statement,
            record.get("source", ""),
            "manual review required" if reasons else "row reconstruction validated",
        ])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "source_req_id", "table_kind", "review_status", "review_reason", "reconstructed_statement", "source", "action"
        ])
        writer.writerows(rows)
    manual_rows = [row for row in rows if row[2] == "manual_review"]
    request_path.parent.mkdir(parents=True, exist_ok=True)
    request_lines = [
        "# Stage 1 Table Row Manual Review",
        "",
        "Stage 1 is stopped because one or more OCR table rows are ambiguous.",
        "Review `table_row_review.csv`, correct the source interpretation if needed, and rerun Stage 1.",
        "Do not approve a row whose mandatory fields or expected final value are still missing.",
        "",
        f"Rows requiring review: {len(manual_rows)}",
        "",
    ]
    for row in manual_rows:
        request_lines.append(f"- {row[0]}: {row[3]} ({row[5]})")
    request_path.write_text("\n".join(request_lines).rstrip() + "\n", encoding="utf-8")
    return len(manual_rows)


def _write_raw_md(path: Path, records: List[Dict[str, str]]) -> None:
    by_cat: Dict[str, List[Dict[str, str]]] = {"System": [], "Analog": [], "Digital": []}
    for item in records:
        by_cat[item["category"]].append(item)

    lines = [
        "# Extracted Functional Requirements (Raw)",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
    ]

    for category in ["System", "Analog", "Digital"]:
        lines.append(f"## {category}")
        if not by_cat[category]:
            lines.append("- No requirements extracted.")
            lines.append("")
            continue
        for row in by_cat[category]:
            statement = (row["requirement_statement"] or "").replace("•", "-")
            lines.append(f"- {row['id']}: {statement} ({row['source']})")
        lines.append("")

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _write_summary_md(path: Path, records: List[Dict[str, str]]) -> None:
    display_headers = {
        "id": "ID",
        "source_req_id": "Source Req ID",
        "covered_source_req_id": "Covered Source Req ID",
        "id_policy": "ID Policy",
        "requirement_statement": "Requirement statement",
        "category": "Category",
        "source": "Source",
        "source_section_owner": "Source Section Owner",
        "derivation_kind": "Derivation Kind",
        "evidence_type": "Evidence type",
        "notes": "Notes",
        "rationale": "Rationale",
        "content_class": "Content class",
        "test_trace_required": "Test trace required",
        "requirement_type": "Requirement type",
        "operating_mode": "Operating mode",
        "parameter_signal_register": "Parameter/Signal/Register",
        "value_range_condition": "Value/Range/Condition",
    }

    lines = [
        "# Functional Requirements Summary",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "| " + " | ".join(display_headers.get(name, name) for name in SUMMARY_FIELDS) + " |",
        "| " + " | ".join(["---"] * len(SUMMARY_FIELDS)) + " |",
    ]
    for row in records:
        cells = [
            str(row.get(name, "") or "").replace("•", "-").replace("|", "\\|")
            for name in SUMMARY_FIELDS
        ]
        lines.append("| " + " | ".join(cells) + " |")

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _write_stage01_report(path: Path, source_spec: str, records: List[Dict[str, str]], tagged_mode: bool) -> None:
    total = len(records)
    sys_count = sum(1 for r in records if r["category"] == "System")
    ana_count = sum(1 for r in records if r["category"] == "Analog")
    dig_count = sum(1 for r in records if r["category"] == "Digital")
    generated_count = sum(1 for r in records if (r.get("id_policy") or "") == "generated_standard")
    tagged_count = sum(1 for r in records if (r.get("id_policy") or "") == "tagged_preserve")

    gate_status = "fail" if tagged_mode and generated_count > 0 else "pass"

    risks = ["- Some statements may need wording normalization during domain review."]
    if tagged_mode:
        if generated_count > 0:
            risks.insert(
                0,
                f"- Strict tagged mode violation: generated_standard rows present ({generated_count}).",
            )
        else:
            risks.insert(0, "- Tagged-source strict mode active: only source-tagged IDs are emitted.")
    else:
        risks.insert(
            0,
            "- Requirement IDs follow mixed policy: tagged sources preserve source IDs; non-tagged content uses generated IDs.",
        )

    lines = [
        "# Stage 01 Report",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## Scope",
        "- Functional requirement extraction and summary table generation from full specification text.",
        f"- Source specification: `{source_spec}`.",
        "",
        "## Evidence",
        "- Functional requirements extracted",
        "- Functional Description sentences extracted through final sentence punctuation",
        "- PDF table row/value candidates extracted",
        "- Timing table rows extracted with one requirement per timing row",
        "- Analog/electrical/measurement characteristic tables extracted with one requirement per row",
        "- Block diagram block names extracted and crosschecked against specification behavior sentences",
        "- PDF image/caption context candidates extracted as derived-from-structure evidence",
        "- Requirement summary table generated",
        "- Source paragraph references validated",
        "",
        "## Extraction Metrics",
        f"- Total requirements listed: {total}",
        f"- System requirements: {sys_count}",
        f"- Analog requirements: {ana_count}",
        f"- Digital requirements: {dig_count}",
        f"- Tagged preserve rows: {tagged_count}",
        f"- Generated standard rows: {generated_count}",
        "",
        "## Status",
        f"- Gate 1: {gate_status}",
        "",
        "## Risks",
    ]
    lines.extend(risks)

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    global TAGGED_SOURCE_MODE

    parser = argparse.ArgumentParser(description="Generate Stage 1 requirement artifacts from OCR extracts")
    parser.add_argument("--index", default="artifacts/stage1_requirements/ocr_extracts/index.csv")
    parser.add_argument("--raw", default="artifacts/stage1_requirements/requirements_raw.md")
    parser.add_argument("--summary-csv", default="artifacts/stage1_requirements/requirements_summary.csv")
    parser.add_argument("--summary-md", default="artifacts/stage1_requirements/requirements_summary.md")
    parser.add_argument(
        "--duplicate-report",
        default="artifacts/stage1_requirements/duplicate_source_req_ids.csv",
        help="Report repeated source requirement IDs found during extraction",
    )
    parser.add_argument(
        "--table-review-report",
        default="artifacts/stage1_requirements/table_row_review.csv",
        help="Report ambiguous reconstructed table rows for manual review",
    )
    parser.add_argument(
        "--table-review-request",
        default="artifacts/stage1_requirements/table_row_review_request.md",
        help="User review request generated when table rows are ambiguous",
    )
    parser.add_argument("--stage-report", default="artifacts/orchestrator/stage_01_report.md")
    parser.add_argument("--min-target", type=int, default=100)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")
    _init_requirement_id_rules(repo_root)

    index_path = Path(args.index)
    if not index_path.is_absolute():
        index_path = (repo_root / index_path).resolve()

    if not index_path.exists():
        print(f"Stage1 generation: FAIL (missing index: {index_path})")
        _append_log(repo_root, script_name, f"FAIL missing_index={index_path.as_posix()}")
        return 1

    index_rows = _read_index(index_path)
    if not index_rows:
        print("Stage1 generation: FAIL (no text-extracted pages in index)")
        _append_log(repo_root, script_name, "FAIL no_text_extracted_pages")
        return 1

    # Rule decision: detect tagged-source format first from extracted content.
    # If tagged source is detected, preserve original source req IDs.
    # Otherwise apply standard generated ID rules.
    configured_tagged_mode = TAGGED_SOURCE_MODE
    detected_tagged_mode = _detect_tagged_source_mode(index_rows)
    # Never disable explicitly configured tagged mode due to weak OCR pre-detection.
    # If either configuration or content detection indicates tagged source, preserve tags.
    effective_tagged_mode = configured_tagged_mode or detected_tagged_mode
    if configured_tagged_mode != detected_tagged_mode:
        _append_log(
            repo_root,
            script_name,
            f"INFO tagged_mode_override configured={configured_tagged_mode} detected={detected_tagged_mode}",
        )
    TAGGED_SOURCE_MODE = effective_tagged_mode

    _init_source_context(index_rows)
    _init_architecture_analysis_rules(repo_root)
    image_block_rules = _load_image_block_rules(repo_root)
    candidates = _collect_candidates(index_rows, image_block_rules)
    source_spec = index_rows[0][2]

    source_spec_path = resolve_repo_path(repo_root, source_spec)
    if source_spec_path.suffix.lower() in {".html", ".htm"} and source_spec_path.exists():
        html_req_map = _extract_html_reqid_definitions(source_spec_path)
        _apply_html_reqid_overrides(candidates, html_req_map)
        _add_missing_html_reqid_candidates(candidates, html_req_map, index_rows)

    _add_missing_approved_tagged_candidates(candidates, index_rows)
    owner_terms = _load_source_section_owner_terms(repo_root)
    _annotate_source_section_owners(candidates, owner_terms)
    power_owner = _configured_power_management_owner(owner_terms)
    if power_owner and not effective_tagged_mode:
        for candidate in candidates:
            if (
                candidate.derivation_kind == "power_management_concept"
                and not candidate.source_section_owner
            ):
                candidate.source_section_owner = power_owner

    # Final source_req_id backfill pass: if a statement embeds a tagged req ID,
    # persist it explicitly even when earlier extraction paths missed it.
    for c in candidates:
        if not c.source_req_id:
            fallback_req_id = _extract_tagged_reqid_fallback(c.statement)
            if fallback_req_id:
                c.source_req_id = fallback_req_id

    # If tagged IDs are present in extracted candidates, enforce tagged preserve mode.
    if not effective_tagged_mode and any(c.source_req_id for c in candidates):
        effective_tagged_mode = True
        TAGGED_SOURCE_MODE = True
        _append_log(repo_root, script_name, "INFO tagged_mode_enable_from_candidates=true")

    # Strict tagged-mode policy: when source is tagged, keep only candidates that
    # carry a source requirement ID. This prevents fallback generated IDs from
    # contaminating tagged-source outputs.
    if effective_tagged_mode:
        before = len(candidates)
        candidates = [
            c
            for c in candidates
            if c.source_req_id
            or c.derivation_kind in {
                "architecture_function",
                "architecture_capability",
                "power_management_concept",
            }
        ]
        dropped = before - len(candidates)
        if dropped > 0:
            _append_log(repo_root, script_name, f"INFO tagged_mode_drop_untagged={dropped}")

    before_table_filter = len(candidates)
    candidates = [c for c in candidates if not _is_non_requirement_table_candidate(c)]
    dropped_table_candidates = before_table_filter - len(candidates)
    if dropped_table_candidates > 0:
        _append_log(repo_root, script_name, f"INFO drop_non_requirement_table_candidates={dropped_table_candidates}")

    deduped: List[Candidate] = []
    by_source_req_id: Dict[str, Candidate] = {}
    conflicting_source_ids: set[str] = set()
    source_id_occurrences: Dict[str, List[Candidate]] = {}
    seen_statement_keys: set[str] = set()
    for candidate in candidates:
        if candidate.source_req_id:
            key = candidate.source_req_id.upper()
            source_id_occurrences.setdefault(key, []).append(candidate)
            existing = by_source_req_id.get(key)
            if existing is None:
                by_source_req_id[key] = candidate
            else:
                existing_statement = re.sub(r"\s+", " ", _clean_statement(existing.statement).lower())
                candidate_statement = re.sub(r"\s+", " ", _clean_statement(candidate.statement).lower())
                if existing_statement != candidate_statement:
                    conflicting_source_ids.add(key)
                by_source_req_id[key] = _prefer_better_candidate(existing, candidate)
            continue

        statement_key = re.sub(r"\s+", " ", _clean_statement(candidate.statement).lower())
        if statement_key in seen_statement_keys:
            continue
        seen_statement_keys.add(statement_key)
        deduped.append(candidate)

    duplicate_report_path = Path(args.duplicate_report)
    if not duplicate_report_path.is_absolute():
        duplicate_report_path = (repo_root / duplicate_report_path).resolve()
    duplicate_report_path.parent.mkdir(parents=True, exist_ok=True)
    duplicate_rows = []
    conflicting_definition_ids: set[str] = set()
    for source_id, occurrences in sorted(source_id_occurrences.items()):
        if len(occurrences) < 2:
            continue
        statements = {
            re.sub(r"\s+", " ", _clean_statement(item.statement)).strip()
            for item in occurrences
        }
        meaningful_statements = {
            re.sub(r"\s+", " ", re.sub(r"\[(?:Vpriority[^]]*|End)\]", "", statement, flags=re.IGNORECASE)).strip()
            for statement in statements
        }
        meaningful_statements = {
            statement for statement in meaningful_statements
            if len(statement) >= 24 and re.search(r"\b(?:shall|must|is required|needs? to)\b", statement, flags=re.IGNORECASE)
        }
        definitions = [
            item
            for item in occurrences
            if re.search(r"\bRequirement\s*:", item.statement or "", flags=re.IGNORECASE)
        ]
        definition_statements = {
            re.sub(r"\s+", " ", _clean_statement(item.statement)).strip()
            for item in definitions
        }
        has_conflicting_definitions = len(meaningful_statements) > 1
        if has_conflicting_definitions:
            conflicting_definition_ids.add(source_id)
        if not has_conflicting_definitions:
            continue
        sources = sorted({(item.source or "").strip() for item in occurrences if item.source})
        duplicate_rows.append(
            [
                source_id,
                str(len(occurrences)),
                "conflicting_definitions",
                " | ".join(sources),
                " || ".join(sorted(statements)),
            ]
        )
    with duplicate_report_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source_req_id", "occurrence_count", "status", "source_locations", "statements"])
        writer.writerows(duplicate_rows)

    if duplicate_rows:
        duplicate_ids = ", ".join(row[0] for row in duplicate_rows)
        conflict_text = ", ".join(sorted(conflicting_definition_ids))
        print(
            "Stage 1 generation: STOP (duplicate source requirement IDs: "
            + duplicate_ids
            + ("; conflicting statements: " + conflict_text if conflict_text else "")
            + ")"
        )
        print(
            "User action required: resolve source requirement ID uniqueness, then rerun Stage 1. "
            f"See {duplicate_report_path.as_posix()}"
        )
        _append_log(repo_root, script_name, f"STOP duplicate_source_req_ids={duplicate_ids}")
        return 1

    deduped.extend(by_source_req_id.values())
    tagged_candidate_count = sum(1 for c in deduped if c.source_req_id)

    records_by_id: Dict[str, Dict[str, str]] = {}
    counters = {"System": 0, "Analog": 0, "Digital": 0}
    for c in deduped:
        routing_text = " ".join([c.statement, c.source, c.source_section_owner or ""]).lower()
        is_pmu_clock_reset = (
            "pmu" in routing_text
            and any(term in routing_text for term in ("clock", "clk", "reset", "resetn", "rst_n", "por"))
        )
        if is_pmu_clock_reset:
            c.category = "Digital"
        counters[c.category] += 1
        requirement_type = _detect_requirement_type(c.statement)
        content_class = _detect_content_class(requirement_type)
        generated_id_core = f"{_category_prefix(c.category)}-RQ-{counters[c.category]:03d}"
        id_prefix = _id_scheme_prefix(content_class)
        generated_id = f"{id_prefix}{generated_id_core}"

        # ID policy:
        # - Tagged source mode: preserve original requirement ID as-is.
        # - Non-tagged mode: apply standard generated/prefixed IDs.
        is_tagged_architecture = effective_tagged_mode and not c.source_req_id and c.derivation_kind in {
            "architecture_function",
            "architecture_capability",
            "power_management_concept",
        }
        if is_tagged_architecture:
            rid = generated_id
            id_policy = "tagged_architecture"
        elif effective_tagged_mode and c.source_req_id:
            rid = c.source_req_id
            id_policy = "tagged_preserve"
        else:
            rid = generated_id if not c.source_req_id else f"{id_prefix}{c.source_req_id}"
            id_policy = "generated_standard"
        note = c.note
        if c.source_req_id:
            if effective_tagged_mode:
                note += f" | source_req_id={c.source_req_id} | id_policy=preserve_tagged_source_id"
            else:
                note += f" | source_req_id={c.source_req_id} | generated_id={generated_id} | category_id_core={generated_id_core}"
        record = {
            "id": rid,
            "source_req_id": c.source_req_id or "",
            "covered_source_req_id": c.covered_source_req_id or "",
            "id_policy": id_policy,
            "requirement_statement": c.statement,
            "category": c.category,
            "source": c.source,
            "source_section_owner": c.source_section_owner or "",
            "derivation_kind": c.derivation_kind,
            "evidence_type": c.evidence_type,
            "notes": note,
            "rationale": _build_rationale(c, requirement_type),
            "content_class": content_class,
            "test_trace_required": _test_trace_required(content_class),
            "requirement_type": requirement_type,
            "operating_mode": _detect_operating_mode(c.statement),
            "parameter_signal_register": _detect_parameter_signal_register(c.statement),
            "value_range_condition": _detect_value_range_condition(c.statement),
        }
        existing = records_by_id.get(rid)
        if existing is None:
            records_by_id[rid] = record
            continue
        existing_score = len(existing["requirement_statement"]) * (0.4 + _text_quality_score(existing["requirement_statement"]))
        record_score = len(record["requirement_statement"]) * (0.4 + _text_quality_score(record["requirement_statement"]))
        if record_score > existing_score:
            records_by_id[rid] = record

    records = list(records_by_id.values())

    raw_path = Path(args.raw)
    if not raw_path.is_absolute():
        raw_path = (repo_root / raw_path).resolve()

    summary_csv_path = Path(args.summary_csv)
    if not summary_csv_path.is_absolute():
        summary_csv_path = (repo_root / summary_csv_path).resolve()

    summary_md_path = Path(args.summary_md)
    if not summary_md_path.is_absolute():
        summary_md_path = (repo_root / summary_md_path).resolve()

    report_path = Path(args.stage_report)
    if not report_path.is_absolute():
        report_path = (repo_root / report_path).resolve()

    _write_summary_csv(summary_csv_path, records)
    _write_raw_md(raw_path, records)
    _write_summary_md(summary_md_path, records)
    _write_stage01_report(report_path, source_spec, records, effective_tagged_mode)
    table_review_path = Path(args.table_review_report)
    if not table_review_path.is_absolute():
        table_review_path = (repo_root / table_review_path).resolve()
    table_review_request_path = Path(args.table_review_request)
    if not table_review_request_path.is_absolute():
        table_review_request_path = (repo_root / table_review_request_path).resolve()
    manual_review_count = _write_table_row_review(table_review_path, table_review_request_path, records)

    generated_in_tagged_mode = sum(
        1 for r in records if (r.get("id_policy") or "") == "generated_standard"
    )
    if effective_tagged_mode and generated_in_tagged_mode > 0:
        print("Stage1 generation: FAIL")
        print("- Reason: strict tagged mode violated (generated_standard rows present)")
        print(f"- generated_standard rows: {generated_in_tagged_mode}")
        print(f"- Output CSV: {summary_csv_path}")
        _append_log(
            repo_root,
            script_name,
            f"FAIL strict_tagged_mode generated_standard_rows={generated_in_tagged_mode}",
        )
        return 1

    status = "PASS" if len(records) >= args.min_target else "WARN"
    print(f"Stage1 generation: {status}")
    print(f"- Source specification: {source_spec}")
    print(f"- Tagged source mode: {'ON' if effective_tagged_mode else 'OFF'}")
    print(f"- Requirements with source_req_id: {tagged_candidate_count}")
    print(f"- Requirements extracted: {len(records)}")
    print(f"- Output CSV: {summary_csv_path}")
    print(f"- Output MD: {summary_md_path}")
    print(f"- Raw output: {raw_path}")
    print(f"- Stage report: {report_path}")
    print(f"- Table-row review report: {table_review_path}")
    print(f"- Table-row review request: {table_review_request_path}")

    if manual_review_count:
        print("Stage1 generation: STOP (manual table-row review required)")
        print(f"- Review: {table_review_request_path}")
        _append_log(repo_root, script_name, f"STOP manual_table_review={manual_review_count}")
        return 2

    _append_log(
        repo_root,
        script_name,
        f"{status} source_spec={source_spec} requirements={len(records)} min_target={args.min_target}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
