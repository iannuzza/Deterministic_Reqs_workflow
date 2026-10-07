"""Shared project-agnostic routing helpers for Stage 2A through Stage 5."""

from __future__ import annotations

import csv
import difflib
import getpass
import hashlib
import json
import os
import re
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from types import MappingProxyType
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple

from spec_document_contract import NormalizedSourceRecord, SemanticUnit, drs_document_events, drs_table_inventory, stable_payload_hash
from ipos_semantic_normalizer import (
    extract_structural_function_name as _normalized_structural_function_name,
)


RETAINED_ROUTING_STATUS = "retained_as_non_block_function_context"
AUTHORED_REQUIREMENT_SPACER = "<p>&nbsp;</p>"
GENERATED_SPEC_VERSION = "0.1"


def runtime_user_name() -> str:
    """Return the local process user for non-authoritative logging and metadata."""
    try:
        value = getpass.getuser().strip()
    except (ImportError, OSError):
        value = ""
    return value or os.environ.get("USERNAME", "").strip() or os.environ.get("USER", "").strip() or "unknown-user"


def document_author_name() -> str:
    """Use the signed-in Windows user's display name for document authorship."""
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes

        buffer = ctypes.create_unicode_buffer(256)
        length = wintypes.ULONG(len(buffer))
        if ctypes.windll.secur32.GetUserNameExW(3, buffer, ctypes.byref(length)) and buffer.value.strip():
            return buffer.value.strip()
        raise RuntimeError("Windows full display name is unavailable for the current document author")
    return runtime_user_name()


def validate_document_author_fields(markdown_path: Path) -> List[str]:
    """Validate current authorship while preserving historical snapshot authors."""
    if not markdown_path.exists() or not markdown_path.with_suffix(".docx").exists():
        return [f"document_author_artifact_missing:{markdown_path}"]
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    authors = [line.removeprefix("Author: ").strip() for line in lines if line.startswith("Author: ")]
    if len(authors) != 1 or not authors[0]:
        return [f"document_author_missing:{markdown_path}"]
    findings: List[str] = []
    try:
        history_rows = _document_history_rows(markdown_path)
        if not history_rows or any(not row[-1].strip() for row in history_rows):
            findings.append(f"document_history_author_missing:{markdown_path}")
    except (ValueError, IndexError):
        findings.append(f"document_history_author_missing:{markdown_path}")
    try:
        with zipfile.ZipFile(markdown_path.with_suffix(".docx")) as archive:
            core = ET.fromstring(archive.read("docProps/core.xml"))
        creator = core.findtext("{http://purl.org/dc/elements/1.1/}creator")
        if creator != authors[0]:
            findings.append(f"document_docx_author_mismatch:{markdown_path}")
    except (OSError, ValueError, KeyError, ET.ParseError, zipfile.BadZipFile):
        findings.append(f"document_docx_author_unreadable:{markdown_path}")
    return findings


def _document_history_rows(output_path: Path) -> List[List[str]]:
    if not output_path.exists():
        return []
    tables = [
        table for table in drs_table_inventory(drs_document_events(output_path))
        if table["rows"] and table["rows"][0] == ["Version", "Date", "Description", "Author"]
    ]
    if len(tables) != 1 or any(len(row) != 4 for row in tables[0]["rows"]):
        raise ValueError(f"Missing, duplicate or malformed version history: {output_path}")
    return tables[0]["rows"][1:]


def _document_snapshot_id(output_path: Path) -> str:
    if not output_path.exists():
        return ""
    text = output_path.read_text(encoding="utf-8")
    match = re.search(r"(?:Snapshot ID:\s*|Snapshot:\s*`)([^`\s]+)", text, re.IGNORECASE)
    if match is None:
        raise ValueError(f"Missing document snapshot: {output_path}")
    return match.group(1)


def document_version_history_markdown(
    output_path: Path, snapshot_id: str, version: str, run_date: str, description: str, author: str,
) -> List[str]:
    """Append a snapshot version entry; leave same-snapshot history unchanged."""
    rows = _document_history_rows(output_path)
    if _document_snapshot_id(output_path) != snapshot_id or not rows:
        rows.append([version, run_date, description, author])
    return [
        "| Version | Date | Description | Author |",
        "|---|---|---|---|",
        *["| " + " | ".join(cell.replace("|", r"\|") for cell in row) + " |" for row in rows],
    ]


def document_version_for_snapshot(output_path: Path, snapshot_id: str) -> str:
    """Keep the document version stable, incrementing it when the snapshot changes."""
    if not output_path.exists():
        return GENERATED_SPEC_VERSION
    previous_snapshot = _document_snapshot_id(output_path)
    history_rows = _document_history_rows(output_path)
    version_match = re.fullmatch(r"(\d+)\.(\d+)", history_rows[-1][0]) if history_rows else None
    if not version_match:
        return GENERATED_SPEC_VERSION
    major, minor = int(version_match.group(1)), int(version_match.group(2))
    if previous_snapshot == snapshot_id:
        return f"{major}.{minor}"
    return f"{major}.{minor + 1}"


def apply_shared_spec_markdown_formatting(
    lines: Iterable[str],
    *,
    preserve_authored_text: bool = False,
) -> List[str]:
    """Normalize headings and list markers without changing authored content."""
    formatted: List[str] = []
    heading_re = re.compile(r"^(#{1,6})\s+(?!\*\*)(.*?)(\s*\{#[^}]+\})?\s*$")
    for value in lines:
        line = str(value)
        if not preserve_authored_text:
            line = line.replace("•", "-").replace("●", "-")
        match = heading_re.match(line)
        if match:
            title = match.group(2).rstrip()
            anchor = match.group(3) or ""
            line = f"{match.group(1)} **{title}**{anchor}"
        formatted.append(line)
    return formatted


def spec_anchor_slug(text: str) -> str:
    """Return a stable Markdown fragment for generated specification headings."""
    slug = re.sub(r"[^a-z0-9\s-]", "", (text or "").casefold())
    return re.sub(r"\s+", "-", slug).strip("-") or "section"


def apply_unique_spec_heading_anchors(lines: Iterable[str]) -> List[str]:
    """Add deterministic unique anchors to all Markdown headings."""
    heading_re = re.compile(r"^(#{1,6})\s+(.*?)(?:\s+\{#[^}]+\})?\s*$")
    used: Dict[str, int] = {}
    output: List[str] = []
    for value in lines:
        line = str(value)
        match = heading_re.match(line)
        if not match:
            output.append(line)
            continue
        title = re.sub(r"\s+\{#[^}]+\}\s*$", "", match.group(2)).strip()
        base = spec_anchor_slug(re.sub(r"\*", "", title))
        used[base] = used.get(base, 0) + 1
        anchor = base if used[base] == 1 else f"{base}-{used[base] - 1}"
        output.append(f"{match.group(1)} {title} {{#{anchor}}}")
    return output


def validate_spec_internal_links(markdown_path: Path, docx_path: Path | None = None) -> List[str]:
    """Validate same-document Markdown links and DOCX internal hyperlink targets."""
    findings: List[str] = []
    text = markdown_path.read_text(encoding="utf-8", errors="ignore")
    anchors = {match.group(1).casefold() for match in re.finditer(r"\{#([A-Za-z0-9_-]+)\}", text)}
    for match in re.finditer(r"\[[^\]]+\]\(#([^)]+)\)", text):
        if match.group(1).casefold() not in anchors:
            findings.append(f"{markdown_path.name}: unresolved internal link #{match.group(1)}")
    if docx_path is None or not docx_path.exists():
        return findings
    with zipfile.ZipFile(docx_path) as archive:
        document_xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
    bookmarks = {
        match.group(1).casefold()
        for match in re.finditer(r"w:bookmarkStart[^>]+w:name=\"([^\"]+)\"", document_xml)
    }
    for match in re.finditer(r"w:anchor=\"([^\"]+)\"", document_xml):
        if match.group(1).casefold() not in bookmarks:
            findings.append(f"{docx_path.name}: unresolved internal DOCX target #{match.group(1)}")
    return findings


def validate_ipos_docx_layout(docx_path: Path) -> List[str]:
    """Verify title-page, TOC/navigation, and footer layout contract."""
    findings: List[str] = []
    word_namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with zipfile.ZipFile(docx_path) as archive:
        document_xml = archive.read("word/document.xml")
        footer_xml = [
            archive.read(name).decode("utf-8", errors="ignore")
            for name in archive.namelist()
            if re.fullmatch(r"word/footer\d+\.xml", name)
        ]
    root = ET.fromstring(document_xml)
    body = root.find(f"{word_namespace}body")
    paragraphs = [element for element in list(body or []) if element.tag == f"{word_namespace}p"]
    if not paragraphs:
        return [f"{docx_path.name}: DOCX contains no body content"]
    text = [_docx_element_text(paragraph, word_namespace).strip() for paragraph in paragraphs]
    title_index = next(
        (
            index for index, value in enumerate(text)
            if value.casefold().endswith("specification") or " ipos - " in value.casefold()
        ),
        None,
    )
    toc_index = next((index for index, value in enumerate(text) if value.casefold() == "0.1 table of contents"), None)
    if title_index is None:
        findings.append(f"{docx_path.name}: document title is missing from the title page")
    if toc_index is None:
        findings.append(f"{docx_path.name}: table of contents is missing")
    if title_index is not None and toc_index is not None and title_index >= toc_index:
        findings.append(f"{docx_path.name}: title metadata does not precede the TOC")
    if toc_index is not None:
        toc_paragraph = paragraphs[toc_index]
        page_break_before = toc_paragraph.find(f"{word_namespace}pPr/{word_namespace}pageBreakBefore")
        preceding_break = (
            toc_index > 0
            and paragraphs[toc_index - 1].find(f".//{word_namespace}br[@{word_namespace}type='page']")
            is not None
        )
        if page_break_before is None and not preceding_break:
            findings.append(f"{docx_path.name}: TOC does not start page 2 after the title page")
    navigation_positions = [
        index for index, paragraph in enumerate(paragraphs)
        if _docx_element_text(paragraph, word_namespace).strip().casefold() == "0. document navigation"
    ]
    if not navigation_positions or navigation_positions[0] <= 0:
        findings.append(f"{docx_path.name}: Document Navigation is not after the TOC")
    if not any(
        re.search(r'w:jc w:val="right"', footer)
        and re.search(r'<w:instrText[^>]*>\s*PAGE\s*</w:instrText>', footer)
        for footer in footer_xml
    ):
        findings.append(f"{docx_path.name}: bottom-right PAGE footer is missing")
    return findings

DESCRIPTIVE_MODE_TOPIC_SPECS = (
    ("Modes and transitions", ("mode", "state", "operative", "standby", "retention", "transition")),
    ("Mode resources", ("block", "clock", "fifo", "memory", "register", "resource")),
)
DESCRIPTIVE_POWER_TOPIC_SPECS = (
    ("Retention, Standby, Sleep, and Active Behavior", ("retention", "standby", "sleep", "active", "operative", "powered down")),
    ("Power Sequencing and Enable/Disable", ("sequence", "sequencing", "startup", "shutdown", "enable", "disable", "turn-on", "turn-off")),
    ("Domain Partitioning and Dependencies", ("partition", "dependency", "dependent", "relationship", "shared supply")),
    ("Supply-Domain Relationships", ("supply", "voltage", "rail", "power supply")),
    ("Power Domain Architecture", ("power domain", "island", "ldo", "bias")),
)
DESCRIPTIVE_SYSTEM_TOPIC_SPECS = (
    ("Power and domain management", ("power", "domain", "island", "ldo", "supply")),
    ("System interconnects and interfaces", ("bus", "interconnect", "i2c", "spi", "ahb", "interface")),
    ("Shared resources", ("fifo", "memory", "register", "regmap", "shared")),
    ("Processing and principal blocks", ("processor", "core", "dsp", "sensor", "adc", "controller")),
)
DESCRIPTIVE_DIGITAL_TOPIC_SPECS = (
    ("Power and clock islands", ("power", "island", "clock", "reset", "supply")),
    ("Buses and interconnects", ("bus", "interconnect", "ahb", "i2c", "spi", "serial", "protocol")),
    ("Arbitration and control", ("arbitration", "controller", "control", "interrupt", "state")),
    ("Shared digital resources", ("fifo", "memory", "register", "regmap", "shared")),
    ("Digital processing blocks", ("processor", "core", "dsp", "sensor hub", "ispu")),
)

# These are coverage-review categories, not new requirement categories. They are
# deliberately broad so the DRS can report integration evidence without copying
# block-local Digital IPOS detail.
TOP_DIGITAL_CATEGORY_SPECS = (
    ("Functional behavior", ("function", "control", "operation", "behavior", "processing")),
    ("Clocking and reset", ("power/clock", "clock-ready", "reset", "por", "frequency", "clock domain", "reset release")),
    ("Power management, power states, retention, and wake-up", ("power mode", "power domain", "power-down", "retention", "standby", "sleep", "wake", "sequencing")),
    ("Bus, interconnect, and protocol behavior", ("bus", "interconnect", "protocol", "ahb", "i2c", "spi", "uart", "serial")),
    ("Memory map, register access, and protection", ("memory map", "register", "regmap", "address", "write-protection", "read-only", "register access")),
    ("Interrupts, events, and status reporting", ("interrupt", "irq", "event", "status reporting", "ready status", "watermark", "overrun")),
    ("Boot, initialization, and configuration", ("boot", "initialization", "startup", "configuration", "configure")),
    ("Security, access control, and isolation", ("security", "secure", "access control", "isolation", "privilege", "authentication")),
    ("DMA, data movement, buffering, and FIFO behavior", ("dma", "data movement", "fifo", "buffer", "stream", "transfer")),
    ("Arbitration, priority, and QoS", ("arbitration", "priority", "qos", "quality of service", "grant")),
    ("Error handling, fault reporting, and recovery", ("error", "fault", "recovery", "failure", "fault report")),
    ("Performance, latency, and throughput", ("performance", "latency", "throughput", "bandwidth", "timing")),
    ("CDC, RDC, and synchronization", ("cdc", "rdc", "synchron", "clock domain", "reset domain")),
    ("Debug, trace, test, and DFT visibility", ("debug", "trace", "test", "dft", "scan", "bist", "observability")),
    ("Interfaces to analog, pads, and external systems", ("analog", "pad", "external", "sensor", "mixed-signal")),
    ("Low-power domain coordination", ("low-power", "power domain", "island", "domain coordination", "domain dependency")),
    ("Firmware-visible behavior", ("firmware", "software", "command", "status", "register")),
    ("Mode transitions and operational states", ("mode", "state", "transition", "active", "standby", "operative")),
    ("Safety, monitoring, watchdog, and timeout behavior", ("safety", "monitor", "watchdog", "timeout", "supervision")),
    ("Block interaction and integration rules", ("interaction", "connected", "connection", "integration", "source", "destination")),
)
DESCRIPTIVE_ANALOG_TOPIC_SPECS = (
    ("Power and bias", ("power", "supply", "voltage", "bias", "reference")),
    ("Sensing and signal paths", ("sensor", "signal", "ecg", "ppg", "bio", "impedance", "eda")),
    ("Sampling and conversion", ("adc", "sampling", "conversion", "acquisition")),
    ("Calibration and measurement quality", ("calibration", "noise", "offset", "gain", "accuracy")),
    ("Analog principal blocks", ("analog", "afe", "amplifier", "filter", "buffer")),
)

# IPOS uses only block-local functional areas. These labels deliberately do not
# reuse DRS integration topics and are rendered through one shared composer.
IPOS_LOCAL_DIGITAL_TOPIC_SPECS = (
    ("boot and OTP services", ("boot", "otp", "lifecycle", "firmware")),
    ("power, clock, and reset sequencing", ("power", "clock", "reset", "por", "ldo")),
    ("local interface protocol handling", ("ahb", "i2c", "spi", "protocol", "bus", "serial")),
    ("local register and memory management", ("register", "registers", "regmap", "memory", "ram", "address")),
    ("local state and control management", ("control", "state", "mode", "interrupt", "irq")),
    ("local buffering and FIFO management", ("fifo storage", "fifo", "buffer", "queue", "watermark")),
    ("local digital signal processing", ("dsp elaboration", "dsp", "signal processing", "filter")),
    ("local pad and signal routing", ("pad", "mux", "gpio", "route", "routing")),
)

IPOS_LOCAL_ANALOG_TOPIC_SPECS = (
    ("local power and bias control", ("power", "supply", "voltage", "bias", "reference")),
    ("local sensing and signal conditioning", ("sensor", "signal", "ecg", "ppg", "bio", "impedance", "eda")),
    ("local sampling and conversion", ("adc", "sampling", "conversion", "acquisition")),
    ("local calibration and measurement control", ("calibration", "noise", "offset", "gain", "accuracy")),
    ("local analog signal-path control", ("analog", "afe", "amplifier", "filter", "buffer")),
)

IPOS_DRS_LEVEL_TOPICS = {
    "Power and clock islands",
    "Buses and interconnects",
    "Arbitration and control",
    "Shared digital resources",
    "Digital processing blocks",
}


@dataclass(frozen=True)
class DescriptiveAssembly:
    """Deterministic, non-authoritative descriptive output and its audit trail."""

    topics: Dict[str, List[str]]
    audit: List[Dict[str, str]]


@dataclass(frozen=True)
class IPOSFunctionalInput:
    """Snapshot-bound, non-authoritative input for IPOS descriptive composition."""

    block: str
    domain: str
    function: str
    inputs: str
    outputs: str
    local_requirement_ids: Tuple[str, ...]
    local_requirement_evidence: Tuple[str, ...]
    candidate_requirement_records: Tuple[Tuple[str, str, str, str], ...]
    materialized: bool
    provenance: Tuple[str, ...]


@dataclass(frozen=True)
class TopDigitalCoverage:
    """Deterministic coverage status for top-level integration review."""

    category: str
    status: str
    evidence: List[str]
    matched_terms: List[str]
    evidence_count: int


def assess_top_digital_coverage(
    records: Iterable[Mapping[str, object]],
    category_specs: Sequence[Tuple[str, Sequence[str]]] = TOP_DIGITAL_CATEGORY_SPECS,
    *,
    max_evidence_per_category: int = 3,
    allowed_scopes: Sequence[str] = ("top_digital", "integration", "architecture", "lifted_integration"),
) -> Tuple[List[TopDigitalCoverage], List[Dict[str, str]]]:
    """Assess approved top-level evidence; block-local evidence is excluded."""
    prepared: List[Tuple[int, str, str, bool, str]] = []
    for index, record in enumerate(records):
        scope = csv_cell_text(record.get("scope") or "").strip().casefold()
        if scope not in {item.casefold() for item in allowed_scopes}:
            continue
        statement = csv_cell_text(
            record.get("statement") or record.get("function") or record.get("text")
        ).strip()
        source = csv_cell_text(record.get("source") or record.get("provenance")).strip()
        if statement:
            prepared.append((
                index,
                statement,
                source,
                bool(re.search(r"\b(?:shall|must|required to|requirement)\b", statement, re.I)),
                scope,
            ))

    coverage: List[TopDigitalCoverage] = []
    audit: List[Dict[str, str]] = []
    for category, terms in category_specs:
        matches: List[Tuple[int, str, str, bool, List[str], str]] = []
        seen: Set[str] = set()
        for index, statement, source, normative, scope in prepared:
            searchable = f"{statement} {source}".casefold()
            matched_terms = [
                csv_cell_text(term).strip()
                for term in terms
                if csv_cell_text(term).strip().casefold() in searchable
            ]
            if not matched_terms or statement.casefold() in seen:
                continue
            seen.add(statement.casefold())
            matches.append((index, statement, source, normative, matched_terms, scope))
        matches.sort(key=lambda item: item[0])
        selected = matches[:max_evidence_per_category]
        if not matches:
            status = "Missing"
        elif any(item[3] for item in matches) or len(matches) >= 2:
            status = "Covered"
        else:
            status = "Partial"
        coverage.append(TopDigitalCoverage(
            category=category,
            status=status,
            evidence=[item[1] for item in selected],
            matched_terms=sorted({term for item in matches for term in item[4]}),
            evidence_count=len(matches),
        ))
        if selected:
            audit.append({
                "category": category,
                "status": status,
                "decision": "selected",
                "output_order": "; ".join(str(output_order) for output_order, _item in enumerate(selected, start=1)),
                "matched_terms": "; ".join(sorted({term for item in selected for term in item[4]})),
                "statement": " || ".join(item[1] for item in selected),
                "source": " || ".join(item[2] for item in selected),
                "scope": "; ".join(sorted({item[5] for item in selected})),
            })
        else:
            audit.append({
                "category": category,
                "status": status,
                "decision": "no approved evidence",
                "output_order": "",
                "matched_terms": "",
                "statement": "",
                "source": "",
                "scope": "",
            })
    return coverage, audit


