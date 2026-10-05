#!/usr/bin/env python3
"""Stage 1 quality control: fix split/truncated requirements and cross-check with RAG.

- Reads requirements_summary.csv
- Repairs likely split/truncated statements using OCR line context
- Verifies each final statement against RAG chunks (exact/overlap)
- Rewrites requirements_summary.csv in-place
- Writes cross-check report artifact
"""

from __future__ import annotations

import argparse
import csv
import difflib
import html as html_lib
import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

TRAILING_BAD_ENDINGS = {
    "and",
    "or",
    "to",
    "of",
    "for",
    "in",
    "on",
    "at",
    "with",
    "from",
    "that",
    "the",
    "a",
    "an",
    "be",
}

NORMATIVE_HINT = re.compile(
    r"\b(shall|must|mandatory|required|needs?\s+to|shall\s+not|must\s+not|not\s+be)\b",
    flags=re.IGNORECASE,
)

SOURCE_REF = re.compile(r"p(?P<page>\d{3}):l(?P<line>\d+)")
ROP_SOURCE_REF = re.compile(r"\bROP-(?P<page>\d{3})\.(?P<paragraph>\d{3})\b", flags=re.IGNORECASE)
SECTION_PARAGRAPH_SOURCE_REF = re.compile(
    r"^Section\s+(?P<section>\d+(?:\.\d+)*)\s+.+?,\s+paragraph\s+(?P<paragraph>\d+)\s+\(page\s+(?P<page>\d+)\)$",
    flags=re.IGNORECASE,
)
PARAGRAPH_SOURCE_REF = re.compile(
    r"^Paragraph\s+(?P<paragraph>\d+)\s+\(page\s+(?P<page>\d+)\)$",
    flags=re.IGNORECASE,
)
DEFAULT_REQ_ID_PATTERN = r"[A-Z][A-Z0-9]*(?:\.\d+)*[A-Z0-9]*"
REQ_ID_PATTERN = DEFAULT_REQ_ID_PATTERN
SOURCE_REQ_ID_NOTE_RE = re.compile(rf"\bsource_req_id=(?P<reqid>{REQ_ID_PATTERN})\b")
REQ_ID_INLINE_DEFINITION_RE = re.compile(rf"\b(?P<reqid>{REQ_ID_PATTERN})\s*:\s*")
REQ_ID_DEFINITION_RE = re.compile(rf"^\s*(?P<reqid>{REQ_ID_PATTERN})\s*:\s*(?P<body>.*)$")
REQ_ID_ONLY_RE = re.compile(rf"^\s*(?P<reqid>{REQ_ID_PATTERN})\s*$")
TAGGED_SOURCE_MODE = False
TAG_REQUIREMENT_LABEL = "Requirement"
TAG_TERMINATOR = "[End]"
REQ_ID_TAGGED_START_RE = re.compile(rf"^\s*\[(?P<reqid>{REQ_ID_PATTERN})\]\s*{re.escape(TAG_REQUIREMENT_LABEL)}\s*:\s*(?P<body>.*)$", re.IGNORECASE)
SOURCE_FORMAT_RE = re.compile(
    r"^(?:ROP-\d{3}\.\d{3}\s+\(page\s+\d+\)|Section\s+\d+(?:\.\d+)*\s+.+?,\s+paragraph\s+\d+\s+\(page\s+\d+\)|Paragraph\s+\d+\s+\(page\s+\d+\))$",
    flags=re.IGNORECASE,
)
ALLOWED_EVIDENCE = {"explicit", "derived-from-structure"}
ALLOWED_CONTENT_CLASS = {"Definition", "Requirement", "Validation constraint", "Configuration", "Description"}
ALLOWED_REQUIREMENT_TYPE = {"functional", "interface", "timing", "electrical", "configuration", "safety", "mode-behavior", "other"}
ID_PREFIX_TO_CLASS = {
    "REQ": "Requirement",
    "CONF": "Configuration",
    "VAL_CONSTR": "Validation constraint",
    "DEF": "Definition",
    "DES": "Description",
}
GENERATED_ID_RE = re.compile(r"^(REQ|CONF|VAL_CONSTR|DEF|DES)_(SYS|ANA|DIG)-RQ-\d{3}$")


@dataclass
class CrosscheckResult:
    changed: bool
    old_statement: str
    new_statement: str
    status: str
    details: str


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\n")


def _load_project_context(repo_root: Path) -> Dict[str, object]:
    config_path = repo_root / "config/project_context.json"
    if not config_path.exists():
        return {}
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _compile_requirement_id_regexes(req_id_pattern: str) -> None:
    global REQ_ID_PATTERN
    global SOURCE_REQ_ID_NOTE_RE
    global REQ_ID_INLINE_DEFINITION_RE
    global REQ_ID_DEFINITION_RE
    global REQ_ID_ONLY_RE
    global REQ_ID_TAGGED_START_RE

    REQ_ID_PATTERN = req_id_pattern
    SOURCE_REQ_ID_NOTE_RE = re.compile(rf"\bsource_req_id=(?P<reqid>{REQ_ID_PATTERN})\b")
    REQ_ID_INLINE_DEFINITION_RE = re.compile(rf"\b(?P<reqid>{REQ_ID_PATTERN})\s*:\s*")
    REQ_ID_DEFINITION_RE = re.compile(rf"^\s*(?P<reqid>{REQ_ID_PATTERN})\s*:\s*(?P<body>.*)$")
    REQ_ID_ONLY_RE = re.compile(rf"^\s*(?P<reqid>{REQ_ID_PATTERN})\s*$")
    REQ_ID_TAGGED_START_RE = re.compile(
        rf"^\s*\[(?P<reqid>{REQ_ID_PATTERN})\]\s*{re.escape(TAG_REQUIREMENT_LABEL)}\s*:\s*(?P<body>.*)$",
        re.IGNORECASE,
    )


