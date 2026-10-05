#!/usr/bin/env python3
"""Run DRS crosscheck for Stage 5 DRS outputs."""

from __future__ import annotations

import csv
import argparse
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from traceability_content_checks import (
    check_authored_markdown_content,
    check_source_traceability_content,
    read_source_requirements,
)
from traceability_hierarchy_coverage import write_hierarchy_coverage_report
from workflow_routing import is_reset_clock_table_row
from workflow_routing import TOP_DIGITAL_CATEGORY_SPECS, is_reset_clock_table_row
from validate_downstream_coherence import resolve_downstream_contract
from traceability_rules import is_direct_upstream_source_id, is_srs_requirement_id, is_valid_upstream_reference
from source_io_coverage import check_source_coverage


REQUIRED = [
    "artifacts/stage5_drs/digital_requirements_specification.md",
    "artifacts/stage5_drs/drs_traceability_matrix.csv",
    "artifacts/stage3_srs/srs_traceability_matrix.csv",
    "artifacts/orchestrator/stage_drs_report.md",
    "artifacts/stage1_requirements/requirements_summary.csv",
    "artifacts/stage2_mirco_arc/block_inventory.csv",
    "artifacts/stage2_mirco_arc/interface_catalog.csv",
        "artifacts/stage2_mirco_arc/interaction_matrix.csv",
        "artifacts/stage5_drs/top_digital_coverage_audit.csv",
]


FUNCTION_STOP_WORDS = {
    "a", "and", "are", "as", "at", "by", "for", "from", "in", "into",
    "of", "on", "or", "the", "to", "with",
}


POWER_FOCUS_TERMS = (
    "power",
    "supply",
    "voltage",
    "brown-out",
    "reverse-polarity",
    "polarity",
)


BLOCK_ANALOG_TERMS = (
    "analog",
    "sensor",
    "relay",
    "voltage",
    "power",
    "brown-out",
    "noise",
    "calibration",
)


BLOCK_DIGITAL_TERMS = (
    "control",
    "dsp",
    "i2c",
    "spi",
    "ahb",
    "data",
    "uart",
    "host",
    "firmware",
    "command",
    "protocol",
    "gpio",
    "led",
    "button",
    "event",
    "schedule",
    "mode",
    "state machine",
    "telemetry",
    "nvm",
    "memory",
    "register",
    "interrupt",
    "fifo",
    "test",
    "debug",
)


DIGITAL_ARCHITECTURE_TERMS = (
    "i2c", "spi", "ahb", "axi", "apb", "uart", "jtag", "serial",
    "protocol", "bus", "processor", "cpu", "microprocessor", "core", "digital",
)

BLOCK_CLASS_ANALOG = "analog_or_mixed"
BLOCK_CLASS_POWER = "power_or_supply"
BLOCK_CLASS_DIGITAL = "digital_or_system"


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\\n")


def _count_rows(csv_path: Path) -> int:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return sum(1 for _ in reader)


def _read_trace_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


