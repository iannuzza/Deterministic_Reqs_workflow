"""Create source-baselined requirement coverage statistics for the document hierarchy."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
import re
import json
from approved_snapshot_resolver import resolve_complete_authoritative_input
from allocation_ledger import read_csv

from generate_architecture_sysml import block_name, sysml_name
from validate_downstream_coherence import (
    approved_generated_document_dependency_graph,
    approved_traceability_hierarchy,
)


LOWER_LEVEL_DOCUMENTS = {
    "ARS": {
        "traceability_path": Path("artifacts/stage4_ars/ars_traceability_matrix.csv"),
        "scoped_domains": frozenset({"ANA"}),
    },
    "DRS": {
        "traceability_path": Path("artifacts/stage5_drs/drs_traceability_matrix.csv"),
        "scoped_domains": frozenset(),
    },
    "Digital IPOS": {
        "traceability_path": Path("artifacts/stage6_digital_ipos/ipos_traceability_matrix.csv"),
        "scoped_domains": frozenset(),
    },
    "Analog IPOS": {
        "traceability_path": Path("artifacts/stage7_analog_ipos/ipos_traceability_matrix.csv"),
        "scoped_domains": frozenset(),
    },
}


def _read_source_ids(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return {
            (row.get("source_req_id") or row.get("id") or "").strip()
            for row in csv.DictReader(handle)
            if (row.get("source_req_id") or row.get("id") or "").strip()
        }


def _read_source_document_name(index_path: Path) -> str:
    if not index_path.exists():
        return "Unknown source document"
    with index_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            source_file = (row.get("source_file") or "").strip()
            if source_file:
                return Path(source_file.replace("\\", "/")).name
    return "Unknown source document"


def _has_source_category(path: Path, expected_category: str) -> bool:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return any(
            (row.get("category") or "").strip().casefold() == expected_category.casefold()
            and (row.get("source_req_id") or row.get("id") or "").strip()
            for row in csv.DictReader(handle)
        )


def _is_document_applicable(path: Path, scoped_domains: frozenset[str]) -> bool:
    """A scoped document is applicable only when it contains an in-scope requirement."""
    return path.exists() and (
        not scoped_domains
        or any(_has_source_category(path, domain) for domain in scoped_domains)
    )


def _format_coverage(covered: int, total: int) -> str:
    percentage = (covered / total * 100.0) if total else 0.0
    return f"{covered} / {total} ({percentage:.1f}%)"


def _central_edge_statistics(repo_root: Path) -> list[dict[str, object]]:
    """Return the validator-owned RM edge statistics used by all renderers."""
    graph = approved_generated_document_dependency_graph(repo_root)
    return [
        statistic
        for statistic in graph.get("edge_statistics", [])
        if isinstance(statistic, dict)
    ]


def _central_source_spec_edges(repo_root: Path) -> list[dict[str, object]]:
    """Return reciprocal source-spec coverage from the central graph contract."""
    graph = approved_generated_document_dependency_graph(repo_root)
    return [
        edge for edge in graph.get("source_spec_edges", [])
        if isinstance(edge, dict)
    ]


def _central_source_spec_relationship_edges(repo_root: Path) -> list[dict[str, object]]:
    """Return approved provenance-backed links between imported specifications."""
    graph = approved_generated_document_dependency_graph(repo_root)
    return [
        edge for edge in graph.get("source_spec_relationship_edges", [])
        if isinstance(edge, dict)
    ]


def _edge_metric(
    edge_statistics: list[dict[str, object]],
    upstream: str,
    derived: str,
) -> str:
    statistic = next(
        (
            item for item in edge_statistics
            if item.get("upstream_node") == upstream
            and item.get("derived_node") == derived
        ),
        None,
    )
    if statistic is None:
        return "Unavailable"
    return _format_coverage(
        len(statistic.get("covered_unique_upstream_req_ids") or []),
        len(statistic.get("total_unique_upstream_req_ids") or []),
    )


def _read_mapping_by_block(path: Path, reviewed_path: Path | None = None) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    rows_by_id: dict[str, tuple[dict[str, str], dict[str, str]]] = {}
    for source_path in (path, reviewed_path):
        if not source_path or not source_path.exists():
            continue
        with source_path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                req_id = (row.get("Requirement ID") or row.get("requirement_id") or "").strip()
                if req_id:
                    base_row, reviewed_row = rows_by_id.get(req_id, ({}, {}))
                    rows_by_id[req_id] = (row, reviewed_row) if source_path == path else (base_row, row)
    if not rows_by_id:
        return result
    for req_id, (base_row, reviewed_row) in rows_by_id.items():
        mapping = (
            reviewed_row.get("approved_block")
            or base_row.get("Block(s)")
            or base_row.get("Block")
            or reviewed_row.get("candidate_block")
            or ""
        )
        for block in re.split(r"\s*;\s*|\s*,\s*", mapping):
            block = re.sub(r"\s*\[[^]]+\]", "", block).strip()
            if block and block.casefold() != "unassigned":
                result.setdefault(_block_key(block), set()).add(req_id)
    return result


def _block_key(value: str) -> str:
    return sysml_name(block_name(value)).casefold()


def _read_matrix_by_block(path: Path) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    if not path.exists():
        return result
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            req_id = (row.get("source_req_id") or "").strip()
            block = (row.get("owning_block") or row.get("mapped_block") or "").strip()
            if req_id and block and block.casefold() != "unassigned":
                result.setdefault(_block_key(block), set()).add(req_id)
    return result


def _read_sysml_by_block(path: Path) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    if not path.exists():
        return result
    for block_path in sorted(path.glob("*.sysml")):
        text = block_path.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"part\s+def\s+([A-Za-z_][A-Za-z0-9_]*)", text)
        if not match:
            continue
        block = _block_key(match.group(1))
        result[block] = set(re.findall(r'attribute\s+sourceReqId\s*=\s*"([^"]+)"', text))
    return result


def write_hierarchy_coverage_report(repo_root: Path) -> Path:
    """Write source-to-SRS/ARS/DRS coverage to the Stage 5 traceability artifacts."""
    context_path = repo_root / "config/project_context.json"
    context = json.loads(context_path.read_text(encoding="utf-8")) if context_path.exists() else {}
    resolved, _selection = resolve_complete_authoritative_input(
        repo_root, "coverage-report", project_id=str(context.get("project_name") or repo_root.name)
    )
    ledger_path = repo_root / "artifacts/traceability_reports/requirement_allocation_ledger.csv"
    manifest_path = repo_root / "artifacts/traceability_reports/requirement_allocation_materialization.json"
    if not ledger_path.exists() or not manifest_path.exists():
        raise RuntimeError("Cannot calculate hierarchy coverage; allocation materialization is missing")
    ledger_rows = read_csv(ledger_path)
    if any(row.get("snapshot_id") != resolved.snapshot_id for row in ledger_rows):
        raise RuntimeError("Cannot calculate hierarchy coverage; ledger snapshot does not match selected snapshot")
    source_ids = {row.get("req_id", "").strip() for row in ledger_rows if row.get("req_id", "").strip()}
    source_index_path = repo_root / "artifacts/stage1_requirements/ocr_extracts/index.csv"
    srs_path = repo_root / "artifacts/stage3_srs/srs_traceability_matrix.csv"
    ars_path = repo_root / LOWER_LEVEL_DOCUMENTS["ARS"]["traceability_path"]
    drs_path = repo_root / LOWER_LEVEL_DOCUMENTS["DRS"]["traceability_path"]
    digital_ipos_path = repo_root / LOWER_LEVEL_DOCUMENTS["Digital IPOS"]["traceability_path"]
    analog_ipos_path = repo_root / LOWER_LEVEL_DOCUMENTS["Analog IPOS"]["traceability_path"]
    mapping_path = repo_root / "artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv"
    sysml_path = repo_root / "artifacts/stage2_mirco_arc/sysml/blocks"
    required_paths = (srs_path, drs_path)
    missing = [path.as_posix() for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError("Cannot calculate hierarchy coverage; missing: " + ", ".join(missing))

    source_document_name = _read_source_document_name(source_index_path)
    srs_ids = _read_source_ids(srs_path)
    drs_ids = _read_source_ids(drs_path)
    digital_ipos_ids = _read_source_ids(digital_ipos_path) if digital_ipos_path.exists() else set()
    analog_ipos_ids = _read_source_ids(analog_ipos_path) if analog_ipos_path.exists() else set()
    ars_available = ars_path.exists()
    ars_ids = _read_source_ids(ars_path) if ars_available else set()
    ars_applicable = _is_document_applicable(
        ars_path, LOWER_LEVEL_DOCUMENTS["ARS"]["scoped_domains"]
    )
    reviewed_mapping_path = repo_root / "artifacts/stage1_specs/architecture_mapping_preview.csv"
    mapping_by_block = _read_mapping_by_block(mapping_path, reviewed_mapping_path)
    edge_path = repo_root / "artifacts/stage1_requirements/source_matrix_edges.csv"
    if edge_path.exists():
        with edge_path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                req_id = (row.get("source_req_id") or "").strip()
                for block in (row.get("from_block") or "", row.get("to_block") or ""):
                    if req_id and block.strip():
                        mapping_by_block.setdefault(_block_key(block), set()).add(req_id)
    sysml_by_block = _read_sysml_by_block(sysml_path)
    srs_by_block = _read_matrix_by_block(srs_path)
    ars_by_block = _read_matrix_by_block(ars_path) if ars_available else {}
    drs_by_block = _read_matrix_by_block(drs_path)
    digital_ipos_by_block = _read_matrix_by_block(digital_ipos_path)
    analog_ipos_by_block = _read_matrix_by_block(analog_ipos_path)
    concrete_blocks = set(sysml_by_block)
    mapping_by_block = {
        block: ids for block, ids in mapping_by_block.items() if block in concrete_blocks
    }

    srs_covered = source_ids & srs_ids
    ars_covered = source_ids & ars_ids if ars_applicable else set()
    drs_covered = source_ids & drs_ids
    lower_level_covered = ars_covered | drs_covered
    end_to_end_covered = srs_covered & lower_level_covered
    digital_end_to_end = srs_covered & drs_covered & digital_ipos_ids
    analog_end_to_end = srs_covered & ars_covered & analog_ipos_ids
    edge_statistics = _central_edge_statistics(repo_root)
    source_spec_edges = _central_source_spec_edges(repo_root)
    source_spec_relationship_edges = _central_source_spec_relationship_edges(repo_root)

    report_path = repo_root / "artifacts/stage5_drs/requirements_hierarchy_coverage_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Requirement Coverage Across Document Hierarchy",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Basis",
        f"- Source document: `{source_document_name}` (from the Stage 1 OCR index).",
        "- Denominator: unique requirement IDs in the selected allocation ledger; class and coverage status are ledger-based.",
        "- A source requirement is covered by a document when its `source_req_id` appears in that document's traceability matrix.",
        "- ARS and DRS are complementary domain documents. Their union measures lower-level coverage without assuming every source requirement belongs in each document individually.",
        "",
        "## Source Specification Coverage",
        "| Traceability destination | Source requirements covered |",
        "| --- | ---: |",
        f"| SRS | {_format_coverage(len(srs_covered), len(source_ids))} |",
        f"| ARS | {_format_coverage(len(ars_covered), len(source_ids)) if ars_applicable else 'Not applicable: no Analog requirements in ARS'} |",
        f"| DRS | {_format_coverage(len(drs_covered), len(source_ids))} |",
        f"| Digital IPOS | {_format_coverage(len(source_ids & digital_ipos_ids), len(source_ids)) if digital_ipos_path.exists() else 'Unavailable'} |",
        f"| Analog IPOS | {_format_coverage(len(source_ids & analog_ipos_ids), len(source_ids)) if analog_ipos_path.exists() else 'Unavailable'} |",
        f"| ARS or DRS | {_format_coverage(len(lower_level_covered), len(source_ids))} |",
        f"| End-to-end: SRS and (ARS or DRS) | {_format_coverage(len(end_to_end_covered), len(source_ids))} |",
        "",
        "## SRS vs Source Specification Coverage",
        f"- Source requirements: {len(source_ids)}",
        f"- Source requirements represented in SRS traceability: {len(srs_covered)}",
        f"- SRS coverage: {_format_coverage(len(srs_covered), len(source_ids))}",
        "- Source requirements absent from SRS: " + (", ".join(sorted(source_ids - srs_ids)) or "None"),
        "",
        "## Hierarchy Link Coverage",
        "| Link | Coverage |",
        "| --- | ---: |",
        f"| Source -> SRS | {_format_coverage(len(srs_covered), len(source_ids))} |",
        f"| SRS -> ARS | {_edge_metric(edge_statistics, 'SRS', 'ARS') if ars_applicable else 'Not applicable: no Analog requirements in ARS'} |",
        f"| SRS -> DRS | {_edge_metric(edge_statistics, 'SRS', 'DRS')} |",
        f"| DRS -> Digital IPOS | {_edge_metric(edge_statistics, 'DRS', 'Digital IPOS') if digital_ipos_path.exists() else 'Unavailable'} |",
        f"| ARS -> Analog IPOS | {_edge_metric(edge_statistics, 'ARS', 'Analog IPOS') if ars_applicable and analog_ipos_path.exists() else ('Not applicable' if not ars_applicable else 'Unavailable')} |",
        f"| Source -> SRS -> DRS -> Digital IPOS | {_format_coverage(len(digital_end_to_end), len(source_ids)) if digital_ipos_path.exists() else 'Unavailable'} |",
        f"| Source -> SRS -> ARS -> Analog IPOS | {_format_coverage(len(analog_end_to_end), len(source_ids)) if ars_applicable and analog_ipos_path.exists() else ('Not applicable' if not ars_applicable else 'Unavailable')} |",
        "",
        "## Reciprocal Imported Source Specification Coverage",
        "- This source-spec coverage is separate from approved RM `Covers` edge coverage.",
        "- Source coverage is unique imported source requirement IDs represented in the target divided by IDs in that source specification.",
        "- Target coverage is unique target requirement IDs linked to that source divided by IDs in the target specification or block.",
        "| Imported source specification | Generated specification or block | Source coverage | Target coverage |",
        "| --- | --- | ---: | ---: |",
    ]
    for edge in source_spec_edges:
        source_coverage = edge.get("source_coverage") or {}
        target_coverage = edge.get("target_coverage") or {}
        source_value = _format_coverage(
            len(source_coverage.get("covered_unique_source_req_ids") or []),
            len(source_coverage.get("total_unique_source_req_ids") or []),
        )
        target_value = (
            _format_coverage(
                len(target_coverage.get("covered_unique_target_req_ids") or []),
                len(target_coverage.get("total_unique_target_req_ids") or []),
            )
            if target_coverage.get("total_unique_target_req_ids") else "Not applicable: target has no requirements"
        )
        lines.append(
            f"| {edge.get('source_specification', '')} | {edge.get('target_specification', edge.get('target', ''))} "
            f"| {source_value} | {target_value} |"
        )
    lines.extend([
        "",
        "### Approved Imported Specification Relationships",
        "- Links appear only when approved source-origin or hierarchy-parent IDs match between specifications.",
        "| Source specification | Related specification | Shared IDs / source scope | Shared IDs / related scope |",
        "| --- | --- | ---: | ---: |",
    ])
    for edge in source_spec_relationship_edges:
        source_coverage = edge.get("source_coverage") or {}
        target_coverage = edge.get("target_coverage") or {}
        lines.append(
            f"| {edge.get('source_specification', '')} | {edge.get('target_specification', '')} "
            f"| {_format_coverage(int(source_coverage.get('covered') or 0), int(source_coverage.get('total') or 0))} "
            f"| {_format_coverage(int(target_coverage.get('covered') or 0), int(target_coverage.get('total') or 0))} |"
        )
    lines.extend([
        "",
        "## Central RM Dependency Edge Statistics",
        "- The central downstream validator owns this payload and methodology.",
        "- Each edge is `covered unique upstream requirement IDs / total unique upstream requirement IDs`; duplicate IDs and downstream row counts are excluded.",
        "| Upstream node | Derived node | Edge type | Coverage |",
        "| --- | --- | --- | ---: |",
    ])
    for statistic in edge_statistics:
        lines.append(
            f"| {statistic.get('upstream_node', '')} | {statistic.get('derived_node', '')} | "
            f"{statistic.get('edge_type', '')} | "
            f"{_format_coverage(len(statistic.get('covered_unique_upstream_req_ids') or []), len(statistic.get('total_unique_upstream_req_ids') or []))} |"
        )
    lines.extend([
        "",
        "## Coverage Gaps",
        "- ARS retained context rows excluded from coverage: " + (
            str(len(ars_ids)) if ars_available and not ars_applicable else "None"
        ),
        "- Missing from SRS: " + (", ".join(sorted(source_ids - srs_ids)) or "None"),
        "- Missing from both ARS and DRS: " + (", ".join(sorted(source_ids - lower_level_covered)) or "None"),
        "- Missing from DRS -> Digital IPOS: " + (", ".join(sorted(drs_ids - digital_ipos_ids)) if digital_ipos_path.exists() else "Unavailable"),
        "- Missing from ARS -> Analog IPOS: " + (", ".join(sorted(ars_ids - analog_ipos_ids)) if ars_applicable and analog_ipos_path.exists() else ("Not applicable" if not ars_applicable else "Unavailable")),
        "- Present downstream without a source requirement: " + (
            ", ".join(sorted((srs_ids | ars_ids | drs_ids | digital_ipos_ids | analog_ipos_ids) - source_ids)) or "None"
        ),
        "",
        "## Per-Block Requirement ID Coverage",
        "- These are `Mapped requirement coverage` metrics, distinct from the System Traceability node's `Source-ledger coverage` and from `Upstream edge coverage`.",
        "- Mapped requirement denominators come from the Stage 2 mapping. SysML counts are read from `attribute sourceReqId` in each generated block file; SRS, ARS, and DRS counts are read from each document traceability matrix.",
        "- A mapped requirement is covered when the same source requirement ID appears in both the mapping and the destination artifact.",
        "",
        "| Block | Mapped IDs | SysML block file | SRS mapped coverage | ARS mapped coverage | DRS mapped coverage | Digital IPOS mapped coverage | Analog IPOS mapped coverage |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for block in sorted(set(mapping_by_block) | set(sysml_by_block) | set(srs_by_block) | set(ars_by_block) | set(drs_by_block) | set(digital_ipos_by_block) | set(analog_ipos_by_block)):
        mapped = mapping_by_block.get(block, set())
        sysml_ids = sysml_by_block.get(block, set())
        srs_block_ids = srs_by_block.get(block, set())
        ars_block_ids = ars_by_block.get(block, set())
        drs_block_ids = drs_by_block.get(block, set())
        digital_ipos_block_ids = digital_ipos_by_block.get(block, set())
        analog_ipos_block_ids = analog_ipos_by_block.get(block, set())
        denominator = len(mapped)
        lines.append(
            f"| {block} | {denominator} | {_format_coverage(len(mapped & sysml_ids), denominator)} | "
            f"{_format_coverage(len(mapped & srs_block_ids), denominator)} | "
            f"{_format_coverage(len(mapped & ars_block_ids), denominator)} | "
            f"{_format_coverage(len(mapped & drs_block_ids), denominator)} |"
            f" {_format_coverage(len(mapped & digital_ipos_block_ids), denominator)} |"
            f" {_format_coverage(len(mapped & analog_ipos_block_ids), denominator)} |"
        )
    lines.extend([
        "",
        "## Cross-Artifact ID Sets",
        "| Comparison | Common source IDs |",
        "| --- | ---: |",
        f"| Source specification -> SysML block files | {_format_coverage(len(source_ids & set().union(*sysml_by_block.values()) if sysml_by_block else set()), len(source_ids))} |",
        f"| Source specification -> SRS | {_format_coverage(len(source_ids & srs_ids), len(source_ids))} |",
        f"| Source specification -> ARS | {_format_coverage(len(source_ids & ars_ids), len(source_ids)) if ars_applicable else 'Not applicable'} |",
        f"| Source specification -> DRS | {_format_coverage(len(source_ids & drs_ids), len(source_ids))} |",
        f"| Source specification -> Digital IPOS | {_format_coverage(len(source_ids & digital_ipos_ids), len(source_ids)) if digital_ipos_path.exists() else 'Unavailable'} |",
        f"| Source specification -> Analog IPOS | {_format_coverage(len(source_ids & analog_ipos_ids), len(source_ids)) if analog_ipos_path.exists() else 'Unavailable'} |",
        f"| Source specification -> SRS and ARS and DRS | {_format_coverage(len(source_ids & srs_ids & ars_ids & drs_ids), len(source_ids))} |",
        f"| Source specification -> SRS -> DRS -> Digital IPOS | {_format_coverage(len(digital_end_to_end), len(source_ids)) if digital_ipos_path.exists() else 'Unavailable'} |",
        f"| Source specification -> SRS -> ARS -> Analog IPOS | {_format_coverage(len(analog_end_to_end), len(source_ids)) if ars_applicable and analog_ipos_path.exists() else ('Not applicable' if not ars_applicable else 'Unavailable')} |",
        "",
    ])
    hierarchy = approved_traceability_hierarchy(repo_root)
    lines.extend([
        "## Shared Design And Requirement Management Hierarchy",
        "- Design and Requirement Management views use the same approved hierarchy contract.",
        "- Coverage arrows identify the exact approved upstream requirement or supplementary source.",
        "",
    ])

    def render_hierarchy(node: dict[str, object], depth: int = 0) -> None:
        indent = "  " * depth
        lines.append(f"{indent}- {node.get('label', '')} (`{node.get('artifact', '')}`)")
        for edge in node.get("coverage_edges") or []:
            lines.append(f"{indent}  - Coverage: {edge}")
        for child in node.get("children") or []:
            render_hierarchy(child, depth + 1)

    render_hierarchy(hierarchy)
    lines.append("")
    ledger_path = repo_root / "artifacts/traceability_reports/requirement_allocation_ledger.csv"
    if ledger_path.exists():
        with ledger_path.open("r", encoding="utf-8-sig", newline="") as handle:
            ledger_rows = list(csv.DictReader(handle))
        by_status: dict[str, int] = {}
        by_lineage: dict[str, int] = {}
        for row in ledger_rows:
            by_status[row.get("coverage_status", "")] = by_status.get(row.get("coverage_status", ""), 0) + 1
            by_lineage[row.get("lineage_mode", "")] = by_lineage.get(row.get("lineage_mode", ""), 0) + 1
        lines.extend([
            "## Central Allocation Ledger Accounting",
            "- The allocation ledger is authoritative for class-based target obligations; source-ID presence alone is not a coverage decision.",
            f"- Ledger rows: {len(ledger_rows)}",
            f"- Coverage statuses: `{json.dumps(by_status, sort_keys=True)}`",
            f"- Lineage modes: `{json.dumps(by_lineage, sort_keys=True)}`",
            "- Direct source-to-IPOS and supplementary-source-to-IPOS paths are lineage modes, not coverage statuses.",
            "",
        ])
    report_path.write_text("\n".join(lines), encoding="utf-8")
    requested_report_path = repo_root / "artifacts/stage5_drs/cross_req_id_coverage_report.md"
    requested_report_path.write_text("\n".join(lines), encoding="utf-8")
    return requested_report_path


if __name__ == "__main__":
    report = write_hierarchy_coverage_report(Path(__file__).resolve().parents[1])
    print(report.as_posix())