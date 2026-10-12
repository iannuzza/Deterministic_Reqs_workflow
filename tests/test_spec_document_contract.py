import tempfile
import json
import unittest
import zipfile
from xml.sax.saxutils import escape
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
    IPOS_TEMPLATE,
    load_ipos_contract,
    load_drs_contract,
    DRS_TEMPLATE,
    ipos_document_contract_report,
)
from workflow_routing import (
    IPOS_DESCRIPTIVE_PROFILE, _ipos_admitted_records, _project_ipos_record,
    build_ipos_functional_input, run_descriptive_flow, validate_ipos_descriptive_output,
    write_ipos_descriptive_audit, ipos_main_function_name,
    compose_ipos_overview, build_ipos_normalized_records, build_ipos_semantic_units,
)
from dataclasses import replace


def _write_docx(path: Path, paragraphs: list[str]) -> None:
    body = "".join(
        '<w:p>' + ('<w:pPr><w:pStyle w:val="Heading3"/></w:pPr>' if text.startswith("#") else '')
        + '<w:r><w:t>' + escape(text.lstrip("# ")) + '</w:t></w:r></w:p>' for text in paragraphs
    )
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body}</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document)


class SpecificationDocumentContractTests(unittest.TestCase):
    def test_all_block_claim_preflight_reports_every_failure_without_output_writes(self):
        from unittest.mock import patch
        from generate_ipos_specs import _require_ipos_claim_preflights
        inventory = {"Function": "Process commands", "Inputs": "commands", "Outputs": "results"}
        rows = [
            {"mapped_block": "First", "source_req_id": "bad-first", "statement": "When ready, it shall transfer samples."},
            {"mapped_block": "Second", "source_req_id": "bad-second", "statement": "Priority is listed below: 1. incomplete"},
            {"mapped_block": "Third", "source_req_id": "good", "statement": "Third shall copy commands into memory."},
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch("generate_ipos_specs._block_inventory_record", return_value=inventory) as lookup:
                with self.assertRaises(RuntimeError) as raised:
                    _require_ipos_claim_preflights(root, "digital", ["First", "Second", "Third"], rows, rows)
            self.assertEqual(lookup.call_count, 3)
            message = str(raised.exception)
            self.assertIn("2/3 digital blocks", message)
            self.assertIn("requirement:First:bad-first", message)
            self.assertIn("requirement:Second:bad-second", message)
            self.assertNotIn("requirement:Third:good", message)
            self.assertEqual(list(root.iterdir()), [])
            with patch("generate_ipos_specs._block_inventory_record", return_value=inventory):
                _require_ipos_claim_preflights(root, "digital", ["Third"], rows, rows)
                _require_ipos_claim_preflights(root, "analog", [], [], [])

    def test_damaged_report_counts_verified_recovery_and_rejects_forged_evidence(self):
        from dataclasses import replace
        from workflow_routing import build_ipos_claim_plan, ipos_damaged_evidence_report, DescriptiveUnresolvedContext, DescriptiveSourceSpan
        statements = ("The controller shall transfer DATA to OUTPUT and", "When READY is high, the controller shall transfer DATA to OUTPUT,", "This")
        functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": str(index), "statement": statement} for index, statement in enumerate(statements)], domain="digital")
        plan = build_ipos_claim_plan(functional)
        contexts = tuple(DescriptiveUnresolvedContext(record.record_id + ":clause:1:unresolved",
                         (DescriptiveSourceSpan(record.record_id, 0, len(record.text), record.text),), "damaged")
                         for record in plan.evidence.records if record.record_id.startswith("requirement:"))
        report = ipos_damaged_evidence_report(functional, contexts)
        self.assertEqual(len(report["classes"]), 6)
        self.assertEqual(sum(value["count"] for value in report["classes"]), 3)
        self.assertEqual(sum(value["recovery_without_invention"] for value in report["observations"]), 2)
        self.assertTrue(all(value["residual_still_blocking"] for value in report["observations"]))
        self.assertFalse(report["cross_record_recomposition_enabled"])
        forged = replace(contexts[0], spans=(replace(contexts[0].spans[0], text="invented"),))
        with self.assertRaises(ValueError):
            ipos_damaged_evidence_report(functional, (forged,))

    def test_partial_command_keeps_separate_configuration_as_unresolved(self):
        from workflow_routing import build_ipos_claim_plan, _ipos_evidence_semantic_findings, ipos_claim_preflight_findings
        functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "commands", "statement": "In order to enable sampling, the user shall always select CHANNEL_MODE, set SAMPLE_LIMIT greater than zero and"}], domain="digital")
        plan = build_ipos_claim_plan(functional)
        supported = next(proposition for proposition in plan.evidence.propositions if proposition.meaning.predicate == "select")
        self.assertEqual(supported.meaning.objects, ("CHANNEL_MODE",))
        self.assertEqual(supported.meaning.qualifiers, ("always",))
        self.assertTrue(any("set SAMPLE_LIMIT" in span.text for context in plan.evidence.unresolved_contexts for span in context.spans))
        self.assertEqual(_ipos_evidence_semantic_findings(plan.evidence), [])
        self.assertTrue(ipos_claim_preflight_findings(functional))

    def test_dangling_coordination_preserves_supported_meaning_not_unfinished_scope(self):
        from workflow_routing import build_ipos_claim_plan, ipos_claim_preflight_findings, _ipos_evidence_semantic_findings
        for statement in ("When READY is high, the controller shall transfer DATA to OUTPUT and",
                          "When READY is high, the controller shall transfer DATA to OUTPUT,"):
            functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
                [{"source_req_id": "partial", "statement": statement}], domain="digital")
            plan = build_ipos_claim_plan(functional)
            self.assertEqual(len(plan.evidence.unresolved_contexts), 1)
            self.assertTrue(any(meaning.predicate == "transfer" and meaning.objects == ("DATA to OUTPUT",)
                                for claim in plan.claims for meaning in claim.meanings))
            self.assertEqual(_ipos_evidence_semantic_findings(plan.evidence), [])
            self.assertTrue(ipos_claim_preflight_findings(functional))
        for statement in ("When READY is high, the controller shall transfer DATA unless",
                          "When READY is high, the controller shall transfer DATA to the and",
                          "When READY is high, the controller shall transfer DATA except for and",
                          "When READY is high, the controller shall transfer DATA only if",
                          "When READY is high, the controller shall transfer DATA within 5 cycles at"):
            functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
                [{"source_req_id": "unsafe", "statement": statement}], domain="digital")
            plan = build_ipos_claim_plan(functional)
            self.assertFalse(any(meaning.predicate == "transfer" for claim in plan.claims for meaning in claim.meanings))
            self.assertTrue(plan.evidence.unresolved_contexts)

    def test_unresolved_body_keeps_exact_guard_provenance(self):
        from workflow_routing import build_ipos_claim_plan, ipos_claim_preflight_findings
        functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "partial", "statement": "When READY is high, the controller shall transfer DATA into the."}], domain="digital")
        plan = build_ipos_claim_plan(functional)
        self.assertEqual(len(plan.evidence.unresolved_contexts), 1)
        context = plan.evidence.unresolved_contexts[0]
        self.assertEqual(context.spans[0].text, "When READY is high,")
        self.assertTrue(ipos_claim_preflight_findings(functional))
        self.assertFalse(any(disposition.reason == "unmodeled_source_span" for disposition in plan.dispositions))

    def test_discourse_marker_does_not_become_functional_actor(self):
        from workflow_routing import build_ipos_claim_plan, _ipos_evidence_semantic_findings
        functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "discourse", "statement": "In particular, the sampling phase shall be controlled by CONFIG_A and the sampled data shall be written in RESULT_A and RESULT_B."}], domain="digital")
        plan = build_ipos_claim_plan(functional)
        subjects = [p.meaning.subject for p in plan.evidence.propositions if p.spans[0].record_id.startswith("requirement:")]
        self.assertEqual(subjects, ["the sampling phase", "the sampled data"])
        self.assertEqual(_ipos_evidence_semantic_findings(plan.evidence), [])

    def test_unsupported_member_does_not_drop_supported_same_context_meaning(self):
        from workflow_routing import build_ipos_claim_plan, ipos_claim_preflight_findings, _ipos_evidence_semantic_findings
        functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "valid", "statement": "When READY is high, the controller shall process DATA."},
             {"source_req_id": "reference", "statement": "When READY is high, the result shall be obtained as explained in UNKNOWN_REFERENCE."}], domain="digital")
        plan = build_ipos_claim_plan(functional)
        self.assertTrue(any(m.predicate == "process" for c in plan.claims for m in c.meanings))
        self.assertTrue(any(d.decision == "unresolved" for d in plan.dispositions))
        self.assertTrue(ipos_claim_preflight_findings(functional))
        self.assertEqual(_ipos_evidence_semantic_findings(plan.evidence), [])

    def test_guard_reference_recovery_requires_one_explicit_numeric_guard_subject(self):
        from workflow_routing import build_ipos_claim_plan, _ipos_evidence_semantic_findings
        for subject, expected in (("RESET is set to 1", True), ("RESET is above LIMIT", False)):
            functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
                [{"source_req_id": "reference", "statement": "If " + subject + ", it shall go to zero after 5ms."}], domain="digital")
            plan = build_ipos_claim_plan(functional)
            self.assertEqual(not plan.evidence.unresolved_contexts, expected)
            self.assertEqual(_ipos_evidence_semantic_findings(plan.evidence), [])

    def test_recomposition_does_not_transfer_guards_across_alternatives(self):
        from workflow_routing import build_ipos_claim_plan, _ipos_evidence_semantic_findings
        for statement in ("When READY is high, controller shall process DATA, otherwise, if BUSY is high, sampler shall transfer INPUT.",
                          "When READY is high, controller shall process DATA and after 10ms, sampler shall transfer INPUT."):
            functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
                [{"source_req_id": "branch", "statement": statement}], domain="digital")
            plan = build_ipos_claim_plan(functional)
            self.assertTrue(plan.evidence.unresolved_contexts)
            self.assertFalse(any(p.meaning.subject == "sampler" for p in plan.evidence.propositions))
        functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "time", "statement": "20ms after RESET is low, if READY is high, the controller shall process DATA and the sampler shall transfer INPUT."}], domain="digital")
        plan = build_ipos_claim_plan(functional)
        self.assertFalse(plan.evidence.unresolved_contexts)
        self.assertEqual(_ipos_evidence_semantic_findings(plan.evidence), [])

    def test_recomposition_retains_common_guard_and_partial_formula_gap(self):
        from dataclasses import replace
        from workflow_routing import build_ipos_claim_plan, _ipos_evidence_semantic_findings, ipos_claim_preflight_findings
        functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "joined", "statement": "When READY is high, the controller shall transfer DATA to OUTPUT and the sampler shall process INPUT."},
             {"source_req_id": "formula", "statement": "The configuration shall define the interval between acquisitions following this formula: result = input 2 value"}], domain="digital")
        plan = build_ipos_claim_plan(functional)
        meanings = [p.meaning for p in plan.evidence.propositions if p.spans[0].record_id.startswith("requirement:")]
        self.assertEqual(len(meanings), 3)
        self.assertEqual([m.contexts[0].text for m in meanings[:2]], ["When READY is high"] * 2)
        self.assertEqual(len(plan.evidence.unresolved_contexts), 1)
        self.assertEqual(_ipos_evidence_semantic_findings(plan.evidence), [])
        self.assertEqual(ipos_claim_preflight_findings(functional), [])
        formula = next(value for value in plan.dispositions if value.reason == "nonprose_output_path:parameter")
        self.assertEqual(formula.decision, "excluded")
        self.assertIn("result = input 2 value", formula.spans[0].text)
        proposition = next(p for p in plan.evidence.propositions if p.meaning.predicate == "process")
        mutated = replace(proposition, meaning=replace(proposition.meaning, contexts=()))
        changed = replace(plan.evidence, propositions=tuple(mutated if p == proposition else p for p in plan.evidence.propositions))
        self.assertTrue(_ipos_evidence_semantic_findings(changed))

    def test_incomplete_forward_reference_preserves_independent_supported_claim(self):
        from workflow_routing import build_ipos_claim_plan, ipos_claim_preflight_findings, _ipos_evidence_semantic_findings
        functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "partial", "statement": "The controller shall transfer DATA to OUTPUT. This"}], domain="digital")
        plan = build_ipos_claim_plan(functional)
        self.assertEqual(len(plan.evidence.unresolved_contexts), 1)
        self.assertTrue(any(meaning.predicate == "transfer" for claim in plan.claims for meaning in claim.meanings))
        self.assertEqual(_ipos_evidence_semantic_findings(plan.evidence), [])
        self.assertTrue(ipos_claim_preflight_findings(functional))
        exception = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "exception", "statement": "The controller shall transfer DATA to OUTPUT. Except when"}], domain="digital")
        self.assertFalse(any(meaning.predicate == "transfer" for claim in build_ipos_claim_plan(exception).claims for meaning in claim.meanings))

    def test_finite_grammar_distinguishes_destination_from_infinitive(self):
        from workflow_routing import _ipos_grammatical_phrase, _ipos_phrase_pattern
        import re
        destination = "into ERROR_STATE and raise an interrupt to the Digital_Top"
        corrected = _ipos_grammatical_phrase(destination, "object", "go")
        self.assertIn("and raises an interrupt to the Digital_Top", corrected)
        self.assertIsNotNone(re.fullmatch(_ipos_phrase_pattern(destination, "object", "go"), corrected))
        infinitive = "to start the ramp and raise an interrupt"
        self.assertEqual(_ipos_grammatical_phrase(infinitive, "object", "go"), infinitive)
        self.assertIsNone(re.fullmatch(_ipos_phrase_pattern(infinitive, "object", "go"), infinitive.replace("raise", "raises")))
        condition = "the timer expire"
        self.assertIsNotNone(re.fullmatch(_ipos_phrase_pattern(condition, "condition"), "the timer expires"))
        self.assertIsNone(re.fullmatch(_ipos_phrase_pattern(condition, "condition"), "the timer expirees"))

    def test_renderer_grammar_bug_cannot_certify_lost_numeric_meaning(self):
        from unittest.mock import patch
        from workflow_routing import build_ipos_claim_plan, realize_descriptive_functional_claim, _ipos_readback_section_findings
        functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "start", "statement": "The user shall start measurement writing register START_CONTROL at 1."}], domain="digital")
        claim = next(value for value in build_ipos_claim_plan(functional).claims if value.role == "functions")
        with patch("workflow_routing._ipos_grammatical_phrase", side_effect=lambda text, *args: text.replace("at 1", "at 2")):
            text = realize_descriptive_functional_claim(claim)
            self.assertIn("at 2", text)
            self.assertTrue(_ipos_readback_section_findings(text, (claim,)))

    def test_registered_always_rule_preserves_adverb_and_purpose_guard_independently(self):
        from workflow_routing import build_ipos_claim_plan, realize_descriptive_functional_claim, _ipos_readback_section_findings, _ipos_evidence_semantic_findings
        functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "select", "statement": "In order to enable a channel operation, the user shall always select CHANNEL_SELECT."}], domain="digital")
        plan = build_ipos_claim_plan(functional)
        self.assertEqual(plan.evidence.unresolved_contexts, ())
        self.assertEqual(_ipos_evidence_semantic_findings(plan.evidence), [])
        claim = next(value for value in plan.claims if value.role == "limits")
        text = realize_descriptive_functional_claim(claim)
        self.assertIn("the user always selects CHANNEL_SELECT", text)
        self.assertEqual(_ipos_readback_section_findings(text, (claim,)), [])
        for changed in (text.replace("always ", ""), text.replace("CHANNEL_SELECT", "OTHER_SELECT"),
                        "The user always selects CHANNEL_SELECT."):
            self.assertTrue(_ipos_readback_section_findings(changed, (claim,)))
        from dataclasses import replace
        meaning = replace(plan.evidence.propositions[-1].meaning, qualifiers=())
        changed = replace(plan.evidence, propositions=(*plan.evidence.propositions[:-1], replace(plan.evidence.propositions[-1], meaning=meaning)))
        self.assertTrue(_ipos_evidence_semantic_findings(changed))

    def test_finite_grammar_repairs_preserve_semantics_and_do_not_inflect_infinitive_effects(self):
        from workflow_routing import build_ipos_claim_plan, realize_descriptive_functional_claim, _ipos_readback_section_findings, ipos_publication_quality_findings
        functional = build_ipos_functional_input("Module", {"Function": "Control sampling", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "start", "statement": "The user shall start measurement writing register START_CONTROL at 1."},
             {"source_req_id": "error", "statement": "When enabled, if the counter reach its limit, the Sequencer shall go into ERROR_STATE and raise an interrupt."},
             {"source_req_id": "effect", "statement": "When ready, TRIGGER shall be set high to start the ramp and go into RISING_STATE."}], domain="digital")
        claims = [claim for claim in build_ipos_claim_plan(functional).claims if claim.role == "functions"]
        texts = [realize_descriptive_functional_claim(claim) for claim in claims]
        self.assertTrue(any("measurement by writing register START_CONTROL at 1" in text for text in texts))
        self.assertTrue(any("counter reaches its limit" in text and "and raises an interrupt" in text for text in texts))
        self.assertTrue(any("to start the ramp and go into RISING_STATE" in text for text in texts))
        for claim, text in zip(claims, texts):
            self.assertEqual(_ipos_readback_section_findings(text, (claim,)), [])
            self.assertEqual(ipos_publication_quality_findings({"1.4": text}), [])
            self.assertTrue(_ipos_readback_section_findings(text.replace(" at 1", " at 2").replace("ERROR_STATE", "OTHER_STATE").replace("RISING_STATE", "OTHER_STATE"), (claim,)))

    def test_ipos_yaml_is_separate_and_rejects_weakened_or_unknown_obligations(self):
        import yaml
        root = Path(__file__).resolve().parents[1]
        contract = load_ipos_contract(root / IPOS_TEMPLATE)
        drs = load_drs_contract(root / DRS_TEMPLATE)
        self.assertEqual(contract["document_type"], "IPOS")
        self.assertNotEqual(contract["sha256"], drs["sha256"])
        self.assertEqual(contract["paragraph"]["claim_scope"][0], "initiation")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "contract.md"
            for field, value in (("document_type", "DRS"), ("profile", "system"),
                                 ("synthesis", "guess_from_labels"), ("mandatory_rules", []),
                                 ("validation_hooks", ["publication_quality"]), ("paragraph", {}),
                                 ("detail_policy", "drop_local_detail"), ("gap_policy", "ignore_gaps"),
                                 ("rendering", "legacy"), ("sha256", "forged"), ("unknown_rule", True)):
                changed = {key: item for key, item in contract.items() if key != "sha256"}
                changed[field] = value
                path.write_text("```yaml ipos-document-contract\n" + yaml.safe_dump(changed) + "```\n", encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_ipos_contract(path)
            path.write_text("```yaml ipos-document-contract\nversion: 1\nversion: 1\ndocument_type: IPOS\n```\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_ipos_contract(path)

    def test_ipos_shared_final_semantics_survive_joint_audit_and_hash_mutation(self):
        for domain in ("digital", "analog"):
            with self.subTest(domain=domain), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                markdown, docx, audit = root / "spec.md", root / "spec.docx", root / "descriptive_summary_audit.csv"
                source = "When enabled, Coordinator shall transfer samples to Receiver."
                functional_input = build_ipos_functional_input(
                    "Module", {"Function": "Coordinate acquisition", "Inputs": "samples", "Outputs": "results"},
                    [{"source_req_id": "one", "statement": source}], domain=domain,
                )
                records = build_ipos_normalized_records(functional_input)

                def materialize(drop_guard=False, move_to_normative=False, extra_relation=False, extra_title=False):
                    sections, rows = compose_ipos_overview(functional_input)
                    if drop_guard:
                        sections["internal_functions"] = [text.replace("When enabled, coordinator", "Coordinator")
                                                          for text in sections["internal_functions"]]
                        for row in rows:
                            if row.get("candidate_evidence_requirement_id") == "one":
                                unit = json.loads(row["semantic_unit_json"])
                                unit["text"] = unit["text"].replace("When enabled, coordinator", "Coordinator")
                                row["semantic_unit_json"] = json.dumps(unit)
                                claim_payload = json.loads(row["claim_json"])
                                claim_payload["meanings"][0]["contexts"] = []
                                row["claim_json"] = json.dumps(claim_payload)
                    scope = sections["scope"]
                    functions = sections["internal_functions"]
                    claim = functions.pop() if move_to_normative else ""
                    if extra_relation:
                        scope.append("Receiver controls Coordinator.")
                    if extra_title:
                        functions.insert(0, "**Coordinator.**")
                    lines = ["## 1. Block overview", "### 1.1 Functionality", *sections["functionality"],
                             "### 1.2 Supported functions and scope", *scope,
                             "### 1.4 Supported block functions", *functions,
                             "## 2. Source I/O", "## 3. Block requirements", source, claim]
                    markdown.write_text("\n\n".join(lines), encoding="utf-8")
                    _write_docx(docx, lines)
                    write_ipos_descriptive_audit(audit, rows)
                    write_materialization_audit(root / "materialization_audit.json", "IPOS",
                                                records, build_ipos_semantic_units(functional_input, sections, rows), markdown, docx)

                def validate():
                    return validate_ipos_descriptive_output(markdown, audit, "Module", [source], ["one"], (), functional_input)

                materialize()
                self.assertEqual(validate(), [])
                materialize(drop_guard=True)
                self.assertTrue(any("ipos_descriptive_audit_invalid_or_changed" in finding for finding in validate()))
                self.assertTrue(any("ipos_final_claim_missing_or_changed" in finding for finding in validate()))
                materialize(move_to_normative=True)
                self.assertTrue(any("ipos_final_claim_missing_or_changed:spec.md" in finding for finding in validate()))
                self.assertTrue(any("ipos_final_claim_missing_or_changed:spec.docx" in finding for finding in validate()))
                materialize(extra_relation=True)
                self.assertTrue(any("ipos_final_unmodeled_content:spec.md" in finding for finding in validate()))
                self.assertTrue(any("ipos_final_unmodeled_content:spec.docx" in finding for finding in validate()))
                materialize(extra_title=True)
                self.assertTrue(any("ipos_final_unmodeled_content:spec.md" in finding for finding in validate()))
                self.assertTrue(any("ipos_final_unmodeled_content:spec.docx" in finding for finding in validate()))

    def test_generator_refuses_unresolved_claim_before_writing_artifacts(self):
        from unittest.mock import patch
        from generate_ipos_specs import _write_ipos_document
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "not-created"
            with patch("generate_ipos_specs._block_inventory_record", return_value={
                "Function": "Coordinate sampling", "Inputs": "samples", "Outputs": "results",
            }):
                with self.assertRaisesRegex(RuntimeError, "preflight blocked materialization"):
                    _write_ipos_document(repo, {}, "digital", "Module", output, "Module", [{
                        "mapped_block": "Module", "source_req_id": "one",
                        "requirement_statement": "Coordinator shall transfer samples into the.",
                    }], "snapshot", require_docx=False)
            self.assertFalse(output.exists())

    def test_generator_cannot_fall_back_to_markdown_only_without_docx_baseline(self):
        from unittest.mock import patch
        from generate_ipos_specs import _write_ipos_document
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "templates").mkdir()
            (root / IPOS_TEMPLATE).write_text((repo / IPOS_TEMPLATE).read_text(encoding="utf-8"), encoding="utf-8")
            output = root / "not-created"
            with patch("generate_ipos_specs._block_inventory_record", return_value={
                "Function": "Coordinate sampling", "Inputs": "samples", "Outputs": "results",
            }):
                with self.assertRaisesRegex(RuntimeError, "DOCX reference template is missing"):
                    _write_ipos_document(root, {}, "digital", "Module", output, "Module", [{
                        "mapped_block": "Module", "source_req_id": "one",
                        "requirement_statement": "Coordinator shall process samples.",
                    }], "snapshot", require_docx=False)
            self.assertFalse(output.exists())

    def test_ipos_contract_checks_are_independent_and_allow_bounded_paraphrase(self):
        functional = build_ipos_functional_input("Module",
            {"Function": "Coordinate acquisition", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "one", "statement": "When ENABLED_STATE is active, Coordinator shall comprise Receiver and Sender."}],
            domain="digital")
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "templates").mkdir()
            (root / IPOS_TEMPLATE).write_text((repo / IPOS_TEMPLATE).read_text(encoding="utf-8"), encoding="utf-8")
            markdown, docx, audit = root / "spec.md", root / "spec.docx", root / "descriptive_summary_audit.csv"
            sections, rows = compose_ipos_overview(functional)
            sections["internal_structure"] = ["Coordinator contains Receiver and Sender, When ENABLED_STATE is active."]
            for row in rows:
                if row.get("candidate_evidence_requirement_id") == "one":
                    unit = json.loads(row["semantic_unit_json"])
                    unit["text"] = sections["internal_structure"][0]
                    row["semantic_unit_json"] = json.dumps(unit)
            lines = ["## 1. Block overview", "### 1.1 Functionality", *sections["functionality"],
                     "### 1.2 Supported functions and scope", *sections["scope"],
                     "### 1.3 Internal structure", *sections["internal_structure"], "## 2. Source I/O"]
            markdown.write_text("\n\n".join(lines), encoding="utf-8")
            _write_docx(docx, lines)
            write_ipos_descriptive_audit(audit, rows)
            units = build_ipos_semantic_units(functional, sections, rows)
            write_materialization_audit(root / "materialization_audit.json", "IPOS", build_ipos_normalized_records(functional), units, markdown, docx)
            report = ipos_document_contract_report(root, markdown, audit, functional)
            self.assertEqual(report["status"], "PASS", report)
            self.assertEqual(set(report["checks"]), {"semantic_fidelity", "publication_quality", "materialization"})
            markdown.write_text(markdown.read_text(encoding="utf-8").replace("ENABLED_STATE", "enabled_state"), encoding="utf-8")
            report = ipos_document_contract_report(root, markdown, audit, functional)
            self.assertEqual(report["checks"]["semantic_fidelity"]["status"], "FAIL")
            self.assertEqual(report["checks"]["materialization"]["status"], "FAIL")
            self.assertEqual(report["checks"]["publication_quality"]["status"], "PASS")

    def test_ipos_actual_readback_retains_bare_identifiers_and_function_initial_case(self):
        from workflow_routing import build_ipos_claim_plan, _ipos_readback_section_findings
        functional = build_ipos_functional_input("Module",
            {"Function": "DSP processing of samples", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "one", "statement": "When READY is active, Coordinator shall write samples to FIFO."}],
            domain="digital")
        sections, rows = compose_ipos_overview(functional)
        self.assertIn("DSP processing", sections["functionality"][0])
        claim = next(value for value in build_ipos_claim_plan(functional).claims if value.role == "functions")
        actual = "Coordinator writes samples to FIFO when READY is active."
        self.assertEqual(_ipos_readback_section_findings(actual, (claim,)), [])
        for changed in (actual.replace("FIFO", "fifo"), actual.replace("READY", "ready"),
                        actual.replace("writes", "write"), actual.replace("samples", "results"),
                        actual.replace(" when READY is active", "")):
            self.assertTrue(_ipos_readback_section_findings(changed, (claim,)), changed)

    def test_ipos_semantic_checks_reject_approved_conflict_and_grammatical_subject_mutation(self):
        from workflow_routing import build_ipos_evidence_model, _ipos_evidence_semantic_findings, _ipos_readback_section_findings, build_ipos_claim_plan
        functional = build_ipos_functional_input("Module",
            {"Function": "Coordinate sampling", "Inputs": "samples", "Outputs": "results"},
            [{"source_req_id": "one", "statement": "Coordinator shall transfer samples."},
             {"source_req_id": "two", "statement": "Coordinator shall not transfer samples."}], domain="digital")
        self.assertTrue(any("ipos_approved_source_conflict" in finding for finding in
                            _ipos_evidence_semantic_findings(build_ipos_evidence_model(functional))))
        claim = next(value for value in build_ipos_claim_plan(functional).claims if value.role == "boundaries")
        self.assertTrue(_ipos_readback_section_findings("The Module block accepts samples and produces results and has extra outputs.", (claim,)))

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

    def test_materialization_accepts_typographic_quotes_but_not_lost_qualifiers(self):
        text = "Preserves the user's configuration when enabled."
        records = (NormalizedSourceRecord("one", text, "authoritative", "Module", ("approved:one",), "retained", "approved"),)
        units = (SemanticUnit("one", "scope", text, ("one",), 1),)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            markdown, docx, audit = root / "spec.md", root / "spec.docx", root / "audit.json"
            markdown.write_text(text, encoding="utf-8")
            _write_docx(docx, [text.replace("'", "\u2019")])
            write_materialization_audit(audit, "IPOS", records, units, markdown, docx)
            self.assertEqual(validate_materialization_chain(audit, "IPOS", records, markdown, docx), [])
            _write_docx(docx, [text.replace(" when enabled", "")])
            write_materialization_audit(audit, "IPOS", records, units, markdown, docx)
            self.assertTrue(any("missing or reordered" in finding for finding in
                                validate_materialization_chain(audit, "IPOS", records, markdown, docx)))

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