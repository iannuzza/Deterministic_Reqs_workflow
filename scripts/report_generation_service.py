"""Snapshot-only report generation foundations."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Mapping

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo

from audit_log import record_event
from approved_snapshot_resolver import resolve_complete_authoritative_input
from canonical_store import connect, fingerprint, utc_now


REPORT_FIELD_PRIORITY = (
    "requirement_id", "source_req_id", "canonical_id", "parent_id", "block",
    "classification", "requirement_statement", "statement", "status", "notes",
)


def _ordered_fields(rows: list[dict[str, object]]) -> list[str]:
    fields = list(dict.fromkeys(key for row in rows for key in row))
    priority = {name: index for index, name in enumerate(REPORT_FIELD_PRIORITY)}
    return sorted(fields, key=lambda name: (priority.get(name, 1000), fields.index(name)))


def _style_data_sheet(worksheet, fields: list[str], row_count: int) -> None:
    worksheet.freeze_panes = "A2"
    worksheet.sheet_view.showGridLines = False
    worksheet.row_dimensions[1].height = 30
    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E78")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for column_index, field in enumerate(fields, start=1):
        values = [str(worksheet.cell(row, column_index).value or "") for row in range(2, row_count + 2)]
        width = min(60, max(12, len(field) + 2, max((len(value) for value in values), default=0) + 2))
        worksheet.column_dimensions[chr(64 + column_index) if column_index <= 26 else worksheet.cell(1, column_index).column_letter].width = width
    if row_count:
        table = Table(displayName="ReportData", ref=f"A1:{worksheet.cell(row_count + 1, len(fields)).coordinate}")
        table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
        worksheet.add_table(table)
    else:
        worksheet.auto_filter.ref = worksheet.dimensions
    worksheet.sheet_properties.pageSetUpPr.fitToPage = True
    worksheet.page_setup.fitToWidth = 1
    worksheet.page_setup.fitToHeight = 0
    worksheet.print_title_rows = "1:1"


def _write_metadata_sheet(
    workbook: Workbook, report_kind: str, resolved, output_path: Path, row_count: int,
    source_catalog_path: Path | None = None,
) -> None:
    worksheet = workbook.create_sheet("Report Metadata")
    worksheet.sheet_view.showGridLines = False
    worksheet.append(["Catalog export metadata" if source_catalog_path else "Snapshot report metadata", ""])
    worksheet.append(["Report kind", report_kind])
    worksheet.append(["Generated at (UTC)", utc_now()])
    worksheet.append(["Snapshot ID", resolved.snapshot_id])
    worksheet.append(["Snapshot hash", resolved.snapshot_hash])
    worksheet.append(["Resolved source", str(resolved.source_path)])
    worksheet.append(["Output path", str(output_path)])
    worksheet.append(["Row count", row_count])
    worksheet.append(["Authority", "Stage 1 extracted catalog; not canonical snapshot authority" if source_catalog_path else "Approved immutable snapshot; derived artifact"])
    if source_catalog_path:
        worksheet.append(["Catalog source", str(source_catalog_path)])
    worksheet.append(["Partial export", "No"])
    worksheet.column_dimensions["A"].width = 28
    worksheet.column_dimensions["B"].width = 96
    worksheet.freeze_panes = "A2"
    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E78")
    for row in worksheet.iter_rows(min_row=2, max_col=2):
        row[0].font = Font(bold=True, color="1F4E78")
        row[1].alignment = Alignment(vertical="top", wrap_text=True)


def generate_snapshot_report(
    repo_root: Path,
    *,
    project_id: str,
    snapshot_id: str | None,
    use_latest_approved: bool,
    report_kind: str,
    output_path: Path,
    rows: Iterable[Mapping[str, object]],
    source_catalog_path: Path | None = None,
) -> Path:
    resolved, selection = resolve_complete_authoritative_input(
        repo_root, report_kind, project_id=project_id, snapshot_id=snapshot_id
    )
    materialized = [dict(row) for row in rows]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = (list(materialized[0]) if source_catalog_path and materialized else _ordered_fields(materialized)) or ["snapshot_id"]
    if output_path.suffix.lower() == ".xlsx":
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = report_kind[:31]
        worksheet.append(fields)
        for row in materialized:
            worksheet.append([row.get(field, "") for field in fields])
        _style_data_sheet(worksheet, fields, len(materialized))
        _write_metadata_sheet(workbook, report_kind, resolved, output_path, len(materialized), source_catalog_path)
        workbook.properties.title = f"{report_kind} catalog export" if source_catalog_path else f"{report_kind} snapshot report"
        workbook.properties.subject = f"Stage 1 catalog: {source_catalog_path}" if source_catalog_path else f"Derived from approved snapshot {resolved.snapshot_id}"
        workbook.save(output_path)
    else:
        with output_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(materialized)
    connection = connect(repo_root)
    try:
        report_material = {"snapshot_id": resolved.snapshot_id, "kind": report_kind, "output": str(output_path), "row_count": len(materialized)}
        report_id = f"report-{fingerprint(report_material)[:24]}"
        metadata = {"row_count": len(materialized), "fields": fields, "authority": "stage1_extracted_catalog" if source_catalog_path else "approved_snapshot", "source_path": str(source_catalog_path or resolved.source_path), "selection": selection}
        connection.execute("INSERT OR REPLACE INTO report_metadata(report_id, snapshot_id, report_kind, output_format, output_path, source_fingerprint, generated_at, status, metadata_json) VALUES (?, ?, ?, ?, ?, ?, ?, 'generated', ?)", (report_id, resolved.snapshot_id, report_kind, output_path.suffix.lower().lstrip(".") or "csv", str(output_path), fingerprint(materialized) if source_catalog_path else resolved.snapshot_hash, utc_now(), json.dumps(metadata, sort_keys=True)))
        connection.commit()
    finally:
        connection.close()
    record_event(repo_root, event_type="report_generated", entity_type="report", entity_id=report_id, actor="system", message=f"{report_kind} exported from Stage 1 catalog" if source_catalog_path else f"{report_kind} report generated from approved snapshot", project_id=project_id, payload={"snapshot_id": resolved.snapshot_id, "output_path": str(output_path)})
    return output_path
