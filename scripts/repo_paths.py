"""Portable addresses for repository-owned inputs and derived artifacts."""

from pathlib import Path, PurePosixPath, PureWindowsPath
import csv


REPOSITORY_DIRECTORIES = frozenset({
    "artifacts", "config", "data", "docs", "local_memory", "scripts", "specs", "templates",
})


def resolve_repo_path(repo_root: Path, value: str | Path) -> Path:
    root = repo_root.resolve()
    text = str(value).replace("\\", "/")
    if not text.strip():
        raise ValueError("Repository path must not be empty")
    path = Path(text)
    if not PurePosixPath(text).is_absolute() and not PureWindowsPath(text).is_absolute():
        return (root / path).resolve()
    if path.is_absolute() and path.is_relative_to(root):
        return path.resolve()
    parts = PurePosixPath(text).parts
    anchors = [index for index, part in enumerate(parts) if part in REPOSITORY_DIRECTORIES]
    if len(anchors) == 1:
        return root.joinpath(*parts[anchors[0]:]).resolve()
    if anchors:
        raise ValueError(f"Ambiguous repository path: {value}")
    return path


def portable_repo_path(repo_root: Path, value: str | Path) -> str:
    path = resolve_repo_path(repo_root, value)
    try:
        return path.relative_to(repo_root.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"Keep portable workflow inputs inside the repository: {value}") from exc


def normalize_ocr_index(repo_root: Path, index_path: Path) -> int:
    """Relativize derived OCR addresses without changing text or authority records."""
    index_path = resolve_repo_path(repo_root, index_path)
    with index_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        if not fields or not {"source_file", "text_file"}.issubset(fields):
            raise ValueError("OCR index must contain source_file and text_file columns")
        rows = list(reader)
    for row in rows:
        for field in ("source_file", "text_file"):
            if row[field]:
                row[field] = portable_repo_path(repo_root, row[field])
    temporary = index_path.with_suffix(index_path.suffix + ".portable.tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(index_path)
    return len(rows)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Normalize derived OCR paths for portable clones")
    parser.add_argument("--normalize-ocr-index", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    count = normalize_ocr_index(root, args.normalize_ocr_index)
    print(f"OCR path normalization: PASS ({count} rows)")