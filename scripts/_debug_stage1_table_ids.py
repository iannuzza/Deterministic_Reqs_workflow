import argparse
from pathlib import Path
import importlib.util

parser = argparse.ArgumentParser()
parser.add_argument("--pages", nargs="+", type=int, help="Only inspect these OCR page numbers.")
parser.add_argument("--output", default="logs/debug_stage1_table_ids.txt")
args = parser.parse_args()

repo = Path(__file__).resolve().parent.parent
script = repo / "scripts/generate_stage1_requirements.py"
spec = importlib.util.spec_from_file_location("stage1gen", script)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

mod._init_requirement_id_rules(repo)
index = mod._read_index(repo / "artifacts/stage1_requirements/ocr_extracts/index.csv")
mod._init_source_context(index)

out_lines = []
for page, text_file, _ in index:
    if args.pages and page not in set(args.pages):
        continue
    lines = text_file.read_text(encoding="utf-8", errors="ignore").splitlines()
    page_text_lower = " ".join(mod._clean_statement(x).lower() for x in lines)
    has_id_hdr = any(mod._line_has_req_id_header(x) for x in lines)
    has_tbl = "table" in page_text_lower
    out_lines.append(f"PAGE {page} id_header={has_id_hdr} table_header={has_tbl}")
    for i, raw in enumerate(lines, start=1):
        cands = mod._extract_table_spec_candidates(lines, i-1, page, i, mod._clean_statement(raw), has_id_hdr, has_tbl)
        if cands:
            for c in cands:
                out_lines.append(f"  L{i}: req={c.source_req_id} stmt={c.statement[:140]}")

out_path = repo / args.output
out_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
