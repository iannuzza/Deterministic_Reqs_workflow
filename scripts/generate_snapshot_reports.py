"""Generate derived SRS, DRS, and ARS XLSX reports from an approved snapshot."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from approved_snapshot_resolver import resolve_complete_authoritative_input
from report_generation_service import generate_snapshot_report
from validate_downstream_coherence import approved_primary_source_name


HIERARCHY_REPORTS = {
    "srs": {
        "stage": "3",
        "upstream_label": "Top Specification",
        "upstream_path": None,
        "upstream_id": "source_req_id",
        "downstream_label": "SRS",
        "downstream_path": "artifacts/stage3_srs/srs_traceability_matrix.csv",
        "downstream_id": "srs_req_id",
    },
    "drs": {
        "stage": "4",
        "upstream_label": "SRS",
        "upstream_path": "artifacts/stage3_srs/srs_traceability_matrix.csv",
        "upstream_id": "srs_req_id",
        "downstream_label": "DRS",
        "downstream_path": "artifacts/stage5_drs/drs_traceability_matrix.csv",
        "downstream_id": "drs_req_id",
    },
    "ars": {
        "stage": "5",
        "upstream_label": "SRS",
        "upstream_path": "artifacts/stage3_srs/srs_traceability_matrix.csv",
        "upstream_id": "srs_req_id",
        "downstream_label": "ARS",
        "downstream_path": "artifacts/stage4_ars/ars_traceability_matrix.csv",
        "downstream_id": "ars_req_id",
    },
    "digital_ipos": {
        "stage": "6",
        "upstream_label": "DRS",
        "upstream_path": "artifacts/stage5_drs/drs_traceability_matrix.csv",
        "upstream_id": "drs_req_id",
        "downstream_label": "Digital IPOS",
        "downstream_path": "artifacts/stage6_digital_ipos/ipos_traceability_matrix.csv",
        "downstream_id": "ipos_req_id",
    },
    "analog_ipos": {
        "stage": "7",
        "upstream_label": "ARS",
        "upstream_path": "artifacts/stage4_ars/ars_traceability_matrix.csv",
        "upstream_id": "ars_req_id",
        "downstream_label": "Analog IPOS",
        "downstream_path": "artifacts/stage7_analog_ipos/ipos_traceability_matrix.csv",
        "downstream_id": "ipos_req_id",
    },
}
TRACEABILITY_REPORT_DIR = Path("artifacts/traceability_reports")
SOURCE_REPORTS = {
    "primary_source": ("Primary Source Requirements", "artifacts/stage1_requirements/requirements_summary.csv", "primary_source_requirements.xlsx"),
    "integrated_sources": ("Source Spec Integrated Requirements", "artifacts/stage1_requirements/integrated_requirements.csv", "source_spec_integrated_reqs.xlsx"),
}


def _classify_integrated_source_rows(
    rows: list[dict[str, str]], primary_ids: set[str], primary_source_name: str,
) -> list[dict[str, str]]:
    classified = []
    for row in rows:
        source_name = Path(str(row.get("source_spec") or "").replace("\\", "/")).name
        source_type = (
            "Supplementary" if source_name and source_name.casefold() != primary_source_name.casefold()
            else "Primary" if row.get("id") in primary_ids else ""
        )
        if not source_type:
            raise RuntimeError(f"Integrated requirement has no identified source: {row.get('id', '')}")
        columns = [(key, value) for key, value in row.items() if key != "source_type"]
        classified.append(dict(columns[:3] + [("source_type", source_type)] + columns[3:]))
    return classified


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise RuntimeError(f"Required traceability matrix is missing: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _source_rows(rows) -> list[dict[str, str]]:
    return [
        {
            "source_req_id": str(row.get("source_req_id") or row.get("id") or "").strip(),
            "canonical_id": str(row.get("canonical_id") or row.get("id") or "").strip(),
            "requirement_statement": str(row.get("statement") or row.get("requirement_statement") or "").strip(),
        }
        for row in rows
        if str(row.get("source_req_id") or row.get("id") or "").strip()
    ]


def _hierarchy_rows(upstream_rows: list[dict[str, str]], downstream_rows: list[dict[str, str]], spec: dict[str, str]) -> list[dict[str, str]]:
    downstream_by_source: dict[str, list[dict[str, str]]] = {}
    for row in downstream_rows:
        source_id = row.get("source_req_id", "")
        if source_id:
            downstream_by_source.setdefault(source_id, []).append(row)
    result = []
    known_sources = set()
    for upstream in upstream_rows:
        source_id = upstream.get("source_req_id", "")
        known_sources.add(source_id)
        matches = downstream_by_source.get(source_id, [])
        if not matches:
            result.append({
                "upstream_level": spec["upstream_label"], "upstream_req_id": upstream.get(spec["upstream_id"], source_id),
                "downstream_level": spec["downstream_label"], "downstream_req_id": "", "source_req_id": source_id,
                "canonical_id": upstream.get("canonical_id", ""), "traceability_status": "missing_downstream",
                "owning_block": "", "requirement_statement": upstream.get("requirement_statement", ""),
            })
            continue
        for downstream in matches:
            result.append({
                "upstream_level": spec["upstream_label"], "upstream_req_id": upstream.get(spec["upstream_id"], source_id),
                "downstream_level": spec["downstream_label"], "downstream_req_id": downstream.get(spec["downstream_id"], ""),
                "source_req_id": source_id, "canonical_id": downstream.get("canonical_id") or upstream.get("canonical_id", ""),
                "traceability_status": "linked", "owning_block": downstream.get("owning_block") or downstream.get("mapped_block", ""),
                "requirement_statement": downstream.get("requirement_statement", ""),
            })
    for downstream in downstream_rows:
        if downstream.get("source_req_id", "") not in known_sources:
            result.append({
                "upstream_level": spec["upstream_label"], "upstream_req_id": "", "downstream_level": spec["downstream_label"],
                "downstream_req_id": downstream.get(spec["downstream_id"], ""), "source_req_id": downstream.get("source_req_id", ""),
                "canonical_id": downstream.get("canonical_id", ""), "traceability_status": "orphaned_downstream",
                "owning_block": downstream.get("owning_block") or downstream.get("mapped_block", ""),
                "requirement_statement": downstream.get("requirement_statement", ""),
            })
    return result


def _split_ids(value: str) -> set[str]:
    return {item.strip() for item in value.replace(",", ";").split(";") if item.strip()}


def _hierarchy_level_label(
    specification: str,
    allocation_class: str,
    owning_target: str,
) -> str:
    allocation = allocation_class.strip().casefold().replace("-", "_")
    target = owning_target.strip().casefold()
    if "top_digital" in allocation:
        return "top_digital"
    if "top_analog" in allocation:
        return "top_analog"
    if allocation in {"system", "system_architecture", "top_system_architecture"} or target in {"srs", "system"}:
        return "System"
    return specification


def _snapshot_statement_index(source_rows: list[dict[str, str]]) -> dict[str, str]:
    """Index unambiguous requirement text from the approved snapshot by its IDs."""
    statements: dict[str, str] = {}
    ambiguous_ids: set[str] = set()
    for row in source_rows:
        statement = row.get("requirement_statement", "").strip()
        if not statement:
            continue
        for requirement_id in (row.get("canonical_id", ""), row.get("source_req_id", "")):
            requirement_id = requirement_id.strip()
            if not requirement_id or requirement_id in ambiguous_ids:
                continue
            previous = statements.get(requirement_id)
            if previous is not None and previous != statement:
                statements.pop(requirement_id, None)
                ambiguous_ids.add(requirement_id)
            else:
                statements[requirement_id] = statement
    return statements


def _snapshot_statement_for(row: dict[str, str], statements: dict[str, str]) -> str:
    """Return only snapshot-backed text for a generated row; never use derived prose."""
    for requirement_id in (row.get("canonical_id", ""), row.get("source_req_id", "")):
        statement = statements.get(requirement_id.strip(), "")
        if statement:
            return statement
    return ""


def _interaction_matrix_statement(
    source_req_id: str,
    specification: str,
    interaction_rows: list[dict[str, str]],
) -> str:
    """Render one source-backed matrix edge using the shared SRS/ARS/DRS rules."""
    if specification not in {"SRS", "ARS", "DRS"}:
        return ""
    edges = {
        (row.get("From block", "").strip(), row.get("To block", "").strip())
        for row in interaction_rows
        if source_req_id in _split_ids(row.get("Requirement IDs", ""))
    }
    if len(edges) != 1:
        return ""
    source_block, destination_block = next(iter(edges))
    if not source_block or not destination_block:
        return ""
    if specification == "SRS":
        return f"The {source_block} block shall be connected to the {destination_block} block."
    return f"The {source_block} block shall implement: connection to the {destination_block} block."


def _generated_requirement_statement(
    row: dict[str, str],
    specification: str,
    snapshot_statements: dict[str, str],
    approved_source_ids: set[str],
    interaction_rows: list[dict[str, str]],
) -> tuple[str, str]:
    """Resolve generated statement through approved source lineage, never its local ID."""
    source_req_id = row.get("source_req_id", "").strip()
    if source_req_id in approved_source_ids:
        matrix_statement = _interaction_matrix_statement(source_req_id, specification, interaction_rows)
        if matrix_statement:
            return matrix_statement, "Source-backed interaction matrix"
    snapshot_statement = _snapshot_statement_for(row, snapshot_statements)
    if snapshot_statement:
        return snapshot_statement, "Approved canonical snapshot"
    return "", "No unique approved source statement"


def _approved_supplementary_imports(
    source_rows: list[dict[str, str]],
    mapping_rows: list[dict[str, str]],
    primary_name: str,
) -> tuple[list[dict[str, str]], dict[str, set[str]]]:
    """Classify snapshot requirements by approved supplementary source metadata."""
    rows_by_id: dict[str, list[dict[str, str]]] = {}
    for source in source_rows:
        for requirement_id in (source.get("source_req_id", ""), source.get("canonical_id", "")):
            requirement_id = requirement_id.strip()
            if requirement_id:
                rows_by_id.setdefault(requirement_id, []).append(source)

    imports_by_source_id: dict[str, dict[str, str]] = {}
    source_specs_by_id: dict[str, set[str]] = {}
    for mapping in mapping_rows:
        if mapping.get("review_decision", "").strip().casefold() != "approved":
            continue
        source_name = Path(mapping.get("supplementary_source_spec", "").replace("\\", "/")).name
        if not source_name or source_name.casefold() == primary_name.casefold():
            continue
        mapping_ids = {
            value.strip()
            for value in (mapping.get("requirement_id", ""), mapping.get("canonical_requirement_id", ""))
            if value.strip()
        }
        matched_rows = {
            id(source): source
            for requirement_id in mapping_ids
            for source in rows_by_id.get(requirement_id, [])
        }
        if len(matched_rows) != 1:
            continue
        source = next(iter(matched_rows.values()))
        source_req_id = source.get("source_req_id", "").strip()
        canonical_id = source.get("canonical_id", "").strip()
        if not source_req_id:
            continue
        record = {
            "requirement_id": source_req_id,
            "canonical_id": canonical_id,
            "source_req_id": source_req_id,
            "specification": source_name,
            "block": mapping.get("approved_block", "").strip(),
            "statement": source.get("requirement_statement", "").strip(),
            "source_origin_req_ids": mapping.get("source_origin_req_ids", "").strip(),
            "staged_requirement_id": mapping.get("supplementary_staged_id", "").strip(),
            "allocation_class": mapping.get("allocation_class", "").strip(),
            "owning_target": mapping.get("owning_target", "").strip(),
            "owning_domain": mapping.get("owning_domain", "").strip(),
        }
        existing = imports_by_source_id.get(source_req_id)
        if existing and existing["specification"] != source_name:
            imports_by_source_id.pop(source_req_id, None)
            for alias in (source_req_id, canonical_id, *mapping_ids):
                source_specs_by_id.pop(alias, None)
            continue
        imports_by_source_id[source_req_id] = record
        for alias in (source_req_id, canonical_id, *mapping_ids):
            if alias:
                source_specs_by_id.setdefault(alias, set()).add(source_name)
    return list(imports_by_source_id.values()), source_specs_by_id


def _inclusive_requirement_rows(
    repo_root: Path,
    source_rows: list[dict[str, str]],
    snapshot_id: str,
) -> list[dict[str, str]]:
    """Build one filterable row per imported or generated requirement."""
    primary_name = "Unknown primary specification"
    source_index = repo_root / "artifacts/stage1_requirements/ocr_extracts/index.csv"
    if source_index.exists():
        for row in _read_csv(source_index):
            source_file = row.get("source_file", "").strip()
            if source_file:
                primary_name = Path(source_file.replace("\\", "/")).name
                break

    mapping_path = repo_root / "artifacts/stage1_specs/architecture_mapping_preview.csv"
    mapping_rows = _read_csv(mapping_path) if mapping_path.exists() else []
    block_by_id: dict[str, str] = {}
    snapshot_statements = _snapshot_statement_index(source_rows)
    approved_source_ids = {row.get("source_req_id", "").strip() for row in source_rows}
    interaction_path = repo_root / "artifacts/stage2_mirco_arc/interaction_matrix.csv"
    interaction_rows = _read_csv(interaction_path) if interaction_path.exists() else []
    for mapping in mapping_rows:
        requirement_id = (mapping.get("requirement_id") or mapping.get("canonical_requirement_id") or "").strip()
        if not requirement_id or mapping.get("review_decision", "").strip().casefold() != "approved":
            continue
        block = (mapping.get("approved_block") or "").strip()
        if block:
            block_by_id[requirement_id] = block
    supplementary_imports, source_specs_by_id = _approved_supplementary_imports(
        source_rows,
        mapping_rows,
        primary_name,
    )

    generated_records: list[dict[str, str]] = []
    matrix_specs = (
        ("SRS", "artifacts/stage3_srs/srs_traceability_matrix.csv", "srs_req_id"),
        ("ARS", "artifacts/stage4_ars/ars_traceability_matrix.csv", "ars_req_id"),
        ("DRS", "artifacts/stage5_drs/drs_traceability_matrix.csv", "drs_req_id"),
        ("Digital IPOS", "artifacts/stage6_digital_ipos/ipos_traceability_matrix.csv", "ipos_req_id"),
        ("Analog IPOS", "artifacts/stage7_analog_ipos/ipos_traceability_matrix.csv", "ipos_req_id"),
    )
    for level, relative_path, id_field in matrix_specs:
        matrix_path = repo_root / relative_path
        if not matrix_path.exists():
            continue
        for row in _read_csv(matrix_path):
            row_snapshot = row.get("snapshot_id", "").strip()
            if row_snapshot and row_snapshot != snapshot_id:
                continue
            source_id = row.get("source_req_id", "").strip()
            requirement_id = (row.get(id_field) or row.get("requirement_id") or "").strip()
            if not requirement_id and not source_id:
                continue
            source_specs = source_specs_by_id.get(source_id, set())
            if not source_specs and source_id:
                source_specs = {primary_name}
            is_drs_record = level == "DRS"
            approved_statement, statement_source = _generated_requirement_statement(
                row,
                level,
                snapshot_statements,
                approved_source_ids,
                interaction_rows,
            )
            generated_records.append({
                "hierarchy_level": _hierarchy_level_label(
                    level,
                    row.get("allocation_class", ""),
                    row.get("owning_target", ""),
                ),
                "specification": level,
                "record_kind": "generated_requirement",
                "requirement_id": requirement_id,
                "source_req_id": source_id,
                "canonical_id": row.get("canonical_id", "").strip(),
                "imported_source_spec": "; ".join(sorted(source_specs, key=str.casefold)),
                "owning_block": "top_digital" if is_drs_record else (row.get("owning_block") or row.get("mapped_block") or "").strip(),
                "requirement_statement": approved_statement,
                "statement_source": statement_source,
                "snapshot_id": row_snapshot or snapshot_id,
                "allocation_class": row.get("allocation_class", "").strip(),
                "owning_target": row.get("owning_target", "").strip(),
                "owning_domain": row.get("owning_domain", "").strip(),
                "source_origin_req_ids": row.get("source_origin_req_ids", "").strip(),
                "hierarchy_parent_req_ids": row.get("hierarchy_parent_req_ids", "").strip(),
                "covers_upstream_req_id": row.get("covers_upstream_req_id", "").strip(),
            })

    generated_by_source: dict[str, list[dict[str, str]]] = {}
    generated_by_id: dict[str, list[dict[str, str]]] = {}
    for record in generated_records:
        source_id = record["source_req_id"]
        if source_id:
            generated_by_source.setdefault(source_id, []).append(record)
        for related_id in _split_ids(";".join((
            record["requirement_id"],
            record["hierarchy_parent_req_ids"],
            record["covers_upstream_req_id"],
        ))):
            generated_by_id.setdefault(related_id, []).append(record)

    result: list[dict[str, str]] = []

    def append_record(record: dict[str, str], relation_records: list[dict[str, str]], basis: str) -> None:
        related_ids = sorted({
            related["requirement_id"]
            for related in relation_records
            if related.get("requirement_id") and related["requirement_id"] != record.get("requirement_id")
        })
        related_levels = sorted({related["hierarchy_level"] for related in relation_records if related.get("hierarchy_level")})
        result.append({
            "hierarchy_level": record.get("hierarchy_level", "Imported source"),
            "specification": record.get("specification", ""),
            "record_kind": record.get("record_kind", "imported_requirement"),
            "requirement_id": record.get("requirement_id", ""),
            "source_req_id": record.get("source_req_id", ""),
            "canonical_id": record.get("canonical_id", ""),
            "imported_source_spec": record.get("imported_source_spec", record.get("specification", "")),
            "owning_block": record.get("owning_block", ""),
            "related_requirement_ids": "; ".join(related_ids),
            "related_hierarchy_levels": "; ".join(related_levels),
            "hierarchy_domain": record.get("owning_domain", ""),
            "allocation_class": record.get("allocation_class", ""),
            "owning_target": record.get("owning_target", ""),
            "relationship_basis": basis,
            "requirement_statement": record.get("requirement_statement", ""),
            "statement_source": record.get("statement_source", ""),
            "snapshot_id": record.get("snapshot_id", snapshot_id),
            "staged_requirement_id": record.get("staged_requirement_id", ""),
        })

    for source in source_rows:
        source_id = source.get("source_req_id", "").strip()
        if not source_id:
            continue
        source_aliases = {source_id, source.get("canonical_id", "").strip()}
        supplementary_names = {
            name
            for alias in source_aliases
            for name in source_specs_by_id.get(alias, set())
        }
        if supplementary_names:
            continue
        record = {
            "hierarchy_level": "Primary source",
            "specification": primary_name,
            "record_kind": "imported_requirement",
            "requirement_id": source_id,
            "source_req_id": source_id,
            "canonical_id": source.get("canonical_id", ""),
            "imported_source_spec": primary_name,
            "owning_block": block_by_id.get(source_id, ""),
            "requirement_statement": source.get("requirement_statement", ""),
            "statement_source": "Approved canonical snapshot",
            "snapshot_id": snapshot_id,
            "allocation_class": "",
            "owning_target": "",
            "owning_domain": "",
        }
        append_record(record, generated_by_source.get(source_id, []), "Matching source_req_id")

    for source in supplementary_imports:
        aliases = {source["source_req_id"], *_split_ids(source["source_origin_req_ids"])}
        related = [row for alias in aliases for row in generated_by_source.get(alias, [])]
        record = {
            "hierarchy_level": "Supplementary source",
            "specification": source["specification"],
            "record_kind": "imported_requirement",
            "requirement_id": source["requirement_id"],
            "source_req_id": source["source_req_id"],
            "canonical_id": source["canonical_id"],
            "imported_source_spec": source["specification"],
            "owning_block": source["block"],
            "requirement_statement": source["statement"],
            "statement_source": "Approved canonical snapshot" if source["statement"] else "No unique approved snapshot statement",
            "snapshot_id": snapshot_id,
            "staged_requirement_id": source["staged_requirement_id"],
            "allocation_class": source["allocation_class"],
            "owning_target": source["owning_target"],
            "owning_domain": source["owning_domain"],
        }
        append_record(record, related, "Approved supplementary source mapping and source-origin IDs")

    for record in generated_records:
        related = list(generated_by_source.get(record["source_req_id"], []))
        for related_id in _split_ids(";".join((record["hierarchy_parent_req_ids"], record["covers_upstream_req_id"]))):
            related.extend(generated_by_id.get(related_id, []))
        related = list({id(item): item for item in related}.values())
        append_record(record, related, "Matching source_req_id and explicit hierarchy/Covers references")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate direct hierarchy traceability XLSX reports from an approved snapshot.")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--snapshot-id")
    selector.add_argument("--use-latest-approved", action="store_true")
    parser.add_argument("--report", choices=(*HIERARCHY_REPORTS, *SOURCE_REPORTS, "all"), default="all")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    context_path = repo_root / "config" / "project_context.json"
    context = json.loads(context_path.read_text(encoding="utf-8")) if context_path.exists() else {}
    project_id = str(context.get("project_name") or repo_root.name)
    selected = tuple(HIERARCHY_REPORTS) if args.report == "all" else (args.report,)
    report_dir = repo_root / TRACEABILITY_REPORT_DIR
    report_dir.mkdir(parents=True, exist_ok=True)
    if args.report in SOURCE_REPORTS:
        resolved, _selection = resolve_complete_authoritative_input(
            repo_root, "srs", project_id=project_id, snapshot_id=args.snapshot_id
        )
        report_kind, relative_source, filename = SOURCE_REPORTS[args.report]
        catalog_path = repo_root / relative_source
        output = report_dir / filename
        with catalog_path.open("r", encoding="utf-8-sig", newline="") as handle:
            catalog_rows = list(csv.DictReader(handle))
        if args.report == "integrated_sources":
            primary_ids = {row["id"] for row in _read_csv(repo_root / SOURCE_REPORTS["primary_source"][1])}
            primary_name = approved_primary_source_name(repo_root)
            if not primary_name:
                raise RuntimeError("Cannot identify the primary specification from the Stage 1 OCR index")
            catalog_rows = _classify_integrated_source_rows(catalog_rows, primary_ids, primary_name)
        generate_snapshot_report(
            repo_root,
            project_id=project_id,
            snapshot_id=resolved.snapshot_id,
            use_latest_approved=False,
            report_kind=report_kind,
            output_path=output,
            rows=catalog_rows,
            source_catalog_path=catalog_path,
        )
        print(output)
        return 0
    resolved_for_all = None
    source_rows_for_all: list[dict[str, str]] = []
    for kind in selected:
        spec = HIERARCHY_REPORTS[kind]
        stage = spec["stage"]
        resolved, _selection = resolve_complete_authoritative_input(
            repo_root, stage, project_id=project_id, snapshot_id=args.snapshot_id
        )
        if kind == "srs":
            resolved_for_all = resolved
            source_rows_for_all = _source_rows(resolved.rows)
        upstream_rows = _source_rows(resolved.rows) if spec["upstream_path"] is None else _read_csv(repo_root / spec["upstream_path"])
        downstream_rows = _read_csv(repo_root / spec["downstream_path"])
        output = report_dir / f"{kind}_vs_{spec['upstream_label'].lower().replace(' ', '_')}.xlsx"
        generate_snapshot_report(
            repo_root,
            project_id=project_id,
            snapshot_id=resolved.snapshot_id,
            use_latest_approved=False,
            report_kind=f"{spec['downstream_label']} vs {spec['upstream_label']}",
            output_path=output,
            rows=_hierarchy_rows(upstream_rows, downstream_rows, spec),
        )
        print(output)
    if args.report == "all":
        if resolved_for_all is None:
            raise RuntimeError("Unable to resolve the approved snapshot for the inclusive hierarchy workbook")
        output = report_dir / "all_requirements_traceability.xlsx"
        generate_snapshot_report(
            repo_root,
            project_id=project_id,
            snapshot_id=resolved_for_all.snapshot_id,
            use_latest_approved=False,
            report_kind="All Requirements Traceability",
            output_path=output,
            rows=_inclusive_requirement_rows(repo_root, source_rows_for_all, resolved_for_all.snapshot_id),
        )
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