def _init_requirement_id_rules(repo_root: Path) -> None:
    global TAGGED_SOURCE_MODE
    global TAG_REQUIREMENT_LABEL
    global TAG_TERMINATOR

    context = _load_project_context(repo_root)
    rules = context.get("requirement_id_rules")
    req_pattern = DEFAULT_REQ_ID_PATTERN

    if isinstance(rules, dict):
        pattern_list = rules.get("source_req_id_patterns")
        if isinstance(pattern_list, list):
            normalized_patterns = [str(p).strip() for p in pattern_list if str(p).strip()]
            if normalized_patterns:
                if len(normalized_patterns) == 1:
                    req_pattern = normalized_patterns[0]
                else:
                    req_pattern = "(?:" + "|".join(normalized_patterns) + ")"

        TAGGED_SOURCE_MODE = bool(rules.get("tagged_source_mode", False))
        TAG_REQUIREMENT_LABEL = str(rules.get("tag_label") or "Requirement").strip() or "Requirement"
        TAG_TERMINATOR = str(rules.get("tag_terminator") or "[End]").strip() or "[End]"

    _compile_requirement_id_regexes(req_pattern)


def _load_image_block_rules(repo_root: Path) -> Dict[str, List[Dict[str, object]]]:
    context = _load_project_context(repo_root)
    raw_rules = context.get("image_block_rules")
    if not isinstance(raw_rules, dict):
        return {}
    normalized: Dict[str, List[Dict[str, object]]] = {}
    for image_label, rules in raw_rules.items():
        if not isinstance(image_label, str) or not isinstance(rules, list):
            continue
        cleaned_rules = [r for r in rules if isinstance(r, dict)]
        if cleaned_rules:
            normalized[image_label] = cleaned_rules
    return normalized


def _clean(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"\s+", " ", text.strip())
    return text


def _norm(text: str) -> str:
    text = _clean(text).lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _looks_complete(statement: str) -> bool:
    s = _clean(statement)
    if len(s) < 35:
        return False
    words = s.split()
    if len(words) < 7:
        return False
    last = re.sub(r"[^a-zA-Z]", "", words[-1]).lower()
    if last in TRAILING_BAD_ENDINGS:
        return False
    if s.endswith((":", ",", "-", "(")):
        return False
    # Many OCR lines don't end with '.', so accept long enough complete-looking phrases.
    if s.endswith((".", ";")):
        return True
    return len(words) >= 11


def _is_section_or_heading(line: str) -> bool:
    l = _clean(line)
    if re.match(r"^\d+(?:\.\d+){0,3}\s+[A-Za-z]", l):
        return True
    if re.match(r"^section\s+\d+", l.lower()):
        return True
    if re.match(r"^(table|figure)\s+\d+[-.]\d+", l.lower()):
        return True
    return False


def _is_colon_continuation_line(line: str) -> bool:
    l = _clean(line)
    if not l:
        return False
    if l in {"-", "*", "•"}:
        return True
    if re.search(r"(<|>|=|%)", l):
        return True
    if re.search(r"\b(good|acceptable|unacceptable|min|max)\b", l.lower()):
        return True
    return False


