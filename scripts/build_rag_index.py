#!/usr/bin/env python3
"""Build a lightweight RAG retrieval index from OCR extracts.

The index is stored in SQLite with an FTS5 table for fast lexical retrieval.
"""

from __future__ import annotations

import argparse
import csv
import html as html_lib
import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from repo_paths import portable_repo_path, resolve_repo_path
from typing import Dict, Iterable, List, Set

try:
    from approved_vocabulary import approved_stopwords, load_approved_vocabulary
except ModuleNotFoundError:
    from scripts.approved_vocabulary import approved_stopwords, load_approved_vocabulary


@dataclass
class PageRecord:
    source_file: str
    page: int
    text_file: Path


@dataclass
class ChunkRecord:
    start_char: int
    end_char: int
    text: str
    section: str
    source_type: str


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\\n")


def _load_project_context(repo_root: Path) -> dict:
    config_path = repo_root / "config/project_context.json"
    if not config_path.exists():
        return {}
    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _load_domain_vocabulary(repo_root: Path, project_context: dict) -> dict:
    return load_approved_vocabulary(repo_root, project_context)


def _tokenize_terms(text: str) -> List[str]:
    normalized = re.sub(r"(?<=[A-Za-z])[-/](?=[A-Za-z])", " ", text or "")
    normalized = re.sub(r"[^A-Za-z0-9_]+", " ", normalized)
    return [token.lower() for token in normalized.split() if token.strip()]


def _simple_lemma(token: str, protected_terms: Set[str]) -> str:
    if token.upper() in protected_terms:
        return token.lower()
    if len(token) <= 3 or re.search(r"\d", token):
        return token
    irregular = {
        "driven": "drive",
        "driving": "drive",
        "configured": "configure",
        "configuring": "configure",
        "configuration": "configure",
        "connections": "connection",
        "connected": "connect",
        "connecting": "connect",
        "samples": "sample",
        "sampled": "sample",
        "sampling": "sample",
        "requirements": "requirement",
        "specifications": "specification",
    }
    if token in irregular:
        return irregular[token]
    if token.endswith("ies") and len(token) > 4:
        return token[:-3] + "y"
    if token.endswith("ing") and len(token) > 5:
        root = token[:-3]
        if len(root) > 2 and root[-1] == root[-2]:
            root = root[:-1]
        return root
    if token.endswith("ed") and len(token) > 4:
        root = token[:-2]
        if len(root) > 2 and root[-1] == root[-2]:
            root = root[:-1]
        return root
    if token.endswith("s") and not token.endswith("ss") and len(token) > 4:
        return token[:-1]
    return token


def _controlled_terms(text: str, domain_vocabulary: dict) -> str:
    stopwords = approved_stopwords(domain_vocabulary)
    protected_terms = {str(term).upper() for term in domain_vocabulary.get("protected_terms", []) if str(term).strip()}
    terms: List[str] = []
    seen: Set[str] = set()

    def add(term: str) -> None:
        clean = re.sub(r"[^a-z0-9_]+", "_", term.lower()).strip("_")
        if clean and clean not in stopwords and clean not in seen:
            seen.add(clean)
            terms.append(clean)

    raw_text = text or ""
    lower_text = raw_text.lower()

    for token in _tokenize_terms(raw_text):
        lemma = _simple_lemma(token, protected_terms)
        add(token)
        add(lemma)

    acronyms = domain_vocabulary.get("acronyms", {})
    if isinstance(acronyms, dict):
        for acronym, expansion in acronyms.items():
            if re.search(rf"\b{re.escape(str(acronym))}\b", raw_text, flags=re.IGNORECASE):
                add(str(acronym))
                for token in _tokenize_terms(str(expansion)):
                    add(_simple_lemma(token, protected_terms))

    for canonical, variants in (domain_vocabulary.get("synonym_groups", {}) or {}).items():
        if not isinstance(variants, list):
            continue
        variant_match = any(re.search(rf"\b{re.escape(str(variant).lower())}\b", lower_text) for variant in variants)
        if variant_match:
            add(str(canonical))
            for variant in variants:
                for token in _tokenize_terms(str(variant)):
                    add(_simple_lemma(token, protected_terms))

    for canonical, variants in (domain_vocabulary.get("phrase_mappings", {}) or {}).items():
        phrase_values = [str(canonical), *[str(variant) for variant in variants if isinstance(variant, str)]] if isinstance(variants, list) else [str(canonical)]
        if any(str(phrase).lower() in lower_text for phrase in phrase_values):
            add(str(canonical))
            for token in _tokenize_terms(str(canonical)):
                add(_simple_lemma(token, protected_terms))

    for unit in domain_vocabulary.get("units", []) or []:
        if re.search(rf"(?<![A-Za-z0-9_]){re.escape(str(unit))}(?![A-Za-z0-9_])", raw_text):
            add(str(unit))

    return " ".join(terms)


