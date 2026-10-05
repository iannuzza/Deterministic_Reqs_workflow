#!/usr/bin/env python3
"""Deterministic coverage checks for source structural tables and ports."""

from __future__ import annotations

import csv
import re
import zipfile
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple
from xml.etree import ElementTree


STATUS_COVERED = "covered"
STATUS_NOT_APPLICABLE = "not_applicable"
STATUS_MISSING_TABLE = "missing_table"
STATUS_MISSING_PORT = "missing_port"


def _read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip()).casefold()


def _docx_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml")
        root = ElementTree.fromstring(xml)
        return " ".join(node.text or "" for node in root.iter() if node.tag.endswith("}t"))
    except (KeyError, OSError, ElementTree.ParseError):
        return ""


def _applicable(table: Dict[str, str], stage: str) -> bool:
    owner = _norm(table.get("Owner", ""))
    title = _norm(table.get("Table title", ""))
    if stage == "sysml":
        return bool(owner) and table.get("Ownership status") == "approved"
    if stage == "srs":
        # Block-owned source I/O is rendered by DRS/ARS and block IPOS specs.
        return table.get("Ownership status") == "requirement_bound"
    if stage == "drs":
        return owner in {
            "adsp", "smart fifo", "i2c_spi_ahb", "ispu", "main controller",
            "otp", "pad mux", "pmu", "sensor-hub", "digital subsystem",
        } or "digital" in title or "i/o list" in title and owner not in {"", "sensor-hub"}
    if stage == "ars":
        return owner in {"pmu", "sensor-hub"} or any(term in title for term in ("analog", "power", "sensor"))
    return False


def _table_marker(table: Dict[str, str]) -> str:
    return f"{table.get('Table title', '')} | owner={table.get('Owner', '')}"


def _table_covered(text: str, table: Dict[str, str]) -> bool:
    title = table.get("Table title", "")
    if not title:
        return False
    normalized = _norm(text)
    if table.get("Ownership status") == "requirement_bound":
        table_number = table.get("Table number", "")
        return bool(table_number) and re.search(rf"\bTable\s+{re.escape(table_number)}\b", text, flags=re.IGNORECASE) is not None
    return _norm(title) in normalized or _norm(f"source interface table") in normalized and _norm(title.replace(" I/O List", "")) in normalized


def _port_covered(text: str, port: Dict[str, str]) -> bool:
    name = port.get("Port name", "")
    if not name:
        return False
    if re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])", text, flags=re.IGNORECASE):
        return True
    return re.search(rf"^\s*-\s*Port name:\s*{re.escape(name)}\s*$", text, flags=re.IGNORECASE | re.MULTILINE) is not None


def _requirement_bound_tables(source_rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    result: List[Dict[str, str]] = []
    for row in source_rows:
        table_title = row.get("source_table_title") or row.get("table_title") or ""
        table_number = row.get("source_table_number") or row.get("table_number") or ""
        if not table_title and not table_number:
            continue
        result.append({
            "Table title": table_title or f"Source Table {table_number}",
            "Owner": row.get("source_section_owner", ""),
            "Ownership status": "requirement_bound",
            "Source requirement IDs": row.get("source_req_id") or row.get("id") or "",
            "Table number": table_number,
        })
    return result


def check_source_coverage(
    repo_root: Path,
    stage: str,
    markdown_path: Path,
    docx_path: Path | None = None,
    sysml_dir: Path | None = None,
    source_rows: Sequence[Dict[str, str]] | None = None,
    stage_active: bool = True,
    report_name: str = "source_structural_coverage_report.md",
) -> Tuple[List[str], Path]:
    """Return blocking findings and write one deterministic coverage report."""
    artifact_dir = repo_root / "artifacts/stage2_mirco_arc"
    coverage_rows = _read_csv(artifact_dir / "source_io_table_coverage.csv")
    port_rows = _read_csv(artifact_dir / "source_port_catalog.csv")
    source_rows = source_rows or []
    tables = coverage_rows + _requirement_bound_tables(source_rows)
    markdown = markdown_path.read_text(encoding="utf-8", errors="ignore") if markdown_path.is_file() else ""
    docx_text = _docx_text(docx_path) if docx_path else ""
    combined = f"{markdown}\n{docx_text}"
    findings: List[str] = []
    report_rows: List[Tuple[str, str, str, str]] = []

    for table in tables:
        title = table.get("Table title", "")
        kind = "requirement_bound" if table.get("Ownership status") == "requirement_bound" else "context"
        applicable = stage_active and (_applicable(table, stage) if kind == "context" else stage in {"srs", "drs", "ars"})
        if not applicable:
            status = STATUS_NOT_APPLICABLE
        elif stage == "sysml":
            owner = re.sub(r"[^A-Za-z0-9_]+", "_", table.get("Owner", "")).strip("_").lower()
            owner_text = ""
            if sysml_dir:
                for path in (sysml_dir / "blocks").glob("*.sysml"):
                    if owner and owner in path.stem.lower():
                        owner_text += path.read_text(encoding="utf-8", errors="ignore")
            has_owned_ports = any(
                port.get("Table title") == title and port.get("Ownership status") == "approved"
                and _port_covered(owner_text, port)
                for port in port_rows
            )
            status = STATUS_COVERED if has_owned_ports else STATUS_MISSING_TABLE
            if status == STATUS_MISSING_TABLE:
                findings.append(f"{stage.upper()} {status}: {title} ({kind})")
        elif not _table_covered(combined, table):
            status = STATUS_MISSING_TABLE
            findings.append(f"{stage.upper()} {status}: {title} ({kind})")
        else:
            status = STATUS_COVERED
        report_rows.append((kind, title, status, table.get("Owner", "")))

        if status != STATUS_COVERED:
            continue
        if kind != "context":
            continue
        for port in port_rows:
            if port.get("Table title") != title or port.get("Ownership status") != "approved":
                continue
            if stage == "sysml":
                owner = re.sub(r"[^A-Za-z0-9_]+", "_", port.get("Owner", "")).strip("_").lower()
                block_text = ""
                if sysml_dir:
                    for path in (sysml_dir / "blocks").glob("*.sysml"):
                        if owner and owner in path.stem.lower():
                            block_text += path.read_text(encoding="utf-8", errors="ignore")
                port_text = block_text
            else:
                port_text = combined
            if _port_covered(port_text, port):
                port_status = STATUS_COVERED
            else:
                port_status = STATUS_MISSING_PORT
                if kind != "context":
                    findings.append(f"{stage.upper()} {port_status}: {title}/{port.get('Port name', '')}")
            report_rows.append(("port", f"{title}/{port.get('Port name', '')}", port_status, port.get("Owner", "")))

    report_path = repo_root / "artifacts/orchestrator" / report_name
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Source Structural Coverage Report",
        "",
        f"Stage: {stage.upper()}",
        "",
        "| Kind | Identity | Status | Owner |",
        "|---|---|---|---|",
    ]
    lines.extend(f"| {kind} | {identity} | {status} | {owner} |" for kind, identity, status, owner in report_rows)
    lines.extend(["", "## Blocking findings", ""])
    lines.extend(f"- {finding}" for finding in findings) if findings else lines.append("- None")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return findings, report_path
