"""Project-agnostic contracts for generated specification documents."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from collections import Counter
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import yaml


CONTRACT_VERSION = "1.0"
IPOS_DETAIL_POLICY = "functional_detail_v1"

DRS_TEMPLATE = "templates/DRS_gen_AI_template_prompt.md"
DRS_RULES = frozenset({
    "structure", "conventions", "navigation", "table_preservation",
    "technical_prose", "evidence_fidelity", "artifact_fidelity",
})

SHARED_CATEGORY_CONVENTIONS = (
    (
        "Comment",
        "This category denotes that the content of the object text is a general comment. For example, this may be an explanation why the requirement demands certain items when there would also be other possibilities. A comment should not be necessary to understand the related requirements",
    ),
    (
        "Definition",
        "This category is used for the definition of terms, wordings, technical expressions etc. It is a documentation of design decisions and general instructions that belong to the document itself, e.g. owner of the document, structure of the document. It is needed to understand a related requirement. It is not linked to any test case.",
    ),
    (
        "Assumption",
        "This category is used for requirements this document provide upstream to another document, indicating what this IP/block/system needs to work properly.",
    ),
    (
        "Requirement",
        "This category denotes a requirement that has to be implemented and verified. Accordingly, it is necessary to establish traces from the different requirement levels to the test cases for this category.",
    ),
)


def shared_category_conventions_markdown() -> list[str]:
    """Render the shared category definitions used by SRS and DRS."""
    lines: list[str] = []
    for index, (name, definition) in enumerate(SHARED_CATEGORY_CONVENTIONS, start=1):
        lines.extend([f"#### 2.5.{index} {name}", "", definition, ""])
    return lines


def load_drs_contract(template_path: Path) -> dict:
    """Load the sole DRS presentation contract; reject unsupported instructions."""
    text = template_path.read_text(encoding="utf-8")
    blocks = re.findall(r"(?ms)^```yaml drs-document-contract\s*\n(.*?)^```\s*$", text)
    if len(blocks) != 1:
        raise ValueError("DRS requires exactly one embedded YAML document contract")

    class UniqueLoader(yaml.SafeLoader):
        pass

    def unique_mapping(loader, node):
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node)
            if key in result:
                raise ValueError(f"Duplicate DRS contract key: {key}")
            result[key] = loader.construct_object(value_node)
        return result

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
    payload = yaml.load(blocks[0], Loader=UniqueLoader)
    fields = {"version", "document_type", "mandatory_rules", "sections", "conventions", "navigation", "writing"}
    if not isinstance(payload, dict) or set(payload) != fields:
        raise ValueError("Invalid DRS contract fields")
    if type(payload["version"]) is not int or payload["version"] != 1 or payload["document_type"] != "DRS":
        raise ValueError("Unsupported DRS contract version or document type")
    rules = payload["mandatory_rules"]
    if not isinstance(rules, list) or any(not isinstance(rule, str) for rule in rules):
        raise ValueError("Invalid DRS mandatory rules")
    if set(rules) != DRS_RULES or len(rules) != len(DRS_RULES):
        raise ValueError("DRS mandatory rule missing or without implementation")
    for field in ("sections", "navigation"):
        values = payload[field]
        if not isinstance(values, list) or not values or any(not isinstance(value, str) or not value.strip() for value in values) or len(set(values)) != len(values):
            raise ValueError(f"Invalid DRS {field}")
    if [value.split(".", 1)[0] for value in payload["sections"]] != [str(number) for number in range(1, 11)]:
        raise ValueError("Unsupported DRS section renderer or section mapping")
    conventions = payload["conventions"]
    if not isinstance(conventions, dict) or set(conventions) != {"heading", "after", "before", "categories"}:
        raise ValueError("Invalid DRS conventions")
    if (conventions["heading"], conventions["after"], conventions["before"]) != (
        "2.1 Conventions", "2. Definitions and terminology", "3. Top Level Overview"
    ):
        raise ValueError("Unsupported DRS conventions placement")
    categories = conventions["categories"]
    if not isinstance(categories, list) or len(categories) != 4:
        raise ValueError("DRS requires four conventions")
    for category, name in zip(categories, ("Comment", "Definition", "Assumption", "Requirement")):
        if not isinstance(category, dict) or set(category) != {"name", "definition"} or category["name"] != name or not isinstance(category["definition"], str) or not category["definition"].strip():
            raise ValueError("Invalid DRS convention order or definition")
    if payload["writing"] != "evidence_bounded_technical_prose_v1":
        raise ValueError("DRS writing rule without implementation")
    payload["sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return payload


def drs_conventions_markdown(contract: dict) -> list[str]:
    lines = ["### " + contract["conventions"]["heading"], ""]
    for category in contract["conventions"]["categories"]:
        lines.extend(["#### " + category["name"], "", " ".join(category["definition"].split()), ""])
    return lines


def _drs_text(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\s*\{#[^}]+\}", "", value).replace("**", "")
    return " ".join(value.split())


def drs_document_events(path: Path) -> list[dict]:
    """Read actual headings, paragraphs and editable tables, in document order."""
    events = []
    if path.suffix == ".md":
        in_table = False
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("<"):
                in_table = False
                continue
            heading = re.match(r"^(#{1,6})\s+(.+)$", line)
            if heading:
                events.append({"kind": "heading", "level": len(heading[1]), "text": _drs_text(heading[2])})
            elif line.startswith("|"):
                if re.fullmatch(r"[| :\-]+", line):
                    continue
                cells = [_drs_text(cell.replace(r"\|", "|")) for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
                if not in_table:
                    events.append({"kind": "table", "rows": []})
                events[-1]["rows"].append(cells)
                in_table = True
            else:
                events.append({"kind": "paragraph", "text": _drs_text(line)})
            if not line.startswith("|"):
                in_table = False
    else:
        word = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        with zipfile.ZipFile(path) as archive:
            body = ET.fromstring(archive.read("word/document.xml")).find(word + "body")
        if body is None:
            raise ValueError("DOCX body missing")
        for element in body:
            if element.tag == word + "tbl":
                rows = [[_drs_text(" ".join("".join(node.text or "" for node in paragraph.iter(word + "t")) for paragraph in cell.iter(word + "p")))
                         for cell in row.findall(word + "tc")] for row in element.findall(word + "tr")]
                events.append({"kind": "table", "rows": rows})
            elif element.tag == word + "p":
                text = _drs_text("".join(node.text or "" for node in element.iter(word + "t")))
                if not text:
                    continue
                style = element.find(word + "pPr/" + word + "pStyle")
                heading = re.fullmatch(r"Heading([1-6])", style.get(word + "val", ""), re.I) if style is not None else None
                events.append({"kind": "heading", "level": int(heading[1]), "text": text} if heading else {"kind": "paragraph", "text": text})
    return events


def drs_table_inventory(events: list[dict]) -> list[dict]:
    owner = ""
    result = []
    for event in events:
        if event["kind"] == "heading":
            owner = event["text"]
        elif event["kind"] == "table":
            result.append({"owner": owner, "rows": event["rows"]})
    return result


def capture_drs_preservation_baseline(markdown: Path, docx: Path, destination: Path, snapshot_id: str) -> None:
    """Explicit one-time baseline capture; never silently refresh it during generation."""
    payload = {"snapshot_id": snapshot_id, "markdown_sha256": file_sha256(markdown), "docx_sha256": file_sha256(docx)}
    for name, path in (("markdown", markdown), ("docx", docx)):
        payload[name] = drs_table_inventory(drs_document_events(path))
    with destination.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def validate_drs_events(events: list[dict], contract: dict, baseline_tables: list[dict]) -> list[str]:
    findings = []
    headings = [event["text"] for event in events if event["kind"] == "heading"]
    top = [event["text"] for event in events if event["kind"] == "heading" and event["level"] == 2 and re.match(r"^[1-9]\d*\. ", event["text"])]
    if top != contract["sections"]:
        findings.append("structure: top-level section order/content differs from template")
    for title in contract["navigation"]:
        if headings.count(title) != 1:
            findings.append(f"navigation: missing or duplicate {title}")
    toc_start = next((index for index, event in enumerate(events) if event.get("text") == "0.1 Table of contents" and event["kind"] == "heading"), None)
    toc_end = next((index for index, event in enumerate(events) if event.get("text") == "0.2 Internal index for paragraphs and pages" and event["kind"] == "heading"), None)
    if toc_start is None or toc_end is None or toc_start >= toc_end:
        findings.append("navigation: invalid TOC placement")
    else:
        entries = {re.sub(r"^-\s+", "", event.get("text", "")) for event in events[toc_start + 1:toc_end]}
        expected_entries = {title for title in headings if re.match(r"^[1-9]\d*\.", title)}
        for title in sorted(expected_entries - entries):
            findings.append(f"navigation: TOC entry missing: {title}")
    conventions = contract["conventions"]
    positions = [index for index, event in enumerate(events) if event["kind"] == "heading" and event["text"] == conventions["heading"]]
    if len(positions) != 1:
        findings.append("conventions: missing or duplicate Conventions")
    else:
        position = positions[0]
        prior_headings = [event["text"] for event in events[:position] if event["kind"] == "heading"]
        if not prior_headings or prior_headings[-1] != conventions["after"]:
            findings.append("conventions: must be the first subsection under Definitions and terminology")
        expected = []
        for category in conventions["categories"]:
            expected.extend([{"kind": "heading", "level": 4, "text": category["name"]}, {"kind": "paragraph", "text": _drs_text(category["definition"])}])
        actual = events[position + 1:position + 1 + len(expected)]
        if actual != expected:
            findings.append("conventions: category content/order differs from template")
        following = events[position + 1 + len(expected):position + 2 + len(expected)]
        if not following or following[0].get("text") != conventions["before"] or following[0]["kind"] != "heading":
            findings.append("conventions: must end before the next top-level section")
        parent = next((event for event in reversed(events[:position]) if event["kind"] == "heading" and event["level"] == 2), None)
        if events[position]["level"] != 3 or not parent or parent["text"] != conventions["after"]:
            findings.append("conventions: 2.1 must be a subsection of Definitions and terminology")
    for category in conventions["categories"]:
        if sum(event.get("text") == _drs_text(category["definition"]) for event in events) != 1:
            findings.append(f"conventions: missing or duplicate definition {category['name']}")
    actual_tables = drs_table_inventory(events)
    remaining = Counter(stable_payload_hash(table) for table in actual_tables)
    for table in baseline_tables:
        if table["owner"] == "Table 3. Section navigation index":
            candidates = [item for item in actual_tables if item["owner"] == table["owner"]]
            def normalize_navigation_row(row):
                if row and row[0] == "3. System context for digital behavior":
                    return ["3. Top Level Overview", *row[1:]]
                return row
            expected_rows = [normalize_navigation_row(row) for row in table["rows"]]
            actual_rows = [normalize_navigation_row(row) for row in candidates[0]["rows"]] if len(candidates) == 1 else []
            if len(candidates) != 1 or any(row not in actual_rows for row in expected_rows):
                findings.append("navigation: existing index rows removed or changed")
            continue
        key = stable_payload_hash(table)
        if remaining[key] < 1:
            findings.append(f"table_preservation: table changed or missing under {table['owner']}")
        else:
            remaining[key] -= 1
    navigation_tables = [table for table in actual_tables if table["owner"] == "Table 3. Section navigation index"]
    if not navigation_tables or not any(row[0] == conventions["heading"] and row[1] == "2.1" for row in navigation_tables[0]["rows"] if len(row) > 1):
        findings.append("navigation: 2.1 Conventions missing from internal index")
    if navigation_tables:
        numbers = [tuple(int(part) for part in row[1].split(".")) for row in navigation_tables[0]["rows"]
                   if len(row) > 1 and re.fullmatch(r"\d+(?:\.\d+)*", row[1])]
        if numbers != sorted(numbers):
            findings.append("navigation: internal index is not in numerical order")
    from workflow_routing import drs_section_prose_findings
    active = ""
    phase = 0
    for event in events:
        if event["kind"] == "heading":
            match = re.match(r"^(\d+(?:\.\d+)*)\.?\s", event["text"])
            if match:
                active = match[1]
            phase = 0
            continue
        if active not in {"1.2", "3", "3.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "7"}:
            continue
        if event["kind"] == "table":
            if phase == 2:
                findings.append(f"technical_prose: {active}: table after clarification")
            phase = max(phase, 1)
            continue
        text = event["text"]
        findings.extend(f"technical_prose: {active}: {item}" for item in drs_section_prose_findings(text))
        if re.search(r"\[(?:TO:|Vpriority|[A-Z]+[_-]REQ)|:\s*[•]\s*|(?:->.*){2,}", text):
            findings.append(f"technical_prose: {active}: raw snippet or path concatenation")
        if "need clarification" in text.casefold() or "requiring clarification" in text.casefold():
            phase = 2
        elif not text.endswith(":"):
            if phase:
                findings.append(f"technical_prose: {active}: known behavior must precede tables and clarification")
    return list(dict.fromkeys(findings))


def arrange_drs_contract_lines(lines: list[str], contract: dict) -> list[str]:
    """Arrange existing semantic content without altering technical evidence or tables."""
    context_start = next((index for index, line in enumerate(lines) if line.startswith("## 6.4 ")), None)
    if context_start is not None:
        context_end = next(index for index in range(context_start + 1, len(lines)) if lines[index].startswith("## 10. "))
        context = ["#" + line if line.startswith(("## ", "### ")) else line for line in lines[context_start:context_end]]
        del lines[context_start:context_end]
        insertion = next(index for index, line in enumerate(lines) if line.startswith("## 7. "))
        lines[insertion:insertion] = context
    starts = [index for index, line in enumerate(lines) if re.match(r"^## [1-9]\d*\. ", line)]
    chunks = {re.match(r"^## (\d+)\.", lines[start])[1]: lines[start:end] for start, end in zip(starts, starts[1:] + [len(lines)])}
    ordered = lines[:starts[0]]
    for title in contract["sections"]:
        number = title.split(".", 1)[0]
        if number not in chunks:
            raise ValueError(f"DRS section has no renderer: {title}")
        chunk = chunks.pop(number)
        chunk[0] = "## " + title
        ordered.extend(chunk)
    if chunks:
        raise ValueError("DRS contract omits implemented sections")
    result = []
    active = ""
    chunk = []

    def flush():
        if active not in {"1.2", "3", "3.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "7"}:
            result.extend(chunk)
            return
        known, tables, clarifications = [], [], []
        for line in chunk:
            if not line.strip():
                tables.append("")
                continue
            if line.startswith("|") or line.endswith(":"):
                tables.append(line)
            elif "need clarification" in line.casefold() or "requiring clarification" in line.casefold():
                clarifications.append(line)
            else:
                known.append(line)
        result.extend(known + [""] + tables + [""] + clarifications + [""])

    for line in ordered:
        if line.startswith("#"):
            flush()
            chunk = []
            result.append(line)
            match = re.match(r"^#+ (\d+(?:\.\d+)*)\.?\s", line)
            if match:
                active = match[1]
        else:
            chunk.append(line)
    flush()
    return result


def validate_drs_document_contract(repo_root: Path, *, check_metadata: bool = True) -> list[str]:
    """Shared final-artifact gate, called by DRS crosscheck and central coherence."""
    root = repo_root / "artifacts/stage5_drs"
    try:
        contract = load_drs_contract(repo_root / DRS_TEMPLATE)
        baseline_path = root / "drs_preservation_baseline.json"
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        findings = []
        for kind, suffix in (("markdown", ".md"), ("docx", ".docx")):
            path = root / ("digital_requirements_specification" + suffix)
            events = drs_document_events(path)
            findings.extend(f"{kind}: {finding}" for finding in validate_drs_events(events, contract, baseline[kind]))
            snapshots = [event["text"].split("Snapshot ID:", 1)[1].strip() for event in events if event.get("text", "").startswith("Snapshot ID:")]
            if snapshots != [baseline["snapshot_id"]]:
                findings.append(f"{kind}: preservation baseline snapshot mismatch")
        markdown_path = root / "digital_requirements_specification.md"
        markdown = markdown_path.read_text(encoding="utf-8")
        anchors = set(re.findall(r"\{#([^}]+)\}", markdown))
        targets = set(re.findall(r"\]\(#([^)]+)\)", markdown))
        if targets - anchors:
            findings.append("navigation: unresolved Markdown internal targets")
        docx_path = markdown_path.with_suffix(".docx")
        word = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        with zipfile.ZipFile(docx_path) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))
        bookmarks = {node.get(word + "name") for node in document.iter(word + "bookmarkStart")}
        docx_targets = {node.get(word + "anchor") for node in document.iter(word + "hyperlink") if node.get(word + "anchor")}
        if docx_targets - bookmarks:
            findings.append("navigation: unresolved DOCX internal targets")
        from workflow_routing import validate_ipos_docx_layout
        findings.extend(validate_ipos_docx_layout(docx_path))
        if check_metadata:
            metadata = json.loads((root / "drs_document_contract.json").read_text(encoding="utf-8"))
            expected = drs_contract_metadata(repo_root, contract)
            if metadata != expected:
                findings.append("artifact_fidelity: contract metadata or final artifact hash mismatch")
        return findings
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError, zipfile.BadZipFile, yaml.YAMLError) as exc:
        return [f"document_contract: {exc}"]


def drs_contract_metadata(repo_root: Path, contract: dict) -> dict:
    root = repo_root / "artifacts/stage5_drs"
    return {
        "version": contract["version"], "template_sha256": contract["sha256"],
        "preservation_baseline_sha256": file_sha256(root / "drs_preservation_baseline.json"),
        "markdown_sha256": file_sha256(root / "digital_requirements_specification.md"),
        "docx_sha256": file_sha256(root / "digital_requirements_specification.docx"),
        "rules": {rule: "PASS" for rule in contract["mandatory_rules"]},
    }

def resolve_ipos_description_policy(repo_root: Path, snapshot_id: str, kind: str, block: str) -> str:
    """Resolve a presentation-only pilot without changing approved scope or ownership."""
    path = repo_root / "config/ipos_description_pilots.json"
    if not path.exists():
        return "legacy"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or set(payload) != {"version", "pilots"} or payload["version"] != 1:
        raise ValueError("Invalid IPOS description pilot configuration")
    pilots = payload["pilots"]
    if not isinstance(pilots, list):
        raise ValueError("IPOS description pilots must be a list")
    identities = set()
    selected = "legacy"
    for pilot in pilots:
        if not isinstance(pilot, dict) or set(pilot) != {"snapshot_id", "kind", "block", "policy"}:
            raise ValueError("Invalid IPOS description pilot selector")
        if any(not isinstance(value, str) or not value.strip() for value in pilot.values()):
            raise ValueError("IPOS description pilot selectors must be nonempty strings")
        if pilot["kind"] not in {"digital", "analog"} or pilot["policy"] != IPOS_DETAIL_POLICY:
            raise ValueError("Unsupported IPOS description pilot policy or domain")
        identity = (pilot["snapshot_id"], pilot["kind"], pilot["block"])
        if identity in identities:
            raise ValueError("Duplicate IPOS description pilot selector")
        identities.add(identity)
        if identity == (snapshot_id, kind, block):
            selected = pilot["policy"]
    return selected


@dataclass(frozen=True)
class DocumentTypeContract:
    """Authority and projection boundary for one generated document type."""

    key: str
    authority_sources: tuple[str, ...]
    discovery_sources: tuple[str, ...]
    abstraction_level: str
    ownership_scope: str
    required_sections: tuple[str, ...]
    promotion_rule: str
    suppression_rule: str


DOCUMENT_TYPE_CONTRACTS: Mapping[str, DocumentTypeContract] = {
    "SRS": DocumentTypeContract(
        key="SRS",
        authority_sources=("approved system-scoped snapshot requirements",),
        discovery_sources=("approved vocabulary and structural context",),
        abstraction_level="system behavior and externally observable capability",
        ownership_scope="system",
        required_sections=("requirements", "traceability"),
        promotion_rule="retain only approved system-owned content",
        suppression_rule="suppress architecture implementation and block-local detail",
    ),
    "ARS": DocumentTypeContract(
        key="ARS",
        authority_sources=("approved analog or mixed-signal snapshot requirements",),
        discovery_sources=("approved interface and architecture context",),
        abstraction_level="analog and mixed-signal architecture",
        ownership_scope="top analog and analog integration",
        required_sections=("requirements", "traceability"),
        promotion_rule="retain only approved analog or mixed-signal architecture content",
        suppression_rule="suppress system-only and unrelated block-local detail",
    ),
    "DRS": DocumentTypeContract(
        key="DRS",
        authority_sources=("approved top-digital and digital-integration snapshot requirements",),
        discovery_sources=("approved interface and architecture context",),
        abstraction_level="top-digital architecture and integration",
        ownership_scope="top digital and digital integration",
        required_sections=("requirements", "traceability"),
        promotion_rule="retain only approved top-digital or integration content",
        suppression_rule="suppress system-only and block-local implementation detail",
    ),
    "IPOS": DocumentTypeContract(
        key="IPOS",
        authority_sources=(
            "approved block inventory function and I/O",
            "approved same-block snapshot requirements",
        ),
        discovery_sources=("complete snapshot-scoped candidate requirement set",),
        abstraction_level="block-local purpose, capability, interface, and requirement detail",
        ownership_scope="one approved concrete block",
        required_sections=("functionality", "supported_functions_and_scope", "source_io", "requirements"),
        promotion_rule="retain supported same-block content within the approved block function and I/O boundary",
        suppression_rule="suppress cross-scope, conflicting, unsupported, table-only, signal-only, and non-projectable normative candidates",
    ),
}


def _json_compatible(value: object) -> object:
    return json.loads(json.dumps(value, sort_keys=True, ensure_ascii=True))


@dataclass(frozen=True)
class NormalizedSourceRecord:
    """One classified input candidate, including retained or suppressed rationale."""

    record_id: str
    text: str
    authority_tier: str
    ownership_scope: str
    provenance: tuple[str, ...]
    decision: str
    rationale: str


@dataclass(frozen=True)
class SemanticUnit:
    """One ordered semantic unit emitted by a deterministic composer."""

    unit_id: str
    section: str
    text: str
    source_record_ids: tuple[str, ...]
    output_order: int


def stable_payload_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_record_hash(records: Sequence[NormalizedSourceRecord]) -> str:
    return stable_payload_hash([asdict(record) for record in records])


def write_materialization_audit(
    path: Path,
    document_type: str,
    records: Sequence[NormalizedSourceRecord],
    units: Sequence[SemanticUnit],
    markdown_path: Path,
    docx_path: Path,
) -> None:
    """Record the approved-input-to-final-artifact chain after post-processing."""
    contract = DOCUMENT_TYPE_CONTRACTS[document_type]
    payload = {
        "contract_version": CONTRACT_VERSION,
        "document_type": document_type,
        "document_contract": asdict(contract),
        "normalized_input_sha256": normalized_record_hash(records),
        "normalized_records": [asdict(record) for record in records],
        "semantic_units": [asdict(unit) for unit in units],
        "markdown": {"path": markdown_path.name, "sha256": file_sha256(markdown_path)},
        "docx": {"path": docx_path.name, "sha256": file_sha256(docx_path)},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _normalized_text(value: str) -> str:
    without_bold_markup = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    return re.sub(r"\s+", " ", without_bold_markup).strip().casefold()


def docx_body_text(docx_path: Path) -> str:
    """Extract final DOCX body text without depending on the composer or renderer."""
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with zipfile.ZipFile(docx_path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    paragraphs = []
    for paragraph in root.iter(f"{namespace}p"):
        paragraphs.append("".join(node.text or "" for node in paragraph.iter(f"{namespace}t")))
    return "\n".join(paragraphs)


def validate_materialization_chain(
    audit_path: Path,
    document_type: str,
    expected_records: Sequence[NormalizedSourceRecord],
    markdown_path: Path,
    docx_path: Path,
) -> list[str]:
    """Independently validate normalized inputs, audit, Markdown, and final DOCX."""
    findings: list[str] = []
    if not audit_path.exists():
        return [f"{audit_path.name}: materialization audit is missing"]
    if not markdown_path.exists() or not docx_path.exists():
        return [f"{audit_path.name}: audited Markdown or DOCX artifact is missing"]
    try:
        payload = json.loads(audit_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"{audit_path.name}: invalid materialization audit: {exc}"]
    if payload.get("contract_version") != CONTRACT_VERSION:
        findings.append(f"{audit_path.name}: contract version mismatch")
    if payload.get("document_type") != document_type:
        findings.append(f"{audit_path.name}: document type mismatch")
    if payload.get("document_contract") != _json_compatible(asdict(DOCUMENT_TYPE_CONTRACTS[document_type])):
        findings.append(f"{audit_path.name}: document contract mismatch")
    expected_hash = normalized_record_hash(expected_records)
    if payload.get("normalized_input_sha256") != expected_hash:
        findings.append(f"{audit_path.name}: normalized input fingerprint mismatch")
    if payload.get("normalized_records") != _json_compatible([asdict(record) for record in expected_records]):
        findings.append(f"{audit_path.name}: normalized input records differ from approved inputs")
    if payload.get("markdown", {}).get("sha256") != file_sha256(markdown_path):
        findings.append(f"{markdown_path.name}: content changed after audited materialization")
    if payload.get("docx", {}).get("sha256") != file_sha256(docx_path):
        findings.append(f"{docx_path.name}: content changed after audited post-processing")

    units = payload.get("semantic_units") or []
    expected_order = list(range(1, len(units) + 1))
    if [unit.get("output_order") for unit in units] != expected_order:
        findings.append(f"{audit_path.name}: semantic unit order is incomplete or unstable")
    record_by_id = {record.record_id: record for record in expected_records}
    represented_record_ids = {
        str(source_id)
        for unit in units
        for source_id in (unit.get("source_record_ids") or ())
    }
    missing_retained = [
        record.record_id
        for record in expected_records
        if record.decision == "retained" and record.record_id not in represented_record_ids
    ]
    if missing_retained:
        findings.append(
            f"{audit_path.name}: retained normalized inputs lack semantic units: "
            + ", ".join(missing_retained)
        )
    markdown = _normalized_text(markdown_path.read_text(encoding="utf-8", errors="replace"))
    docx = _normalized_text(docx_body_text(docx_path))
    markdown_position = -1
    docx_position = -1
    for unit in units:
        unit_id = str(unit.get("unit_id") or "").strip()
        unit_text = _normalized_text(str(unit.get("text") or ""))
        source_ids = tuple(unit.get("source_record_ids") or ())
        if not unit_id or not unit_text or not source_ids:
            findings.append(f"{audit_path.name}: semantic unit lacks identity, text, or provenance")
            continue
        if any(source_id not in record_by_id for source_id in source_ids):
            findings.append(f"{audit_path.name}: semantic unit references an unknown source record")
        if any(record_by_id[source_id].decision == "suppressed" for source_id in source_ids if source_id in record_by_id):
            findings.append(f"{audit_path.name}: semantic unit promotes a suppressed source record")
        next_markdown_position = markdown.find(unit_text, markdown_position + 1)
        next_docx_position = docx.find(unit_text, docx_position + 1)
        if next_markdown_position < 0:
            findings.append(f"{markdown_path.name}: selected semantic unit missing or reordered: {unit_id}")
        else:
            markdown_position = next_markdown_position
        if next_docx_position < 0:
            findings.append(f"{docx_path.name}: selected semantic unit missing or reordered: {unit_id}")
        else:
            docx_position = next_docx_position
    retained_texts = {
        _normalized_text(record.text)
        for record in expected_records
        if record.decision == "retained" and record.text
    }
    for record in expected_records:
        normalized_record_text = _normalized_text(record.text)
        suppressed_tokens = re.findall(r"[a-z0-9]+", normalized_record_text)
        if (
            record.decision == "suppressed"
            and normalized_record_text
            and len(suppressed_tokens) >= 2
            and len(normalized_record_text) >= 16
            and normalized_record_text not in retained_texts
            and normalized_record_text in markdown
        ):
            findings.append(f"{markdown_path.name}: suppressed source content was rendered: {record.record_id}")
    return findings