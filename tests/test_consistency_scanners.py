import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from approved_vocabulary import approved_stopwords, load_approved_vocabulary
from authority_consistency_scan import scan


class ConsistencyScannerTests(unittest.TestCase):
    def test_scanner_flags_legacy_and_project_specific_authoritative_code(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "run_stage_demo.py").write_text(
                "from requirement_corpus import load_approved_input\nDDS_STBIO1_0001 = 'x'\nSTOPWORDS = {'x'}\n",
                encoding="utf-8",
            )
            findings = scan(root)
            codes = {finding.code for finding in findings}
            self.assertIn("legacy_authority_bypass", codes)
            self.assertIn("hardcoded_project_identifier", codes)
            self.assertIn("embedded_lexical_resource", codes)

    def test_approved_vocabulary_is_centralized_and_deterministic(self):
        root = Path(__file__).resolve().parents[1]
        context = {"domain_vocabulary_path": "config/domain_vocabulary.json"}
        first = load_approved_vocabulary(root, context)
        second = load_approved_vocabulary(root, context)
        self.assertEqual(approved_stopwords(first), approved_stopwords(second))
        self.assertTrue(first["_approved"])
        self.assertIn("the", approved_stopwords(first))


if __name__ == "__main__":
    unittest.main()