def _token_overlap(a: str, b: str) -> float:
    ta = set(_norm(a).split())
    tb = set(_norm(b).split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(1, len(ta))


def _text_quality_score(text: str) -> float:
    words = re.findall(r"[A-Za-z0-9%+\-]+", text)
    if not words:
        return 0.0
    strong = sum(1 for w in words if len(w) >= 3)
    alpha = sum(1 for ch in text if ch.isalpha())
    weird = text.count(" o ") + text.count(" i ")
    return (strong / len(words)) + (alpha / max(1, len(text))) - (0.02 * weird)


def _is_footer_or_page_noise(line: str) -> bool:
    l = line.lower()
    if "customer, inc" in l:
        return True
    if re.match(r"^\(?[ivx]+\)?\s*$", l):
        return True
    if re.match(r"^\d+\s*/\s*\d+$", l):
        return True
    return False


def _extract_text_from_html_fragment(fragment: str) -> str:
    no_tags = re.sub(r"<[^>]+>", " ", fragment)
    unescaped = html_lib.unescape(no_tags)
    return _clean(unescaped)


def _extract_inline_reqid_segments(text: str) -> List[Tuple[str, str]]:
    cleaned = _clean(text)
    if not cleaned:
        return []

    matches = list(REQ_ID_INLINE_DEFINITION_RE.finditer(cleaned))
    if not matches:
        return []

    segments: List[Tuple[str, str]] = []
    for idx, m in enumerate(matches):
        req_id = (m.group("reqid") or "").upper()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(cleaned)
        body = _clean(cleaned[start:end].lstrip("•*- "))
        body = _trim_at_next_definition_token(body, req_id)
        if req_id and body:
            segments.append((req_id, body))
    return segments


def _split_by_tag_terminator(text: str) -> Tuple[str, bool]:
    cleaned = _clean(text)
    if not cleaned:
        return "", False
    token = TAG_TERMINATOR.lower()
    idx = cleaned.lower().find(token)
    if idx < 0:
        return cleaned, False
    return _clean(cleaned[:idx]), True


def _extract_tagged_reqid_candidate(lines: List[str], start_idx: int) -> Tuple[Optional[str], Optional[str], int]:
    if not TAGGED_SOURCE_MODE:
        return None, None, start_idx

    start_line = _clean(lines[start_idx])
    match = REQ_ID_TAGGED_START_RE.match(start_line)
    if not match:
        return None, None, start_idx

    req_id = (match.group("reqid") or "").upper()
    first_body = _clean(match.group("body") or "")
    first_body, closed = _split_by_tag_terminator(first_body)
    parts: List[str] = [first_body] if first_body else []
    end_idx = start_idx

    if not closed:
        for j in range(start_idx + 1, min(len(lines), start_idx + 40)):
            nxt = _clean(lines[j])
            if not nxt:
                continue
            if REQ_ID_TAGGED_START_RE.match(nxt):
                end_idx = j - 1
                break

            part, found_end = _split_by_tag_terminator(nxt)
            if part:
                parts.append(part)
            end_idx = j
            if found_end:
                break

    return req_id, _clean(" ".join(parts)), max(end_idx, start_idx)


def _extract_html_reqid_definitions(source_html: Path) -> Dict[str, str]:
    html_text = source_html.read_text(encoding="utf-8", errors="ignore")
    p_fragments = re.findall(r"(?is)<p\b[^>]*>(.*?)</p>", html_text)
    lines = [_extract_text_from_html_fragment(frag) for frag in p_fragments]
    lines = [line for line in lines if line]

    req_map: Dict[str, str] = {}

    if TAGGED_SOURCE_MODE:
        idx = 0
        while idx < len(lines):
            req_id, statement, consumed_idx = _extract_tagged_reqid_candidate(lines, idx)
            if req_id and statement:
                existing = req_map.get(req_id, "")
                if _text_quality_score(statement) >= _text_quality_score(existing):
                    req_map[req_id] = statement
                idx = consumed_idx + 1
                continue
            idx += 1

    for idx, raw in enumerate(lines):
        m = REQ_ID_DEFINITION_RE.match(raw)
        if not m:
            continue

        req_id = (m.group("reqid") or "").upper()
        body = _clean(m.group("body") or "")
        parts: List[str] = [body] if body else []
        bullet_mode = body.endswith(":")

        for j in range(idx + 1, min(len(lines), idx + 13)):
            nxt = _clean(lines[j])
            if not nxt:
                continue
            if REQ_ID_DEFINITION_RE.match(nxt) or REQ_ID_ONLY_RE.match(nxt):
                break
            if (not bullet_mode) and _is_section_or_heading(nxt):
                break
            if _is_footer_or_page_noise(nxt):
                break

            parts.append(nxt)
            if nxt.endswith(".") or nxt.endswith(";"):
                break

        merged = _trim_at_next_definition_token(_clean(" ".join(parts)), req_id)
        if merged:
            req_map[req_id] = merged

    for idx, raw in enumerate(lines):
        m = REQ_ID_ONLY_RE.match(raw)
        if not m:
            continue

        req_id = (m.group("reqid") or "").upper()
        parts: List[str] = []
        for j in range(idx + 1, min(len(lines), idx + 10)):
            nxt = _clean(lines[j])
            if not nxt:
                continue
            if REQ_ID_DEFINITION_RE.match(nxt) or REQ_ID_ONLY_RE.match(nxt):
                break
            if _is_section_or_heading(nxt) or _is_footer_or_page_noise(nxt):
                break

            parts.append(nxt)
            if nxt.endswith(".") or nxt.endswith(";"):
                break

        merged = _trim_at_next_definition_token(_clean(" ".join(parts)), req_id)
        if merged and NORMATIVE_HINT.search(merged):
            existing = req_map.get(req_id, "")
            if _text_quality_score(merged) >= _text_quality_score(existing):
                req_map[req_id] = merged

    # Handle multiple inline definitions on a single line, e.g. R3.1 : ... R3.2 : ...
    for raw in lines:
        for req_id, body in _extract_inline_reqid_segments(raw):
            existing = req_map.get(req_id, "")
            if _text_quality_score(body) >= _text_quality_score(existing):
                req_map[req_id] = body

    return req_map


def _extract_html_page_lines(source_html: Path) -> Dict[int, List[str]]:
    html_text = source_html.read_text(encoding="utf-8", errors="ignore")
    sections = re.findall(r"(?is)<section\b[^>]*class=\"page\"[^>]*>(.*?)</section>", html_text)
    page_map: Dict[int, List[str]] = {}

    for section in sections:
        m_page = re.search(r"(?is)<div\b[^>]*class=\"page-title\"[^>]*>\s*Page\s*(\d+)\s*</div>", section)
        if not m_page:
            continue

        page_no = int(m_page.group(1))
        p_fragments = re.findall(r"(?is)<p\b[^>]*>(.*?)</p>", section)
        lines: List[str] = []
        for frag in p_fragments:
            line = _extract_text_from_html_fragment(frag)
            # Keep empty placeholders to preserve line-number alignment with OCR extracts.
            lines.append(line)

        if lines:
            page_map[page_no] = lines

    return page_map


def _char_similarity(a: str, b: str) -> float:
    aa = re.sub(r"[^a-z0-9]", "", _clean(a).lower())
    bb = re.sub(r"[^a-z0-9]", "", _clean(b).lower())
    if not aa or not bb:
        return 0.0
    return difflib.SequenceMatcher(None, aa, bb).ratio()


def _build_html_candidate(lines: List[str], start_idx: int) -> str:
    parts: List[str] = []
    for j in range(start_idx, min(len(lines), start_idx + 10)):
        cur = _clean(lines[j])
        if not cur:
            continue
        if _is_footer_or_page_noise(cur):
            continue
        if cur.lower().startswith(("title:", "number:", "rev:", "size:", "scale:")):
            continue
        if _is_section_or_heading(cur):
            break
        parts.append(cur)
        if cur.endswith("."):
            break
    return _clean(" ".join(parts))


def _find_best_html_page_statement(statement: str, source: str, page_lines: Dict[int, List[str]]) -> Optional[str]:
    ref = _parse_source(source)
    if not ref:
        return None

    page, line_no = ref
    lines = page_lines.get(page)
    if not lines:
        return None

    best_idx = -1
    best_score = 0.0
    # Prefer a local search around source line hint (pXXX:lYYY) to align with OCR extract numbering.
    anchor = max(0, min(len(lines) - 1, line_no - 1))
    local_start = max(0, anchor - 8)
    local_end = min(len(lines), anchor + 9)
    for idx in range(local_start, local_end):
        line = lines[idx]
        tok = _token_overlap(statement, line)
        chs = _char_similarity(statement, line)
        score = max(tok, chs)
        if score > best_score:
            best_score = score
            best_idx = idx

    # Fallback to full-page search if local area is too weak.
    if best_idx < 0 or best_score < 0.24:
        for idx, line in enumerate(lines):
            tok = _token_overlap(statement, line)
            chs = _char_similarity(statement, line)
            score = max(tok, chs)
            if score > best_score:
                best_score = score
                best_idx = idx

    if best_idx < 0 or best_score < 0.24:
        # Final fallback: start from source line directly when similarity is poor but page/source are known.
        best_idx = anchor

    candidate = _build_html_candidate(lines, best_idx)
    if not candidate or not NORMATIVE_HINT.search(candidate):
        # Global fallback restricted to normative-looking HTML lines.
        fallback_best = None
        fallback_score = 0.0
        for idx, line in enumerate(lines):
            if not NORMATIVE_HINT.search(line):
                continue
            tok = _token_overlap(statement, line)
            chs = _char_similarity(statement, line)
            score = max(tok, chs)
            if score > fallback_score:
                fallback_score = score
                fallback_best = idx
        if fallback_best is None:
            return None
        candidate = _build_html_candidate(lines, fallback_best)
        if not candidate or not NORMATIVE_HINT.search(candidate):
            return None

    cand_overlap = _token_overlap(statement, candidate)
    cand_char = _char_similarity(statement, candidate)
    if max(cand_overlap, cand_char) < 0.20:
        return None
    return candidate


def _prefer_html_statement(current: str, html_stmt: str) -> bool:
    cur = _clean(current)
    hst = _clean(html_stmt)
    if not hst:
        return False
    if _norm(cur) == _norm(hst):
        return False
    # Prefer HTML if it is clearly cleaner or longer while still normative.
    cur_score = _text_quality_score(cur)
    html_score = _text_quality_score(hst)
    if html_score > cur_score + 0.1:
        return True
    if len(hst) > len(cur) and html_score >= cur_score:
        return True
    return False


def _strip_existing_rag_note(notes: str) -> str:
    cleaned = re.sub(r"\s*\|\s*rag_crosscheck=[^|]+", "", notes or "")
    return cleaned.strip(" |")


def _extract_source_req_id_from_row(row: Dict[str, str]) -> str:
    direct = (row.get("source_req_id") or "").strip()
    if direct:
        return direct.upper()
    notes = row.get("notes", "") or ""
    source_req_match = SOURCE_REQ_ID_NOTE_RE.search(notes)
    return (source_req_match.group("reqid") if source_req_match else "").upper()


def _extract_id_policy_from_row(row: Dict[str, str]) -> str:
    direct = (row.get("id_policy") or "").strip().lower()
    if direct:
        return direct
    notes = (row.get("notes") or "").lower()
    if "id_policy=preserve_tagged_source_id" in notes:
        return "tagged_preserve"
    return "generated_standard"


def _parse_source(source: str) -> Optional[Tuple[int, int]]:
    m = SOURCE_REF.search(source or "")
    if m:
        return int(m.group("page")), int(m.group("line"))
    rop_match = ROP_SOURCE_REF.search(source or "")
    if rop_match:
        return int(rop_match.group("page")), int(rop_match.group("paragraph"))
    section_para_match = SECTION_PARAGRAPH_SOURCE_REF.match((source or "").strip())
    if section_para_match:
        return int(section_para_match.group("page")), int(section_para_match.group("paragraph"))
    para_match = PARAGRAPH_SOURCE_REF.match((source or "").strip())
    if para_match:
        return int(para_match.group("page")), int(para_match.group("paragraph"))
    return None


def _trim_at_next_definition_token(text: str, current_req_id: str) -> str:
    if not text:
        return text
    current = (current_req_id or "").upper()
    for m in REQ_ID_INLINE_DEFINITION_RE.finditer(text):
        token = (m.group("reqid") or "").upper()
        if token and token != current:
            return text[: m.start()].strip()
    return text.strip()


def _contains_new_definition_token(text: str, current_req_id: str) -> bool:
    current = (current_req_id or "").upper()
    for m in REQ_ID_INLINE_DEFINITION_RE.finditer(text or ""):
        token = (m.group("reqid") or "").upper()
        if token and token != current:
            return True
    return False


def _load_index(index_csv: Path) -> Tuple[Dict[int, Path], Optional[str]]:
    page_to_file: Dict[int, Path] = {}
    source_spec: Optional[str] = None
    with index_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if (row.get("status") or "").strip() != "text-extracted":
                continue
            if not source_spec and (row.get("source_file") or "").strip():
                source_spec = (row.get("source_file") or "").strip()
            page = int(row["page"])
            page_to_file[page] = Path(row["text_file"])
    return page_to_file, source_spec


def _maybe_rebuild_statement(statement: str, source: str, req_id: str, page_to_file: Dict[int, Path]) -> str:
    ref = _parse_source(source)
    if not ref:
        return _trim_at_next_definition_token(_clean(statement), req_id)

    page, line_no = ref
    text_file = page_to_file.get(page)
    if not text_file or not text_file.exists():
        return _trim_at_next_definition_token(_clean(statement), req_id)

    lines = text_file.read_text(encoding="utf-8", errors="ignore").splitlines()
    if line_no < 1 or line_no > len(lines):
        return _trim_at_next_definition_token(_clean(statement), req_id)

    idx = line_no - 1

    # Include previous line when current line looks like continuation.
    start_idx = idx
    cur = _clean(lines[idx])
    if idx > 0:
        prev = _clean(lines[idx - 1])
        if cur[:1].islower() or cur.lower().startswith(("and ", "or ", "for ", "that ")):
            if NORMATIVE_HINT.search(prev):
                start_idx = idx - 1

    candidate = _trim_at_next_definition_token(_clean(lines[start_idx]), req_id)
    max_join = 8 if candidate.endswith(":") else 5
    for j in range(start_idx + 1, min(len(lines), start_idx + 1 + max_join)):
        if _looks_complete(candidate):
            break
        nxt = _clean(lines[j])
        if not nxt:
            continue
        if _is_section_or_heading(nxt):
            break
        if len(nxt) < 4 and not _is_colon_continuation_line(nxt):
            continue
        if REQ_ID_INLINE_DEFINITION_RE.match(nxt):
            break
        # Avoid TOC-like fragments.
        if re.search(r"\.{5,}\s*\d{1,4}\s*$", nxt.lower()):
            continue
        nxt = _trim_at_next_definition_token(nxt, req_id)
        if not nxt:
            break
        candidate = _clean(candidate + " " + nxt)

    # Keep repaired only if it keeps normative intent and is not shorter.
    old_norm = _norm(statement)
    new_norm = _norm(candidate)
    if not new_norm:
        return _trim_at_next_definition_token(_clean(statement), req_id)
    if len(new_norm) < len(old_norm):
        return _trim_at_next_definition_token(_clean(statement), req_id)
    if not NORMATIVE_HINT.search(candidate) and NORMATIVE_HINT.search(statement):
        return _trim_at_next_definition_token(_clean(statement), req_id)

    # If original appears embedded in candidate, prefer candidate.
    if old_norm and old_norm in new_norm and len(new_norm) >= len(old_norm):
        return candidate

    # Otherwise use candidate only if statement looked incomplete and candidate looks complete.
    if not _looks_complete(statement) and _looks_complete(candidate):
        return candidate

    return _trim_at_next_definition_token(_clean(statement), req_id)


def _rag_check(conn: sqlite3.Connection, statement: str, source: str) -> Tuple[str, str]:
    ref = _parse_source(source)
    norm_stmt = _norm(statement)
    if not norm_stmt:
        return "fail", "empty_statement"

    page = ref[0] if ref else None
    if page is not None:
        rows = conn.execute(
            "SELECT chunk_text FROM chunks WHERE page = ?",
            (page,),
        ).fetchall()
    else:
        rows = conn.execute("SELECT chunk_text FROM chunks LIMIT 200").fetchall()

    if not rows:
        return "warn", "no_rag_rows_for_source"

    best_overlap = 0.0
    exact = False

    def inspect(candidate_rows: list[tuple[str]]) -> None:
        nonlocal best_overlap, exact
        for (chunk_text,) in candidate_rows:
            n_chunk = _norm(chunk_text)
            if not n_chunk:
                continue
            if norm_stmt in n_chunk:
                exact = True
                return
            ov = _token_overlap(statement, chunk_text)
            if ov > best_overlap:
                best_overlap = ov

    inspect(rows)
    # OCR tags can end one page before the normative body. Include adjacent
    # pages only when the primary source page does not provide a good match.
    if page is not None and not exact and best_overlap < 0.65:
        adjacent_rows = conn.execute(
            "SELECT chunk_text FROM chunks WHERE page IN (?, ?)",
            (page - 1, page + 1),
        ).fetchall()
        inspect(adjacent_rows)

    if exact:
        return "ok", "exact_match"

    return_status = "warn"
    if best_overlap >= 0.85:
        return return_status, f"high_overlap={best_overlap:.2f}"
    if best_overlap >= 0.65:
        return return_status, f"partial_overlap={best_overlap:.2f}"
    return "fail", f"low_overlap={best_overlap:.2f}"

def _update_summary_md(csv_path: Path, summary_md: Path) -> None:
    rows: List[Dict[str, str]] = []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    lines = [
        "# Functional Requirements Summary",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join(["---"] * len(fieldnames)) + " |",
    ]
    for row in rows:
        cells = [(row.get(name, "") or "").replace("|", "\\|") for name in fieldnames]
        lines.append("| " + " | ".join(cells) + " |")
    summary_md.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _update_raw_md(csv_path: Path, raw_md: Path) -> None:
    rows: List[Dict[str, str]] = []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    groups: Dict[str, List[Dict[str, str]]] = {"System": [], "Analog": [], "Digital": []}
    for row in rows:
        groups.setdefault(row.get("category", "System"), []).append(row)

    lines = [
        "# Extracted Functional Requirements (Raw)",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
    ]

    for cat in ["System", "Analog", "Digital"]:
        lines.append(f"## {cat}")
        items = groups.get(cat, [])
        if not items:
            lines.append("- No requirements extracted.")
        else:
            for row in items:
                lines.append(f"- {row.get('id','')}: {row.get('requirement_statement','')} ({row.get('source','')})")
        lines.append("")

    raw_md.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _append_report(report_path: Path, total: int, changed: int, ok: int, warn: int, fail: int) -> None:
    base = ""
    if report_path.exists():
        base = report_path.read_text(encoding="utf-8", errors="ignore").rstrip() + "\n\n"

    block = [
        "## Stage1 Text Quality Cross-Check",
        f"- Checked requirements: {total}",
        f"- Corrected split/truncated statements: {changed}",
        f"- RAG exact matches: {ok}",
        f"- RAG warnings: {warn}",
        f"- RAG fails: {fail}",
    ]
    report_path.write_text(base + "\n".join(block) + "\n", encoding="utf-8")

def _evaluate_rule_checks(rows: List[Dict[str, str]], repo_root: Path) -> Tuple[List[str], int, int]:
    checks: List[str] = []
    warn_count = 0
    fail_count = 0

    def add_check(name: str, status: str, detail: str) -> None:
        nonlocal warn_count, fail_count
        checks.append(f"- {name}: {status} ({detail})")
        if status == "WARN":
            warn_count += 1
        if status == "FAIL":
            fail_count += 1

    total = len(rows)
    if total == 0:
        add_check("summary rows", "FAIL", "no rows found")
        return checks, warn_count, fail_count

    missing_source = sum(1 for r in rows if not SOURCE_FORMAT_RE.match((r.get("source") or "").strip()))
    add_check(
        "source format rule",
        "PASS" if missing_source == 0 else "FAIL",
        f"invalid_sources={missing_source}/{total}",
    )

    invalid_evidence = sum(1 for r in rows if (r.get("evidence_type") or "").strip() not in ALLOWED_EVIDENCE)
    add_check(
        "evidence type rule",
        "PASS" if invalid_evidence == 0 else "FAIL",
        f"invalid_evidence={invalid_evidence}/{total}",
    )

    invalid_content_class = sum(1 for r in rows if (r.get("content_class") or "").strip() not in ALLOWED_CONTENT_CLASS)
    add_check(
        "content class vocabulary",
        "PASS" if invalid_content_class == 0 else "FAIL",
        f"invalid_content_class={invalid_content_class}/{total}",
    )

    invalid_req_type = sum(1 for r in rows if (r.get("requirement_type") or "").strip() not in ALLOWED_REQUIREMENT_TYPE)
    add_check(
        "requirement type vocabulary",
        "PASS" if invalid_req_type == 0 else "FAIL",
        f"invalid_requirement_type={invalid_req_type}/{total}",
    )

    id_class_mismatch = 0
    for r in rows:
        rid = (r.get("id") or "").strip()
        content_class = (r.get("content_class") or "").strip()
        prefix = rid.split("_", 1)[0] if "_" in rid else ""
        expected = ID_PREFIX_TO_CLASS.get(prefix)
        if expected and expected != content_class:
            id_class_mismatch += 1
    add_check(
        "ID prefix vs content class",
        "PASS" if id_class_mismatch == 0 else "FAIL",
        f"mismatch={id_class_mismatch}/{total}",
    )

    tagged_id_mismatch = 0
    generated_id_mismatch = 0
    generated_rows_in_tagged_mode = 0
    missing_source_req_id_in_tagged_mode = 0
    for r in rows:
        rid = (r.get("id") or "").strip()
        source_req_id = _extract_source_req_id_from_row(r)
        id_policy = _extract_id_policy_from_row(r)
        if id_policy == "tagged_preserve" and source_req_id and rid != source_req_id:
            tagged_id_mismatch += 1
        if id_policy == "tagged_architecture" and (not rid or source_req_id):
            tagged_id_mismatch += 1
        if id_policy == "generated_standard" and rid and not GENERATED_ID_RE.match(rid):
            generated_id_mismatch += 1
        if TAGGED_SOURCE_MODE and id_policy == "generated_standard":
            generated_rows_in_tagged_mode += 1
        if TAGGED_SOURCE_MODE and not source_req_id and id_policy != "tagged_architecture":
            missing_source_req_id_in_tagged_mode += 1

    add_check(
        "tagged preserve id rule",
        "PASS" if tagged_id_mismatch == 0 else "FAIL",
        f"mismatch={tagged_id_mismatch}/{total}",
    )
    add_check(
        "generated id format rule",
        "PASS" if generated_id_mismatch == 0 else "WARN",
        f"mismatch={generated_id_mismatch}/{total}",
    )
    add_check(
        "strict tagged mode no-generated rule",
        "PASS" if generated_rows_in_tagged_mode == 0 else "FAIL",
        f"generated_standard_rows={generated_rows_in_tagged_mode}/{total}",
    )
    add_check(
        "strict tagged mode source_req_id presence",
        "PASS" if missing_source_req_id_in_tagged_mode == 0 else "FAIL",
        f"missing_source_req_id_rows={missing_source_req_id_in_tagged_mode}/{total}",
    )

    trace_mismatch = 0
    for r in rows:
        cc = (r.get("content_class") or "").strip()
        tr = (r.get("test_trace_required") or "").strip().lower()
        expected = "yes" if cc in {"Requirement", "Configuration", "Validation constraint"} else "no"
        if tr != expected:
            trace_mismatch += 1
    add_check(
        "test trace required rule",
        "PASS" if trace_mismatch == 0 else "FAIL",
        f"mismatch={trace_mismatch}/{total}",
    )

    notes_lower = [(r.get("notes") or "").lower() for r in rows]
    table_rows = sum(1 for n in notes_lower if "table row value" in n)
    add_check(
        "ontology table-row extraction",
        "PASS" if table_rows >= 10 else "WARN",
        f"table_candidates={table_rows}",
    )

    image_rows = sum(1 for n in notes_lower if "image/caption context" in n)
    sub_block_rows = sum(1 for n in notes_lower if "sub-block/interface" in n)
    add_check(
        "ontology image extraction",
        "PASS" if image_rows >= 5 and sub_block_rows >= 5 else "WARN",
        f"image_candidates={image_rows}, sub_block_candidates={sub_block_rows}",
    )

    image_statements_lower = [
        (r.get("requirement_statement") or "").lower()
        for r in rows
        if "image/caption context" in (r.get("notes") or "").lower()
    ]
    image_block_rules = _load_image_block_rules(repo_root)
    missing_image_blocks: List[str] = []
    for image_label, rules in image_block_rules.items():
        image_label_lower = image_label.lower()
        for rule in rules:
            block_name = str(rule.get("name") or "unnamed_block")
            match_any = rule.get("match_any")
            if not isinstance(match_any, list):
                trigger_any = rule.get("trigger_any")
                match_any = trigger_any if isinstance(trigger_any, list) else []
            terms = [str(t).lower() for t in match_any if isinstance(t, str) and t.strip()]
            if not terms:
                continue
            present = any(
                (image_label_lower in stmt) and any(term in stmt for term in terms)
                for stmt in image_statements_lower
            )
            if not present:
                missing_image_blocks.append(f"{image_label}:{block_name}")

    add_check(
        "image block inventory coverage",
        "PASS" if not image_block_rules or not missing_image_blocks else "WARN",
        "missing_blocks=" + ("none" if not missing_image_blocks else ", ".join(missing_image_blocks)),
    )

    generic_image_summary = sum(
        1
        for r in rows
        if "system-context hardware block diagram with sub-blocks and io connections" in (r.get("requirement_statement") or "").lower()
    )
    add_check(
        "atomic image candidates only",
        "PASS" if generic_image_summary == 0 else "WARN",
        f"generic_image_summary_rows={generic_image_summary}",
    )

    functional_desc_rows = sum(1 for n in notes_lower if "functional description sentence using ontology rule" in n)
    add_check(
        "functional description all-sentence rule",
        "PASS" if functional_desc_rows >= 1 else "WARN",
        f"functional_description_rows={functional_desc_rows}",
    )

    categories = {((r.get("category") or "").strip()) for r in rows}
    missing_categories = {"System", "Analog", "Digital"} - categories
    add_check(
        "category coverage",
        "PASS" if not missing_categories else "WARN",
        f"categories={sorted(categories)}, missing={sorted(missing_categories)}",
    )

    return checks, warn_count, fail_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Fix split requirement statements and cross-check with RAG")
    parser.add_argument("--summary-csv", default="artifacts/stage1_requirements/requirements_summary.csv")
    parser.add_argument("--index-csv", default="artifacts/stage1_requirements/ocr_extracts/index.csv")
    parser.add_argument("--rag-db", default=None)
    parser.add_argument("--summary-md", default="artifacts/stage1_requirements/requirements_summary.md")
    parser.add_argument("--raw-md", default="artifacts/stage1_requirements/requirements_raw.md")
    parser.add_argument("--stage-report", default="artifacts/orchestrator/stage_01_report.md")
    parser.add_argument("--crosscheck-report", default="artifacts/stage1_requirements/requirements_rag_crosscheck.md")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")
    _init_requirement_id_rules(repo_root)
    project_context = _load_project_context(repo_root)

    rag_db_value = args.rag_db or project_context.get("rag_db_path") or "artifacts/rag/rag_index.sqlite"

    summary_csv = (repo_root / args.summary_csv).resolve()
    index_csv = (repo_root / args.index_csv).resolve()
    rag_db = (repo_root / str(rag_db_value)).resolve()
    summary_md = (repo_root / args.summary_md).resolve()
    raw_md = (repo_root / args.raw_md).resolve()
    stage_report = (repo_root / args.stage_report).resolve()
    crosscheck_report = (repo_root / args.crosscheck_report).resolve()

    if not summary_csv.exists():
        print(f"Crosscheck: FAIL (missing summary csv: {summary_csv})")
        _append_log(repo_root, script_name, f"FAIL missing_summary={summary_csv.as_posix()}")
        return 1
    if not index_csv.exists():
        print(f"Crosscheck: FAIL (missing index csv: {index_csv})")
        _append_log(repo_root, script_name, f"FAIL missing_index={index_csv.as_posix()}")
        return 1
    if not rag_db.exists():
        print(f"Crosscheck: FAIL (missing rag db: {rag_db})")
        _append_log(repo_root, script_name, f"FAIL missing_rag_db={rag_db.as_posix()}")
        return 1

    page_to_file, source_spec = _load_index(index_csv)

    html_req_map: Dict[str, str] = {}
    html_page_lines: Dict[int, List[str]] = {}
    if source_spec:
        source_spec_path = Path(source_spec)
        if source_spec_path.suffix.lower() in {".html", ".htm"} and source_spec_path.exists():
            html_req_map = _extract_html_reqid_definitions(source_spec_path)
            html_page_lines = _extract_html_page_lines(source_spec_path)

    with summary_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        summary_fieldnames = list(reader.fieldnames or [])

    conn = sqlite3.connect(str(rag_db))

    changed = 0
    ok = 0
    warn = 0
    fail = 0
    details: List[str] = []

    try:
        for row in rows:
            old = _clean(row.get("requirement_statement", ""))
            req_id = row.get("id", "")
            notes = row.get("notes", "")
            source_req_id = _extract_source_req_id_from_row(row)
            has_explicit_source_req = bool(source_req_id)
            preserve_complete_ontology_sentence = "functional sentence using ontology rule" in notes.lower() and old.endswith(".")

            # Preserve explicit req-id definitions normalized by the generator from source HTML.
            repaired = old if (has_explicit_source_req or preserve_complete_ontology_sentence) else _maybe_rebuild_statement(old, row.get("source", ""), req_id, page_to_file)
            html_overridden = False
            if source_req_id and source_req_id in html_req_map:
                html_stmt = html_req_map[source_req_id]
                if _prefer_html_statement(repaired, html_stmt):
                    repaired = _clean(html_stmt)
                    html_overridden = True
            elif html_page_lines:
                html_stmt = _find_best_html_page_statement(repaired, row.get("source", ""), html_page_lines)
                if html_stmt and _prefer_html_statement(repaired, html_stmt):
                    repaired = _clean(html_stmt)
                    html_overridden = True

            status, reason = _rag_check(conn, repaired, row.get("source", ""))

            derivation_kind = (row.get("derivation_kind") or "").strip().lower()
            if derivation_kind in {"reset_table_connection", "clock_table_connection_frequency", "interrupt_table_connection"}:
                status = "warn"
                reason = "structural_table_derivation"

            if _contains_new_definition_token(repaired, req_id):
                status = "fail"
                reason = "contains_next_req_token"

            if status == "fail":
                # Keep original when repaired does not validate but original does.
                old_status, old_reason = _rag_check(conn, old, row.get("source", ""))
                if (not html_overridden) and old_status in {"ok", "warn"} and not _contains_new_definition_token(old, req_id):
                    old_norm = _norm(old)
                    repaired_norm = _norm(repaired)
                    # Prefer repaired text if it is a clear extension of the original statement.
                    if old_norm and repaired_norm and old_norm in repaired_norm and len(repaired_norm) >= int(len(old_norm) * 1.2):
                        status, reason = "warn", f"kept_repaired_longer:old_{old_status}:{old_reason}"
                    else:
                        repaired = old
                        status, reason = old_status, f"kept_original:{old_reason}"

            if _norm(repaired) != _norm(old):
                changed += 1

            row["requirement_statement"] = repaired
            note = _strip_existing_rag_note(row.get("notes", ""))
            if html_overridden:
                note = (note + " | html_quality_override=true").strip(" |")
            row["notes"] = (note + f" | rag_crosscheck={status}:{reason}").strip(" |")

            if status == "ok":
                ok += 1
            elif status == "warn":
                warn += 1
            else:
                fail += 1

            if status != "ok" or _norm(repaired) != _norm(old):
                details.append(
                    f"- {row.get('id','')}: status={status} reason={reason} changed={_norm(repaired) != _norm(old)}"
                )
    finally:
        conn.close()

    with summary_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=summary_fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)

    _update_summary_md(summary_csv, summary_md)
    _update_raw_md(summary_csv, raw_md)
    _append_report(stage_report, len(rows), changed, ok, warn, fail)

    crosscheck_report.parent.mkdir(parents=True, exist_ok=True)
    rule_checks, rule_warn, rule_fail = _evaluate_rule_checks(rows, repo_root)

    report_lines = [
        "# Requirements RAG Cross-Check",
        "",
        f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Checked requirements: {len(rows)}",
        f"- Corrected statements: {changed}",
        f"- RAG exact: {ok}",
        f"- RAG warn: {warn}",
        f"- RAG fail: {fail}",
        f"- Rule-check warn: {rule_warn}",
        f"- Rule-check fail: {rule_fail}",
        "",
        "## Ontology and Extraction Rule Checks",
    ]
    report_lines.extend(rule_checks)
    report_lines.extend([
        "",
        "## Details",
    ])
    if details:
        report_lines.extend(details)
    else:
        report_lines.append("- No anomalies detected.")

    crosscheck_report.write_text("\n".join(report_lines).rstrip() + "\n", encoding="utf-8")

    if rule_fail > 0:
        print("Crosscheck: FAIL")
        print(f"- Checked requirements: {len(rows)}")
        print(f"- Corrected statements: {changed}")
        print(f"- RAG exact/warn/fail: {ok}/{warn}/{fail}")
        print(f"- Rule-check warn/fail: {rule_warn}/{rule_fail}")
        print(f"- Updated CSV: {summary_csv}")
        print(f"- Crosscheck report: {crosscheck_report}")
        _append_log(
            repo_root,
            script_name,
            f"FAIL total={len(rows)} changed={changed} ok={ok} warn={warn} fail={fail} rule_warn={rule_warn} rule_fail={rule_fail}",
        )
        return 1

    print("Crosscheck: PASS")
    print(f"- Checked requirements: {len(rows)}")
    print(f"- Corrected statements: {changed}")
    print(f"- RAG exact/warn/fail: {ok}/{warn}/{fail}")
    print(f"- Rule-check warn/fail: {rule_warn}/{rule_fail}")
    print(f"- Updated CSV: {summary_csv}")
    print(f"- Crosscheck report: {crosscheck_report}")

    _append_log(
        repo_root,
        script_name,
        f"PASS total={len(rows)} changed={changed} ok={ok} warn={warn} fail={fail} rule_warn={rule_warn} rule_fail={rule_fail}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
