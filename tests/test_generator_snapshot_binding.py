import ast
import sys
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from approved_snapshot_resolver import ApprovedResolverError, resolve_complete_authoritative_input
from requirement_corpus import RequirementInput
from workflow_routing import document_version_for_snapshot, document_version_history_markdown, validate_document_author_fields
from docx import Document
from spec_document_contract import drs_document_events, drs_table_inventory


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_FILES = (
    "run_srs_gen_spec_agent.py",
    "run_drs_gen_spec_agent.py",
    "run_ars_gen_spec_agent.py",
    "generate_ipos_specs.py",
)


class GeneratorSnapshotBindingTests(unittest.TestCase):
    def test_history_changes_only_for_new_snapshot_and_preserves_prior_rows(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "spec.md"
            previous = []
            previous_snapshot = ""
            for snapshot, run_date, author, expected_version in (
                ("snap-1", "2026-01-01", "First Author", "0.1"),
                ("snap-1", "2026-01-02", "Second Author", "0.1"),
                ("snap-1", "2026-01-02", "Second Author", "0.1"),
                ("snap-2", "2026-01-03", "Third Author", "0.2"),
                ("snap-2", "2026-01-04", "Fourth Author", "0.2"),
                ("snap-3", "2026-01-05", "Fifth Author", "0.3"),
            ):
                with self.subTest(snapshot=snapshot, date=run_date, author=author):
                    version = document_version_for_snapshot(output, snapshot)
                    self.assertEqual(version, expected_version)
                    history = document_version_history_markdown(output, snapshot, version, run_date, f"Snapshot {snapshot} generated", author)
                    output.write_text(f"Snapshot ID: {snapshot}\nAuthor: {author}\n\n#### Table 1. Version history\n" + "\n".join(history), encoding="utf-8")
                    rows = drs_table_inventory(drs_document_events(output))[0]["rows"][1:]
                    if snapshot == previous_snapshot:
                        self.assertEqual(rows, previous)
                    else:
                        self.assertEqual(rows[:-1], previous)
                        self.assertEqual(rows[-1], [version, run_date, f"Snapshot {snapshot} generated", author])
                    document = Document()
                    document.core_properties.author = author
                    document.save(output.with_suffix(".docx"))
                    self.assertEqual(validate_document_author_fields(output), [])
                    previous = rows
                    previous_snapshot = snapshot
            self.assertEqual(len(previous), 3)

    def test_history_rejects_missing_or_duplicate_table(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "spec.md"
            for content in ("# Existing document without history", "\n\n".join(["| Version | Date | Description | Author |\n|---|---|---|---|\n| 0.1 | today | baseline | author |"] * 2)):
                output.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    document_version_history_markdown(output, "snap-1", "0.1", "today", "run", "author")

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

    def test_generators_share_snapshot_history_renderer(self):
        for filename in GENERATOR_FILES:
            tree = ast.parse((ROOT / "scripts" / filename).read_text(encoding="utf-8-sig"), filename=filename)
            calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "document_version_history_markdown"]
            self.assertEqual(len(calls), 1, filename)
            self.assertEqual(len(calls[0].args), 6, filename)

    def test_ipos_snapshot_format_preserves_history_until_snapshot_changes(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "block.md"
            history = document_version_history_markdown(output, "snap-1", "0.1", "2026-01-01", "Snapshot snap-1 baseline", "Original Author")
            output.write_text("- Snapshot: `snap-1`\n\n#### Table 1. Version history\n" + "\n".join(history), encoding="utf-8")
            self.assertEqual(document_version_history_markdown(output, "snap-1", "0.1", "2026-01-02", "rerun", "Another Author"), history)
            self.assertEqual(document_version_for_snapshot(output, "snap-2"), "0.2")
            updated = document_version_history_markdown(output, "snap-2", "0.2", "2026-01-03", "Snapshot snap-2 baseline", "New Author")
            self.assertEqual(updated[:-1], history)
            self.assertIn("0.2 | 2026-01-03", updated[-1])

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