def _load_index(index_csv: Path, repo_root: Path) -> List[PageRecord]:
    if not index_csv.exists():
        raise FileNotFoundError(f"Index CSV not found: {index_csv}")

    records: List[PageRecord] = []
    with index_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"source_file", "page", "text_file", "status"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"Index CSV missing required columns: {required}")

        for row in reader:
            if (row.get("status") or "").strip() != "text-extracted":
                continue
            text_file = resolve_repo_path(repo_root, row["text_file"])
            if not text_file.exists():
                continue
            records.append(
                PageRecord(
                    source_file=portable_repo_path(repo_root, row["source_file"]),
                    page=int(row["page"]),
                    text_file=text_file,
                )
            )
    return records


def _normalize_text(text: str) -> str:
    return "\\n".join(line.rstrip() for line in text.replace("\\r\\n", "\\n").split("\\n")).strip()


def _extract_text_from_html_fragment(fragment: str) -> str:
    no_script = re.sub(r"<script\\b[^>]*>.*?</script>", " ", fragment, flags=re.IGNORECASE | re.DOTALL)
    no_style = re.sub(r"<style\\b[^>]*>.*?</style>", " ", no_script, flags=re.IGNORECASE | re.DOTALL)
    with_breaks = re.sub(r"</(p|div|section|br|li|tr|h[1-6])>", "\\n", no_style, flags=re.IGNORECASE)
    no_tags = re.sub(r"<[^>]+>", " ", with_breaks)
    unescaped = html_lib.unescape(no_tags)
    compact = re.sub(r"[\\t\\r ]+", " ", unescaped)
    compact = re.sub(r"\\n\\s*\\n+", "\\n", compact)
    return compact.strip()


def _is_html_noise_line(line: str) -> bool:
    l = line.strip().lower()
    if not l:
        return True
    if l.startswith(("title:", "number:", "rev:", "size:", "scale:")):
        return True
    if "customer, inc" in l:
        return True
    if re.match(r"^page\\s*\\d+\\s*of\\s*\\d+", l):
        return True
    if re.match(r"^page\\s*\\d+", l):
        return True
    if re.match(r"^\\(?[ivx]+\\)?$", l):
        return True
    if re.match(r"^\\d+\\s*/\\s*\\d+$", l):
        return True
    if len(l) <= 2 and not re.search(r"\\b(odr|i2c|spi)\\b", l):
        return True
    if sum(ch.isalpha() for ch in l) < 3 and not re.search(r"\\d", l):
        return True
    return False