def _check_srs_covers_alignment(
    drs_markdown: str,
    drs_trace_rows: List[Dict[str, str]],
    srs_trace_rows: List[Dict[str, str]],
    approved_targets: Dict[str, str] | None = None,
) -> List[str]:
    source_by_drs_id = {
        row.get("drs_req_id", ""): row.get("source_req_id", "")
        for row in drs_trace_rows
        if row.get("drs_req_id") and row.get("source_req_id")
    }
    srs_by_source_id = {
        row.get("source_req_id", ""): row
        for row in srs_trace_rows
        if row.get("source_req_id") and is_srs_requirement_id(row.get("srs_req_id", ""))
    }
    authored_blocks = re.findall(
        r"^\s*\*\*\[(DRS-REQ-\d{3})\]\s+Requirement:\*\*\s*\n(.*?)(?=^\s*\*\*\[DRS-REQ-\d{3}\]\s+Requirement:\*\*\s*$|\Z)",
        drs_markdown,
        flags=re.M | re.S,
    )
    findings: List[str] = []
    for drs_req_id, block in authored_blocks:
        source_req_id = source_by_drs_id.get(drs_req_id)
        expected_srs_row = srs_by_source_id.get(source_req_id, {})
        expected_srs_id = expected_srs_row.get("srs_req_id", "")
        covers_match = re.search(r"^\s*Covers:\s*([A-Z][A-Z0-9_-]*)\s*$", block, flags=re.M)
        if (
            source_req_id
            and not expected_srs_row
            and not _is_direct_supplementary_source(source_req_id)
            and (approved_targets or {}).get(source_req_id) != "DRS"
        ):
            findings.append(f"{drs_req_id} source {source_req_id} has no SRS traceability row")
        if _is_direct_supplementary_source(source_req_id) and covers_match and covers_match.group(1) != source_req_id:
            findings.append(f"{drs_req_id} Covers {covers_match.group(1)} but direct supplementary source is {source_req_id}")
        if expected_srs_row:
            drs_row = next((row for row in drs_trace_rows if row.get("drs_req_id") == drs_req_id), {})
            drs_statement = re.sub(r"\s+", " ", drs_row.get("requirement_statement", "")).strip()
            srs_statement = re.sub(r"\s+", " ", expected_srs_row.get("requirement_statement", "")).strip()
            if not drs_statement or not srs_statement or drs_statement != srs_statement:
                findings.append(f"{drs_req_id} statement differs from SRS statement for source {source_req_id}")
        if source_req_id and expected_srs_id and covers_match and covers_match.group(1) != expected_srs_id:
            findings.append(
                f"{drs_req_id} Covers {covers_match.group(1)} but source {source_req_id} maps to {expected_srs_id}"
            )
    return findings


def _validate_top_digital_coverage_audit(repo_root: Path) -> list[str]:
    path = repo_root / "artifacts/stage5_drs/top_digital_coverage_audit.csv"
    if not path.exists():
        return ["Missing top-digital coverage audit"]
    allowed_scopes = {"top_digital", "integration", "architecture", "lifted_integration"}
    expected_categories = {name for name, _terms in TOP_DIGITAL_CATEGORY_SPECS}
    findings: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    actual_categories = {row.get("category", "").strip() for row in rows}
    if actual_categories != expected_categories:
        findings.append("Top-digital coverage audit categories do not match the approved category set")
    if len(rows) != len(expected_categories):
        findings.append("Top-digital coverage audit must contain exactly one row per category")
    for row in rows:
        status = row.get("status", "").strip()
        statement = row.get("statement", "").strip()
        scopes = {
            item.strip().casefold()
            for item in row.get("scope", "").split(";")
            if item.strip()
        }
        source = row.get("source", "").strip()
        if status not in {"Covered", "Partial", "Missing"}:
            findings.append(f"Invalid top-digital coverage status: {status}")
        if statement and (not scopes or not scopes.issubset(allowed_scopes) or not source):
            findings.append(f"Top-digital evidence has invalid scope or missing provenance: {row.get('category', '')}")
        if "block_local" in scopes or "digital ipos" in f"{statement} {source}".casefold():
            findings.append(f"Top-digital coverage leaks Digital IPOS detail: {row.get('category', '')}")
        if re.search(r"\bblock\s+shall\s+implement\s*:", statement, flags=re.IGNORECASE):
            findings.append(f"Top-digital coverage contains block-local normative detail: {row.get('category', '')}")
    return findings


def _split_blocks(mapped_blocks: str) -> List[str]:
    return [token.strip() for token in (mapped_blocks or "").split(";") if token.strip()]


def _normalize_block_heading_name(value: str) -> str:
    text = (value or "").strip()
    # Strip explicit markdown heading IDs, e.g. "AnalogFrontEnd {#91-analogfrontend}".
    text = re.sub(r"\s*\{#[a-zA-Z0-9_-]+\}\s*$", "", text)
    return text.strip()


def _is_single_upstream_id(covers_value: str) -> bool:
    value = (covers_value or "").strip()
    if not value or value.lower() == "none":
        return False
    if ";" in value or "," in value:
        return False
    return is_valid_upstream_reference(value)


def _is_direct_supplementary_source(source_req_id: str) -> bool:
    return is_direct_upstream_source_id(source_req_id)


