#!/usr/bin/env python3
"""Extract source I/O-list rows into a provenance-preserving Stage 2A catalog."""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


TABLE_OWNER_ALIASES = {
    "adsp": "ADSP",
    "fifo_ctrl": "Smart FIFO",
    "fifo controller": "Smart FIFO",
    "i2c spi ahb": "I2C_SPI_AHB",
    "i2c_spi_ahb": "I2C_SPI_AHB",
    "i2c/spi ahb": "I2C_SPI_AHB",
    "ispu": "ISPU",
    "main controller": "Main Controller",
    "otp": "OTP",
    "pad mux": "PAD MUX",
    "pmu": "PMU",
    "sensor hub": "Sensor-Hub",
}

STRUCTURAL_TABLE_OWNERS = {
    "i/o list": "STBIOSystem",
    "digital i/o list": "Digital Subsystem",
}

PORT_FIELDS = [
    "Table title",
    "Port name",
    "Direction",
    "Type / details",
    "Owner",
    "Source page",
    "Source file",
    "Ownership status",
]

COVERAGE_FIELDS = [
    "Table title",
    "Owner",
    "Ownership status",
    "First source page",
    "Extracted port rows",
]


def _read_inventory(path: Path) -> set[str]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return {
            (row.get("Block") or "").strip()
            for row in csv.DictReader(handle)
            if (row.get("Block") or "").strip() not in {"", "Unassigned"}
        }


def _read_pages(index_path: Path) -> List[Tuple[str, Path, List[str]]]:
    pages: List[Tuple[str, Path, List[str]]] = []
    with index_path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            text_path = Path((row.get("text_file") or "").strip())
            if not text_path.is_absolute():
                text_path = index_path.parent / text_path
            if not text_path.exists():
                continue
            pages.append((
                (row.get("page") or "").strip(),
                text_path,
                text_path.read_text(encoding="utf-8", errors="ignore").splitlines(),
            ))
    return pages


def _table_title(line: str) -> str:
    clean = re.sub(r"\s+", " ", line).strip(" .")
    if re.search(r"\.{3,}", clean):
        return ""
    if not re.search(r"\bI/O\s+List\b", clean, re.IGNORECASE):
        return ""
    clean = re.sub(r"^\d+(?:\.\d+)*\.?\s*", "", clean)
    clean = re.sub(r"^Table\s+\d+\s*:\s*", "", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\s+TOP\s+I/O\s+List$", " I/O List", clean, flags=re.IGNORECASE)
    return clean.strip(" .")


def _section_title(line: str) -> str:
    match = re.match(r"^\d+(?:\.\d+)+\.?\s+(.+?)\s*$", line)
    return match.group(1).strip() if match else ""


def _table_title_from_section(section: str) -> str:
    if section.strip().lower() == "top pinout list":
        return "Digital I/O List"
    clean = re.sub(r"\b(?:top\s+description|description|integration|ips?)\b", "", section, flags=re.IGNORECASE)
    clean = re.sub(r"\s+", " ", clean).strip(" .:-")
    aliases = {
        "fifo_ctrl": "FIFO Controller",
        "i2c/spi ahb": "I2C/SPI AHB",
        "i2c_spi_ahb": "I2C/SPI AHB",
        "sensorhub": "Sensor Hub",
    }
    clean = aliases.get(clean.lower(), clean)
    known_keys = set(TABLE_OWNER_ALIASES) | {"pad mux", "otp"}
    if clean.lower() not in known_keys:
        return ""
    return f"{clean} I/O List"


def _owner_for_title(title: str, inventory: set[str]) -> Tuple[str, str]:
    structural_owner = STRUCTURAL_TABLE_OWNERS.get(title.lower())
    if structural_owner:
        return structural_owner, "approved"
    key = re.sub(r"\s+", " ", re.sub(r"\b(?:top\s+)?i/o\s+list\b", "", title, flags=re.IGNORECASE)).strip(" -").lower()
    owner = TABLE_OWNER_ALIASES.get(key, "")
    if owner:
        return owner, "approved"
    return "", "unresolved"


def _is_port_header(line: str, next_line: str) -> bool:
    joined = re.sub(r"\s+", " ", f"{line} {next_line}").lower()
    has_name = "port name" in joined or "por name" in joined
    has_direction = "direction" in joined or "directio n" in joined or "directi on" in joined
    return has_name and has_direction


def _is_pin_header(line: str) -> bool:
    return bool(re.search(r"\bPin\s+Name\s+Function\b|\bNr\.\s+Name\s+Function\s+Pin\s+No\.\s+Type\b", line, re.IGNORECASE))


def _parse_port_line(line: str) -> Tuple[str, str, str]:
    clean = re.sub(r"\s+", " ", line).strip()
    match = re.match(r"^(.+?)\s+(input|output|inout|bidirectional)\b\s*(.*)$", clean, re.IGNORECASE)
    if not match:
        return "", "", ""
    name = match.group(1).strip()
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_<>:/\[\].-]*", name):
        return "", "", ""
    return name, match.group(2).lower(), match.group(3).strip()