def _extract_clean_html_pages(source_html: Path) -> dict[int, str]:
    html_text = source_html.read_text(encoding="utf-8", errors="ignore")
    sections = re.findall(r"(?is)<section\\b[^>]*class=[\"']page[\"'][^>]*>(.*?)</section>", html_text)
    if not sections:
        sections = [html_text]

    page_map: dict[int, str] = {}
    for idx, section in enumerate(sections, start=1):
        m_page = re.search(r"(?is)<div\\b[^>]*class=[\"']page-title[\"'][^>]*>\\s*Page\\s*(\\d+)\\s*</div>", section)
        page_no = int(m_page.group(1)) if m_page else idx

        p_fragments = re.findall(r"(?is)<p\\b[^>]*>(.*?)</p>", section)
        lines: List[str] = []
        for frag in p_fragments:
            text = _extract_text_from_html_fragment(frag)
            if _is_html_noise_line(text):
                continue
            lines.append(text)

        if lines:
            page_map[page_no] = "\\n".join(lines)

    return page_map


def _chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> Iterable[tuple[int, int, str]]:
    if not text:
        return

    clean = _normalize_text(text)
    if not clean:
        return

    start = 0
    text_len = len(clean)
    while start < text_len:
        target_end = min(start + chunk_size, text_len)
        end = clean.rfind("\\n", start, target_end)
        if end == -1 or end <= start + chunk_size // 3:
            end = target_end

        chunk = clean[start:end].strip()
        if chunk:
            yield start, end, chunk

        if end >= text_len:
            break
        start = max(0, end - chunk_overlap)


def _line_spans(text: str) -> List[tuple[int, int, str]]:
    spans: List[tuple[int, int, str]] = []
    start = 0
    for raw_line in text.replace("\r\n", "\n").splitlines(keepends=True):
        end = start + len(raw_line)
        spans.append((start, end, raw_line.rstrip("\r\n")))
        start = end
    if text and not text.endswith(("\n", "\r")) and not spans:
        spans.append((0, len(text), text))
    return spans


def _is_table_caption(line: str) -> bool:
    return bool(re.match(r"^\s*Table\s+\d+\b\s*[:.\-]?\s*\S*", line, flags=re.IGNORECASE))


def _is_figure_caption(line: str) -> bool:
    return bool(re.match(r"^\s*Figure\s+\d+\b\s*[:.\-]?\s*\S*", line, flags=re.IGNORECASE))


def _is_section_heading(line: str) -> bool:
    stripped = line.strip()
    if not stripped or _is_table_caption(stripped) or _is_figure_caption(stripped):
        return False
    return bool(re.match(r"^\d+(?:\.\d+)*\.?\s+[A-Z][A-Za-z0-9][A-Za-z0-9 /_(),+\-:]{2,}$", stripped))


def _section_title(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip()).strip(" .")


def _chunk_line_range(
    spans: List[tuple[int, int, str]],
    start_line: int,
    end_line: int,
    section: str,
    source_type: str,
) -> ChunkRecord | None:
    if start_line >= end_line:
        return None
    start_char = spans[start_line][0]
    end_char = spans[end_line - 1][1]
    text = "\n".join(line for _start, _end, line in spans[start_line:end_line]).strip()
    if not text:
        return None
    return ChunkRecord(start_char, end_char, text, section, source_type)


def _emit_text_chunks(
    spans: List[tuple[int, int, str]],
    start_line: int,
    end_line: int,
    section: str,
    chunk_size: int,
    chunk_overlap: int,
) -> Iterable[ChunkRecord]:
    if start_line >= end_line:
        return
    start_char = spans[start_line][0]
    text = "\n".join(line for _start, _end, line in spans[start_line:end_line]).strip()
    for rel_start, rel_end, chunk in _chunk_text(text, chunk_size, chunk_overlap):
        yield ChunkRecord(start_char + rel_start, start_char + rel_end, chunk, section, "text")


