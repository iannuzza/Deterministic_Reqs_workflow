"""Centralized deterministic vocabulary and lexical-resource loading."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

DEFAULT_STOPWORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "into",
    "is", "it", "of", "on", "or", "shall", "should", "that", "the", "this", "to", "with",
})


class VocabularyResolutionError(RuntimeError):
    """Raised when the approved vocabulary resource is missing or invalid."""


def load_approved_vocabulary(repo_root: Path, project_context: Mapping[str, object] | None = None) -> dict:
    context = project_context or {}
    configured = context.get("domain_vocabulary_path") or "config/domain_vocabulary.json"
    path = Path(str(configured))
    if not path.is_absolute():
        path = repo_root / path
    if not path.exists():
        raise VocabularyResolutionError(f"Approved vocabulary resource is missing: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VocabularyResolutionError(f"Approved vocabulary resource is invalid: {path}") from exc
    if not isinstance(payload, dict):
        raise VocabularyResolutionError("Approved vocabulary must be a JSON object.")
    payload["stopwords"] = sorted({str(item).lower() for item in payload.get("stopwords", DEFAULT_STOPWORDS) if str(item).strip()})
    payload["_source_path"] = path.as_posix()
    payload["_approved"] = True
    return payload


def approved_stopwords(vocabulary: Mapping[str, object]) -> frozenset[str]:
    values = vocabulary.get("stopwords", DEFAULT_STOPWORDS)
    return frozenset(str(item).lower() for item in values)
