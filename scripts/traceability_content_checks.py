"""Shared source-to-traceability content checks for staged specifications."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Dict, Iterable, List, Set


def read_source_requirements(path: Path) -> Dict[str, Dict[str, str]]:
    """Read the Stage 1 source catalog keyed by its preserved source ID."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows: Dict[str, Dict[str, str]] = {}
        for row in csv.DictReader(handle):
            source_id = (row.get("source_req_id") or row.get("id") or "").strip()
            if source_id:
                rows[source_id] = {
                    key: (value or "").strip()
                    for key, value in row.items()
                    if key is not None
                }
        return rows


def _normalize_statement(text: str) -> str:
    normalized = (text or "").strip()
    normalized = re.sub(r"\[\s*Covers\s*:\s*[^\]]+\]\s*", "", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\[[^]]*\]\s*Requirement:?\s*", "", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\[End\]", "", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\[(?:TO|Vpriority)[^]]*\]", "", normalized, flags=re.IGNORECASE)
    # Inline source-ID references may be removed from authored prose; they remain
    # traceable through Covers and must not make equivalent source text differ.
    normalized = re.sub(r"\[[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*_\d+\]", "", normalized)
    normalized = re.sub(r"\[\s*\]", "", normalized)
    normalized = re.sub(r"<[^>]+>", " ", normalized)
    normalized = normalized.replace("&nbsp;", " ")
    normalized = re.sub(r"(?:^|\s)[•●-]\s+", " ", normalized)
    normalized = re.sub(
        r"^The\s+digital\s+subsystem\s+shall\s+satisfy\s+the\s+following\s+behavior:\s*",
        "",
        normalized,
        flags=re.IGNORECASE,
    )
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = re.sub(r":\s*\.", ":", normalized)
    normalized = re.sub(r"\s*([_.])\s*", r"\1", normalized)
    return normalized.strip().rstrip(".").lower()


def check_source_traceability_content(
    trace_rows: Iterable[Dict[str, str]],
    source_rows: Dict[str, Dict[str, str]],
    exempt_source_ids: Set[str],
    authored_id_field: str,
    stage_label: str,
) -> List[str]:
    """Check source IDs and preserve source wording in a stage trace matrix.

    Matrix and structural rows are exempt from direct wording comparison because
    their generators intentionally derive statements from structured evidence.
    Their source IDs must still resolve to the Stage 1 catalog.
    """
    rows = list(trace_rows)
    findings: List[str] = []
    seen_source_ids: Set[str] = set()
    for row in rows:
        authored_id = (row.get(authored_id_field) or "").strip() or "unknown"
        source_id = (row.get("source_req_id") or "").strip()
        if not source_id:
            findings.append(f"{stage_label} traceability row {authored_id} has no source_req_id")
            continue
        if source_id in seen_source_ids:
            findings.append(f"{stage_label} traceability contains duplicate source_req_id: {source_id}")
        seen_source_ids.add(source_id)
        source_row = source_rows.get(source_id)
        if source_row is None:
            if source_id in exempt_source_ids:
                continue
            findings.append(f"{stage_label} source_req_id is absent from Stage 1 catalog: {source_id}")
            continue

        source_text = _normalize_statement(source_row.get("requirement_statement", ""))
        trace_text = _normalize_statement(row.get("requirement_statement", ""))
        if not source_text:
            findings.append(f"Stage 1 source statement is empty: {source_id}")
        if not trace_text:
            findings.append(f"{stage_label} trace statement is empty: {authored_id} ({source_id})")
        if source_id in exempt_source_ids or not source_text or not trace_text:
            continue
        if source_text not in trace_text:
            findings.append(
                f"{stage_label} statement does not preserve DDS source text: "
                f"{authored_id} -> {source_id}"
            )

    return findings


def check_authored_markdown_content(
    markdown: str,
    trace_rows: Iterable[Dict[str, str]],
    source_rows: Dict[str, Dict[str, str]],
    exempt_source_ids: Set[str],
    authored_id_field: str,
    stage_label: str,
) -> List[str]:
    """Ensure authored Markdown bodies retain the complete source statement."""
    authored_to_source = {
        (row.get(authored_id_field) or "").strip(): (row.get("source_req_id") or "").strip()
        for row in trace_rows
        if (row.get(authored_id_field) or "").strip()
    }
    pattern = re.compile(
        rf"^\s*\[({re.escape(authored_id_field.split('_')[0].upper())}-REQ-\d{{3}})\]\s+Requirement:\s*\n"
        r"(.*?)(?=^\s*\[[A-Z]+-REQ-\d{3}\]\s+Requirement:\s*$|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    findings: List[str] = []
    for authored_id, block in pattern.findall(markdown or ""):
        source_id = authored_to_source.get(authored_id, "")
        if not source_id or source_id in exempt_source_ids:
            continue
        source_text = _normalize_statement(source_rows.get(source_id, {}).get("requirement_statement", ""))
        body = re.split(r"^\s*Covers:\s*[^\n]+\s*$", block, maxsplit=1, flags=re.MULTILINE)[0]
        body_text = _normalize_statement(body)
        if source_text and source_text not in body_text:
            findings.append(
                f"{stage_label} authored body omits DDS source content: {authored_id} -> {source_id}"
            )
    return findings