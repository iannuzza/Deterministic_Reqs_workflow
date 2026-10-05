#!/usr/bin/env python3
"""Shared Markdown formatting checks for Stage 0 through Stage 5 gates."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Tuple


LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+(?:\.\d+)+[.:]?\s+|\d+[.)]\s+|•\s+)")
AUTHORED_HEADER_RE = re.compile(r"^\s*\*\*\[(?:SRS|ARS|DRS)-REQ-\d{3}\]\s+Requirement:\*\*\s*$")
COVERS_RE = re.compile(r"^\s*Covers:\s*\S+\s*$")
END_RE = re.compile(r"^\s*\[End\]\s*$", flags=re.IGNORECASE)
AUTHORED_REQUIREMENT_SPACER = "<p>&nbsp;</p>"
SECTION_NUMBER_RE = re.compile(r"^(\d+(?:\.\d+)*)\b")


def _section_sort_key(value: str) -> Optional[Tuple[int, ...]]:
    match = SECTION_NUMBER_RE.match((value or "").strip())
    if not match:
        return None
    return tuple(int(part) for part in match.group(1).split("."))


def _validate_numerical_navigation_order(relative_path: Path, text: str) -> list[str]:
    """Validate numeric order in generated TOCs and section navigation tables."""
    findings: list[str] = []
    toc_match = re.search(
        r"^###\s+(?:\*\*)?0\.1\s+Table of contents(?:\*\*)?.*?$(.*?)(?=^###\s+(?:\*\*)?0\.2\s+|\Z)",
        text,
        flags=re.M | re.S | re.I,
    )
    if not toc_match:
        return [f"{relative_path.as_posix()} is missing a Table of contents section"]

    toc_keys = [
        key
        for title in re.findall(r"^\s*-\s+\[([^\]]+)\]", toc_match.group(1), flags=re.M)
        if (key := _section_sort_key(title)) is not None
    ]
    if toc_keys != sorted(toc_keys):
        findings.append(f"{relative_path.as_posix()} table of contents is not in numerical section order")

    table_match = re.search(
        r"^\|\s*Section\s*\|\s*Paragraph anchor\s*\|.*?$\n"
        r"^\|\s*-+.*?$\n(?P<rows>(?:^\|.*?$\n)+)",
        text,
        flags=re.M | re.I,
    )
    if not table_match:
        findings.append(f"{relative_path.as_posix()} is missing a Section navigation index table")
        return findings

    index_keys = []
    for row in table_match.group("rows").splitlines():
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        key = _section_sort_key(cells[1])
        if key is not None:
            index_keys.append(key)
    if index_keys != sorted(index_keys):
        findings.append(f"{relative_path.as_posix()} Section navigation index is not in numerical order")
    return findings


def _validate_source_function_context(relative_path: Path, text: str) -> list[str]:
    """Require retained source context to use complete local requirement blocks."""
    prefix_by_filename = {
        "system_requirements_specification.md": "SRS",
        "analog_requirements_specification.md": "ARS",
        "digital_requirements_specification.md": "DRS",
    }
    prefix = prefix_by_filename.get(relative_path.name)
    if not prefix:
        return []
    context_match = re.search(
        r"^##\s+.*?Source Function Context\b(?P<context>.*?)(?=^##\s+|\Z)",
        text,
        flags=re.M | re.S | re.I,
    )
    if not context_match:
        return []

    findings: list[str] = []
    context = context_match.group("context")
    header_re = re.compile(rf"^\s*\*\*\[{prefix}-REQ-\d{{3}}\]\s+Requirement:\*\*\s*$", re.M)
    for source_match in re.finditer(r"^\s*Source paragraph:\s*\S.*$", context, flags=re.M):
        preceding = context[:source_match.start()]
        headers = list(header_re.finditer(preceding))
        if not headers:
            findings.append(
                f"{relative_path.as_posix()} Source Function Context entry lacks a local {prefix}-REQ header"
            )
            break
        requirement_block = preceding[headers[-1].end():]
        if not re.search(r"^\s*Covers:\s*\S+\s*$", requirement_block, flags=re.M):
            findings.append(
                f"{relative_path.as_posix()} Source Function Context requirement lacks a Covers link"
            )
            break
        if not re.search(r"^\s*\[End\]\s*$", requirement_block, flags=re.M | re.I):
            findings.append(
                f"{relative_path.as_posix()} Source Function Context requirement lacks [End]"
            )
            break
    return findings


def validate_markdown_paths(
    repo_root: Path, paths: list[Path], *, check_list_spacing: bool = False
) -> list[str]:
    """Return hard formatting findings for the supplied generated Markdown files."""
    findings: list[str] = []
    for relative_path in paths:
        path = repo_root / relative_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        if relative_path.name in {
            "system_requirements_specification.md",
            "analog_requirements_specification.md",
            "digital_requirements_specification.md",
        }:
            findings.extend(_validate_numerical_navigation_order(relative_path, text))
            findings.extend(_validate_source_function_context(relative_path, text))
        if text and not text.endswith("\n"):
            findings.append(f"{relative_path.as_posix()} does not end with a newline")
        authored_blocks = re.findall(
            r"^\s*\*\*\[(?:SRS|ARS|DRS)-REQ-\d{3}\]\s+Requirement:\*\*\s*$"
            r"(?P<body>.*?)(?=^\s*\*\*\[(?:SRS|ARS|DRS)-REQ-\d{3}\]\s+Requirement:\*\*\s*$|\Z)",
            text,
            flags=re.M | re.S,
        )
        for index, block in enumerate(authored_blocks, start=1):
            end_match = re.search(r"^\s*\[End\]\s*$", block, flags=re.M | re.I)
            if not end_match:
                findings.append(f"{relative_path.as_posix()} authored requirement {index} is missing [End]")
                continue
            covers_match = re.search(r"^\s*Covers:\s*\S+\s*$", block, flags=re.M)
            if covers_match and end_match.start() < covers_match.end():
                findings.append(f"{relative_path.as_posix()} authored requirement {index} has [End] before Covers")
        in_fenced_block = False
        for line in lines:
            if line.strip().startswith("```"):
                in_fenced_block = not in_fenced_block
                continue
            if not in_fenced_block and line.lstrip().startswith("• "):
                findings.append(f"{relative_path.as_posix()} contains non-standard Unicode bullet markers")
                break

        previous_line = ""
        list_block_open = False
        previous_was_covers = False
        previous_was_authored_header = False
        for line_number, line in enumerate(lines, start=1):
            is_list_item = bool(LIST_ITEM_RE.match(line))
            is_authored_header = bool(AUTHORED_HEADER_RE.match(line))
            is_covers = bool(COVERS_RE.match(line))
            has_authored_requirement_spacer = (
                previous_line.strip() == AUTHORED_REQUIREMENT_SPACER
                or (
                    line_number >= 3
                    and not previous_line.strip()
                    and lines[line_number - 3].strip() == AUTHORED_REQUIREMENT_SPACER
                )
            )
            if check_list_spacing and is_list_item and line.strip() and previous_line.strip() and not list_block_open:
                findings.append(
                    f"{relative_path.as_posix()}:{line_number} list block is not preceded by a blank line"
                )
            if is_authored_header and not has_authored_requirement_spacer:
                findings.append(
                    f"{relative_path.as_posix()}:{line_number} authored requirement header is not preceded by {AUTHORED_REQUIREMENT_SPACER}"
                )
            if is_authored_header and has_authored_requirement_spacer:
                if line_number >= 3 and previous_line.strip() == "" and lines[line_number - 3].strip() == AUTHORED_REQUIREMENT_SPACER:
                    pass
                elif line_number < 2 or lines[line_number - 2].strip():
                    findings.append(
                        f"{relative_path.as_posix()}:{line_number} {AUTHORED_REQUIREMENT_SPACER} is not preceded by a blank line"
                    )
            if is_authored_header and previous_was_covers:
                findings.append(
                    f"{relative_path.as_posix()}:{line_number} authored requirement follows Covers without a blank line"
                )
            if previous_was_authored_header and line.strip():
                findings.append(
                    f"{relative_path.as_posix()}:{line_number} requirement content is not separated from its header"
                )
            if is_covers and previous_line.strip():
                findings.append(
                    f"{relative_path.as_posix()}:{line_number} Covers is not separated from the requirement statement"
                )
            if not line.strip():
                list_block_open = False
            elif is_list_item or list_block_open:
                list_block_open = True
            previous_line = line
            previous_was_covers = is_covers
            previous_was_authored_header = is_authored_header
    return findings


def paths_for_stage(stage_key: str) -> list[Path]:
    """Return generated Markdown paths whose formatting is owned by the stage."""
    stage_paths = {
        "0": [
            Path("artifacts/stage0_ontology/ontology.md"),
            Path("artifacts/stage0_ontology/semantic_issues.md"),
            Path("artifacts/orchestrator/stage_00_report.md"),
        ],
        "1": [
            Path("artifacts/stage1_requirements/requirements_raw.md"),
            Path("artifacts/stage1_requirements/requirements_summary.md"),
            Path("artifacts/stage1_requirements/requirements_rag_crosscheck.md"),
            Path("artifacts/stage1_requirements/coverage_crosscheck.md"),
            Path("artifacts/orchestrator/stage_01_report.md"),
        ],
        "2": [
            Path("artifacts/stage1_specs/specs.md"),
            Path("artifacts/orchestrator/stage_02_report.md"),
        ],
        "2a": [
            Path("artifacts/stage2_mirco_arc/function_decomposition.md"),
            Path("artifacts/stage2_mirco_arc/micro_architecture_report.md"),
            Path("artifacts/stage2_mirco_arc/architecture_crosscheck_report.md"),
            Path("artifacts/orchestrator/stage_02_micro_arch_report.md"),
        ],
        "3": [Path("artifacts/stage3_srs/system_requirements_specification.md")],
        "4": [Path("artifacts/stage4_ars/analog_requirements_specification.md")],
        "5": [Path("artifacts/stage5_drs/digital_requirements_specification.md")],
    }
    return stage_paths[stage_key]


def validate_stage_markdown(repo_root: Path, stage_key: str) -> list[str]:
    """Apply common checks with list-boundary rules for rendered specifications."""
    return validate_markdown_paths(
        repo_root,
        paths_for_stage(stage_key),
        check_list_spacing=stage_key in {"3", "4", "5"},
    )
