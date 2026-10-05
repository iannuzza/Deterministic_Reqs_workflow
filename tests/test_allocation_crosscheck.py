from pathlib import Path
import csv
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from allocation_ledger import write_allocation_ledger  # noqa: E402
from requirement_allocation_policy import allocation_row  # noqa: E402
from run_allocation_crosscheck import run  # noqa: E402


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def test_crosscheck_reports_normal_and_direct_paths(tmp_path: Path):
    ledger = allocation_row(
        req_id="SRC-001", source_type="primary", spec_level="DRS",
        requirement_class="top_digital_architecture", owning_domain="digital",
        actual_targets=(), lineage_mode="normal_hierarchical",
    )
    direct = allocation_row(
        req_id="SRC-002", source_type="primary", spec_level="Digital IPOS",
        requirement_class="block_local_digital", owning_block="CTRL",
        actual_targets=(), lineage_mode="direct_source_to_ipos",
    )
    ledger_path = tmp_path / "artifacts/traceability_reports/requirement_allocation_ledger.csv"
    write_allocation_ledger(ledger_path, [ledger, direct])
    _write(tmp_path / "artifacts/stage5_drs/drs_traceability_matrix.csv", [{"source_req_id": "SRC-001"}])
    _write(tmp_path / "artifacts/stage6_digital_ipos/ipos_traceability_matrix.csv", [{"source_req_id": "SRC-002"}])
    json_path, markdown_path = run(tmp_path)
    summary = json.loads(json_path.read_text(encoding="utf-8"))
    assert summary["by_coverage_status"]["covered"] == 2
    assert summary["by_lineage_mode"]["direct_source_to_ipos"] == 1
    assert markdown_path.exists()
