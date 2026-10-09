import importlib
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
reporting = importlib.import_module("generate_cross_spec_issue_report")
contracts = importlib.import_module("spec_document_contract")


class CrossSpecIssueReportTests(unittest.TestCase):
    def test_presentation_omits_review_notes_without_guessing_missing_content(self):
        original = "The interface accepts samples. External placement is not specified."
        self.assertEqual(contracts.clean_descriptive_review_text(original), "The interface accepts samples.")
        self.assertEqual(contracts.clean_descriptive_review_text("Flow control: need clarification"), "")
        self.assertEqual(contracts.clean_descriptive_review_text("- TBD-001: Review the owner."), "")
        self.assertEqual(contracts.clean_descriptive_review_text(
            "Gated; control expression: u_pm u.enable; signal spelling: need clarification"), "")
        supported = "When reset is low, the output remains low."
        self.assertEqual(contracts.clean_descriptive_review_text(supported), supported)

    def user_report_fixture(self):
        finding = reporting.issue("SRS", "Section | 3", ["REQ-1"], "projection_gap",
                                  "Guard not modeled.", ["source.md#L1"])
        finding.update(issue_id="REVIEW-0001", source_excerpt="The unit shall wait if ready.\n```source```")
        finding["source_spans"] = [{"record_id": "REQ-1", "start": 31, "end": 100,
                       "text": "The unit shall wait if ready."}]
        return {"authority": False, "user_review_only": True, "snapshot_id": "test-snapshot", "run_start": "test-run",
                "issue_count": 1, "issue_counts_by_document": {"SRS": 1}, "issues": [finding],
                "documents": [{"document_type": "SRS", "gate_status": "PASS"}]}

    def test_clean_presentation_records_omissions_and_protects_normative_text(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "spec.md"
            lines = ["Snapshot ID: approved", "## 8. Assumptions and TBD", "Flow control: need clarification",
                     "| Device | An interrupt triggers wake-up. Local function: need clarification. |",
                     "[DRS-REQ-001]", "The clock shall run at 16 MHz.", "[End]"]
            projected = contracts.apply_clean_document_presentation(lines, path, "DRS")
            self.assertEqual(projected[-3:], lines[-3:])
            self.assertIn("An interrupt triggers wake-up.", projected[3])
            self.assertFalse(contracts.PUBLICATION_REVIEW_MARKERS.search("\n".join(projected)))
            audit = importlib.import_module("json").loads(path.with_name("descriptive_publication_audit.json").read_text())
            self.assertEqual(len(audit["omissions"]), 3)
            self.assertFalse(audit["authority"])
            with self.assertRaises(ValueError):
                contracts.apply_clean_document_presentation(["[DRS-REQ-001]", "The clock shall run: TBD."], path, "DRS")

    def test_accounting_cannot_drop_supported_meaning_or_unreported_notes(self):
        original = "The clock runs at 16 MHz. Timing: need clarification."
        audit = {"omissions": [{"original": original}]}
        self.assertTrue(contracts.publication_text_is_accounted(original, "The clock runs at 16 MHz.", "The clock runs at 16 MHz.", audit))
        self.assertFalse(contracts.publication_text_is_accounted(original, "The clock runs.", "The clock runs.", audit))
        self.assertFalse(contracts.publication_text_is_accounted(original, "The clock runs at 16 MHz.", "The clock runs at 16 MHz.", {}))

    def test_mixed_supported_prose_is_arranged_before_tables(self):
        contract = contracts.load_drs_contract(Path(__file__).resolve().parents[1] / contracts.DRS_TEMPLATE)
        mixed = "The clock runs at 16 MHz. Timing: need clarification."
        lines = []
        for title in contract["sections"]:
            lines.append("## " + title)
            if title.startswith("4."):
                lines.extend(["### 4.7 Clock and synchronization across domains", "| Clock | Frequency |",
                              "| --- | --- |", "| ClockA | 16 MHz |", mixed])
        arranged = contracts.arrange_drs_contract_lines(lines, contract)
        self.assertLess(arranged.index(mixed), arranged.index("| Clock | Frequency |"))

    def test_user_markdown_preserves_issue_fields_and_escapes_evidence(self):
        report = self.user_report_fixture()
        markdown = reporting.report_markdown(report)
        self.assertEqual(markdown.count("### REVIEW-0001"), 1)
        self.assertIn("Solo per revisione utente", markdown)
        self.assertIn("Section \\| 3", markdown)
        self.assertIn("REQ\\-1", markdown)
        self.assertIn("````text\n" + report["issues"][0]["source_excerpt"] + "\n````", markdown)
        with self.assertRaises(ValueError):
            reporting.report_markdown({**report, "authority": True})

    def test_ipos_publication_observation_requires_fresh_files_real_gate_and_no_markers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / reporting.ipos.CONFIG["digital"]["output_dir"] / "blocks" / "controller"
            folder.mkdir(parents=True)
            markdown = folder / reporting.ipos._block_markdown_name("digital", "Controller")
            markdown.write_text("Supported behavior.", encoding="utf-8")
            markdown.with_suffix(".docx").write_bytes(b"fixture")
            with patch.object(reporting.subprocess, "run") as run_gate, patch.object(reporting, "drs_document_events") as events:
                events.return_value = [{"kind": "paragraph", "text": "Supported behavior."}]
                run_gate.return_value = SimpleNamespace(returncode=0, stdout="block gate PASS", stderr="")
                state = reporting.observe_ipos_block_publication(root, "digital", "Controller", "snapshot", "2000-01-01 00:00:00")
                self.assertEqual(state["publication_status"], "PASS")
                self.assertEqual(len(state["artifact_hashes"]), 2)
                self.assertEqual(run_gate.call_args.args[0][-2:], ["--block", "Controller"])
                events.return_value = [{"kind": "table", "rows": [["Clock", "TBD"]]}]
                self.assertEqual(reporting.observe_ipos_block_publication(root, "digital", "Controller", "snapshot", "2000-01-01 00:00:00")["publication_status"], "FAIL_INLINE_MARKERS")
                run_gate.return_value = SimpleNamespace(returncode=1, stdout="", stderr="materialization failed")
                self.assertEqual(reporting.observe_ipos_block_publication(root, "digital", "Controller", "snapshot", "2000-01-01 00:00:00")["publication_status"], "FAIL_EXISTING_BLOCK_GATE")
                run_gate.reset_mock()
                self.assertEqual(reporting.observe_ipos_block_publication(root, "digital", "Controller", "snapshot", "2099-01-01 00:00:00")["publication_status"], "NOT_REGENERATED_IN_THIS_RUN")
                run_gate.assert_not_called()

    @unittest.skipUnless(shutil.which("pandoc"), "Pandoc is required for DOCX conversion")
    def test_user_docx_contains_issue_evidence_and_review_notice(self):
        with tempfile.TemporaryDirectory() as directory:
            report = self.user_report_fixture()
            markdown, docx = reporting.export_user_report(report, Path(directory) / "report.json")
            self.assertTrue(markdown.is_file())
            document = importlib.import_module("docx").Document(docx)
            text = "\n".join(paragraph.text for paragraph in document.paragraphs)
            self.assertIn("REVIEW-0001", text)
            self.assertIn("Solo per revisione utente", text)
            self.assertIn("REQ-1", text)
            self.assertIn(report["issues"][0]["source_excerpt"], text)
            self.assertIn("offset 31:100:", text)

    def test_audit_omissions_and_candidates_are_retained_without_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "audit.csv"
            path.write_text("decision,reason,statement,source\nselected,eligible,supported,source-a\n"
                            "rejected,projection_gap,unmodeled,source-b\n"
                            "candidate_only,not rendered,candidate,source-c\n", encoding="utf-8")
            before = path.read_bytes()
            findings = reporting.collect_csv_issues(path, "SRS", root)
            self.assertEqual(len(findings), 2)
            self.assertEqual([value["audit_decision"] for value in findings], ["rejected", "candidate_only"])
            self.assertTrue(all(value["user_review_only"] for value in findings))
            self.assertEqual(path.read_bytes(), before)

    def test_publication_markers_preserve_location_and_exact_requirement_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "spec.md"
            path.write_text("# Assumptions and TBD\nSupported function.\n"
                            "REQ-10: need clarification.\nState retention is not specified.\n", encoding="utf-8")
            findings = reporting.collect_publication_issues(path, "DRS", root, ["REQ-1", "REQ-10"])
            self.assertEqual(len(findings), 2)
            self.assertEqual(findings[0]["requirement_or_context_references"], ["REQ-10"])
            self.assertIn("line 3", findings[0]["location"])

    def test_conclusions_are_bounded_and_do_not_label_parser_gaps_as_source_damage(self):
        for blocker, expected in (("unsupported predicate grammar", "Need clarification"),
                                  ("ipos_source_relationship_changed", "Source-model relationship needs review"),
                                  ("unsupported structured/table/procedure evidence", "Structured evidence not sufficiently recoverable")):
            finding = reporting.issue("IPOS", "block", ["context"], blocker, "Observed finding", ["source"])
            self.assertEqual(finding["conclusion"], expected)
            self.assertIn(finding["conclusion"], reporting.CONCLUSIONS)

    def test_unclaimed_and_withheld_dispositions_are_reported(self):
        span = reporting.ipos.build_ipos_normalized_records(
            reporting.build_ipos_functional_input("Controller", {"Function": "control measurements"},
                                                  [{"source_req_id": "REQ-1", "requirement_statement": "The Controller shall start sampling."}],
                                                  domain="digital"))
        record = next(value for value in span if value.record_id.startswith("requirement:"))
        source_span = importlib.import_module("workflow_routing").DescriptiveSourceSpan(
            record.record_id, 0, len(record.text), record.text)
        disposition = SimpleNamespace(decision="unresolved", reason="no_supported_claim",
                                      spans=(source_span,), proposition_ids=("proposition-1",))
        plan = SimpleNamespace(evidence=SimpleNamespace(records=(record,), unresolved_contexts=()),
                               dispositions=(disposition,))
        findings = reporting.collect_plan_disposition_issues(plan, "IPOS", "Controller")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["blocker_class"], "no_supported_claim")
        self.assertEqual(findings[0]["source_spans"][0]["text"], record.text)


if __name__ == "__main__":
    unittest.main()