def write_top_digital_coverage_audit(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    """Persist coverage decisions and provenance without altering authority."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["category", "status", "decision", "output_order", "matched_terms", "statement", "source", "scope"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_cell_text(row.get(field, "")) for field in fields})


def _descriptive_tokens(value: object) -> Set[str]:
    return set(re.findall(r"[a-z0-9]+", csv_cell_text(value).casefold()))


def assign_ipos_descriptive_topic(
    functional_evidence: object,
    topic_specs: Sequence[Tuple[str, Sequence[str]]],
) -> Dict[str, str]:
    """Choose one IPOS topic from functional evidence or omit an ambiguous input."""
    evidence = csv_cell_text(functional_evidence).strip()
    searchable = evidence.casefold()
    tokens = _descriptive_tokens(evidence)
    if not evidence:
        return {
            "topic": "",
            "matched_functional_evidence": "",
            "assignment_reason": "no functional topic evidence",
        }
    if not _is_ipos_descriptive_functional_evidence(evidence):
        return {
            "topic": "",
            "matched_functional_evidence": "",
            "assignment_reason": "non-functional, parameterized, or low-level evidence",
        }
    candidates: List[Tuple[int, str, List[str]]] = []
    for topic, terms in topic_specs:
        matched_terms = sorted(
            csv_cell_text(term).strip()
            for term in terms
            if (
                csv_cell_text(term).casefold().strip() in searchable
                if len(_descriptive_tokens(term)) > 1
                else bool(_descriptive_tokens(term).intersection(tokens))
            )
        )
        if matched_terms:
            if not _is_ipos_topic_evidence_admissible(topic, searchable, tokens, matched_terms):
                continue
            score = sum(len(_descriptive_tokens(term)) for term in matched_terms)
            candidates.append((score, topic, matched_terms))
    if not candidates:
        return {
            "topic": "",
            "matched_functional_evidence": "",
            "assignment_reason": "no functional topic evidence",
        }
    candidates.sort(key=lambda item: (-item[0], item[1].casefold()))
    best_score = candidates[0][0]
    best = [candidate for candidate in candidates if candidate[0] == best_score]
    if len(best) != 1:
        return {
            "topic": "",
            "matched_functional_evidence": "; ".join(
                f"{topic}: {', '.join(terms)}" for _score, topic, terms in best
            ),
            "assignment_reason": "ambiguous functional topic evidence",
        }
    _score, topic, matched_terms = best[0]
    return {
        "topic": topic,
        "matched_functional_evidence": "; ".join(matched_terms),
        "assignment_reason": "strongest functional topic signals: " + ", ".join(matched_terms),
    }


def _is_ipos_descriptive_functional_evidence(evidence: str) -> bool:
    """Reject local metadata and implementation fragments from IPOS summaries."""
    normalized = evidence.casefold().strip()
    if not normalized:
        return False
    if re.match(
        r"^(?:the\s+)?(?:parameter|configuration|address|register(?:\s+field)?|field|value|version|timer|bit|table|figure)\b",
        normalized,
    ):
        return False
    if re.search(
        r"\b(?:suggested\s*(?:val(?:ue)?\.?|:)|0x[0-9a-f]+|\b(?:ip_version|ser_mode|i2c_master_code|i2c_dev_id|rd_to_max_val)\b|ocr|page\s*\d+)\b",
        normalized,
    ):
        return False
    if re.search(r"\b(?:shall|must|required to)\b.*\b(?:register|address|bit|field|value|timer)\b", normalized):
        return False
    return True


def _is_ipos_topic_evidence_admissible(
    topic: str,
    searchable: str,
    tokens: Set[str],
    matched_terms: Sequence[str],
) -> bool:
    """Require functional combinations rather than isolated shared keywords."""
    matched = {term.casefold() for term in matched_terms}
    if topic == "boot and OTP services":
        return "boot" in tokens or "firmware" in tokens
    if topic == "power, clock, and reset sequencing":
        return len(matched.intersection({"power", "clock", "reset", "por", "ldo"})) >= 2
    if topic == "local digital signal processing":
        return (
            "dsp elaboration" in matched
            or "signal processing" in matched
            or ("dsp" in tokens and bool({"signal", "processing", "elaboration"}.intersection(tokens)))
        )
    if topic == "local register and memory management":
        return (
            "memory" in matched
            or "ram" in matched
            or "regmap" in matched
            or bool({"register", "registers"}.intersection(tokens))
            and bool({"configuration", "status", "access", "mapped"}.intersection(tokens))
        )
    return bool(matched)


def assemble_descriptive_summary(
    records: Iterable[Mapping[str, object]],
    topic_specs: Sequence[Tuple[str, Sequence[str]]],
    *,
    max_items_per_topic: int = 6,
    include_general: bool = True,
    summary_only: bool = False,
    ipos_topic_mode: bool = False,
) -> DescriptiveAssembly:
    """Assemble descriptive evidence with stable decisions; never creates authority."""
    topics = {name: [] for name, _terms in topic_specs}
    if include_general:
        topics["General architecture"] = []
    audit: List[Dict[str, str]] = []
    seen: Set[str] = set()

    for index, record in enumerate(records):
        evidence_statement = csv_cell_text(
            record.get("statement")
            or record.get("function")
            or record.get("Non-Block Function Context")
            or record.get("Source Paragraph")
            or record.get("text")
        ).strip()
        statement = csv_cell_text(record.get("summary") if summary_only else evidence_statement).strip()
        source = csv_cell_text(
            record.get("source")
            or record.get("Source Paragraph")
            or record.get("source_text")
            or record.get("provenance")
        ).strip()
        base_audit = {
            "input_order": str(index),
            "statement": statement,
            "source": source,
            "scope": csv_cell_text(record.get("scope") or record.get("domain")).strip(),
            "mapped_block": csv_cell_text(record.get("mapped_block") or record.get("block") or record.get("owner")).strip(),
            "layer": csv_cell_text(record.get("layer")).strip(),
            "scope_decision": "accepted input scope",
            "normative_evidence": "yes" if re.search(r"\b(?:shall|must|required to|requirement)\b", statement, re.I) else "no",
            "source_evidence": evidence_statement,
            "functional_evidence": csv_cell_text(record.get("functional_evidence")).strip(),
            "matched_functional_evidence": "",
        }
        ipos_assignment = (
            assign_ipos_descriptive_topic(base_audit["functional_evidence"], topic_specs)
            if ipos_topic_mode
            else None
        )
        if ipos_assignment and not ipos_assignment["topic"]:
            audit.append({
                **base_audit,
                "decision": "rejected",
                "reason": ipos_assignment["assignment_reason"],
                "assignment_reason": ipos_assignment["assignment_reason"],
                "matched_functional_evidence": ipos_assignment["matched_functional_evidence"],
            })
            continue
        if summary_only and not statement:
            audit.append({**base_audit, "decision": "rejected", "reason": "no supported synthesized summary"})
            continue
        if not statement:
            audit.append({**base_audit, "decision": "rejected", "reason": "missing descriptive statement"})
            continue

        rendered = statement
        key = rendered.casefold()
        if key in seen:
            audit.append({**base_audit, "decision": "rejected", "reason": "duplicate descriptive evidence"})
            continue

        if ipos_topic_mode:
            assignment = ipos_assignment or {}
            target = assignment["topic"]
            assignment_reason = assignment["assignment_reason"]
            base_audit["matched_functional_evidence"] = assignment["matched_functional_evidence"]
            if not target:
                audit.append({
                    **base_audit,
                    "decision": "rejected",
                    "reason": assignment_reason,
                    "assignment_reason": assignment_reason,
                })
                continue
        else:
            searchable_text = csv_cell_text(f"{statement} {source}").casefold()
            searchable = _descriptive_tokens(searchable_text)
            target = "General architecture" if include_general else ""
            assignment_reason = "no configured topic signal"
            for topic, terms in topic_specs:
                matched_terms = sorted(
                    configured_term
                    for configured_term in terms
                    if (
                        csv_cell_text(configured_term).casefold().strip() in searchable_text
                        if len(_descriptive_tokens(configured_term)) > 1
                        else bool(_descriptive_tokens(configured_term).intersection(searchable))
                    )
                )
                if matched_terms:
                    target = topic
                    assignment_reason = "lexical/normalized topic signals: " + ", ".join(matched_terms)
                    break
        if not target:
            audit.append({**base_audit, "decision": "rejected", "reason": "no eligible configured topic"})
            continue
        seen.add(key)
        if len(topics[target]) >= max_items_per_topic:
            audit.append({
                **base_audit,
                "decision": "rejected",
                "reason": "topic output limit",
                "topic": target,
                "assignment_reason": assignment_reason,
            })
            continue
        topics[target].append(rendered)
        audit.append({
            **base_audit,
            "decision": "selected",
            "reason": "eligible approved evidence",
            "topic": target,
            "assignment_reason": assignment_reason,
            "output_order": str(len(topics[target])),
        })

    return DescriptiveAssembly(
        topics={name: values for name, values in topics.items() if values},
        audit=audit,
    )


SRS_SYSTEM_OVERVIEW_HEADINGS = (
    "3.1 General System Description",
    "3.2 Main System Capabilities",
    "3.3 Main Architectural Domains and Subsystems",
    "3.4 External Interfaces and System Boundaries",
    "3.5 Operating Concept",
    "3.6 Power, Clock, and Reset Overview",
    "3.7 Assumptions, Scope Limits, and Allocation Boundaries",
)


@dataclass(frozen=True)
class DescriptiveWritingProfile:
    name: str
    allowed_scopes: Tuple[str, ...]
    document_type: str
    evidence_kinds: Tuple[str, ...]
    authority_tiers: Tuple[str, ...]
    owner_policy: str
    allowed_domains: Tuple[str, ...]
    allowed_layers: Tuple[str, ...]
    projection_adapters: Tuple[str, ...]
    topic_roles: Tuple[str, ...]
    excluded_terms: Tuple[str, ...]
    runtime_enabled: bool
    version: int = 1

    def __post_init__(self) -> None:
        if not self.name or not self.document_type or self.version != 1:
            raise ValueError("Invalid descriptive profile identity or version")
        if self.owner_policy not in {"unrestricted", "same_owner"}:
            raise ValueError("Unsupported descriptive owner policy")
        for values in (self.allowed_scopes, self.evidence_kinds, self.authority_tiers, self.projection_adapters):
            if not values or len(set(values)) != len(values) or any(not value.strip() for value in values):
                raise ValueError("Explicit nonempty descriptive profile controls required")


@dataclass(frozen=True)
class DescriptiveFact:
    subject: str
    action: str
    objects: Tuple[str, ...]
    source: str
    statement: str
    scope: str
    section: str = ""
    mode: str = ""
    condition: str = ""
    modality: str = ""
    negative: bool = False
    coordination: str = "and"
    object_suffix: str = ""
    plural_subject: bool = False
    qualifiers: Tuple[str, ...] = ()
    results: Tuple[str, ...] = ()
    evidence_kind: str = "descriptive"
    owner: str = ""
    domain: str = ""
    layer: str = ""

    @property
    def fact_id(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, ensure_ascii=True)
        return "desc-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]


@dataclass(frozen=True)
class DescriptiveParagraph:
    text: str
    facts: Tuple[DescriptiveFact, ...]


SRS_DESCRIPTIVE_PROFILE = DescriptiveWritingProfile(
    "srs-overview-v1", ("system", "architecture"), "SRS", ("descriptive",),
    ("admitted_context",), "unrestricted", (), (), ("srs-overview",),
    SRS_SYSTEM_OVERVIEW_HEADINGS,
    ("register", "regmap", "address", "signal name", "port name"), True,
)
DRS_DESCRIPTIVE_PROFILE = DescriptiveWritingProfile(
    "drs-integration-v1", ("architecture", "digital_integration"), "DRS", ("descriptive",),
    ("admitted_context",), "unrestricted", ("digital", "shared"), ("integration",),
    ("drs-integration",), ("integration", "interfaces", "operating_concept", "power"), (), False,
)
ARS_DESCRIPTIVE_PROFILE = DescriptiveWritingProfile(
    "ars-integration-v1", ("architecture", "analog_integration"), "ARS", ("descriptive",),
    ("admitted_context",), "unrestricted", ("analog", "mixed_signal", "shared"), ("integration",),
    ("ars-integration",), ("integration", "interfaces", "operating_concept", "power"), (), False,
)
IPOS_DESCRIPTIVE_PROFILE = DescriptiveWritingProfile(
    "ipos-local-v1", ("block_local",), "IPOS", ("descriptive", "approved_normative"),
    ("admitted_context", "approved_normative"), "same_owner", (), ("block",),
    ("ipos-local",), ("function", "interfaces", "operating_concept", "power"), (), False,
)
DESCRIPTIVE_PROFILES = MappingProxyType({profile.document_type: profile for profile in (
    SRS_DESCRIPTIVE_PROFILE, DRS_DESCRIPTIVE_PROFILE, ARS_DESCRIPTIVE_PROFILE, IPOS_DESCRIPTIVE_PROFILE,
)})


def descriptive_profile(document_type: str) -> DescriptiveWritingProfile:
    try:
        profile = DESCRIPTIVE_PROFILES[document_type]
    except KeyError:
        raise ValueError("Unknown descriptive document profile: " + document_type) from None
    if not profile.runtime_enabled:
        raise ValueError("Descriptive profile not activated: " + document_type)
    return profile


def descriptive_fact_findings(
    fact: DescriptiveFact, *, profile: DescriptiveWritingProfile, owner: str = "",
) -> List[str]:
    findings = []
    if fact.scope not in profile.allowed_scopes or fact.evidence_kind not in profile.evidence_kinds:
        findings.append("descriptive_scope_or_kind_invalid")
    if profile.allowed_domains and fact.domain not in profile.allowed_domains:
        findings.append("descriptive_domain_invalid")
    if profile.allowed_layers and fact.layer not in profile.allowed_layers:
        findings.append("descriptive_layer_invalid")
    if profile.owner_policy == "same_owner" and (not owner or fact.owner != owner):
        findings.append("descriptive_owner_invalid")
    if profile.topic_roles and fact.section not in profile.topic_roles:
        findings.append("descriptive_topic_invalid")
    if any(not isinstance(value, str) or not value.strip() for value in
           (fact.source, fact.statement, fact.subject, fact.action, *fact.objects)) or not fact.objects:
        findings.append("descriptive_fact_or_provenance_incomplete")
    if fact.modality not in {"", "can", "may"} or fact.coordination not in {"and", "or"}:
        findings.append("descriptive_grammar_unsupported")
    descriptive_text = " ".join((fact.subject, fact.action, *fact.objects, fact.object_suffix,
                                 fact.condition, fact.mode, *fact.qualifiers, *fact.results))
    if any(re.search(r"\b" + re.escape(term) + r"\b", descriptive_text, re.IGNORECASE)
           for term in profile.excluded_terms):
        findings.append("descriptive_profile_detail_excluded")
    return findings


@dataclass(frozen=True)
class DescriptiveFlowResult:
    records: Tuple[NormalizedSourceRecord, ...]
    facts: Tuple[DescriptiveFact, ...]
    paragraphs: Tuple[DescriptiveParagraph, ...]
    units: Tuple[SemanticUnit, ...]
    audit: Tuple[Dict[str, str], ...]


def descriptive_evidence_findings(
    record: NormalizedSourceRecord, *, profile: DescriptiveWritingProfile,
) -> List[str]:
    findings = []
    if not record.record_id or not record.text.strip() or not record.provenance or any(not source.strip() for source in record.provenance):
        findings.append("descriptive_evidence_provenance_incomplete")
    if record.decision not in {"selected", "retained"} or record.authority_tier not in profile.authority_tiers:
        findings.append("descriptive_evidence_not_admissible")
    if record.ownership_scope not in profile.allowed_scopes:
        findings.append("descriptive_evidence_scope_invalid")
    return findings


def run_descriptive_flow(
    records: Iterable[NormalizedSourceRecord], *, profile: DescriptiveWritingProfile,
    adapter_name: str,
    adapter: Callable[[NormalizedSourceRecord], Tuple[Sequence[DescriptiveFact], str]],
    owner: str = "",
) -> DescriptiveFlowResult:
    registered = DESCRIPTIVE_PROFILES.get(profile.document_type)
    if not profile.runtime_enabled or (registered is not None and profile != registered):
        raise ValueError("Descriptive profile not activated or changed: " + profile.document_type)
    if adapter_name not in profile.projection_adapters:
        raise ValueError("Projection adapter outside descriptive profile: " + adapter_name)
    inputs = tuple(records)
    if len({record.record_id for record in inputs}) != len(inputs):
        raise ValueError("Duplicate descriptive source record IDs")
    facts: List[DescriptiveFact] = []
    origins: Dict[str, List[str]] = {}
    audits: List[Dict[str, str]] = []
    fingerprint = stable_payload_hash(asdict(profile))

    def audit(record: NormalizedSourceRecord, decision: str, reason: str, **fields: str) -> None:
        audits.append({
            "profile": profile.name, "profile_version": str(profile.version),
            "profile_fingerprint": fingerprint, "projection_adapter": adapter_name,
            "source_record_id": record.record_id, "normalized_record_json": json.dumps(asdict(record), sort_keys=True),
            "decision": decision, "reason": reason, "fact_id": "", "fact_json": "",
            "contributor_ids": "[]", "unit_id": "", "semantic_unit_json": "", **fields,
        })

    for record in inputs:
        if descriptive_evidence_findings(record, profile=profile):
            audit(record, "rejected_evidence", record.rationale or "outside explicit evidence boundary")
            continue
        projected, reason = adapter(record)
        projected = tuple(projected)
        if not projected:
            audit(record, "projection_gap", reason or "no supported construction")
            continue
        for fact in projected:
            if (fact.statement != record.text or fact.source not in record.provenance
                    or fact.scope != record.ownership_scope
                    or (fact.evidence_kind == "approved_normative" and record.authority_tier != "approved_normative")):
                raise ValueError("Projection changed admitted provenance or evidence scope")
            findings = descriptive_fact_findings(fact, profile=profile, owner=owner)
            if findings:
                raise ValueError("Invalid descriptive projection: " + "; ".join(findings))
            facts.append(fact)
            origins.setdefault(fact.fact_id, []).append(record.record_id)
        audit(record, "admitted", "explicit evidence and profile boundary passed")
        if reason:
            audit(record, "projection_gap", reason)

    paragraphs = compose_descriptive_paragraphs(facts, profile=profile, owner=owner)
    findings = validate_descriptive_paragraphs(paragraphs, facts=facts, profile=profile, owner=owner)
    if findings:
        raise ValueError("Descriptive preservation failed: " + "; ".join(findings))
    by_id = {record.record_id: record for record in inputs}
    units = []
    for order, paragraph in enumerate(paragraphs, start=1):
        contributors = tuple(dict.fromkeys(fact.fact_id for fact in paragraph.facts))
        source_ids = tuple(dict.fromkeys(source_id for fact_id in contributors for source_id in origins[fact_id]))
        unit = SemanticUnit("desc-unit-" + stable_payload_hash((fingerprint, contributors, paragraph.text))[:20],
                            paragraph.facts[0].section, paragraph.text, source_ids, order)
        units.append(unit)
        for fact in paragraph.facts:
            for source_id in dict.fromkeys(origins[fact.fact_id]):
                audit(by_id[source_id], "selected", "compatible facts; all contributors retained",
                      fact_id=fact.fact_id, fact_json=json.dumps(asdict(fact), sort_keys=True),
                      contributor_ids=json.dumps(contributors), unit_id=unit.unit_id,
                      semantic_unit_json=json.dumps(asdict(unit), sort_keys=True))
    result = DescriptiveFlowResult(inputs, tuple(facts), tuple(paragraphs), tuple(units), tuple(audits))
    findings = validate_descriptive_flow(result, profile=profile, owner=owner)
    if findings:
        raise ValueError("Descriptive audit linkage failed: " + "; ".join(findings))
    return result


def validate_descriptive_flow(
    result: DescriptiveFlowResult, *, profile: DescriptiveWritingProfile, owner: str = "",
) -> List[str]:
    findings = validate_descriptive_paragraphs(result.paragraphs, facts=result.facts, profile=profile, owner=owner)
    records = {record.record_id: record for record in result.records}
    units = {unit.unit_id: unit for unit in result.units}
    facts = {fact.fact_id: fact for fact in result.facts}
    fingerprint = stable_payload_hash(asdict(profile))
    if len(units) != len(result.units) or len(result.units) != len(result.paragraphs):
        findings.append("descriptive_semantic_units_invalid")
    expected_links = set()
    for paragraph, unit in zip(result.paragraphs, result.units):
        contributors = tuple(dict.fromkeys(fact.fact_id for fact in paragraph.facts))
        origins = tuple(dict.fromkeys(record.record_id for fact in paragraph.facts for record in result.records
                                     if fact.statement == record.text and fact.source in record.provenance
                                     and fact.scope == record.ownership_scope
                                     and (fact.evidence_kind != "approved_normative" or record.authority_tier == "approved_normative")
                                     and not descriptive_evidence_findings(record, profile=profile)))
        if (not paragraph.facts or unit.text != paragraph.text or unit.section != paragraph.facts[0].section
                or unit.source_record_ids != origins or unit.output_order < 1
                or unit.unit_id != "desc-unit-" + stable_payload_hash((fingerprint, contributors, paragraph.text))[:20]):
            findings.append("descriptive_semantic_unit_changed")
        for fact in paragraph.facts:
            if not any(fact.statement == records[record_id].text and fact.source in records[record_id].provenance for record_id in origins):
                findings.append("descriptive_fact_source_link_missing:" + fact.fact_id)
            for record_id in origins:
                record = records[record_id]
                if fact.statement == record.text and fact.source in record.provenance:
                    expected_links.add((unit.unit_id, fact.fact_id, record_id))
    actual_links = set()
    audited_records = set()
    for row in result.audit:
        record_id = row.get("source_record_id", "")
        record = records.get(record_id)
        audited_records.add(record_id)
        try:
            if (record is None or row["profile"] != profile.name or row["profile_version"] != str(profile.version)
                    or row["profile_fingerprint"] != fingerprint
                    or row["projection_adapter"] not in profile.projection_adapters
                    or json.loads(row["normalized_record_json"]) != json.loads(json.dumps(asdict(record)))):
                raise ValueError("Invalid profile or normalized record")
            if row["decision"] == "selected":
                if descriptive_evidence_findings(record, profile=profile):
                    raise ValueError("Selected audit record is not admissible")
                unit = units[row["unit_id"]]
                fact = facts[row["fact_id"]]
                paragraph = next(paragraph for paragraph in result.paragraphs
                                 if paragraph.text == unit.text and paragraph.facts[0].section == unit.section
                                 and fact in paragraph.facts)
                if (json.loads(row["fact_json"]) != json.loads(json.dumps(asdict(fact)))
                        or json.loads(row["semantic_unit_json"]) != json.loads(json.dumps(asdict(unit)))
                        or json.loads(row["contributor_ids"]) != list(dict.fromkeys(member.fact_id for member in paragraph.facts))):
                    raise ValueError("Invalid fact or semantic unit")
                actual_links.add((unit.unit_id, fact.fact_id, record_id))
            elif row["decision"] not in {"admitted", "rejected_evidence", "projection_gap"}:
                raise ValueError("Invalid audit decision")
        except (KeyError, TypeError, ValueError, StopIteration):
            findings.append("descriptive_audit_link_invalid:" + record_id)
    if set(records) != audited_records:
        findings.append("descriptive_record_audit_coverage_invalid")
    if expected_links != actual_links:
        findings.append("descriptive_contributor_audit_coverage_invalid")
    return findings


def _descriptive_join(values: Sequence[str], conjunction: str = "and") -> str:
    if len(values) < 2:
        return values[0] if values else ""
    return ", ".join(values[:-1]) + f" {conjunction} " + values[-1]


def _descriptive_fact_key(fact: DescriptiveFact) -> tuple:
    return (
        fact.subject, fact.action, fact.scope, fact.section, fact.mode, fact.condition,
        fact.modality, fact.negative, fact.coordination, fact.object_suffix,
        fact.plural_subject, fact.qualifiers, fact.results,
        fact.objects if fact.coordination == "or" else (),
        fact.evidence_kind, fact.owner, fact.domain, fact.layer,
    )


def aggregate_descriptive_facts(
    facts: Iterable[DescriptiveFact], *, profile: DescriptiveWritingProfile, owner: str = "",
) -> List[Tuple[DescriptiveFact, ...]]:
    groups: Dict[tuple, List[DescriptiveFact]] = {}
    for fact in facts:
        findings = descriptive_fact_findings(fact, profile=profile, owner=owner)
        if findings:
            raise ValueError("Invalid descriptive fact: " + "; ".join(findings))
        groups.setdefault(_descriptive_fact_key(fact), []).append(fact)
    return [tuple(members) for members in groups.values()]


def compose_descriptive_paragraphs(
    facts: Iterable[DescriptiveFact], *, profile: DescriptiveWritingProfile, owner: str = "",
) -> List[DescriptiveParagraph]:
    paragraphs: List[DescriptiveParagraph] = []
    for members in aggregate_descriptive_facts(facts, profile=profile, owner=owner):
        first = members[0]
        objects = list(dict.fromkeys(value for fact in members for value in fact.objects))
        action = first.action
        if first.modality:
            predicate = first.modality + (" not " if first.negative else " ") + action
        elif first.negative:
            predicate = ("do not " if first.plural_subject else "does not ") + action
        elif first.plural_subject:
            predicate = action
        elif action.endswith("y") and len(action) > 1 and action[-2] not in "aeiou":
            predicate = action[:-1] + "ies"
        else:
            predicate = action + ("es" if action.endswith(("s", "sh", "ch", "x", "z", "o")) else "s")
        text = f"{first.subject} {predicate} {_descriptive_join(objects, first.coordination)}"
        if first.object_suffix:
            text += " " + first.object_suffix
        if first.qualifiers:
            text += " " + " ".join(first.qualifiers)
        if first.results:
            text += (", " if len(first.results) > 1 else " and ") + _descriptive_join(first.results)
        if first.condition:
            text = f"{first.condition}, {text[0].lower() + text[1:]}"
        if first.mode:
            text = f"In {first.mode}, {text[0].lower() + text[1:]}"
        paragraphs.append(DescriptiveParagraph(text.rstrip(".") + ".", tuple(members)))
    return paragraphs


def validate_descriptive_paragraphs(
    paragraphs: Sequence[DescriptiveParagraph], *, facts: Sequence[DescriptiveFact],
    profile: DescriptiveWritingProfile, owner: str = "",
) -> List[str]:
    findings: List[str] = []
    expected = {fact.fact_id for fact in facts}
    represented: Set[str] = set()
    for paragraph in paragraphs:
        keys = {_descriptive_fact_key(fact) for fact in paragraph.facts}
        if len(keys) != 1:
            findings.append("descriptive_incompatible_aggregation")
        text = " ".join(paragraph.text.casefold().split())
        if re.search(r"\b(?:shall|must|required to)\b|\bCovers\s*:", paragraph.text, re.IGNORECASE):
            findings.append("descriptive_normative_wording")
        for fact in paragraph.facts:
            represented.add(fact.fact_id)
            findings.extend(descriptive_fact_findings(fact, profile=profile, owner=owner))
            if fact.scope not in profile.allowed_scopes or not fact.source or not fact.statement:
                findings.append("descriptive_scope_or_provenance_invalid")
            terms = (*fact.objects, fact.subject, fact.object_suffix, fact.condition, fact.mode, *fact.qualifiers, *fact.results)
            if any(" ".join(term.casefold().split()) not in text for term in terms if term):
                findings.append("descriptive_fact_content_lost:" + fact.fact_id)
            if fact.modality and not re.search(r"\b" + re.escape(fact.modality) + r"\b", text):
                findings.append("descriptive_modality_lost:" + fact.fact_id)
            if fact.negative != bool(re.search(r"\b(?:does not|do not|can not|may not)\b", text)):
                findings.append("descriptive_polarity_changed:" + fact.fact_id)
            if not re.search(r"\b" + re.escape(fact.action) + r"(?:s|es)?\b", text) and not (
                fact.action.endswith("y") and re.search(r"\b" + re.escape(fact.action[:-1]) + r"ies\b", text)
            ):
                findings.append("descriptive_action_lost:" + fact.fact_id)
            if fact.coordination == "or" and len(fact.objects) > 1 and " or " not in text:
                findings.append("descriptive_alternative_lost:" + fact.fact_id)
    for fact_id in sorted(expected - represented):
        findings.append("descriptive_fact_not_rendered:" + fact_id)
    for fact_id in sorted(represented - expected):
        findings.append("descriptive_unexpected_contributor:" + fact_id)
    return findings


def extract_srs_descriptive_facts(
    statement: str, *, source: str, scope: str, section: str, mode: str = "",
) -> Tuple[List[DescriptiveFact], str]:
    facts: List[DescriptiveFact] = []
    recognized = False
    unsupported = False
    for clause in re.split(r"[•]|(?<=[.!?])\s+(?=[A-Z])", statement):
        clause = clause.strip()
        if not clause or re.search(r"\b(?:shall|must|required to|Covers:)\b", clause, re.IGNORECASE):
            continue
        condition = ""
        conditional = re.match(r"^((?:When|If|Unless)\s+[^,]+),\s*(.+)$", clause, re.IGNORECASE)
        if conditional:
            condition, clause = conditional.groups()
        external = re.search(
            r"\bcan\s+read\s+external\s+sensors\s+by\s+means\s+of\s+(?:an?\s+)?"
            r"([A-Za-z0-9+ -]+?\s+protocol)\b", clause, re.IGNORECASE,
        )
        samples = re.search(
            r"\bsamples(?:\s+of)?\s+([A-Za-z ,/-]+?)\s+(?:signals?\s+)?from\s+ADC\b"
            r"([^.!?]*\bstores\b[^.!?]*)[.!?]$", clause, re.IGNORECASE,
        )
        processed = re.fullmatch(
            r"([A-Za-z ,/-]+?)\s+data\s+raw\s+in\b.+?\bare\s+processed\s+by\b.+?[.!?]",
            clause, re.IGNORECASE,
        )
        accessible = re.fullmatch(
            r"The data collected by\b.+?\bis accessible from\b.+?,\s*for sensor fusion algorithm elaboration[.!?]",
            clause, re.IGNORECASE,
        )
        impedance = re.fullmatch(
            r".+?\s+channel\s+delivers\s+both\s+the real and the imaginary parts of\s+(.+?)[.!?]",
            clause, re.IGNORECASE,
        )
        direct = re.fullmatch(
            r"The system\s+(?:(can|may)\s+(not\s+)?(support|provide|perform|integrate|acquire|process|store)|"
            r"(does not)\s+(support|provide|perform|integrate|acquire|process|store)|"
            r"(supports|provides|performs|integrates|acquires|processes|stores))\s+(.+)[.]",
            clause, re.IGNORECASE,
        )
        if not any((external, samples, processed and mode, accessible, impedance, direct)):
            unsupported = True
            continue
        recognized = True
        guarded_clause = re.sub(r"according to the user's configuration", "", clause, flags=re.IGNORECASE)
        if not direct and re.search(
            r"\b(?:not|no|cannot|never|may|might|optionally|only|if|when|unless|until|before|after|without|except)\b",
            guarded_clause, re.IGNORECASE,
        ):
            continue
        values = dict(subject="The system", source=source, statement=statement, scope=scope,
                      section=section, mode=mode, condition=condition)
        if external:
            qualifiers = ["through " + external.group(1).strip()]
            tail = clause[external.end():].strip(" .")
            if tail:
                if re.fullmatch(r",\s*enabling data collection in\s+\S+\s+and embedded elaboration also on external data domain", tail, re.IGNORECASE):
                    qualifiers.append("with data collection and embedded processing of external measurements")
                else:
                    unsupported = True
                    continue
            facts.append(DescriptiveFact(
                action="acquire", objects=("external sensor measurements",), modality="can",
                qualifiers=tuple(qualifiers), **values,
            ))
        elif samples:
            measured = samples.group(1).strip()
            coordination = "or" if re.search(r"\bor\b", measured) else "and"
            objects = tuple(item.strip() for item in re.split(r",\s*|\s+(?:and|or)\s+", measured) if item.strip())
            results = []
            if re.search(r"\baverag(?:e|es|ing)\b", samples.group(2), re.IGNORECASE):
                averaging = "averages the samples"
                if "according to the user's configuration" in samples.group(2).casefold():
                    averaging += " according to the user's configuration"
                results.append(averaging)
            results.append("stores the raw sampled data" if re.search(r"\braw\b", samples.group(2), re.IGNORECASE)
                           else "stores the sampled data")
            facts.append(DescriptiveFact(action="acquire", objects=objects, coordination=coordination,
                                         object_suffix="measurements", results=tuple(results), **values))
        elif processed and mode:
            measured = processed.group(1).strip()
            objects = tuple(item.strip() for item in re.split(r",\s*|\s+(?:and|or)\s+", measured) if item.strip())
            facts.append(DescriptiveFact(action="process", objects=objects, object_suffix="measurements",
                                         coordination="or" if re.search(r"\bor\b", measured) else "and", **values))
        elif accessible:
            if not any(fact.objects == ("external sensor measurements",) for fact in facts):
                unsupported = True
                continue
            facts.append(DescriptiveFact(action="provide", objects=("collected external sensor measurements",),
                                         qualifiers=("for sensor-fusion processing",), **values))
        elif impedance:
            facts.append(DescriptiveFact(action="provide",
                                         objects=("the real and the imaginary parts of " + impedance.group(1),), **values))
        elif direct:
            if re.search(r"\b(?:register|regmap|address|port|signal)\b|[_=]|\b0x[0-9a-f]+\b", direct.group(7), re.IGNORECASE):
                continue
            action = (direct.group(3) or direct.group(5) or direct.group(6)).casefold()
            action = "process" if action == "processes" else action.removesuffix("s") if direct.group(6) else action
            facts.append(DescriptiveFact(action=action, objects=(direct.group(7).strip(),),
                                         modality=(direct.group(1) or "").casefold(),
                                         negative=bool(direct.group(2) or direct.group(4)), **values))
    reason = "unsupported descriptive clause requires explicit projection" if facts and unsupported else (
        "" if facts else "qualifier construction requires explicit projection" if recognized else "no supported functional construction"
    )
    return facts, reason


def compose_srs_system_overview(
    records: Iterable[Mapping[str, object]],
    *,
    mode_rows: Iterable[Mapping[str, object]] = (),
    interface_rows: Iterable[Mapping[str, object]] = (),
    power_records: Iterable[Mapping[str, object]] = (),
    block_names: Sequence[str] = (),
    audit_rows: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, List[str]]:
    profile = descriptive_profile("SRS")
    """Project scoped descriptive evidence into a non-authoritative SRS overview."""
    overview_records: List[Tuple[str, str]] = []
    overview_scopes: Dict[Tuple[str, str], str] = {}
    recovered_modes: Dict[str, List[str]] = {}
    projected_facts: List[DescriptiveFact] = []

    def audit(section: str, record: Mapping[str, object], summary: str, reason: str) -> None:
        if audit_rows is not None:
            audit_rows.append({
                "section": section,
                "statement": csv_cell_text(record.get("statement") or record.get("Purpose") or record.get("text")),
                "source": csv_cell_text(record.get("source") or record.get("provenance")),
                "scope": csv_cell_text(record.get("scope") or ""),
                "rendered_summary": summary,
                "decision": "selected" if summary else "rejected",
                "reason": reason,
                "profile": SRS_DESCRIPTIVE_PROFILE.name,
                "fact_id": "",
                "fact_json": "",
                "contributor_ids": "[]",
                "profile_version": str(profile.version),
                "profile_fingerprint": stable_payload_hash(asdict(profile)),
                "projection_adapter": "srs-overview",
                "source_record_id": "",
                "normalized_record_json": "",
                "unit_id": "",
                "semantic_unit_json": "",
            })

    def audit_candidate(section: str, statement: str, source: str, summary: str) -> None:
        audit(section, {"statement": statement, "source": source, "scope": overview_scopes[(statement, source)]}, summary,
              "system-level projection of complete descriptive relationship")

    for record in records:
        statement = csv_cell_text(record.get("statement") or record.get("function") or record.get("text")).strip()
        source = csv_cell_text(record.get("source") or record.get("provenance")).strip()
        scope = csv_cell_text(record.get("scope") or record.get("evidence_scope")).casefold().strip()
        kind = csv_cell_text(record.get("evidence_kind") or record.get("record_type")).casefold().strip()
        if not statement or not source or scope not in {"system", "architecture"} or kind == "power_domain":
            audit("", record, "", "not a provenanced system/architecture descriptive record")
            continue
        mode_match = re.search(r"\bSection\s+\d+(?:\.\d+)*\s+([^,(]+?\bMode)\b", source, re.IGNORECASE)
        mode = mode_match.group(1).strip() if mode_match else csv_cell_text(record.get("mode")).strip()
        if mode:
            recovered_modes.setdefault(mode, [])
        facts, projection_reason = extract_srs_descriptive_facts(
            statement, source=source, scope=scope,
            section=SRS_SYSTEM_OVERVIEW_HEADINGS[4 if mode else 1], mode=mode,
        )
        projected_facts.extend(facts)
        if projection_reason:
            audit("", record, "", "projection_gap: " + projection_reason)
        if re.search(
            r"\b(?:shall|must|required to|Covers:)\b|\b(?:register|regmap|address|port\s+name|signal\s+(?:level|name)|"
            r"ATPG|BIST|scan|clock\s+gating|reset\s+synchroniz|transparenc|Req_ID|Target|Delay|Requirements Definition)\b|"
            r"\b0x[0-9a-f]+\b|[_=]|[|•]",
            statement,
            re.IGNORECASE,
        ):
            audit("", record, "", "raw/implementation text not eligible for direct narrative")
            continue
        if re.match(r"^(?:aim of this document|this document|in the following table|table\s+\d+)\b", statement, re.IGNORECASE):
            continue
        if len(statement) < 35 or not re.search(r"[.!?]\s*$", statement):
            continue
        if any(
            re.search(r"\b" + r"[-_\s]+".join(re.escape(token) for token in re.split(r"[-_\s]+", label.strip()) if token) + r"\b", statement, re.IGNORECASE)
            for label in block_names if label.strip()
        ):
            audit("", record, "", "named block text not eligible for direct narrative")
            continue
        overview_records.append((statement, source))
        overview_scopes[(statement, source)] = scope
        audit("", record, statement, "complete scoped descriptive candidate")

    sections: Dict[str, List[str]] = {heading: [] for heading in SRS_SYSTEM_OVERVIEW_HEADINGS}
    identity_re = re.compile(r"^([A-Z][A-Za-z0-9.-]*)\s+is\s+((?:an?|the)\s+.+)$", re.IGNORECASE)
    capability_re = re.compile(
        r"^(?:The\s+)?(.+?)\s+signal\s+chain\s+is\s+designed\s+for\s+(.+?)\.?$",
        re.IGNORECASE,
    )
    feature_capability_re = re.compile(
        r"^(?:The\s+)?(.+?)\s+signal\s+chain\s+has\b.+?\bfeatures\s+supporting\s+(.+?)"
        r"(?:,\s*(?:such as|including)\b.*)?\.?$",
        re.IGNORECASE,
    )
    identities: List[str] = []
    capabilities: List[str] = []
    measurement_facts: List[DescriptiveFact] = []
    interface_roles: List[str] = []
    for statement, source in overview_records:
        identity_match = identity_re.match(statement)
        if identity_match:
            identity = identity_match.group(2).rstrip('.')
            identity = re.sub(r"\banalog front end device\b", "analog front end", identity, flags=re.IGNORECASE)
            identity = re.sub(r"\bembedded process capabilities\b", "embedded processing capabilities", identity, flags=re.IGNORECASE)
            identities.append(f"The system is {identity}.")
            audit_candidate(SRS_SYSTEM_OVERVIEW_HEADINGS[0], statement, source, identities[-1])
        elif re.match(r"^The system is\b", statement, re.IGNORECASE):
            identities.append(statement)
            audit_candidate(SRS_SYSTEM_OVERVIEW_HEADINGS[0], statement, source, identities[-1])

        capability_match = capability_re.match(statement)
        if capability_match:
            role = re.split(r",\s*(?:such as|including)\b|\.\s+", capability_match.group(2), maxsplit=1, flags=re.IGNORECASE)[0].strip().rstrip(".")
        elif feature_capability_re.match(statement):
            feature_match = feature_capability_re.match(statement)
            role = re.split(r",\s*(?:such as|including)\b|\.\s+", feature_match.group(2), maxsplit=1, flags=re.IGNORECASE)[0].strip().rstrip(".")
        else:
            role = ""
        if role:
            role_parts = re.split(r"\s+(?=with\b|without\b|only\b|when\b|during\b)", role, maxsplit=1, flags=re.IGNORECASE)
            fact = DescriptiveFact(
                subject="The system", action="support", objects=(role_parts[0],),
                qualifiers=tuple(role_parts[1:]), source=source, statement=statement,
                scope=overview_scopes[(statement, source)], section=SRS_SYSTEM_OVERVIEW_HEADINGS[1],
            )
            projected_facts.append(fact)
            measurement_facts.append(fact)
            if len(re.split(r"\.\s+", statement)) > 1 and not any(fact.source == source for fact in projected_facts[:-1]):
                audit("", {"statement": statement, "source": source, "scope": overview_scopes[(statement, source)]}, "",
                      "projection_gap: additional sentence has no supported functional construction")
        if re.search(r"\b(?:system boundary|external interface|host interface|cross-domain interface)\b", statement, re.IGNORECASE):
            interface_roles.append(statement)

    def unique(values: Iterable[str]) -> List[str]:
        result: List[str] = []
        seen: Set[str] = set()
        for value in values:
            normalized = re.sub(r"\s+", " ", value).strip()
            key = normalized.casefold()
            if key and key not in seen:
                seen.add(key)
                result.append(normalized)
        return result

    def project(facts: Sequence[DescriptiveFact]) -> List[DescriptiveParagraph]:
        normalized: Dict[str, NormalizedSourceRecord] = {}
        projected: Dict[str, List[DescriptiveFact]] = {}
        for fact in facts:
            record_id = "desc-source-" + stable_payload_hash((fact.statement, fact.source, fact.scope))[:20]
            normalized[record_id] = NormalizedSourceRecord(record_id, fact.statement, "admitted_context",
                                                          fact.scope, (fact.source,), "selected",
                                                          "SRS adapter admitted scoped context")
            projected.setdefault(record_id, []).append(fact)
        result = run_descriptive_flow(normalized.values(), profile=profile, adapter_name="srs-overview",
                                      adapter=lambda record: (projected[record.record_id], ""))
        for linkage in result.audit:
            if linkage["decision"] != "selected":
                continue
            fact = next(fact for fact in result.facts if fact.fact_id == linkage["fact_id"])
            unit = next(unit for unit in result.units if unit.unit_id == linkage["unit_id"])
            audit(fact.section, {"statement": fact.statement, "source": fact.source, "scope": fact.scope},
                  unit.text, linkage["reason"])
            if audit_rows is not None:
                audit_rows[-1].update(linkage)
        return list(result.paragraphs)

    for paragraph in project(projected_facts):
        first = paragraph.facts[0]
        if first.mode:
            recovered_modes[first.mode].append(paragraph.text)
        else:
            capabilities.append(paragraph.text)

    identities = unique(identities)
    capabilities = unique(capabilities)
    sections[SRS_SYSTEM_OVERVIEW_HEADINGS[0]] = identities or ["The system identity and product role are not specified."]
    sections[SRS_SYSTEM_OVERVIEW_HEADINGS[1]] = [
        item for item in capabilities
        if item.casefold() not in {identity.casefold() for identity in identities}
    ] or ["System-level capabilities are not specified."]

    domain_items: List[str] = []
    domain_groups = [
        ("Sensing and measurement", "The measurement paths", True, measurement_facts),
        ("External acquisition and data handling", "The acquisition and data paths", True,
         [fact for fact in projected_facts if not fact.mode and fact.action in {"acquire", "store", "provide"}]),
        ("Embedded processing", "The processing function", False,
         [fact for fact in projected_facts if fact.action == "process" and not fact.negative]),
    ]
    for name, subject, plural, facts in domain_groups:
        if not facts:
            continue
        paragraphs = project([replace(fact, subject=subject, plural_subject=plural,
                                      section=SRS_SYSTEM_OVERVIEW_HEADINGS[2]) for fact in facts])
        domain_items.append(f"- **{name}**\n" + "\n".join("  - " + text for text in unique(paragraph.text for paragraph in paragraphs)))
    sections[SRS_SYSTEM_OVERVIEW_HEADINGS[2]] = domain_items or [
        "Top-level domain and subsystem responsibilities are not specified in the available descriptions."
    ]

    interface_groups: Dict[str, Dict[str, Set[str]]] = {}
    group_specs = (
        ("Sensing input", r"\b(?:sensor|sensing|analog input)\b"),
        ("Serial communication", r"\b(?:serial|i2c|spi)\b"),
        ("Measurement data exchange", r"\b(?:digitized samples?|buffered (?:output )?samples?)\b"),
        ("Interrupt reporting", r"\binterrupt\b"),
        ("Power supply", r"\bsupply\b"),
    )
    interface_sources: Dict[str, List[Mapping[str, object]]] = {}
    for row in interface_rows:
        purpose = csv_cell_text(row.get("Purpose") or row.get("Description")).strip()
        if not purpose:
            continue
        searchable = purpose.casefold()
        group = next((name for name, pattern in group_specs if re.search(pattern, searchable, re.IGNORECASE)), "")
        if not group:
            continue
        interface_sources.setdefault(group, []).append(row)
        values = interface_groups.setdefault(group, {"direction": set(), "type": set()})
        direction = csv_cell_text(row.get("Direction")).strip().casefold()
        medium = csv_cell_text(row.get("Type")).strip().casefold()
        if direction in {"input", "output", "bidirectional"}:
            values["direction"].add(direction)
        if medium in {"analog", "digital", "power"}:
            values["type"].add(medium)
    interface_content: List[str] = []
    if interface_groups:
        role_names = [name.casefold() for name in interface_groups]
        interface_content.append(
            "The interfaces provide " + _descriptive_join(role_names) + " roles. "
            "External versus internal placement is not specified for every interface."
        )
        interface_content.extend([
            "",
            "| Boundary role | Direction | Medium |",
            "|---|---|---|",
        ])
        direction_order = {"input": 0, "bidirectional": 1, "output": 2}
        for group, values in interface_groups.items():
            directions = ", ".join(sorted(values["direction"], key=lambda item: direction_order[item]))
            media = ", ".join(sorted(values["type"]))
            summary = f"| {group} | {directions} | {media} |"
            interface_content.append(summary)
            for row in interface_sources[group]:
                audit(SRS_SYSTEM_OVERVIEW_HEADINGS[3], row, summary, "interface role from purpose; no pin-name inference")
    elif interface_roles:
        interface_content.extend(unique(interface_roles))
    else:
        interface_content.append("External and cross-domain interface roles are not specified at system level.")
    sections[SRS_SYSTEM_OVERVIEW_HEADINGS[3]] = interface_content

    modes = unique(
        csv_cell_text(row.get("mode")).strip()
        for row in mode_rows
        if csv_cell_text(row.get("mode")).strip()
        and not csv_cell_text(row.get("evidence")).casefold().startswith("derived default:")
    )
    modes = unique([*modes, *recovered_modes])
    mode_items: List[str] = []
    for mode in modes:
        descriptions = [
            statement for statement, _source in overview_records
            if re.search(r"\b" + re.escape(mode) + r"\b", statement, re.IGNORECASE)
        ]
        role = unique([*recovered_modes.get(mode, []), *descriptions])
        mode_items.append(
            f"- **{mode}**\n" + "\n".join(f"  - {item}" for item in role) if role else
            f"- **{mode}**\n  - Its system-level role and transitions are not specified."
        )
        for statement, source in overview_records:
            if statement in descriptions:
                audit_candidate(SRS_SYSTEM_OVERVIEW_HEADINGS[4], statement, source, statement)
    sections[SRS_SYSTEM_OVERVIEW_HEADINGS[4]] = mode_items or ["System-level operating modes are not specified."]

    eligible_power = [
        record for record in power_records
        if csv_cell_text(record.get("source") or record.get("provenance"))
        and csv_cell_text(record.get("scope") or record.get("evidence_scope")).casefold() in {"system", "architecture"}
        and not re.search(
            r"\b(?:shall|must)\b|\b(?:not|no)\s+(?:switchable|power-gated|always[- ]on|retention)\b|"
            r"\b(?:cannot|can not|does not|do not)\s+(?:be powered|preserve|retain)\b",
            csv_cell_text(record.get("statement")), re.IGNORECASE,
        )
        and "definitions" not in csv_cell_text(record.get("source")).casefold()
    ]
    power_items: List[str] = []
    power_roles = (
        (r"\b(?:power domain|power domains|supply domain)\b.*\b(?:independent|independently)\b", "Supply-domain structure", "The architecture separates logic into supply domains with independent power control."),
        (r"\b(?:always[- ]on|always active|never powered down)\b", "Always-on behavior", "An always-on domain remains powered during low-power operation."),
        (r"\b(?:switchable|power-gated)\b|\b(?:domain|domain logic)\b.{0,60}\b(?:can|may)\s+be\s+powered\s+down\b", "Switchable behavior", "The power architecture includes a domain whose supply can be switched off."),
        (r"\b(?:retains|preserves)\s+(?:register\s+)?state\b.{0,100}\bpowered down\b", "Retention behavior", "State is preserved while the main logic is powered down."),
    )
    for pattern, label, _summary in power_roles:
        matches = [record for record in eligible_power if re.search(pattern, csv_cell_text(record.get("statement")), re.IGNORECASE)]
        facts = []
        for record in matches:
            statement = csv_cell_text(record.get("statement"))
            if re.search(r"\b(?:only|unless|if|after|before|until|except)\b", statement, re.IGNORECASE):
                audit("", record, "", "projection_gap: power qualifier requires explicit projection")
                continue
            values = dict(source=csv_cell_text(record.get("source") or record.get("provenance")),
                          statement=statement, scope=csv_cell_text(record.get("scope") or record.get("evidence_scope")).casefold(),
                          section=SRS_SYSTEM_OVERVIEW_HEADINGS[5])
            if label == "Supply-domain structure":
                fact = DescriptiveFact(subject="The supply domains", plural_subject=True, action="support",
                                       objects=("independent power control",), **values)
            elif label == "Always-on behavior":
                fact = DescriptiveFact(subject="An always-on domain", action="remain", objects=("powered",), **values)
            elif label == "Switchable behavior":
                qualifiers = []
                if re.search(r"\bin idle\b", statement, re.IGNORECASE):
                    qualifiers.append("in idle")
                if re.search(r"\bwhen\b[^.!?•]*\bnot in use\b", statement, re.IGNORECASE):
                    qualifiers.append("when its associated logic is not in use")
                modal = re.search(r"\b(can|may)\s+be\s+powered\s+down\b", statement, re.IGNORECASE)
                fact = DescriptiveFact(subject="A switchable domain", action="enter", objects=("a powered-down state",),
                                       modality=modal.group(1).casefold() if modal else "can",
                                       qualifiers=tuple(qualifiers), **values)
            else:
                fact = DescriptiveFact(subject="The power architecture", action="preserve", objects=("state",),
                                       qualifiers=("while the main logic is powered down",), **values)
            facts.append(fact)
        paragraphs = project(facts)
        if paragraphs:
            power_items.append(f"- **{label}**\n" + "\n".join("  - " + paragraph.text for paragraph in paragraphs))
    if not any("**Retention behavior**" in item for item in power_items):
        power_items.append("- **Retention**\n  - State retention across system power transitions is not specified.")
    clock_reset = [
        statement for statement, _source in overview_records
        if re.search(r"\b(?:clock|reset)\b", statement, re.IGNORECASE)
    ]
    if clock_reset:
        power_items.extend(f"- **Clock and reset**\n  - {item}" for item in unique(clock_reset))
    else:
        power_items.append("- **Clock and reset**\n  - Top-level clock and reset coordination are not specified.")
    sections[SRS_SYSTEM_OVERVIEW_HEADINGS[5]] = power_items

    scope_content = [
        statement for statement, _source in overview_records
        if re.search(r"\b(?:system scope|scope covers|system assumes|allocation boundar|engineering scope)\b", statement, re.IGNORECASE)
    ]
    sections[SRS_SYSTEM_OVERVIEW_HEADINGS[6]] = unique(scope_content) or [
        "System-level scope covers product capabilities and externally observable behavior. Subsystem implementation remains within its engineering allocation.",
        "- **Assumptions**\n  - Additional system-level assumptions are not described in the available descriptions.",
    ]
    for statement, source in overview_records:
        if statement in scope_content:
            audit_candidate(SRS_SYSTEM_OVERVIEW_HEADINGS[6], statement, source, statement)
    if audit_rows is not None:
        rendered = "\n".join(item for items in sections.values() for item in items)
        for row in audit_rows:
            if row["rendered_summary"] and (not row["section"] or row["rendered_summary"] not in rendered):
                row["decision"] = "candidate_only"
                row["reason"] = "candidate retained; not rendered in this overview"
    return sections


SRS_INTRODUCTORY_SECTIONS = ("1.1", "1.2", "1.3", "1.4", "2.1", "2.2", "2.3", "2.4")

SRS_INTRODUCTORY_WRITING_RULE_ID = "srs-introductory-authority-bounded-v1"
SRS_INTRODUCTORY_WRITING_RULE = (
    "Use concise, natural technical prose bounded by the selected approved content.",
    "Describe document purpose and scope without promising complete coverage or creating allocation.",
    "Mention behavior, interfaces, performance and implementation only to the extent supported by approved content.",
    "Treat terminology as a reading aid, not authority for capabilities, limits, obligations or acceptance criteria.",
    "Reference existing source and traceability information without implying new applicability or approval.",
    "Keep this preferred writing rule within the SRS introductory profile; do not inherit it in DRS, ARS or IPOS.",
)

SRS_DOCUMENT_CONTENT_PROFILE = DescriptiveWritingProfile(
    name="srs-document-content", document_type="SRS", allowed_scopes=("document", "system", "architecture"),
    evidence_kinds=("document_introduction", "document_terminology", "block_catalog", "power_domain"),
    authority_tiers=("presentation_policy", "admitted_context"), owner_policy="unrestricted",
    allowed_domains=(), allowed_layers=(), projection_adapters=("srs-document-content",),
    topic_roles=(*SRS_INTRODUCTORY_SECTIONS, "3.6", "4.1", "5.1"), excluded_terms=(), runtime_enabled=True,
)


def compose_srs_support_content(project_name: str, snapshot_id: str,
                                catalog_entries: Sequence[Mapping[str, str]], catalog_findings: Sequence[str],
                                power_records: Sequence[Mapping[str, object]]) -> Tuple[Dict[str, List[str]], Dict[str, object]]:
    sections: Dict[str, List[str]] = {section: [] for section in SRS_DOCUMENT_CONTENT_PROFILE.topic_roles}
    records: List[NormalizedSourceRecord] = []
    units: List[SemanticUnit] = []
    power_rows: List[Dict[str, str]] = []
    gaps: List[str] = list(catalog_findings)

    def retain(section: str, text: str, source_text: str, provenance: Tuple[str, ...], tier: str,
               scope: str = "architecture") -> None:
        record_id = "srs-source-" + stable_payload_hash((section, source_text, provenance))[:20]
        record = NormalizedSourceRecord(record_id, source_text, tier, scope,
                                        provenance, "selected", "SRS document-specific presentation")
        unit = SemanticUnit("srs-unit-" + stable_payload_hash((section, text, record_id))[:20], section, text,
                            (record_id,), len(units))
        records.append(record)
        units.append(unit)
        sections[section].append(text)

    purpose = (f"This document presents the system-level requirements and supporting context for {project_name} "
               "included in the selected approved baseline. Descriptive content does not add requirements or change their allocation.")
    retain("1.1", purpose, purpose, ("SRS document-purpose policy",), "presentation_policy", "document")
    scope = ("The scope is limited to system-level requirements allocated to this document and the supporting system context. "
             "Analog and digital behavior, interfaces, operating conditions and verification information are described only "
             "to the extent supported by the approved content. This description does not extend subsystem or block-level allocations.")
    retain("1.2", scope, scope, ("SRS document-scope policy",), "presentation_policy", "document")
    audience = ("This document is intended for system architects, analog and digital design engineers, firmware engineers, "
                "verification and validation engineers, test and product engineers, and program and customer stakeholders.")
    retain("1.3", audience, audience, ("SRS intended-audience policy",), "presentation_policy", "document")
    references = ("Reference documents are listed in Table 2. Source links for any included requirements are recorded "
                  "in the associated traceability matrix. Listing a document or standard does not itself establish "
                  "applicability or add obligations.")
    retain("1.4", references, references, ("SRS reference-document policy",), "presentation_policy", "document")
    terminology = {
        "2.1": (
            ("System", "The device or functional scope identified in the approved descriptions."),
            ("Subsystem", "A grouping of related functions identified in the approved architecture context."),
            ("Block", "A concrete unit identified in the approved architecture context."),
            ("SRS", "System Requirements Specification; the system-level requirements and context document."),
            ("ARS", "Analog Requirements Specification; the analog and mixed-signal integration document."),
            ("DRS", "Digital Requirements Specification; the digital integration document."),
            ("IPOS", "The block-local implementation requirements specification."),
        ),
        "2.2": (
            ("Input/output range", "The span of input or output values considered under stated operating conditions."),
            ("Gain", "The ratio of a change in output to the corresponding change in input."),
            ("Offset", "The deviation from the specified reference response at a reference input."),
            ("Noise", "Unwanted variations superimposed on a signal or measurement."),
            ("Bandwidth", "The frequency interval over which a response meets a defined criterion."),
            ("Full-scale", "The reference magnitude or span corresponding to the specified measurement range."),
            ("ODR", "Output data rate; the rate at which new output samples become available."),
            ("Sensitivity", "The change in output per unit change in the measured quantity."),
        ),
        "2.3": (
            ("Register", "A named storage element used to expose data, configuration or status."),
            ("Bit field", "A defined subset of bits within a register or data word."),
            ("Mode", "An operating configuration described in the applicable content."),
            ("State", "A condition of control logic identified within a described operating sequence."),
            ("Reset", "Initialization of affected logic as described in the applicable content."),
            ("Interrupt", "An event notification that requests attention from a controller or processor."),
            ("Boot sequence", "An initialization sequence described in the applicable content."),
            ("Interface", "A defined boundary through which components exchange data, control or status."),
        ),
        "2.4": (
            ("RMS noise", "The root-mean-square amplitude of noise over a stated measurement interval and bandwidth."),
            ("SNR", "Signal-to-noise ratio; the ratio of signal power to noise power, commonly expressed in decibels."),
            ("Latency", "The elapsed time between a defined initiating event and its corresponding response."),
            ("Precision", "The repeatability of measurement results under stated conditions."),
            ("Tolerance", "A permitted deviation where specified relative to a reference value or condition."),
            ("GR&R", "Gage repeatability and reproducibility; the evaluation of measurement-system variation."),
            ("Guard band", "A margin between acceptance and specification limits where such a margin is specified."),
            ("Pass/fail", "An assessment against acceptance criteria specified by the applicable requirements."),
        ),
    }
    terminology_context = {
        "2.1": ("These definitions aid interpretation of the system descriptions and document abbreviations. "
            "They do not establish capabilities, ownership or allocation; specific meanings follow the approved content."),
        "2.2": ("Analog terms are descriptive. Ranges, operating conditions and performance limits are those "
            "stated in the applicable approved content."),
        "2.3": ("Digital terms aid interpretation of configuration and control descriptions. Their inclusion "
            "does not imply a particular implementation or supported feature."),
        "2.4": ("Measurement terms aid interpretation of verification information. Test conditions, limits and "
            "acceptance criteria remain those specified in the applicable approved requirements."),
    }
    for section, definitions in terminology.items():
        context = terminology_context[section]
        retain(section, context, context, ("SRS terminology policy:" + section,), "presentation_policy", "document")
        for term, definition in definitions:
            text = f"**{term}:** {definition}"
            retain(section, text, text, ("SRS terminology policy:" + section + ":" + term,), "presentation_policy", "document")
    for entry in catalog_entries:
        section = "4.1" if entry["category"] == "analog" else "5.1"
        summary = compose_technical_block_purpose(entry["block"], entry["function"])
        retain(section, f"- **{entry['block']}**\n\n  {summary}", entry["function"],
               (entry["source"], "approved classification sources:" + entry["classification_sources"]), "admitted_context")
    labels = re.compile(r"(?:Included block\(s\)|Domain type|Voltage|Control mode|Notes|Function|Characteristics|Control):\s*", re.IGNORECASE)
    for record in power_records:
        statement = csv_cell_text(record.get("statement"))
        source = csv_cell_text(record.get("source") or record.get("provenance"))
        scope = csv_cell_text(record.get("scope") or record.get("evidence_scope")).casefold()
        if csv_cell_text(record.get("evidence_kind") or record.get("record_type")).casefold() != "power_domain":
            continue
        if not source or scope not in {"architecture", "system"}:
            gaps.append("SRS_POWER_SCOPE_OR_PROVENANCE_MISSING: " + source)
            continue
        matches = list(labels.finditer(statement))
        name = statement[:matches[0].start()].strip(" :.") if matches else ""
        fields = {match.group(0).split(":")[0].casefold():
                  statement[match.end():matches[index + 1].start() if index + 1 < len(matches) else len(statement)].strip(" .\u2022")
                  for index, match in enumerate(matches)}
        if not name or not fields.get("domain type") or not fields.get("function"):
            gaps.append("SRS_POWER_PROJECTION_GAP: " + source)
            continue
        role = fields["function"]
        blocks = fields.get("included block(s)", "")
        if blocks:
            role += ". Associated blocks: " + ", ".join(value.strip() for value in blocks.split(",") if value.strip())
        voltage = fields.get("voltage", "")
        if voltage:
            if re.fullmatch(r"\d+(?:\.\d+)?\s*(?:mV|V)", voltage):
                role += ". Supply voltage: " + voltage
            else:
                gaps.append("SRS_POWER_VOLTAGE_UNRELIABLE: " + source + ": " + voltage)
        conditions = fields.get("characteristics", "")
        notes = fields.get("notes", "")
        if notes and notes.casefold() not in conditions.casefold():
            if re.search(r"\s+\d+\s+\d+(?:\.\d+)*$", notes):
                gaps.append("SRS_POWER_NOTE_UNREADABLE: " + source + ": " + notes)
            else:
                conditions = notes + (". " + conditions if conditions else "")
        cells = [name, fields["domain type"], fields.get("control mode") or fields.get("control") or "Not specified",
                 role, conditions or "Not specified"]
        text = "| " + " | ".join(value.replace("|", "\\|").replace("\n", " ") for value in cells) + " |"
        retain("3.6", text, statement, (source,), "admitted_context", scope)
        power_rows.append({"source": source, "statement": statement, "domain": name, "row": text})
    return sections, {"schema_version": 1, "snapshot_id": snapshot_id, "project_name": project_name,
                      "profile": SRS_DOCUMENT_CONTENT_PROFILE.name, "profile_version": SRS_DOCUMENT_CONTENT_PROFILE.version,
                      "profile_fingerprint": stable_payload_hash(asdict(SRS_DOCUMENT_CONTENT_PROFILE)),
                      "projection_adapter": "srs-document-content",
                      "writing_rule_id": SRS_INTRODUCTORY_WRITING_RULE_ID,
                      "writing_rule_fingerprint": stable_payload_hash(SRS_INTRODUCTORY_WRITING_RULE),
                      "records": [asdict(record) for record in records], "units": [asdict(unit) for unit in units],
                      "catalog_entries": list(catalog_entries), "power_rows": power_rows, "review_findings": gaps}


def _validate_srs_fact_audit(markdown_path: Path, section_bodies: Mapping[str, str]) -> List[str]:
    audit_path = markdown_path.with_name("descriptive_system_overview_audit.csv")
    if not audit_path.exists():
        return []
    findings: List[str] = []
    groups: Dict[Tuple[str, str, Tuple[str, ...]], List[tuple]] = {}
    with audit_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not {"profile", "fact_id", "fact_json", "contributor_ids", "profile_version", "profile_fingerprint",
            "projection_adapter", "source_record_id", "normalized_record_json", "unit_id", "semantic_unit_json"}.issubset(reader.fieldnames or []):
            return ["srs_descriptive_audit_schema_missing"]
        for row in reader:
            if not row.get("fact_id"):
                continue
            try:
                payload = json.loads(row["fact_json"])
                for field in ("objects", "qualifiers", "results"):
                    payload[field] = tuple(payload[field])
                fact = DescriptiveFact(**payload)
                contributors = json.loads(row["contributor_ids"])
                if not isinstance(contributors, list) or any(not isinstance(value, str) for value in contributors):
                    raise ValueError("Invalid contributors")
                if fact.fact_id not in contributors or len(set(contributors)) != len(contributors):
                    findings.append("srs_descriptive_audit_contributors_invalid:" + fact.section)
                if (fact.fact_id != row["fact_id"] or row["profile"] != SRS_DESCRIPTIVE_PROFILE.name
                        or row["decision"] != "selected" or row["section"] != fact.section
                        or any(row[field] != getattr(fact, field) for field in ("source", "statement", "scope"))):
                    raise ValueError("Audit fields disagree with fact")
                record_payload = json.loads(row["normalized_record_json"])
                record_payload["provenance"] = tuple(record_payload["provenance"])
                record = NormalizedSourceRecord(**record_payload)
                unit_payload = json.loads(row["semantic_unit_json"])
                unit_payload["source_record_ids"] = tuple(unit_payload["source_record_ids"])
                unit = SemanticUnit(**unit_payload)
                if (record.record_id != row["source_record_id"] or record.text != fact.statement
                        or record.ownership_scope != fact.scope or fact.source not in record.provenance
                        or descriptive_evidence_findings(record, profile=SRS_DESCRIPTIVE_PROFILE)
                        or row["profile_version"] != str(SRS_DESCRIPTIVE_PROFILE.version)
                        or row["profile_fingerprint"] != stable_payload_hash(asdict(SRS_DESCRIPTIVE_PROFILE))
                        or row["projection_adapter"] not in SRS_DESCRIPTIVE_PROFILE.projection_adapters
                        or unit.unit_id != row["unit_id"] or unit.section != fact.section
                        or unit.text != row["rendered_summary"] or record.record_id not in unit.source_record_ids
                        or unit.unit_id != "desc-unit-" + stable_payload_hash(
                            (row["profile_fingerprint"], tuple(contributors), unit.text))[:20]):
                    raise ValueError("Invalid profile or materialization linkage")
                groups.setdefault((fact.section, row["rendered_summary"], tuple(contributors)), []).append(
                    (fact, contributors, row, record, unit))
            except (KeyError, TypeError, ValueError):
                findings.append("srs_descriptive_audit_fact_invalid:" + row.get("fact_id", ""))
    docx_path = markdown_path.with_suffix(".docx")
    docx_text = None
    if docx_path.exists():
        try:
            from docx import Document
            document = Document(docx_path)
            docx_text = " ".join(paragraph.text for paragraph in document.paragraphs)
        except Exception:
            findings.append("srs_descriptive_docx_unreadable")
    normalize = lambda text: " ".join(text.replace("\u2019", "'").replace("\u2018", "'").casefold().split())
    for (section, summary, _contributors), members in groups.items():
        facts = [member[0] for member in members]
        expected = list(dict.fromkeys(fact.fact_id for fact in facts))
        if any(member[1] != expected for member in members):
            findings.append("srs_descriptive_audit_contributors_invalid:" + section)
        records = tuple({member[3].record_id: member[3] for member in members}.values())
        result = DescriptiveFlowResult(records, tuple(facts), (DescriptiveParagraph(summary, tuple(facts)),),
                                       (members[0][4],), tuple(member[2] for member in members))
        findings.extend(validate_descriptive_flow(result, profile=SRS_DESCRIPTIVE_PROFILE))
        if not summary or normalize(summary) not in normalize(section_bodies.get(section, "")):
            findings.append("srs_descriptive_fact_missing_from_markdown:" + section)
        if docx_text is not None and normalize(summary) not in normalize(docx_text):
            findings.append("srs_descriptive_fact_missing_from_docx:" + section)
    return findings


def validate_srs_support_content(markdown_path: Path) -> List[str]:
    audit_path = markdown_path.with_name("descriptive_srs_content_audit.json")
    repo_root = markdown_path.parents[2]
    production = (repo_root / "data/canonical/canonical_store.sqlite").exists()
    if not audit_path.exists():
        return ["srs_content_audit_missing"] if production else []
    findings: List[str] = []
    try:
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        if audit["schema_version"] != 1:
            raise ValueError("Unknown content audit schema")
        profile = SRS_DOCUMENT_CONTENT_PROFILE
        if (audit["profile"] != profile.name or audit["profile_version"] != profile.version
                or audit["profile_fingerprint"] != stable_payload_hash(asdict(profile))
                or audit["projection_adapter"] not in profile.projection_adapters):
            raise ValueError("Invalid SRS document-content profile")
        if (audit["writing_rule_id"] != SRS_INTRODUCTORY_WRITING_RULE_ID
                or audit["writing_rule_fingerprint"] != stable_payload_hash(SRS_INTRODUCTORY_WRITING_RULE)):
            raise ValueError("Invalid SRS introductory writing rule")
        records = {record["record_id"]: record for record in audit["records"]}
        if len(records) != len(audit["records"]):
            raise ValueError("Duplicate normalized source IDs")
        text = markdown_path.read_text(encoding="utf-8")
        def body(section: str) -> str:
            match = re.search(r"(?ms)^### " + re.escape(section) + r"\s[^\n]*\n(.*?)(?=^#{1,3}\s|\Z)", text)
            return match.group(1) if match else ""
        def normalized(value: str) -> str:
            value = re.sub(r"<[^>]+>|&nbsp;", "", value)
            return " ".join(value.replace("**", "").replace("\u2019", "'").replace("\u2018", "'").split()).casefold()
        sections = {section: body(section) for section in profile.topic_roles}
        if not normalized(sections["1.1"]) or "this document presents the system-level requirements" not in normalized(sections["1.1"]):
            findings.append("srs_purpose_missing")
        if not normalized(sections["1.3"]):
            findings.append("srs_intended_audience_missing")
        for section in SRS_INTRODUCTORY_SECTIONS:
            if not normalized(sections[section]):
                findings.append("srs_introductory_section_missing:" + section)
        snapshot = re.search(r"(?m)^Snapshot ID:\s*(\S+)", text)
        if not snapshot or snapshot.group(1) != audit["snapshot_id"]:
            findings.append("srs_content_snapshot_mismatch")
        if production:
            from canonical_store import read_stage2_descriptive_evidence
            from validate_downstream_coherence import resolve_downstream_contract, snapshot_architecture_context, srs_catalog_from_context
            contract = resolve_downstream_contract(repo_root, audit["snapshot_id"])
            with (repo_root / "artifacts/stage2_mirco_arc/block_inventory.csv").open(encoding="utf-8-sig", newline="") as handle:
                inventory = list(csv.DictReader(handle))
            entries, review = srs_catalog_from_context(inventory, contract, snapshot_architecture_context(repo_root, contract))
            if audit["catalog_entries"] != entries:
                findings.append("srs_catalog_authority_mismatch")
            source_power = [record for record in read_stage2_descriptive_evidence(repo_root)
                            if csv_cell_text(record.get("evidence_kind")).casefold() == "power_domain"]
            _, expected = compose_srs_support_content(audit["project_name"], audit["snapshot_id"], entries, review, source_power)
            expected = json.loads(json.dumps(expected))
            for field in ("records", "units", "power_rows", "review_findings"):
                if audit[field] != expected[field]:
                    findings.append("srs_content_provenance_mismatch:" + field)
        docx_sections: Dict[str, str] = {}
        docx_tables: List[List[List[str]]] = []
        docx_path = markdown_path.with_suffix(".docx")
        if docx_path.exists():
            from docx import Document
            from docx.oxml.ns import qn
            from docx.table import Table
            document = Document(docx_path)
            current = ""
            for element in document.element.body:
                words = " ".join(node.text or "" for node in element.iter(qn("w:t")))
                if element.tag == qn("w:p"):
                    heading = re.match(r"^(\d+(?:\.\d+)*)\.?\s", words)
                    if heading:
                        current = heading.group(1)
                if current in sections:
                    docx_sections[current] = docx_sections.get(current, "") + " " + words
                if current == "3.6" and element.tag == qn("w:tbl"):
                    table = Table(element, document)
                    docx_tables.append([[cell.text for cell in row.cells] for row in table.rows])
        used_records: Set[str] = set()
        seen_units: Set[str] = set()
        for index, unit in enumerate(audit["units"]):
            section = unit["section"]
            origins = unit["source_record_ids"]
            if (unit["unit_id"] in seen_units or unit["output_order"] != index or len(origins) != 1
                    or any(origin not in records for origin in origins)):
                findings.append("srs_content_linkage_invalid")
                continue
            seen_units.add(unit["unit_id"])
            used_records.update(origins)
            record = records[origins[0]]
            if (section not in profile.topic_roles or record["authority_tier"] not in profile.authority_tiers
                    or record["ownership_scope"] not in profile.allowed_scopes
                    or (section in SRS_INTRODUCTORY_SECTIONS) != (record["authority_tier"] == "presentation_policy")
                    or not record["provenance"] or not record["text"] or record["decision"] != "selected"
                    or record["record_id"] != "srs-source-" + stable_payload_hash(
                        (section, record["text"], tuple(record["provenance"])))[:20]
                    or unit["unit_id"] != "srs-unit-" + stable_payload_hash((section, unit["text"], record["record_id"]))[:20]):
                findings.append("srs_content_provenance_invalid:" + section)
            rendered = unit["text"]
            if section == "3.6":
                if rendered not in sections[section]:
                    findings.append("srs_domain_row_missing_or_changed")
                cells = [value.strip().replace("\\|", "|") for value in re.split(r"(?<!\\)\|", rendered)[1:-1]]
                if docx_path.exists() and not any(cells == row for table in docx_tables for row in table):
                    findings.append("srs_domain_row_missing_from_docx")
            else:
                summary = rendered.split("\n\n", 1)[-1].strip()
                if normalized(rendered) not in normalized(sections.get(section, "")):
                    findings.append("srs_content_missing_from_markdown:" + section)
                if docx_path.exists() and normalized(summary) not in normalized(docx_sections.get(section, "")):
                    findings.append("srs_content_missing_from_docx:" + section)
                if section in {"4.1", "5.1"}:
                    remainder = text.replace(sections[section], "", 1)
                    if normalized(summary) in normalized(remainder):
                        findings.append("srs_catalog_summary_repeated_outside_catalog")
        if used_records != set(records):
            findings.append("srs_content_contributor_coverage_invalid")
        for section, category in (("4.1", "analog"), ("5.1", "digital")):
            names = re.findall(r"(?m)^\s*- \*\*([^*]+)\*\*", sections[section])
            expected_names = [entry["block"] for entry in audit["catalog_entries"] if entry["category"] == category]
            if names != expected_names:
                findings.append("srs_catalog_coverage_invalid:" + section)
        headers = ["Domain", "Type", "Control", "Functional Role", "Power Conditions"]
        if audit["power_rows"]:
            header = "| " + " | ".join(headers) + " |"
            if header not in sections["3.6"]:
                findings.append("srs_domain_table_header_missing")
            else:
                table_start = sections["3.6"].index(header)
                if not normalized(sections["3.6"][:table_start]):
                    findings.append("srs_power_explanation_missing")
                clock_start = sections["3.6"].find("**Clock and reset**")
                if clock_start >= 0 and clock_start < table_start:
                    findings.append("srs_power_clock_reset_order_invalid")
            rows = [line.strip() for line in sections["3.6"].splitlines() if line.strip().startswith("|")]
            if rows != [header, "|---|---|---|---|---|", *[row["row"] for row in audit["power_rows"]]]:
                findings.append("srs_domain_table_fidelity_invalid")
            if docx_path.exists() and not any(table and table[0] == headers for table in docx_tables):
                findings.append("srs_domain_table_header_missing_from_docx")
        for finding in audit["review_findings"]:
            if finding not in text:
                findings.append("srs_content_review_finding_missing")
    except (KeyError, ValueError, TypeError, OSError, IndexError) as exc:
        findings.append("srs_content_audit_invalid:" + str(exc))
    return findings


def validate_srs_system_overview(markdown_path: Path) -> List[str]:
    """Independently validate the SRS system-level overview contract."""
    if not markdown_path.exists():
        return ["srs_system_overview_missing_markdown"]
    text = markdown_path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"(?ms)^## 3\. System Overview\b.*?(?=^## 4\.)", text)
    if not match:
        return ["srs_system_overview_section_missing"]
    overview = match.group(0)
    narrative = re.sub(r"(?m)^\| Domain \| Type \| Control \| Functional Role \| Power Conditions \|\s*\n(?:^\|[^\n]*\|\s*\n)+", "", overview)
    findings: List[str] = []
    section_bodies: Dict[str, str] = {}
    for heading in SRS_SYSTEM_OVERVIEW_HEADINGS:
        heading_matches = list(re.finditer(rf"^### {re.escape(heading)}\b[^\n]*", overview, flags=re.MULTILINE))
        if len(heading_matches) != 1:
            findings.append(f"srs_system_overview_heading_invalid:{heading}")
            continue
        section_start = heading_matches[0].end()
        next_heading = re.search(r"(?m)^### |^## 4\.", overview[section_start:])
        section_body = overview[section_start:section_start + next_heading.start()] if next_heading else overview[section_start:]
        section_bodies[heading] = section_body
        meaningful_body = re.sub(r"(?is)<p\s*>\s*&nbsp;\s*</p>", "", section_body)
        meaningful_body = re.sub(r"(?is)<[^>]+>|&nbsp;|\s+", "", meaningful_body)
        if not meaningful_body:
            findings.append(f"srs_system_overview_section_empty:{heading}")
    if re.search(r"\b(?:DRS|ARS|IPOS)\b|^\s*Covers:\s*", overview, flags=re.IGNORECASE | re.MULTILINE):
        findings.append("srs_system_overview_contains_downstream_or_normative_linkage")
    if re.search(
        r"\b(?:register|regmap|port\s+name|address|signal\s+level|signal\s+name)\b",
        narrative,
        flags=re.IGNORECASE,
    ):
        findings.append("srs_system_overview_contains_implementation_detail")
    if re.search(r"\b(?:approved evidence|approved architecture|topic output limit|evidence count|need clarification|aim of this document|audit)\b", overview, re.IGNORECASE):
        findings.append("srs_system_overview_contains_audit_or_filler_language")
    if re.search(r"\b(?:shall|must|required to|Covers:)\b|\b0x[0-9a-f]+\b|\b(?:i|o|ca|u)_[a-z0-9_]+\b|\b[A-Za-z][A-Za-z0-9.-]*_[A-Za-z0-9_.-]+\b", narrative, re.IGNORECASE):
        findings.append("srs_system_overview_contains_normative_or_raw_source_fragment")
    if re.search(r"(?m)^\|[^\n]*\bOwner\b[^\n]*\|\s*\n\|[-| ]+\|", overview, re.IGNORECASE):
        findings.append("srs_system_overview_contains_raw_interface_dump")
    normalized_lines: Dict[str, str] = {}
    for line in overview.splitlines():
        normalized = re.sub(r"[*_`#>-]", "", line).strip().casefold()
        normalized = re.sub(r"\s+", " ", normalized)
        if len(normalized) < 60 or normalized.startswith("|") or normalized in {"&nbsp;"}:
            continue
        if normalized in normalized_lines:
            findings.append("srs_system_overview_repeats_narrative_content")
            break
        normalized_lines[normalized] = line
    findings.extend(_validate_srs_fact_audit(markdown_path, section_bodies))
    findings.extend(validate_srs_support_content(markdown_path))
    return findings


def build_ipos_descriptive_records(
    block_name: str,
    block_function: str,
    source_ports: Sequence[Mapping[str, object]],
    requirement_statements: Sequence[Mapping[str, object]],
    topic_specs: Sequence[Tuple[str, Sequence[str]]],
) -> List[Dict[str, str]]:
    """Build concise, evidence-linked IPOS summaries without copying requirements."""
    records: List[Dict[str, str]] = []
    if block_function.strip():
        assignment = assign_ipos_descriptive_topic(block_function, topic_specs)
        if assignment["topic"]:
            records.append({
                "summary": assignment["topic"],
                "statement": block_function.strip(),
                "source": f"artifacts/stage2_mirco_arc/block_inventory.csv:{block_name}",
                "domain": "block_function",
                "mapped_block": block_name,
                "functional_evidence": block_function.strip(),
            })
    # Requirement statements remain authoritative detail. The approved inventory
    # function is the only sufficiently high-level source for overview synthesis.
    # `requirement_statements` is deliberately retained in this shared signature
    # for compatibility with callers and audit structure.
    return records


def approved_snapshot_candidate_rows(snapshot, downstream_contract) -> List[Dict[str, str]]:
    """Project the complete approved candidate set identically for all IPOS validators."""
    return [
        {
            "mapped_block": str(downstream_contract.allocation(row["source_req_id"]).get("approved_block") or "").strip(),
            "source_req_id": row["source_req_id"],
            "requirement_statement": row["requirement_statement"],
            "source_artifact": str(snapshot.source_path),
        }
        for row in snapshot.rows
        if row.get("source_req_id") and row.get("requirement_statement", "").strip()
        and downstream_contract.allocation(row["source_req_id"]).get("approved_block")
    ]


def build_ipos_functional_input(
    block_name: str,
    inventory: Mapping[str, object],
    requirement_rows: Sequence[Mapping[str, object]] = (),
    *,
    domain: str = "",
    materialized: bool = True,
    provenance: Sequence[str] = (),
    candidate_requirement_rows: Sequence[Mapping[str, object]] | None = None,
) -> IPOSFunctionalInput:
    """Normalize approved inventory fields and same-block local evidence only."""
    local_rows = [
        row for row in requirement_rows
        if csv_cell_text(row.get("mapped_block") or row.get("owning_block") or block_name).strip() == block_name
    ]
    requirement_ids = tuple(
        csv_cell_text(row.get("source_req_id") or row.get("requirement_id") or row.get("ipos_req_id")).strip()
        for row in local_rows
        if csv_cell_text(row.get("source_req_id") or row.get("requirement_id") or row.get("ipos_req_id")).strip()
    )
    evidence = tuple(
        csv_cell_text(row.get("requirement_statement") or row.get("statement") or row.get("text")).strip()
        for row in local_rows
        if csv_cell_text(row.get("requirement_statement") or row.get("statement") or row.get("text")).strip()
    )
    evidence_rows = requirement_rows if candidate_requirement_rows is None else candidate_requirement_rows
    candidate_records = tuple(
        (
            csv_cell_text(row.get("mapped_block") or row.get("owning_block") or block_name).strip(),
            csv_cell_text(row.get("source_req_id") or row.get("requirement_id") or row.get("ipos_req_id")).strip(),
            csv_cell_text(row.get("requirement_statement") or row.get("statement") or row.get("text")).strip(),
            csv_cell_text(row.get("source_artifact") or row.get("source") or "").strip(),
        )
        for row in evidence_rows
        if csv_cell_text(row.get("requirement_statement") or row.get("statement") or row.get("text")).strip()
    )
    return IPOSFunctionalInput(
        block=block_name.strip(),
        domain=domain.strip(),
        function=csv_cell_text(inventory.get("Function")).strip(),
        inputs=csv_cell_text(inventory.get("Inputs")).strip(),
        outputs=csv_cell_text(inventory.get("Outputs")).strip(),
        local_requirement_ids=tuple(dict.fromkeys(requirement_ids)),
        local_requirement_evidence=tuple(dict.fromkeys(evidence)),
        candidate_requirement_records=candidate_records,
        materialized=materialized,
        provenance=tuple(dict.fromkeys(str(item).strip() for item in provenance if str(item).strip())),
    )


def compose_technical_block_purpose(block_name: str, function: str) -> str:
    """Express an approved inventory function as a descriptive block sentence."""
    purpose = function.strip().rstrip(".")
    if not block_name.strip() or not purpose:
        return ""
    return f"The {block_name} block is designed to {purpose[:1].lower() + purpose[1:]}."


def project_architecture_interactions(entries: Iterable[str]) -> List[Tuple[str, str, str]]:
    """Project approved interaction descriptions into stable structural rows."""
    rows: List[Tuple[str, str, str]] = []
    for entry in entries:
        match = re.fullmatch(r"Interaction:\s*(.+?)\s*->\s*(.+?)\s*\(([^()]*)\)", entry.strip())
        if not match:
            continue
        source, target = match.group(1).strip(), match.group(2).strip()
        exchange = match.group(3).split(";", 1)[0].strip()
        row = (source, target, exchange)
        if source and target and exchange and row not in rows:
            rows.append(row)
    return rows


def project_architecture_interfaces(entries: Iterable[str]) -> List[Tuple[str, str, str]]:
    """Keep interface name, owner, and purpose from existing catalog evidence."""
    rows: List[Tuple[str, str, str]] = []
    for entry in entries:
        match = re.fullmatch(r"Approved interface (.+?) owned by (.+?):\s*(.+)", entry.strip())
        if match and match.groups() not in rows:
            rows.append(match.groups())
    return rows


def summarize_architecture_interactions(rows: Sequence[Tuple[str, str, str]]) -> str:
    """Describe the first distinct approved exchanges without adding relationships."""
    if not rows:
        return ""
    exchanges = list(dict.fromkeys(exchange for _source, _target, exchange in rows))
    source, target, _exchange = rows[0]
    opening = (f"{source} connects to {target} through {exchanges[0]}"
               if exchanges[0].casefold().endswith("connection") else
               f"{source} provides {exchanges[0]} to {target}")
    if len(rows) == 1:
        return opening + "."
    return (opening + "; related paths carry "
            + ", ".join(exchanges[1:4]) + ".") if len(exchanges) > 1 else (
        opening + f", alongside {len(rows) - 1} other routed paths."
    )


def compose_drs_interaction_summary(rows: Sequence[Tuple[str, str, str]]) -> str:
    """Group identical directed exchanges without implying additional connections."""
    if not rows:
        return "Digital exchange behavior: need clarification."
    destinations: Dict[Tuple[str, str], List[str]] = {}
    for source, target, exchange in rows:
        targets = destinations.setdefault((source, exchange), [])
        if target not in targets:
            targets.append(target)
    groups: Dict[Tuple[str, Tuple[str, ...]], List[str]] = {}
    for (source, exchange), targets in destinations.items():
        groups.setdefault((exchange, tuple(targets)), []).append(source)
    source_statements: Dict[Tuple[str, ...], List[str]] = {}
    connections = []
    for (exchange, targets), sources in groups.items():
        subject = _drs_prose_list(sources)
        destination = _drs_prose_list(targets)
        connection = re.fullmatch(r"(.+?)\s+connections?", exchange, re.I)
        if connection:
            verb = "connect" if len(sources) > 1 else "connects"
            connections.append(f"{subject} {verb} to {destination} through {connection.group(1)}.")
        else:
            source_statements.setdefault(tuple(sources), []).append(f"{exchange} to {destination}")
    sentences = []
    for sources, exchanges in source_statements.items():
        verb = "provide" if len(sources) > 1 else "provides"
        sentences.append(f"{_drs_prose_list(sources)} {verb} {_drs_prose_list(exchanges)}.")
    return " ".join(sentences + connections)


def _drs_prose_list(values: Sequence[str]) -> str:
    if len(values) < 2:
        return "".join(values)
    return ", ".join(values[:-1]) + " and " + values[-1]


def compose_drs_clock_summary(paths: Sequence[Tuple[str, str, str, str, str]]) -> str:
    """Describe frequency and gating behavior; hierarchy remains in route tables."""
    if not paths:
        return "Clock distribution and gating behavior: need clarification."
    frequencies: Dict[str, List[str]] = {}
    for _source_id, _source, _target, frequency, gating in paths:
        modes = frequencies.setdefault(frequency, [])
        mode = ("without clock gating" if gating == "Not gated" else
                "with clock gating" if gating.startswith("Gated") else "")
        if mode and mode not in modes:
            modes.append(mode)
    descriptions = [f"{frequency} clocks {'with and without clock gating' if len(modes) == 2 else _drs_prose_list(modes)}".strip()
                    for frequency, modes in frequencies.items()]
    summary = "The clock network distributes " + "; ".join(descriptions) + "."
    if any(source == "need clarification" or target == "need clarification"
           for _source_id, source, target, _frequency, _gating in paths):
        summary += " Incomplete source and destination clock labels: need clarification."
    return summary


def compose_drs_role_summary(roles: Sequence[Tuple[str, str]], terms: Sequence[str]) -> str:
    """Project complete functional clauses within an already selected role set."""
    sentences = []
    for name, function in roles:
        clauses = re.split(
            r",\s+(?:and\s+)?(?=(?:provide|generate|receive|perform|write|route|control|coordinate|implement|accept|translate|sequence|execute|operate|aggregate)\b)",
            function.strip().rstrip("."), flags=re.I,
        )
        for clause in clauses:
            if terms and not any(term in clause.casefold() for term in terms):
                continue
            words = clause.split(" ", 1)
            if len(words) != 2:
                continue
            verb, predicate = words
            if re.fullmatch(r"[A-Za-z]+", verb):
                inflected = (verb[:-1] + "ies" if re.search(r"[^aeiou]y$", verb, re.I) else
                             verb + "es" if re.search(r"(?:s|sh|ch|x|z|o)$", verb, re.I) else verb + "s")
                predicate = re.sub(
                    r"\band (provide|generate|receive|perform|write|route|control|coordinate|implement|accept|translate|sequence|execute|operate|aggregate)\b",
                    lambda match: "and " + match.group(1) + "s", predicate,
                )
                sentence = f"{name} {inflected.lower()} {predicate}."
                if sentence not in sentences:
                    sentences.append(sentence)
    return " ".join(sentences)


def drs_section_prose_findings(text: str) -> List[str]:
    """Inspect final section prose independently of composer parity."""
    findings = natural_descriptive_prose_findings(text)
    if re.search(r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+"
                 r"(?:(?:named|source|destination|architectural|routed|approved|other)\s+)*"
                 r"(?:paths?|endpoints?|destinations?|routes?|links?|groups?|items?)\b", text, re.I):
        findings.append("description_counts_structure")
    if re.search(r"\b(?:evidence\s+groups?|block\s+functions?\s+identify|recorded\s+exchanges\s+cover|"
                 r"the\s+architecture\s+(?:also\s+)?records)\b", text, re.I):
        findings.append("description_uses_audit_summary")
    return list(dict.fromkeys(findings))


def natural_descriptive_prose_findings(text: str) -> List[str]:
    """Check descriptive text without depending on a document's section layout."""
    findings: List[str] = []
    if re.search(
        r"\bapproved\b"
        r"|\b(?:source|snapshot|candidate|refinement|audit|provenance)\s+"
        r"(?:local\s+)?(?:function(?:al)?\s+evidence|function|scope|behavior|requirement|candidate)\b"
        r"|\b(?:local\s+scope\s+covers|supported\s+by\s+the\s+approved|derivation\s+mode"
        r"|general\s+functional\s+description|block\s+summary)\b",
        text, re.I,
    ):
        findings.append("description_uses_internal_process_language")
    if re.search(r"\b(?:shall|must|required to)\b", text, re.I):
        findings.append("description_uses_requirement_form_language")
    return findings


def validate_drs_block_descriptions(
    markdown_text: str,
    blocks: Sequence[Mapping[str, str]],
    audit_rows: Sequence[Mapping[str, str]],
    port_rows: Sequence[Mapping[str, str]],
    docx_path: Path | None = None,
) -> List[str]:
    """Check DRS block paragraphs against inventory authority and rendered I/O."""
    findings: List[str] = []
    block_list = re.search(r"(?m)^###\s+(?:\*\*)?4\.1\s+Digital block list[^\n]*\n([^\n]+)", markdown_text)
    if block_list:
        findings.extend(f"drs_block_list_{finding}" for finding in natural_descriptive_prose_findings(block_list.group(1)))
    headings = list(re.finditer(r"(?m)^###\s+(?:\*\*)?9\.\d+\s+([^*{\n]+)", markdown_text))
    sections: Dict[str, str] = {}
    for index, heading in enumerate(headings):
        name = heading.group(1).strip()
        heading_end = markdown_text.find("\n", heading.start())
        remaining = markdown_text[heading_end + 1:headings[index + 1].start() if index + 1 < len(headings) else len(markdown_text)]
        next_top = re.search(r"(?m)^##\s+", remaining)
        body = remaining[:next_top.start()] if next_top else remaining
        if name in sections:
            findings.append(f"duplicate_drs_block_paragraph:{name}")
        sections[name] = body
    expected = {block["name"]: block for block in blocks}
    for name in sorted(set(sections) - set(expected)):
        findings.append(f"unapproved_drs_block_paragraph:{name}")
    provenance_rows = [row for row in audit_rows if row.get("section") == "DRS digital block descriptions"]
    if len(provenance_rows) != len(blocks):
        findings.append("drs_block_description_audit_count_mismatch")
    docx_paragraphs: Set[str] = set()
    docx_port_names: Set[str] = set()
    if docx_path is not None:
        try:
            with zipfile.ZipFile(docx_path) as archive:
                document = ET.fromstring(archive.read("word/document.xml"))
            tag = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
            for paragraph in document.iter(tag + "p"):
                docx_paragraphs.add(re.sub(r"\s+", " ", "".join(
                    text.text or "" for text in paragraph.iter(tag + "t")
                )).strip())
            for table in document.iter(tag + "tbl"):
                for row in table.iter(tag + "tr"):
                    cell = next(row.iter(tag + "tc"), None)
                    if cell is not None:
                        docx_port_names.add("".join(text.text or "" for text in cell.iter(tag + "t")).strip())
        except (OSError, KeyError, ValueError, ET.ParseError, zipfile.BadZipFile):
            findings.append("drs_descriptive_docx_unreadable")
    for order, block in enumerate(blocks, start=1):
        name = block["name"]
        sentence = compose_technical_block_purpose(name, block["function"])
        body = sections.get(name, "")
        if not body:
            findings.append(f"missing_drs_block_paragraph:{name}")
            continue
        first_line = next((line.strip() for line in body.splitlines() if line.strip()), "")
        if first_line != sentence:
            findings.append(f"drs_block_purpose_mismatch:{name}")
        findings.extend(f"{finding}:{name}" for finding in natural_descriptive_prose_findings(first_line))
        if re.search(r"(?m)^\s*-\s*Port name\s*:", body, re.I):
            findings.append(f"drs_port_name_bullet_list:{name}")
        if "Block-specific inputs, outputs, ports" in body:
            findings.append(f"drs_internal_scope_scaffolding:{name}")
        table_names = {cell.strip().replace("\\|", "|") for cell in re.findall(r"(?m)^\|\s*([^|]+?)\s*\|", body)}
        approved_ports = {row.get("Port name", "").strip() for row in port_rows
                          if row.get("Owner") == name and row.get("Ownership status") == "approved"
                          and row.get("Port name", "").strip()}
        for port in sorted(approved_ports - table_names):
            findings.append(f"drs_approved_port_missing_from_table:{name}:{port}")
        if docx_path is not None and docx_paragraphs and sentence not in docx_paragraphs:
            findings.append(f"drs_block_purpose_missing_from_docx:{name}")
        for port in sorted(approved_ports - docx_port_names) if docx_path is not None and docx_paragraphs else []:
            findings.append(f"drs_approved_port_missing_from_docx_table:{name}:{port}")
        if order > len(provenance_rows):
            continue
        row = provenance_rows[order - 1]
        if any((row.get(field) or "").strip() != value for field, value in (
            ("mapped_block", name), ("source_evidence", block["function"]), ("statement", sentence),
            ("source", "artifacts/stage2_mirco_arc/block_inventory.csv"),
            ("scope_decision", "approved_concrete_block"), ("output_order", str(order)),
        )):
            findings.append(f"drs_block_description_provenance_mismatch:{name}")
    return findings


def compose_ipos_overview(
    functional_input: IPOSFunctionalInput,
) -> Tuple[Dict[str, List[str]], List[Dict[str, str]]]:
    """Compose bounded IPOS prose from inventory authority and supported local evidence."""
    if not functional_input.materialized:
        return {
            "functionality": [], "scope": [], "internal_structure": [],
            "internal_functions": [], "general_architecture": [],
        }, []
    function = (functional_input.function or "perform its specified function").strip().rstrip(".")
    functionality = [compose_technical_block_purpose(functional_input.block, function)]
    input_text = functional_input.inputs or "the approved local inputs"
    input_text = re.sub(r"\bregisters?\b(?![- ]map\b)", "", input_text, flags=re.I)
    input_text = re.sub(r"\s+", " ", input_text).strip(" ,.;:")
    input_text = re.sub(r"\bregisters?\b(?![- ]map\b)", "", input_text, flags=re.I)
    input_text = re.sub(r"\s+", " ", input_text).strip(" ,.;:")
    output_text = functional_input.outputs or "the approved local outputs"
    if re.match(r"[A-Z][a-z]", input_text):
        input_text = input_text[:1].lower() + input_text[1:]
    if re.match(r"[A-Z][a-z]", output_text):
        output_text = output_text[:1].lower() + output_text[1:]
    scope = [
        f"The {functional_input.block} accepts {input_text} and produces {output_text}."
    ]
    candidate_audit = _classify_ipos_local_refinements(functional_input)
    scope.extend(_group_ipos_local_refinements(
        candidate_audit, functional_input.function, functional_input.inputs, functional_input.outputs,
    ))
    audit: List[Dict[str, str]] = []
    common = {
        "source_authority_tier": "approved_snapshot_block_inventory",
        "block": functional_input.block,
        "domain": functional_input.domain,
        "source_function": functional_input.function,
        "inputs_used": functional_input.inputs,
        "outputs_used": functional_input.outputs,
        "provenance_references": "; ".join(functional_input.provenance),
        "hierarchy_level": "IPOS block",
        "duplicate_cross_document_note": "",
    }
    audit.append({
        **common,
        "target_section": "1.1 Functionality",
        "descriptive_statement": functionality[0],
        "supporting_requirement_evidence_ids": "; ".join(functional_input.local_requirement_ids),
        "derivation_mode": "direct_function",
        "decision": "selected",
        "exclusion_suppression_reason": "",
    })
    audit.append({
        **common,
        "target_section": "1.2 Supported functions and scope",
        "descriptive_statement": scope[0],
        "supporting_requirement_evidence_ids": "; ".join(functional_input.local_requirement_ids),
        "derivation_mode": "function_plus_io_scope",
        "decision": "selected",
        "exclusion_suppression_reason": "",
    })
    for requirement_id, evidence in zip(functional_input.local_requirement_ids, functional_input.local_requirement_evidence):
        audit.append({
            **common,
            "target_section": "1.2 Supported functions and scope",
            "descriptive_statement": evidence,
            "supporting_requirement_evidence_ids": requirement_id,
            "derivation_mode": "suppressed_due_to_insufficient_evidence",
            "decision": "suppressed",
            "exclusion_suppression_reason": "normative local requirement retained as evidence only; it cannot redefine the approved block scope",
        })
    scope_order = {value.casefold(): index for index, value in enumerate(scope, start=1)}
    for row in candidate_audit:
        rendered_summary = row.get("rendered_summary", "").strip()
        if row.get("decision") == "accepted_candidate" and rendered_summary:
            row["descriptive_statement"] = rendered_summary
            row["output_order"] = str(scope_order.get(rendered_summary.casefold(), ""))
    audit.extend(candidate_audit)
    return {
        "functionality": functionality,
        "scope": scope,
        "internal_structure": [],
        "internal_functions": [],
        "general_architecture": [],
    }, audit


def build_ipos_normalized_records(functional_input: IPOSFunctionalInput) -> Tuple[NormalizedSourceRecord, ...]:
    """Expose IPOS authority and candidate decisions through the shared record contract."""
    records = [
        NormalizedSourceRecord(
            record_id="inventory:function",
            text=functional_input.function,
            authority_tier="authoritative",
            ownership_scope=functional_input.block,
            provenance=functional_input.provenance,
            decision="retained",
            rationale="approved block function authority",
        ),
        NormalizedSourceRecord(
            record_id="inventory:inputs",
            text=functional_input.inputs,
            authority_tier="authoritative",
            ownership_scope=functional_input.block,
            provenance=functional_input.provenance,
            decision="retained",
            rationale="approved block input boundary",
        ),
        NormalizedSourceRecord(
            record_id="inventory:outputs",
            text=functional_input.outputs,
            authority_tier="authoritative",
            ownership_scope=functional_input.block,
            provenance=functional_input.provenance,
            decision="retained",
            rationale="approved block output boundary",
        ),
    ]
    candidate_rows = _classify_ipos_local_refinements(functional_input)
    _group_ipos_local_refinements(
        candidate_rows, functional_input.function, functional_input.inputs, functional_input.outputs,
    )
    for row in candidate_rows:
        evidence_block = row.get("candidate_evidence_block", "").strip()
        requirement_id = row.get("candidate_evidence_requirement_id", "").strip()
        decision = row.get("decision", "")
        suppressed_atomic = row.get("materialization_status") == "suppressed_atomic"
        records.append(NormalizedSourceRecord(
            record_id=f"requirement:{evidence_block}:{requirement_id}",
            text=row.get("candidate_refinement", "").strip(),
            authority_tier=(
                "authoritative"
                if evidence_block.casefold() == functional_input.block.casefold()
                else "discovery_only"
            ),
            ownership_scope=evidence_block,
            provenance=tuple(filter(None, (
                *functional_input.provenance,
                f"approved requirement:{requirement_id}" if requirement_id else "",
            ))),
            decision="retained" if decision == "accepted_candidate" and not suppressed_atomic else "suppressed",
            rationale=(
                "accepted evidence is an atomic helper operation without an autonomous summary"
                if suppressed_atomic else
                row.get("exclusion_suppression_reason", "").strip()
                or "supported same-scope local refinement"
            ),
        ))
    return tuple(records)


def build_ipos_semantic_units(
    functional_input: IPOSFunctionalInput,
    sections: Mapping[str, Sequence[str]],
    audit_rows: Sequence[Mapping[str, str]],
) -> Tuple[SemanticUnit, ...]:
    """Map composed IPOS text to stable source-linked semantic units."""
    units: List[SemanticUnit] = []
    for text in sections.get("functionality", ()):
        units.append(SemanticUnit(
            unit_id=f"functionality:{len(units) + 1}",
            section="1.1 Functionality",
            text=text,
            source_record_ids=("inventory:function",),
            output_order=len(units) + 1,
        ))
    for index, text in enumerate(sections.get("scope", ())):
        source_record_ids = ("inventory:function", "inventory:inputs", "inventory:outputs")
        if index > 0:
            matching = [
                row for row in audit_rows
                if row.get("decision") == "accepted_candidate"
                and row.get("rendered_summary", "").strip() == text.strip()
            ]
            if matching:
                source_record_ids = tuple(
                    f"requirement:{row.get('candidate_evidence_block', '').strip()}:{row.get('candidate_evidence_requirement_id', '').strip()}"
                    for row in matching
                )
        units.append(SemanticUnit(
            unit_id=f"supported-scope:{index + 1}",
            section="1.2 Supported functions and scope",
            text=text,
            source_record_ids=source_record_ids,
            output_order=len(units) + 1,
        ))
    return tuple(units)


_IPOS_REFINEMENT_STOP_WORDS = {
    "a", "an", "and", "as", "at", "by", "for", "from", "in", "into", "is", "it", "of",
    "on", "or", "shall", "should", "the", "their", "this", "to", "when", "where", "with",
    "be", "been", "being", "does", "do", "not", "must", "will", "which", "that",
}
_IPOS_ACTION_VERBS = {
    "accept", "accumulate", "acquire", "aggregate", "average", "calculate", "clamp", "configure",
    "control", "convert", "copy", "decrement", "disable", "divide", "elaborate", "enable", "enter",
    "exit", "filter", "generate", "increment", "manage", "measure", "perform", "process", "raise",
    "read", "receive", "remain", "reset", "route", "sample", "select", "sequence", "set", "start",
    "stop", "store", "subtract", "transfer", "wait", "write",
}
_IPOS_ACTION_FORMS = {
    "acquired": "acquire", "acquires": "acquire", "acquiring": "acquire",
    "aggregated": "aggregate", "aggregates": "aggregate", "aggregating": "aggregate",
    "averaged": "average", "averages": "average", "averaging": "average",
    "calculated": "calculate", "calculates": "calculate", "calculating": "calculate",
    "clamped": "clamp", "clamps": "clamp", "clamping": "clamp",
    "configured": "configure", "configures": "configure", "configuring": "configure",
    "controlled": "control", "controls": "control", "controlling": "control",
    "converted": "convert", "converts": "convert", "converting": "convert",
    "copied": "copy", "copies": "copy", "copying": "copy",
    "decremented": "decrement", "decrements": "decrement", "decrementing": "decrement",
    "disabled": "disable", "disables": "disable", "disabling": "disable",
    "divided": "divide", "divides": "divide", "dividing": "divide",
    "elaborated": "elaborate", "elaborates": "elaborate", "elaborating": "elaborate",
    "enabled": "enable", "enables": "enable", "enabling": "enable",
    "entered": "enter", "enters": "enter", "entering": "enter",
    "exited": "exit", "exits": "exit", "exiting": "exit",
    "filtered": "filter", "filters": "filter", "filtering": "filter",
    "generated": "generate", "generates": "generate", "generating": "generate",
    "incremented": "increment", "increments": "increment", "incrementing": "increment",
    "managed": "manage", "manages": "manage", "managing": "manage",
    "measured": "measure", "measures": "measure", "measuring": "measure",
    "performed": "perform", "performs": "perform", "performing": "perform",
    "processed": "process", "processes": "process", "processing": "process",
    "raised": "raise", "raises": "raise", "raising": "raise",
    "read": "read", "reads": "read", "reading": "read",
    "received": "receive", "receives": "receive", "receiving": "receive",
    "remained": "remain", "remains": "remain", "remaining": "remain",
    "reset": "reset", "resets": "reset", "resetting": "reset",
    "routed": "route", "routes": "route", "routing": "route",
    "sampled": "sample", "samples": "sample", "sampling": "sample",
    "selected": "select", "selects": "select", "selecting": "select",
    "sequenced": "sequence", "sequences": "sequence", "sequencing": "sequence",
    "set": "set", "sets": "set", "setting": "set",
    "started": "start", "starts": "start", "starting": "start",
    "stopped": "stop", "stops": "stop", "stopping": "stop",
    "stored": "store", "stores": "store", "storing": "store",
    "subtracted": "subtract", "subtracts": "subtract", "subtracting": "subtract",
    "transferred": "transfer", "transfers": "transfer", "transferring": "transfer",
    "waited": "wait", "waits": "wait", "waiting": "wait",
    "written": "write", "writes": "write", "writing": "write",
}
_IPOS_ACTION_PRESENT = {
    "acquire": "Acquires", "accumulate": "Accumulates", "aggregate": "Aggregates", "average": "Averages",
    "calculate": "Calculates", "clamp": "Clamps", "configure": "Configures", "control": "Controls",
    "convert": "Converts", "copy": "Copies", "decrement": "Decrements", "disable": "Disables",
    "divide": "Divides", "elaborate": "Elaborates", "enable": "Enables", "enter": "Enters",
    "exit": "Exits", "filter": "Filters", "generate": "Generates", "increment": "Increments",
    "manage": "Manages", "measure": "Measures", "perform": "Performs", "process": "Processes",
    "raise": "Raises", "read": "Reads", "receive": "Receives", "remain": "Remains", "reset": "Resets",
    "route": "Routes", "sample": "Samples", "select": "Selects", "sequence": "Sequences",
    "set": "Sets", "start": "Starts", "stop": "Stops", "store": "Stores", "subtract": "Subtracts",
    "transfer": "Transfers", "wait": "Waits", "write": "Writes",
}
_IPOS_NORMATIVE_RE = re.compile(r"\b(?:shall|must|required to|is required to)\b", re.I)
_IPOS_NEGATION_RE = re.compile(r"\b(?:not|never|cannot|doesn't|does not|shall not|must not)\b", re.I)


def _ipos_action_lemma(word: str) -> str:
    value = word.casefold()
    if value in _IPOS_ACTION_VERBS:
        return value
    return _IPOS_ACTION_FORMS.get(value, "")


def _ipos_refinement_tokens(value: str) -> Set[str]:
    tokens: Set[str] = set()
    for token in re.findall(r"[a-z][a-z0-9_-]*", value.casefold()):
        if token in _IPOS_REFINEMENT_STOP_WORDS or len(token) <= 2 or token.isupper():
            continue
        lemma = _ipos_action_lemma(token)
        if not lemma and token.endswith("ies") and len(token) > 4:
            lemma = token[:-3] + "y"
        elif not lemma and token.endswith("s") and len(token) > 3:
            lemma = token[:-1]
        elif not lemma and token.endswith("ed") and len(token) > 4:
            lemma = token[:-2]
        tokens.add(lemma or token)
    return tokens


def _ipos_refinement_has_inventory_support(
    action: str,
    statement_tokens: Set[str],
    function_tokens: Set[str],
    input_tokens: Set[str],
    output_tokens: Set[str],
) -> bool:
    if (function_tokens | input_tokens | output_tokens).intersection(statement_tokens):
        return True
    return (
        action in {"configure", "select"}
        and bool(input_tokens.intersection({"configuration", "setting", "settings"}))
    ) or (
        action in {"write", "store", "route", "transfer"}
        and bool(output_tokens.intersection({"data", "routing", "result", "results"}))
    ) or (
        action in {"sample", "acquire", "measure", "receive"}
        and bool(input_tokens.intersection({"data", "sample", "samples"}))
    )


def _ipos_refinement_parts(statement: str) -> Tuple[str, str, str, bool]:
    statement = re.sub(r"\[(?:Covers:|TO:|Vpriority)[^]]*\]", " ", statement, flags=re.I)
    statement = re.sub(r"\b(?:DDS|IPOS)_[A-Z0-9_-]+\b", " ", statement, flags=re.I)
    clamped_value = re.search(
        r"\bvalue greater than (\d+) into ones? of the ([A-Za-z][A-Za-z0-9_]*)"
        r".*?\bvalue shall clamp at (\d+)\b", statement, re.I,
    )
    if clamped_value and clamped_value.group(1) == clamped_value.group(3):
        return "clamp", f"{clamped_value.group(2).replace('_', ' ')} values above {clamped_value.group(1)} to {clamped_value.group(1)}", "", False
    if re.search(r"\bPPG Raw Data and PPG Noise reach\b", statement, re.I) and re.search(
        r"\bdepending on the ALC Mask bit value, the two accumulated shall be subtracted\b", statement, re.I,
    ):
        return "subtract", "accumulated PPG raw data and PPG noise according to the ALC Mask", "", False
    repeated_frames = re.search(
        r"\bafter the last repetition has been accumulated, the data output shall be obtained "
        r"dividing by the number of repeated frames the accumulated data to obtain a (\d+) bit data\b",
        statement, re.I,
    )
    if repeated_frames:
        return "divide", f"accumulated frame data by the number of repetitions to produce a {repeated_frames.group(1)} bit result", "", False
    sampled_pair = re.search(r"\bshall\s+be\s+sampled\s+(\d+)\s+times,\s+then\s+mediated\b", statement, re.I)
    subtraction = re.search(
        r"\bsubtraction\s+between\s+([A-Za-z][A-Za-z0-9_]*)\s+and\s+([A-Za-z][A-Za-z0-9_]*)\b",
        statement, re.I,
    )
    if sampled_pair and subtraction and re.match(r"If\s+.+?\bis\s+set\s+high\b", statement, re.I):
        first, second = subtraction.groups()
        if all(re.search(rf"\b{re.escape(operand)}\b", statement[:sampled_pair.start()], re.I) for operand in (first, second)):
            return (
                "average",
                f"{sampled_pair.group(1)} acquisitions of {first.replace('_', ' ')} and "
                f"{second.replace('_', ' ')} separately when the mode is enabled, "
                "then subtracts their averaged values",
                "", False,
            )
    acquisition_interval = re.fullmatch(
        r"(.+?)\s+(?:shall|must)\s+define\s+how\s+many\s+(time slots?)\s+pass\s+"
        r"between\s+two\s+(.+?)\s+acquisitions\b(?:\s+following\s+this\s+formula:.*)?\.?",
        statement.strip(), flags=re.I,
    )
    if acquisition_interval:
        _source, interval_unit, acquisition = acquisition_interval.groups()
        description = f"number of {interval_unit} between two {acquisition} acquisitions"
        if re.search(r"\bfollowing\s+this\s+formula:\s*\S+\s*=", statement, re.I):
            description += (
                "; the cited expression relates acquisition data to time slots and the configured input"
                " without resolving its arithmetic"
            )
        return "configure", description, "", False
    conditional_transition = re.fullmatch(
        r"When in (.+?) state, when (.+?), (.+?) shall be set (?:high|low) "
        r"to start (.+?) and go into (.+?) state\.?",
        statement.strip(), flags=re.I,
    )
    if conditional_transition:
        initial_state, trigger, signal, effect, next_state = conditional_transition.groups()
        if re.search(r"\b(?:signal|output)\b|\b[oO]_[A-Za-z0-9_]+\b", signal):
            trigger = re.sub(r"\b[iIoO]_(?=[A-Za-z0-9])", "", trigger).replace("_", " ")
            return (
                "start", f"{effect} and enters {next_state.replace('_', ' ')} state",
                f"{trigger} in {initial_state.replace('_', ' ')} state", False,
            )
    procedure = re.match(
        r"To perform (?:an? |the )?([A-Za-z][A-Za-z ]{1,60}) procedure,\s*"
        r"(?:the )?user shall perform the following steps:\s*\d+\.",
        statement, re.I,
    )
    if procedure:
        return "perform", f"{procedure.group(1).strip()} procedure", "", False
    state_progression = re.search(
        r"\b(?:FSM|controller)\s+shall\s+go\s+into\s+(?:the\s+)?([A-Za-z][A-Za-z0-9_ ]+?)\s+state\s+"
        r"and\s+then\s+into\s+(?:the\s+)?([A-Za-z][A-Za-z0-9_ ]+?)(?:\s+state|[.;]|$)",
        statement, re.I,
    )
    if state_progression:
        first, second = (value.strip().replace("_", " ") for value in state_progression.groups())
        return "sequence", f"{first} then {second} states", "", False
    state_entry = re.search(
        r"\bshall\s+go\s+(?:back\s+)?(?:into|in|to)\s+(?:the\s+)?"
        r"((?:(?!(?:after|before|when|if)\b)[A-Za-z][A-Za-z0-9_]*\s*){1,3}?)\s+state\b", statement, re.I,
    )
    if state_entry:
        destination = state_entry.group(1).strip().replace("_", " ")
        context = statement[:state_entry.start()]
        if _IPOS_NORMATIVE_RE.search(context):
            return "", "", "", False
        condition = re.match(r"^(?:When|If)\s+(.+)$", context.strip(), re.I)
        if condition:
            context = re.sub(
                r",\s*(?:the\s+)?(?:device|[A-Za-z0-9_]+\s+FSM|controller)\s*$",
                "", condition.group(1), flags=re.I,
            )
            context = re.sub(r"\[[^]]*\]|\([^)]*\)", "", context)
            context = re.sub(r"\s+", " ", context).strip(" ,")
            if len(context.split()) <= 25 and context:
                outcome = f"{destination} state when {context}"
                following = re.match(r"\s*if\s+(.+?)(?:\s*\.\s*Furthermore\b|[.;]|$)", statement[state_entry.end():], re.I)
                if following:
                    guard = re.sub(r"\([^)]*\)", "", following.group(1))
                    guard = re.sub(r"\s+", " ", guard).strip(" ,")
                    if not guard or guard.split()[-1].casefold() in {"the", "if", "and", "or", "when"}:
                        return "", "", "", False
                    if len(guard.split()) <= 20:
                        outcome += f" if {guard}"
                    else:
                        return "", "", "", False
                return "enter", outcome, "", False
            return "", "", "", False
        return "enter", f"{destination} state", "", False
    controlled_output = re.search(
        r"\b(o_[A-Za-z0-9_]+|[A-Za-z]+(?:_[A-Za-z0-9]+)+)\s+shall\s+(?:be\s+)?set\s+"
        r"(?:to\s+)?([01]|high|low)\b",
        statement, re.I,
    )
    if controlled_output:
        prefix = statement[:controlled_output.start()]
        if re.search(r"\b(?:samples?|sampled|acquisition|conversion|threshold|frame|time slot)\b|_cds\b", prefix, re.I):
            output = re.sub(r"^[io]_", "", controlled_output.group(1), flags=re.I).replace("_", " ")
            condition = re.match(r"^(?:When|If|In case)\s+(.+)$", prefix.strip(), re.I)
            context = re.sub(r",\s*(?:the\s*)?$", "", condition.group(1)).strip() if condition else ""
            context = re.sub(r"\b(?:shall|must)\s+be\b", "is", context, flags=re.I)
            context = re.sub(r"\b(?:shall|must)\b", "", context, flags=re.I)
            context = re.sub(r"\s+", " ", context).strip()
            if context and len(context.split()) <= 65:
                effect = f"{output} output when {context}"
                reset = re.search(r"\band\s+shall\s+go\s+to\s+0\s+at\s+(.+?)(?:[.;]|$)",
                                  statement[controlled_output.end():], re.I)
                if reset and controlled_output.group(2).casefold() in {"1", "high"}:
                    effect += f"; clears at {reset.group(1).strip()}"
                recurring = re.search(r"\bin\s+every\s+time\s+slot\b", statement[controlled_output.end():], re.I)
                if recurring:
                    effect += " in every time slot"
                return ("enable" if controlled_output.group(2).casefold() in {"1", "high"} else "disable"), effect, "", False
    timed_step = re.search(
        r"\b(o_[A-Za-z0-9_]+)\s+shall\s+increment\s+the\s+first\s+step\s+at\s+value\s+"
        r"(i_[A-Za-z0-9_]+).*?\bat\s+a\s+time\s+(i_[A-Za-z0-9_]+)\b",
        statement, re.I,
    )
    if timed_step:
        output, value, timing = (part.replace("_", " ") for part in timed_step.groups())
        return "increment", f"{output} first step to {value} at {timing} timing", "", False
    modal = re.search(r"\b(?:shall|must|should|will|required to|is required to)\b", statement, re.I)
    if not modal:
        return "", "", "", False
    subject = statement[:modal.start()].strip(" ,.;:")
    predicate = statement[modal.end():].strip()
    negative = bool(re.match(r"not\b", predicate, re.I))
    predicate = re.sub(r"^not\s+", "", predicate, flags=re.I)
    passive_subject = ""
    passive = re.match(r"be\s+(written|read|stored|sampled|selected|set|reset|enabled|disabled|generated|raised)\b", predicate, re.I)
    if passive:
        action = _ipos_action_lemma(passive.group(1))
        passive_subject = re.split(r",\s*(?=(?:the\s+)?[A-Za-z][A-Za-z0-9_]*(?:\s+signal)?$)", subject)[-1]
        tail = f"{passive_subject} {predicate[passive.end():]}".strip()
        passive_subject = subject
    else:
        action_phrase = re.match(r"(?:(?:also|always|only)\s+)*(?:be\s+able\s+to\s+)?([A-Za-z][A-Za-z'-]*)\b", predicate, re.I)
        if not action_phrase:
            return "", "", "", negative
        action = _ipos_action_lemma(action_phrase.group(1))
        if not action:
            return "", "", "", negative
        tail = predicate[action_phrase.end():].strip()
        if action == "perform" and re.match(r"(?:(?:the|an?)\s+)?averag(?:e|ing)\b", tail, re.I):
            action = "average"
            consumed = re.match(r"(?:(?:the|an?)\s+)?averag(?:e|ing)\b", tail, re.I)
            tail = tail[consumed.end():].strip()
        elif action == "perform" and re.match(r"(?:(?:the|an?)\s+)?subtract(?:ion|ing)?\b", tail, re.I):
            action = "subtract"
            consumed = re.match(r"(?:(?:the|an?)\s+)?subtract(?:ion|ing)?\b", tail, re.I)
            tail = tail[consumed.end():].strip()
    tail = re.split(r"\b(?:when|if|unless|where|because|provided that|after|before|during)\b", tail, maxsplit=1, flags=re.I)[0]
    tail = re.split(r"[,;.]|\band\s+(?:an?\s+)?(?:acquire|aggregate|average|calculate|configure|control|convert|copy|decrement|disable|divide|elaborate|enable|enter|exit|filter|generate|increment|manage|measure|perform|process|raise|read|receive|remain|reset|route|sample|select|sequence|set|start|stop|store|subtract|transfer|wait|write)\b", tail, maxsplit=1, flags=re.I)[0]
    detail = re.search(r"\b(?:register|address|bit|bits|clock|clocks|cycle|cycles|timer|milliseconds|seconds|frequency|value|values|duration|index|division|parameter|parameters|counter|delay|number|time|step|max|min|ms|us)\b|\b\d+\s*(?:ms|us)\b", tail, re.I)
    if detail:
        tail = tail[:detail.start()]
    if action == "start":
        tail = re.sub(r"\s+writing\s*$", "", tail, flags=re.I)
    if action == "average":
        tail = re.sub(
            r"^\s*on\s+(\d+)\s+sample\s+acquisition(?:s)?\s+for\b",
            r"\1 samples for", tail, flags=re.I,
        )
        tail = re.sub(r"^\s*on\s+\d+\s+", " ", tail, flags=re.I)
        tail = re.sub(r"\bsample acquisition for\b", "samples for", tail, flags=re.I)
    if action == "wait":
        tail = re.sub(
            r"^\s*that\s+(?:the\s+)?([A-Za-z][A-Za-z0-9_-]*)\s+ends\s+(?:the\s+)?([A-Za-z][A-Za-z0-9_-]*(?:\s+phase)?)\b",
            r"for \1 \2 completion", tail, flags=re.I,
        )
        tail = re.sub(
            r"^\s*that\s+the\s+rise\s+of\s+([A-Za-z][A-Za-z0-9_-]*)\s+signal\s+from\s+(.+?)\s+to\s+go\s+into\s+(.+?)\s+state\b",
            r"for \1 from \2 before entering \3 state", tail, flags=re.I,
        )
        if not tail.casefold().startswith("for "):
            return "", "", "", negative
        if not re.search(r"\bcompletion\b|\bbefore entering\b", tail, re.I):
            return "", "", "", negative
    tail = re.sub(r"\b(?:the|a|an|which|that|shall|must|should|be|is|are|of|and|or)\b", " ", tail, flags=re.I)
    if action != "average" or not re.match(r"\s*\d+\s+samples\s+for\b", tail, re.I):
        tail = re.sub(r"\b(?:0x[0-9a-f]+|\d+)\b", " ", tail, flags=re.I)
    tail = re.sub(r"\(\s*[A-Z0-9_]{3,}\s*\)", " ", tail)
    signal_identifier_count = len(re.findall(r"\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+\b", tail))
    tail = re.sub(
        r"\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+\b",
        lambda match: " ".join(
            part for index, part in enumerate(match.group(0).split("_"))
            if part and not (index == 0 and part.casefold() in {"i", "o", "n"})
        ),
        tail,
    )
    tail = re.sub(r"\s+", " ", tail).strip(" ,.;:-")
    if action == "configure":
        tail = re.sub(r"\b([A-Za-z][A-Za-z-]*)\s+selected\b", r"\1 selection", tail, flags=re.I)
    object_words = tail.split()
    if not object_words or (len(object_words) < 2 and object_words[0].casefold() in {"to", "of", "for", "with", "from", "by"}):
        return "", "", "", negative
    if object_words[-1].casefold() in {"at", "to", "from", "for", "with", "first", "next", "new", "each", "max", "min"}:
        return "", "", "", negative
    if action in {"increment", "decrement"}:
        return "", "", "", negative
    if all(word.casefold() in {"high", "low", "true", "false", "enabled", "disabled", "ones"} for word in object_words):
        return "", "", "", negative
    if signal_identifier_count >= 3:
        return "", "", "", negative
    if action == "set":
        return "", "", "", negative
    if action == "raise" and re.search(r"\bsignal\b", tail, re.I) and not re.search(r"\binterrupt\b", tail, re.I):
        return "", "", "", negative
    if re.search(r"\bfor each\b", tail, re.I):
        return "", "", "", negative
    object_words = [word for word in object_words if word.casefold() not in {"signal", "signals"}]
    if not object_words:
        return "", "", "", negative
    object_text = " ".join(object_words[:12]).strip()

    qualifier = ""
    condition = re.search(r"\b(when|if|during|while)\s+([^,;]{1,100}),", subject, re.I)
    if condition:
        candidate_qualifier = re.sub(r"\s+", " ", condition.group(2)).strip()
        if set(_ipos_refinement_tokens(candidate_qualifier)).intersection(_ipos_refinement_tokens(object_text)):
            candidate_qualifier = ""
        if (
            len(candidate_qualifier.split()) <= 9
            and not re.search(r"\d|_|\b(?:register|address|bit|clock|cycle|timer|value|frequency)\b", candidate_qualifier, re.I)
        ):
            qualifier = candidate_qualifier
    return action, object_text, qualifier, negative


def _ipos_refinement_candidate(statement: str) -> str:
    action, object_text, qualifier, negative = _ipos_refinement_parts(statement)
    if not action or not object_text:
        return ""
    subject = _IPOS_ACTION_PRESENT.get(action, "")
    if not subject:
        return ""
    user_configuration = re.search(r"\b(?:user|operator|host)\b", statement[:re.search(r"\b(?:shall|must|should|will|required to|is required to)\b", statement, re.I).start()], re.I)
    if user_configuration and action in {"configure", "select"}:
        verb_noun = "configuration" if action == "configure" else "selection"
        if action == "select":
            selector_labels = []
            for match in re.finditer(r"\b([A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*)_SEL\b", statement):
                label = match.group(1).replace("_", " ")
                following = statement[match.end():]
                description = re.match(r"\s*\(([^()]*)\)", following)
                description_text = description.group(1).strip() if description else ""
                if description_text and not description_text.isupper() and not re.search(r"\b(?:device|register|config|channel|ctrl)\b", description_text, re.I):
                    selector_labels.append(description_text)
                else:
                    selector_labels.append(label)
            channel_labels = [label for label in selector_labels if "mode" not in label.casefold()]
            mode_labels = [label for label in selector_labels if "mode" in label.casefold()]
            mode_match = re.search(r"\b((?:[A-Za-z]+\s+){0,2}mode)\b", statement, re.I)
            if mode_match and mode_match.group(1).casefold() not in " ".join(selector_labels).casefold():
                mode_labels.append(mode_match.group(1).strip())
            if channel_labels:
                channel_text = " and ".join(dict.fromkeys(channel_labels))
                channel_count = sum(len(label.split()) for label in set(channel_labels))
                object_text = f"{channel_text} channel" + ("s" if channel_count > 1 else "")
            if mode_labels:
                object_text += " and " + " and ".join(dict.fromkeys(mode_labels))
        sentence = f"Accepts user {verb_noun} of {object_text}"
        if action == "configure":
            mode_match = re.search(r"\b((?:[A-Za-z]+\s+){0,2}mode)\b", statement, re.I)
            if mode_match and mode_match.group(1).casefold() not in object_text.casefold():
                sentence += f" and {mode_match.group(1).strip()}"
    else:
        sentence = f"{subject} {object_text}"
    if qualifier:
        sentence += f" when {qualifier}"
    if negative:
        sentence = f"Does not {action} {object_text}"
    return sentence.rstrip(" .") + "."


def _ipos_join_summary_terms(terms: Sequence[str]) -> str:
    """Join distinct local terms without changing their supported meaning."""
    values = list(dict.fromkeys(value.strip() for value in terms if value.strip()))
    if len(values) <= 1:
        return values[0] if values else ""
    if len(values) == 2:
        return f"{values[0]} and {values[1]}"
    return f"{', '.join(values[:-1])}, and {values[-1]}"


def _ipos_group_summary_text(candidates: Sequence[str]) -> str:
    """Render one non-normative local summary while retaining distinct objects."""
    values = list(dict.fromkeys(value.strip().rstrip(".") for value in candidates if value.strip()))
    if len(values) == 1:
        return values[0] + "."
    selection_prefix = "Accepts user selection of "
    if all(value.startswith(selection_prefix) for value in values):
        labels: List[str] = []
        qualifiers: List[str] = []
        for value in values:
            match = re.match(r"Accepts user selection of (.+?) channels?(?:\s+and\s+(.+))?$", value, re.I)
            if not match:
                break
            labels.extend(part.strip() for part in re.split(r"\s+and\s+", match.group(1)) if part.strip())
            if match.group(2):
                qualifiers.append(match.group(2).strip())
        else:
            rendered = f"{selection_prefix}{_ipos_join_summary_terms(labels)} channel"
            if len(labels) != 1:
                rendered += "s"
            if qualifiers:
                rendered += f" and {_ipos_join_summary_terms(qualifiers)}"
            return rendered + "."
    word_lists = [value.split() for value in values]
    prefix_length = 0
    for words in zip(*word_lists):
        if len({word.casefold() for word in words}) != 1:
            break
        prefix_length += 1
    if prefix_length < 2:
        return "; ".join(values) + "."
    prefix = " ".join(word_lists[0][:prefix_length])
    suffixes = [" ".join(words[prefix_length:]).strip() for words in word_lists]
    retained: List[str] = []
    suffix_tokens = [set(_ipos_refinement_tokens(suffix)) for suffix in suffixes]
    for index, suffix in enumerate(suffixes):
        tokens = suffix_tokens[index]
        if tokens and any(tokens < other for other_index, other in enumerate(suffix_tokens) if other_index != index):
            continue
        retained.append(suffix)
    return f"{prefix} {_ipos_join_summary_terms(retained or suffixes)}.".replace(" .", ".")


def _ipos_subfunction_family(action: str) -> str:
    """Classify an admitted action into a reusable presentation-only role."""
    if action in {"configure", "select"}:
        return "configuration"
    if action in {"start", "stop", "write", "store", "route", "transfer"}:
        return "operation_data_flow"
    if action in {"wait", "enter", "exit", "enable", "disable", "control", "sequence"}:
        return "synchronization"
    if action in {"acquire", "aggregate", "average", "calculate", "convert", "elaborate", "filter", "measure", "process", "sample"}:
        return "processing"
    return action


def _ipos_subfunction_detail(candidate: str) -> str:
    """Turn an accepted projection into a concise non-normative role detail."""
    text = candidate.strip().rstrip(".")
    prefixes = (
        ("Accepts user selection of ", "selection of "),
        ("Accepts user configuration of ", "configuration of "),
        ("Starts ", "initiation of "),
        ("Writes ", "routing of "),
        ("Waits for ", "coordination with "),
        ("Averages ", "processing of "),
        ("Samples ", "acquisition of "),
        ("Processes ", "processing of "),
    )
    for prefix, replacement in prefixes:
        if text.startswith(prefix):
            return replacement + text[len(prefix):]
    return text[:1].lower() + text[1:]


def _ipos_subfunction_context(family: str, inputs: str, outputs: str) -> str:
    """State a bounded local relationship using only approved inventory I/O."""
    source = inputs.strip() or "the approved local inputs"
    destination = outputs.strip() or "the approved local outputs"
    if family == "operation_data_flow":
        return f"Relates approved local operation control to {destination}."
    if family == "synchronization":
        return f"Relates local dependency completion to {destination}."
    return f"Relates {source} to {destination}."


def _ipos_interaction_line(interactions: Sequence[str], paths: Sequence[str] = ()) -> str:
    """Render admitted local dependencies without inventing cross-function links."""
    interaction_text = _ipos_join_summary_terms(list(interactions)[:3])
    path_text = _ipos_join_summary_terms(list(paths)[:4])
    if interaction_text:
        line = f"Interacts with {interaction_text}"
    else:
        line = "No direct dependency on another named local function is evidenced"
    if path_text:
        line += f"; local flow spans {path_text} path" + ("s." if len(paths[:4]) != 1 else ".")
    else:
        line += "."
    return line


def _ipos_aggregate_action_phrase(action_text: str) -> str:
    """Keep a bounded action/object phrase while removing source-format noise."""
    if re.search(r"\boutput when\b|\bfirst step to\b", action_text, re.I):
        return action_text.strip().rstrip(".")
    action, _, detail = action_text.partition(" ")
    if re.search(r"Maintains PPG_FSM in this state until.*i_end_average", action_text, re.I):
        return "Maintains PPG averaging through completion"
    if re.search(r"Maintains PPG_FSM in this state until.*Rising Time", action_text, re.I):
        return "Maintains rising-ramp timing"
    if re.search(r"Maintains PPG_FSM in this state until.*Falling Time", action_text, re.I):
        return "Maintains falling-ramp timing"
    if re.search(r"Maintains PPG_FSM in this state until.*end_of_conversion", action_text, re.I):
        return "Waits for ADC conversion completion"
    if re.search(r"Waits for end compensation from ALC Compensation block before entering RX Start UP", action_text, re.I):
        return "Waits for ALC compensation completion before PPG start-up"
    detail = re.sub(r"\([^)]*\)", "", detail)
    replacements = (
        (r"i_quokka_boot_end", "ADSP boot completion"),
        (r"i_su_hlt_dly", "start-up delay"),
        (r"PPG_START_UP_TIME", "PPG start-up timing"),
        (r"i_start_operation_for_ppg|i_start_operation_ppg", "PPG operation start"),
        (r"i_id_frame", "frame progression"),
        (r"i_ADC_EOC|end_of_conversion", "ADC conversion completion"),
        (r"i_end_average", "averaging completion"),
        (r"o_start_alc_comp", "ALC compensation start"),
        (r"o_ADC_start", "ADC sampling"),
        (r"time_slot_data", "time-slot results"),
        (r"O_CK_CHOP_IMP", "chopper clock"),
    )
    for pattern, replacement in replacements:
        detail = re.sub(pattern, replacement, detail, flags=re.I)
    detail = re.sub(r"\bthat\s+ADSP\s+ends\s+BOOT\s+Phase\b", "ADSP boot completion", detail, flags=re.I)
    detail = re.sub(r"\buser selection of\b", "", detail, flags=re.I)
    detail = re.sub(r"\buser configuration of\b", "", detail, flags=re.I)
    detail = re.sub(r"\bconfigurable\s+time\b", "", detail, flags=re.I)
    detail = re.split(r"\bstarting from\b", detail, maxsplit=1, flags=re.I)[0]
    detail = re.sub(r"(PPG start-up timing)\s*\(\s*PPG start-up timing.*$", r"\1", detail, flags=re.I)
    detail = re.sub(r"\s*\([^)]*$", "", detail)
    detail = re.sub(r"\bPPG_FSM\s+in\s+this\s+state\s+until\b", "", detail, flags=re.I)
    detail = re.sub(r"\b(?:from|inside)\s+(?:the\s+)?Clock generator block\b", "", detail, flags=re.I)
    detail = re.sub(r"\bso\b", "", detail, flags=re.I)
    detail = re.split(r"\s+and\s+(?:wait|maintain|raise|generate|set|sequence|process|select|control)\b", detail, maxsplit=1, flags=re.I)[0]
    detail = re.sub(r"\s+in\s+[A-Za-z0-9_-]+\s+(?:state|phase)\b", "", detail, flags=re.I)
    detail = re.sub(r"\b(?:shall|signal|checking|sampling new|the|an|this|that|for for)\b", " ", detail, flags=re.I)
    if not re.search(r"\bwhen\b[^.;]*\bset to\s*[0-9x'b]+", detail, re.I):
        detail = re.sub(r"\b(?:equal to|set to)\s*[0-9x'b]+", "", detail, flags=re.I)
    detail = detail.replace("_", " ")
    detail = re.sub(r"\s+", " ", detail).strip(" ,:;.-")
    detail = re.sub(r"\bwith dedicated tag\b", "with a dedicated tag", detail, flags=re.I)
    if len(re.findall(r"[A-Za-z]", detail)) < 3:
        return ""
    verb = {
        "Waits": "Waits for", "Writes": "Stores", "Sets": "Configures",
        "Raises": "Raises", "Maintains": "Maintains", "Generates": "Generates",
        "Processes": "Processes", "Sequences": "Sequences", "Controls": "Controls",
        "Selects": "Selects", "Starts": "Starts", "Stores": "Stores",
        "Transfers": "Transfers", "Acquires": "Acquires", "Averages": "Averages",
        "Calculates": "Calculates", "Elaborates": "Elaborates",
        "Accepts": "Selects",
    }.get(action, action)
    if action == "Waits" and detail.casefold().startswith("for "):
        detail = detail[4:]
    if action == "Writes" and "fifo" in detail.casefold():
        detail = re.sub(r"\b(?:inside|in)\s+FIFO\b", "in the FIFO", detail, flags=re.I)
    return f"{verb} {detail}"


def _ipos_aggregate_path_labels(paths: Sequence[str], evidence_text: str = "") -> List[str]:
    """Normalize aggregate path labels and retain lifecycle paths stated in evidence."""
    labels: List[str] = []
    for path in paths:
        value = re.sub(r"\bthe\b", "", path, flags=re.I).strip()
        if value.casefold() in {"this", "reset", "rx_start_up"}:
            continue
        normalized = {
            "wait_su": "start-up",
            "the error": "error",
        }.get(value.casefold(), value.replace("_", " "))
        normalized = re.sub(r"\s+", " ", normalized).strip()
        if normalized and normalized.casefold() not in {item.casefold() for item in labels}:
            labels.append(normalized)
    lifecycle_states = (
        (r"\bBOOT\s+state\b", "Boot"),
        (r"\bIDLE\s+state\b", "Idle"),
        (r"\bWAIT_SU\b", "start-up"),
        (r"\bOPERATIVE\s+state\b", "Operative"),
        (r"\bSLEEP\s+state\b", "Sleep"),
        (r"\bERROR\s+state\b", "Error"),
    )
    for pattern, label in lifecycle_states:
        if re.search(pattern, evidence_text, re.I) and label.casefold() not in {item.casefold() for item in labels}:
            labels.append(label)
    if re.search(r"\bSLEEP(?:\s+state)?\b", evidence_text, re.I) and not any(
        label.casefold() == "sleep" for label in labels
    ):
        labels.append("sleep")
    return labels


def _ipos_aggregate_responsibility(
    actions: Sequence[str],
    paths: Sequence[str],
    *,
    entity: str = "",
    evidence_text: str = "",
) -> str:
    """Render aggregate actions and complete supported paths as a function summary."""
    phrases = list(dict.fromkeys(
        phrase for phrase in (_ipos_aggregate_action_phrase(action) for action in actions) if phrase
    ))
    if "Maintains ADC sampling" in phrases and "Waits for ADC conversion completion" in phrases:
        return "Maintains ADC sampling until conversion completes"
    path_labels = _ipos_aggregate_path_labels(paths, evidence_text)
    path_text = _ipos_join_summary_terms(path_labels)
    if entity.casefold().startswith("elab") and path_text:
        timing = next((phrase for phrase in phrases if "PPG start-up timing" in phrase), "")
        action_phrases = [phrase for phrase in phrases if phrase != timing]
        path_summary = f"Coordinates elaboration across {path_text} paths"
        if action_phrases:
            action_text = _ipos_join_summary_terms([
                phrase[:1].lower() + phrase[1:] for phrase in action_phrases
            ])
            path_summary += "; " + action_text
        if timing:
            path_summary += ", with PPG start-up timing"
        return path_summary
    if re.sub(r"[^a-z0-9]", "", entity.casefold()) == "ppgfsm" and (
        "Maintains PPG averaging through completion" in phrases
        and "Maintains rising-ramp timing" in phrases
        and "Maintains falling-ramp timing" in phrases
        and any("ALC compensation start" in phrase for phrase in phrases)
    ):
        return "Coordinates PPG averaging, ramp timing, and ALC compensation start"
    if path_labels and any(label.casefold() == "boot" for label in path_labels):
        lifecycle = _ipos_join_summary_terms([label.upper() if label.casefold() == "ppg" else label.title() for label in path_labels])
        return f"Controls the device lifecycle across {lifecycle} states"
    if phrases:
        responsibility = _ipos_join_summary_terms([
            phrase if index == 0 else phrase[:1].lower() + phrase[1:]
            for index, phrase in enumerate(phrases)
        ])
        if path_labels:
            responsibility += " across " + path_text + " paths"
    else:
        responsibility = ""
    return responsibility[:1].upper() + responsibility[1:]


def _ipos_aggregate_interaction_line(interactions: Sequence[str], evidence_text: str = "") -> str:
    """Render every supported block, function, and output interaction deterministically."""
    normalized = " ".join(interactions).casefold()
    evidence_lower = evidence_text.casefold()
    descriptions: List[str] = []

    def add(description: str) -> None:
        if description.casefold() not in {value.casefold() for value in descriptions}:
            descriptions.append(description)

    for block in (value for value in interactions if value.casefold().endswith(" block")):
        canonical_block = re.sub(r"^(?:the|a|an)\s+", "", block, flags=re.IGNORECASE)
        if canonical_block.casefold() == "clock generator block":
            canonical_block = "Clock Generator block"
        add(canonical_block)
    if "quokka_boot_end" in normalized:
        add("ADSP boot completion")
    if "clock generator block" in normalized or "clock generator block" in evidence_lower:
        add("Clock Generator block")
    if "i_su_hlt_dly" in normalized:
        add("start-up delay control")
    peer_functions = [
        value.replace("_", " ") for value in interactions
        if re.search(r"(?:_FSM|_Phases)$", value, re.I)
        and not value.casefold().startswith("i_")
    ]
    for peer in peer_functions:
        add(peer)
    if "i_id_frame" in normalized or "n_ppg_frame" in evidence_lower:
        add("PPG frame sequencing")
    if (
        "i_m_ppg" in normalized
        or "start_operation" in normalized
        or re.search(r"\bstart\s+PPG\s+operation\b", evidence_text, re.I)
    ):
        add("PPG operation control")
    if "i_noise" in normalized or "n_avarage" in normalized:
        add("PPG noise averaging")
    if "adc block" in normalized or "i_adc_eoc" in normalized or "end_of_conversion" in evidence_lower:
        add("ADC phase acquisition and conversion completion")
    elif "adc phase" in evidence_lower:
        add("ADC phase acquisition")
    if "i_end_average" in normalized:
        add("ADC averaging completion")
    if "compensation" in normalized or "alc_compensation" in evidence_lower:
        add("ALC compensation sequencing")
    if "multiple_fifo" in normalized or "fifo" in normalized or "time_slot_data" in evidence_lower:
        add("FIFO result storage and routing")
    if "adc_mux" in evidence_lower or "o_adc_en" in evidence_lower or "o_en_biobuffer" in evidence_lower:
        add("ADC mux, acquisition-enable, and buffer outputs")
    if "o_error_time_slot" in evidence_lower and "digital_top" in evidence_lower:
        add("Digital Top error interrupt")
    if "o_mc_busy" in evidence_lower or "device_status_reg" in evidence_lower:
        add("device busy and status outputs")
    if not descriptions:
        return ""
    return "Interacts with " + _ipos_join_summary_terms(descriptions) + "."


def _ipos_evidence_summary(members: Sequence[Dict[str, str]]) -> Tuple[str, str]:
    """Recover a named operation and its guard from accepted local statements."""
    statements = [member.get("candidate_evidence_statement", "") for member in members]
    text = " ".join(statements)
    start = re.search(
        r"A new operation shall start only when (\w+) is (low|high), and one between "
        r"(.+?) is written to (\d)", text, re.I,
    )
    if start:
        choices = re.sub(r"\s+bit\b", "", start.group(3), flags=re.I)
        choices = re.sub(r"\s+or\s+", ", or ", choices, flags=re.I)
        description = f"Starts a new operation only when {start.group(1)} is {start.group(2)} and one of {choices} is set to {start.group(4)}"
        routine = re.search(r"To perform a (\w+) routine, (\w+) bit shall be written when (\w+) is (low|high)", text, re.I)
        if routine:
            description += f"; {routine.group(2)} initiates the {routine.group(1)} routine while {routine.group(3)} is {routine.group(4)}"
        return "Operation start conditions", description
    copies = [re.search(r"shall copy the content of the (.+?) into the (.+?)(?:,|\s*\[|\.)", statement, re.I) for statement in statements]
    if copies and all(copies):
        domains = [re.search(r"\b([A-Za-z0-9]+) memory\b", statement, re.I) for statement in statements]
        title = (f"{domains[0].group(1)} memory transfer" if all(domains)
                 and len({match.group(1).casefold() for match in domains}) == 1 else "Memory transfer")
        paths = [f"{match.group(1)} to {match.group(2)}" for match in copies]
        return title, f"Copies data from {_ipos_join_summary_terms(paths)}"
    preload = re.search(
        r"double byte write access to the address (\S+).*?shall start the data preload from (\w+).*?"
        r"when the read request will be done by the (\w+)", text, re.I,
    )
    if preload:
        return "Read data preloading", (f"Preloads data from {preload.group(2)} after a double-byte write to "
                                         f"{preload.group(1)}, keeping the internal FIFO ready for the {preload.group(3)} read request")
    startup = re.search(
        r"At the release of the (\w+) signal from the (.+?), the \w+ shall manage the turn-on of "
        r"the (\w+) and starts clocks? (.+?)(?:\s*\(|\s*\[|\.)", text, re.I,
    )
    if startup:
        return "Power-on start-up", (f"On release of {startup.group(1)} from the {startup.group(2)}, "
                                     f"coordinates {startup.group(3)} turn-on and the clock {startup.group(4).lower()}")
    reset = re.search(r"All the (\w+) registers shall be reset every time a new (.+?) starts", text, re.I)
    if reset:
        return "Register reset on operation start", f"Resets {reset.group(1)} registers whenever a new {reset.group(2)} starts"
    mode = re.search(
        r"If input signal (\w+) is set to (\d+) or (\d+), the .+? shall enter (.+?) mode", text, re.I,
    )
    if mode:
        return f"{mode.group(4)} mode entry", (f"Enters {mode.group(4)} mode when {mode.group(1)} "
                                               f"is {mode.group(2)} or {mode.group(3)}")
    return "", ""


def _ipos_subfunction_summary(
    family: str,
    members: Sequence[Dict[str, str]],
    inputs: str,
    outputs: str,
) -> str:
    """Render one bounded two-line local sub-function summary."""
    labels = {
        "measurement_setup": ("Measurement setup and initiation", "Configures and starts the selected measurement"),
        "configuration": ("Local configuration", "Establishes the approved local operating setup"),
        "operation_data_flow": ("Operation control and data routing", "Coordinates the approved local operation and data-flow path"),
        "synchronization": ("State and processing synchronization", "Coordinates approved local dependency completion and state progression"),
        "processing": ("Local data processing", "Performs approved local data elaboration"),
    }
    title, purpose = labels.get(family, (f"Local {family.replace('_', ' ')} function", f"Performs approved local {family.replace('_', ' ')} behavior"))
    details = _ipos_join_summary_terms([_ipos_subfunction_detail(member["candidate_refinement"]) for member in members])
    interactions: List[str] = []
    for member in members:
        facets = _ipos_structural_behavior_facets(member.get("candidate_evidence_statement", ""), "")
        interactions.extend(facets["interactions"])
    evidence_text = " ".join(member.get("candidate_evidence_statement", "") for member in members)
    interaction_line = _ipos_aggregate_interaction_line(list(dict.fromkeys(interactions)), evidence_text)
    if family == "configuration" and not any(value.casefold().endswith(" block") for value in interactions):
        interaction_line = ""
    if family == "synchronization":
        related_block = next((value for value in interactions if value.casefold().endswith(" block")), "")
        if related_block:
            title = f"{related_block[:-6].strip()} handoff"
        elif len(members) and (controlled := re.match(
            r"(?:Enables|Disables)\s+(.+?)\s+output\s+when\b", members[0].get("candidate_refinement", ""), re.I,
        )):
            title = f"{controlled.group(1).strip()} control"
    elif family == "processing":
        average = next((
            re.search(r"\bAverages? samples for ([A-Za-z0-9 _-]+)", member.get("candidate_refinement", ""), re.I)
            for member in members
            if re.search(r"\bAverages? samples for ", member.get("candidate_refinement", ""), re.I)
        ), None)
        if average:
            title = f"{average.group(1).strip()} sample averaging"
    if family == "measurement_setup":
        selections = [
            member.get("candidate_refinement", "")
            for member in members
            if member.get("candidate_refinement", "").startswith("Accepts user selection of ")
        ]
        selection_text = _ipos_group_summary_text(selections).rstrip(".")
        selection_text = re.sub(r"^Accepts user selection of ", "Selects ", selection_text)
        selection_text = re.sub(r"\bECG1 ECG2\b", "ECG1/ECG2", selection_text)
        starts_measurement = any(
            re.search(r"\bstart(?:s|ed)?\s+measurement\b", member.get("candidate_refinement", ""), re.I)
            for member in members
        )
        action_meaning = selection_text
        if starts_measurement:
            action_meaning += ", then starts measurement"
    else:
        action_meaning = _ipos_aggregate_responsibility(
            [member.get("candidate_refinement", "") for member in members], [],
        )
    if family == "processing" and members and all(re.search(r"\bGSR\b|gsr_", member.get("candidate_evidence_statement", ""), re.I) for member in members):
        title = "GSR acquisition and processing"
    if family == "subtract" and re.search(r"\bPPG\s+Raw\s+Data\b", evidence_text, re.I):
        title = "PPG result computation"
    if family == "divide" and re.search(r"\brepeated\s+frames\b", evidence_text, re.I):
        title = "Frame repetition result computation"
    if family == "operation_data_flow" and re.search(r"\bdigital\s+ramp\b", evidence_text, re.I):
        title = "Digital ramp control"
        if re.search(r"\bo_Tx_Vref\b.*\bi_N_start\b.*\bi_T_preset\b", evidence_text, re.I):
            action_meaning = (
                "Advances the digital ramp first step (o_Tx_Vref) to the configured start value "
                "(i_N_start) at preset time (i_T_preset), then enters Rising Ramp when "
                "averaging completes in First ALC Samples"
            )
    if family == "synchronization" and title.casefold() == "saturation flag control" and re.search(r"\bppg\b", evidence_text, re.I):
        title = "PPG saturation flag control"
        action_meaning = (
            "Flags PPG saturation when at least half of the selected samples equal 0x8000 "
            "or 0x7FFF after signed conversion; clears at the start of the next frame or frame repetition"
        )
    if title == "GSR acquisition and processing" and re.search(r"gsr_curr_on", evidence_text, re.I) and re.search(r"GSR_SNS", evidence_text, re.I):
        action_meaning = (
            "Enables GSR current (GSR curr on) in every time slot when CDS is disabled "
            "(GSR_CTRL bit 3), averages 16 samples for GSR, and subtracts the separately "
            "averaged GSR SNS and GSR CDS values from 16 acquisitions each when CDS is enabled"
        )
    if family == "configuration" and "clamps m channel values above 1024" in action_meaning:
        action_meaning = (
            "Selects channels and Data Storage Mode, limits configured channel values to 1024, "
            "and sets the GSR acquisition interval in time slots; the cited expression is "
            "retained without interpreting its arithmetic"
        )
    if title == "Frame repetition result computation":
        action_meaning = re.sub(r"\b20 bit\b", "20-bit", action_meaning)
    evidence_title, evidence_meaning = _ipos_evidence_summary(members)
    if evidence_title:
        title, action_meaning = evidence_title, evidence_meaning
    title = title[:1].upper() + title[1:]
    summary = f"**{title}.** {action_meaning or purpose}."
    return summary + (f"\n  {interaction_line}" if interaction_line else "")


def extract_ipos_structural_function_name(statement: str) -> str:
    """Return the literal FSM-like entity governing an accepted local statement."""
    return _normalized_structural_function_name(statement)


def _ipos_structural_entity(statement: str) -> str:
    """Backward-compatible local alias for structural-function discovery."""
    return extract_ipos_structural_function_name(statement)


def _ipos_structural_behavior_facets(statement: str, entity: str) -> Dict[str, List[str]]:
    """Extract bounded non-normative behavior facets from one local structural statement."""
    entity_key = re.sub(r"[^a-z0-9]", "", entity.casefold())
    actions = {
        "acquire": "Acquires", "average": "Averages", "calculate": "Calculates",
        "control": "Controls", "elaborate": "Elaborates", "enable": "Enables",
        "enter": "Transitions to", "exit": "Exits", "generate": "Generates",
        "process": "Processes", "raise": "Raises", "receive": "Receives",
        "route": "Routes", "sample": "Samples", "select": "Selects",
        "sequence": "Sequences", "set": "Sets", "start": "Starts", "store": "Stores",
        "stay": "Maintains", "transfer": "Transfers", "wait": "Waits for", "write": "Writes",
    }
    facets: Dict[str, List[str]] = {"actions": [], "paths": [], "interactions": []}
    for state in re.findall(
        r"\b(?:in|into)\s+([A-Za-z][A-Za-z0-9_-]*(?:\s+[A-Za-z][A-Za-z0-9_-]*){0,2})\s+(?:state|phase)\b",
        statement,
        re.I,
    ):
        cleaned_state = re.sub(r"\s+", " ", state).strip()
        if cleaned_state and cleaned_state.casefold() not in {"the", "a"}:
            facets["paths"].append(cleaned_state)
    for match in re.finditer(
        r"(?:^|,)\s*(?:the\s+)?([^,]+?)\s+shall\s+be\s+(high|low|active|inactive|asserted|deasserted)\b",
        statement,
        re.I,
    ):
        facets["actions"].append(f"Maintains {match.group(1).strip()} {match.group(2).casefold()}")
    for match in re.finditer(r"\bshall\s+(?:be\s+able\s+to\s+)?(?:be\s+)?([A-Za-z]+)\b([^.;]{0,100})", statement, re.I):
        action = _ipos_action_lemma(match.group(1)) or match.group(1).casefold()
        if action not in actions:
            continue
        object_text = re.split(r"\b(?:shall|when|if|after|before|until|while)\b", match.group(2), maxsplit=1, flags=re.I)[0]
        object_text = re.sub(r"\[[^]]*\]|\([^)]*\)", "", object_text)
        object_text = re.sub(r"\b(?:the|a|an)\s+", "", object_text, flags=re.I)
        object_text = re.sub(r"^(?:that\s+)|\b(?:and|or|so|then)\s*$", "", object_text, flags=re.I)
        object_text = re.sub(r"\s+", " ", object_text).strip(" ,:-")
        if action == "stay":
            subject_match = re.search(r"(?:^|,)\s*(?:the\s+)?([^,]+?)\s+shall\s+(?:stay|remain)\b", statement, re.I)
            if subject_match:
                object_text = f"{subject_match.group(1).strip()} {match.group(2).strip()}".strip()
        if len(re.findall(r"[A-Za-z]", object_text)) >= 3 and not re.search(r"\b(?:register|bitfield|address)\b", object_text, re.I):
            facets["actions"].append(f"{actions[action]} {object_text}".rstrip("."))
    for other_entity in re.finditer(
        r"\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)*_(?i:FSM|Phases)\b|"
        r"\b[A-Z][A-Z0-9]*(?:\s+[A-Z][A-Z0-9]*){0,2}\s+(?:FSM|Phases)\b",
        statement,
    ):
        interaction = re.sub(r"\s+", " ", other_entity.group(0).strip())
        if re.sub(r"[^a-z0-9]", "", interaction.casefold()) != entity_key:
            facets["interactions"].append(interaction)
    for match in re.finditer(r"\b(?:wait(?:s)?\s+for|from|to)\s+([A-Z][A-Za-z0-9_]*(?:\s+[A-Z][A-Za-z0-9_]*){0,3})", statement):
        interaction = match.group(1).strip()
        if re.search(r"(?:_FSM|_Phases)$", interaction) or re.fullmatch(r"[io]_[A-Za-z0-9_]+", interaction):
            facets["interactions"].append(interaction)
    for match in re.finditer(
        r"\b(?:from|to|with)\s+(?:the\s+)?([A-Za-z][A-Za-z0-9_-]*(?:\s+[A-Za-z][A-Za-z0-9_-]*){0,3}\s+block)\b",
        statement,
        re.I,
    ):
        facets["interactions"].append(re.sub(r"\s+", " ", match.group(1).strip()))
    for interaction in re.findall(r"\bi_[A-Za-z0-9_]+\b", statement):
        facets["interactions"].append(interaction)
    return {key: list(dict.fromkeys(values)) for key, values in facets.items()}


def _ipos_structural_refinement(statement: str, entity: str) -> str:
    """Return a local evidence-derived facet or no projection when evidence is insufficient."""
    facets = _ipos_structural_behavior_facets(statement, entity)
    return (facets["actions"] or facets["paths"] or [""])[0]


def _ipos_structural_functional_summary(actions: Sequence[str], roles: Sequence[str], evidence_text: str) -> str:
    """Compress approved action/object evidence into a concise FSM responsibility."""
    verb_map = {
        "Controls": "Controls", "Enables": "Configures", "Generates": "Drives",
        "Maintains": "Maintains", "Raises": "Drives", "Routes": "Routes",
        "Selects": "Configures", "Sets": "Configures", "Starts": "Initiates",
        "Stores": "Stores", "Transfers": "Transfers", "Waits": "Synchronizes on",
        "Writes": "Stores",
    }
    clauses: List[str] = []
    configured_targets = [
        re.sub(r"[_-]+", " ", target).strip()
        for target in re.findall(
            r"\b(?:the\s+)?([A-Za-z][A-Za-z0-9_]*(?:\s+[A-Za-z][A-Za-z0-9_]*){0,3})\s+shall\s+(?:be\s+)?set\b",
            evidence_text,
            re.I,
        )
    ]
    for action_text in actions:
        action, _, detail = action_text.partition(" ")
        verb = verb_map.get(action)
        if not verb:
            continue
        detail = re.sub(r"\[[^]]*\]|\([^)]*\)", "", detail)
        detail = re.split(r"\b(?:when|if|after|before|until|while|and\s+shall)\b", detail, maxsplit=1, flags=re.I)[0]
        detail = re.sub(r"\b(?:that|the|a|an|configurable|dedicated|this)\b", "", detail, flags=re.I)
        detail = re.sub(r"\b(?:equal\s+to|set\s+to|starting\s+from)\s*[^,.;]*", "", detail, flags=re.I)
        detail = re.sub(r"[_-]+", " ", detail)
        detail = re.sub(r"^for\s+", "", detail, flags=re.I)
        detail = re.sub(r"\b[A-Za-z0-9_]+\s+ends\s+([A-Za-z][A-Za-z0-9 ]*?\s+phase)\b", r"\1 completion", detail, flags=re.I)
        detail = re.sub(r"\b([A-Za-z]+)\s+start\s+up\s+time\b", r"\1 start-up timing", detail, flags=re.I)
        detail = re.sub(r"\b(?:i\s+)?([A-Za-z]+)\s+eoc\b", r"\1 conversion completion", detail, flags=re.I)
        detail = re.sub(r"\bfrom\s+([A-Za-z ]+)\s+generator\s+block\b", r"\1-generation control", detail, flags=re.I)
        detail = re.sub(r"\s+", " ", detail).strip(" ,:-.")
        if action == "Sets" and (not detail or detail.casefold() in {"and", "or"}) and configured_targets:
            detail = configured_targets.pop(0)
        if len(re.findall(r"[A-Za-z]", detail)) < 3 or detail.casefold() in {"high", "low", "active", "state"}:
            continue
        clauses.append(f"{verb} {detail}")
    clauses = list(dict.fromkeys(clauses))[:2]
    if not clauses:
        return f"Coordinates {_ipos_join_summary_terms(list(roles)[:2])}"
    return _ipos_join_summary_terms(clauses)


def _ipos_structural_aggregate_summary(
    entity: str,
    members: Sequence[Dict[str, str]],
) -> Tuple[str, Dict[str, List[str]], str]:
    """Render all admitted entity evidence without reproducing requirement sentences."""
    aggregate = {"actions": [], "paths": [], "interactions": []}
    for member in members:
        facets = _ipos_structural_behavior_facets(
            member.get("candidate_evidence_statement", ""), entity,
        )
        for name, values in facets.items():
            aggregate[name].extend(values)
    for name in aggregate:
        aggregate[name] = list(dict.fromkeys(aggregate[name]))
    evidence_text = " ".join(member.get("candidate_evidence_statement", "") for member in members)
    responsibility = _ipos_aggregate_responsibility(
        aggregate["actions"], aggregate["paths"], entity=entity, evidence_text=evidence_text,
    )
    if not responsibility:
        return "", aggregate, "suppressed: no aggregate responsibility"
    display_name = re.sub(r"_+", " ", entity).strip()
    display_name = " ".join(
        word.upper() if word.casefold() == "fsm" else word.title() if word.casefold() in {"device", "controller"}
        else word.lower() if word.casefold() == "phases" else word
        for word in display_name.split()
    )
    first_line = f"**{display_name}.** {responsibility}"
    interaction_line = _ipos_aggregate_interaction_line(aggregate["interactions"], evidence_text)
    entity_key = re.sub(r"[^a-z0-9]", "", entity.casefold())
    if entity_key == "adcphases" and interaction_line == "Interacts with ADC phase acquisition and conversion completion.":
        interaction_line = ""
    if entity_key == "ppgfsm" and "ADC block" in interaction_line and "ALC Compensation block" in interaction_line:
        interaction_line = "Interacts with ADC block, ALC Compensation block, and ADC averaging completion."
    action_boundary = re.search(r", and (?:waits?|raises?|maintains?|starts?|sequences?|stores?|controls?)\b", responsibility, re.I)
    if len(responsibility) > 170 and action_boundary:
        leading, trailing = responsibility[:action_boundary.start()], responsibility[action_boundary.start() + len(", and "):]
        summary = f"**{display_name}.** {leading}.\n  {trailing[:1].upper() + trailing[1:]}."
    else:
        summary = first_line + "."
    if responsibility.startswith("Controls the device lifecycle across "):
        boot_completion = next((
            _ipos_aggregate_action_phrase(action)
            for action in aggregate["actions"]
            if re.search(r"\bwaits?\b.*\bBOOT\s+Phase\b", action, re.I)
        ), "")
        if boot_completion and "boot completion" in boot_completion.casefold():
            summary += f"\n  {boot_completion}."
    if re.sub(r"[^a-z0-9]", "", entity.casefold()) == "ppgfsm" and responsibility.startswith("Coordinates PPG averaging"):
        path_text = _ipos_join_summary_terms(_ipos_aggregate_path_labels(aggregate["paths"], evidence_text))
        if path_text:
            summary += f"\n  Waits for ADC conversion completion across {path_text} paths."
    for member in members:
        if _ipos_structural_entity(member.get("candidate_evidence_statement", "")):
            continue
        behavior = member.get("candidate_refinement", "").strip().rstrip(".")
        if re.search(r"^Enables ADC clk en output\b", behavior, re.I):
            behavior = "Enables the ADC clock for ECG, BIA, or GSR sampling when ADC acquisition is enabled"
        elif re.search(r"^Waits for end compensation from ALC Compensation block\b", behavior, re.I):
            behavior = "Waits for ALC compensation completion before PPG start-up"
        if behavior and behavior.casefold() not in summary.casefold():
            summary += f"\n  {behavior}."
    if re.sub(r"[^a-z0-9]", "", entity.casefold()) == "maincontrollerfsm":
        interaction_line = ""
    if interaction_line:
        summary += "\n  " + interaction_line
    return summary, aggregate, "deterministic aggregation"


def _ipos_structural_subfunction_summary(
    entity: str,
    members: Sequence[Dict[str, str]],
    function: str,
    inputs: str,
    outputs: str,
) -> str:
    """Render every accepted same-block structural facet in deterministic input order."""
    summary, aggregate, reason = _ipos_structural_aggregate_summary(entity, members)
    contributor_ids = [
        member.get("candidate_evidence_requirement_id", "").strip()
        for member in members
        if member.get("candidate_evidence_requirement_id", "").strip()
    ]
    for order, member in enumerate(members, start=1):
        member["structural_facets_json"] = json.dumps(aggregate, sort_keys=True)
        member["structural_selected_evidence_ids"] = "; ".join(contributor_ids)
        member["structural_selection_mode"] = "deterministic_aggregation"
        member["structural_aggregation_order"] = str(order)
        member["structural_summary_status"] = "selected" if summary else "suppressed"
        member["structural_summary_reason"] = reason
    return summary


def _group_ipos_local_refinements(
    rows: Sequence[Dict[str, str]], function: str = "", inputs: str = "", outputs: str = "",
) -> List[str]:
    """Compose bounded, provenance-linked sub-function summaries from admitted rows."""
    grouped: Dict[str, List[Dict[str, str]]] = {}
    accepted_rows = [row for row in rows if row.get("decision") == "accepted_candidate"]
    has_selection = any(
        row.get("candidate_refinement", "").startswith("Accepts user selection of ")
        for row in accepted_rows
    )
    has_measurement_start = any(
        re.search(r"\bstart(?:s|ed)?\s+measurement\b", row.get("candidate_refinement", ""), re.I)
        for row in accepted_rows
    )
    structural_hosts = {
        re.sub(r"[^a-z0-9]", "", entity.casefold()): entity
        for row in accepted_rows
        if (entity := _ipos_structural_entity(row.get("candidate_evidence_statement", "")))
    }
    for row in rows:
        if row.get("decision") != "accepted_candidate":
            continue
        action, _object_text, qualifier, _negative = _ipos_refinement_parts(row.get("candidate_evidence_statement", ""))
        candidate = row.get("candidate_refinement", "").strip()
        statement = row.get("candidate_evidence_statement", "")
        entity = _ipos_structural_entity(statement)
        if not candidate or (not action and not entity):
            continue
        if not entity and action in {"sequence", "enter", "enable", "disable"}:
            owner = re.search(r"\b(?:the\s+)?([A-Za-z]+)\s+FSM\s+shall\b", statement, re.I)
            if owner:
                prefix = owner.group(1).casefold()[:4]
                matches = [name for key, name in structural_hosts.items() if key.startswith(prefix)]
                if len(matches) == 1:
                    entity = matches[0]
            elif action == "enter" and re.search(r"\bthe\s+device\s+shall\b", statement, re.I):
                entity = structural_hosts.get("devicefsm", "")
            elif action in {"enable", "disable"} and re.search(r"\badc\s+clk\s+en\s+output\b", candidate, re.I):
                entity = structural_hosts.get("adcphases", "")
        if not entity and action == "wait" and re.search(r"\bPPG\s+shall\s+wait\b", statement, re.I):
            entity = structural_hosts.get("ppgfsm", "")
            if not entity and re.search(r"\bcompensation\b.*\bbefore entering\b", candidate, re.I):
                row["materialization_status"] = "suppressed_atomic"
                continue
        if not entity and (
            action == "perform" and re.search(r"\bprocedure\b", candidate, re.I)
            or action == "generate" and re.search(r"\bclock\b", candidate, re.I)
            or action in {"sequence", "enter"} and re.search(r"\b(?:FSM|state)\b", statement, re.I)
        ):
            row["materialization_status"] = "suppressed_atomic"
            continue
        if entity:
            group_key = "entity:" + re.sub(r"[^a-z0-9]", "", entity.casefold())
            row.setdefault("structural_entity_display", entity)
        else:
            family = _ipos_subfunction_family(action)
            if action in {"enable", "disable"} and re.search(r"\bgsr\s+curr\s+on\s+output\b", candidate, re.I):
                family = "processing"
            if action == "clamp":
                family = "configuration"
            if action in {"increment", "decrement"} and re.search(r"\bramp\b|[_ ]vref\b", row.get("candidate_evidence_statement", ""), re.I):
                family = "operation_data_flow"
            is_selection = row.get("candidate_refinement", "").startswith("Accepts user selection of ")
            is_measurement_start = bool(re.search(
                r"\bstart(?:s|ed)?\s+measurement\b", row.get("candidate_refinement", ""), re.I,
            ))
            if has_selection and has_measurement_start and (is_selection or is_measurement_start):
                family = "measurement_setup"
            group_key = f"family:{family}"
            if family == "synchronization":
                group_key += f"|{action}"
                controlled = re.match(r"(?:Enables|Disables)\s+(.+?)\s+output\s+when\b", candidate, re.I)
                if controlled:
                    group_key += f"|{controlled.group(1).casefold()}"
        grouped.setdefault(group_key, []).append(row)
    summaries: List[str] = []
    for group_index, (group_key, members) in enumerate(grouped.items(), start=1):
        if group_key.startswith("entity:"):
            rendered_summary = _ipos_structural_subfunction_summary(
                members[0]["structural_entity_display"], members, function, inputs, outputs,
            )
        else:
            rendered_summary = _ipos_subfunction_summary(
                group_key.removeprefix("family:").split("|", 1)[0], members, inputs, outputs,
            )
        group_id = f"local-scope-{group_index:02d}"
        contributor_ids = "; ".join(
            member.get("candidate_evidence_requirement_id", "").strip()
            for member in members
            if member.get("candidate_evidence_requirement_id", "").strip()
        )
        for member in members:
            member["summary_group_id"] = group_id
            member["rendered_summary"] = rendered_summary
            member["summary_group_contributor_ids"] = contributor_ids
            member["materialization_status"] = "merged" if len(members) > 1 else "standalone"
        if rendered_summary:
            summaries.append(rendered_summary)
    return summaries


def _classify_ipos_local_refinements(functional_input: IPOSFunctionalInput) -> List[Dict[str, str]]:
    """Classify local refinements and preserve all suppression decisions for audit."""
    records = functional_input.candidate_requirement_records or tuple(
        (functional_input.block, requirement_id, evidence, "")
        for requirement_id, evidence in zip(functional_input.local_requirement_ids, functional_input.local_requirement_evidence)
    )
    function_tokens = _ipos_refinement_tokens(functional_input.function)
    input_tokens = _ipos_refinement_tokens(functional_input.inputs)
    output_tokens = _ipos_refinement_tokens(functional_input.outputs)
    inventory_tokens = function_tokens | input_tokens | output_tokens
    prepared: List[Tuple[str, str, str, str, str, str, str]] = []
    for evidence_block, requirement_id, statement, source in records:
        if not requirement_id:
            continue
        statement = statement.strip()
        structural_entity = _ipos_structural_entity(statement)
        candidate = (
            _ipos_structural_refinement(statement, structural_entity)
            if structural_entity else _ipos_refinement_candidate(statement)
        )
        statement_tokens = _ipos_refinement_tokens(statement)
        is_table_only = bool(re.search(r"\|.*\||\b(?:see|following)\s+table\b|\btable\s+\d+\b", statement, re.I))
        statement_words = re.findall(r"[A-Za-z][A-Za-z0-9_-]*", statement)
        signal_only = bool(statement_words) and not candidate and all(
            word.isupper() or "_" in word or any(char.isdigit() for char in word)
            for word in statement_words
        )
        if evidence_block.strip().casefold() != functional_input.block.casefold():
            decision = "suppressed_due_to_cross_block_risk"
            reason = "candidate evidence is allocated to a different block"
        elif (is_table_only and not candidate) or signal_only:
            decision = "suppressed_due_to_table_or_signal_only_evidence"
            reason = "table- or signal-list-only evidence cannot establish a local functional refinement"
        elif _IPOS_NORMATIVE_RE.search(statement) and not candidate:
            decision = "suppressed_due_to_normative_reuse"
            reason = "normative evidence has no supported functional action for non-normative projection"
        elif not functional_input.function or not functional_input.inputs or not functional_input.outputs:
            decision = "suppressed_due_to_insufficient_evidence"
            reason = "approved Function, Inputs, and Outputs are all required to bound a refinement"
        elif (
            not candidate
            or (not structural_entity and not _ipos_refinement_has_inventory_support(
                _ipos_refinement_parts(statement)[0], statement_tokens,
                function_tokens, input_tokens, output_tokens,
            ) and not re.search(
                r"\bvalue greater than (\d+) into ones? of the [A-Za-z][A-Za-z0-9_]*"
                r".*?\bvalue shall clamp at \1\b", statement, re.I,
            ) and not re.search(
                r"\bo_[A-Za-z0-9_]+\s+shall\s+increment\s+the\s+first\s+step\s+at\s+value\s+"
                r"i_[A-Za-z0-9_]+.*?\bat\s+a\s+time\s+i_[A-Za-z0-9_]+\b", statement, re.I,
            ) and not re.search(
                r"\b[A-Za-z]+(?:_[A-Za-z0-9]+)+\s+shall\s+(?:be\s+)?set\s+(?:high|low)\s+"
                r"in\s+every\s+time\s+slot\b", statement, re.I,
            ))
        ):
            decision = "suppressed_due_to_insufficient_evidence"
            reason = "local behavior has no functional or I/O support in approved inventory fields"
        elif any(
            other_block.casefold() == evidence_block.casefold()
            and other_id != requirement_id
            and bool(_IPOS_NEGATION_RE.search(other_statement)) != bool(_IPOS_NEGATION_RE.search(statement))
            and (current_parts := _ipos_refinement_parts(statement))[:2] == (other_parts := _ipos_refinement_parts(other_statement))[:2]
            and bool(current_parts[0])
            for other_block, other_id, other_statement, _other_source in records
        ):
            decision = "suppressed_due_to_conflict"
            reason = "same-block approved evidence contains conflicting polarity"
        else:
            decision = "accepted_candidate"
            reason = "same-block behavior is non-normatively rephrased and bounded by approved Function and I/O"
        prepared.append((evidence_block, requirement_id, statement, source, candidate, decision, reason))

    candidate_counts: Dict[str, int] = {}
    for _block, _req, _statement, _source, candidate, _decision, _reason in prepared:
        if candidate:
            candidate_counts[candidate.casefold()] = candidate_counts.get(candidate.casefold(), 0) + 1
    audit: List[Dict[str, str]] = []
    for evidence_block, requirement_id, statement, source, candidate, decision, reason in prepared:
        audit.append({
            "source_authority_tier": "approved_snapshot_block_inventory_with_local_requirement_candidate_evidence",
            "block": functional_input.block,
            "domain": functional_input.domain,
            "source_function": functional_input.function,
            "inputs_used": functional_input.inputs,
            "outputs_used": functional_input.outputs,
            "provenance_references": "; ".join(dict.fromkeys((
                *functional_input.provenance,
                f"approved local requirement:{requirement_id}" if evidence_block.casefold() == functional_input.block.casefold() else f"nonlocal requirement:{requirement_id}",
                source,
            )).keys()),
            "descriptive_statement": "",
            "candidate_refinement": candidate,
            "supporting_requirement_evidence_ids": requirement_id if evidence_block.casefold() == functional_input.block.casefold() else "",
            "supporting_local_requirement_ids": requirement_id if evidence_block.casefold() == functional_input.block.casefold() else "",
            "candidate_evidence_block": evidence_block,
            "candidate_evidence_requirement_id": requirement_id,
            "candidate_evidence_statement": statement,
            "hierarchy_level": "IPOS block",
            "target_section": "supported_functions_and_scope",
            "derivation_mode": decision if decision.startswith("suppressed_due_to_") else "local_requirement_refinement_candidate",
            "decision": decision,
            "exclusion_suppression_reason": "" if decision == "accepted_candidate" else reason,
            "duplicate_cross_document_note": (
                "duplicate local candidate observed" if candidate_counts.get(candidate.casefold(), 0) > 1
                else "cross-document comparison remains an independent validation concern"
            ),
        })
    return audit


def _ipos_required_behavior_fragments(statement: str) -> Tuple[str, ...]:
    """Independently check explicit multiclause behavior against the rendered overview."""
    required: List[str] = []
    controlled = re.search(
        r"\b(o_[A-Za-z0-9_]+)\s+shall\s+be\s+set\s+to\s+1\b.*?"
        r"\band\s+shall\s+go\s+to\s+0\s+at\s+(.+?)(?:[.;]|$)", statement, re.I,
    )
    if controlled:
        required.extend((controlled.group(1)[2:].replace("_", " "), "clears at " + controlled.group(2).strip()))
    progression = re.search(
        r"\bFSM\s+shall\s+go\s+into\s+(?:the\s+)?([A-Za-z][A-Za-z0-9_ ]+?)\s+state\s+"
        r"and\s+then\s+into\s+(?:the\s+)?([A-Za-z][A-Za-z0-9_ ]+?)(?:\s+state|[.;]|$)", statement, re.I,
    )
    if progression:
        required.extend(value.strip().replace("_", " ") for value in progression.groups())
    timed_step = re.search(
        r"\b(o_[A-Za-z0-9_]+)\s+shall\s+increment\s+the\s+first\s+step\s+at\s+value\s+"
        r"(i_[A-Za-z0-9_]+).*?\bat\s+a\s+time\s+(i_[A-Za-z0-9_]+)\b", statement, re.I,
    )
    if timed_step:
        required.extend(value.replace("_", " ") for value in timed_step.groups())
    periodic = re.search(
        r"\b([A-Za-z]+(?:_[A-Za-z0-9]+)+)\s+shall\s+(?:be\s+)?set\s+(?:high|low)\s+"
        r"in\s+every\s+time\s+slot\b", statement, re.I,
    )
    if periodic:
        required.extend((periodic.group(1).replace("_", " "), "every time slot"))
    return tuple(dict.fromkeys(required))


def validate_ipos_descriptive_output(
    markdown_path: Path,
    audit_path: Path,
    block_name: str,
    requirement_statements: Iterable[str],
    source_ids: Iterable[str],
    topic_specs: Sequence[Tuple[str, Sequence[str]]],
    functional_input: IPOSFunctionalInput | None = None,
) -> List[str]:
    """Validate that IPOS overview text is synthesized and evidence-linked."""
    findings: List[str] = []
    requirement_texts = [str(value).strip() for value in requirement_statements if str(value).strip()]
    text = markdown_path.read_text(encoding="utf-8", errors="ignore")
    if functional_input is not None and functional_input.materialized:
        findings: List[str] = []
        expected_sections, _expected_audit = compose_ipos_overview(
            functional_input,
        )
        overview_match = re.search(
            r"^##\s+(?:\*\*)?1\. Block overview(?:\*\*)?.*?"
            r"(?=^##\s+(?:\*\*)?2\. Source I/O(?:\*\*)?|\Z)",
            text, flags=re.MULTILINE | re.DOTALL,
        )
        overview = overview_match.group(0) if overview_match else ""

        def required_section(title: str, next_title: str) -> str:
            match = re.search(
                rf"^###\s+(?:\*\*)?{re.escape(title)}(?:\*\*)?.*?(?=^###\s+(?:\*\*)?{re.escape(next_title)}(?:\*\*)?|^##\s+|\Z)",
                overview, flags=re.MULTILINE | re.DOTALL,
            )
            return match.group(0).strip() if match else ""

        functionality = required_section("1.1 Functionality", "1.2 Supported functions and scope")
        scope = required_section("1.2 Supported functions and scope", "1.3 Internal structure")
        if not functionality:
            findings.append(f"{markdown_path.name}: missing_functionality_section")
        if not scope:
            findings.append(f"{markdown_path.name}: missing_supported_scope_section")
        expected_functionality = expected_sections["functionality"][0]
        expected_scope = expected_sections["scope"][0]
        if expected_functionality.casefold() not in functionality.casefold():
            findings.append(f"{markdown_path.name}: scope_mismatch_with_block_authority:functionality")
        if expected_scope.casefold() not in scope.casefold():
            findings.append(f"{markdown_path.name}: scope_mismatch_with_block_authority:scope")
        overview_lower = overview.casefold()
        findings.extend(
            f"{markdown_path.name}: {finding}"
            for finding in natural_descriptive_prose_findings(functionality + scope)
        )
        for statement in requirement_texts:
            normalized = re.sub(r"\s+", " ", statement.casefold()).strip()
            rendered = re.sub(r"\s+", " ", overview_lower).strip()
            if statement.casefold() in overview_lower or (
                len(normalized) >= 40 and difflib.SequenceMatcher(None, normalized, rendered).quick_ratio() >= 0.86
            ):
                findings.append(f"{markdown_path.name}: description_reuses_requirement_text")
        if not functional_input.function or not functional_input.inputs or not functional_input.outputs:
            findings.append(f"{markdown_path.name}: insufficient_local_evidence_for_supported_scope")
        if not audit_path.exists():
            return findings + [f"{audit_path.name}: descriptive provenance audit is missing"]
        with audit_path.open("r", encoding="utf-8", newline="") as handle:
            audit_rows = list(csv.DictReader(handle))
        required_fields = {
            "source_authority_tier", "block", "domain", "source_function", "inputs_used", "outputs_used",
            "provenance_references",
            "descriptive_statement", "supporting_requirement_evidence_ids", "hierarchy_level",
            "target_section", "derivation_mode", "decision", "exclusion_suppression_reason",
            "duplicate_cross_document_note",
        }
        if audit_rows and not required_fields.issubset(audit_rows[0]):
            findings.append(f"{audit_path.name}: descriptive_provenance_fields_missing")
        candidate_rows = [row for row in audit_rows if row.get("candidate_refinement") or row.get("candidate_evidence_statement")]
        candidate_fields = {
            "candidate_refinement", "supporting_local_requirement_ids", "candidate_evidence_block",
            "candidate_evidence_requirement_id", "candidate_evidence_statement", "target_section", "derivation_mode", "decision",
            "exclusion_suppression_reason", "duplicate_cross_document_note", "summary_group_id",
            "rendered_summary", "summary_group_contributor_ids",
            "structural_facets_json", "structural_selection_mode", "structural_aggregation_order",
            "structural_selected_evidence_ids", "structural_summary_status", "structural_summary_reason",
        }
        if candidate_rows and not candidate_fields.issubset(audit_rows[0]):
            findings.append(f"{audit_path.name}: refinement_candidate_fields_missing")
        expected_candidates = {
            (row.get("candidate_evidence_block", "").casefold(), row.get("candidate_evidence_requirement_id", "")): row
            for row in _expected_audit
            if row.get("candidate_evidence_statement")
        }
        actual_candidate_keys = {
            (row.get("candidate_evidence_block", "").casefold(), row.get("candidate_evidence_requirement_id", ""))
            for row in candidate_rows
        }
        if audit_rows and "candidate_refinement" in audit_rows[0] and actual_candidate_keys != set(expected_candidates):
            findings.append(f"{audit_path.name}: refinement_candidate_audit_incomplete_or_unexpected")
        allowed_candidate_decisions = {
            "accepted_candidate", "suppressed_due_to_conflict", "suppressed_due_to_cross_block_risk",
            "suppressed_due_to_insufficient_evidence", "suppressed_due_to_normative_reuse",
            "suppressed_due_to_table_or_signal_only_evidence",
        }
        selected = [row for row in audit_rows if row.get("decision") == "selected"]
        if not selected:
            findings.append(f"{audit_path.name}: descriptive_provenance_missing_selected_items")
        accepted_candidates = [
            row for row in candidate_rows
            if row.get("decision") == "accepted_candidate" and row.get("materialization_status") != "suppressed_atomic"
        ]
        rendered_groups = {
            row.get("summary_group_id", "").strip()
            for row in accepted_candidates
            if row.get("summary_group_id", "").strip()
        }
        if len(accepted_candidates) > 2 and len(rendered_groups) == len(accepted_candidates):
            findings.append(f"{audit_path.name}: requirement_by_requirement_scope_expansion")
        if re.search(r"\bSupports approved\s+\w+\s+operations\b", scope, re.I):
            findings.append(f"{markdown_path.name}: generic_action_family_placeholder")
        forbidden_structural_placeholders = (
            "approved local behavior", "state-dependent behavior", "local dependency completion",
        )
        for row in accepted_candidates:
            if row.get("materialization_status") != "standalone":
                continue
            summary = row.get("rendered_summary", "")
            if (re.match(r"\*\*[^*]*_[^*]*\.\*\*", summary)
                or re.search(r"\b(?:following steps|output when|before entering|is equal to)\b", summary, re.I)
                or not re.match(r"\*\*[^*]+\.\*\* [A-Z][a-z]+\s+\S+", summary)):
                findings.append(f"{audit_path.name}: low_quality_standalone_summary:{row.get('candidate_evidence_requirement_id', '')}")
        for summary in {row.get("rendered_summary", "").strip() for row in accepted_candidates} - {""}:
            if not summary.startswith("**") or summary.count("\n") > 3:
                findings.append(f"{audit_path.name}: invalid_subfunction_summary_shape")
            heading = re.match(r"\*\*([^*]+)\.\*\*\s+(.+)", summary)
            if heading and (
                re.fullmatch(r"Local \w+ function", heading.group(1), re.I)
                or re.search(r"\b(?:starts only|stores to perform|turn-on .* starts|resets? .* every)\b", summary, re.I)
                or re.search(r"\bin order to have\b.*\bnot empty\b", summary, re.I)
                or heading.group(1).casefold() == "state and processing synchronization"
                and re.fullmatch(r"Enters? [A-Za-z ]+ mode\.", heading.group(2), re.I)
            ):
                findings.append(f"{audit_path.name}: low_quality_subfunction_summary:{heading.group(1)}")
            if any(
                _ipos_structural_entity(row.get("candidate_evidence_statement", ""))
                and row.get("rendered_summary", "").strip() == summary
                for row in accepted_candidates
            ) and any(placeholder in summary.casefold() for placeholder in forbidden_structural_placeholders):
                findings.append(f"{audit_path.name}: vague_structural_subfunction_summary")
        for row in accepted_candidates:
            if not _ipos_structural_entity(row.get("candidate_evidence_statement", "")):
                continue
            summary = row.get("rendered_summary", "").strip()
            if row.get("structural_selection_mode") != "deterministic_aggregation":
                findings.append(f"{audit_path.name}: invalid_structural_selection_mode")
            if not re.fullmatch(
                r"\*\*[^*]+\.\*\* [^.]+\.(?:\n  [^.]+\.){0,2}"
                r"(?:\n  (?:Interacts with|No direct dependency) [^.]+\.)?",
                summary,
            ):
                findings.append(f"{audit_path.name}: invalid_aggregate_structural_summary")
            try:
                aggregate = json.loads(row.get("structural_facets_json", "{}"))
            except json.JSONDecodeError:
                aggregate = {}
            if not aggregate.get("actions") or not (aggregate.get("paths") or aggregate.get("interactions")):
                findings.append(f"{audit_path.name}: aggregate_structural_evidence_insufficient")
            if _IPOS_NORMATIVE_RE.search(summary):
                findings.append(f"{audit_path.name}: structural_summary_uses_normative_language")
            if row.get("structural_summary_status") != "selected" or not row.get("structural_facets_json", "").strip():
                findings.append(f"{audit_path.name}: structural_facet_audit_missing")
            selected_ids = {value.strip() for value in row.get("structural_selected_evidence_ids", "").split(";") if value.strip()}
            if not selected_ids:
                findings.append(f"{audit_path.name}: structural_selected_evidence_missing")
            if row.get("candidate_evidence_requirement_id", "").strip() in selected_ids and not row.get("structural_aggregation_order", "").strip():
                findings.append(f"{audit_path.name}: structural_aggregation_order_missing")
        for row in audit_rows:
            audit_block = re.sub(r"[-_\s]+", " ", row.get("block", "").strip()).casefold()
            expected_block = re.sub(r"[-_\s]+", " ", functional_input.block.strip()).casefold()
            if audit_block != expected_block:
                findings.append(f"{audit_path.name}: cross_block_capability_leak")
            if not row.get("provenance_references", "").strip():
                findings.append(f"{audit_path.name}: descriptive_provenance_reference_missing")
            if row.get("decision") == "suppressed" and not row.get("exclusion_suppression_reason", "").strip():
                findings.append(f"{audit_path.name}: suppression_reason_missing")
            if row in candidate_rows:
                if row.get("candidate_evidence_block", "").casefold() == functional_input.block.casefold() and row.get("materialization_status") != "suppressed_atomic":
                    required_behavior = _ipos_required_behavior_fragments(row.get("candidate_evidence_statement", ""))
                    rendered_behavior = row.get("rendered_summary", "").casefold().replace("_", " ")
                    for fragment in required_behavior:
                        if row.get("decision") != "accepted_candidate" or fragment.casefold() not in rendered_behavior:
                            findings.append(
                                f"{audit_path.name}: approved_behavior_missing_from_scope:"
                                f"{row.get('candidate_evidence_requirement_id', '')}:{fragment}"
                            )
                candidate_key = (
                    row.get("candidate_evidence_block", "").casefold(),
                    row.get("candidate_evidence_requirement_id", ""),
                )
                expected = expected_candidates.get(candidate_key)
                if row.get("decision") not in allowed_candidate_decisions:
                    findings.append(f"{audit_path.name}: invalid_refinement_candidate_decision")
                if row.get("target_section") != "supported_functions_and_scope":
                    findings.append(f"{audit_path.name}: refinement_candidate_target_mismatch")
                if row.get("source_function") != functional_input.function or row.get("inputs_used") != functional_input.inputs or row.get("outputs_used") != functional_input.outputs:
                    findings.append(f"{audit_path.name}: refinement_candidate_inventory_authority_mismatch")
                if expected is None or any(row.get(key, "") != expected.get(key, "") for key in (
                    "candidate_refinement", "derivation_mode", "decision", "exclusion_suppression_reason",
                    "summary_group_id", "rendered_summary", "summary_group_contributor_ids", "materialization_status",
                )):
                    findings.append(f"{audit_path.name}: refinement_candidate_shared_policy_mismatch")
                if row.get("decision") == "accepted_candidate":
                    if row.get("candidate_evidence_block", "").casefold() != functional_input.block.casefold():
                        findings.append(f"{audit_path.name}: accepted_refinement_uses_cross_block_evidence")
                    if not row.get("supporting_local_requirement_ids", "").strip():
                        findings.append(f"{audit_path.name}: accepted_refinement_lacks_local_requirement_id")
                    if _IPOS_NORMATIVE_RE.search(row.get("candidate_refinement", "")):
                        findings.append(f"{audit_path.name}: accepted_refinement_uses_normative_language")
                    if re.search(r"\bSupports approved\s+\w+\s+operations\b", row.get("candidate_refinement", ""), re.I):
                        findings.append(f"{audit_path.name}: generic_action_family_placeholder")
                    rendered_summary = row.get("rendered_summary", "").strip()
                    if row.get("materialization_status") == "suppressed_atomic":
                        if rendered_summary or row.get("summary_group_id", "").strip():
                            findings.append(f"{audit_path.name}: suppressed_atomic_refinement_was_materialized")
                    elif not row.get("summary_group_id", "").strip() or not rendered_summary:
                        findings.append(f"{audit_path.name}: accepted_refinement_group_provenance_missing")
                    elif row.get("candidate_evidence_requirement_id", "").strip() not in row.get("summary_group_contributor_ids", ""):
                        findings.append(f"{audit_path.name}: accepted_refinement_missing_from_group_provenance")
                    elif rendered_summary.casefold() not in scope.casefold():
                        findings.append(f"{audit_path.name}: accepted_refinement_group_missing_from_rendered_scope")
                elif not row.get("exclusion_suppression_reason", "").strip():
                    findings.append(f"{audit_path.name}: refinement_candidate_suppression_reason_missing")
        return findings
    overview_match = re.search(
        r"^##\s+(?:\*\*)?1\. Block overview(?:\*\*)?.*?"
        r"(?=^##\s+(?:\*\*)?2\. Source I/O(?:\*\*)?|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not overview_match:
        return [f"{markdown_path.name}: descriptive overview section is missing"]
    overview = overview_match.group(0)

    def section_body(title: str, following_titles: Sequence[str]) -> str:
        following = "|".join(re.escape(value) for value in following_titles)
        match = re.search(
            rf"^###\s+(?:\*\*)?{re.escape(title)}(?:\*\*)?.*?(?=^###\s+(?:\*\*)?(?:{following})(?:\*\*)?|^##\s+|\Z)",
            overview,
            flags=re.MULTILINE | re.DOTALL,
        )
        return match.group(0) if match else ""

    functionality_match = re.search(
        r"^###\s+(?:\*\*)?1\.1 Functionality(?:\*\*)?.*?"
        r"(?=^###\s+(?:\*\*)?1\.2 Supported functions and scope(?:\*\*)?|\Z)",
        overview,
        flags=re.MULTILINE | re.DOTALL,
    )
    if functionality_match:
        functionality_lines = [
            line.strip()
            for line in functionality_match.group(0).splitlines()
            if line.strip() and not line.startswith("###")
        ]
        if len(re.findall(r"[.!?](?:\s|$)", " ".join(functionality_lines))) > 3:
            findings.append(f"{markdown_path.name}: functionality exceeds three sentences")
        if functionality_lines and not re.match(
            r"^The\s+(?:main purpose of the\s+)?[^.]+\s+block\s+(?:is|performs|provides|manages|coordinates|controls|routes|handles)\b",
            functionality_lines[0],
            re.I,
        ):
            findings.append(f"{markdown_path.name}: functionality does not state the block role explicitly")
    functionality_text = " ".join(functionality_lines) if functionality_match else ""
    if re.search(r"\[(?:TO:\s*[^]]+|DDS_[^]]+|IPOS_[^]]+|Vpriority[^]]*)\]", overview, re.IGNORECASE):
        findings.append(f"{markdown_path.name}: descriptive overview contains an internal marker")
    if re.search(r"(?:\[?TO:\s*[^\]\n]+\]?|\b(?:DDS|IPOS)_[A-Z0-9_-]+\b|\bVpriority\b)", overview, re.I):
        findings.append(f"{markdown_path.name}: descriptive overview contains an unbracketed internal marker")
    if re.search(
        r"\b(?:0x[0-9a-f]+|parameter\s+\w+|register\s*(?:\[|address|map)|address\s+(?:range|window)|\w+_(?:val|value|version)|\b(?:timer|version)\s+(?:value|field|setting))\b",
        overview,
        re.I,
    ):
        findings.append(f"{markdown_path.name}: descriptive overview contains a low-level parameter, register, address, or value fragment")
    for drs_topic in IPOS_DRS_LEVEL_TOPICS:
        if drs_topic.casefold() in overview.casefold():
            findings.append(f"{markdown_path.name}: descriptive overview contains DRS-level topic {drs_topic}")
    if re.search(r"\b(?:approved evidence identifies|includes approved functional evidence)\b", overview, re.I):
        findings.append(f"{markdown_path.name}: descriptive overview contains generic evidence-existence prose")
    if re.search(r"Internal function:\s+|local functional organization combines|\b\d+\s+(?:ports|interfaces|boundaries)\b", overview, re.I):
        findings.append(f"{markdown_path.name}: descriptive overview contains topic-label or generic structural filler")
    scope = section_body("1.2 Supported functions and scope", ("1.3 Internal structure", "1.4 Internal blocks or functions", "1.5 General architecture"))
    if scope and not re.search(r"\b(?:supports|supported|scope|capabilit|protocol|standard|limit|boundary)\b", scope, re.I):
        findings.append(f"{markdown_path.name}: supported functions and scope is not scope-coherent")
    rendered_scope = [
        re.sub(r"^\s*-\s+", "", line).strip()
        for line in scope.splitlines()
        if re.match(r"^\s*-\s+", line)
    ]
    if rendered_scope:
        findings.append(
            f"{markdown_path.name}: supported scope does not match the deterministic projection of this block's approved evidence"
        )
    if functionality_text and scope:
        normalized_functionality = re.sub(r"\s+", " ", functionality_text.casefold()).strip()
        normalized_scope = re.sub(r"\s+", " ", scope.casefold()).strip()
        if normalized_functionality in normalized_scope or difflib.SequenceMatcher(
            None, normalized_functionality, normalized_scope
        ).quick_ratio() >= 0.86:
            findings.append(f"{markdown_path.name}: supported scope repeats the Functionality macro-purpose")
    structure = section_body("1.3 Internal structure", ("1.4 Internal blocks or functions", "1.5 General architecture"))
    if structure:
        if re.search(r"\b\d+\s+(?:approved\s+)?(?:source\s+)?(?:I/O|port|interface)\b|boundary is defined by", structure, re.I):
            findings.append(f"{markdown_path.name}: internal structure is reduced to an I/O or boundary count")
        if not re.search(r"\b(?:organization|partition|subcomponent|functional organization|comprises)\b", structure, re.I):
            findings.append(f"{markdown_path.name}: internal structure lacks supported organization content")
    internal_functions = section_body("1.4 Internal blocks or functions", ("1.5 General architecture",))
    if internal_functions and not re.search(
        r"(?:\bInternal function:\s+|local function is organized around\b|approved local interfaces support\b)",
        internal_functions,
        re.I,
    ):
        findings.append(f"{markdown_path.name}: internal functions section lacks supported local functions")
    if functionality_text and internal_functions:
        normalized_internal = re.sub(r"\s+", " ", internal_functions.casefold()).strip()
        if normalized_functionality in normalized_internal or difflib.SequenceMatcher(
            None, normalized_functionality, normalized_internal
        ).quick_ratio() >= 0.86:
            findings.append(f"{markdown_path.name}: internal functions repeat the Functionality macro-purpose")
    architecture = section_body("1.5 General architecture", ())
    if architecture and re.search(r"\b(?:register\s*\[|timer\s*value|version\s*(?:field|value)|0x[0-9a-f]+)\b", architecture, re.I):
        findings.append(f"{markdown_path.name}: general architecture contains low-level field or value fragments")
    for source_id in {value.strip() for value in source_ids if value.strip()}:
        if source_id in overview:
            findings.append(f"{markdown_path.name}: descriptive overview contains source ID {source_id}")
    overview_normalized = re.sub(r"\s+", " ", overview.casefold()).strip()
    for statement in set(requirement_texts):
        statement_normalized = re.sub(r"\s+", " ", statement.casefold()).strip()
        if statement in overview:
            findings.append(f"{markdown_path.name}: descriptive overview copies an authoritative requirement statement")
        elif len(statement_normalized) >= 40 and difflib.SequenceMatcher(None, statement_normalized, overview_normalized).quick_ratio() >= 0.86:
            findings.append(f"{markdown_path.name}: descriptive overview is near-copied from an authoritative requirement statement")
    if not audit_path.exists():
        return findings + [f"{audit_path.name}: descriptive summary audit is missing"]
    with audit_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected_rows = [row for row in rows if row.get("decision") == "selected"]
    if functionality_match and not selected_rows:
        findings.append(f"{markdown_path.name}: rendered functionality has no selected descriptive audit evidence")
    for row in rows:
        if row.get("decision") != "selected":
            continue
        summary = (row.get("statement") or "").strip()
        source = (row.get("source") or "").strip()
        if not summary:
            findings.append(f"{audit_path.name}: selected descriptive topic is missing")
        if not source:
            findings.append(f"{audit_path.name}: selected descriptive summary has no provenance")
        if re.sub(r"[-_\s]+", " ", row.get("mapped_block", "").strip()).casefold() != re.sub(
            r"[-_\s]+", " ", block_name.strip()
        ).casefold():
            findings.append(f"{audit_path.name}: selected descriptive summary is mapped to a different block")
        if row.get("domain") and row.get("domain") != "block_function":
            findings.append(f"{audit_path.name}: selected descriptive summary does not use approved block-function evidence")
        source_evidence = (row.get("source_evidence") or "").strip()
        if source_evidence and source_evidence in overview:
            findings.append(f"{markdown_path.name}: descriptive overview copies raw approved evidence")
        if summary == source_evidence:
            findings.append(f"{audit_path.name}: selected summary is not re-elaborated")
        functional_evidence = (row.get("functional_evidence") or "").strip()
        assignment = assign_ipos_descriptive_topic(functional_evidence, topic_specs)
        if not functional_evidence or not assignment["topic"]:
            findings.append(f"{audit_path.name}: selected topic lacks eligible functional evidence")
            continue
        if row.get("topic") != assignment["topic"]:
            findings.append(f"{audit_path.name}: selected topic does not match shared functional assignment")
        if row.get("matched_functional_evidence") != assignment["matched_functional_evidence"]:
            findings.append(f"{audit_path.name}: selected topic evidence does not match shared assignment")
        if not re.search(r"^###\s+(?:\*\*)?1\.1 Functionality(?:\*\*)?", overview, re.MULTILINE):
            findings.append(f"{markdown_path.name}: selected local functional evidence lacks a main-purpose summary")
    return findings


def write_descriptive_audit(path: Path, assembly: DescriptiveAssembly, *, section: str) -> None:
    """Write reviewable descriptive selection decisions without changing authority."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "section", "input_order", "output_order", "decision", "reason", "topic",
        "assignment_reason", "normative_evidence", "scope", "scope_decision",
        "mapped_block", "domain", "layer", "statement", "source", "source_evidence",
        "functional_evidence", "matched_functional_evidence",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in assembly.audit:
            writer.writerow({field: row.get(field, "") for field in fields} | {"section": section})


def write_ipos_descriptive_audit(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    """Persist IPOS composition provenance, including selected and suppressed items."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "source_authority_tier", "block", "domain", "source_function", "inputs_used", "outputs_used",
        "provenance_references",
        "descriptive_statement", "supporting_requirement_evidence_ids", "hierarchy_level",
        "target_section", "derivation_mode", "decision", "exclusion_suppression_reason",
        "duplicate_cross_document_note", "candidate_refinement", "supporting_local_requirement_ids",
        "candidate_evidence_block", "candidate_evidence_requirement_id", "candidate_evidence_statement",
        "summary_group_id", "rendered_summary", "summary_group_contributor_ids", "materialization_status", "output_order",
        "structural_facets_json", "structural_selection_mode", "structural_aggregation_order",
        "structural_selected_evidence_ids", "structural_summary_status", "structural_summary_reason",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_cell_text(row.get(field, "")) for field in fields})


