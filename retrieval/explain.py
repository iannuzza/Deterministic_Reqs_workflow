"""Explainability helpers for deterministic retrieval results."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


def explain_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    """Return only stable channel and fused-score fields for audit output."""
    return {
        key: candidate.get(key)
        for key in (
            "entity_id", "chunk_id", "entity_type",
            "rank_lexical", "rank_normalized", "rank_semantic",
            "lexical_score", "normalized_score", "semantic_score", "rrf_score",
        )
        if key in candidate
    }


def render_explain_markdown(*, query: str, mode: str, candidates: Sequence[dict[str, Any]]) -> str:
    lines = [
        "# Retrieval Explanation",
        "",
        f"- Query: {query}",
        f"- Mode: {mode}",
        "",
        "| Candidate | Lexical rank | Normalized rank | Semantic rank | Lexical score | Normalized score | Semantic score | Final RRF |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for candidate in candidates:
        item = explain_candidate(candidate)
        lines.append(
            "| {id} | {lex} | {norm} | {sem} | {lex_score} | {norm_score} | {sem_score} | {rrf} |".format(
                id=item.get("entity_id", item.get("chunk_id", "")),
                lex=item.get("rank_lexical", ""), norm=item.get("rank_normalized", ""), sem=item.get("rank_semantic", ""),
                lex_score=item.get("lexical_score", ""), norm_score=item.get("normalized_score", ""),
                sem_score=item.get("semantic_score", ""), rrf=item.get("rrf_score", ""),
            )
        )
    return "\n".join(lines) + "\n"
