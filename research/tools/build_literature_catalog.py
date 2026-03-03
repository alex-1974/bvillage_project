#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

CHUNK = 1024 * 1024  # 1MB


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            b = f.read(CHUNK)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def slugify(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^A-Za-z0-9_\-\.]+", "", s)
    s = re.sub(r"_+", "_", s)
    return s.strip("_") or "unknown"


def try_page_count(pdf_path: Path) -> Optional[int]:
    try:
        from pypdf import PdfReader  # type: ignore
        reader = PdfReader(str(pdf_path))
        return len(reader.pages)
    except Exception:
        return None


def infer_year(fname: str) -> Optional[int]:
    years = re.findall(r"(19\d{2}|20\d{2}|1[5-9]\d{2})", fname)
    if not years:
        return None
    try:
        return int(years[0])
    except Exception:
        return None


def infer_country(fname: str, rel_parts: Tuple[str, ...]) -> str:
    m = re.match(r"^(DE|AT|UK|FR|CH|EU)_", fname)
    if m:
        return m.group(1)
    for p in rel_parts:
        if p in {"DE", "AT", "UK", "FR", "CH", "EU"}:
            return p
    return "UNKNOWN"


def infer_authors(fname: str) -> Optional[str]:
    parts = fname.split("_")
    if len(parts) < 3:
        return None
    if parts[0] in {"DE", "AT", "UK", "FR", "CH", "EU"}:
        for i, tok in enumerate(parts):
            if re.fullmatch(r"(19\d{2}|20\d{2}|1[5-9]\d{2})", tok):
                if i >= 2:
                    author = "_".join(parts[2:i])
                    author = author.replace("__", "_").strip("_")
                    return author or None
    return None


def tags_from_relpath(rel: Path) -> List[str]:
    parts = rel.parts
    tags: List[str] = []
    if parts:
        cat = parts[0]
        cat = re.sub(r"^\d+_", "", cat)
        tags.append(cat)
    if "09_case_studies" in parts:
        tags.append("case_study")
        for p in parts:
            if p in {"DE", "AT", "UK", "FR", "CH", "EU"}:
                tags.append(p)
    return sorted(set(tags))


def is_ignored(rel: Path) -> bool:
    # Ignore internal maintenance folders anywhere under root
    parts = rel.parts
    return "__hash_reports" in parts or "__duplicates" in parts or ".git" in parts


@dataclass
class CatalogRow:
    id: str
    sha256: str
    bytes: int
    pages: Optional[int]
    filename: str
    relpath: str
    category: str
    country: str
    year: Optional[int]
    authors_guess: Optional[str]
    title_guess: str
    tags: List[str]
    dup_group_size: int
    dup_is_canonical: bool


def to_yaml(rows: List[CatalogRow]) -> str:
    def esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"')

    out = []
    out.append("# Literature Catalog")
    out.append(f"# generated: {datetime.now().isoformat(timespec='seconds')}")
    out.append("entries:")
    for r in rows:
        out.append(f"  - id: \"{esc(r.id)}\"")
        out.append(f"    sha256: \"{r.sha256}\"")
        out.append(f"    bytes: {r.bytes}")
        out.append(f"    pages: {r.pages if r.pages is not None else 'null'}")
        out.append(f"    filename: \"{esc(r.filename)}\"")
        out.append(f"    relpath: \"{esc(r.relpath)}\"")
        out.append(f"    category: \"{esc(r.category)}\"")
        out.append(f"    country: \"{esc(r.country)}\"")
        out.append(f"    year: {r.year if r.year is not None else 'null'}")
        out.append(f"    authors_guess: \"{esc(r.authors_guess)}\"" if r.authors_guess else "    authors_guess: null")
        out.append(f"    title_guess: \"{esc(r.title_guess)}\"")
        out.append("    tags:")
        for t in r.tags:
            out.append(f"      - \"{esc(t)}\"")
        out.append(f"    dup_group_size: {r.dup_group_size}")
        out.append(f"    dup_is_canonical: {str(r.dup_is_canonical).lower()}")
    out.append("")
    return "\n".join(out)


