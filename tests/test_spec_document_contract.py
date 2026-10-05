import tempfile
import json
import unittest
import zipfile
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from spec_document_contract import (
    DOCUMENT_TYPE_CONTRACTS,
    IPOS_DETAIL_POLICY,
    resolve_ipos_description_policy,
    NormalizedSourceRecord,
    SemanticUnit,
    validate_materialization_chain,
    write_materialization_audit,
)


def _write_docx(path: Path, paragraphs: list[str]) -> None:
    body = "".join(
        f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>" for text in paragraphs
    )
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body}</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document)


class SpecificationDocumentContractTests(unittest.TestCase):
    def test_description_pilot_is_exact_opt_in_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(resolve_ipos_description_policy(root, "snap-one", "digital", "Module One"), "legacy")
            (root / "config").mkdir()
            path = root / "config/ipos_description_pilots.json"
            pilot = {"snapshot_id": "snap-one", "kind": "digital", "block": "Module One", "policy": IPOS_DETAIL_POLICY}
            path.write_text(json.dumps({"version": 1, "pilots": [pilot]}), encoding="utf-8")
            self.assertEqual(resolve_ipos_description_policy(root, "snap-one", "digital", "Module One"), IPOS_DETAIL_POLICY)
            for snapshot, kind, block in (("snap-two", "digital", "Module One"), ("snap-one", "analog", "Module One"), ("snap-one", "digital", "Module Two")):
                self.assertEqual(resolve_ipos_description_policy(root, snapshot, kind, block), "legacy")
            path.write_text(json.dumps({"version": 1, "pilots": [pilot, pilot]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                resolve_ipos_description_policy(root, "snap-one", "digital", "Module One")

    def test_contract_registry_preserves_document_specific_boundaries(self):
        self.assertEqual(set(DOCUMENT_TYPE_CONTRACTS), {"SRS", "ARS", "DRS", "IPOS"})
        self.assertEqual(DOCUMENT_TYPE_CONTRACTS["SRS"].ownership_scope, "system")
        self.assertIn("integration", DOCUMENT_TYPE_CONTRACTS["DRS"].ownership_scope)
        self.assertIn("same-block", DOCUMENT_TYPE_CONTRACTS["IPOS"].promotion_rule)

    def test_shared_contract_contains_no_project_capability_catalogue(self):
        source = (Path(__file__).resolve().parents[1] / "scripts" / "spec_document_contract.py").read_text(
            encoding="utf-8"
        ).casefold()
        for forbidden in ("main controller", "smart fifo", "ecg", "bia", "ppg", "gsr"):
            self.assertNotIn(forbidden, source)

    def test_end_to_end_chain_detects_loss_order_and_wrong_promotion(self):
        records = (
            NormalizedSourceRecord(
                "authority:function", "Coordinate approved data", "authoritative", "Module One",
                ("approved snapshot",), "retained", "approved local function",
            ),
            NormalizedSourceRecord(
                "local:req-1", "Local processing capability.", "authoritative", "Module One",
                ("approved:req-1",), "retained", "supported same-scope detail",
            ),
            NormalizedSourceRecord(
                "other:req-2", "Foreign capability.", "discovery_only", "Module Two",
                ("approved:req-2",), "suppressed", "cross-scope candidate",
            ),
        )
        units = (
            SemanticUnit("purpose:1", "functionality", "Coordinate approved data", ("authority:function",), 1),
            SemanticUnit("scope:1", "supported_functions_and_scope", "Local processing capability.", ("local:req-1",), 2),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            markdown = root / "spec.md"
            docx = root / "spec.docx"
            audit = root / "materialization_audit.json"
            markdown.write_text("Coordinate approved data\n\nLocal processing capability.\n", encoding="utf-8")
            _write_docx(docx, ["Coordinate approved data", "Local processing capability."])
            write_materialization_audit(audit, "IPOS", records, units, markdown, docx)
            self.assertEqual(validate_materialization_chain(audit, "IPOS", records, markdown, docx), [])

            markdown.write_text("Coordinate approved data\n", encoding="utf-8")
            findings = validate_materialization_chain(audit, "IPOS", records, markdown, docx)
            self.assertTrue(any("missing or reordered" in finding for finding in findings))

            markdown.write_text("Foreign capability.\nCoordinate approved data\nLocal processing capability.\n", encoding="utf-8")
            wrong_units = units + (
                SemanticUnit("scope:2", "supported_functions_and_scope", "Foreign capability.", ("other:req-2",), 3),
            )
            _write_docx(docx, ["Coordinate approved data", "Local processing capability.", "Foreign capability."])
            write_materialization_audit(audit, "IPOS", records, wrong_units, markdown, docx)
            findings = validate_materialization_chain(audit, "IPOS", records, markdown, docx)
            self.assertTrue(any("promotes a suppressed source" in finding for finding in findings))

    def test_docx_post_processing_loss_invalidates_audit(self):
        records = (
            NormalizedSourceRecord(
                "source:1", "Approved capability.", "authoritative", "Scope A",
                ("approved:1",), "retained", "approved content",
            ),
        )
        units = (SemanticUnit("unit:1", "requirements", "Approved capability.", ("source:1",), 1),)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            markdown = root / "spec.md"
            docx = root / "spec.docx"
            audit = root / "materialization_audit.json"
            markdown.write_text("Approved capability.\n", encoding="utf-8")
            _write_docx(docx, ["Approved capability."])
            write_materialization_audit(audit, "SRS", records, units, markdown, docx)
            _write_docx(docx, ["Content removed during post-processing."])
            findings = validate_materialization_chain(audit, "SRS", records, markdown, docx)
            self.assertTrue(any("changed after audited post-processing" in finding for finding in findings))
            self.assertTrue(any("missing or reordered" in finding for finding in findings))

    def test_ipos_scope_semantic_unit_matches_flattened_docx_bold_text(self):
        records = (
            NormalizedSourceRecord(
                "local:req-1", "Approved local behavior.", "authoritative", "Module One",
                ("approved:req-1",), "retained", "supported same-scope detail",
            ),
        )
        units = (
            SemanticUnit(
                "scope:1", "supported_functions_and_scope",
                "**Local control.** Coordinates approved local behavior.\n  Relates input to output.",
                ("local:req-1",), 1,
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            markdown = root / "spec.md"
            docx = root / "spec.docx"
            audit = root / "materialization_audit.json"
            markdown.write_text(units[0].text + "\n", encoding="utf-8")
            _write_docx(docx, ["Local control. Coordinates approved local behavior.", "Relates input to output."])
            write_materialization_audit(audit, "IPOS", records, units, markdown, docx)
            self.assertEqual(validate_materialization_chain(audit, "IPOS", records, markdown, docx), [])

    def test_suppressed_single_token_does_not_match_legitimate_descriptive_text(self):
        records = (
            NormalizedSourceRecord(
                "local:req-1", "Coordinates the approved ADC acquisition flow.", "authoritative", "Module One",
                ("approved:req-1",), "retained", "supported same-scope detail",
            ),
            NormalizedSourceRecord(
                "other:req-2", "ADC", "discovery_only", "Module Two",
                ("approved:req-2",), "suppressed", "cross-scope fragment",
            ),
        )
        units = (
            SemanticUnit("scope:1", "supported_functions_and_scope", "Coordinates the approved ADC acquisition flow.", ("local:req-1",), 1),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            markdown = root / "spec.md"
            docx = root / "spec.docx"
            audit = root / "materialization_audit.json"
            markdown.write_text("Coordinates the approved ADC acquisition flow.\n", encoding="utf-8")
            _write_docx(docx, ["Coordinates the approved ADC acquisition flow."])
            write_materialization_audit(audit, "IPOS", records, units, markdown, docx)
            self.assertEqual(validate_materialization_chain(audit, "IPOS", records, markdown, docx), [])


if __name__ == "__main__":
    unittest.main()