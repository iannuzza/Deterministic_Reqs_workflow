"""Persisted exact cosine semantic index."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Iterable, Sequence

from .embeddings import LocalEmbeddingModel
from .models import IndexedEntity, SemanticCandidate


class SemanticIndexUnavailable(RuntimeError):
    """Raised when a semantic index cannot be loaded or used."""


class ExactCosineIndex:
    backend_name = "exact_cosine"

    def __init__(self) -> None:
        self.dimension = 0
        self.model_fingerprint = ""
        self.model_id = ""
        self.entities: list[IndexedEntity] = []
        self.vectors: list[list[float]] = []

    def build(self, entities: Iterable[IndexedEntity], embedding_model: LocalEmbeddingModel, batch_size: int = 32) -> None:
        self.entities = list(entities)
        if not self.entities:
            raise ValueError("cannot build semantic index without entities")
        self.vectors = []
        for start in range(0, len(self.entities), batch_size):
            self.vectors.extend(embedding_model.embed([item.full_text_for_embedding for item in self.entities[start:start + batch_size]]))
        self.dimension = len(self.vectors[0])
        if self.dimension == 0 or any(len(vector) != self.dimension for vector in self.vectors):
            raise ValueError("embedding vectors must have a consistent non-zero dimension")
        self.model_id = embedding_model.model_id
        self.model_fingerprint = embedding_model.fingerprint()

    def save(self, path: Path) -> None:
        if len(self.entities) != len(self.vectors) or not self.entities:
            raise ValueError("semantic index has not been built")
        path.mkdir(parents=True, exist_ok=True)
        (path / "entities.jsonl").write_text(
            "".join(json.dumps({"entity": entity.__dict__}, sort_keys=True, default=dict) + "\n" for entity in self.entities),
            encoding="utf-8",
        )
        (path / "vectors.json").write_text(json.dumps(self.vectors, separators=(",", ":")), encoding="utf-8")
        manifest = {
            "format_version": 1,
            "backend": self.backend_name,
            "dimension": self.dimension,
            "entity_count": len(self.entities),
            "model_id": self.model_id,
            "model_fingerprint": self.model_fingerprint,
        }
        (path / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "ExactCosineIndex":
        try:
            manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
            vectors = json.loads((path / "vectors.json").read_text(encoding="utf-8"))
            entities = [json.loads(line)["entity"] for line in (path / "entities.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            raise SemanticIndexUnavailable(f"invalid semantic index at {path}") from exc
        if manifest.get("backend") != cls.backend_name or manifest.get("entity_count") != len(entities) or len(vectors) != len(entities):
            raise SemanticIndexUnavailable(f"incompatible semantic index manifest at {path}")
        index = cls()
        index.dimension = int(manifest["dimension"])
        index.model_id = str(manifest.get("model_id", ""))
        index.model_fingerprint = str(manifest.get("model_fingerprint", ""))
        index.vectors = [[float(value) for value in vector] for vector in vectors]
        index.entities = [IndexedEntity(**entity) for entity in entities]
        if any(len(vector) != index.dimension for vector in index.vectors):
            raise SemanticIndexUnavailable(f"vector dimension mismatch at {path}")
        return index

    def is_compatible(self, embedding_model: LocalEmbeddingModel) -> bool:
        return self.model_fingerprint == embedding_model.fingerprint() and self.dimension == embedding_model.dimension

    def search(self, query_vector: Sequence[float], top_k: int) -> list[SemanticCandidate]:
        if top_k <= 0:
            raise ValueError("top_k must be > 0")
        if len(query_vector) != self.dimension:
            raise ValueError("query vector dimension does not match index")
        query_norm = math.sqrt(sum(value * value for value in query_vector))
        if query_norm == 0:
            return []
        scored: list[tuple[float, IndexedEntity]] = []
        for entity, vector in zip(self.entities, self.vectors):
            vector_norm = math.sqrt(sum(value * value for value in vector))
            score = sum(left * right for left, right in zip(query_vector, vector)) / (query_norm * vector_norm) if vector_norm else 0.0
            scored.append((score, entity))
        scored.sort(key=lambda item: (-item[0], item[1].entity_id))
        return [SemanticCandidate(entity.entity_id, entity.entity_type, score, rank, entity.metadata) for rank, (score, entity) in enumerate(scored[:top_k], start=1)]


def semantic_search(
    *,
    query: str,
    top_k: int,
    index: ExactCosineIndex,
    embedding_model: LocalEmbeddingModel,
    entity_types: set[str] | None = None,
) -> list[SemanticCandidate]:
    """Embed a query locally and return candidates from an optional type scope."""
    if not index.is_compatible(embedding_model):
        raise SemanticIndexUnavailable("semantic index and embedding model are incompatible")
    candidates = index.search(embedding_model.embed_query(query), len(index.entities))
    if entity_types is not None:
        candidates = [candidate for candidate in candidates if candidate.entity_type in entity_types]
    return [
        SemanticCandidate(candidate.entity_id, candidate.entity_type, candidate.semantic_score, rank, candidate.metadata)
        for rank, candidate in enumerate(candidates[:top_k], start=1)
    ]
