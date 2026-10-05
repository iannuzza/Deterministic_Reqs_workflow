"""Deterministic, labeled text construction for local embeddings."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import re

from .models import IndexedEntity


def _clean(value: object) -> str:
    return re.sub(r"\\s+", " ", str(value or "")).strip()


def _join_values(values: Sequence[str]) -> str:
    return ", ".join(value for value in (_clean(item) for item in values) if value)


def canonical_full_text_for_embedding(
    *,
    entity_type: str,
    name: str,
    description: str = "",
    function: str = "",
    inputs: Sequence[str] = (),
    outputs: Sequence[str] = (),
    requirement_text: str = "",
    source_context: str = "",
) -> str:
    """Build stable labeled text while retaining technical terms and IDs."""
    fields = [
        ("Entity type", entity_type),
        ("Name", name),
        ("Description", description),
        ("Function", function),
        ("Inputs", _join_values(inputs)),
        ("Outputs", _join_values(outputs)),
        ("Requirement", requirement_text),
        ("Source context", source_context),
    ]
    return "\n".join(f"{label}: {_clean(value)}" for label, value in fields if _clean(value))


def build_block_embedding_text(row: Mapping[str, str]) -> str:
    return canonical_full_text_for_embedding(
        entity_type="block",
        name=row.get("Block", ""),
        description=row.get("Description", ""),
        function=row.get("Function", ""),
        inputs=_split_values(row.get("Inputs", "")),
        outputs=_split_values(row.get("Outputs", "")),
        source_context=row.get("Source Context", ""),
    )


def build_function_embedding_text(row: Mapping[str, str]) -> str:
    return canonical_full_text_for_embedding(
        entity_type="function",
        name=row.get("Function", row.get("Name", "")),
        description=row.get("Description", ""),
        function=row.get("Function", ""),
        inputs=_split_values(row.get("Inputs", "")),
        outputs=_split_values(row.get("Outputs", "")),
        source_context=row.get("Source Context", ""),
    )


def build_requirement_embedding_text(row: Mapping[str, str]) -> str:
    requirement_id = row.get("source_req_id", row.get("Requirement ID", row.get("id", "")))
    statement = row.get("Requirement", row.get("Requirement Statement", row.get("statement", "")))
    return canonical_full_text_for_embedding(
        entity_type="requirement",
        name=requirement_id,
        requirement_text=statement,
        source_context=row.get("Source", row.get("Source Paragraph", "")),
    )


def build_interface_embedding_text(row: Mapping[str, str]) -> str:
    return canonical_full_text_for_embedding(
        entity_type="interface",
        name=row.get("Interface", row.get("Name", row.get("Port", ""))),
        description=row.get("Description", row.get("Details", "")),
        inputs=_split_values(row.get("Inputs", row.get("Direction", ""))),
        outputs=_split_values(row.get("Outputs", row.get("Type", ""))),
        source_context=row.get("Source Context", row.get("Source", "")),
    )


def _split_values(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"[;,|]", value or "") if item.strip()]


def validate_embedding_text(entity: IndexedEntity) -> None:
    """Validate that stored text has stable identity labels."""
    text = entity.full_text_for_embedding
    if not text.strip():
        raise ValueError(f"empty embedding text for {entity.entity_id}")
    required_labels = ("Entity type:", "Name:")
    missing = [label for label in required_labels if label not in text]
    if missing:
        raise ValueError(f"embedding text for {entity.entity_id} misses {', '.join(missing)}")
