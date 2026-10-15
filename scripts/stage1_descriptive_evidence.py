"""Deterministic, artifact-only Stage 1 descriptive evidence projection."""

from __future__ import annotations

import csv
import hashlib
import json
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


def extract_indexed_descriptive_candidates(
    index_path: Path,
    *,
    source_context: Mapping[str, Mapping[str, str]] | None = None,
) -> List[Dict[str, str]]:
    """Extract review candidates only; indexed material does not confer approval."""
    with index_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not {"source_file", "page", "text_file"}.issubset(reader.fieldnames or ()):
            raise ValueError("Descriptive source index is missing identity/page/text fields")
        indexed = list(reader)
    sources: Dict[str, Dict[int, Path]] = {}
    for row in indexed:
        source = str(row.get("source_file") or "").strip()
        text_file = str(row.get("text_file") or "").strip()
        if not source or not text_file:
            raise ValueError("Descriptive source index contains an incomplete entry")
        page = int(row["page"])
        if page < 1:
            raise ValueError("Descriptive source page must be positive")
        path = Path(text_file)
        if not path.is_absolute():
            path = index_path.parent / path
        path = path.resolve(strict=True)
        if path.suffix.lower() != ".txt":
            raise ValueError("Descriptive extraction accepts indexed text artifacts only")
        pages = sources.setdefault(source, {})
        if page in pages and pages[page] != path:
            raise ValueError("Conflicting descriptive source page identity")
        pages[page] = path

    records: List[Dict[str, str]] = []
    excluded_heading = re.compile(
        r"\b(?:requirements?|parameters?|ports?|i/o\s+list|register\s+map|"
        r"contents|references|abbreviations|terms\s+and)\b", re.I,
    )
    marker = re.compile(r"^\s*\[[^\]]+\]\s*(?:requirement|assumption|definition|comment|$)", re.I)
    for source, pages in sources.items():
        context = dict((source_context or {}).get(source, {}))
        headings: List[Tuple[str, str]] = []
        current: List[Tuple[int, int, str, str, str]] = []
        active = False
        previous_page = 0

        def flush() -> None:
            if not current:
                return
            statement = " ".join(text.strip() for _page, _line, text, _path, _hash in current)
            spans = [{"page": page, "line": line, "text_file": path, "artifact_sha256": digest}
                     for page, line, _text, path, digest in current]
            current.clear()
            if len(statement) < 20 or len(statement.split()) < 4:
                return
            if re.search(r"\b(?:shall|must|required to)\b|\bCovers:\s*", statement, re.I):
                return
            text_hash = hashlib.sha256(statement.encode("utf-8")).hexdigest()
            section = headings[-1][0] if headings else ""
            identity = json.dumps([source, context, section, spans, text_hash], sort_keys=True)
            records.append({
                "record_id": "source-context-" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24],
                "statement": statement,
                "source_file": source,
                "source_revision": str(context.get("source_revision") or ""),
                "source_revision_id": str(context.get("source_revision_id") or ""),
                "ingestion_id": str(context.get("ingestion_id") or ""),
                "section": section,
                "section_context_json": json.dumps(headings, ensure_ascii=True),
                "source_spans_json": json.dumps(spans, sort_keys=True),
                "content_sha256": text_hash,
                "evidence_kind": "descriptive",
                "admission_state": "candidate",
            })

        for page, path in sorted(pages.items()):
            if previous_page and page != previous_page + 1:
                flush()
                active = False
                headings.clear()
            previous_page = page
            raw = path.read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            lines = raw.decode("utf-8-sig").splitlines()
            for line_number, raw_line in enumerate(lines, start=1):
                line = raw_line.strip()
                heading = re.fullmatch(r"(\d+(?:\.\d+)*)\.?\s+(.+)", line)
                if heading and re.search(r"\.{2,}|\s\d+\s*$", heading[2]):
                    flush()
                    active = False
                    continue
                if heading:
                    flush()
                    depth = heading[1].count(".")
                    while headings and headings[-1][0].count(".") >= depth:
                        headings.pop()
                    headings.append((heading[1], heading[2]))
                    active = not any(excluded_heading.search(title) for _number, title in headings)
                    continue
                if marker.match(line) or line.upper() == "[END]":
                    flush()
                    active = False
                    continue
                if re.match(r"^(?:Figure|Table)\s+\d+\b", line, re.I):
                    flush()
                    active = False
                    continue
                if re.fullmatch(r"\d{1,4}", line):
                    continue
                if not line:
                    flush()
                    continue
                if active and not re.search(r"\t|\|", raw_line):
                    current.append((page, line_number, raw_line, str(path), digest))
                elif current:
                    flush()
        flush()
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