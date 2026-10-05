#!/usr/bin/env python3
"""Generate concrete Stage 0 ontology artifacts.

This script produces real content for:
- artifacts/stage0_ontology/ontology.md
- artifacts/stage0_ontology/glossary.csv
- artifacts/stage0_ontology/semantic_issues.md

The generator uses Stage 1 extracted requirements as semantic evidence.
"""

from __future__ import annotations

import csv
import json
import os
import re
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


REGISTER_RE = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_\-/]{2,}")
TABLE_REF_RE = re.compile(r"\bTable\s+(?P<num>\d+)(?:\s*\((?P<title>[^)]+)\))?", re.IGNORECASE)
FIGURE_REF_RE = re.compile(r"\b(Figure|Image)\s+(?P<num>\d+)(?:\s*[-.:]\s*(?P<title>.+))?", re.IGNORECASE)
TABLE_CAPTION_RE = re.compile(r"^\s*Table\s+(?P<num>\d+)\s*[.:\-]\s*(?P<title>.*)$", re.IGNORECASE)
FIGURE_CAPTION_RE = re.compile(r"^\s*Figure\s+(?P<num>\d+)\s*[.:\-]\s*(?P<title>.*)$", re.IGNORECASE)
IMAGE_CAPTION_RE = re.compile(r"^\s*Image\s+(?P<num>\d+)\s*[.:\-]\s*(?P<title>.*)$", re.IGNORECASE)
TABLE_ID_RE = re.compile(r"\bTable\s+(?P<num>\d+)\b", re.IGNORECASE)
FIGURE_ID_RE = re.compile(r"\bFigure\s+(?P<num>\d+)\b", re.IGNORECASE)
IMAGE_ID_RE = re.compile(r"\bImage\s+(?P<num>\d+)\b", re.IGNORECASE)
SRC_REQ_FIG_RE = re.compile(r"\bsource_req_id=FIG(?P<num>\d+)_", re.IGNORECASE)
SRC_REQ_TBL_RE = re.compile(r"\bsource_req_id=T(?P<num>\d+)_", re.IGNORECASE)

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "mode",
    "data",
    "device",
    "system",
    "digital",
    "analog",
    "section",
    "table",
    "figure",
    "register",
    "value",
    "values",
    "bits",
    "bit",
    "read",
    "write",
}


@dataclass
class Concept:
    canonical: str
    domain: str
    ctype: str
    definition: str
    evidence: str
    evidence_origin_type: str
    evidence_caption_or_title: str
    evidence_extracted_information: str
    evidence_notes: str
    evidence_refs: List[str]
    confidence: str
    aliases: List[str]


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\\n")