def _has_markdown_table_with_columns(raw_text: str, required_terms: list[str]) -> bool:
    for line in raw_text.splitlines():
        if "|" not in line:
            continue
        low = line.lower()
        if all(term in low for term in required_terms):
            return True
    return False


def _read_block_inventory(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


def _read_interface_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


def _function_terms(text: str) -> set[str]:
    terms = set(re.findall(r"[a-z][a-z0-9]+", (text or "").lower()))
    return {
        term[:-1] if term.endswith("s") and len(term) > 4 else term
        for term in terms
        if term not in FUNCTION_STOP_WORDS and len(term) > 2
    }


def _read_matrix_requirement_ids(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        ids: set[str] = set()
        for row in reader:
            ids.update(item.strip() for item in (row.get("Requirement IDs") or "").split(";") if item.strip())
        return ids


def _read_reset_clock_table_requirement_ids(path: Path) -> set[str]:
    out: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            req_id = (row.get("source_req_id") or row.get("id") or "").strip()
            if req_id and is_reset_clock_table_row(row):
                out.add(req_id)
    return out


def _read_source_section_owners(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {
            (row.get("source_req_id") or row.get("id") or "").strip(): (row.get("source_section_owner") or "").strip()
            for row in csv.DictReader(handle)
            if (row.get("source_req_id") or row.get("id") or "").strip()
            and (row.get("source_section_owner") or "").strip()
        }


def _read_approved_requirement_owners(path: Path) -> dict[str, set[str]]:
    owners: dict[str, set[str]] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            req_id = (row.get("Requirement ID") or "").strip()
            if not req_id:
                continue
            blocks = {
                block.strip()
                for block in (row.get("Block(s)") or "").split(";")
                if block.strip() and block.strip().lower() != "unassigned"
            }
            if blocks:
                owners[req_id] = blocks
    return owners


def _read_interrupt_table_requirement_ids(path: Path) -> set[str]:
    out: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            req_id = (row.get("source_req_id") or row.get("id") or "").strip()
            metadata = " ".join(
                (
                    row.get("derivation_kind") or "",
                    row.get("evidence_type") or "",
                    row.get("notes") or "",
                )
            ).lower()
            if req_id and "interrupt_table_connection" in metadata and "derived-from-structure" in metadata:
                out.add(req_id)
    return out


def _reset_clock_owner(block_functions: Dict[str, str]) -> str:
    for block in block_functions:
        if block.strip().lower() == "pmu":
            return block

    ranked: List[Tuple[int, str]] = []
    for block, function in block_functions.items():
        text = f"{block} {function}".lower()
        if "clock" not in text and "reset" not in text:
            continue
        score = sum(
            1
            for term in ("pmu", "power", "clock", "reset", "por", "ldo", "sequence", "sequencing", "release", "ready")
            if term in text
        )
        if score:
            ranked.append((score, block))

    if not ranked:
        return ""
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return ranked[0][1]


def _interrupt_owner(block_functions: Dict[str, str]) -> str:
    ranked: List[Tuple[int, str]] = []
    for block, function in block_functions.items():
        text = f"{block} {function}".lower()
        score = sum(1 for term in ("processor", "cpu", "microcontroller", "controller", "interrupt", "irq") if term in text)
        if score:
            ranked.append((score, block))
    if not ranked:
        return ""
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return ranked[0][1]


def _check_function_contract(
    raw_text: str,
    trace_rows: List[Dict[str, str]],
    block_functions: Dict[str, str],
    matrix_ids: set[str],
    source_section_owners: dict[str, str],
    approved_requirement_owners: dict[str, set[str]],
    reset_clock_table_ids: set[str],
    interrupt_table_ids: set[str],
) -> List[str]:
    findings: List[str] = []
    reset_clock_owner = _reset_clock_owner(block_functions)
    interrupt_owner = _interrupt_owner(block_functions)
    for block_name, function in block_functions.items():
        if not function:
            findings.append(f"Inventory block has empty Function: {block_name}")

    for row in trace_rows:
        source_id = row.get("source_req_id", "").strip()
        expected = approved_requirement_owners.get(source_id, set())
        if not source_id or not expected or source_id in matrix_ids:
            continue
        actual = {
            item.strip()
            for item in row.get("owning_block", "").split(";")
            if item.strip() and item.strip().lower() != "unassigned"
        }
        if expected != actual:
            findings.append(
                f"DRS owner differs from authoritative Stage 2A mapping: {source_id} "
                f"(stage2={'; '.join(sorted(expected))}, "
                f"drs={'; '.join(sorted(actual)) or 'Unassigned'})"
            )

    for row in trace_rows:
        source_id = row.get("source_req_id", "")
        if source_id in matrix_ids:
            continue
        requirement_terms = _function_terms(row.get("requirement_statement", ""))
        for owner in [item.strip() for item in row.get("owning_block", "").split(";") if item.strip()]:
            if owner.lower() == "unassigned":
                continue
            if owner not in block_functions:
                findings.append(f"DRS traceability owner is absent from block inventory: {owner}")
            elif source_section_owners.get(source_id) == owner:
                continue
            elif owner in approved_requirement_owners.get(source_id, set()):
                continue
            elif source_id in reset_clock_table_ids and owner == reset_clock_owner:
                continue
            elif source_id in interrupt_table_ids and owner == interrupt_owner:
                continue
            elif not requirement_terms & _function_terms(block_functions[owner]):
                findings.append(f"DRS owner is not supported by inventory Function: {source_id} -> {owner}")
    return findings


def _interface_types_by_owner(interface_rows: List[Dict[str, str]]) -> Dict[str, Dict[str, int]]:
    owner_types: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in interface_rows:
        owner = (row.get("Owner") or "").strip()
        iface_type = (row.get("Type") or "").strip().lower()
        if owner and iface_type:
            owner_types[owner][iface_type] += 1
    return owner_types


def _linked_domain_counts(linked_requirements: str) -> Dict[str, int]:
    counts = {"ana": 0, "dig": 0, "sys": 0}
    for token in [t.strip().upper() for t in (linked_requirements or "").split(";") if t.strip()]:
        if "ANA-RQ" in token or "CONF_ANA" in token:
            counts["ana"] += 1
        elif "DIG-RQ" in token or "CONF_DIG" in token:
            counts["dig"] += 1
        elif "SYS-RQ" in token or "CONF_SYS" in token:
            counts["sys"] += 1
    return counts


def _text_score(text: str, terms: Tuple[str, ...]) -> int:
    t = (text or "").lower()
    return sum(1 for token in terms if token in t)


def _classify_block_category(block: Dict[str, str], owner_types: Dict[str, Dict[str, int]]) -> str:
    bundle = block.get("Function", "")
    if _text_score(bundle, DIGITAL_ARCHITECTURE_TERMS) > 0:
        return BLOCK_CLASS_DIGITAL
    if "convert" in bundle.lower() and _text_score(bundle, ("adc", "analog")) > 0:
        return BLOCK_CLASS_ANALOG
    analog_score = _text_score(bundle, BLOCK_ANALOG_TERMS)
    power_score = _text_score(bundle, POWER_FOCUS_TERMS)
    digital_score = _text_score(bundle, BLOCK_DIGITAL_TERMS)

    if power_score > 0 and power_score >= digital_score:
        return BLOCK_CLASS_POWER
    if analog_score > digital_score:
        return BLOCK_CLASS_ANALOG

    return BLOCK_CLASS_DIGITAL


def main() -> int:
    parser = argparse.ArgumentParser(description="Run DRS crosscheck for Stage 5 DRS outputs.")
    selector = parser.add_mutually_exclusive_group()
    selector.add_argument("--snapshot-id")
    selector.add_argument("--use-latest-approved", action="store_true")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    missing = [rel for rel in REQUIRED if not (repo_root / rel).exists()]
    drs_md = repo_root / "artifacts/stage5_drs/digital_requirements_specification.md"
    trace_csv = repo_root / "artifacts/stage5_drs/drs_traceability_matrix.csv"
    srs_trace_csv = repo_root / "artifacts/stage3_srs/srs_traceability_matrix.csv"
    req_block_trace_csv = repo_root / "artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv"
    block_inventory_csv = repo_root / "artifacts/stage2_mirco_arc/block_inventory.csv"
    interface_catalog_csv = repo_root / "artifacts/stage2_mirco_arc/interface_catalog.csv"

    status = "pass"
    findings: list[str] = []
    coverage_findings = _validate_top_digital_coverage_audit(repo_root)
    from spec_document_contract import validate_drs_document_contract
    contract_findings = validate_drs_document_contract(repo_root)
    if contract_findings:
        status = "fail"
        findings.extend(contract_findings)
    if coverage_findings:
        status = "fail"
        findings.extend(coverage_findings)

    if missing:
        status = "fail"
        findings.append("Missing required artifacts: " + ", ".join(missing))

    trace_rows = _count_rows(trace_csv) if trace_csv.exists() else 0
    if trace_csv.exists() and trace_rows == 0:
        status = "fail"
        findings.append("DRS traceability matrix has zero rows")

    trace_details = _read_trace_rows(trace_csv) if trace_csv.exists() else []
    srs_trace_details = _read_trace_rows(srs_trace_csv) if srs_trace_csv.exists() else []
    trace_ids = [row.get("drs_req_id", "") for row in trace_details]
    if any(not re.fullmatch(r"DRS-REQ-\d{3}", req_id) for req_id in trace_ids):
        status = "fail"
        findings.append("DRS traceability contains an invalid authored ID namespace")
    if len(trace_ids) != len(set(trace_ids)):
        status = "fail"
        findings.append("DRS traceability contains duplicate DRS-REQ IDs")
    summary_path = repo_root / "artifacts/stage1_requirements/requirements_summary.csv"
    source_rows = None
    source_path = summary_path
    approved_targets: Dict[str, str] = {}
    if args.snapshot_id or args.use_latest_approved:
        context_path = repo_root / "config/project_context.json"
        context = json.loads(context_path.read_text(encoding="utf-8"))
        downstream_contract = resolve_downstream_contract(repo_root, args.snapshot_id)
        requirement_input = downstream_contract.requirement_input
        source_rows = {
            (row.get("source_req_id") or row.get("id") or "").strip(): {
                key: (value or "").strip() for key, value in row.items() if key is not None
            }
            for row in requirement_input.rows
            if (row.get("source_req_id") or row.get("id") or "").strip()
        }
        approved_targets = {
            source_id: downstream_contract.target(source_id)
            for source_id in downstream_contract.expected
        }

    def source_catalog() -> Dict[str, Dict[str, str]]:
        return source_rows if source_rows is not None else read_source_requirements(source_path)

    source_catalog_rows = source_catalog()
    direct_supplementary_ids = {
        row.get("source_req_id", "").strip()
        for row in trace_details
        if is_direct_upstream_source_id(row.get("source_req_id", ""))
    }
    block_rows = _read_block_inventory(block_inventory_csv) if block_inventory_csv.exists() else []
    interface_rows = _read_interface_rows(interface_catalog_csv) if interface_catalog_csv.exists() else []
    owner_types = _interface_types_by_owner(interface_rows)
    block_category = {
        (row.get("Block") or "").strip(): _classify_block_category(row, owner_types)
        for row in block_rows
        if (row.get("Block") or "").strip()
    }
    interaction_matrix_path = repo_root / "artifacts/stage2_mirco_arc/interaction_matrix.csv"
    matrix_requirement_ids = _read_matrix_requirement_ids(interaction_matrix_path)
    source_content_findings = check_source_traceability_content(
        trace_details,
        source_catalog_rows,
        matrix_requirement_ids
        | _read_reset_clock_table_requirement_ids(summary_path)
        | _read_interrupt_table_requirement_ids(summary_path)
        | direct_supplementary_ids,
        "drs_req_id",
        "DRS",
    )
    if source_content_findings:
        status = "fail"
        findings.extend(source_content_findings[:20])
    authored_content_findings = check_authored_markdown_content(
        drs_md.read_text(encoding="utf-8") if drs_md.exists() else "",
        trace_details,
        source_catalog_rows,
        matrix_requirement_ids
        | _read_reset_clock_table_requirement_ids(summary_path)
        | _read_interrupt_table_requirement_ids(summary_path)
        | direct_supplementary_ids,
        "drs_req_id",
        "DRS",
    )
    if authored_content_findings:
        status = "fail"
        findings.extend(authored_content_findings[:20])
    if drs_md.exists() and interaction_matrix_path.exists():
        function_findings = _check_function_contract(
            drs_md.read_text(encoding="utf-8"),
            trace_details,
            {(row.get("Block") or "").strip(): (row.get("Function") or "").strip() for row in block_rows if (row.get("Block") or "").strip()},
            matrix_requirement_ids,
            _read_source_section_owners(summary_path),
            _read_approved_requirement_owners(req_block_trace_csv),
            _read_reset_clock_table_requirement_ids(summary_path) if summary_path.exists() else set(),
            _read_interrupt_table_requirement_ids(summary_path) if summary_path.exists() else set(),
        )
        if function_findings:
            status = "fail"
            findings.extend(function_findings[:20])
        from run_drs_gen_spec_agent import validate_drs_descriptive_artifacts
        descriptive_findings = validate_drs_descriptive_artifacts(repo_root)
        if descriptive_findings:
            status = "fail"
            findings.extend(descriptive_findings[:20])
    # DRS accepts both digital logic blocks and power/clock support blocks.
    # Some digital requirements are legitimately owned by power/clock control logic.
    drs_allowed_blocks = {
        block_name
        for block_name, category in block_category.items()
        if category in {BLOCK_CLASS_DIGITAL, BLOCK_CLASS_POWER}
    }

    unmapped_trace_rows: List[Dict[str, str]] = []
    for row in trace_details:
        if (row.get("source_req_id") or "") in matrix_requirement_ids:
            continue
        owning = row.get("owning_block", "")
        tokens = _split_blocks(owning)
        if not tokens or all(token.lower() == "unassigned" for token in tokens):
            continue
        has_allowed_block = any(token in drs_allowed_blocks for token in tokens)
        if not has_allowed_block:
            unmapped_trace_rows.append(row)

    if unmapped_trace_rows:
        status = "fail"
        findings.append(
            "Requirements not mapped to included digital blocks: "
            + ", ".join((r.get("source_req_id") or r.get("drs_req_id") or "unknown") for r in unmapped_trace_rows[:20])
        )

    if drs_md.exists():
        raw_text = drs_md.read_text(encoding="utf-8")
        covers_findings = _check_srs_covers_alignment(
            raw_text,
            trace_details,
            srs_trace_details,
            approved_targets,
        )
        if covers_findings:
            status = "fail"
            findings.extend(covers_findings[:20])
        text = raw_text.lower()
        if "0. document navigation" not in text:
            status = "fail"
            findings.append("DRS is missing the required '0. Document Navigation' section")
        if "table of contents" not in text:
            status = "fail"
            findings.append("DRS is missing a table of contents section")
        if "internal index" not in text:
            status = "fail"
            findings.append("DRS is missing an internal index section")
        if "document control" not in text:
            status = "fail"
            findings.append("DRS is missing a document control section")
        if "table of tables" not in text:
            status = "fail"
            findings.append("DRS is missing a table of tables section")
        if "category convention" not in text:
            status = "fail"
            findings.append("DRS is missing a Category Convention section/table")
        else:
            if not _has_markdown_table_with_columns(raw_text, ["category", "scope"]):
                status = "fail"
                findings.append("DRS Category Convention table is missing required columns (at least Category and Scope)")

        if "digital" not in text:
            findings.append("DRS appears to lack digital-focused narrative")

        authored_ids = re.findall(r"^\s*\*\*\[(DRS-REQ-\d{3})\]\s+Requirement:\*\*\s*$", raw_text, flags=re.M)
        has_top_level_integration_section = bool(
            re.search(r"^##\s+\d+\.\s+Top-level integration requirements(?:\s+\{#[^}]+\})?\s*$", raw_text, flags=re.M)
        )
        if not authored_ids and not has_top_level_integration_section:
            status = "fail"
            findings.append("DRS is missing authored requirement entries or the top-level integration requirements section")
        if re.search(r"^\s*(?:-\s*)?Requirement ID:\s*DRS-REQ-\d{3}\b", raw_text, flags=re.M):
            status = "fail"
            findings.append("DRS markdown uses deprecated 'Requirement ID: DRS-REQ-xxx' format; expected '[DRS-REQ-xxx] Requirement:'")
        if re.search(r"^\s*####\s+DRS-REQ-\d{3}\b", raw_text, flags=re.M):
            status = "fail"
            findings.append("DRS markdown uses deprecated '#### DRS-REQ-xxx' heading format; expected '[DRS-REQ-xxx] Requirement:'")
        if re.search(
            r"^\s*####\s+DRS-REQ-\d{3}[^\n]*\n\s*-\s*Statement:\s*",
            raw_text,
            flags=re.M,
        ):
            status = "fail"
            findings.append("DRS markdown uses deprecated '- Statement:' authored field under DRS-REQ headings")
        if len(authored_ids) != len(set(authored_ids)):
            status = "fail"
            findings.append("DRS markdown contains duplicate DRS-REQ IDs")
        if set(authored_ids) - set(trace_ids):
            status = "fail"
            findings.append("DRS markdown contains authored IDs absent from DRS traceability")
        authored_blocks = re.findall(
            r"^\s*\*\*\[(DRS-REQ-\d{3})\]\s+Requirement:\*\*\s*\n(.*?)(?=^\s*\*\*\[DRS-REQ-\d{3}\]\s+Requirement:\*\*\s*$|\Z)",
            raw_text,
            flags=re.M | re.S,
        )
        if any(not re.search(r"^\s*(?:-\s*)?Covers:\s*[A-Z][A-Z0-9_-]*\s*$", block, flags=re.M) for _req_id, block in authored_blocks):
            status = "fail"
            findings.append("DRS markdown contains authored DRS-REQ entries without valid SRS or supplementary-source Covers linkage")
        if re.search(r"^\s*\[(?!DRS-REQ-\d{3}\])[A-Z][A-Z0-9_\-]*\]\s+Requirement:?\s*$", raw_text, flags=re.M):
            status = "fail"
            findings.append("DRS markdown contains raw source requirement headers; only DRS-REQ authored headers are allowed")

        if "linked requirements" in text:
            status = "fail"
            findings.append("DRS markdown contains deprecated 'Linked requirements' wording; expected 'Covers'")
        unresolved_directives = [
            "Summarize high-level system behavior derived from requirements and micro-architecture artifacts.",
            "Describe current-project high-level behavior using only current Stage 1 and Stage 2A artifacts; do not reuse wording or identifiers from other projects.",
            "This section is generated from current Stage 1 and Stage 2A artifacts.",
        ]
        if any(directive in raw_text for directive in unresolved_directives):
            status = "fail"
            findings.append("DRS markdown contains unresolved template directive text in narrative sections")
        if "mapped requirements by digital block" in text:
            status = "fail"
            findings.append(
                "DRS markdown contains redundant mapped-summary section; mapped items shall be captured atomically in project-specific sub-block requirement paragraphs"
            )

        project_section = re.search(
            r"##\s+\d+\.\s+Project-specific digital block sections(.*?)(\n##\s+\d+\.|\n##\s+Assumptions|\n##\s+Missing|\Z)",
            raw_text,
            flags=re.S,
        )
        if project_section:
            req_ids = re.findall(r"^\s*\*\*\[(DRS-REQ-\d{3})\]\s+Requirement:\*\*\s*$", project_section.group(1), flags=re.M)
            if not req_ids:
                status = "fail"
                findings.append("Project-specific digital sub-block requirement paragraphs have no atomic DRS-REQ entries")
            elif len(req_ids) != len(set(req_ids)):
                status = "fail"
                findings.append("Project-specific digital sub-block requirement paragraphs contain duplicate DRS-REQ IDs")

            blocks = re.split(r"(?=^###\s+\d+\.\d+\s+)", project_section.group(1), flags=re.M)
            for block_text in blocks:
                if not block_text.strip().startswith("###"):
                    continue
                local_req_ids = re.findall(r"^\s*\*\*\[(DRS-REQ-\d{3})\]\s+Requirement:\*\*\s*$", block_text, flags=re.M)
                local_covers = re.findall(r"^\s*(?:-\s*)?Covers:\s*(.+?)\s*$", block_text, flags=re.M)
                local_statements = re.findall(r"^\s*(The\s+.+?\s+block\s+shall\s+implement:\s*.+?)\s*$", block_text, flags=re.M)
                if re.search(r"^\s*(?:-\s*)?Statement:\s*", block_text, flags=re.M):
                    status = "fail"
                    findings.append("DRS authored entries must not use the legacy 'Statement:' field")

                if not local_req_ids and not re.search(r"^Source interface table\s+\d+:", block_text, flags=re.M):
                    status = "fail"
                    findings.append("A project-specific digital sub-block paragraph has no atomic DRS-REQ entries")
                    continue
                if len(local_req_ids) != len(local_covers):
                    status = "fail"
                    findings.append("A project-specific digital sub-block paragraph has mismatched Requirement ID and Covers counts")
                if len(local_req_ids) != len(local_statements):
                    status = "fail"
                    findings.append("A project-specific digital sub-block paragraph has mismatched Requirement ID and Statement counts")

                for covers_value in local_covers:
                    if not _is_single_upstream_id(covers_value):
                        status = "fail"
                        findings.append("Atomic Covers entry must contain exactly one upstream SRS-REQ-xxx ID")
                        break

                block_header = re.search(r"^###\s+\d+\.\d+\s+(.+?)\s*$", block_text, flags=re.M)
                block_name = _normalize_block_heading_name(block_header.group(1) if block_header else "")
                for statement in local_statements:
                    if "the following atomic functionality" in statement.lower():
                        status = "fail"
                        findings.append("Project-specific digital sub-block requirement statement uses deprecated filler phrase 'the following atomic functionality'")
                        break
                    if block_name and not statement.startswith(f"The {block_name} block shall implement:"):
                        status = "fail"
                        findings.append(
                            f"Project-specific digital sub-block statement format mismatch for block {block_name}; expected 'The {block_name} block shall implement: ...'"
                        )
                        break
                    if re.search(r"\b(?:DDS_[A-Z0-9_]+|(?:SYS|ANA|DIG|XDN)-RQ-\d+)\b", statement):
                        status = "fail"
                        findings.append("DRS authored statement must not contain an upstream requirement ID")
                        break

            listed = re.findall(r"^###\s+\d+\.\d+\s+(.+?)\s*$", project_section.group(1), flags=re.M)
            for raw_block_name in listed:
                block_name = _normalize_block_heading_name(raw_block_name)
                category = block_category.get(block_name, "unknown")
                if category == BLOCK_CLASS_ANALOG:
                    status = "fail"
                    findings.append(
                        f"Block in project-specific digital section is classified analog by architecture data: {block_name}"
                    )

    io_findings, io_report = check_source_coverage(
        repo_root,
        "drs",
        drs_md,
        repo_root / "artifacts/stage5_drs/digital_requirements_specification.docx",
        source_rows=list(source_catalog_rows.values()),
        report_name="stage_drs_source_structural_coverage_report.md",
    )
    if io_findings:
        status = "fail"
        findings.extend(io_findings[:20])
    hierarchy_coverage_report = write_hierarchy_coverage_report(repo_root)
    out = repo_root / "artifacts/orchestrator/stage_drs_crosscheck_report.md"
    lines = [
        "# Stage DRS Crosscheck Report",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        f"Status: {status}",
        "",
        "## Summary",
        f"- Traceability rows: {trace_rows}",
        f"- Unmapped to included digital blocks: {len(unmapped_trace_rows)}",
        f"- Source-baselined hierarchy coverage: {hierarchy_coverage_report.relative_to(repo_root).as_posix()}",
        f"- Source structural coverage: {io_report.relative_to(repo_root).as_posix()}",
        "",
        "## Findings",
    ]
    if findings:
        lines.extend([f"- {f}" for f in findings])
    else:
        lines.append("- None")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if status != "pass":
        print(f"DRS crosscheck: FAIL ({out})")
        _append_log(repo_root, script_name, "FAIL")
        return 1

    print(f"DRS crosscheck: PASS ({out})")
    _append_log(repo_root, script_name, f"PASS rows={trace_rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
