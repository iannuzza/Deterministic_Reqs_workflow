import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from extract_source_io_catalog import extract_catalog


class MainControllerContinuationTests(unittest.TestCase):
    def test_page_81_output_ports_keep_main_controller_table_context(self):
        repo_root = Path(__file__).resolve().parents[1]
        rows, _ = extract_catalog(
            repo_root / "artifacts/stage1_requirements/ocr_extracts/index.csv",
            repo_root / "artifacts/stage2_mirco_arc/block_inventory.csv",
        )
        expected = {
            "SCANOUTHCLK",
            "HSEL",
            "HADDR",
            "HTRANS",
            "HWRITE",
            "HSIZE",
            "HBURST",
            "HPROT",
            "HWDATA",
        }

        extracted = {
            row["Port name"]: row
            for row in rows
            if row["Port name"] in expected and row["Owner"] == "Main Controller"
        }

        self.assertEqual(set(extracted), expected)
        for row in extracted.values():
            self.assertEqual(row["Direction"], "output")
            self.assertEqual(row["Source page"], "81")
            self.assertEqual(Path(row["Source file"]).name, "DDS_STBIO1_p081.txt")


if __name__ == "__main__":
    unittest.main()