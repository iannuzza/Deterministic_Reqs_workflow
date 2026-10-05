#!/usr/bin/env python3
"""Query the local SQLite RAG index and export top-k evidence chunks."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from retrieval.embeddings import LocalHashEmbeddingModel, LocalSentenceTransformerEmbedding
from retrieval.fusion import fuse_lexical_normalized_semantic
from retrieval.semantic_index import ExactCosineIndex, SemanticIndexUnavailable, semantic_search
try:
    from approved_vocabulary import approved_stopwords, load_approved_vocabulary
except ModuleNotFoundError:
    from scripts.approved_vocabulary import approved_stopwords, load_approved_vocabulary


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


def _chunk_columns(conn: sqlite3.Connection) -> set[str]:
    return {str(row[1]) for row in conn.execute("PRAGMA table_info(chunks)").fetchall()}


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table', 'view') AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def _tokenize_terms(text: str) -> list[str]:
    normalized = re.sub(r"(?<=[A-Za-z])[-/](?=[A-Za-z])", " ", text or "")
    normalized = re.sub(r"[^A-Za-z0-9_]+", " ", normalized)
    return [token.lower() for token in normalized.split() if token.strip()]


def _simple_lemma(token: str, protected_terms: set[str]) -> str:
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
    terms: list[str] = []
    seen: set[str] = set()

    def add(term: str) -> None:
        clean = re.sub(r"[^a-z0-9_]+", "_", term.lower()).strip("_")
        if clean and clean not in stopwords and clean not in seen:
            seen.add(clean)
            terms.append(clean)

    raw_text = text or ""
    lower_text = raw_text.lower()
    for token in _tokenize_terms(raw_text):
        add(token)
        add(_simple_lemma(token, protected_terms))

    acronyms = domain_vocabulary.get("acronyms", {})
    if isinstance(acronyms, dict):
        for acronym, expansion in acronyms.items():
            if re.search(rf"\b{re.escape(str(acronym))}\b", raw_text, flags=re.IGNORECASE):
                add(str(acronym))
                for token in _tokenize_terms(str(expansion)):
                    add(_simple_lemma(token, protected_terms))

    for canonical, variants in (domain_vocabulary.get("synonym_groups", {}) or {}).items():
        if isinstance(variants, list) and any(re.search(rf"\b{re.escape(str(variant).lower())}\b", lower_text) for variant in variants):
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


def _fts_or_query(terms_text: str) -> str:
    terms: list[str] = []
    seen: set[str] = set()
    for term in _tokenize_terms(terms_text):
        safe = re.sub(r"[^a-z0-9_]+", "", term.lower())
        if safe and safe not in seen:
            seen.add(safe)
            terms.append(safe)
    return " OR ".join(terms)


def _metadata_selects(columns: set[str]) -> tuple[str, str, str]:
    section_expr = "c.section" if "section" in columns else "''"
    source_type_expr = "c.source_type" if "source_type" in columns else "'text'"
    normalized_terms_expr = "c.normalized_terms" if "normalized_terms" in columns else "''"
    return section_expr, source_type_expr, normalized_terms_expr


def _load_semantic_resources(repo_root: Path, args: argparse.Namespace, project_context: dict):
    config_path = repo_root / "config/retrieval_config.json"
    config_root = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    config = config_root.get("semantic_retrieval", {})
    index_value = args.semantic_index or config.get("index_path")
    if not index_value:
        raise SemanticIndexUnavailable("semantic index path is not configured")
    index_path = Path(str(index_value))
    if not index_path.is_absolute():
        index_path = repo_root / index_path
    index = ExactCosineIndex.load(index_path)
    model_type = config.get("model_type", "local_sentence_transformer")
    if model_type == "local_hash":
        model = LocalHashEmbeddingModel(int(config.get("dimension", 256)))
    else:
        model_value = args.model_path or config.get("model_path")
        if not model_value:
            raise SemanticIndexUnavailable("local embedding model path is not configured")
        model_path = Path(str(model_value))
        if not model_path.is_absolute():
            model_path = repo_root / model_path
        model = LocalSentenceTransformerEmbedding(model_path, device=str(config.get("device", "cpu")))
    return index, model


def _semantic_chunk_rows(conn: sqlite3.Connection, candidates: list[dict], columns: set[str]) -> list[dict]:
    """Adapt semantic chunk entities to the legacy evidence-row shape."""
    result: list[dict] = []
    for candidate in candidates:
        chunk_id = candidate.get("metadata", {}).get("chunk_id")
        if chunk_id is None:
            continue
        row = conn.execute("SELECT * FROM chunks WHERE id = ?", (chunk_id,)).fetchone()
        if row is None:
            continue
        values = dict(zip((item[1] for item in conn.execute("PRAGMA table_info(chunks)").fetchall()), row))
        result.append({
            "chunk_id": values.get("id"),
            "source_file": values.get("source_file", ""),
            "page": values.get("page", ""),
            "section": values.get("section", ""),
            "source_type": values.get("source_type", "text"),
            "normalized_terms": values.get("normalized_terms", ""),
            "chunk_index": values.get("chunk_index", ""),
            "chunk_text": values.get("chunk_text", ""),
            "semantic_score": candidate["semantic_score"],
        })
    return result


def _protected_exact_ids(query: str, rows: list[dict]) -> set[int]:
    """Protect exact technical identifiers already found by lexical retrieval."""
    identifiers = re.findall(r"\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+\b", query or "")
    if not identifiers:
        return set()
    lowered = [identifier.casefold() for identifier in identifiers]
    return {
        int(row["chunk_id"])
        for row in rows
        if row.get("chunk_id") is not None
        and all(identifier in (row.get("chunk_text") or "").casefold() for identifier in lowered)
    }


def _query_requirement_ids(query: str) -> list[str]:
    return sorted(set(re.findall(r"\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)*_\d+\b", query or "")))


def _requirement_id_mapping_check(repo_root: Path, query: str, rows: list[dict]) -> dict[str, object]:
    """Audit queried requirement IDs against Stage 1 ownership and returned evidence."""
    query_ids = _query_requirement_ids(query)
    result: dict[str, object] = {"query_ids": query_ids, "status": "not_applicable"}
    if not query_ids:
        return result
    catalog_path = repo_root / "artifacts/stage1_requirements/requirements_summary.csv"
    catalog: dict[str, dict[str, str]] = {}
    if catalog_path.exists():
        with catalog_path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                req_id = (row.get("source_req_id") or row.get("Requirement ID") or row.get("id") or "").strip()
                if req_id:
                    catalog[req_id.casefold()] = row
    checks = []
    for req_id in query_ids:
        source_row = catalog.get(req_id.casefold(), {})
        owner = (source_row.get("source_section_owner") or source_row.get("Block") or "System level").strip()
        evidence_ids = [
            row.get("chunk_id")
            for row in rows
            if req_id.casefold() in (row.get("chunk_text") or "").casefold()
        ]
        checks.append({
            "source_req_id": req_id,
            "known_in_stage1": bool(source_row),
            "expected_owner": owner or "System level",
            "evidence_chunk_ids": evidence_ids,
            "evidence_match": bool(evidence_ids),
        })
    result["checks"] = checks
    result["status"] = "pass" if all(item["known_in_stage1"] and item["evidence_match"] for item in checks) else "review"
    return result


def _fetch_lexical(conn: sqlite3.Connection, query: str, top_k: int, columns: set[str]) -> list[dict]:
    section_expr, source_type_expr, normalized_terms_expr = _metadata_selects(columns)
    rows = conn.execute(
        f"""
        SELECT
            c.id,
            c.source_file,
            c.page,
            {section_expr} AS section,
            {source_type_expr} AS source_type,
            {normalized_terms_expr} AS normalized_terms,
            c.chunk_index,
            c.chunk_text,
            bm25(chunk_fts) AS score
        FROM chunk_fts
        JOIN chunks c ON c.id = CAST(chunk_fts.chunk_id AS INTEGER)
        WHERE chunk_fts MATCH ?
        ORDER BY score
        LIMIT ?
        """,
        (query, top_k),
    ).fetchall()
    return [
        {
            "chunk_id": row[0],
            "source_file": row[1],
            "page": row[2],
            "section": row[3],
            "source_type": row[4],
            "normalized_terms": row[5],
            "chunk_index": row[6],
            "chunk_text": row[7],
            "lexical_score": row[8],
        }
        for row in rows
    ]


def _fetch_normalized(conn: sqlite3.Connection, query_terms: str, top_k: int, columns: set[str]) -> list[dict]:
    if not query_terms or not _table_exists(conn, "chunk_terms_fts"):
        return []
    section_expr, source_type_expr, normalized_terms_expr = _metadata_selects(columns)
    rows = conn.execute(
        f"""
        SELECT
            c.id,
            c.source_file,
            c.page,
            {section_expr} AS section,
            {source_type_expr} AS source_type,
            {normalized_terms_expr} AS normalized_terms,
            c.chunk_index,
            c.chunk_text,
            bm25(chunk_terms_fts) AS score
        FROM chunk_terms_fts
        JOIN chunks c ON c.id = CAST(chunk_terms_fts.chunk_id AS INTEGER)
        WHERE chunk_terms_fts MATCH ?
        ORDER BY score
        LIMIT ?
        """,
        (query_terms, top_k),
    ).fetchall()
    return [
        {
            "chunk_id": row[0],
            "source_file": row[1],
            "page": row[2],
            "section": row[3],
            "source_type": row[4],
            "normalized_terms": row[5],
            "chunk_index": row[6],
            "chunk_text": row[7],
            "normalized_score": row[8],
        }
        for row in rows
    ]


def _rrf_fuse(lexical_rows: list[dict], normalized_rows: list[dict], final_top_k: int, rrf_k: int) -> list[dict]:
    fused: dict[int, dict] = {}
    for rank, row in enumerate(lexical_rows, start=1):
        item = fused.setdefault(row["chunk_id"], dict(row))
        item.update(row)
        item["rank_lexical"] = rank
        item["rrf_score"] = item.get("rrf_score", 0.0) + 1.0 / (rrf_k + rank)
    for rank, row in enumerate(normalized_rows, start=1):
        item = fused.setdefault(row["chunk_id"], dict(row))
        item.update(row)
        item["rank_normalized"] = rank
        item["rrf_score"] = item.get("rrf_score", 0.0) + 1.0 / (rrf_k + rank)
    return sorted(fused.values(), key=lambda row: (-row.get("rrf_score", 0.0), row.get("chunk_id", 0)))[:final_top_k]


def main() -> int:
    parser = argparse.ArgumentParser(description="Query SQLite FTS RAG index")
    parser.add_argument("--query", required=True, help="FTS query string")
    parser.add_argument("--top-k", type=int, default=8, help="How many chunks to return")
    parser.add_argument(
        "--mode",
        choices=("auto", "lexical", "normalized", "hybrid", "semantic", "hybrid-semantic"),
        default="auto",
        help="Retrieval mode: auto-selected, lexical, normalized, legacy hybrid RRF, semantic, or optional semantic hybrid.",
    )
    parser.add_argument("--lexical-top-k", type=int, default=30, help="Candidate count for lexical retrieval in hybrid mode.")
    parser.add_argument("--normalized-top-k", type=int, default=30, help="Candidate count for normalized retrieval in hybrid mode.")
    parser.add_argument("--semantic-top-k", type=int, default=30, help="Candidate count for semantic retrieval in semantic modes.")
    parser.add_argument("--semantic-index", default=None, help="Path to the optional local semantic index.")
    parser.add_argument("--model-path", default=None, help="Path to the local embedding model.")
    parser.add_argument("--explain", action="store_true", help="Include per-channel ranks and scores in the output.")
    parser.add_argument(
        "--no-semantic-fallback",
        action="store_true",
        help="Disable automatic semantic recovery when a legacy query returns no rows.",
    )
    parser.add_argument("--rrf-k", type=int, default=60, help="RRF stabilizing constant for hybrid retrieval.")
    parser.add_argument("--db-path", default=None, help="RAG SQLite database path")
    parser.add_argument(
        "--output",
        default=None,
        help="Markdown output file with retrieved chunks",
    )
    args = parser.parse_args()

    if args.top_k <= 0:
        raise ValueError("top-k must be > 0")
    if args.lexical_top_k <= 0 or args.normalized_top_k <= 0 or args.semantic_top_k <= 0:
        raise ValueError("lexical-top-k, normalized-top-k, and semantic-top-k must be > 0")
    if args.rrf_k <= 0:
        raise ValueError("rrf-k must be > 0")

    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, f"START query={args.query}")
    project_context = _load_project_context(repo_root)
    domain_vocabulary = _load_domain_vocabulary(repo_root, project_context)
    retrieval_config_path = repo_root / "config/retrieval_config.json"
    retrieval_config_root = json.loads(retrieval_config_path.read_text(encoding="utf-8")) if retrieval_config_path.exists() else {}
    semantic_config = retrieval_config_root.get("semantic_retrieval", {})

    requested_mode = args.mode
    if args.mode == "auto":
        selection_value = project_context.get("retrieval_selection_path") or "config/retrieval_selection.json"
        selection_path = Path(str(selection_value))
        if not selection_path.is_absolute():
            selection_path = repo_root / selection_path
        try:
            selected_mode = json.loads(selection_path.read_text(encoding="utf-8")).get("selected_mode", "hybrid")
        except (OSError, ValueError, TypeError):
            selected_mode = "hybrid"
        args.mode = selected_mode if selected_mode in {"lexical", "normalized", "hybrid", "semantic", "hybrid-semantic"} else "hybrid"

    db_path_value = args.db_path or project_context.get("rag_db_path") or "artifacts/rag/rag_index.sqlite"
    output_value = args.output or project_context.get("rag_query_output_path") or "artifacts/rag/last_query_results.md"

    db_path = Path(str(db_path_value))
    if not db_path.is_absolute():
        db_path = (repo_root / db_path).resolve()

    output_path = Path(str(output_value))
    if not output_path.is_absolute():
        output_path = (repo_root / output_path).resolve()

    if not db_path.exists():
        print(f"RAG query: FAIL (db not found: {db_path})")
        _append_log(repo_root, script_name, f"FAIL db_not_found={db_path.as_posix()}")
        return 1

    semantic_resources = None
    semantic_error = ""
    semantic_attempted = args.mode in {"semantic", "hybrid-semantic"}
    if semantic_attempted:
        try:
            semantic_resources = _load_semantic_resources(repo_root, args, project_context)
        except (OSError, RuntimeError, ValueError, SemanticIndexUnavailable) as exc:
            semantic_error = str(exc)

    conn = sqlite3.connect(str(db_path))
    try:
        columns = _chunk_columns(conn)
        normalized_query = _controlled_terms(args.query, domain_vocabulary)
        normalized_match_query = _fts_or_query(normalized_query)
        if args.mode == "lexical":
            rows = _fetch_lexical(conn, args.query, args.top_k, columns)
            for rank, row in enumerate(rows, start=1):
                row["rank_lexical"] = rank
        elif args.mode == "normalized":
            rows = _fetch_normalized(conn, normalized_match_query, args.top_k, columns)
            for rank, row in enumerate(rows, start=1):
                row["rank_normalized"] = rank
        elif args.mode == "hybrid":
            lexical_rows = _fetch_lexical(conn, args.query, args.lexical_top_k, columns)
            normalized_rows = _fetch_normalized(conn, normalized_match_query, args.normalized_top_k, columns)
            rows = _rrf_fuse(lexical_rows, normalized_rows, args.top_k, args.rrf_k)
        else:
            semantic_rows = []
            if semantic_resources is not None:
                index, model = semantic_resources
                candidates = semantic_search(
                    query=args.query,
                    top_k=args.semantic_top_k,
                    index=index,
                    embedding_model=model,
                    entity_types={"chunk"},
                )
                semantic_rows = _semantic_chunk_rows(conn, [candidate.__dict__ for candidate in candidates], columns)
            if args.mode == "semantic":
                rows = semantic_rows[:args.top_k]
            else:
                lexical_rows = _fetch_lexical(conn, args.query, args.lexical_top_k, columns)
                normalized_rows = _fetch_normalized(conn, normalized_match_query, args.normalized_top_k, columns)
                protected_ids = _protected_exact_ids(args.query, lexical_rows + normalized_rows)
                rows = fuse_lexical_normalized_semantic(
                    lexical_rows,
                    normalized_rows,
                    semantic_rows,
                    final_top_k=args.top_k,
                    rrf_k=args.rrf_k,
                    protected_ids=protected_ids,
                )

        fallback_used = False
        if (
            not rows
            and args.mode in {"lexical", "normalized", "hybrid"}
            and not args.no_semantic_fallback
            and semantic_config.get("automatic_fallback", True)
        ):
            semantic_attempted = True
            if semantic_resources is None:
                try:
                    semantic_resources = _load_semantic_resources(repo_root, args, project_context)
                except (OSError, RuntimeError, ValueError, SemanticIndexUnavailable) as exc:
                    semantic_error = str(exc)
            if semantic_resources is not None:
                index, model = semantic_resources
                candidates = semantic_search(
                    query=args.query,
                    top_k=args.semantic_top_k,
                    index=index,
                    embedding_model=model,
                    entity_types={"chunk"},
                )
                semantic_rows = _semantic_chunk_rows(conn, [candidate.__dict__ for candidate in candidates], columns)
                if args.mode == "hybrid":
                    rows = fuse_lexical_normalized_semantic(
                        [], [], semantic_rows, final_top_k=args.top_k, rrf_k=args.rrf_k
                    )
                else:
                    rows = semantic_rows[:args.top_k]
                fallback_used = bool(rows)
                if fallback_used:
                    for row in rows:
                        row["recovery_mode"] = "hybrid-semantic" if args.mode == "hybrid" else "semantic"
    finally:
        conn.close()

    if args.mode == "semantic" and semantic_resources is None:
        print(f"RAG query: FAIL (semantic unavailable: {semantic_error})")
        _append_log(repo_root, script_name, f"FAIL semantic_unavailable={semantic_error}")
        return 1

    requirement_check = _requirement_id_mapping_check(repo_root, args.query, rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RAG Query Results",
        "",
        f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Query: {args.query}",
        f"- Mode: {args.mode}",
        f"- Requested mode: {requested_mode}",
        f"- Normalized Query: {normalized_query or '(empty)'}",
        f"- Normalized FTS Query: {normalized_match_query or '(empty)'}",
        f"- Top K: {args.top_k}",
        f"- DB: {db_path.as_posix()}",
        f"- Semantic status: {'available' if semantic_resources is not None else 'unavailable' if semantic_attempted else 'not requested'}",
        f"- Semantic diagnostic: {semantic_error}" if semantic_error else "",
        f"- Automatic semantic fallback: {'used' if fallback_used else 'not used'}",
        f"- Recovery mode: {rows[0].get('recovery_mode', '')}" if fallback_used and rows else "",
        f"- Requirement-ID mapping check: {requirement_check['status']}",
        "",
    ]
    lines = [line for line in lines if line != ""]

    if not rows:
        lines.append("No results found.")
        print("RAG query: PASS (no results)")
    else:
        for rank, row in enumerate(rows, start=1):
            lines.extend(
                [
                    f"## Result {rank}",
                    f"- chunk_id: {row['chunk_id']}",
                    f"- source_file: {row['source_file']}",
                    f"- page: {row['page']}",
                    f"- section: {row.get('section') or '(unknown)'}",
                    f"- source_type: {row.get('source_type') or 'text'}",
                    f"- chunk_index: {row['chunk_index']}",
                    f"- rank_lexical: {row.get('rank_lexical', '(not returned)')}",
                    f"- rank_normalized: {row.get('rank_normalized', '(not returned)')}",
                    f"- rank_semantic: {row.get('rank_semantic', '(not returned)')}",
                    f"- lexical_score: {row['lexical_score']:.6f}" if row.get("lexical_score") is not None else "- lexical_score: (not returned)",
                    f"- normalized_score: {row['normalized_score']:.6f}" if row.get("normalized_score") is not None else "- normalized_score: (not returned)",
                    f"- semantic_score: {row['semantic_score']:.6f}" if row.get("semantic_score") is not None else "- semantic_score: (not returned)",
                    f"- rrf_score: {row.get('rrf_score', 0.0):.6f}" if args.mode in {"hybrid", "hybrid-semantic"} else "- rrf_score: (not used)",
                    f"- normalized_terms: {row.get('normalized_terms') or '(not indexed)'}",
                    "",
                    "```text",
                    row["chunk_text"].strip(),
                    "```",
                    "",
                ]
            )
        if requirement_check.get("status") != "not_applicable":
            lines.extend(["## Requirement-ID Mapping Check", "", "```json", json.dumps(requirement_check, indent=2), "```", ""])
        print(f"RAG query: PASS ({len(rows)} results)")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"- Output: {output_path}")
    _append_log(repo_root, script_name, f"PASS results={len(rows)} output={output_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
