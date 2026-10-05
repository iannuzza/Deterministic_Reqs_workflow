"""Shared, non-authoritative low-power descriptive retrieval and assembly."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Iterable, Mapping, Sequence


DEFAULT_CONFIG_PATH = Path("config/descriptive_topics.json")
DRS_TOP_LEVEL_SCOPES = frozenset({"top_digital", "integration", "architecture", "lifted_integration", "shared_domain"})
_SIGNAL_TOKEN_RE = re.compile(r"\b(?:i|o|ca|u)_[a-z0-9_]+\b", re.IGNORECASE)


def load_low_power_config(repo_root: Path) -> dict:
    path = repo_root / DEFAULT_CONFIG_PATH
    if not path.exists():
        return {"topics": [], "scope_profiles": {}}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def is_drs_top_level_record(record: Mapping[str, object]) -> bool:
    """Return whether a record can establish top-level DRS descriptive evidence."""
    scope = _text(record, "scope", "evidence_scope", "layer").casefold()
    if scope not in DRS_TOP_LEVEL_SCOPES:
        return False
    evidence_kind = _text(record, "evidence_kind", "source_type").casefold()
    return evidence_kind not in {"block_local", "digital_ipos", "ipos"}


def architecture_records_from_function_rows(
    rows: Iterable[Sequence[str]],
) -> list[dict[str, str]]:
    """Convert Stage 2 function rows into scoped descriptive evidence records."""
    records: list[dict[str, str]] = []
    for row in rows:
        if len(row) < 3:
            continue
        statement, metadata, owner = (str(value).strip() for value in row[:3])
        statement = re.sub(r"^[\u2022*-]\s*", "", statement)
        source_match = re.search(r"(?:^|;)\s*source=(.+)$", metadata)
        source = source_match.group(1).strip() if source_match else metadata
        is_system = owner.casefold() in {"system", "sys"}
        evidence_kind = "power_domain" if metadata.casefold().startswith("power_domain;") else ("architecture" if is_system else "block_local")
        records.append({
            "statement": statement,
            "source": source,
            "scope": "architecture" if is_system else "block_local",
            "domain": "system" if is_system else owner,
            "evidence_kind": evidence_kind,
            "record_type": evidence_kind,
        })
    return records


def filter_configured_descriptive_exclusions(
    records: Iterable[Mapping[str, object]],
    *,
    repo_root: Path,
) -> list[Mapping[str, object]]:
    """Remove configured non-technical descriptive content from render inputs."""
    config = load_low_power_config(repo_root)
    return [
        record
        for record in records
        if not _excluded(
            f"{_text(record, 'statement', 'function', 'text')} "
            f"{_text(record, 'source', 'provenance', 'source_file')}",
            config,
        )
    ]


def power_domain_records_from_ocr(repo_root: Path, *, ocr_root: Path | None = None) -> list[dict[str, str]]:
    """Read approved Stage 1 OCR power-domain tables as structured evidence."""
    config = load_low_power_config(repo_root).get("structured_extractors", {}).get("power_domain", {})
    ocr_root = ocr_root or (repo_root / "artifacts/stage1_requirements/ocr_extracts")
    index_path = ocr_root / "index.csv"
    paths: list[Path] = []
    if index_path.exists() and index_path.is_file():
        with index_path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if str(row.get("status") or "").casefold() == "text-extracted":
                    path = Path(str(row.get("text_file") or ""))
                    paths.append(path if path.is_absolute() else ocr_root / path)
    else:
        paths = sorted(ocr_root.glob("*.txt"))
    paths = [path for path in paths if path.exists()]
    if not paths:
        return []
    full_text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    architecture_pattern = "|".join(re.escape(str(item)) for item in config.get("architecture_markers", []))
    description_pattern = "|".join(re.escape(str(item)) for item in config.get("description_markers", []))
    if not architecture_pattern or not description_pattern:
        return []
    architecture_matches = list(re.finditer(
        rf"(?:\d+(?:\.\d+)?\s*)?(?:{architecture_pattern})(?P<body>.*?)(?=(?:\d+(?:\.\d+)?\s*)?(?:{description_pattern})|\Z)",
        full_text,
        flags=re.IGNORECASE | re.DOTALL,
    ))
    description_matches = list(re.finditer(
        rf"(?:\d+(?:\.\d+)?\s*)?(?:{description_pattern})(?P<body>.*?)(?=\n\s*\d+(?:\.\d+)+\s+[A-Z]|\Z)",
        full_text,
        flags=re.IGNORECASE | re.DOTALL,
    ))
    if not architecture_matches:
        return []
    architecture_match = architecture_matches[-1]
    description_match = description_matches[-1] if description_matches else None
    table_text = architecture_match.group("body")
    description_text = description_match.group("body") if description_match else ""
    records: list[dict[str, str]] = []
    body = re.sub(r"\s+", " ", table_text).strip()
    identifier_pattern = str(config.get("domain_identifier_pattern") or r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b")
    descriptions: dict[str, str] = {}
    for match in re.finditer(
        rf"(?:\d+\.)+\s*({identifier_pattern})\s+(.*?)(?=\n\s*(?:\d+\.)+\s+[A-Z]|\Z)",
        description_text,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        descriptions[match.group(1)] = re.sub(r"\s+", " ", match.group(2)).strip()
    if descriptions:
        domain_matches = sorted(
            (match for name in descriptions for match in re.finditer(re.escape(name), body)),
            key=lambda match: match.start(),
        )
    else:
        domain_matches = list(re.finditer(f"({identifier_pattern})", body))
    for index, match in enumerate(domain_matches):
        name = match.group(1) if match.lastindex else match.group(0)
        end = domain_matches[index + 1].start() if index + 1 < len(domain_matches) else len(body)
        row = body[match.end():end].strip()
        type_terms = "|".join(re.escape(str(item)) for item in config.get("domain_type_terms", []))
        type_match = re.search(rf"\b({type_terms})\b", row, flags=re.IGNORECASE)
        if not type_match:
            continue
        domain_type = type_match.group(1)
        prefix = row[:type_match.start()].strip()
        suffix = row[type_match.end():].strip()
        control_terms = "|".join(re.escape(str(item)) for item in config.get("control_terms", []))
        control_match = re.search(rf"\b({control_terms})\b", suffix)
        control = control_match.group(1) if control_match else ""
        notes = suffix[control_match.end():].strip() if control_match else suffix
        voltage_match = re.search(r"\b\d+(?:\.\d+)?(?:V|[A-Z])?(?:[÷-]\d+(?:\.\d+)?V?)?\b", prefix)
        voltage = voltage_match.group(0) if voltage_match else ""
        included = prefix[:voltage_match.start()].strip() if voltage_match else prefix
        for block_pattern in config.get("non_architecture_block_patterns", []):
            included = re.sub(str(block_pattern), "", included, flags=re.IGNORECASE)
        for block_prefix in config.get("non_architecture_block_prefixes", []):
            included = re.sub(
                rf"\b{re.escape(str(block_prefix))}[A-Za-z0-9_]*\s*,?\s*",
                "",
                included,
                flags=re.IGNORECASE,
            )
        included = re.sub(r"\s*,\s*,", ",", included).strip(" ,")
        parts = [f"{name}: Included block(s): {included}.", f"Domain type: {domain_type}."]
        if voltage:
            parts.append(f"Voltage: {voltage}.")
        if control:
            parts.append(f"Control mode: {control}.")
        if notes:
            parts.append(f"Notes: {notes}.")
        if name in descriptions:
            parts.append(descriptions[name])
        records.append({
            "statement": " ".join(parts),
            "source": f"Stage 1 OCR power-domain table/description ({name})",
            "scope": "architecture",
            "domain": "power",
            "evidence_kind": "power_domain",
            "record_type": "power_domain",
        })
    return records


def read_selected_low_power_audit(path: Path) -> list[dict[str, str]]:
    """Read selected, provenanced records from an upstream low-power audit."""
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [
        {
            "statement": str(row.get("statement") or "").strip(),
            "source": str(row.get("source") or "").strip(),
            "scope": str(row.get("scope") or "").strip(),
            "domain": str(row.get("domain") or "").strip(),
            "evidence_kind": "architecture",
        }
        for row in rows
        if str(row.get("decision") or "").strip().casefold() == "selected"
        and str(row.get("statement") or "").strip()
        and str(row.get("source") or "").strip()
    ]


def _text(record: Mapping[str, object], *keys: str) -> str:
    for key in keys:
        value = record.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def _tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def _normalized_tokens(value: str) -> set[str]:
    tokens = _tokens(value)
    normalized = set(tokens)
    for token in tokens:
        if token.endswith("ies") and len(token) > 4:
            normalized.add(token[:-3] + "y")
        elif token.endswith("ing") and len(token) > 5:
            normalized.add(token[:-3])
        elif token.endswith("ed") and len(token) > 4:
            normalized.add(token[:-2])
        elif token.endswith("s") and not token.endswith("ss") and len(token) > 4:
            normalized.add(token[:-1])
    return normalized


def _matches_seed(text: str, seed: str) -> bool:
    seed_tokens = _tokens(seed)
    if not seed_tokens:
        return False
    haystack = text.casefold()
    if len(seed_tokens) > 1:
        return seed.casefold() in haystack
    return bool(seed_tokens.intersection(_normalized_tokens(text)))


def _excluded(text: str, config: Mapping[str, object]) -> str:
    for phrase in config.get("exclude_phrases", []):
        if str(phrase).casefold() in text.casefold():
            return f"excluded phrase: {phrase}"
    return ""


def assemble_low_power_descriptive(
    records: Iterable[Mapping[str, object]],
    *,
    repo_root: Path,
    profile: str,
    max_items_per_topic: int = 6,
) -> tuple[dict[str, list[str]], list[dict[str, str]]]:
    """Return grouped low-power descriptions and a reviewable decision audit."""
    config = load_low_power_config(repo_root)
    profile_config = (config.get("scope_profiles") or {}).get(profile, {})
    allowed_scopes = {str(item).casefold() for item in profile_config.get("allowed_scopes", [])}
    allowed_domains = {str(item).casefold() for item in profile_config.get("allowed_domains", [])}
    topics = [item for item in config.get("topics", []) if item.get("name")]
    grouped: dict[str, list[str]] = {str(item["name"]): [] for item in topics}
    audit: list[dict[str, str]] = []
    seen: set[str] = set()

    for input_order, record in enumerate(records):
        statement = _text(record, "statement", "function", "text", "Source Paragraph", "Non-Block Function Context")
        source = _text(record, "source", "provenance", "source_file", "Source Paragraph")
        scope = _text(record, "scope", "evidence_scope", "layer").casefold()
        domain = _text(record, "domain", "competence_domain", "source_type").casefold()
        combined = f"{statement} {source}"
        row = {
            "profile": profile,
            "input_order": str(input_order),
            "query_seed": "",
            "statement": statement,
            "source": source,
            "scope": scope,
            "domain": domain,
            "decision": "rejected",
            "reason": "",
            "topic": "",
            "output_order": "",
        }
        if not statement:
            row["reason"] = "missing statement"
            audit.append(row)
            continue
        if allowed_scopes and scope not in allowed_scopes:
            row["reason"] = "scope not allowed"
            audit.append(row)
            continue
        if allowed_domains and domain and domain not in allowed_domains:
            row["reason"] = "competence domain not allowed"
            audit.append(row)
            continue
        excluded = _excluded(combined, config)
        if excluded:
            row["reason"] = excluded
            audit.append(row)
            continue
        if _SIGNAL_TOKEN_RE.search(statement) and _text(record, "record_type", "evidence_kind").casefold() != "power_domain":
            row["reason"] = "signal-level detail not eligible for top-level descriptive text"
            audit.append(row)
            continue
        key = re.sub(r"\s+", " ", statement.casefold()).strip()
        if key in seen:
            row["reason"] = "duplicate descriptive evidence"
            audit.append(row)
            continue

        selected_topic = None
        selected_seed = ""
        if _text(record, "record_type", "evidence_kind").casefold() == "power_domain":
            selected_topic = "Power-domain architecture"
            selected_seed = "structured power-domain evidence"
        for topic in topics:
            if selected_topic:
                break
            if not all(_matches_seed(combined, str(seed)) for seed in topic.get("required_seeds", [])):
                continue
            for seed in topic.get("seeds", []):
                if _matches_seed(combined, str(seed)):
                    selected_topic = str(topic["name"])
                    selected_seed = str(seed)
                    break
            if selected_topic:
                break
        if not selected_topic:
            row["reason"] = "no configured low-power topic match"
            audit.append(row)
            continue
        row["query_seed"] = selected_seed
        row["topic"] = selected_topic
        if len(grouped[selected_topic]) >= max_items_per_topic:
            row["reason"] = "topic output limit"
            audit.append(row)
            continue
        seen.add(key)
        grouped[selected_topic].append(statement)
        row["decision"] = "selected"
        row["reason"] = "eligible descriptive evidence"
        row["output_order"] = str(len(grouped[selected_topic]))
        audit.append(row)

    return {name: values for name, values in grouped.items() if values}, audit


def write_low_power_audit(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    """Write deterministic low-power candidate and assembly decisions."""
    fields = [
        "profile", "query_seed", "input_order", "output_order", "decision", "reason",
        "topic", "scope", "domain", "statement", "source",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def render_low_power_topics(grouped: Mapping[str, list[str]]) -> list[str]:
    """Render selected descriptive topics without adding normative wording."""
    lines: list[str] = []
    for topic, entries in grouped.items():
        lines.append(f"#### {topic}")
        for entry in entries:
            parts = re.split(r"\s+(?=(?:Domain type|Voltage|Control mode|Notes|Functions|Function|Characteristics|Description|Control):)", entry)
            if len(parts) > 1 and ": Included block(s):" in parts[0]:
                domain, included = parts[0].split(": Included block(s):", 1)
                lines.append(f"- Domain: {domain.strip()}")
                included = re.sub(r"\s*,\s*,+", ", ", included).strip(" ,.")
                if included:
                    lines.append(f"- Included blocks: {included}.")
                fields: dict[str, str] = {}
                for part in parts[1:]:
                    label, _, value = part.partition(":")
                    value = re.split(r"\s+-\s+(?=(?:Function|Control|Characteristics):)", value, maxsplit=1)[0]
                    value = re.sub(r"\s+", " ", value)
                    value = re.sub(r"(?:\s*[-.])+$", "", value).strip()
                    if not value or ".." in value or re.search(r"\b(?:next chapter|see)\b", value, re.IGNORECASE):
                        continue
                    normalized_label = {"Function": "Functions", "Control": "Control mode"}.get(label.strip(), label.strip())
                    if normalized_label == "Control mode" and normalized_label in fields:
                        continue
                    fields[normalized_label] = value
                for label in ("Domain type", "Voltage", "Control mode", "Notes", "Functions", "Characteristics", "Description"):
                    value = fields.get(label, "")
                    if value:
                        lines.append(f"- {label}: {value}.")
            else:
                lines.append(f"- {entry}")
        lines.append("")
    return lines
