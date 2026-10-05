#!/usr/bin/env python3
"""Convert the SRS traceability and architecture CSVs to a SysML v2-style model."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Dict, List

from validate_downstream_coherence import canonical_human_label


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _sysml_name(value: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", value or "")
    name = "".join(word[:1].upper() + word[1:] for word in words)
    if not name:
        return "Unnamed"
    if name[0].isdigit():
        return "Block_" + name
    return name


def _block_name(value: str) -> str:
    return canonical_human_label(value)


def _quote(value: str) -> str:
    return (value or "").replace("\\", "\\\\").replace('"', '\\"').replace("\r", " ").replace("\n", " ")


def _doc_text(value: str) -> str:
    return re.sub(r"\*/", "* /", (value or "").strip())


def _requirement_rows(path: Path) -> List[Dict[str, str]]:
    rows = _read_csv(path)
    return [row for row in rows if row.get("srs_req_id") and row.get("requirement_statement")]


def _architecture_blocks(inventory_rows: List[Dict[str, str]], interaction_rows: List[Dict[str, str]], requirement_rows: List[Dict[str, str]]) -> List[str]:
    names = set()
    for row in inventory_rows:
        if row.get("Block"):
            names.add(_block_name(row["Block"]))
    for row in interaction_rows:
        names.add(_block_name(row.get("From block", "")))
        names.add(_block_name(row.get("To block", "")))
    for row in requirement_rows:
        names.add(_block_name(row.get("owning_block", "")))
    names.discard("")
    return sorted(names, key=lambda value: (_sysml_name(value) == "Unassigned", _sysml_name(value)))


def _write_model(output: Path, requirements: List[Dict[str, str]], inventory_rows: List[Dict[str, str]], interaction_rows: List[Dict[str, str]]) -> None:
    blocks = _architecture_blocks(inventory_rows, interaction_rows, requirements)
    block_ids = {_block_name(block): _sysml_name(_block_name(block)) for block in blocks}
    lines = [
        "package STBIO_SRS_Architecture {",
        "",
        "    // Generated from the Stage 3 SRS and Stage 2 architecture CSV artifacts.",
        "    // Requirement wording and source IDs are retained; block names are SysML identifiers.",
        "",
        "    connection def ArchitectureConnection {",
        "        attribute signal : String;",
        "        attribute trigger : String;",
        "        attribute sourceArtifact : String;",
        "        attribute sourceRequirementIds : String;",
        "    }",
        "",
    ]

    for block in blocks:
        block_id = block_ids[block]
        inventory = next((row for row in inventory_rows if _block_name(row.get("Block", "")) == block), {})
        lines.extend([
            "    part def " + block_id + " {",
            '        attribute displayName : String = "' + _quote(block) + '";',
            '        attribute function : String = "' + _quote(inventory.get("Function", "")) + '";',
            "    }",
            "",
        ])

    lines.extend([
        "    requirement def SRSRequirement {",
        "        attribute srsReqId : String;",
        "        attribute sourceReqId : String;",
        "        attribute domain : String;",
        "        attribute verificationMethod : String;",
        "        attribute acceptanceCriteria : String;",
        "        attribute sourceArtifact : String;",
        "        attribute status : String;",
        "    }",
        "",
    ])

    for row in requirements:
        requirement_id = _sysml_name(row["srs_req_id"])
        lines.extend([
            "    requirement def " + requirement_id + " : SRSRequirement {",
            '        attribute srsReqId = "' + _quote(row["srs_req_id"]) + '";',
            '        attribute sourceReqId = "' + _quote(row.get("source_req_id", "")) + '";',
            '        attribute domain = "' + _quote(row.get("domain", "")) + '";',
            '        attribute verificationMethod = "' + _quote(row.get("verification_method", "")) + '";',
            '        attribute acceptanceCriteria = "' + _quote(row.get("acceptance_criteria", "")) + '";',
            '        attribute sourceArtifact = "' + _quote(row.get("source_artifact", "")) + '";',
            '        attribute status = "' + _quote(row.get("status", "")) + '";',
            "        doc /* " + _doc_text(row["requirement_statement"]) + " */;",
            "    }",
            "",
        ])

    lines.extend([
        "    part def STBIOSystem {",
        "        doc /* STBIO system architecture represented by SRS allocations and the Stage 2 interaction matrix. */;",
    ])
    for block in blocks:
        block_id = block_ids[block]
        lines.append("        part " + block_id[:1].lower() + block_id[1:] + " : " + block_id + ";")

    lines.extend(["", "        // SRS requirements are allocated to their identified owning architecture block."])
    for index, row in enumerate(requirements, start=1):
        requirement_id = _sysml_name(row["srs_req_id"])
        requirement_usage = "req_" + str(index).zfill(3)
        owner = _block_name(row.get("owning_block", "Unassigned")) or "Unassigned"
        owner_id = block_ids.get(owner, "Unassigned")
        owner_part = owner_id[:1].lower() + owner_id[1:]
        lines.extend([
            "        requirement " + requirement_usage + " : " + requirement_id + ";",
            "        satisfy requirement " + requirement_usage + " by " + owner_part + ";",
        ])

    lines.extend(["", "        // Architecture interconnections from the Stage 2 interaction matrix."])
    for index, row in enumerate(interaction_rows, start=1):
        source_id = block_ids.get(_block_name(row.get("From block", "")), _sysml_name(row.get("From block", "")))
        target_id = block_ids.get(_block_name(row.get("To block", "")), _sysml_name(row.get("To block", "")))
        source_part = source_id[:1].lower() + source_id[1:]
        target_part = target_id[:1].lower() + target_id[1:]
        connection_id = "connection_" + str(index).zfill(3)
        connection_doc = (
            _doc_text(row.get("Notes", ""))
            + " | signal=" + _doc_text(row.get("Signal/control", ""))
            + " | trigger=" + _doc_text(row.get("Trigger", ""))
            + " | sourceReqIds=" + _doc_text(row.get("Requirement IDs", ""))
        )
        lines.extend([
            "        connection " + connection_id + " : ArchitectureConnection connect " + source_part + " to " + target_part + ";",
            "        doc " + connection_id + " /* " + connection_doc + " */;",
        ])

    lines.extend(["    }", "", "}", ""])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert SRS CSV traceability to SysML")
    parser.add_argument("--srs", default="artifacts/stage3_srs/srs_traceability_matrix.csv")
    parser.add_argument("--inventory", default="artifacts/stage2_mirco_arc/block_inventory.csv")
    parser.add_argument("--interactions", default="artifacts/stage2_mirco_arc/interaction_matrix.csv")
    parser.add_argument("--output", default="artifacts/stage3_srs/system_requirements_specification.sysml")
    args = parser.parse_args()

    _write_model(
        Path(args.output),
        _requirement_rows(Path(args.srs)),
        _read_csv(Path(args.inventory)),
        _read_csv(Path(args.interactions)),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())