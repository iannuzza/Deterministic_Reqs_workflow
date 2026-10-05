import glob

keywords = ["shall", "must", "mandatory", "required", "should", "not be", "need to", "needs to"]
count = 0
files = glob.glob("artifacts/stage1_requirements/ocr_extracts/*.txt")
for fp in files:
    with open(fp, encoding="utf-8", errors="ignore") as f:
        for ln in f.read().splitlines():
            s = ln.strip().lower()
            if s and any(k in s for k in keywords):
                count += 1
print("FILES", len(files))
print("NORMATIVE_LINE_HITS", count)