def to_markdown(rows: List[CatalogRow]) -> str:
    groups: Dict[str, List[CatalogRow]] = {}
    for r in rows:
        groups.setdefault(r.category, []).append(r)

    lines: List[str] = []
    lines.append("# Literaturkatalog")
    lines.append("")
    lines.append(f"_Generiert: {datetime.now().isoformat(timespec='seconds')}_")
    lines.append("")
    for cat in sorted(groups.keys()):
        lines.append(f"## {cat}")
        lines.append("")
        for r in sorted(groups[cat], key=lambda x: (x.country, x.year or 9999, x.filename.lower())):
            meta = []
            if r.country != "UNKNOWN":
                meta.append(r.country)
            if r.year is not None:
                meta.append(str(r.year))
            if r.pages is not None:
                meta.append(f"{r.pages}p")
            if r.dup_group_size > 1:
                meta.append(f"DUP×{r.dup_group_size}" + (" (canonical)" if r.dup_is_canonical else ""))
            meta_str = " · ".join(meta)
            lines.append(f"- **{r.title_guess}**  \n  `{r.relpath}`  \n  {meta_str}")
        lines.append("")
    return "\n".join(lines)


def to_duplicates_csv(path: Path, dup_map: Dict[str, List[CatalogRow]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sha256", "bytes", "canonical_relpath", "dup_relpath"])
        for sha, recs in sorted(dup_map.items(), key=lambda kv: (len(kv[1]), kv[0]), reverse=True):
            if len(recs) < 2:
                continue
            # canonical = lexicographically smallest relpath (stable + predictable)
            recs_sorted = sorted(recs, key=lambda r: r.relpath)
            canonical = recs_sorted[0]
            for dup in recs_sorted[1:]:
                w.writerow([sha, canonical.bytes, canonical.relpath, dup.relpath])


def to_duplicates_md(path: Path, dup_map: Dict[str, List[CatalogRow]]) -> None:
    lines: List[str] = []
    lines.append("# Dublettenreport")
    lines.append("")
    lines.append(f"_Generiert: {datetime.now().isoformat(timespec='seconds')}_")
    lines.append("")
    groups = [(sha, recs) for sha, recs in dup_map.items() if len(recs) > 1]
    groups.sort(key=lambda x: (len(x[1]), x[0]), reverse=True)

    if not groups:
        lines.append("Keine Dubletten gefunden.")
        path.write_text("\n".join(lines), encoding="utf-8")
        return

    for sha, recs in groups:
        recs_sorted = sorted(recs, key=lambda r: r.relpath)
        canonical = recs_sorted[0]
        lines.append(f"## SHA256 {sha} (×{len(recs_sorted)})")
        lines.append("")
        lines.append(f"- **canonical:** `{canonical.relpath}`")
        for dup in recs_sorted[1:]:
            lines.append(f"- dup: `{dup.relpath}`")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Folder to scan (catalog root). Everything below is indexed.")
    ap.add_argument("--outdir", required=True, help="Output directory for catalog files.")
    ap.add_argument("--ext", default=".pdf", help="Comma-separated extensions to include. Default: .pdf")
    ap.add_argument("--include-nonpdf", action="store_true", help="Also include .html/.csv/.txt regardless of --ext")
    ap.add_argument("--no-hash", action="store_true", help="Skip SHA256 (faster, disables duplicate detection).")
    ap.add_argument("--no-pages", action="store_true", help="Skip PDF page counting.")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    exts = {e.strip().lower() for e in args.ext.split(",") if e.strip()}
    if args.include_nonpdf:
        exts |= {".html", ".htm", ".csv", ".txt"}

    rows: List[CatalogRow] = []
    temp: List[Tuple[Path, Path]] = []  # (abs, rel)

    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if is_ignored(rel):
            continue
        if p.suffix.lower() not in exts:
            continue
        temp.append((p, rel))

    # First pass: compute hashes if enabled
    sha_by_rel: Dict[str, str] = {}
    size_by_rel: Dict[str, int] = {}
    pages_by_rel: Dict[str, Optional[int]] = {}

    for abs_p, rel in temp:
        rel_s = rel.as_posix()
        size_by_rel[rel_s] = abs_p.stat().st_size
        if args.no_pages or abs_p.suffix.lower() != ".pdf":
            pages_by_rel[rel_s] = None
        else:
            pages_by_rel[rel_s] = try_page_count(abs_p)
        if args.no_hash:
            sha_by_rel[rel_s] = "SKIPPED"
        else:
            sha_by_rel[rel_s] = sha256_file(abs_p)

    # Build duplicate map (sha -> list of relpaths) if hashing enabled
    dup_map_paths: Dict[str, List[str]] = {}
    if not args.no_hash:
        for rel_s, sha in sha_by_rel.items():
            dup_map_paths.setdefault(sha, []).append(rel_s)

    # Determine canonical relpath per sha (lexicographically smallest)
    canonical_by_sha: Dict[str, str] = {}
    if not args.no_hash:
        for sha, rel_list in dup_map_paths.items():
            canonical_by_sha[sha] = sorted(rel_list)[0]

    # Second pass: build rows with duplicate annotation
    for abs_p, rel in temp:
        rel_s = rel.as_posix()
        fname = abs_p.name
        rel_parts = rel.parts

        sha = sha_by_rel[rel_s]
        size = size_by_rel[rel_s]
        pages = pages_by_rel[rel_s]

        category = rel_parts[0] if rel_parts else "UNKNOWN"
        category_pretty = category.replace("_", " ")

        country = infer_country(fname, rel_parts)
        year = infer_year(fname)
        authors = infer_authors(fname)

        title_guess = Path(fname).stem.replace("__", " — ").replace("_", " ")
        title_guess = re.sub(r"\s+", " ", title_guess).strip()

        short = sha[:12] if sha != "SKIPPED" else slugify(rel_s)[:12]
        rid = f"{country}:{slugify(Path(fname).stem)[:40]}:{short}"

        tags = tags_from_relpath(rel)

        dup_group_size = 1
        dup_is_canonical = True
        if sha != "SKIPPED":
            dup_group_size = len(dup_map_paths.get(sha, [rel_s]))
            dup_is_canonical = (canonical_by_sha.get(sha, rel_s) == rel_s)

        rows.append(
            CatalogRow(
                id=rid,
                sha256=sha,
                bytes=size,
                pages=pages,
                filename=fname,
                relpath=rel_s,
                category=category_pretty,
                country=country,
                year=year,
                authors_guess=authors,
                title_guess=title_guess,
                tags=tags,
                dup_group_size=dup_group_size,
                dup_is_canonical=dup_is_canonical,
            )
        )

    # Write main CSV
    csv_path = outdir / "library_catalog.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "id", "sha256", "bytes", "pages", "country", "year",
            "category", "authors_guess", "title_guess", "tags",
            "relpath", "filename",
            "dup_group_size", "dup_is_canonical",
        ])
        for r in rows:
            w.writerow([
                r.id, r.sha256, r.bytes, r.pages if r.pages is not None else "",
                r.country, r.year if r.year is not None else "",
                r.category, r.authors_guess or "", r.title_guess,
                ";".join(r.tags), r.relpath, r.filename,
                r.dup_group_size, str(r.dup_is_canonical).lower()
            ])

    # Write YAML + MD
    (outdir / "library_catalog.yaml").write_text(to_yaml(rows), encoding="utf-8")
    (outdir / "library_catalog.md").write_text(to_markdown(rows), encoding="utf-8")

    # Write duplicates reports (only if hashing enabled)
    dup_map: Dict[str, List[CatalogRow]] = {}
    if not args.no_hash:
        for r in rows:
            dup_map.setdefault(r.sha256, []).append(r)

        duplicates_csv = outdir / "duplicates.csv"
        duplicates_md = outdir / "duplicates.md"
        to_duplicates_csv(duplicates_csv, dup_map)
        to_duplicates_md(duplicates_md, dup_map)
        print(f"- {duplicates_csv}")
        print(f"- {duplicates_md}")
    else:
        print("(hashing disabled; duplicate detection skipped)")

    print(f"Wrote {len(rows)} entries")
    print(f"- {csv_path}")
    print(f"- {outdir / 'library_catalog.yaml'}")
    print(f"- {outdir / 'library_catalog.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