def _chunk_page_text(text: str, chunk_size: int, chunk_overlap: int) -> Iterable[ChunkRecord]:
    clean = _normalize_text(text)
    if not clean:
        return

    spans = _line_spans(clean)
    if not spans:
        return

    current_section = ""
    text_start = 0
    text_section = ""
    index = 0
    while index < len(spans):
        line = spans[index][2]
        if _is_section_heading(line):
            current_section = _section_title(line)

        if _is_table_caption(line) or _is_figure_caption(line):
            for chunk in _emit_text_chunks(spans, text_start, index, text_section, chunk_size, chunk_overlap):
                yield chunk

            source_type = "table" if _is_table_caption(line) else "figure"
            start_line = index
            if source_type == "figure":
                nearby_start = max(text_start, index - 3)
                while nearby_start < index and not spans[nearby_start][2].strip():
                    nearby_start += 1
                start_line = nearby_start

            end_line = index + 1
            while end_line < len(spans):
                next_line = spans[end_line][2]
                if _is_table_caption(next_line) or _is_figure_caption(next_line):
                    break
                if _is_section_heading(next_line):
                    break
                end_line += 1

            chunk = _chunk_line_range(spans, start_line, end_line, current_section, source_type)
            if chunk is not None:
                yield chunk
            text_start = end_line
            text_section = current_section
            index = end_line
            continue

        if index == text_start:
            text_section = current_section
        index += 1

    for chunk in _emit_text_chunks(spans, text_start, len(spans), text_section, chunk_size, chunk_overlap):
        yield chunk


def _prepare_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")

    conn.executescript(
        """
        DROP TABLE IF EXISTS chunks;
        DROP TABLE IF EXISTS chunk_fts;
        DROP TABLE IF EXISTS chunk_terms_fts;

        CREATE TABLE chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT NOT NULL,
            page INTEGER NOT NULL,
            section TEXT NOT NULL,
            source_type TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            start_char INTEGER NOT NULL,
            end_char INTEGER NOT NULL,
            chunk_text TEXT NOT NULL,
            normalized_terms TEXT NOT NULL,
            text_file TEXT NOT NULL
        );

        CREATE VIRTUAL TABLE chunk_fts USING fts5(
            chunk_id UNINDEXED,
            source_file,
            page,
            section,
            source_type,
            chunk_text
        );

        CREATE VIRTUAL TABLE chunk_terms_fts USING fts5(
            chunk_id UNINDEXED,
            source_file,
            page,
            section,
            source_type,
            normalized_terms
        );
        """
    )
    return conn


