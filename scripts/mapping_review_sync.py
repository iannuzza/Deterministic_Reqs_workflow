"""Synchronize the editable Stage 2 mapping workbook into its authoritative CSV."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from tempfile import NamedTemporaryFile

from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.styles import Protection, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from requirement_allocation_policy import requires_hierarchy_parent
from approved_snapshot_resolver import validate_governed_source_context


DESCRIPTIVE_SHEET = "Descriptive Content Review"
DESCRIPTIVE_REVIEW_FIELDS = ("review_decision", "mapped_block", "domain", "review_rationale")


def write_descriptive_review_sheet(workbook_path: Path, draft: dict) -> None:
    records = draft.get("governed_source_context", {}).get("records", [])
    workbook = load_workbook(workbook_path)
    try:
        if DESCRIPTIVE_SHEET in workbook.sheetnames:
            raise ValueError("Descriptive review sheet already exists; do not overwrite reviewer decisions.")
        sheet = workbook.create_sheet(DESCRIPTIVE_SHEET)
        fields = list(DESCRIPTIVE_REVIEW_FIELDS) + sorted({
            field for record in records for field in record if field not in DESCRIPTIVE_REVIEW_FIELDS
        })
        sheet.append(fields)
        for record in records:
            sheet.append([json.dumps(record[field], sort_keys=True) if isinstance(record.get(field), (dict, list))
                          else str(record.get(field, "")) for field in fields])
        for row in sheet.iter_rows(min_row=2):
            for field, cell in zip(fields, row):
                cell.data_type = "s"
                cell.protection = Protection(locked=field not in DESCRIPTIVE_REVIEW_FIELDS)
                cell.alignment = Alignment(wrap_text=True, vertical="top")
                if field in DESCRIPTIVE_REVIEW_FIELDS:
                    cell.fill = PatternFill("solid", fgColor="FFF2CC")
        for column, field in enumerate(fields, 1):
            sheet.column_dimensions[get_column_letter(column)].width = 75 if field == "statement" else 28
        sheet.freeze_panes = "E2"
        sheet.auto_filter.ref = sheet.dimensions
        sheet.protection.sheet = True
        for column, options in ((1, "pending,approved,rejected"), (3, "digital,analog,mixed_signal,system")):
            validation = DataValidation(type="list", formula1='"' + options + '"', allow_blank=False)
            validation.showErrorMessage = True
            sheet.add_data_validation(validation)
            if records:
                validation.add(f"{get_column_letter(column)}2:{get_column_letter(column)}{len(records) + 1}")
        workbook.save(workbook_path)
    finally:
        workbook.close()


def reviewed_descriptive_context(workbook_path: Path, draft: dict, profile: dict) -> dict | None:
    context = draft.get("governed_source_context")
    if context is None:
        return None
    lock_path = workbook_path.with_name("~$" + workbook_path.name)
    if lock_path.exists():
        raise ValueError("Save and close the architecture workbook before descriptive admission.")
    workbook = load_workbook(workbook_path, data_only=False)
    try:
        if DESCRIPTIVE_SHEET not in workbook.sheetnames:
            raise ValueError("Architecture workbook is missing Descriptive Content Review.")
        sheet = workbook[DESCRIPTIVE_SHEET]
        headers = [str(cell.value or "") for cell in sheet[1]]
        expected_fields = set(DESCRIPTIVE_REVIEW_FIELDS) | {
            field for record in context["records"] for field in record
        }
        if len(headers) != len(set(headers)) or set(headers) != expected_fields:
            raise ValueError("Descriptive review columns differ from the draft.")
        originals = {record["record_id"]: record for record in context["records"]}
        if len(originals) != len(context["records"]):
            raise ValueError("Duplicate descriptive candidate in draft.")
        reviewed = {}
        for cells in sheet.iter_rows(min_row=2):
            if not any(cell.value is not None for cell in cells):
                continue
            if any(cell.data_type == "f" for cell in cells):
                raise ValueError("Formulas are not allowed in descriptive review.")
            values = {field: "" if cell.value is None else str(cell.value) for field, cell in zip(headers, cells)}
            identity = values.get("record_id")
            if identity not in originals or identity in reviewed:
                raise ValueError("Unknown or duplicate descriptive candidate.")
            original = originals[identity]
            for field in expected_fields - set(DESCRIPTIVE_REVIEW_FIELDS):
                expected = original.get(field, "")
                expected = json.dumps(expected, sort_keys=True) if isinstance(expected, (dict, list)) else str(expected)
                if values[field] != expected:
                    raise ValueError("Descriptive candidate text/provenance was changed: " + identity)
            reviewed[identity] = dict(original, **{field: values[field].strip() for field in DESCRIPTIVE_REVIEW_FIELDS})
        if set(reviewed) != set(originals):
            raise ValueError("Descriptive review is missing candidates.")
        result = dict(context, records=[reviewed[record["record_id"]] for record in context["records"]])
        findings = validate_governed_source_context(dict(profile, governed_source_context=result))
        if findings:
            raise ValueError("; ".join(findings))
        return result
    finally:
        workbook.close()


EDITABLE_FIELDS = {
    "approved_classification",
    "review_decision",
    "approved_block",
    "allocation_class",
    "owning_target",
    "allocation_rationale",
    "lineage_mode",
    "source_origin_req_ids",
    "hierarchy_parent_req_ids",
    "lineage_candidate_parent_req_ids",
    "owning_domain",
    "reviewer_notes",
}
ALLOWED_REVIEW_DECISIONS = {
    "approved",
    "reassigned",
    "rejected",
    "pending_review",
    "needs_clarification",
}


def _row_is_valid(record: dict[str, str]) -> bool:
    allocation_targets = {
        "system_level": "srs",
        "top_digital_architecture": "drs",
        "top_analog_architecture": "ars",
        "block_local_digital": "digital ipos",
        "block_local_analog": "analog ipos",
        "descriptive_only": "none",
    }
    classification = (record.get("approved_classification") or "").strip().casefold()
    block = (record.get("approved_block") or "").strip()
    allocation_class = (record.get("allocation_class") or "").strip().casefold()
    owning_target = (record.get("owning_target") or "").strip().casefold()
    rationale = (record.get("allocation_rationale") or "").strip()
    lineage_mode = (record.get("lineage_mode") or "").strip()
    source_origin_req_ids = (record.get("source_origin_req_ids") or "").strip()
    hierarchy_parent_req_ids = (record.get("hierarchy_parent_req_ids") or "").strip()
    if classification not in {"analog", "digital", "system"} or not block:
        return False
    if allocation_class not in allocation_targets or owning_target != allocation_targets[allocation_class]:
        return False
    if not rationale or rationale.startswith("REVIEW_REQUIRED:") or not lineage_mode or not source_origin_req_ids:
        return False
    if allocation_class in {"block_local_digital", "block_local_analog"} and lineage_mode in {"normal_hierarchical", "split_lineage"} and not hierarchy_parent_req_ids:
        return False
    return not (block.casefold() in {"system", "digital", "analog"} and block.casefold() != classification)


def _explicit_parent_candidates(record: dict[str, str], approved_ids: set[str]) -> list[str]:
    """Return only explicit approved requirement IDs from Covers references."""
    statement = record.get("requirement_statement") or ""
    candidates = {
        candidate.strip()
        for covered in re.findall(r"\[\s*Covers\s*:\s*([^\]]+)\]", statement, flags=re.IGNORECASE)
        for candidate in re.split(r"[,;\s]+", covered)
        if candidate.strip() in approved_ids
        and candidate.strip() != (record.get("requirement_id") or "").strip()
    }
    return sorted(candidates)


def _restore_mapping_validations(workbook, worksheet, headers: list[str]) -> None:
    choices = workbook["Approved Block Choices"] if "Approved Block Choices" in workbook.sheetnames else None
    if choices is None:
        raise ValueError("Mapping workbook is missing the Approved Block Choices sheet.")

    worksheet.data_validations.dataValidation = []
    choice_ranges = {
        "approved_block": "A",
        "approved_classification": "B",
        "allocation_class": "C",
        "owning_target": "D",
        "allocation_rationale": "E",
        "lineage_mode": "F",
        "review_decision": "G",
    }
    for field_name, choice_column in choice_ranges.items():
        if field_name not in headers:
            continue
        values = [
            choices.cell(row=row_number, column=ord(choice_column) - ord("A") + 1).value
            for row_number in range(2, choices.max_row + 1)
            if choices.cell(row=row_number, column=ord(choice_column) - ord("A") + 1).value not in (None, "")
        ]
        if not values:
            continue
        field_column = get_column_letter(headers.index(field_name) + 1)
        last_choice_row = len(values) + 1
        validation = DataValidation(
            type="list",
            formula1=f"'Approved Block Choices'!${choice_column}$2:${choice_column}${last_choice_row}",
            allow_blank=field_name == "approved_block",
        )
        validation.errorTitle = f"Invalid {field_name}"
        validation.error = "Choose a value from the drop-down list."
        validation.errorStyle = "stop"
        validation.promptTitle = field_name.replace("_", " ").title()
        validation.prompt = "Choose a value from the approved review choices."
        validation.showErrorMessage = True
        validation.showInputMessage = True
        worksheet.add_data_validation(validation)
        validation.add(f"{field_column}2:{field_column}{worksheet.max_row}")


def sync_mapping_workbook_to_csv(workbook_path: Path, csv_path: Path) -> int:
    """Import the user-edited workbook into the tool-managed CSV."""
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        baseline_records = list(reader)
    if not fieldnames or "requirement_id" not in fieldnames:
        raise ValueError("Mapping review CSV is missing the requirement_id column.")

    workbook = load_workbook(workbook_path, data_only=False)
    try:
        worksheet = workbook["Architecture Mapping Review"]
        rows = list(worksheet.iter_rows(values_only=True))
    finally:
        workbook.close()
    if not rows:
        raise ValueError("Mapping review workbook is empty.")
    headers = [str(value or "").strip() for value in rows[0]]
    if headers != fieldnames:
        raise ValueError("Mapping review workbook columns do not match the generated CSV.")

    baseline_by_id = {(record.get("requirement_id") or "").strip(): record for record in baseline_records}
    workbook_by_id: dict[str, dict[str, str]] = {}
    for row in rows[1:]:
        values = ["" if value is None else str(value).strip() for value in row]
        if not any(values):
            continue
        record = dict(zip(fieldnames, values))
        requirement_id = record.get("requirement_id", "").strip()
        if not requirement_id:
            raise ValueError("Mapping review workbook contains a row without requirement_id.")
        if requirement_id in workbook_by_id:
            raise ValueError(f"Mapping review workbook duplicates requirement_id: {requirement_id}")
        if requirement_id not in baseline_by_id:
            raise ValueError(f"Mapping review workbook contains unknown requirement_id: {requirement_id}")
        workbook_by_id[requirement_id] = record
    missing = sorted(set(baseline_by_id) - set(workbook_by_id))
    if missing:
        raise ValueError("Mapping review workbook is missing requirement IDs: " + ", ".join(missing[:10]))

    synchronized: list[dict[str, str]] = []
    for baseline in baseline_records:
        requirement_id = (baseline.get("requirement_id") or "").strip()
        record = workbook_by_id[requirement_id]
        workbook_decision = (record.get("review_decision") or "").strip()
        baseline_decision = (baseline.get("review_decision") or "").strip()
        record["review_decision"] = workbook_decision or baseline_decision or "pending_review"
        if record["review_decision"].casefold() not in ALLOWED_REVIEW_DECISIONS:
            raise ValueError(
                f"Unsupported review_decision for {requirement_id}: {record['review_decision']}"
            )
        workbook_by_id[requirement_id]["review_decision"] = record["review_decision"]
        approved_ids = {
            candidate_id
            for candidate_id, candidate in baseline_by_id.items()
            if (candidate.get("review_decision") or "").strip().casefold() in {"approved", "reassigned"}
        }
        candidates = _explicit_parent_candidates(record, approved_ids)
        if "lineage_candidate_parent_req_ids" in fieldnames:
            record["lineage_candidate_parent_req_ids"] = ";".join(candidates)
        if (
            not (record.get("hierarchy_parent_req_ids") or "").strip()
            and requires_hierarchy_parent(
                (record.get("allocation_class") or "").strip(),
                (record.get("lineage_mode") or "").strip(),
            )
            and len(candidates) == 1
            and record["review_decision"].casefold() in {"approved", "reassigned"}
        ):
            record["hierarchy_parent_req_ids"] = candidates[0]
        changed = any(
            (record.get(field) or "").strip() != (baseline.get(field) or "").strip()
            for field in EDITABLE_FIELDS - {"review_decision"}
        )
        if changed and record["review_decision"].casefold() in {"pending", "pending_review"} and _row_is_valid(record):
            record["review_decision"] = "approved"
        synchronized.append(record)
    with NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="", dir=csv_path.parent,
        prefix=csv_path.name + ".", suffix=".tmp", delete=False,
    ) as temporary:
        writer = csv.DictWriter(temporary, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(synchronized)
        temporary_path = Path(temporary.name)
    temporary_path.replace(csv_path)

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        persisted = {(row.get("requirement_id") or "").strip(): row for row in csv.DictReader(handle)}
    synchronized_by_id = {
        (record.get("requirement_id") or "").strip(): record for record in synchronized
    }
    mismatched = [
        requirement_id for requirement_id, record in workbook_by_id.items()
        if any(
            persisted.get(requirement_id, {}).get(field, "").strip()
            != synchronized_by_id[requirement_id].get(field, "").strip()
            for field in fieldnames
        )
    ]
    if mismatched:
        raise RuntimeError("Mapping workbook synchronization did not persist approved_block values: " + ", ".join(mismatched[:10]))

    workbook = load_workbook(workbook_path, data_only=False)
    try:
        worksheet = workbook["Architecture Mapping Review"]
        headers = [str(cell.value or "").strip() for cell in worksheet[1]]
        decision_column = headers.index("review_decision") + 1
        approved_fill = PatternFill("solid", fgColor="C6EFCE")
        pending_fill = PatternFill("solid", fgColor="FFC7CE")
        for row_number in range(2, worksheet.max_row + 1):
            decision = str(worksheet.cell(row_number, decision_column).value or "").strip().casefold()
            row_fill = approved_fill if decision == "approved" else pending_fill
            for column_number, field_name in enumerate(headers, start=1):
                if field_name in EDITABLE_FIELDS:
                    worksheet.cell(row_number, column_number).fill = row_fill
        _restore_mapping_validations(workbook, worksheet, headers)
        workbook.save(workbook_path)
    finally:
        workbook.close()
    return len(synchronized)