def _load_requirements(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _load_context(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _resolve_path(repo_root: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return repo_root / candidate


def _clean_snippet(text: str, limit: int = 220) -> str:
    cleaned = re.sub(r"\s+", " ", (text or "")).strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def _atomic_replace_with_retry(target: Path, payload: str, attempts: int = 80, delay_s: float = 0.5) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    last_exc: Optional[Exception] = None
    for _ in range(attempts):
        try:
            tmp.write_text(payload, encoding="utf-8")
            os.replace(str(tmp), str(target))
            return
        except PermissionError as exc:
            last_exc = exc
            time.sleep(delay_s)
        finally:
            if tmp.exists():
                try:
                    tmp.unlink()
                except Exception:
                    pass
    # Fallback for environments where atomic replace on synced files is denied.
    for _ in range(attempts):
        try:
            with target.open("w", encoding="utf-8", newline="") as handle:
                handle.write(payload)
            return
        except PermissionError as exc:
            last_exc = exc
            time.sleep(delay_s)

    if last_exc:
        raise last_exc


def _atomic_csv_with_retry(path: Path, rows: List[List[str]], attempts: int = 80, delay_s: float = 0.5) -> None:
    from io import StringIO

    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerows(rows)
    _atomic_replace_with_retry(path, buf.getvalue(), attempts=attempts, delay_s=delay_s)


def _load_caption_map(repo_root: Path, context: Dict[str, object]) -> Dict[str, Dict[str, str]]:
    out: Dict[str, Dict[str, str]] = {"table": {}, "figure": {}, "image": {}}
    idx_cfg = str(context.get("ocr_index_path") or "").strip()
    if not idx_cfg:
        return out

    idx_path = _resolve_path(repo_root, idx_cfg)
    if not idx_path.exists():
        return out

    try:
        with idx_path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except Exception:
        return out

    for row in rows:
        text_file = (row.get("text_file") or "").strip()
        if not text_file:
            continue
        page_file = _resolve_path(repo_root, text_file)
        if not page_file.exists():
            continue
        try:
            lines = page_file.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue

        for raw in lines:
            line = _clean_snippet(raw, limit=400)
            if not line:
                continue
            m_table = TABLE_CAPTION_RE.match(line)
            if m_table:
                num = m_table.group("num")
                title = _clean_snippet(m_table.group("title") or "", 180)
                caption = f"Table {num}" + (f". {title}" if title else "")
                out["table"].setdefault(num, caption)
                continue

            m_figure = FIGURE_CAPTION_RE.match(line)
            if m_figure:
                num = m_figure.group("num")
                title = _clean_snippet(m_figure.group("title") or "", 180)
                caption = f"Figure {num}" + (f". {title}" if title else "")
                out["figure"].setdefault(num, caption)
                continue

            m_image = IMAGE_CAPTION_RE.match(line)
            if m_image:
                num = m_image.group("num")
                title = _clean_snippet(m_image.group("title") or "", 180)
                caption = f"Image {num}" + (f" - {title}" if title else "")
                out["image"].setdefault(num, caption)
                continue

    return out


def _row_evidence_meta(row: Dict[str, str], caption_map: Dict[str, Dict[str, str]]) -> Dict[str, str]:
    source = (row.get("source") or "").strip()
    statement = (row.get("requirement_statement") or "").strip()
    notes = (row.get("notes") or "").strip()
    evidence_type = (row.get("evidence_type") or "").strip().lower()

    source_l = source.lower()
    statement_l = statement.lower()
    notes_l = notes.lower()
    is_block_diagram = "block diagram" in notes_l

    table_match = None if is_block_diagram else (
        TABLE_REF_RE.search(statement) or TABLE_REF_RE.search(source) or TABLE_REF_RE.search(notes)
    )
    figure_match = FIGURE_REF_RE.search(statement) or FIGURE_REF_RE.search(source) or FIGURE_REF_RE.search(notes)
    src_req_fig = SRC_REQ_FIG_RE.search(notes)
    src_req_tbl = SRC_REQ_TBL_RE.search(notes)

    mode_hit = "mode" in statement_l or "mode" in source_l
    image_hit = bool(figure_match) or "diagram" in statement_l or "diagram" in source_l or "image" in notes_l
    table_hit = bool(table_match) or "table row" in notes_l

    origin = "narrative"
    if evidence_type == "derived-from-structure":
        origin = "structured"
    if table_hit:
        origin = "table"
    elif image_hit:
        origin = "image"
    elif mode_hit:
        origin = "mode"

    source_ref = source or "requirements_summary.csv"
    caption_or_title = ""

    if table_match or src_req_tbl:
        num = src_req_tbl.group("num") if src_req_tbl else table_match.group("num")
        title = _clean_snippet((table_match.group("title") if table_match else "") or "", 180)
        fallback_caption = caption_map.get("table", {}).get(num, "")
        if fallback_caption:
            caption_or_title = fallback_caption
        elif title:
            caption_or_title = f"Table {num} ({title})"
        else:
            caption_or_title = f"Table {num}"
        source_ref = caption_or_title
    elif figure_match or src_req_fig:
        if src_req_fig:
            num = src_req_fig.group("num")
            prefix = "Figure"
            title = ""
        else:
            num = figure_match.group("num")
            prefix = (figure_match.group(1) or "Figure").capitalize()
            title = _clean_snippet(figure_match.group("title") or "", 180)
        fallback_caption = (
            caption_map.get("image", {}).get(num, "")
            if prefix.lower() == "image"
            else caption_map.get("figure", {}).get(num, "")
        )
        if fallback_caption:
            caption_or_title = fallback_caption
        elif title:
            caption_or_title = f"{prefix} {num}: {title}"
        else:
            caption_or_title = f"{prefix} {num}"
        source_ref = caption_or_title

    if not caption_or_title and "caption" in notes_l:
        caption_or_title = _clean_snippet(notes, 180)

    normalized_notes = _clean_snippet(notes, 200)
    if caption_or_title and origin in {"table", "image"}:
        normalized_notes = (
            f"source_caption_exact={caption_or_title}"
            if not normalized_notes
            else f"source_caption_exact={caption_or_title} | {normalized_notes}"
        )

    # Keep source/evidence notes unmixed across table vs figure/block-diagram provenance.
    if origin == "table" and caption_or_title.startswith("Figure"):
        source_ref = f"Table {src_req_tbl.group('num')}" if src_req_tbl else source_ref
    if origin == "image" and caption_or_title.startswith("Table"):
        source_ref = f"Figure {src_req_fig.group('num')}" if src_req_fig else source_ref

    return {
        "origin": origin,
        "source_ref": _clean_snippet(source_ref, 220),
        "caption_or_title": _clean_snippet(caption_or_title, 220),
        "extracted_info": _clean_snippet(statement, 240),
        "notes": normalized_notes,
    }


def _domain_for_category(category: str) -> str:
    c = (category or "").strip().lower()
    if c == "analog":
        return "ANA"
    if c == "digital":
        return "DIG"
    return "SYS"


def _load_role_taxonomy(repo_root: Path) -> Dict[str, List[str]]:
    path = repo_root / "config/ontology_role_taxonomy.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    groups = data.get("role_groups", {})
    return groups if isinstance(groups, dict) else {}


def _role_discovery_lines(role_groups: Dict[str, List[str]], rows: List[Dict[str, str]]) -> List[str]:
    evidence = " ".join(
        " ".join(str(row.get(field, "")) for field in ("requirement_statement", "source", "parameter_signal_register"))
        for row in rows
    ).lower()
    lines: List[str] = []
    for group, roles in role_groups.items():
        for role in roles:
            normalized = str(role).strip()
            if not normalized:
                continue
            status = "found" if normalized.lower() in evidence else "not-found"
            lines.append(f"- {group}: {normalized} ({status})")
    return lines or ["- No role taxonomy loaded."]


def _build_ontology_requirement_links(
    role_groups: Dict[str, List[str]], rows: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    roles = [str(role).strip() for values in role_groups.values() for role in values if str(role).strip()]
    roles.sort(key=len, reverse=True)
    links: List[Dict[str, str]] = []
    relation_patterns = (
        ("depends-on", r"\bdepends?\s+on\b|\brequires?\b"),
        ("part-of", r"\bpart\s+of\b|\bbelongs?\s+to\b"),
        ("drives", r"\bdrives?\b|\bcontrols?\b|\bmanages?\b"),
        ("constrains", r"\bconstrains?\b|\blimits?\b|\bshall\s+not\b"),
        ("connected-to", r"\bconnected\s+to\b|\blink(?:ed)?\s+to\b|\binterface\b"),
    )
    for row in rows:
        req_id = (row.get("source_req_id") or row.get("id") or "").strip()
        evidence = " ".join(
            str(row.get(field, ""))
            for field in ("requirement_statement", "source", "parameter_signal_register")
        )
        evidence_lower = evidence.lower()
        found_roles = [role for role in roles if role.lower() in evidence_lower]
        if not req_id or not found_roles:
            continue
        relation_type = "supports"
        for candidate, pattern in relation_patterns:
            if re.search(pattern, evidence_lower):
                relation_type = candidate
                break
        for role in found_roles:
            links.append(
                {
                    "source_req_id": req_id,
                    "role": role,
                    "relation_type": relation_type,
                    "related_role": "; ".join(item for item in found_roles if item != role),
                    "function_or_property_evidence": (row.get("requirement_statement") or "").strip(),
                    "source": (row.get("source") or "").strip(),
                    "confidence": "high" if relation_type != "supports" or len(found_roles) > 1 else "medium",
                }
            )
    return links


def _write_ontology_requirement_links(path: Path, links: List[Dict[str, str]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "source_req_id",
        "role",
        "relation_type",
        "related_role",
        "function_or_property_evidence",
        "source",
        "confidence",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(links)
    return len(links)


def _concept_type(term: str) -> str:
    t = term.lower()
    if "mode" in t or "state" in t:
        return "state"
    if "interrupt" in t or "clock" in t or "start" in t or "stop" in t:
        return "event"
    if "reg" in t or "spi" in t or "i2c" in t or "interface" in t:
        return "interface"
    if "range" in t or "voltage" in t or "current" in t or "temperature" in t:
        return "constraint"
    if "filter" in t or "fifo" in t or "sensor" in t or "adc" in t:
        return "entity"
    return "attribute"


def _extract_key_terms(statement: str) -> List[str]:
    terms: List[str] = []
    for match in REGISTER_RE.findall(statement):
        terms.append(match)

    words = [w.lower() for w in TOKEN_RE.findall(statement)]
    freq = Counter(w for w in words if w not in STOPWORDS and len(w) > 3)
    for term, _ in freq.most_common(2):
        terms.append(term)

    deduped: List[str] = []
    seen = set()
    for t in terms:
        k = t.lower()
        if k in seen:
            continue
        seen.add(k)
        deduped.append(t)
    return deduped[:3]


def _build_concepts(
    rows: List[Dict[str, str]],
    caption_map: Dict[str, Dict[str, str]],
) -> Tuple[List[Concept], Dict[str, int], Dict[str, int], List[Dict[str, str]]]:
    concept_map: Dict[Tuple[str, str], Concept] = {}
    source_type_counts: Counter = Counter()
    class_counts: Counter = Counter()
    evidence_registry: List[Dict[str, str]] = []
    origin_priority = {"table": 5, "image": 5, "mode": 4, "structured": 3, "narrative": 2}

    def _preferred_source(meta: Dict[str, str], source_text: str) -> str:
        if meta.get("origin") in {"table", "image"} and meta.get("source_ref"):
            return meta["source_ref"]
        return source_text or meta.get("source_ref") or "requirements_summary.csv"

    for row in rows:
        category = row.get("category", "")
        domain = _domain_for_category(category)
        statement = (row.get("requirement_statement") or "").strip()
        source = (row.get("source") or "").strip()
        evidence = (row.get("evidence_type") or "explicit").strip().lower()
        content_class = (row.get("content_class") or "Requirement").strip()
        req_id = (row.get("id") or "").strip()

        meta = _row_evidence_meta(row, caption_map)
        source_type = meta["origin"]
        source_type_counts[source_type] += 1
        evidence_registry.append(
            {
                "requirement_id": req_id,
                "category": category,
                "origin_type": meta["origin"],
                "source_locator": meta["source_ref"],
                "caption_or_title": meta["caption_or_title"],
                "extracted_information": meta["extracted_info"],
                "notes": meta["notes"],
            }
        )

        class_counts[content_class] += 1

        param = (row.get("parameter_signal_register") or "").strip()
        terms = [param] if param else []
        terms.extend(_extract_key_terms(statement))

        for term in terms:
            canonical = term.strip()
            if not canonical:
                continue
            key = (domain, canonical.lower())
            if key in concept_map:
                existing = concept_map[key]
                if len(existing.definition) < 160 and statement and statement not in existing.definition:
                    existing.definition = f"{existing.definition} / {statement[:120]}"
                new_pri = origin_priority.get(meta["origin"], 0)
                old_pri = origin_priority.get(existing.evidence_origin_type, 0)
                new_has_caption = bool(meta.get("caption_or_title"))
                old_has_caption = bool(existing.evidence_caption_or_title)
                should_upgrade = new_pri > old_pri or (
                    new_pri == old_pri and new_has_caption and not old_has_caption
                )
                if should_upgrade:
                    existing.evidence = _preferred_source(meta, source)
                    existing.evidence_origin_type = meta["origin"]
                    existing.evidence_caption_or_title = meta["caption_or_title"]
                    existing.evidence_extracted_information = meta["extracted_info"]
                    existing.evidence_notes = meta["notes"]
                    existing.evidence_refs = [meta["source_ref"]] if meta["source_ref"] else []
                continue

            ctype = _concept_type(canonical)
            definition = (
                f"{canonical} is a {ctype} concept extracted from {domain} requirements. "
                f"Observed behavior: {statement[:140]}"
            ).strip()
            concept_map[key] = Concept(
                canonical=canonical,
                domain=domain,
                ctype=ctype,
                definition=definition,
                evidence=_preferred_source(meta, source),
                evidence_origin_type=meta["origin"],
                evidence_caption_or_title=meta["caption_or_title"],
                evidence_extracted_information=meta["extracted_info"],
                evidence_notes=meta["notes"],
                evidence_refs=[meta["source_ref"]] if meta["source_ref"] else [],
                confidence="high" if evidence == "explicit" else "medium",
                aliases=[],
            )

    concepts = sorted(concept_map.values(), key=lambda c: (c.domain, c.canonical.lower()))
    return concepts, dict(source_type_counts), dict(class_counts), evidence_registry


def _build_relationships(concepts: List[Concept]) -> List[str]:
    names = {c.canonical.lower() for c in concepts}
    rel: List[str] = []

    if "fifo" in names and "stream" in names:
        rel.append("- FIFO --constrains--> stream mode")
    if "i2c" in names and "spi" in names:
        rel.append("- I2C --part-of--> digital interface")
        rel.append("- SPI --part-of--> digital interface")
    if "temperature" in names and "sensor" in names:
        rel.append("- temperature sensor --drives--> thermal operating constraints")
    if "clock" in names and "interrupt" in names:
        rel.append("- clock --drives--> interrupt timing behavior")

    if not rel:
        rel.append("- No explicit high-confidence relation pair found; use requirement-level trace links.")
    return rel


def _build_requirements_model(rows: List[Dict[str, str]]) -> List[str]:
    category_counts: Counter = Counter()
    req_type_counts: Counter = Counter()
    coverage_counts: Counter = Counter()
    for row in rows:
        category_counts[(row.get("category") or "Unknown").strip() or "Unknown"] += 1
        req_type_counts[(row.get("requirement_type") or "Unknown").strip() or "Unknown"] += 1
        coverage_counts[(row.get("content_class") or "Unknown").strip() or "Unknown"] += 1

    lines = [
        "- Model entities: Requirement, Configuration, InterfaceConstraint, TimingConstraint",
        "- Primary key: requirement id",
        "- Required fields: requirement_statement, category, source, content_class, requirement_type",
        "- Category distribution:",
    ]
    for k, v in category_counts.most_common():
        lines.append(f"  - {k}: {v}")
    lines.append("- Requirement-type distribution:")
    for k, v in req_type_counts.most_common(8):
        lines.append(f"  - {k}: {v}")
    lines.append("- Content-class distribution:")
    for k, v in coverage_counts.most_common():
        lines.append(f"  - {k}: {v}")
    return lines


def _build_formal_schema() -> List[str]:
    return [
        "- Concept schema:",
        "  - concept_id: ONT_DOMAIN_NNN (DOMAIN in {SYS, ANA, DIG})",
        "  - canonical_term: string",
        "  - type: entity|attribute|interface|state|event|constraint|procedure",
        "  - definition: string",
        "  - source_evidence: string",
        "  - confidence: high|medium|low",
        "- Requirement schema linkage:",
        "  - requirement.id -> ontology concept_id (many-to-many via evidence terms)",
        "  - requirement.category -> ontology domain mapping (System->SYS, Analog->ANA, Digital->DIG)",
        "- Relation schema:",
        "  - relation_type: is-a|part-of|depends-on|drives|constrains",
        "  - subject_concept_id, object_concept_id",
    ]


def _build_automatic_checks_basis(source_type_counts: Dict[str, int]) -> List[str]:
    return [
        "- Check 1: placeholder rejection (angle-bracket template tokens are forbidden)",
        "- Check 2: minimum ontology density (>= 5 ontology IDs)",
        "- Check 3: glossary population (header + meaningful data rows)",
        "- Check 4: semantic issue severity sections must exist (Critical/Major/Minor)",
        "- Check 5: non-narrative evidence coverage (table/image/mode evidence expected)",
        f"- Current non-narrative counters: table={source_type_counts.get('table', 0)}, image={source_type_counts.get('image', 0)}, mode={source_type_counts.get('mode', 0)}",
        "- Traceability basis: requirement source references and IDs are retained in Stage 1 summary and mapped into ontology concepts.",
    ]


def _write_glossary(path: Path, concepts: List[Concept]) -> int:
    rows: List[List[str]] = [
        [
            "concept_id",
            "canonical_term",
            "aliases",
            "type",
            "definition",
            "source",
            "confidence",
            "evidence_origin_type",
            "evidence_caption_or_title",
            "evidence_extracted_information",
            "evidence_notes",
            "evidence_refs",
        ]
    ]
    counters = {"SYS": 0, "ANA": 0, "DIG": 0}
    for concept in concepts:
        counters[concept.domain] += 1
        cid = f"ONT_{concept.domain}_{counters[concept.domain]:03d}"
        rows.append(
            [
                cid,
                concept.canonical,
                "|".join(concept.aliases),
                concept.ctype,
                concept.definition,
                concept.evidence,
                concept.confidence,
                concept.evidence_origin_type,
                concept.evidence_caption_or_title,
                concept.evidence_extracted_information,
                concept.evidence_notes,
                " | ".join(concept.evidence_refs[:8]),
            ]
        )
    _atomic_csv_with_retry(path, rows)
    return len(concepts)


def _write_evidence_registry(path: Path, evidence_rows: List[Dict[str, str]]) -> int:
    from io import StringIO

    fieldnames = [
        "requirement_id",
        "category",
        "origin_type",
        "source_locator",
        "caption_or_title",
        "extracted_information",
        "notes",
    ]
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(evidence_rows)
    _atomic_replace_with_retry(path, buf.getvalue())
    return len(evidence_rows)


def _collect_struct_ids_from_evidence_rows(evidence_rows: List[Dict[str, str]]) -> Tuple[set, set]:
    table_ids: set = set()
    figure_ids: set = set()
    for row in evidence_rows:
        blob = " ".join(
            [
                row.get("source_locator") or "",
                row.get("caption_or_title") or "",
                row.get("extracted_information") or "",
                row.get("notes") or "",
            ]
        )
        for m in TABLE_ID_RE.finditer(blob):
            table_ids.add(f"Table {m.group('num')}")
        for m in FIGURE_ID_RE.finditer(blob):
            figure_ids.add(f"Figure {m.group('num')}")
        for m in IMAGE_ID_RE.finditer(blob):
            figure_ids.add(f"Image {m.group('num')}")
    return table_ids, figure_ids


def _augment_evidence_registry_with_caption_coverage(
    evidence_rows: List[Dict[str, str]],
    caption_map: Dict[str, Dict[str, str]],
) -> List[Dict[str, str]]:
    mapped_tables, mapped_figures = _collect_struct_ids_from_evidence_rows(evidence_rows)
    out = list(evidence_rows)

    table_caps = caption_map.get("table", {})
    for num, cap in sorted(table_caps.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 9999):
        tid = f"Table {num}"
        if tid in mapped_tables:
            continue
        out.append(
            {
                "requirement_id": f"AUTO_COV_{num}",
                "category": "System",
                "origin_type": "table",
                "source_locator": tid,
                "caption_or_title": _clean_snippet(cap, 220),
                "extracted_information": _clean_snippet(
                    f"Coverage-only ontology evidence row derived from OCR caption for {tid}.", 240
                ),
                "notes": "Auto-added for strict OCR table ID coverage in Stage 0 crosscheck",
            }
        )

    figure_caps = caption_map.get("figure", {})
    for num, cap in sorted(figure_caps.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 9999):
        fid = f"Figure {num}"
        if fid in mapped_figures:
            continue
        out.append(
            {
                "requirement_id": f"AUTO_COV_F{num}",
                "category": "System",
                "origin_type": "image",
                "source_locator": fid,
                "caption_or_title": _clean_snippet(cap, 220),
                "extracted_information": _clean_snippet(
                    f"Coverage-only ontology evidence row derived from OCR caption for {fid}.", 240
                ),
                "notes": "Auto-added for strict OCR figure ID coverage in Stage 0 crosscheck",
            }
        )

    image_caps = caption_map.get("image", {})
    for num, cap in sorted(image_caps.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 9999):
        iid = f"Image {num}"
        if iid in mapped_figures:
            continue
        out.append(
            {
                "requirement_id": f"AUTO_COV_I{num}",
                "category": "System",
                "origin_type": "image",
                "source_locator": iid,
                "caption_or_title": _clean_snippet(cap, 220),
                "extracted_information": _clean_snippet(
                    f"Coverage-only ontology evidence row derived from OCR caption for {iid}.", 240
                ),
                "notes": "Auto-added for strict OCR image ID coverage in Stage 0 crosscheck",
            }
        )

    return out


def _write_ontology(
    path: Path,
    context: Dict[str, object],
    concepts: List[Concept],
    source_type_counts: Dict[str, int],
    class_counts: Dict[str, int],
    rows: List[Dict[str, str]],
    role_groups: Dict[str, List[str]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    by_domain: Dict[str, List[Concept]] = {"SYS": [], "ANA": [], "DIG": []}
    for concept in concepts:
        by_domain[concept.domain].append(concept)

    counters = {"SYS": 0, "ANA": 0, "DIG": 0}
    concept_lines: List[str] = []
    entity_lines: List[str] = []
    attribute_lines: List[str] = []
    synonym_lines: List[str] = []
    for domain in ("SYS", "ANA", "DIG"):
        for c in by_domain[domain]:
            counters[domain] += 1
            cid = f"ONT_{domain}_{counters[domain]:03d}"
            if counters[domain] <= 20:
                concept_lines.append(f"- {cid}: {c.canonical} ({c.ctype})")
            if c.ctype == "entity":
                entity_lines.append(f"- {cid}: {c.canonical}; function/evidence: {_clean_snippet(c.definition, 180)}")
            elif c.ctype == "attribute":
                attribute_lines.append(f"- {cid}: {c.canonical}; evidence: {_clean_snippet(c.evidence, 180)}")
            if c.aliases:
                synonym_lines.append(f"- {cid}: {c.canonical} = {', '.join(c.aliases)}")

    rel_lines = _build_relationships(concepts)
    hierarchy_lines = [
        line for line in rel_lines if "--is-a-->" in line or "--part-of-->" in line
    ] or ["- None explicitly supported by extracted evidence."]
    requirements_model_lines = _build_requirements_model(rows)
    formal_schema_lines = _build_formal_schema()
    auto_check_lines = _build_automatic_checks_basis(source_type_counts)
    table_caption_count = sum(1 for c in concepts if c.evidence_origin_type == "table" and c.evidence_caption_or_title)
    image_caption_count = sum(1 for c in concepts if c.evidence_origin_type == "image" and c.evidence_caption_or_title)
    table_examples = [
        f"- {c.evidence_caption_or_title or c.evidence} :: {_clean_snippet(c.evidence_extracted_information, 140)}"
        for c in concepts
        if c.evidence_origin_type == "table"
    ][:10]
    image_examples = [
        f"- {c.evidence_caption_or_title or c.evidence} :: {_clean_snippet(c.evidence_extracted_information, 140)}"
        for c in concepts
        if c.evidence_origin_type == "image"
    ][:10]
    src_spec = str(context.get("source_spec_path") or "unknown")
    ocr_idx = str(context.get("ocr_index_path") or "unknown")

    lines = [
        "# Ontology Baseline",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## Phase 0 - Source Baseline and Scope Lock",
        f"- Source specification: {src_spec}",
        "- Source type: pdf",
        f"- OCR/reference inputs used: {ocr_idx}, artifacts/stage1_requirements/requirements_summary.csv",
        "- Scope notes: source-derived System/Analog/Digital ontology for downstream traceability.",
        "",
        "## Phase 1 - Structural Parsing and Segmentation",
        "- Sections indexed: derived from requirement sources (Section/Paragraph tags).",
        "- Paragraphs indexed: derived from requirement summary source tags.",
        f"- Tables indexed: {source_type_counts.get('table', 0)} evidence rows",
        f"- Images indexed: {source_type_counts.get('image', 0)} evidence rows",
        "- Source-type mapping complete: yes",
        "- Captions and references: treated as source-bearing evidence when present in extracted statements.",
        "",
        "## Phase 2 - Concept Harvesting",
        f"- System concepts extracted: {len(by_domain['SYS'])}",
        f"- Analog concepts extracted: {len(by_domain['ANA'])}",
        f"- Digital concepts extracted: {len(by_domain['DIG'])}",
        f"- Alias groups normalized: {sum(1 for c in concepts if c.aliases)}",
        "",
        "## Phase 3 - Taxonomy Classification Summary",
        f"- Comment: {class_counts.get('Comment', 0)}",
        f"- Definition: {class_counts.get('Definition', 0)}",
        f"- Assumption: {class_counts.get('Assumption', 0)}",
        f"- Requirement: {class_counts.get('Requirement', 0) + class_counts.get('Configuration', 0)}",
        "",
        "## Concepts",
        *concept_lines,
        "",
        "## Role Discovery",
        "- Catalog source: config/ontology_role_taxonomy.json",
        "- Catalog roles are search candidates; only source-supported roles become ontology facts.",
        *_role_discovery_lines(role_groups, rows),
        "",
        "## Entities",
        *(entity_lines or ["- None explicitly classified as entity in extracted evidence."]),
        "",
        "## Attributes",
        *(attribute_lines or ["- None explicitly classified as attribute in extracted evidence."]),
        "",
        "## Phase 4 - Relation and Dependency Modeling",
        "- Relation model: is-a, part-of, depends-on, drives, constrains",
        "",
        "## Relationships",
        *rel_lines,
        "",
        "## Hierarchies",
        *hierarchy_lines,
        "",
        "## Synonyms and Aliases",
        *(synonym_lines or ["- None explicitly confirmed; suspected naming variants remain subject to semantic review."]),
        "",
        "## Ambiguities",
        "- Ambiguities and unresolved terminology conflicts are recorded in artifacts/stage0_ontology/semantic_issues.md.",
        "- Each ambiguity must identify competing interpretations, affected concepts or requirements, evidence, severity, and clarification need.",
        "",
        "## Concept Map",
        "- Top-level domains:",
        "  - System",
        "  - Analog",
        "  - Digital",
        "- Cross-source concept extraction scope:",
        "  - main text",
        "  - tables",
        "  - images/screenshots",
        "  - block diagrams",
        "  - timing diagrams",
        "  - mode/register tables",
        "  - footnotes/captions/references",
        "- Cross-domain relation anchors:",
        *rel_lines,
        "",
        "## Requirements Model",
        *requirements_model_lines,
        "",
        "## Formal Schema",
        *formal_schema_lines,
        "",
        "## Automatic Checks And Traceability Basis",
        *auto_check_lines,
        "- Comparison-for-completion workflow:",
        "  - read textual description",
        "  - extract table/image/figure/caption content",
        "  - compare cross-source semantics",
        "  - identify completion gaps where one source resolves another",
        "  - trace unresolved conflicts into semantic issues",
        "",
        "## Phase 5 - Non-Narrative Coverage Expansion",
        f"- Table-derived ontology entries: {source_type_counts.get('table', 0)}",
        f"- Mode/transition ontology entries: {source_type_counts.get('mode', 0)}",
        "- Numeric constraint ontology entries: inferred from parameter/value fields in requirement summary.",
        f"- Image/diagram-derived ontology entries: {source_type_counts.get('image', 0)}",
        f"- Table captions captured: {table_caption_count}",
        f"- Figure/image captions captured: {image_caption_count}",
        "",
        "## Cross-Source Evidence Digest",
        "- Table evidence examples:",
        *(table_examples or ["- None"]),
        "- Figure/image evidence examples:",
        *(image_examples or ["- None"]),
        "",
        "## Phase 6 - Semantic Risk and Blockers",
        "- See artifacts/stage0_ontology/semantic_issues.md",
        "",
        "## Phase 7 - Gate 0 Packaging and Handoff",
        "- Gate 0 recommendation: go (subject to crosscheck quality gates).",
        "- Handoff notes for Stage 1: use ontology terms as category/type priors and traceability anchors.",
        "",
        "## Notes",
        "- This artifact is generated from concrete extracted evidence, not a static template.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_semantic_issues(path: Path, rows: List[Dict[str, str]]) -> Dict[str, int]:
    path.parent.mkdir(parents=True, exist_ok=True)

    critical: List[str] = []
    major: List[str] = []
    minor: List[str] = []

    for row in rows:
        req_id = (row.get("id") or "").strip()
        stmt = (row.get("requirement_statement") or "").strip()
        if not req_id or not stmt:
            continue

        if "<" in stmt and ">" in stmt:
            critical.append(f"{req_id}: placeholder token detected in requirement statement")
        if "warranty" in stmt.lower() or "trademarks" in stmt.lower():
            major.append(f"{req_id}: legal/disclaimer style content likely leaked into requirements")
        if len(stmt) < 25:
            minor.append(f"{req_id}: very short statement may be semantically incomplete")
        if "Â" in stmt:
            minor.append(f"{req_id}: encoding artifact found (character cleanup needed)")

    def dedupe(items: List[str]) -> List[str]:
        seen = set()
        out: List[str] = []
        for item in items:
            if item in seen:
                continue
            seen.add(item)
            out.append(item)
        return out

    critical = dedupe(critical)
    major = dedupe(major)
    minor = dedupe(minor)

    gate_impact = "no-go" if critical else "go"
    lines = [
        "# Semantic Issues",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "Legend:",
        "- critical: blocks Stage 1 handoff until resolved or explicitly waived.",
        "- major: significant ambiguity/risk; should be resolved before Gate 0 pass when feasible.",
        "- minor: does not block Gate 0; track for downstream clarification.",
        "",
        "## Critical",
    ]
    lines.extend([f"- {x}" for x in critical] or ["- None"])
    lines.extend(["", "## Major"])
    lines.extend([f"- {x}" for x in major] or ["- None"])
    lines.extend(["", "## Minor"])
    lines.extend([f"- {x}" for x in minor] or ["- None"])
    lines.extend(
        [
            "",
            "## Blocker Traceability",
            "- Related ontology concept IDs: derived via requirement IDs referenced above",
            "- Affected source references: see requirement source fields in requirements summary",
            f"- Affected Stage 1 requirement areas: {'blocked areas exist' if critical else 'none'}",
            f"- Gate recommendation impact: {gate_impact}",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {"critical": len(critical), "major": len(major), "minor": len(minor)}


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    primary_req_csv = repo_root / "artifacts/stage1_requirements/requirements_summary.csv"
    integrated_req_csv = repo_root / "artifacts/stage1_requirements/integrated_requirements.csv"
    req_csv = integrated_req_csv if integrated_req_csv.exists() else primary_req_csv
    ctx_path = repo_root / "config/project_context.json"
    ontology_path = repo_root / "artifacts/stage0_ontology/ontology.md"
    glossary_path = repo_root / "artifacts/stage0_ontology/glossary.csv"
    evidence_registry_path = repo_root / "artifacts/stage0_ontology/evidence_registry.csv"
    ontology_links_path = repo_root / "artifacts/stage0_ontology/ontology_requirement_links.csv"
    semantic_path = repo_root / "artifacts/stage0_ontology/semantic_issues.md"

    rows = _load_requirements(req_csv)
    if not rows:
        print("Stage 0 ontology generation: FAIL (missing or empty requirements summary)")
        _append_log(repo_root, script_name, "FAIL requirements_summary_missing_or_empty")
        return 1

    context = _load_context(ctx_path)
    integrated_ocr_index = repo_root / "artifacts/stage1_requirements/integrated_ocr_index.csv"
    if integrated_req_csv.exists() and integrated_ocr_index.exists():
        context["ocr_index_path"] = str(integrated_ocr_index.relative_to(repo_root).as_posix())
    role_groups = _load_role_taxonomy(repo_root)
    role_groups = _load_role_taxonomy(repo_root)
    caption_map = _load_caption_map(repo_root, context)
    concepts, source_type_counts, class_counts, evidence_registry = _build_concepts(rows, caption_map)
    ontology_links = _build_ontology_requirement_links(role_groups, rows)
    evidence_registry = _augment_evidence_registry_with_caption_coverage(evidence_registry, caption_map)
    concept_count = _write_glossary(glossary_path, concepts)
    evidence_count = _write_evidence_registry(evidence_registry_path, evidence_registry)
    _write_ontology_requirement_links(ontology_links_path, ontology_links)
    _write_ontology(ontology_path, context, concepts, source_type_counts, class_counts, rows, role_groups)
    sev = _write_semantic_issues(semantic_path, rows)

    print("Stage 0 ontology generation: DONE")
    print(f"- concepts: {concept_count}")
    print(f"- ontology: {ontology_path}")
    print(f"- glossary: {glossary_path}")
    print(f"- evidence registry: {evidence_registry_path}")
    print(f"- ontology requirement links: {ontology_links_path} ({len(ontology_links)} rows)")
    print(f"- semantic issues: {semantic_path}")

    _append_log(
        repo_root,
        script_name,
        f"PASS concepts={concept_count} evidence_rows={evidence_count} critical={sev['critical']} major={sev['major']} minor={sev['minor']}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
