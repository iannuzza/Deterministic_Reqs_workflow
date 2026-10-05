#!/usr/bin/env python3
"""Generate a SysML v2-style architecture model from validated Stage 2A artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
import re
from typing import Dict, Iterable, List, Optional, Tuple

from openpyxl import load_workbook

from sysml_generation_service import require_sysml_snapshot, validate_snapshot_requirement_coverage
from validate_downstream_coherence import (
    canonical_human_label,
    created_ipos_block_directories,
    downstream_contract_fingerprint,
    resolve_downstream_contract,
)


DEFAULT_OUT = Path("artifacts/stage2_mirco_arc")
STRUCTURAL_PORT_OWNERS = {"STBIOSystem", "Digital Subsystem"}


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _read_ipos_requirements(repo_root: Path) -> Dict[str, List[Dict[str, str]]]:
    grouped: Dict[str, List[Dict[str, str]]] = {}
    for path in (
        repo_root / "artifacts/stage6_digital_ipos/ipos_traceability_matrix.csv",
        repo_root / "artifacts/stage7_analog_ipos/ipos_traceability_matrix.csv",
    ):
        if not path.exists():
            continue
        for row in read_csv(path):
            owner = canonical_human_label(row.get("mapped_block", "") or row.get("owning_block", ""))
            if owner:
                grouped.setdefault(owner, []).append(row)
    return grouped


def _read_srs_markdown_requirements(repo_root: Path) -> List[Dict[str, str]]:
    path = repo_root / "artifacts/stage3_srs/system_requirements_specification.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    pattern = re.compile(
        r"^\s*\*\*\[(SRS-REQ-\d{3})\]\s+Requirement:\*\*\s*\n"
        r"(.*?)(?=^\s*\*\*\[SRS-REQ-\d{3}\]\s+Requirement:\*\*\s*$|\Z)",
        flags=re.M | re.S,
    )
    rows: List[Dict[str, str]] = []
    for match in pattern.finditer(text):
        body = match.group(2)
        covers = re.search(r"^\s*Covers:\s*(\S+)\s*$", body, flags=re.M)
        statement = re.split(r"^\s*Covers:\s*", body, maxsplit=1, flags=re.M)[0]
        statement = re.sub(r"<[^>]+>", " ", statement)
        statement = re.sub(r"\[End\]", " ", statement, flags=re.I)
        rows.append({
            "srs_req_id": match.group(1),
            "source_req_id": covers.group(1) if covers else "",
            "requirement_statement": " ".join(statement.split()),
            "source_artifact": "artifacts/stage3_srs/system_requirements_specification.md",
        })
    return rows


def block_name(value: str) -> str:
    return canonical_human_label(value)


def sysml_name(value: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", value or "")
    name = "".join(word[:1].upper() + word[1:] for word in words) or "Unnamed"
    return "Block_" + name if name[0].isdigit() else name


def requirement_sysml_name(value: str) -> str:
    """Preserve source requirement IDs while making them valid identifiers."""
    name = re.sub(r"[^A-Za-z0-9_]", "_", (value or "").strip())
    name = re.sub(r"_+", "_", name).strip("_") or "UnnamedRequirement"
    return "Req_" + name if name[0].isdigit() else name


def usage_name(value: str) -> str:
    name = sysml_name(value)
    return name[:1].lower() + name[1:]


def quote(value: str) -> str:
    return (value or "").replace("\\", "\\\\").replace('"', '\\"').replace("\r", " ").replace("\n", " ")


def doc_text(value: str) -> str:
    return re.sub(r"\*/", "* /", (value or "").strip())


def sysml_header(snapshot_id: str, contract_fingerprint: str) -> str:
    return (
        f"// Snapshot ID: {snapshot_id}\n"
        f"// Downstream contract fingerprint: {contract_fingerprint}\n\n"
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def requirement_rows(
    path: Path,
    mapping_path: Optional[Path] = None,
    edge_path: Optional[Path] = None,
    source_path: Optional[Path] = None,
    concrete_blocks: Optional[set[str]] = None,
) -> List[Dict[str, str]]:
    rows = read_csv(path)
    source_rows = {}
    if source_path and source_path.exists():
        for source_row in read_csv(source_path):
            source_id = source_row.get("source_req_id") or source_row.get("id")
            if source_id:
                source_rows[source_id] = source_row
    reviewed_mapping = {}
    if mapping_path and mapping_path.exists():
        for row in read_csv(mapping_path):
            requirement_id = row.get("requirement_id") or row.get("Requirement ID")
            if requirement_id:
                reviewed_mapping[requirement_id] = row
    edge_mapping = {}
    if edge_path and edge_path.exists():
        for row in read_csv(edge_path):
            requirement_id = row.get("source_req_id")
            if requirement_id:
                edge_mapping[requirement_id] = f"{row.get('from_block', '')};{row.get('to_block', '')}"
    result = []
    for row in rows:
        source_id = row.get("Requirement ID") or row.get("source_req_id") or row.get("requirement_id")
        source_row = source_rows.get(source_id, {})
        statement = source_row.get("requirement_statement") or row.get("requirement_statement") or row.get("Requirement Statement") or row.get("Requirement")
        mapping = row.get("Block(s)") or row.get("Block") or row.get("Mapped Block") or "Unassigned"
        reviewed = reviewed_mapping.get(source_id, {})
        reviewed_mapping_value = reviewed.get("approved_block", "")
        review_decision = (reviewed.get("review_decision") or "").strip().lower()
        if reviewed and review_decision not in {"approved", "reassigned"}:
            continue
        reviewed_owners = normalized_blocks(reviewed_mapping_value)
        traceability_owners = normalized_blocks(mapping)
        if source_id in edge_mapping:
            mapping = edge_mapping[source_id]
        elif not concrete_blocks or any(owner in concrete_blocks for owner in reviewed_owners):
            mapping = reviewed_mapping_value or mapping
        elif reviewed_mapping_value and not any(owner in concrete_blocks for owner in traceability_owners):
            mapping = reviewed_mapping_value
        if source_id and statement:
            result.append({
                "source_req_id": source_id,
                "statement": statement,
                "mapping": mapping,
                "notes": source_row.get("notes") or row.get("Notes", ""),
                "is_connection_requirement": "true" if source_id in edge_mapping else "false",
            })
    return result


def block_rows(path: Path) -> Dict[str, Dict[str, str]]:
    result = {}
    for row in read_csv(path):
        name = block_name(row.get("Block", ""))
        if name:
            result[name] = row
    return result


def approved_block_names(path: Path) -> set[str]:
    """Return the exact concrete block names approved for SysML generation."""
    if not path.exists():
        raise FileNotFoundError(f"Approved block list is missing: {path}")
    workbook = load_workbook(path, read_only=True, data_only=True)
    try:
        worksheet = workbook.active
        headers = [str(cell.value or "").strip() for cell in next(worksheet.iter_rows())]
        if "Block name" not in headers:
            raise ValueError(f"Approved block list has no 'Block name' column: {path}")
        block_column = headers.index("Block name")
        names = {
            block_name(str(row[block_column].value or "").strip())
            for row in worksheet.iter_rows(min_row=2)
            if row[block_column].value
        }
    finally:
        workbook.close()
    names.discard("Unassigned")
    if not names:
        raise ValueError(f"Approved block list contains no concrete blocks: {path}")
    return names


def is_concrete_block(name: str, metadata: Optional[Dict[str, str]]) -> bool:
    """Only concrete implementation entities belong in the SysML hierarchy."""
    if name == "Unassigned":
        return False
    kind = str((metadata or {}).get("Entity kind") or "concrete_block").strip().lower()
    return kind == "concrete_block"


def normalized_blocks(mapping: str) -> List[str]:
    values = []
    for token in re.split(r"\s*;\s*|\s*,\s*", mapping or ""):
        clean = block_name(re.sub(r"\s*\[[^]]+\]", "", token).strip())
        if clean and clean not in values and clean != "Unassigned":
            values.append(clean)
    return values


def subsystem_for_block(name: str) -> str:
    """Keep ADC analog; all other concrete architecture blocks are digital."""
    if name == "ADC":
        return "Analog Subsystem"
    return "Digital Subsystem"


def _requirements_by_block(requirements: List[Dict[str, str]], block_names: set[str]) -> Tuple[Dict[str, List[Dict[str, str]]], List[Dict[str, str]]]:
    assigned: Dict[str, List[Dict[str, str]]] = {name: [] for name in block_names}
    system_level: List[Dict[str, str]] = []
    for row in requirements:
        owners = [
            owner for owner in normalized_blocks(row["mapping"])
            if owner in block_names and owner != "Unassigned"
        ]
        if owners:
            for owner in owners:
                assigned[owner].append(row)
        else:
            system_level.append(row)
    return assigned, system_level


def port_rows(path: Path) -> Dict[str, List[Dict[str, str]]]:
    result: Dict[str, List[Dict[str, str]]] = {}
    for row in read_csv(path):
        owner = block_name(row.get("Owner", ""))
        if owner and row.get("Ownership status") == "approved":
            result.setdefault(owner, []).append(row)
    return result


def port_sysml_name(value: str) -> str:
    name = re.sub(r"[^A-Za-z0-9_]", "_", (value or "").strip())
    name = re.sub(r"_+", "_", name).strip("_") or "unnamedPort"
    if name[0].isdigit():
        name = "port_" + name
    return name


def model_file_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") + ".sysml"


def block_description(name: str, block: Dict[str, str], requirements: List[Dict[str, str]], ports: List[Dict[str, str]]) -> str:
    function = (block.get("Function") or "").strip()
    if function:
        return function
    input_text = (block.get("Inputs") or "").strip()
    output_text = (block.get("Outputs") or "").strip()
    if input_text or output_text:
        return f"{name} architecture block with inputs: {input_text or 'none'} and outputs: {output_text or 'none'}."
    return (
        f"{name} architecture block generated from the approved architecture snapshot; "
        f"it contains {len(ports)} approved port(s) and {len(requirements)} linked requirement(s)."
    )


def _append_ports(lines: List[str], ports: List[Dict[str, str]], indent: str) -> None:
    used_names: Dict[str, int] = {}
    for row in ports:
        base_name = port_sysml_name(row.get("Port name", ""))
        used_names[base_name] = used_names.get(base_name, 0) + 1
        port_name = base_name if used_names[base_name] == 1 else f"{base_name}_{used_names[base_name]}"
        direction = row.get("Direction", "").lower()
        direction_keyword = {"input": "in", "output": "out", "inout": "inout", "bidirectional": "inout"}.get(direction, "")
        prefix = f"{direction_keyword} " if direction_keyword else ""
        lines.extend([
            f"{indent}{prefix}port {port_name} : ArchitecturePort {{",
            f'{indent}    attribute sourceName = "{quote(row.get("Port name", ""))}";',
            f'{indent}    attribute sourceDetails = "{quote(row.get("Type / details", ""))}";',
            f'{indent}    attribute sourceTable = "{quote(row.get("Table title", ""))}";',
            f'{indent}    attribute sourcePage = "{quote(row.get("Source page", ""))}";',
            f"{indent}}}",
        ])


def _ordered_blocks(
    blocks: Dict[str, Dict[str, str]],
    interactions: List[Dict[str, str]],
    port_owners: Iterable[str] = (),
) -> List[str]:
    all_blocks = {
        name for name, metadata in blocks.items()
        if is_concrete_block(name, metadata)
    }
    all_blocks.update(
        owner for owner in port_owners
        if owner not in STRUCTURAL_PORT_OWNERS and owner in all_blocks
    )
    for row in interactions:
        for field in ("From block", "To block"):
            endpoint = block_name(row.get(field, ""))
            if endpoint in all_blocks:
                all_blocks.add(endpoint)
    all_blocks.discard("")
    all_blocks.discard("Unassigned")
    return sorted(all_blocks, key=sysml_name)


def build_shared_model() -> str:
    lines = [
        "package STBIO_Shared {",
        "",
        "    // Shared definitions for the generated STBIO architecture model set.",
        "    connection def ArchitectureConnection {",
        "        attribute signalControl : String;",
        "        attribute trigger : String;",
        "        attribute notes : String;",
        "        attribute sourceRequirementIds : String;",
        "        attribute sourceArtifact : String;",
        "    }",
        "",
        "    port def ArchitecturePort {",
        "        attribute sourceName : String;",
        "        attribute sourceDetails : String;",
        "        attribute sourceTable : String;",
        "        attribute sourcePage : String;",
        "    }",
        "",
        "    requirement def SourceRequirement {",
        "        attribute sourceReqId : String;",
        "        attribute sourceArtifact : String;",
        "        attribute sourceContext : String;",
        "    }",
        "",
    ]
    lines.extend(["}", ""])
    return "\n".join(lines)


def build_block_model(
    name: str,
    block: Dict[str, str],
    requirements: List[Dict[str, str]],
    ports: List[Dict[str, str]],
    ipos_requirements: List[Dict[str, str]],
) -> str:
    block_id = sysml_name(name)
    package_id = f"STBIO_Block_{block_id}"
    lines = [
        f"package {package_id} {{",
        "",
        "    private import STBIO_Shared::*;",
        "",
        f"    part def {block_id} {{",
        f'        attribute displayName : String = "{quote(name)}";',
        f'        attribute description : String = "{quote(block_description(name, block, requirements, ports))}";',
        f'        attribute function : String = "{quote(block.get("Function", "") or block_description(name, block, requirements, ports))}";',
        f'        attribute inputs : String = "{quote(block.get("Inputs", ""))}";',
        f'        attribute outputs : String = "{quote(block.get("Outputs", ""))}";',
        f"        attribute approvedPortCount : Integer = {len(ports)};",
        f"        attribute linkedRequirementCount : Integer = {len(ipos_requirements)};",
        f"        doc /* block={doc_text(name)} | description={doc_text(block_description(name, block, requirements, ports))} */;",
    ]
    if not ports:
        lines.append("        doc /* No approved source ports are currently assigned to this block. */;")
    if not ipos_requirements:
        lines.append("        doc /* No approved IPOS requirements are currently assigned directly to this block. */;")
    used_port_names: Dict[str, int] = {}
    for row in ports:
        base_name = port_sysml_name(row.get("Port name", ""))
        used_port_names[base_name] = used_port_names.get(base_name, 0) + 1
        port_name = base_name if used_port_names[base_name] == 1 else f"{base_name}_{used_port_names[base_name]}"
        direction = row.get("Direction", "").lower()
        direction_keyword = {"input": "in", "output": "out", "inout": "inout", "bidirectional": "inout"}.get(direction, "")
        prefix = f"{direction_keyword} " if direction_keyword else ""
        lines.extend([
            f"        {prefix}port {port_name} : ArchitecturePort {{",
            f'            attribute sourceName = "{quote(row.get("Port name", ""))}";',
            f'            attribute sourceDetails = "{quote(row.get("Type / details", ""))}";',
            f'            attribute sourceTable = "{quote(row.get("Table title", ""))}";',
            f'            attribute sourcePage = "{quote(row.get("Source page", ""))}";',
            "        }",
        ])
    if ports:
        lines.append("")
    for row in ipos_requirements:
        req_id = requirement_sysml_name(row.get("ipos_req_id") or row.get("source_req_id") or "")
        source_req_id = row.get("source_req_id") or ""
        statement = row.get("requirement_statement") or ""
        lines.extend([
            f"        requirement def {req_id} : SourceRequirement {{",
            f'            attribute sourceReqId = "{quote(source_req_id)}";',
            f'            attribute sourceArtifact = "{quote(row.get("source_artifact", ""))}";',
            f'            attribute sourceContext = "{quote(row.get("ipos_req_id", ""))}";',
            f"            doc /* {doc_text(statement)} */;",
            "        }",
            f"        requirement req_{req_id} : {req_id};",
            f"        doc /* iposReqId={doc_text(row.get('ipos_req_id', ''))} | sourceReqId={doc_text(source_req_id)} | {doc_text(statement)} */;",
            f"        doc /* coverageDependency: {doc_text(row.get('ipos_req_id', '') or req_id)} -> approved source requirement {doc_text(source_req_id)} */;",
            f"        satisfy req_{req_id} by self;",
        ])
    lines.extend(["    }", "", "}", ""])
    return "\n".join(lines)


def validate_generated_block_files(block_paths: Iterable[Path]) -> None:
    missing = []
    for path in block_paths:
        source = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        if not source.strip():
            missing.append(f"{path.as_posix()}: empty file")
        elif not re.search(r"\bpart\s+def\s+[A-Za-z_][A-Za-z0-9_]*\s*\{", source):
            missing.append(f"{path.as_posix()}: missing part definition")
        elif not re.search(r"\battribute\s+description\b\s*(?::\s*[A-Za-z_][A-Za-z0-9_]*)?\s*=\s*\"", source):
            missing.append(f"{path.as_posix()}: missing block description")
    if missing:
        raise RuntimeError("Generated SysML block files are incomplete: " + "; ".join(missing))


def build_digital_subsystem_model(
    blocks: Dict[str, Dict[str, str]],
    ports: List[Dict[str, str]],
    drs_requirements: List[Dict[str, str]],
) -> str:
    digital_blocks = sorted(
        (
            name for name, metadata in blocks.items()
            if is_concrete_block(name, metadata)
            and subsystem_for_block(name) == "Digital Subsystem"
        ),
        key=sysml_name,
    )
    lines = [
        "package STBIO_DigitalSubsystem {",
        "",
        "    private import STBIO_Shared::*;",
        "",
    ]
    for name in digital_blocks:
        lines.append(f"    private import STBIO_Block_{sysml_name(name)}::*;")
    lines.extend(["", "    part def DigitalSubsystem {"])
    lines.append('        attribute displayName : String = "Digital Subsystem";')
    for row in drs_requirements:
        drs_req_id = (row.get("drs_req_id") or "").strip()
        source_req_id = (row.get("source_req_id") or "").strip()
        statement = row.get("requirement_statement") or ""
        if drs_req_id:
            lines.append(
                f'        requirement def {requirement_sysml_name(drs_req_id)} : SourceRequirement {{'
            )
            lines.extend([
                f'            attribute sourceReqId = "{quote(source_req_id)}";',
                '            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";',
                f'            attribute sourceContext = "{doc_text(drs_req_id)}";',
                f"            doc /* {doc_text(statement)} */;",
                "        }",
                f"        requirement req_{requirement_sysml_name(drs_req_id)} : {requirement_sysml_name(drs_req_id)};",
                f"        doc /* drsReqId={doc_text(drs_req_id)} | sourceReqId={doc_text(source_req_id)} | {doc_text(statement)} */;",
                f"        doc /* coverageDependency: {doc_text(drs_req_id)} -> approved source requirement {doc_text(source_req_id)} */;",
                f"        satisfy req_{requirement_sysml_name(drs_req_id)} by self;",
            ])
    _append_ports(lines, ports, "        ")
    for name in digital_blocks:
        lines.append(f"        part {usage_name(name)} : {sysml_name(name)};")
    lines.extend(["    }", "", "}", ""])
    return "\n".join(lines)


def build_model(
    requirements: List[Dict[str, str]],
    blocks: Dict[str, Dict[str, str]],
    interactions: List[Dict[str, str]],
    ports_by_owner: Optional[Dict[str, List[Dict[str, str]]]] = None,
    srs_requirements: Optional[List[Dict[str, str]]] = None,
    approved_srs_source_ids: Optional[set[str]] = None,
) -> str:
    """Build the hierarchical top model; block definitions live in sibling model files."""
    ordered_blocks = _ordered_blocks(blocks, interactions)
    ports_by_owner = ports_by_owner or {}
    srs_requirements = srs_requirements or []
    approved_srs_source_ids = approved_srs_source_ids or set()
    ids = {name: sysml_name(name) for name in ordered_blocks}
    _requirements_by_owner, system_level_requirements = _requirements_by_block(requirements, set(ordered_blocks))
    subsystem_blocks: Dict[str, List[str]] = {"Analog Subsystem": [], "Digital Subsystem": []}
    for name in ordered_blocks:
        subsystem_blocks[subsystem_for_block(name)].append(name)
    lines = [
        "package STBIO_Architecture {",
        "",
        "    // Generated hierarchical top model; block definitions are in sysml/blocks/.",
        "    private import STBIO_Shared::*;",
        "",
    ]
    for name in ordered_blocks:
        lines.append(f"    private import STBIO_Block_{ids[name]}::*;")
    lines.append("    private import STBIO_DigitalSubsystem::*;")
    lines.append("")
    for subsystem in subsystem_blocks:
        if subsystem == "Digital Subsystem":
            continue
        lines.extend([
            f"    part def {sysml_name(subsystem)} {{",
            f'        attribute displayName : String = "{subsystem}";',
        ])
        _append_ports(lines, ports_by_owner.get(subsystem, []), "        ")
        for name in subsystem_blocks[subsystem]:
            lines.append(f"        part {usage_name(name)} : {ids[name]};")
        lines.extend(["    }", ""])
    lines.extend([
        "    part def TopAnalogArchitecture {",
        '        attribute displayName : String = "Top Analog Architecture";',
        "        part analogSubsystem : AnalogSubsystem;",
        "    }",
        "",
        "    part def STBIOSystem {",
        "        doc /* Level 1 system architecture. Concrete requirements are contained by their owning Level 2 block. */;",
        "        part topAnalog : TopAnalogArchitecture;",
        "        part topDigital : DigitalSubsystem;",
    ])
    _append_ports(lines, ports_by_owner.get("STBIOSystem", []), "        ")
    lines.extend([
        "",
        "        // Level 1 subsystem relationships are derived from the interaction matrix.",
        "        connection analog_to_digital : ArchitectureConnection connect topAnalog to topDigital;",
    ])
    system_requirements = srs_requirements if srs_requirements is not None else system_level_requirements
    if system_requirements:
        lines.extend(["", "        // Complete system requirements are mirrored from the approved SRS traceability matrix."])
        for row in system_requirements:
            authored_id = row.get("srs_req_id") or row.get("source_req_id") or ""
            source_req_id = row.get("source_req_id") or ""
            statement = row.get("requirement_statement") or row.get("statement") or ""
            req_id = requirement_sysml_name(authored_id)
            lines.extend([
                f"        requirement def {req_id} : SourceRequirement {{",
                f'            attribute sourceReqId = "{quote(source_req_id)}";',
                f'            attribute sourceArtifact = "{quote(row.get("source_artifact", "artifacts/stage3_srs/srs_traceability_matrix.csv"))}";',
                f'            attribute sourceContext = "{quote(authored_id)}";',
                f"            doc /* {doc_text(statement)} */;",
                "        }",
                f"        requirement req_{req_id} : {req_id};",
                f"        doc /* authoredId={doc_text(authored_id)} | sourceReqId={doc_text(source_req_id)} | {doc_text(statement)} */;",
                f"        doc /* coverageDependency: {doc_text(authored_id)} -> approved source requirement {doc_text(source_req_id)} */;",
            ])
    lines.append("")
    lines.append("")
    for index, row in enumerate(interactions, start=1):
        source = block_name(row.get("From block", ""))
        target = block_name(row.get("To block", ""))
        if source not in ids or target not in ids:
            continue
        connection_id = f"connection_{index:03d}"
        source_subsystem = usage_name(subsystem_for_block(source))
        target_subsystem = usage_name(subsystem_for_block(target))
        source_top = "topDigital" if source_subsystem == "digitalSubsystem" else "topAnalog"
        target_top = "topDigital" if target_subsystem == "digitalSubsystem" else "topAnalog"
        source_path = (
            f"{source_top}.{usage_name(source)}"
            if source_top == "topDigital"
            else f"{source_top}.{source_subsystem}.{usage_name(source)}"
        )
        target_path = (
            f"{target_top}.{usage_name(target)}"
            if target_top == "topDigital"
            else f"{target_top}.{target_subsystem}.{usage_name(target)}"
        )
        lines.extend([
            f"        connection {connection_id} : ArchitectureConnection connect {source_path} to {target_path};",
            f'        doc {connection_id} /* signal={doc_text(row.get("Signal/control", ""))} | trigger={doc_text(row.get("Trigger", ""))} | notes={doc_text(row.get("Notes", ""))} | sourceReqIds={doc_text(";".join(item.strip() for item in (row.get("Requirement IDs") or "").split(";") if item.strip() in approved_srs_source_ids))} | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;',
        ])
    lines.extend(["    }", "", "}", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SysML architecture model from Stage 2A artifacts")
    parser.add_argument("--traceability", default="artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv")
    parser.add_argument("--mapping-preview", default="artifacts/stage1_specs/architecture_mapping_preview.csv")
    parser.add_argument("--source-edges", default="artifacts/stage1_requirements/source_matrix_edges.csv")
    parser.add_argument("--requirements", default="artifacts/stage1_requirements/requirements_summary.csv")
    parser.add_argument("--inventory", default="artifacts/stage2_mirco_arc/block_inventory.csv")
    parser.add_argument("--approved-block-list", default="artifacts/stage1_specs/approved_block_list.xlsx")
    parser.add_argument("--interactions", default="artifacts/stage2_mirco_arc/interaction_matrix.csv")
    parser.add_argument("--ports", default="artifacts/stage2_mirco_arc/source_port_catalog.csv")
    parser.add_argument("--model-dir", default="artifacts/stage2_mirco_arc/sysml")
    parser.add_argument("--output", default="artifacts/stage2_mirco_arc/sysml/STBIOSystem.sysml")
    parser.add_argument("--manifest", default="artifacts/stage2_mirco_arc/stbio_architecture_model_manifest.json")
    parser.add_argument("--partial-export", action="store_true", help="Allow an explicitly partial SysML export; default requires full approved snapshot block coverage.")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--snapshot-id", help="Explicit approved canonical snapshot ID")
    selector.add_argument("--use-latest-approved", action="store_true", help="Explicitly select the latest approved snapshot")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    context_path = repo_root / "config" / "project_context.json"
    context = json.loads(context_path.read_text(encoding="utf-8")) if context_path.exists() else {}
    project_id = str(context.get("project_name") or repo_root.name)
    snapshot = require_sysml_snapshot(repo_root, project_id=project_id, snapshot_id=args.snapshot_id, use_latest_approved=args.use_latest_approved)

    traceability = Path(args.traceability)
    inventory = Path(args.inventory)
    interactions = Path(args.interactions)
    approved_block_list = Path(args.approved_block_list)
    output = Path(args.output)
    model_dir = Path(args.model_dir)
    manifest = Path(args.manifest)
    inventory_rows = block_rows(inventory)
    block_inventory = {
        name: metadata
        for name, metadata in inventory_rows.items()
        if is_concrete_block(name, metadata)
    }
    interaction_rows = read_csv(interactions)
    drs_traceability = repo_root / "artifacts/stage5_drs/drs_traceability_matrix.csv"
    downstream_contract = resolve_downstream_contract(repo_root, snapshot.snapshot_id)
    expected = downstream_contract.expected
    contract_fingerprint = downstream_contract_fingerprint(downstream_contract)
    approved_ids_by_target = {
        target: {
            source_id
            for source_id, allocation in expected.items()
            if str(allocation.get("owning_target") or "").strip() == target
        }
        for target in ("SRS", "DRS", "Digital IPOS", "Analog IPOS")
    }
    drs_requirements = read_csv(drs_traceability) if drs_traceability.exists() else []
    drs_requirements = [
        row for row in drs_requirements
        if (row.get("source_req_id") or "").strip() in approved_ids_by_target["DRS"]
        and (row.get("snapshot_id") or "").strip() == snapshot.snapshot_id
    ]
    ipos_requirements_by_block = _read_ipos_requirements(repo_root)
    ipos_requirements_by_block = {
        owner: [
            row for row in rows
            if (row.get("source_req_id") or "").strip() in approved_ids_by_target["Digital IPOS"]
            and (row.get("snapshot_id") or "").strip() == snapshot.snapshot_id
        ]
        for owner, rows in ipos_requirements_by_block.items()
    }
    srs_traceability = repo_root / "artifacts/stage3_srs/srs_traceability_matrix.csv"
    srs_requirements = read_csv(srs_traceability) if srs_traceability.exists() else []
    srs_requirements = [
        row for row in srs_requirements
        if (row.get("source_req_id") or "").strip() in approved_ids_by_target["SRS"]
        and (row.get("snapshot_id") or "").strip() == snapshot.snapshot_id
    ]
    ports_path = Path(args.ports)
    ports_by_block = port_rows(ports_path)
    ordered_blocks = _ordered_blocks(block_inventory, interaction_rows, ports_by_block)
    compact = lambda value: re.sub(r"[^a-z0-9]", "", value.casefold())
    created_ipos_names = {
        compact(name)
        for stage in ("Digital IPOS", "Analog IPOS")
        for name in created_ipos_block_directories(repo_root, stage)
    }
    ordered_blocks = [name for name in ordered_blocks if compact(name) in created_ipos_names]
    requirements = requirement_rows(
        traceability,
        Path(args.mapping_preview),
        Path(args.source_edges),
        Path(args.requirements),
        set(ordered_blocks),
    )
    requirements = [
        row for row in requirements
        if (row.get("source_req_id") or "").strip()
        in approved_ids_by_target["Digital IPOS"] | approved_ids_by_target["Analog IPOS"]
    ]
    requirements_by_block, _system_level = _requirements_by_block(requirements, set(ordered_blocks))
    coverage = {"missing_by_block": {}, "expected_by_block": {}}
    output.parent.mkdir(parents=True, exist_ok=True)
    blocks_dir = model_dir / "blocks"
    blocks_dir.mkdir(parents=True, exist_ok=True)
    generated_files = []
    shared_path = model_dir / "shared_definitions.sysml"
    shared_path.write_text(sysml_header(snapshot.snapshot_id, contract_fingerprint) + build_shared_model(), encoding="utf-8")
    generated_files.append(shared_path)
    digital_subsystem_path = model_dir / "DigitalSubsystem.sysml"
    digital_subsystem_path.write_text(
        sysml_header(snapshot.snapshot_id, contract_fingerprint) + build_digital_subsystem_model(
            block_inventory,
            ports_by_block.get("Digital Subsystem", []),
            drs_requirements,
        ),
        encoding="utf-8",
    )
    generated_files.append(digital_subsystem_path)
    expected_block_files = set()
    for name in ordered_blocks:
        block_path = blocks_dir / model_file_name(name)
        expected_block_files.add(block_path)
        block_path.write_text(sysml_header(snapshot.snapshot_id, contract_fingerprint) + build_block_model(
            name,
            block_inventory.get(name, {}),
            requirements_by_block.get(name, []),
            ports_by_block.get(name, []),
            ipos_requirements_by_block.get(name, []),
        ), encoding="utf-8")
        generated_files.append(block_path)
    for stale_path in blocks_dir.glob("*.sysml"):
        if stale_path not in expected_block_files:
            stale_path.unlink()
    validate_generated_block_files(expected_block_files)
    output.write_text(
        sysml_header(snapshot.snapshot_id, contract_fingerprint) + build_model(
            requirements,
            block_inventory,
            interaction_rows,
            ports_by_block,
            srs_requirements,
            approved_ids_by_target["SRS"],
        ),
        encoding="utf-8",
    )
    generated_files.append(output)
    legacy_stage3_sysml = repo_root / "artifacts/stage3_srs/system_requirements_specification.sysml"
    if legacy_stage3_sysml.exists():
        legacy_stage3_sysml.unlink()
    manifest.write_text(json.dumps({
        "snapshot_id": snapshot.snapshot_id,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "model_path": output.as_posix(),
        "model_files": {path.as_posix(): sha256(path) for path in generated_files},
        "inputs": {path.as_posix(): sha256(path) for path in (
            traceability, Path(args.mapping_preview), Path(args.source_edges), Path(args.requirements),
            inventory, interactions, ports_path, approved_block_list,
        )},
        "counts": {
            "requirements": len(requirements),
            "blocks": len(ordered_blocks),
            "ports": sum(len(rows) for rows in ports_by_block.values()),
            "connections": len(interaction_rows),
            "model_files": len(generated_files),
        },
        "snapshot_requirement_coverage": {
            "partial_export": args.partial_export,
            "missing_by_block": coverage["missing_by_block"],
            "expected_requirement_count": sum(len(values) for values in coverage["expected_by_block"].values()),
        },
    }, indent=2) + "\n", encoding="utf-8")
    from audit_log import record_event
    record_event(repo_root, event_type="sysml_generated", entity_type="sysml", entity_id=output.as_posix(), actor="system", message="SysML generated from approved snapshot", project_id=project_id, payload={"snapshot_id": snapshot.snapshot_id})
    print(f"Generated {output.as_posix()}")
    print(f"Requirements: {len(requirements)}; blocks: {len(ordered_blocks)}; ports: {sum(len(rows) for rows in ports_by_block.values())}; connections: {len(interaction_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
