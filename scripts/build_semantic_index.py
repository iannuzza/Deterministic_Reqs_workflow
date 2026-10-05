#!/usr/bin/env python3
"""Build the optional local semantic retrieval index."""

from __future__ import annotations

import argparse
import csv
import json
import sqlite3
from pathlib import Path
import sys
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from retrieval.embedding_text import (
    build_block_embedding_text,
    build_function_embedding_text,
    build_interface_embedding_text,
    build_requirement_embedding_text,
    canonical_full_text_for_embedding,
)
from retrieval.embeddings import LocalHashEmbeddingModel, LocalSentenceTransformerEmbedding
from retrieval.models import IndexedEntity
from retrieval.semantic_index import ExactCosineIndex


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _first(row: dict[str, str], *names: str) -> str:
    for name in names:
        if (row.get(name) or "").strip():
            return row[name].strip()
    return ""


def _artifact_entity(row: dict[str, str], entity_type: str, text: str, name: str, source_file: str) -> IndexedEntity | None:
    if not name or not text.strip():
        return None
    return IndexedEntity(
        entity_id=f"{entity_type}:{name}",
        entity_type=entity_type,
        display_name=name,
        full_text_for_embedding=text,
        source_file=source_file,
        source_locator=_first(row, "Source", "Source Paragraph", "Source Locator"),
        metadata={"source_row": row},
    )


def _collect_csv_entities(repo_root: Path) -> list[IndexedEntity]:
    entities: list[IndexedEntity] = []
    sources = [
        (repo_root / "artifacts/stage2_mirco_arc/block_inventory.csv", "block"),
        (repo_root / "artifacts/stage1_requirements/requirements_summary.csv", "requirement"),
    ]
    for path, entity_type in sources:
        for row in _read_rows(path):
            if entity_type == "block":
                name = _first(row, "Block", "Name")
                text = build_block_embedding_text(row)
            else:
                name = _first(row, "source_req_id", "Requirement ID", "id")
                text = build_requirement_embedding_text(row)
            entity = _artifact_entity(row, entity_type, text, name, path.relative_to(repo_root).as_posix())
            if entity:
                entities.append(entity)

    function_path = repo_root / "artifacts/stage2_mirco_arc/block_inventory.csv"
    for row in _read_rows(function_path):
        name = _first(row, "Function", "Function Name")
        text = build_function_embedding_text(row)
        entity = _artifact_entity(row, "function", text, name, function_path.relative_to(repo_root).as_posix())
        if entity:
            entities.append(entity)

    interface_paths = [
        repo_root / "artifacts/stage2_mirco_arc/source_io_table_coverage.csv",
        repo_root / "artifacts/stage2_mirco_arc/interface_catalog.csv",
    ]
    for path in interface_paths:
        for row in _read_rows(path):
            name = _first(row, "Interface", "Name", "Port", "I/O")
            text = build_interface_embedding_text(row)
            entity = _artifact_entity(row, "interface", text, name, path.relative_to(repo_root).as_posix())
            if entity:
                entities.append(entity)
    return entities


def _collect_chunk_entities(repo_root: Path, db_path: Path) -> list[IndexedEntity]:
    if not db_path.exists():
        return []
    entities: list[IndexedEntity] = []
    with sqlite3.connect(str(db_path)) as conn:
        columns = {str(row[1]) for row in conn.execute("PRAGMA table_info(chunks)").fetchall()}
        selected = [name for name in ("id", "source_file", "page", "section", "source_type", "chunk_text") if name in columns]
        if "id" not in selected or "chunk_text" not in selected:
            return []
        for row in conn.execute(f"SELECT {', '.join(selected)} FROM chunks ORDER BY id"):
            values = dict(zip(selected, row))
            text = canonical_full_text_for_embedding(
                entity_type="chunk",
                name=f"{values['source_file']}:{values['page']}:{values['id']}",
                requirement_text=str(values.get("chunk_text") or ""),
                source_context=f"page {values.get('page', '')}; section {values.get('section', '')}",
            )
            entities.append(IndexedEntity(
                entity_id=f"chunk:{values['id']}",
                entity_type="chunk",
                display_name=f"{values['source_file']}:{values['page']}:{values['id']}",
                full_text_for_embedding=text,
                source_file=str(values.get("source_file") or ""),
                source_locator=f"page {values.get('page', '')}",
                metadata={"chunk_id": values["id"], "source_type": values.get("source_type", "text")},
            ))
    return entities


def collect_indexed_entities(repo_root: Path, db_path: Path) -> list[IndexedEntity]:
    """Collect all available searchable entities with collision-safe IDs."""
    entities = _collect_csv_entities(repo_root) + _collect_chunk_entities(repo_root, db_path)
    unique: dict[str, IndexedEntity] = {}
    for entity in entities:
        unique.setdefault(entity.entity_id, entity)
    return list(unique.values())


def _embedding_model(config: dict, repo_root: Path):
    model_type = config.get("model_type", "local_sentence_transformer")
    if model_type == "local_hash":
        return LocalHashEmbeddingModel(int(config.get("dimension", 256)))
    model_path = Path(str(config.get("model_path", "models/local_embedding_model")))
    if not model_path.is_absolute():
        model_path = repo_root / model_path
    return LocalSentenceTransformerEmbedding(model_path, device=str(config.get("device", "cpu")))


def build_semantic_index(*, repo_root: Path, output_path: Path, db_path: Path, config: dict) -> dict:
    model = _embedding_model(config, repo_root)
    entities = collect_indexed_entities(repo_root, db_path)
    index = ExactCosineIndex()
    index.build(entities, model, batch_size=int(config.get("batch_size", 32)))
    index.save(output_path)
    return {"backend": index.backend_name, "entity_count": len(entities), "dimension": index.dimension, "model_id": index.model_id, "output": output_path.as_posix()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the optional local semantic index")
    parser.add_argument("--output", default=None)
    parser.add_argument("--db-path", default=None)
    parser.add_argument("--config", default="config/retrieval_config.json")
    parser.add_argument("--model-type", choices=("local_hash", "local_sentence_transformer"), default=None)
    parser.add_argument("--dimension", type=int, default=None, help="Dimension for the local_hash model override.")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    config_root = _load_json(repo_root / args.config)
    config = config_root.get("semantic_retrieval", config_root)
    if args.model_type:
        config = dict(config)
        config["model_type"] = args.model_type
    if args.dimension is not None:
        config = dict(config)
        config["dimension"] = args.dimension
    context = _load_json(repo_root / "config/project_context.json")
    db_path = Path(str(args.db_path or context.get("rag_db_path") or "artifacts/rag/rag_index.sqlite"))
    output_path = Path(str(args.output or config.get("index_path", "artifacts/rag/semantic_index")))
    if not db_path.is_absolute():
        db_path = repo_root / db_path
    if not output_path.is_absolute():
        output_path = repo_root / output_path
    summary = build_semantic_index(repo_root=repo_root, output_path=output_path, db_path=db_path, config=config)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
