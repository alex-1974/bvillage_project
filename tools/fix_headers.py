#!/usr/bin/env python3
# tools/fix_headers.py

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple


EXCLUDE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".mypy_cache", ".pytest_cache",
    "dist", "build", ".tox", ".ruff_cache",
    "bvillage.egg-info", "bvillage_project.egg-info",
}


@dataclass(frozen=True)
class Result:
    path: Path
    changed: bool
    repaired: bool
    parse_ok_before: bool
    parse_ok_after: bool
    note: str


def should_skip(p: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in p.parts)


def normalize_newlines(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def read_text(p: Path) -> str:
    return normalize_newlines(p.read_text(encoding="utf-8", errors="strict"))


def write_text(p: Path, s: str) -> None:
    p.write_text(s, encoding="utf-8", newline="\n")


def ast_ok(text: str) -> bool:
    try:
        ast.parse(text)
        return True
    except SyntaxError:
        return False


def expected_header(repo_root: Path, file_path: Path) -> str:
    rel = file_path.relative_to(repo_root).as_posix()
    return f"# {rel}"


def is_shebang(line: str) -> bool:
    return line.startswith("#!")


def is_future_import(line: str) -> bool:
    return line.lstrip().startswith("from __future__ import ")


def is_docstring_opener(line: str) -> bool:
    t = line.strip()
    # allow optional prefixes (r, u, f, fr, rf, ...)
    prefixes = ("", "r", "u", "f", "fr", "rf", "ur", "ru", "fu", "uf")
    quotes = ('"""', "'''")
    for pref in prefixes:
        for q in quotes:
            if t == pref + q:
                return True
    return False


def ensure_blank_after(lines: list[str], idx: int) -> None:
    nxt = idx + 1
    if nxt >= len(lines):
        lines.append("")
        return
    if lines[nxt].strip() != "":
        lines.insert(nxt, "")


def enforce_header(lines: list[str], header: str) -> Tuple[bool, str]:
    """
    ARCH_SCAN compatible:
    - if shebang present: line1 shebang, line2 header
    - else: line1 header
    """
    changed = False

    if not lines:
        lines[:] = [header, ""]
        return True, "created header in empty file"

    if is_shebang(lines[0]):
        # ensure line2 exists and equals header
        if len(lines) == 1:
            lines.append(header)
            changed = True
        elif lines[1] != header:
            lines[1] = header
            changed = True
        # keep a blank line after header (line3) if needed
        if len(lines) > 2 and lines[2].strip() != "":
            lines.insert(2, "")
            changed = True
        elif len(lines) == 2:
            lines.append("")
            changed = True
        return changed, "shebang: enforced header on line 2"

    # no shebang
    if lines[0] != header:
        # if the file starts with docstring opener or future import, insert header above it
        if is_docstring_opener(lines[0]) or is_future_import(lines[0]):
            lines.insert(0, header)
            ensure_blank_after(lines, 0)
            return True, "inserted header above docstring/future-import"
        else:
            lines[0] = header
            ensure_blank_after(lines, 0)
            return True, "replaced first line with header"

    # already correct, but ensure blank line after header
    if len(lines) > 1 and lines[1].strip() != "":
        lines.insert(1, "")
        return True, "inserted blank line after header"

    return False, "header ok"


def repair_removed_docstring_opener(lines: list[str]) -> Tuple[bool, str]:
    """
    Repairs the common damage: docstring opener was removed when a header was inserted.

    Pattern:
      - Header exists (line1 or line2 if shebang)
      - File does NOT parse
      - There exists a triple-quote later in the file (likely closing delimiter)
      - The first non-blank, non-comment, non-future-import line after the header
        is not already a docstring opener.
      => Insert a docstring opener right before that line.

    Conservative: only triggers if we find at least one triple-quote later.
    """
    # determine where "code starts" after header
    i = 0
    if not lines:
        return False, "no content"
    if is_shebang(lines[0]):
        hdr_idx = 1
        start_idx = 2
    else:
        hdr_idx = 0
        start_idx = 1

    if len(lines) <= hdr_idx or not lines[hdr_idx].startswith("# "):
        return False, "no header present (unexpected)"

    joined = "\n".join(lines)
    if ('"""' not in joined) and ("'''" not in joined):
        return False, "no triple-quotes found (skip repair)"

    # find first "substantive" line after header
    j = start_idx
    while j < len(lines):
        s = lines[j].strip()
        if s == "" or s.startswith("#"):
            j += 1
            continue
        if is_future_import(lines[j]):
            j += 1
            continue
        break

    if j >= len(lines):
        return False, "no substantive line found"

    if is_docstring_opener(lines[j]) or lines[j].lstrip().startswith(('"""', "'''")):
        return False, "docstring opener already present"

    # Insert docstring opener at line j
    lines.insert(j, '"""')
    return True, "inserted missing docstring opener"


def process_file(repo_root: Path, p: Path, apply: bool) -> Result:
    original = read_text(p)
    parse_ok_before = ast_ok(original)

    header = expected_header(repo_root, p)
    lines = original.split("\n")

    changed1, note1 = enforce_header(lines, header)
    candidate = "\n".join(lines)

    # if parse is still broken, try repair
    repaired = False
    parse_ok_after = ast_ok(candidate)
    note2 = ""
    if not parse_ok_after:
        changed2, note2 = repair_removed_docstring_opener(lines)
        if changed2:
            repaired = True
            candidate = "\n".join(lines)
            parse_ok_after = ast_ok(candidate)

    changed = (candidate != original)

    if apply and changed:
        write_text(p, candidate)

    note = note1
    if note2:
        note = f"{note1}; {note2}"

    return Result(
        path=p,
        changed=changed,
        repaired=repaired,
        parse_ok_before=parse_ok_before,
        parse_ok_after=parse_ok_after,
        note=note,
    )


def iter_py(repo_root: Path) -> list[Path]:
    out: list[Path] = []
    for p in repo_root.rglob("*.py"):
        if should_skip(p):
            continue
        if p.is_file():
            out.append(p)
    return sorted(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Fix '# <repo path>' headers and repair common docstring damage.")
    ap.add_argument("--root", default=".", help="Repo root (default: .)")
    ap.add_argument("--apply", action="store_true", help="Write changes to disk")
    ap.add_argument("--report-unrepaired", action="store_true", help="Only list files that still don't parse after fixes")
    args = ap.parse_args()

    repo_root = Path(args.root).resolve()
    files = iter_py(repo_root)

    results: list[Result] = []
    for p in files:
        results.append(process_file(repo_root, p, apply=args.apply))

    unrepaired = [r for r in results if not r.parse_ok_after]
    changed = [r for r in results if r.changed]

    if args.report_unrepaired:
        if not unrepaired:
            print("UNREPAIRED: none")
            return 0
        print(f"UNREPAIRED: {len(unrepaired)} file(s)")
        for r in unrepaired:
            rel = r.path.relative_to(repo_root).as_posix()
            print(f"- {rel}  (before_parse={r.parse_ok_before}, after_parse={r.parse_ok_after})  note={r.note}")
        return 1

    if not args.apply:
        print(f"Planned changes: {len(changed)} file(s)")
        for r in changed:
            rel = r.path.relative_to(repo_root).as_posix()
            print(f"- {rel}  repaired={r.repaired}  note={r.note}")
        if unrepaired:
            print(f"\nWARNING: {len(unrepaired)} file(s) still do not parse after planned fixes.")
            print("Run: ./tools/fix_headers.py --report-unrepaired")
        print("\nDry-run only. Re-run with --apply to write changes.")
        return 0

    print(f"Applied changes: {len(changed)} file(s)")
    if unrepaired:
        print(f"ERROR: {len(unrepaired)} file(s) still do not parse after applying fixes.")
        print("Run: ./tools/fix_headers.py --report-unrepaired")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
