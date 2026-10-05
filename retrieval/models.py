"""Shared records for deterministic retrieval."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class IndexedEntity:
    """One searchable project entity and its canonical embedding input."""

    entity_id: str
    entity_type: str
    display_name: str
    full_text_for_embedding: str
    source_file: str = ""
    source_locator: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.entity_id.strip():
            raise ValueError("entity_id must not be empty")
        if not self.entity_type.strip():
            raise ValueError("entity_type must not be empty")
        if not self.display_name.strip():
            raise ValueError("display_name must not be empty")
        if not self.full_text_for_embedding.strip():
            raise ValueError("full_text_for_embedding must not be empty")


@dataclass(frozen=True)
class SemanticCandidate:
    """A semantic result with its cosine score and channel rank."""

    entity_id: str
    entity_type: str
    semantic_score: float
    rank_semantic: int
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FusedCandidate:
    """A result assembled from any available retrieval channels."""

    entity_id: str
    entity_type: str
    final_score: float
    rank_lexical: int | None = None
    rank_normalized: int | None = None
    rank_semantic: int | None = None
    lexical_score: float | None = None
    normalized_score: float | None = None
    semantic_score: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