def main() -> int:
    parser = argparse.ArgumentParser(description="Build SQLite FTS index for specification RAG")
    parser.add_argument(
        "--source-index",
        default=None,
        help="OCR index CSV produced by extract_requirements_ocr.py",
    )
    parser.add_argument("--db-path", default=None, help="Output SQLite index path")
    parser.add_argument("--manifest", default=None, help="Output build manifest")
    parser.add_argument("--chunk-size", type=int, default=1200, help="Chunk size in characters")
    parser.add_argument("--chunk-overlap", type=int, default=150, help="Overlap in characters")
    args = parser.parse_args()

    if args.chunk_size <= 0:
        raise ValueError("chunk-size must be > 0")
    if args.chunk_overlap < 0 or args.chunk_overlap >= args.chunk_size:
        raise ValueError("chunk-overlap must be >= 0 and < chunk-size")

    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")
    project_context = _load_project_context(repo_root)
    domain_vocabulary = _load_domain_vocabulary(repo_root, project_context)

    source_index_value = (
        args.source_index
        or project_context.get("ocr_index_path")
        or "artifacts/stage1_requirements/ocr_extracts/index.csv"
    )
    db_path_value = args.db_path or project_context.get("rag_db_path") or "artifacts/rag/rag_index.sqlite"
    manifest_value = args.manifest or project_context.get("rag_manifest_path") or "artifacts/rag/index_manifest.json"

    source_index = Path(str(source_index_value))
    if not source_index.is_absolute():
        source_index = (repo_root / source_index).resolve()

    db_path = Path(str(db_path_value))
    if not db_path.is_absolute():
        db_path = (repo_root / db_path).resolve()

    manifest_path = Path(str(manifest_value))
    if not manifest_path.is_absolute():
        manifest_path = (repo_root / manifest_path).resolve()

    try:
        records = _load_index(source_index, repo_root)
    except Exception as exc:
        print(f"RAG build: FAIL ({exc})")
        _append_log(repo_root, script_name, f"FAIL {exc}")
        return 1

    if not records:
        print("RAG build: FAIL (no text-extracted pages found in source index)")
        _append_log(repo_root, script_name, "FAIL no_text_extracted_pages")
        return 1

    conn = _prepare_db(db_path)
    chunk_count = 0
    source_type_counts: Dict[str, int] = {}
    html_page_cache: dict[str, dict[int, str]] = {}

    try:
        with conn:
            for rec in records:
                text = ""
                source_path = resolve_repo_path(repo_root, rec.source_file)

                if source_path.suffix.lower() in {".html", ".htm"} and source_path.exists():
                    cache_key = source_path.as_posix()
                    if cache_key not in html_page_cache:
                        html_page_cache[cache_key] = _extract_clean_html_pages(source_path)
                    text = html_page_cache[cache_key].get(rec.page, "")

                if not text:
                    text = rec.text_file.read_text(encoding="utf-8", errors="ignore")

                for idx, chunk in enumerate(
                    _chunk_page_text(text, args.chunk_size, args.chunk_overlap),
                    start=1,
                ):
                    normalized_terms = _controlled_terms(chunk.text, domain_vocabulary)
                    cur = conn.execute(
                        """
                        INSERT INTO chunks (source_file, page, section, source_type, chunk_index, start_char, end_char, chunk_text, normalized_terms, text_file)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            rec.source_file,
                            rec.page,
                            chunk.section,
                            chunk.source_type,
                            idx,
                            chunk.start_char,
                            chunk.end_char,
                            chunk.text,
                            normalized_terms,
                            portable_repo_path(repo_root, rec.text_file),
                        ),
                    )
                    chunk_id = cur.lastrowid
                    conn.execute(
                        "INSERT INTO chunk_fts (chunk_id, source_file, page, section, source_type, chunk_text) VALUES (?, ?, ?, ?, ?, ?)",
                        (chunk_id, rec.source_file, str(rec.page), chunk.section, chunk.source_type, chunk.text),
                    )
                    conn.execute(
                        "INSERT INTO chunk_terms_fts (chunk_id, source_file, page, section, source_type, normalized_terms) VALUES (?, ?, ?, ?, ?, ?)",
                        (chunk_id, rec.source_file, str(rec.page), chunk.section, chunk.source_type, normalized_terms),
                    )
                    source_type_counts[chunk.source_type] = source_type_counts.get(chunk.source_type, 0) + 1
                    chunk_count += 1
    finally:
        conn.close()

    sources = sorted({rec.source_file for rec in records})
    manifest = {
        "built_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_index": portable_repo_path(repo_root, source_index),
        "db_path": portable_repo_path(repo_root, db_path),
        "chunk_size": args.chunk_size,
        "chunk_overlap": args.chunk_overlap,
        "pages_indexed": len(records),
        "chunks_indexed": chunk_count,
        "chunk_source_types": source_type_counts,
        "term_normalization": {
            "enabled": True,
            "method": "rule_based_lemma_plus_controlled_domain_vocabulary",
            "domain_vocabulary_path": str(project_context.get("domain_vocabulary_path") or "config/domain_vocabulary.json"),
            "normalized_terms_index": True,
            "normalized_terms_table": "chunk_terms_fts"
        },
        "source_files": sources,
        "html_clean_mode": True,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"RAG build: PASS")
    print(f"- Source index: {source_index}")
    print(f"- Pages indexed: {len(records)}")
    print(f"- Chunks indexed: {chunk_count}")
    print(f"- DB: {db_path}")
    print(f"- Manifest: {manifest_path}")
    _append_log(
        repo_root,
        script_name,
        f"PASS pages={len(records)} chunks={chunk_count} db={db_path.as_posix()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
