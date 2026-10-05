import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from run_drs_gen_spec_agent import _top_digital_coverage_records
from workflow_routing import TOP_DIGITAL_CATEGORY_SPECS, assess_top_digital_coverage, write_top_digital_coverage_audit


class TopDigitalCoverageTests(unittest.TestCase):
    def test_block_local_evidence_cannot_cover_category(self):
        coverage, audit = assess_top_digital_coverage([
            {
                "statement": "The Smart FIFO block shall implement local buffering and overflow handling.",
                "source": "Digital IPOS: Smart FIFO",
                "scope": "block_local",
            }
        ])
        fifo = next(item for item in coverage if item.category.startswith("DMA,"))
        self.assertEqual(fifo.status, "Missing")
        self.assertFalse(any(row.get("statement") for row in audit if row.get("category") == fifo.category))

    def test_integration_evidence_is_scoped_and_provenanced(self):
        records = _top_digital_coverage_records(
            [{"From block": "Main Controller", "To block": "Smart FIFO", "Signal/control": "sample stream"}],
            [{"Interface": "SPI", "Owner": "SPI interface", "Purpose": "register transactions"}],
            [],
        )
        coverage, audit = assess_top_digital_coverage(records)
        self.assertTrue(any(item.status != "Missing" for item in coverage))
        selected = [row for row in audit if row.get("statement")]
        self.assertTrue(selected)
        self.assertTrue(all(row.get("scope") == "integration" for row in selected))
        self.assertTrue(all(row.get("source") for row in selected))

    def test_audit_has_one_row_per_category(self):
        coverage, audit = assess_top_digital_coverage([])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "top_digital_coverage_audit.csv"
            write_top_digital_coverage_audit(path, audit)
            with path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), len(TOP_DIGITAL_CATEGORY_SPECS))
        self.assertEqual({row["category"] for row in rows}, {name for name, _terms in TOP_DIGITAL_CATEGORY_SPECS})
        self.assertEqual(len(coverage), len(rows))


if __name__ == "__main__":
    unittest.main()