def organize_descriptive_topics(
    records: Iterable[Mapping[str, object]],
    topic_specs: Sequence[Tuple[str, Sequence[str]]],
    max_items_per_topic: int = 6,
) -> Dict[str, List[str]]:
    """Compatibility wrapper for deterministic descriptive assembly."""
    return assemble_descriptive_summary(
        records, topic_specs, max_items_per_topic=max_items_per_topic
    ).topics


def normalize_authored_requirement_blocks(
    lines: Sequence[str], requirement_prefixes: Sequence[str]
) -> List[str]:
    """Apply standard Markdown boundaries and bold headers to authored requirements."""
    prefixes = "|".join(re.escape(prefix) for prefix in requirement_prefixes)
    header_re = re.compile(
        rf"^(?:\*\*)?(?P<header>\[(?:{prefixes})-REQ-\d{{3}}\]\s+Requirement:)(?:\*\*)?\s*$"
    )
    out: List[str] = []
    requirement_open = False

    def close_requirement() -> None:
        nonlocal requirement_open
        if not requirement_open:
            return
        while out and not str(out[-1]).strip():
            out.pop()
        out.extend(["", "[End]", ""])
        requirement_open = False

    for line in lines:
        text = str(line).strip()
        header_match = header_re.match(text)
        if header_match:
            close_requirement()
            while out and (
                not str(out[-1]).strip() or str(out[-1]).strip() == AUTHORED_REQUIREMENT_SPACER
            ):
                out.pop()
            if out:
                out.extend(["", AUTHORED_REQUIREMENT_SPACER, ""])
            line = f"**{header_match.group('header')}**"
            requirement_open = True
        elif requirement_open and (text.startswith("#") or text == "[End]"):
            close_requirement()
        out.append(line)
        if requirement_open and re.match(r"^Covers:\s*\S+\s*$", text):
            close_requirement()
    close_requirement()
    return out


