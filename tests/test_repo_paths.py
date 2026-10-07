import sys
import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from repo_paths import normalize_ocr_index, portable_repo_path, resolve_repo_path
import build_rag_index
import crosscheck_stage1_requirements_rag
import extract_source_io_catalog
import generate_stage1_requirements


class RepoPathTests(unittest.TestCase):
    def test_normalize_ocr_index_preserves_columns_and_non_path_values(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            index = root / "index.csv"
            fields = ["source_file", "page", "text_file", "status"]
            with index.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerow({"source_file": "C:/old/project/specs/source.pdf", "page": "3", "text_file": "C:/old/project/artifacts/stage1_requirements/page.txt", "status": "text-extracted"})
            self.assertEqual(normalize_ocr_index(root, index), 1)
            original = index.read_bytes()
            self.assertEqual(normalize_ocr_index(root, index), 1)
            self.assertEqual(index.read_bytes(), original)
            with index.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(reader.fieldnames, fields)
                self.assertEqual(list(reader), [{"source_file": "specs/source.pdf", "page": "3", "text_file": "artifacts/stage1_requirements/page.txt", "status": "text-extracted"}])

    def test_ocr_readers_use_current_clone_for_relative_and_legacy_index_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            index = root / "artifacts/stage1_requirements/ocr_extracts/index.csv"
            index.parent.mkdir(parents=True)
            page = index.with_name("page.txt")
            page.write_text("Source-backed controller behavior.\n", encoding="utf-8")
            modules = (generate_stage1_requirements, crosscheck_stage1_requirements_rag, extract_source_io_catalog)
            for prefix in ("", "C:/previous/account/project/", "/home/previous/project/"):
                with self.subTest(prefix=prefix):
                    with index.open("w", newline="", encoding="utf-8") as handle:
                        writer = csv.writer(handle)
                        writer.writerow(["source_file", "page", "text_file", "status"])
                        writer.writerow([prefix + "specs/source.pdf", 1, prefix + "artifacts/stage1_requirements/ocr_extracts/page.txt", "text-extracted"])
                    with patch.object(modules[0], "__file__", str(root / "scripts/generate_stage1_requirements.py")), \
                            patch.object(modules[1], "__file__", str(root / "scripts/crosscheck_stage1_requirements_rag.py")), \
                            patch.object(modules[2], "__file__", str(root / "scripts/extract_source_io_catalog.py")):
                        records = generate_stage1_requirements._read_index(index)
                        coverage_pages, source = crosscheck_stage1_requirements_rag._load_index(index)
                        io_pages = extract_source_io_catalog._read_pages(index)
                    rag_pages = build_rag_index._load_index(index, root)
                    self.assertEqual(records, [(1, page, "specs/source.pdf")])
                    self.assertEqual(coverage_pages, {1: page})
                    self.assertEqual(source, "specs/source.pdf")
                    self.assertEqual(io_pages[0][1], page)
                    self.assertEqual(rag_pages[0].text_file, page)
                    self.assertEqual(rag_pages[0].source_file, "specs/source.pdf")

    def test_relative_paths_resolve_from_repo_not_working_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(resolve_repo_path(root, "specs/source.pdf"), root / "specs/source.pdf")
            self.assertEqual(resolve_repo_path(root, r"artifacts\stage1_requirements\page.txt"), root / "artifacts/stage1_requirements/page.txt")

    def test_legacy_addresses_bind_to_current_clone(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for prefix in ("C:/old/account/project/", "/home/old/project/", "//server/share/project/"):
                with self.subTest(prefix=prefix):
                    value = prefix + "artifacts/stage1_requirements/page.txt"
                    self.assertEqual(resolve_repo_path(root, value), root / "artifacts/stage1_requirements/page.txt")
                    self.assertEqual(portable_repo_path(root, value), "artifacts/stage1_requirements/page.txt")

    def test_current_paths_serialize_without_machine_prefix(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(portable_repo_path(root, root / "specs/source.pdf"), "specs/source.pdf")

    def test_external_and_ambiguous_paths_are_not_silently_relocated(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                portable_repo_path(root, "/external/source.pdf")
            with self.assertRaises(ValueError):
                resolve_repo_path(root, "/old/specs/archive/artifacts/page.txt")
            with self.assertRaises(ValueError):
                resolve_repo_path(root, "")