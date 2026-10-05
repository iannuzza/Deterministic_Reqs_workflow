"""Deterministic S0 primary-source tagging and req-ID prefix assessment."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

from audit_log import record_event
from canonical_store import connect, fingerprint, utc_now

HEADER_ALIASES = {
    "reqid", "requirementid", "specid", "sourceid", "source_req_id",
}
TAGGED_ID_RE = re.compile(r"\[\s*(?P<reqid>[A-Z][A-Z0-9]*(?:[_-][A-Z0-9]+)*_?\d+)\s*\]", re.IGNORECASE)
BARE_ID_RE = re.compile(r"\b(?P<reqid>[A-Z][A-Z0-9]*(?:[_-][A-Z0-9]+)*_?\d+)\b", re.IGNORECASE)


@dataclass(frozen=True)
class BootstrapAssessment:
    source_path: str
    status: str
    proposed_prefix: str
    tagged_count: int
    table_id_count: int
    unbracketed_id_count: int
    evidence: tuple[dict[str, object], ...]
    reason: str


class _HtmlTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.parts.append(data.strip())


def _extract_text(path: Path) -> list[str]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader
        return [(page.extract_text() or "") for page in PdfReader(str(path)).pages]
    if suffix in {".html", ".htm"}:
        parser = _HtmlTextParser()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        return ["\n".join(parser.parts)]
    if suffix == ".docx":
        from zipfile import ZipFile
        from xml.etree import ElementTree
        with ZipFile(path) as archive:
            xml = archive.read("word/document.xml")
        root = ElementTree.fromstring(xml)
        return ["\n".join(node.text or "" for node in root.iter() if node.tag.endswith("}t"))]
    raise ValueError(f"Unsupported source type: {path.suffix}")


def _header_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def _configured_patterns(project_context: dict) -> tuple[re.Pattern[str], ...]:
    rules = project_context.get("requirement_id_rules") or {}
    values = rules.get("table_req_id_patterns") or rules.get("source_req_id_patterns") or []
    compiled = []
    for value in values:
        try:
            compiled.append(re.compile(str(value), re.IGNORECASE))
        except re.error:
            continue
    return tuple(compiled) or (BARE_ID_RE,)


def _prefix(req_id: str) -> str:
    return re.sub(r"[_-]?\d+$", "", req_id.upper()).rstrip("_-")


def assess_source(source: Path, project_context: dict | None = None) -> BootstrapAssessment:
    if not source.exists():
        raise FileNotFoundError(source)
    context = project_context or {}
    patterns = _configured_patterns(context)
    tagged: list[dict[str, object]] = []
    table_ids: list[dict[str, object]] = []
    unbracketed: list[dict[str, object]] = []
    prefixes: list[str] = []
    for page_no, text in enumerate(_extract_text(source), start=1):
        lines = [" ".join(line.split()) for line in text.splitlines() if line.strip()]
        table_header = False
        for line_no, line in enumerate(lines, start=1):
            normalized_tokens = {_header_key(token) for token in re.split(r"[|,;\t]+", line)}
            if normalized_tokens & HEADER_ALIASES or _header_key(line) in HEADER_ALIASES:
                table_header = True
                table_ids.append({"page": page_no, "line": line_no, "kind": "table_header", "text": line})
            tagged_matches = list(TAGGED_ID_RE.finditer(line))
            for match in tagged_matches:
                req_id = match.group("reqid").upper()
                if any(pattern.search(req_id) for pattern in patterns):
                    prefixes.append(_prefix(req_id))
                    tagged.append({"page": page_no, "line": line_no, "kind": "tagged", "req_id": req_id, "text": line})
            if table_header:
                for match in BARE_ID_RE.finditer(line):
                    req_id = match.group("reqid").upper()
                    if any(pattern.search(req_id) for pattern in patterns):
                        prefixes.append(_prefix(req_id))
                        table_ids.append({"page": page_no, "line": line_no, "kind": "table_req_id", "req_id": req_id, "text": line})
            elif not tagged_matches:
                for match in BARE_ID_RE.finditer(line):
                    req_id = match.group("reqid").upper()
                    if any(pattern.search(req_id) for pattern in patterns):
                        prefixes.append(_prefix(req_id))
                        unbracketed.append({"page": page_no, "line": line_no, "kind": "unbracketed", "req_id": req_id, "text": line})
    unique_prefixes = sorted(set(prefixes))
    proposed_prefix = unique_prefixes[0] if len(unique_prefixes) == 1 else ""
    if tagged and (unbracketed or len(unique_prefixes) > 1):
        status = "ambiguous"
        reason = "bracketed tags coexist with unbracketed IDs or multiple prefix families"
    elif tagged:
        status = "tagged"
        reason = "bracketed requirement tags were detected"
    elif table_ids or unbracketed:
        status = "ambiguous"
        reason = "IDs were detected in tables or unbracketed text without definitive tagged requirement markers"
    else:
        status = "untagged"
        reason = "no configured requirement ID evidence was detected"
    evidence = tuple(tagged + table_ids + unbracketed)
    return BootstrapAssessment(str(source), status, proposed_prefix, len(tagged), sum(item["kind"] == "table_req_id" for item in table_ids), len(unbracketed), evidence, reason)


def persist_candidate(repo_root: Path, *, project_id: str, assessment: BootstrapAssessment, actor: str = "system") -> str:
    payload = asdict(assessment)
    profile_id = "source-baseline-" + fingerprint({"project_id": project_id, "assessment": payload})[:24]
    connection = connect(repo_root)
    try:
        connection.execute("INSERT OR IGNORE INTO projects(project_id, project_name, created_at) VALUES (?, ?, ?)", (project_id, project_id, utc_now()))
        connection.execute(
            """INSERT OR IGNORE INTO profile_revisions(
                profile_revision_id, project_id, profile_kind, profile_name, revision_number,
                profile_payload_json, content_fingerprint, lifecycle_state, approval_state,
                created_at)
                VALUES (?, ?, 'source_baseline', 'primary_source_bootstrap', ?, ?, ?, 'staged', 'pending', ?)""",
            (profile_id, project_id, "candidate-" + fingerprint(payload)[:12], json.dumps(payload, sort_keys=True), fingerprint(payload), utc_now()),
        )
        connection.commit()
    finally:
        connection.close()
    record_event(repo_root, event_type="source_imported", entity_type="source_baseline", entity_id=profile_id, actor=actor, message="S0 source tagging assessment stored as candidate; approval required", project_id=project_id, source=assessment.source_path, payload=payload)
    return profile_id


def approve_candidate(repo_root: Path, *, profile_id: str, actor: str, approved_prefix: str | None = None) -> None:
    connection = connect(repo_root)
    try:
        row = connection.execute("SELECT profile_payload_json FROM profile_revisions WHERE profile_revision_id = ? AND profile_kind = 'source_baseline'", (profile_id,)).fetchone()
        if row is None:
            raise LookupError(f"Unknown source bootstrap candidate: {profile_id}")
        payload = json.loads(row[0])
        if approved_prefix is not None:
            payload["proposed_prefix"] = approved_prefix
        payload["approved_prefix"] = payload.get("proposed_prefix", "")
        payload["approved_by"] = actor
        payload["approved_at"] = utc_now()
        connection.execute("UPDATE profile_revisions SET profile_payload_json = ?, lifecycle_state = 'approved', approval_state = 'approved', approved_by = ?, approved_at = ? WHERE profile_revision_id = ?", (json.dumps(payload, sort_keys=True), actor, payload["approved_at"], profile_id))
        connection.commit()
    finally:
        connection.close()
    record_event(repo_root, event_type="review_approved", entity_type="source_baseline", entity_id=profile_id, actor=actor, message="S0 source bootstrap candidate explicitly approved", payload={"approved_prefix": payload.get("approved_prefix", "")})