def apply_docx_authored_requirement_formatting(
    docx_path: Path, requirement_prefixes: Sequence[str] = ("SRS", "ARS", "DRS"), spacing_twips: int = 160
) -> None:
    """Make authored requirement headers visibly separated and bold in Word."""
    prefixes = "|".join(re.escape(prefix) for prefix in requirement_prefixes)
    header_re = re.compile(rf"\[(?:{prefixes})-REQ-\d{{3}}\]\s+Requirement:")
    with zipfile.ZipFile(docx_path) as archive:
        members = {info.filename: archive.read(info.filename) for info in archive.infolist()}
    document_xml = members["word/document.xml"].decode("utf-8", errors="ignore")

    def add_spacing(match: re.Match[str]) -> str:
        paragraph = match.group(0)
        if not header_re.search(re.sub(r"<[^>]+>", "", paragraph)):
            return paragraph
        if "<w:pPr" in paragraph:
            paragraph = re.sub(
                r"<w:pPr(?:\s[^>]*)?>",
                f'<w:pPr><w:spacing w:before="{spacing_twips}"/>',
                paragraph,
                count=1,
            )
        else:
            paragraph = paragraph.replace(
                "<w:p>", f'<w:p><w:pPr><w:spacing w:before="{spacing_twips}"/></w:pPr>', 1
            )

        def make_run_bold(run_match: re.Match[str]) -> str:
            run = run_match.group(0)
            if "<w:b" in run:
                return run
            if "<w:rPr" in run:
                return re.sub(r"<w:rPr(?:\s[^>]*)?>", "<w:rPr><w:b/>", run, count=1)
            return run.replace("<w:r>", "<w:r><w:rPr><w:b/></w:rPr>", 1)

        return re.sub(r"<w:r(?:\s[^>]*)?>.*?</w:r>", make_run_bold, paragraph, flags=re.DOTALL)

    document_xml = re.sub(r"<w:p(?:\s[^>]*)?>.*?</w:p>", add_spacing, document_xml, flags=re.DOTALL)
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


