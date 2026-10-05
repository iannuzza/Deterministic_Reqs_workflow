"""Deterministic, artifact-only Stage 1 descriptive evidence projection."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


_OVERVIEW_HEADING = re.compile(
    r"\b(?:overview|introduction|architecture|functional\s+(?:description|overview))\b",
    re.IGNORECASE,
)
_REQUIREMENT_MARKER = re.compile(
    r"^\s*\[[A-Z][A-Z0-9_-]*\]\s+(?:Definition|Assumption|Comment|Requirement)\b",
    re.IGNORECASE,
)


def _ocr_extract_lines(index_path: Path) -> List[Tuple[int, int, str]]:
    """Read only Stage 1 OCR extracts listed by the artifact directory."""
    extracts_dir = index_path.parent
    if not extracts_dir.exists():
        return []
    rows: List[Tuple[int, int, str]] = []
    for path in sorted(extracts_dir.glob("*.txt")):
        match = re.search(r"_p(\d+)\.txt$", path.name)
        page = int(match.group(1)) if match else 0
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        rows.extend((page, number, line.rstrip()) for number, line in enumerate(lines, start=1))
    return rows


def _runtime_block_match(statement: str, block_names: Sequence[str]) -> List[str]:
    matches: List[str] = []
    for block_name in sorted({name.strip() for name in block_names if name.strip()}):
        tokens = [re.escape(token) for token in re.split(r"[-_\s]+", block_name) if token]
        if tokens and re.search(r"\b" + r"[-_\s]+".join(tokens) + r"\b", statement, re.IGNORECASE):
            matches.append(block_name)
    return matches


def _location(locations: Sequence[Tuple[int, int]]) -> str:
    first_page, first_line = locations[0]
    last_page, last_line = locations[-1]
    if first_page == last_page:
        return f"Stage 1 OCR page {first_page}, lines {first_line}-{last_line}"
    return (
        f"Stage 1 OCR page {first_page}, line {first_line}, through "
        f"page {last_page}, line {last_line}"
    )


def extract_stage1_descriptive_evidence(
    index_path: Path,
    *,
    block_names: Sequence[str] = (),
) -> List[Dict[str, str]]:
    """Project complete descriptive paragraphs from Stage 1 OCR artifacts.

    The extractor is intentionally unaware of project names, block catalogs, and
    document-specific topics. Runtime artifacts provide candidate block labels;
    ambiguous matches remain system-scoped and are never assigned by guessing.
    """
    lines = _ocr_extract_lines(index_path)
    paragraphs: List[Tuple[str, List[Tuple[int, int]]]] = []
    active = False
    current: List[Tuple[int, int, str]] = []

    def flush() -> None:
        if not current:
            return
        statement = re.sub(r"\s+", " ", " ".join(text.strip() for _page, _line, text in current)).strip()
        if statement:
            paragraphs.append((statement, [(page, line) for page, line, _text in current]))
        current.clear()

    for page, line_number, raw_line in lines:
        line = raw_line.strip()
        heading = re.match(r"^\s*\d+(?:\.\d+)*\.\s+(.+?)\s*$", line)
        if heading:
            if re.search(r"\.{2,}|\s\d+\s*$", heading.group(1)):
                heading = None
        if heading:
            flush()
            if _OVERVIEW_HEADING.search(heading.group(1)):
                active = True
                continue
            if active:
                break
        if not active:
            continue
        if _REQUIREMENT_MARKER.match(line):
            flush()
            break
        if not line or re.fullmatch(r"\d{1,3}", line) or re.match(r"^(?:Figure|Table)\s+\d+\b", line, re.IGNORECASE):
            flush()
            continue
        if line.startswith(("•", "- ", "* ")):
            candidate = re.sub(r"^(?:•|-|\*)\s*", "", line).strip()
            matches = _runtime_block_match(candidate, block_names)
            if len(matches) == 1 and candidate:
                flush()
                paragraphs.append((candidate.rstrip(".") + ".", [(page, line_number)]))
            else:
                flush()
            continue
        current.append((page, line_number, line))
    flush()

    records: List[Dict[str, str]] = []
    for statement, locations in paragraphs:
        if len(statement) < 20 or not re.search(r"[.!?]\s*$", statement):
            continue
        if re.search(r"\b(?:shall|must|required to)\b", statement, re.IGNORECASE):
            continue
        matches = _runtime_block_match(statement, block_names)
        scope = "block_local" if len(matches) == 1 else "system"
        record = {
            "statement": statement,
            "source": _location(locations),
            "source_evidence": statement,
            "scope": scope,
            "record_type": "stage1_descriptive_evidence",
            "evidence_kind": "descriptive",
        }
        if len(matches) == 1:
            record["mapped_block"] = matches[0]
        records.append(record)
    return records


def validate_stage1_descriptive_records(records: Iterable[Mapping[str, object]]) -> List[str]:
    """Validate the shared evidence shape without validating normative authority."""
    findings: List[str] = []
    for index, record in enumerate(records):
        statement = str(record.get("statement") or "").strip()
        source = str(record.get("source") or "").strip()
        scope = str(record.get("scope") or "").strip()
        if not statement or not source:
            findings.append(f"stage1_descriptive_record_{index}_missing_statement_or_provenance")
        if scope not in {"system", "block_local"}:
            findings.append(f"stage1_descriptive_record_{index}_invalid_scope")
        if re.search(r"\b(?:shall|must|required to)\b", statement, re.IGNORECASE):
            findings.append(f"stage1_descriptive_record_{index}_contains_normative_modality")
        if re.search(r"\bCovers:\s*", statement, re.IGNORECASE):
            findings.append(f"stage1_descriptive_record_{index}_contains_normative_linkage")
    return findings