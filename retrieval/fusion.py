"""Deterministic reciprocal-rank fusion for optional retrieval channels."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


def reciprocal_rank_fusion(
    channels: Mapping[str, Sequence[Mapping[str, Any]]],
    *,
    top_k: int,
    rrf_k: int = 60,
    weights: Mapping[str, float] | None = None,
    protected_ids: set[Any] | None = None,
    id_field: str = "entity_id",
) -> list[dict[str, Any]]:
    """Fuse ranked channel rows while retaining channel ranks and scores."""
    if top_k <= 0 or rrf_k <= 0:
        raise ValueError("top_k and rrf_k must be > 0")
    fused: dict[Any, dict[str, Any]] = {}
    for channel_name, rows in channels.items():
        channel_weight = (weights or {}).get(channel_name, 1.0)
        if channel_weight < 0:
            raise ValueError("channel weights must be >= 0")
        for rank, row in enumerate(rows, start=1):
            item_id = row.get(id_field)
            if item_id is None:
                continue
            item = fused.setdefault(item_id, {id_field: item_id})
            item.update(row)
            item[f"rank_{channel_name}"] = rank
            score = row.get(f"{channel_name}_score")
            if score is not None:
                item[f"{channel_name}_score"] = score
            item["rrf_score"] = item.get("rrf_score", 0.0) + channel_weight / (rrf_k + rank)
    protected = protected_ids or set()
    return sorted(
        fused.values(),
        key=lambda row: (
            0 if row[id_field] in protected else 1,
            -row.get("rrf_score", 0.0),
            str(row[id_field]),
        ),
    )[:top_k]


def fuse_lexical_normalized(
    lexical_rows: list[dict[str, Any]],
    normalized_rows: list[dict[str, Any]],
    *,
    final_top_k: int,
    rrf_k: int = 60,
) -> list[dict[str, Any]]:
    """Compatibility wrapper for the original two-channel contract."""
    return reciprocal_rank_fusion(
        {"lexical": lexical_rows, "normalized": normalized_rows},
        top_k=final_top_k,
        rrf_k=rrf_k,
        id_field="chunk_id",
    )


def fuse_lexical_normalized_semantic(
    lexical_rows: list[dict[str, Any]],
    normalized_rows: list[dict[str, Any]],
    semantic_rows: list[dict[str, Any]],
    *,
    final_top_k: int,
    rrf_k: int = 60,
    protected_ids: set[Any] | None = None,
) -> list[dict[str, Any]]:
    """Fuse lexical, normalized, and semantic rows by shared entity ID."""
    return reciprocal_rank_fusion(
        {"lexical": lexical_rows, "normalized": normalized_rows, "semantic": semantic_rows},
        top_k=final_top_k,
        rrf_k=rrf_k,
        weights={"lexical": 1.0, "normalized": 1.0, "semantic": 0.25},
        protected_ids=protected_ids,
        id_field="chunk_id",
    )