def extract_catalog(index_path: Path, inventory_path: Path) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    inventory = _read_inventory(inventory_path)
    rows: List[Dict[str, str]] = []
    table_pages: Dict[str, str] = {}
    table_counts: Dict[str, int] = defaultdict(int)
    table_owners: Dict[str, Tuple[str, str]] = {}
    active_title = ""
    active_section = ""
    in_port_table = False
    pin_table = False
    last_row: Dict[str, str] | None = None

    for page, text_path, lines in _read_pages(index_path):
        for index, raw_line in enumerate(lines):
            line = re.sub(r"\s+", " ", raw_line).strip()
            if not line:
                continue
            section = _section_title(line)
            if section and not (in_port_table and re.match(r"^\d+\.\d+\b", line)):
                active_section = section
                active_title = ""
                in_port_table = False
                pin_table = False
                last_row = None
            title = _table_title(line)
            if title:
                active_title = title
                table_pages.setdefault(title, page)
                table_owners.setdefault(title, _owner_for_title(title, inventory))
                in_port_table = False
                pin_table = False
                last_row = None
                continue
            next_line = lines[index + 1] if index + 1 < len(lines) else ""
            if _is_port_header(line, next_line):
                if not active_title:
                    active_title = _table_title_from_section(active_section)
                    if active_title:
                        table_pages.setdefault(active_title, page)
                        table_owners.setdefault(active_title, _owner_for_title(active_title, inventory))
                if not active_title:
                    continue
                in_port_table = True
                pin_table = False
                last_row = None
                continue
            if active_title and _is_pin_header(line):
                in_port_table = True
                pin_table = True
                last_row = None
                continue
            if not in_port_table or not active_title:
                continue
            if re.match(r"^(?:Table\s+\d+|Figure\s+\d+|\d+(?:\.\d+)+\.\s+)", line, re.IGNORECASE):
                in_port_table = False
                pin_table = False
                last_row = None
                continue
            if pin_table:
                pin_match = (
                    re.match(r"^\d+\s+([A-Za-z][A-Za-z0-9_<>:/\[\].-]*)\s+(.+)$", line)
                    or re.match(r"^([A-Za-z][A-Za-z0-9_<>:/\[\].-]*)\s+(.+)$", line)
                )
                name, direction, details = (
                    (pin_match.group(1), "unspecified", pin_match.group(2)) if pin_match else ("", "", "")
                )
            else:
                name, direction, details = _parse_port_line(line)
            if name:
                owner, status = table_owners[active_title]
                last_row = {
                    "Table title": active_title,
                    "Port name": name,
                    "Direction": direction,
                    "Type / details": details,
                    "Owner": owner,
                    "Source page": page,
                    "Source file": text_path.as_posix(),
                    "Ownership status": status,
                }
                rows.append(last_row)
                table_counts[active_title] += 1
            elif last_row and not re.search(r"\b(?:Requirement|Definition|Assumption|Comment):", line, re.IGNORECASE):
                last_row["Type / details"] = " ".join(filter(None, [last_row["Type / details"], line]))

    coverage = []
    for title in sorted(table_pages, key=str.lower):
        owner, status = table_owners[title]
        if table_counts[title] == 0 and status == "approved":
            status = "empty"
        coverage.append({
            "Table title": title,
            "Owner": owner,
            "Ownership status": status,
            "First source page": table_pages[title],
            "Extracted port rows": str(table_counts[title]),
        })
    return rows, coverage


def _write_csv(path: Path, fields: List[str], rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract source I/O-list ports for Stage 2A SysML generation")
    parser.add_argument("--index", default="artifacts/stage1_requirements/ocr_extracts/index.csv")
    parser.add_argument("--inventory", default="artifacts/stage2_mirco_arc/block_inventory.csv")
    parser.add_argument("--output", default="artifacts/stage2_mirco_arc/source_port_catalog.csv")
    parser.add_argument("--coverage", default="artifacts/stage2_mirco_arc/source_io_table_coverage.csv")
    args = parser.parse_args()

    rows, coverage = extract_catalog(Path(args.index), Path(args.inventory))
    _write_csv(Path(args.output), PORT_FIELDS, rows)
    _write_csv(Path(args.coverage), COVERAGE_FIELDS, coverage)
    unresolved = [row for row in coverage if row["Ownership status"] not in {"approved", "system_context"}]
    print(f"Extracted {len(rows)} ports from {len(coverage)} source I/O tables")
    for row in unresolved:
        print(f"- {row['Ownership status']}: {row['Table title']} (page {row['First source page']})")
    return 2 if unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())