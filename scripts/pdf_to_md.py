import sys
from pathlib import Path
import pymupdf as fitz  # PyMuPDF


def pdf_to_markdown(pdf_path: str, md_path: str) -> None:
    pdf_file = Path(pdf_path)
    md_file = Path(md_path)

    if not pdf_file.exists():
        raise FileNotFoundError(f"File PDF non trovato: {pdf_file}")

    markdown_parts = []

    with fitz.open(pdf_file) as doc:
        title = pdf_file.stem
        markdown_parts.append(f"# {title}\n")

        for page_number, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()

            markdown_parts.append(f"\n## Pagina {page_number}\n")

            if text:
                markdown_parts.append(text + "\n")
            else:
                markdown_parts.append("_Nessun testo estratto da questa pagina._\n")

    md_file.write_text("\n".join(markdown_parts), encoding="utf-8")


def main():
    if len(sys.argv) != 3:
        print("Uso: python pdf_to_md.py input.pdf output.md")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_md = sys.argv[2]

    try:
        pdf_to_markdown(input_pdf, output_md)
        print(f"Conversione completata: {output_md}")
    except Exception as exc:
        print(f"Errore: {exc}")
        sys.exit(2)


if __name__ == "__main__":
    main()