import shutil
import io
import re
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.workflow_routing import (
    apply_docx_common_spec_formatting,
    apply_docx_ipos_requirement_style_guard,
    validate_ipos_docx_layout,
)


class DocxLayoutTests(unittest.TestCase):
    def test_core_date_type_namespace_survives_common_formatting(self):
        terms = "http://purl.org/dc/terms/"
        xsi = "{http://www.w3.org/2001/XMLSchema-instance}"
        members = {
            "docProps/core.xml": (
                '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                'xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                '<dcterms:created xsi:type="dcterms:W3CDTF">2026-01-01T00:00:00Z</dcterms:created>'
                '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-01-02T00:00:00Z</dcterms:modified>'
                '</cp:coreProperties>'
            ),
            "word/document.xml": '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:sectPr/></w:body></w:document>',
            "word/_rels/document.xml.rels": '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>',
            "[Content_Types].xml": '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"></Types>',
        }
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "metadata.docx"
            with zipfile.ZipFile(output, "w") as archive:
                for name, content in members.items():
                    archive.writestr(name, content)
            ET.register_namespace("otherterms", terms)
            apply_docx_common_spec_formatting(output)
            with zipfile.ZipFile(output) as archive:
                core = archive.read("docProps/core.xml")
            namespaces = dict(value for _, value in ET.iterparse(io.BytesIO(core), events=("start-ns",)))
            root = ET.fromstring(core)
            for name in ("created", "modified"):
                node = root.find("{" + terms + "}" + name)
                prefix, local_name = node.get(xsi + "type").split(":")
                self.assertEqual(namespaces.get(prefix), terms)
                self.assertEqual(local_name, "W3CDTF")

    def test_ipos_requirement_style_guard_removes_template_requirement_styles(self):
        root = Path(__file__).parents[1] / "artifacts"
        source = next(root.glob("stage6_digital_ipos/blocks/*/*.docx"))
        word_namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "ipos.docx"
            shutil.copyfile(source, output)
            with zipfile.ZipFile(output) as archive:
                members = {info.filename: archive.read(info.filename) for info in archive.infolist()}
            root_xml = ET.fromstring(members["word/document.xml"])
            body = root_xml.find(f"{word_namespace}body")
            authored = next(
                paragraph
                for paragraph in body
                if paragraph.tag == f"{word_namespace}p"
                and re.fullmatch(
                    r"IPOS-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}",
                    "".join(node.text or "" for node in paragraph.iter(f"{word_namespace}t")).strip(),
                )
            )
            properties = authored.find(f"{word_namespace}pPr")
            if properties is None:
                properties = ET.Element(f"{word_namespace}pPr")
                authored.insert(0, properties)
            ET.SubElement(properties, f"{word_namespace}pStyle", {f"{word_namespace}val": "STReq"})
            members["word/document.xml"] = ET.tostring(root_xml, encoding="utf-8", xml_declaration=True)
            with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for filename, content in members.items():
                    archive.writestr(filename, content)

            apply_docx_ipos_requirement_style_guard(output)

            with zipfile.ZipFile(output) as archive:
                result = archive.read("word/document.xml")
            self.assertNotIn(b'w:val="STReq"', result)
            self.assertNotIn(b'w:val="STMacroReq"', result)
            self.assertNotIn(b'w:val="NoSpacing"', result)

    def test_all_materialized_docx_files_have_title_page_and_explicit_toc_break(self):
        root = Path(__file__).parents[1] / "artifacts"
        word_namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        documents = sorted(path for path in root.rglob("*.docx") if not path.name.startswith("~$"))
        self.assertEqual(len(documents), 11)
        for document in documents:
            self.assertEqual(validate_ipos_docx_layout(document), [], str(document))
            with zipfile.ZipFile(document) as archive:
                root_xml = ET.fromstring(archive.read("word/document.xml"))
            body = root_xml.find(f"{word_namespace}body")
            paragraphs = [element for element in body if element.tag == f"{word_namespace}p"]
            toc_index = next(
                index
                for index, paragraph in enumerate(paragraphs)
                if "".join(node.text or "" for node in paragraph.iter(f"{word_namespace}t")).strip()
                == "0.1 Table of contents"
            )
            nav_index = next(
                index
                for index, paragraph in enumerate(paragraphs)
                if "".join(node.text or "" for node in paragraph.iter(f"{word_namespace}t")).strip()
                == "0. Document Navigation"
            )
            title_index = next(
                index
                for index, paragraph in enumerate(paragraphs)
                if "Specification" in "".join(node.text or "" for node in paragraph.iter(f"{word_namespace}t"))
                or " IPOS - " in "".join(node.text or "" for node in paragraph.iter(f"{word_namespace}t"))
            )
            self.assertLess(title_index, toc_index, str(document))
            self.assertLess(toc_index, nav_index, str(document))
            self.assertIsNotNone(
                paragraphs[toc_index - 1].find(f".//{word_namespace}br[@{word_namespace}type='page']"),
                str(document),
            )

    def test_shared_layout_puts_title_page_before_navigation_and_adds_page_footer(self):
        source = Path(__file__).parents[1] / "artifacts" / "stage5_drs" / "digital_requirements_specification.docx"
        word_namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "layout.docx"
            shutil.copyfile(source, output)
            apply_docx_common_spec_formatting(output)
            with zipfile.ZipFile(output) as archive:
                root = ET.fromstring(archive.read("word/document.xml"))
                body = root.find(f"{word_namespace}body")
                paragraphs = [element for element in body if element.tag == f"{word_namespace}p"]
                text = [
                    "".join(node.text or "" for node in paragraph.iter(f"{word_namespace}t")).strip()
                    for paragraph in paragraphs
                ]
                self.assertLess(text.index("0.1 Table of contents"), text.index("0. Document Navigation"))
                self.assertLess(text.index("Digital Requirements Specification"), text.index("0.1 Table of contents"))
                self.assertLess(text.index("0.1 Table of contents"), text.index("0. Document Navigation"))
                table_of_contents = paragraphs[text.index("0.1 Table of contents")]
                self.assertIsNotNone(table_of_contents.find(f"{word_namespace}pPr/{word_namespace}pageBreakBefore"))
                first_body_paragraph = paragraphs[text.index("0.1 Table of contents") - 1]
                self.assertIsNotNone(
                    first_body_paragraph.find(f".//{word_namespace}br[@{word_namespace}type='page']")
                )
                footer_parts = [name for name in archive.namelist() if name.startswith("word/footer")]
                self.assertTrue(
                    any(
                        "PAGE" in archive.read(name).decode("utf-8", errors="ignore")
                        and "right" in archive.read(name).decode("utf-8", errors="ignore")
                        for name in footer_parts
                    )
                )


if __name__ == "__main__":
    unittest.main()
