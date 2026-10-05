#!/usr/bin/env python3
"""Convert a PDF file to a single HTML file using PyMuPDF.

Usage:
  python scripts/pdf_to_html.py --input specs/Morag_Module_ERS_v1.1.pdf
  python scripts/pdf_to_html.py --input input.pdf --output output.html
"""

import argparse
import html
from pathlib import Path

import pymupdf as fitz


def convert_pdf_to_html(input_pdf: Path, output_html: Path) -> None:
    doc = fitz.open(input_pdf)

    parts = [
        "<!doctype html><html><head><meta charset=\"utf-8\"><title>"
        + html.escape(input_pdf.name)
        + "</title><style>"
        + "body{font-family:Arial,sans-serif;margin:24px}"
        + ".page{margin:0 0 28px 0;padding:12px;border:1px solid #ddd}"
        + ".page-title{font-weight:700;margin:0 0 12px 0}"
        + "</style></head><body>"
    ]

    for i, page in enumerate(doc):
        parts.append(
            f'<section class="page"><div class="page-title">Page {i + 1}</div>'
            + page.get_text("html")
            + "</section>"
        )

    parts.append("</body></html>")
    output_html.write_text("".join(parts), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert PDF to HTML")
    parser.add_argument("--input", required=True, help="Path to input PDF")
    parser.add_argument("--output", help="Path to output HTML (optional)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    input_pdf = Path(args.input)
    if not input_pdf.exists():
        raise FileNotFoundError(f"Input PDF not found: {input_pdf}")

    output_html = Path(args.output) if args.output else input_pdf.with_suffix(".html")
    convert_pdf_to_html(input_pdf, output_html)

    print(f"Generated HTML: {output_html.resolve()}")
    print(f"Size (bytes): {output_html.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
