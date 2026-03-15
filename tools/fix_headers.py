#!/usr/bin/env python3
# tools/fix_headers.py

"""
Fix Python file headers.

Repairs the canonical header:

    # relative/path/to/file.py

Rules
-----
If a shebang exists:

    #!/usr/bin/env python3
    # relative/path.py

Otherwise:

    # relative/path.py

Guarantees
----------
- never changes program semantics
- AST parse validated before/after
- minimal modifications
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path


EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
    ".tox",
    ".ruff_cache",
    "generated",
    "research",
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
    if not s.endswith("\n"):
        s += "\n"
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


def is_docstring_opener(line: str) -> bool:
    t = line.strip()
    return t in ('"""', "'''")


def enforce_header(lines: list[str], header: str):
    changed = False

    if not lines:
        lines[:] = [header, ""]
        return True, "created header in empty file"

    if is_shebang(lines[0]):

        if len(lines) == 1:
            lines.append(header)
            changed = True
        elif lines[1] != header:
            lines[1] = header
            changed = True

        if len(lines) < 3 or lines[2].strip() != "":
            lines.insert(2, "")
            changed = True

        return changed, "shebang header ensured"

    if lines[0] != header:

        if is_docstring_opener(lines[0]):
            lines.insert(0, header)
            lines.insert(1, "")
            return True, "header inserted above docstring"

        lines[0] = header

        if len(lines) < 2 or lines[1].strip() != "":
            lines.insert(1, "")

        return True, "header replaced"

    if len(lines) > 1 and lines[1].strip() != "":
        lines.insert(1, "")
        return True, "blank after header inserted"

    return False, "header ok"


def repair_missing_docstring(lines: list[str]):
    joined = "\n".join(lines)

    if ('"""' not in joined) and ("'''" not in joined):
        return False, "no triple quotes"

    start = 1
    if is_shebang(lines[0]):
        start = 2

    i = start
    while i < len(lines):

        s = lines[i].strip()

        if s == "" or s.startswith("#"):
            i += 1
            continue

        if is_docstring_opener(lines[i]):
            return False, "docstring exists"

        lines.insert(i, '"""')
        return True, "docstring opener inserted"

    return False, "no insertion point"


def process_file(repo_root: Path, p: Path, apply: bool):

    original = read_text(p)
    parse_ok_before = ast_ok(original)

    header = expected_header(repo_root, p)

    lines = original.split("\n")

    changed1, note1 = enforce_header(lines, header)

    candidate = "\n".join(lines)

    parse_ok_after = ast_ok(candidate)

    repaired = False
    note2 = ""

    if not parse_ok_after:

        changed2, note2 = repair_missing_docstring(lines)

        if changed2:
            repaired = True
            candidate = "\n".join(lines)
            parse_ok_after = ast_ok(candidate)

    changed = candidate != original

    if apply and changed:
        write_text(p, candidate)

    note = note1
    if note2:
        note = note1 + "; " + note2

    return Result(
        p,
        changed,
        repaired,
        parse_ok_before,
        parse_ok_after,
        note,
    )


def iter_py(root: Path):

    for p in root.rglob("*.py"):

        if should_skip(p):
            continue

        if p.is_file():
            yield p


def main():

    ap = argparse.ArgumentParser()

    ap.add_argument("--root", default=".")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report-unrepaired", action="store_true")

    args = ap.parse_args()

    root = Path(args.root).resolve()

    results = []

    for p in iter_py(root):
        results.append(process_file(root, p, args.apply))

    unrepaired = [r for r in results if not r.parse_ok_after]
    changed = [r for r in results if r.changed]

    if args.report_unrepaired:

        if not unrepaired:
            print("UNREPAIRED: none")
            return 0

        print("UNREPAIRED FILES")

        for r in unrepaired:
            rel = r.path.relative_to(root)
            print(rel)

        return 1

    if not args.apply:

        print("Planned changes:", len(changed))

        for r in changed:
            print(r.path.relative_to(root), r.note)

        return 0

    print("Applied changes:", len(changed))

    if unrepaired:
        print("ERROR: some files still do not parse")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