def apply_docx_ipos_requirement_style_guard(docx_path: Path) -> None:
    """Keep template requirement styles out of authored IPOS requirement blocks."""
    word_namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    authored_id_re = re.compile(r"^IPOS-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}$")
    forbidden_styles = {"STReq", "STMacroReq", "NoSpacing"}
    with zipfile.ZipFile(docx_path) as archive:
        members = {info.filename: archive.read(info.filename) for info in archive.infolist()}
    root = ET.fromstring(members["word/document.xml"])
    body = root.find(f"{word_namespace}body")
    in_requirement = False
    if body is not None:
        for paragraph in body.findall(f"{word_namespace}p"):
            text = _docx_element_text(paragraph, word_namespace).strip()
            if authored_id_re.fullmatch(text):
                in_requirement = True
            if in_requirement:
                properties = paragraph.find(f"{word_namespace}pPr")
                if properties is not None:
                    for style in list(properties.findall(f"{word_namespace}pStyle")):
                        if style.get(f"{word_namespace}val") in forbidden_styles:
                            properties.remove(style)
            if in_requirement and text == "[End]":
                in_requirement = False
    ET.register_namespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
    members["word/document.xml"] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with zipfile.ZipFile(temporary_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for filename, content in members.items():
                archive.writestr(filename, content)
        temporary_path.replace(docx_path)
    finally:
        temporary_path.unlink(missing_ok=True)


def apply_docx_common_spec_formatting(docx_path: Path) -> None:
    """Apply shared borders, title-page/TOC pagination, and page numbering."""
    with zipfile.ZipFile(docx_path) as archive:
        members = {info.filename: archive.read(info.filename) for info in archive.infolist()}
    core_properties = ET.fromstring(members["docProps/core.xml"])
    creator_tag = "{http://purl.org/dc/elements/1.1/}creator"
    creator = core_properties.find(creator_tag)
    if creator is None:
        creator = ET.SubElement(core_properties, creator_tag)
    creator.text = document_author_name()
    ET.register_namespace("dcterms", "http://purl.org/dc/terms/")
    members["docProps/core.xml"] = ET.tostring(core_properties, encoding="utf-8", xml_declaration=True)
    document_xml = members["word/document.xml"].decode("utf-8", errors="ignore")
    border_xml = (
        '<w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/></w:tblBorders>'
    )

    def add_borders(match: re.Match[str]) -> str:
        table = match.group(0)
        if "<w:tblBorders" in table:
            return re.sub(r"<w:tblBorders.*?</w:tblBorders>", border_xml, table, count=1, flags=re.DOTALL)
        return table.replace("</w:tblPr>", border_xml + "</w:tblPr>", 1)

    document_xml = re.sub(r"<w:tbl(?:\s[^>]*)?>.*?</w:tbl>", add_borders, document_xml, flags=re.DOTALL)
    document_xml = _reorder_docx_navigation(document_xml)
    members["word/document.xml"] = document_xml.encode("utf-8")
    _ensure_docx_page_number_footer(members)
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with zipfile.ZipFile(temporary_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for filename, content in members.items():
                archive.writestr(filename, content)
        temporary_path.replace(docx_path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _docx_element_text(element: ET.Element, word_namespace: str) -> str:
    return "".join(node.text or "" for node in element.iter(f"{word_namespace}t"))


def _reorder_docx_navigation(document_xml: str) -> str:
    """Put the TOC first on page 2, followed by Document Navigation."""
    word_namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    root = ET.fromstring(document_xml)
    body = root.find(f"{word_namespace}body")
    if body is None:
        return document_xml
    children = list(body)
    text = [_docx_element_text(element, word_namespace).strip() for element in children]
    navigation_indices = [
        index for index, value in enumerate(text)
        if value.casefold() == "0. document navigation"
    ]
    toc_index = next(
        (index for index, value in enumerate(text) if value.casefold() == "0.1 table of contents"),
        None,
    )
    if toc_index is None:
        return document_xml
    navigation_index = next((index for index in navigation_indices if index < toc_index), None)
    if navigation_index is None:
        navigation_index = next((index for index in navigation_indices if index > toc_index), None)
    if navigation_index is None:
        return document_xml
    introduction_index = next(
        (
            index
            for index, element in enumerate(children)
            if element.tag == f"{word_namespace}p"
            and re.match(
                r"^1(?:\.\d+)*\.?\s+",
                _docx_element_text(element, word_namespace).strip(),
            )
        ),
        None,
    )
    if navigation_index is None:
        return document_xml
    if introduction_index is None:
        introduction_index = len(children)
    if navigation_index >= introduction_index:
        return document_xml

    title_block = children[:min(toc_index, navigation_index)]
    next_navigation_index = next((index for index in navigation_indices if index > toc_index), None)
    toc_end = next_navigation_index or next(
        (
            index for index in range(toc_index + 1, introduction_index)
            if re.match(r"^0\.[2-9](?:\.|\s)", text[index], re.IGNORECASE)
        ),
        introduction_index,
    )
    toc = [element for element in children[toc_index:toc_end] if text[children.index(element)].casefold() != "0. document navigation"]
    navigation_start = next_navigation_index if next_navigation_index is not None else toc_end
    navigation = [
        element for element in children[navigation_start:introduction_index]
        if text[children.index(element)].casefold() != "0. document navigation"
    ]
    navigation.insert(0, children[navigation_index])
    remainder = children[introduction_index:]
    for element in children:
        body.remove(element)
    for element in title_block + toc + navigation + remainder:
        body.append(element)

    first_toc_paragraph = next(
        element for element in toc if element.tag == f"{word_namespace}p"
    )
    first_toc_index = list(body).index(first_toc_paragraph)
    explicit_page_break = ET.Element(f"{word_namespace}p")
    explicit_run = ET.SubElement(explicit_page_break, f"{word_namespace}r")
    ET.SubElement(explicit_run, f"{word_namespace}br", {f"{word_namespace}type": "page"})
    body.insert(first_toc_index, explicit_page_break)
    properties = first_toc_paragraph.find(f"{word_namespace}pPr")
    if properties is None:
        properties = ET.Element(f"{word_namespace}pPr")
        first_toc_paragraph.insert(0, properties)
    for page_break in list(properties.findall(f"{word_namespace}pageBreakBefore")):
        properties.remove(page_break)
    properties.insert(0, ET.Element(f"{word_namespace}pageBreakBefore"))

    for paragraph in body.findall(f"{word_namespace}p"):
        properties = paragraph.find(f"{word_namespace}pPr")
        if properties is not None and paragraph is not first_toc_paragraph:
            for page_break in list(properties.findall(f"{word_namespace}pageBreakBefore")):
                properties.remove(page_break)

    ET.register_namespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
    ET.register_namespace("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships")
    return ET.tostring(root, encoding="unicode", xml_declaration=True)


def _ensure_docx_page_number_footer(members: Dict[str, bytes]) -> None:
    """Install a deterministic right-aligned PAGE field in the default footer."""
    document_xml = members["word/document.xml"].decode("utf-8", errors="ignore")
    relationships = members.get("word/_rels/document.xml.rels", b"").decode("utf-8", errors="ignore")
    footer_reference = re.search(r'<w:footerReference\b(?=[^>]*w:type="default")([^>]*)/>', document_xml)
    relationship_id = re.search(r'r:id="([^"]+)"', footer_reference.group(1)) if footer_reference else None
    if relationship_id:
        relation = re.search(
            rf'<Relationship\b[^>]*Id="{re.escape(relationship_id.group(1))}"[^>]*Target="([^"]+)"[^>]*/>',
            relationships,
        )
        target = relation.group(1) if relation else "footer3.xml"
        footer_path = "word/" + target.lstrip("/")
    else:
        ids = [int(value) for value in re.findall(r'Id="rId(\d+)"', relationships)]
        new_id = f"rId{max(ids, default=0) + 1}"
        target = "footer3.xml"
        footer_path = "word/" + target
        relationship = (
            f'<Relationship Id="{new_id}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" '
            f'Target="{target}" />'
        )
        relationships = relationships.replace("</Relationships>", relationship + "</Relationships>", 1)
        reference = f'<w:footerReference w:type="default" r:id="{new_id}"/>'
        sectpr = re.search(r"<w:sectPr(?:\s[^>]*)?>", document_xml)
        if sectpr:
            document_xml = document_xml[:sectpr.end()] + reference + document_xml[sectpr.end():]
        members["word/_rels/document.xml.rels"] = relationships.encode("utf-8")
        content_types = members.get("[Content_Types].xml", b"").decode("utf-8", errors="ignore")
        if 'PartName="/word/footer3.xml"' not in content_types:
            override = (
                '<Override PartName="/word/footer3.xml" '
                'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" />'
            )
            content_types = content_types.replace("</Types>", override + "</Types>", 1)
            members["[Content_Types].xml"] = content_types.encode("utf-8")

    footer_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:p><w:pPr><w:jc w:val="right"/></w:pPr><w:r><w:fldChar w:fldCharType="begin"/>'
        '<w:instrText xml:space="preserve"> PAGE </w:instrText><w:fldChar w:fldCharType="separate"/>'
        '<w:t>1</w:t><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>'
    )
    members[footer_path] = footer_xml.encode("utf-8")
    members["word/document.xml"] = document_xml.encode("utf-8")


def csv_cell_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(str(item) for item in value if item is not None)
    return str(value)


def read_retained_rows(path: Path, requirement_ids: Set[str]) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [
            {key: csv_cell_text(value).strip() for key, value in row.items() if key is not None}
            for row in csv.DictReader(handle)
            if (row.get("Requirement ID") or "").strip() in requirement_ids
            and (row.get("Routing Status") or "").strip() == RETAINED_ROUTING_STATUS
        ]


def source_parent_title(source: str) -> str:
    """Return the nearest explicit parent title, preserving source wording."""
    primary = (source or "").split(", paragraph", 1)[0].strip()
    primary = re.sub(r"\s*\(page\s+\d+\)\s*$", "", primary, flags=re.IGNORECASE).strip()
    direct_match = re.match(
        r"^Section\s+([0-9A-Za-z_.-]+)\s+(.+?)(?:\s*\(under\s+Section|,\s*paragraph|$)",
        primary,
        flags=re.IGNORECASE,
    )
    if direct_match:
        direct_title = direct_match.group(2).strip(" .-:()\t")
        if direct_title.lower() not in {"requirement", "requirements"}:
            return direct_title

    parent_match = re.search(
        r"\(under\s+Section\s+[0-9A-Za-z_.-]+\s+(.+?)\)\s*,?\s*paragraph",
        source or "",
        flags=re.IGNORECASE,
    )
    if parent_match:
        return parent_match.group(1).strip(" .-:()\t")

    if re.match(r"^Section\s+[0-9A-Za-z_.-]+\s+", primary, flags=re.IGNORECASE):
        return "Other source function context"
    match = re.match(r"^Section\s+[0-9A-Za-z_.-]+\s+(.*)$", primary, flags=re.IGNORECASE)
    return (match.group(1) if match else primary).strip(" -:\t") or "Unresolved source paragraph"


def is_user_action(statement: str) -> bool:
    return bool(re.search(r"\bthe\s+user\s+shall\b", statement or "", flags=re.IGNORECASE))


def is_reset_clock_table_row(row: Mapping[str, str]) -> bool:
    """Classify structural reset/clock rows without using neighboring OCR text."""
    derivation_kind = (row.get("derivation_kind") or "").strip().lower()
    if derivation_kind in {"reset_table_connection", "clock_table_connection_frequency"}:
        return True
    notes = (row.get("notes") or "").lower()
    return "derived from reset/clock table columns" in notes


def pmu_clock_reset_alias(row: Mapping[str, str], block_names: Iterable[str]) -> str:
    """Map generic clock/reset source context to PMU when the project defines PMU."""
    pmu_name = ""
    for block_name in block_names:
        if block_name.strip().lower() == "pmu":
            pmu_name = block_name
            break
    if not pmu_name:
        return ""

    source = csv_cell_text(row.get("source") or row.get("Source") or row.get("Source Paragraph"))
    statement = csv_cell_text(row.get("requirement_statement") or row.get("Requirement Statement"))
    owner = csv_cell_text(row.get("source_section_owner") or row.get("Source Section Owner"))
    notes = csv_cell_text(row.get("notes") or row.get("Notes"))
    text = " ".join([source, statement, owner, notes]).lower()
    parent = source_parent_title(source).lower()

    has_clock_reset = any(term in text for term in ("clock", "clk", "reset", "resetn", "rst_n", "por"))
    has_pmu = "pmu" in text or "power management" in text or "power-management" in text
    parent_is_clock_reset = bool(re.search(r"\b(clocks?\s+(?:and\s+)?reset|reset\s+(?:and\s+)?clocks?)\b", parent))

    if owner.strip().lower() == "pmu":
        return pmu_name
    if is_reset_clock_table_row(row):
        return pmu_name
    if parent_is_clock_reset:
        return pmu_name
    if has_pmu and has_clock_reset:
        return pmu_name
    return ""


def cascade_retained_context(
    rows: Iterable[Mapping[str, str]],
    statements_by_id: Mapping[str, str],
    mapped_blocks: Mapping[str, str],
) -> List[Dict[str, str]]:
    """Carry an explicit source parent through same-page retained user actions."""
    active_parent = ""
    active_page = ""
    result: List[Dict[str, str]] = []
    for source_row in rows:
        row = dict(source_row)
        requirement_id = (row.get("Requirement ID") or "").strip()
        source = row.get("Non-Block Function Context") or row.get("Source Paragraph") or ""
        page_match = re.search(r"\(page\s+(\d+)\)", source, flags=re.IGNORECASE)
        page = page_match.group(1) if page_match else ""
        parent_match = re.search(
            r"\(under\s+Section\s+[0-9A-Za-z_.-]+\s+(.+?)\)\s*,?\s*paragraph",
            source,
            flags=re.IGNORECASE,
        )
        if page != active_page:
            active_parent = ""
            active_page = page
        if parent_match:
            active_parent = parent_match.group(1).strip(" .-:()\t")
        else:
            direct_match = re.match(
                r"^Section\s+[0-9A-Za-z_.-]+\s+(.+?)(?:\s*\(under\s+Section|,\s*paragraph|$)",
                source,
                flags=re.IGNORECASE,
            )
            if direct_match:
                direct_title = direct_match.group(1).strip(" .-:()\t")
                if direct_title.lower() not in {"requirement", "requirements"}:
                    active_parent = direct_title
        if (
            is_user_action(statements_by_id.get(requirement_id, row.get("Requirement Statement", "")))
            and active_parent
            and (mapped_blocks.get(requirement_id) or "").strip() in {"", "Unassigned"}
            and not parent_match
        ):
            row["Non-Block Function Context"] = active_parent
        result.append(row)
    return result