import ast
import sys
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from approved_snapshot_resolver import ApprovedResolverError, resolve_complete_authoritative_input
from requirement_corpus import RequirementInput
from workflow_routing import document_version_for_snapshot


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_FILES = (
    "run_srs_gen_spec_agent.py",
    "run_drs_gen_spec_agent.py",
    "run_ars_gen_spec_agent.py",
    "generate_ipos_specs.py",
)


class GeneratorSnapshotBindingTests(unittest.TestCase):
    def test_document_version_increments_only_when_snapshot_changes(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "spec.md"
            self.assertEqual(document_version_for_snapshot(output, "snap-1"), "0.1")
            output.write_text(
                "Snapshot ID: snap-1\n| Version | Date | Description | Author |\n| 0.1 | today | baseline | test |\n",
                encoding="utf-8",
            )
            self.assertEqual(document_version_for_snapshot(output, "snap-1"), "0.1")
            self.assertEqual(document_version_for_snapshot(output, "snap-2"), "0.2")

    def test_generators_use_only_complete_selector(self):
        for filename in GENERATOR_FILES:
            source = (ROOT / "scripts" / filename).read_text(encoding="utf-8-sig")
            tree = ast.parse(source, filename=filename)
            calls = [
                node.func.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            ]
            self.assertIn("resolve_complete_authoritative_input", calls, filename)
            legacy_calls = [
                node.func.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in {"resolve_authoritative_input", "load_approved_input"}
            ]
            self.assertEqual(legacy_calls, [], filename)

    def test_incomplete_and_empty_selection_fail_before_generation(self):
        incomplete = RequirementInput(
            stage="test", snapshot_id="incomplete", corpus_hash="c", snapshot_hash="s",
            source_path=Path("canonical.sqlite"), rows=({"canonical_id": "req-1"},),
            source_links={}, mapping={},
        )
        with patch("approved_snapshot_resolver.resolve_authoritative_input", return_value=incomplete):
            with self.assertRaisesRegex(ApprovedResolverError, "incomplete.*mapping set is empty"):
                resolve_complete_authoritative_input(Path("."), "test", project_id="P", snapshot_id="incomplete")

        class EmptyConnection:
            def execute(self, _query, _params):
                return self

            def fetchall(self):
                return []

            def close(self):
                pass

        with patch("canonical_store.connect", return_value=EmptyConnection()):
            with self.assertRaisesRegex(ApprovedResolverError, "No complete approved snapshot"):
                resolve_complete_authoritative_input(Path("."), "test", project_id="P")

    def test_selected_snapshot_id_is_propagated_to_ledger(self):
        selected = RequirementInput(
            stage="test", snapshot_id="selected", corpus_hash="c", snapshot_hash="s",
            source_path=Path("canonical.sqlite"), rows=({"canonical_id": "req-1"},),
            source_links={}, mapping={"req-1": "block"},
        )
        with patch("approved_snapshot_resolver.resolve_authoritative_input", return_value=selected):
            resolved, record = resolve_complete_authoritative_input(
                Path("."), "test", project_id="P", snapshot_id="selected"
            )
        self.assertEqual(resolved.snapshot_id, "selected")
        self.assertEqual(record["selected_snapshot_id"], "selected")


if __name__ == "__main__":
    unittest.main()