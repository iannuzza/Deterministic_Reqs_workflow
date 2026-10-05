import csv
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_stage2_specs import (
    _infer_block_classification,
    _infer_supplementary_owner,
    _preview_blocks_for_requirement,
)
from run_stage2_micro_arch_and_crosscheck import _validate_mapping_preview_csv
from run_drs_gen_spec_agent import _resolve_digital_owners


class SupplementaryMappingRuleTests(unittest.TestCase):
    def setUp(self):
        self.block_defs = {
            "Analog Front End": {
                "function": "Condition analog sensor signals.",
                "inputs": "Analog sensor input",
                "outputs": "Conditioned signal",
            },
            "Digital Controller": {
                "function": "Control digital state and register routing.",
                "inputs": "Configuration registers",
                "outputs": "Digital status",
            },
            "Configured Mixed Block": {
                "classification": "Analog",
                "function": "General mixed-signal behavior.",
                "inputs": "Input",
                "outputs": "Output",
            },
            "Unassigned": {},
        }

    def test_supplementary_id_proposes_only_an_existing_block(self):
        row = {
            "source_req_id": "SUPP_DEVICE_DIGITAL_CONTROLLER_0042",
            "source_spec": "supplementary.pdf",
        }
        self.assertEqual(_infer_supplementary_owner(row, self.block_defs), "Digital Controller")

    def test_unknown_supplementary_id_does_not_invent_a_block(self):
        row = {
            "source_req_id": "SUPP_DEVICE_UNKNOWN_UNIT_0042",
            "source_spec": "supplementary.pdf",
        }
        self.assertEqual(_infer_supplementary_owner(row, self.block_defs), "")

    def test_existing_owner_precedes_missing_source_fallback(self):
        row = {
            "source_req_id": "SUPP_DEVICE_DIGITAL_CONTROLLER_0042",
            "source_spec": "supplementary.pdf",
            "source_section_owner": "Digital Controller",
            "source": "",
        }
        self.assertEqual(
            _preview_blocks_for_requirement(row, ["Digital Controller"], self.block_defs),
            ["Digital Controller"],
        )

    def test_explicit_source_owner_and_category_have_precedence(self):
        row = {
            "source_req_id": "SUPP_DEVICE_DIGITAL_CONTROLLER_0042",
            "source_spec": "supplementary.pdf",
            "source_section_owner": "Analog Front End",
            "category": "Analog",
            "requirement_statement": "The register shall control a digital state.",
        }
        self.assertEqual(_infer_supplementary_owner(row, self.block_defs), "Analog Front End")
        self.assertEqual(_infer_block_classification(row, "Analog Front End", self.block_defs), "Analog")

    def test_configured_block_classification_is_used(self):
        row = {"requirement_statement": "The block shall process data."}
        self.assertEqual(
            _infer_block_classification(row, "Configured Mixed Block", self.block_defs),
            "Analog",
        )

    def test_evidence_classification_is_deterministic(self):
        analog_row = {"requirement_statement": "The analog sensor signal shall be conditioned."}
        digital_row = {"requirement_statement": "The register state shall control the digital bus."}
        empty_row = {"requirement_statement": "The product shall meet the requirement."}
        self.assertEqual(_infer_block_classification(analog_row, "Analog Front End", self.block_defs), "Analog")
        self.assertEqual(_infer_block_classification(digital_row, "Digital Controller", self.block_defs), "Digital")
        self.assertEqual(_infer_block_classification(empty_row, "Unassigned", self.block_defs), "System")

    def test_unresolved_source_paragraph_blocks_approval(self):
        fields = [
            "candidate_block",
            "requirement_id",
            "approved_classification",
            "review_decision",
            "approved_block",
            "generated_block_paragraph_preview",
        ]
        row = {
            "candidate_block": "Unresolved source paragraph",
            "requirement_id": "SUPP_0042",
            "approved_classification": "Digital",
            "review_decision": "approved",
            "approved_block": "Unresolved source paragraph",
            "generated_block_paragraph_preview": "Pending unresolved source paragraph mapping",
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mapping.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerow(row)
            findings = _validate_mapping_preview_csv(path)
        self.assertTrue(any("requires user block mapping" in finding for finding in findings))

    def test_explicit_digital_mapping_survives_function_wording_mismatch(self):
        owners = _resolve_digital_owners(
            requirement=None,
            mapped_blocks="Main Controller",
            block_by_name={"Main Controller": object()},
            digital_blocks={"Main Controller"},
        )
        self.assertEqual(owners, ["Main Controller"])


if __name__ == "__main__":
    unittest.main()
