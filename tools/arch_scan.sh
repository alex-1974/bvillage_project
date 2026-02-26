#!/usr/bin/env bash
# tools/arch_scan.sh
#
# BVILLAGE – Architecture Scanner
#
# Usage:
#   ./tools/arch_scan.sh
#   ./tools/arch_scan.sh .                         # explicit root
#   ./tools/arch_scan.sh . --out docs/ARCH_SCAN.txt
#   ./tools/arch_scan.sh . --json --out docs/ARCH_SCAN.json
#   ./tools/arch_scan.sh . --archive               # writes to docs/archive with timestamp
#   ./tools/arch_scan.sh . --summary-only          # only summary sections (no per-file overview)
#
# Header rule:
# - If line 1 starts with '#!' (shebang), then line 2 must be '# <repo path>'
# - Else line 1 must be '# <repo path>'

set -euo pipefail

ROOT="."
MODE="--text"
OUT_PATH=""
ARCHIVE=0
SUMMARY_ONLY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) MODE="--json"; shift ;;
    --text) MODE="--text"; shift ;;
    --out)
      OUT_PATH="${2:-}"
      [[ -z "$OUT_PATH" ]] && { echo "ERROR: --out requires a path" >&2; exit 2; }
      shift 2
      ;;
    --archive) ARCHIVE=1; shift ;;
    --summary-only) SUMMARY_ONLY=1; shift ;;
    -h|--help)
      sed -n '1,80p' "$0"
      exit 0
      ;;
    *)
      if [[ "$1" == -* ]]; then
        echo "ERROR: Unknown flag: $1" >&2
        exit 2
      fi
      ROOT="$1"
      shift
      ;;
  esac
done

ROOT="${ROOT%/}"

if [[ "$ARCHIVE" -eq 1 ]]; then
  ts="$(date +%Y-%m-%d_%H-%M-%S)"
  ext="txt"
  [[ "$MODE" == "--json" ]] && ext="json"
  mkdir -p "$ROOT/docs/archive"
  OUT_PATH="$ROOT/docs/archive/ARCH_SCAN_${ts}.${ext}"
fi

PY_SCAN="$(cat <<'PY'
import ast
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(sys.argv[1]).resolve()
MODE = (sys.argv[2] if len(sys.argv) > 2 else "--text").strip()
SUMMARY_ONLY = (sys.argv[3] if len(sys.argv) > 3 else "0").strip() == "1"

INCLUDE_TOP = ("bvillage", "tests", "tools")

EXCLUDE_DIRS = {
    ".venv", ".git", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".tox", "build", "dist", ".eggs", "bvillage.egg-info", "bvillage_project.egg-info",
}
EXCLUDE_SUFFIXES = {".pyc"}

def relpath(p: Path) -> str:
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except Exception:
        return p.as_posix()

def detect_layer(rp: str) -> str:
    if rp.startswith("bvillage/core/"):
        return "core"
    if rp.startswith("bvillage/domains/") and "/blender/" in rp:
        return "domain-blender"
    if rp.startswith("bvillage/domains/") and "/core/" in rp:
        return "domain-core"
    if rp.startswith("bvillage/blender/"):
        return "blender"
    if rp.startswith("bvillage/types/"):
        return "type"
    if rp.startswith("tests/"):
        return "tests"
    if rp.startswith("tools/"):
        return "tools"
    if rp.startswith("bvillage/"):
        return "package"
    return "other"

def should_skip(p: Path) -> bool:
    if p.suffix in EXCLUDE_SUFFIXES:
        return True
    if any(part in EXCLUDE_DIRS for part in p.parts):
        return True
    return False

def first_line(text: str) -> str:
    return text.splitlines()[0] if text else ""

def second_line(text: str) -> str:
    lines = text.splitlines()
    return lines[1] if len(lines) > 1 else ""

def header_expected(rp: str) -> str:
    return f"# {rp}"

def check_header(rp: str, text: str) -> Optional[str]:
    exp = header_expected(rp)
    fl = first_line(text).rstrip("\n")
    if fl.startswith("#!"):
        sl = second_line(text).rstrip("\n")
        if sl.strip() != exp:
            return f"Header mismatch (shebang present). Expected line2: {exp!r}, got: {sl!r}"
        return None
    if fl.strip() != exp:
        return f"First line header mismatch. Expected: {exp!r}, got: {fl!r}"
    return None

def module_docstring(tree: ast.AST) -> Optional[str]:
    try:
        return ast.get_docstring(tree)
    except Exception:
        return None

def parse_imports(tree: ast.AST) -> List[str]:
    out: List[str] = []
    for node in getattr(tree, "body", []):
        if isinstance(node, ast.Import):
            for n in node.names:
                out.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for n in node.names:
                if n.name == "*":
                    out.append(f"{mod}.*".strip("."))
                else:
                    out.append(f"{mod}.{n.name}".strip("."))
    return out

def is_dataclass_decorated(node: ast.ClassDef) -> bool:
    for d in node.decorator_list:
        if isinstance(d, ast.Name) and d.id == "dataclass":
            return True
        if isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id == "dataclass":
            return True
        if isinstance(d, ast.Attribute) and d.attr == "dataclass":
            return True
        if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr == "dataclass":
            return True
    return False

def class_methods(node: ast.ClassDef) -> List[str]:
    ms: List[str] = []
    for n in node.body:
        if isinstance(n, ast.FunctionDef):
            args = [a.arg for a in n.args.args]
            ms.append(f"def {n.name}({', '.join(args)})")
        elif isinstance(n, ast.AsyncFunctionDef):
            args = [a.arg for a in n.args.args]
            ms.append(f"async def {n.name}({', '.join(args)})")
    return ms

def top_defs(tree: ast.AST) -> Tuple[List[str], List[Dict[str, Any]]]:
    funcs: List[str] = []
    classes: List[Dict[str, Any]] = []
    for node in getattr(tree, "body", []):
        if isinstance(node, ast.FunctionDef):
            args = [a.arg for a in node.args.args]
            funcs.append(f"def {node.name}({', '.join(args)})")
        elif isinstance(node, ast.AsyncFunctionDef):
            args = [a.arg for a in node.args.args]
            funcs.append(f"async def {node.name}({', '.join(args)})")
        elif isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "is_dataclass": is_dataclass_decorated(node),
                "methods": class_methods(node),
            })
    return funcs, classes

def find_calls(tree: ast.AST, names: Tuple[str, ...]) -> Dict[str, int]:
    counts = {n: 0 for n in names}
    class V(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call):
            fn = node.func
            if isinstance(fn, ast.Name) and fn.id in counts:
                counts[fn.id] += 1
            elif isinstance(fn, ast.Attribute) and fn.attr in counts:
                counts[fn.attr] += 1
            self.generic_visit(node)
    V().visit(tree)
    return counts

def find_substrings(text: str, subs: List[str]) -> Dict[str, int]:
    return {s: text.count(s) for s in subs}

def check_layer_import_rules(layer: str, imports: List[str]) -> List[str]:
    issues: List[str] = []
    has_bpy = any(i == "bpy" or i.startswith("bpy.") for i in imports)
    has_bmesh = any(i == "bmesh" or i.startswith("bmesh.") for i in imports)
    if layer in ("core", "domain-core", "type") and (has_bpy or has_bmesh):
        issues.append("Forbidden Blender import in non-Blender layer (bpy/bmesh).")
    return issues

def check_print_statements(tree: ast.AST, layer: str) -> List[str]:
    issues: List[str] = []
    if layer in ("core", "domain-core", "domain-blender", "type"):
        class V(ast.NodeVisitor):
            found = 0
            def visit_Call(self, node: ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "print":
                    self.found += 1
                self.generic_visit(node)
        v = V(); v.visit(tree)
        if v.found:
            issues.append(f"print() used ({v.found}x). Prefer logging.")
    return issues

def check_notes_schema(text: str) -> List[str]:
    issues: List[str] = []
    if "notes[" in text and '"domains"' not in text and "'domains'" not in text:
        issues.append("Notes accessed but 'domains' schema not visible here (review).")
    return issues

def check_determinism_smells(text: str, layer: str) -> List[str]:
    issues: List[str] = []
    if layer != "tests":
        if "import random" in text or "random." in text:
            if "random.Random(" not in text and "Random(" not in text:
                issues.append("random used without local Random(seed) (review determinism).")
    return issues

def load_bvillage_version() -> Optional[str]:
    try:
        sys.path.insert(0, str(ROOT))
        import bvillage  # type: ignore
        return getattr(bvillage, "__version__", None)
    except Exception:
        return None

@dataclass
class FileReport:
    path: str
    layer: str
    header_ok: bool
    header_issue: Optional[str]
    docstring: str
    imports: List[str]
    funcs: List[str]
    classes: List[Dict[str, Any]]
    dataclasses: List[str]
    signals: Dict[str, Any]
    issues: List[str]

def scan_file(p: Path) -> FileReport:
    rp = relpath(p)
    layer = detect_layer(rp)
    text = p.read_text(encoding="utf-8", errors="ignore")

    header_issue = check_header(rp, text)
    header_ok = header_issue is None

    try:
        tree = ast.parse(text)
    except Exception as e:
        issues: List[str] = []
        if header_issue:
            issues.append(header_issue)
        issues.append("AST parse error.")
        return FileReport(
            path=rp, layer=layer,
            header_ok=header_ok, header_issue=header_issue,
            docstring="(parse error)", imports=[],
            funcs=[], classes=[], dataclasses=[],
            signals={"parse_error": str(e)}, issues=issues,
        )

    doc = (module_docstring(tree) or "(no module docstring)").strip()
    imps = parse_imports(tree)
    funcs, classes = top_defs(tree)
    dcs = [c["name"] for c in classes if c.get("is_dataclass")]

    calls = find_calls(tree, ("set_domain_artifact", "get_domain_artifact", "configure_logging"))
    substr = find_substrings(text, [
        "notes[", 'notes["domains"]', "notes['domains']",
        "structure.notes",
        "axis_x", "axis_y", "axes_u", "axes_z",
        "frameplan",
        "logging.getLogger",
    ])

    issues: List[str] = []
    if header_issue:
        issues.append(header_issue)
    issues.extend(check_layer_import_rules(layer, imps))
    issues.extend(check_print_statements(tree, layer))
    issues.extend(check_determinism_smells(text, layer))
    issues.extend(check_notes_schema(text))

    signals = {"calls": calls, "substr": {k: v for k, v in substr.items() if v}}

    return FileReport(
        path=rp,
        layer=layer,
        header_ok=header_ok,
        header_issue=header_issue,
        docstring=doc,
        imports=imps,
        funcs=funcs,
        classes=classes,
        dataclasses=dcs,
        signals=signals,
        issues=issues,
    )

def scan_repo() -> List[FileReport]:
    reports: List[FileReport] = []
    for top in INCLUDE_TOP:
        base = ROOT / top
        if not base.exists():
            continue
        for p in base.rglob("*.py"):
            if should_skip(p):
                continue
            reports.append(scan_file(p))
    reports.sort(key=lambda r: r.path)
    return reports

def render_text(reports: List[FileReport], meta: Dict[str, Any]) -> str:
    total = len(reports)
    bad_headers = [r for r in reports if not r.header_ok]
    files_with_issues = [r for r in reports if r.issues]

    layer_counts: Dict[str, int] = {}
    for r in reports:
        layer_counts[r.layer] = layer_counts.get(r.layer, 0) + 1

    lines: List[str] = []
    lines.append("BVILLAGE – ARCHITECTURE SCAN")
    lines.append(f"Generated: {meta['generated']}")
    lines.append(f"Root: {meta['root']}")
    lines.append(f"Python: {meta['python']}")
    if meta.get("bvillage_version"):
        lines.append(f"bvillage.__version__: {meta['bvillage_version']}")
    lines.append("")
    lines.append(f"FILES: {total}")
    lines.append("LAYER COUNTS:")
    for k in sorted(layer_counts):
        lines.append(f"  - {k}: {layer_counts[k]}")
    lines.append("")
    lines.append("SUMMARY")
    lines.append(f"- Header mismatches: {len(bad_headers)}")
    lines.append(f"- Files with issues: {len(files_with_issues)}")
    lines.append("")

    if bad_headers:
        lines.append("HEADER MISMATCHES (header '# <repo path>' on line 1; if shebang then on line 2)")
        for r in bad_headers:
            lines.append(f"- {r.path}: {r.header_issue}")
        lines.append("")

    def is_hard(issue: str) -> bool:
        hard_keys = [
            "Forbidden Blender import",
            "AST parse error",
        ]
        return any(k in issue for k in hard_keys)

    hard: List[Tuple[str, str]] = []
    soft: List[Tuple[str, str]] = []
    for r in reports:
        for iss in r.issues:
            (hard if is_hard(iss) else soft).append((r.path, iss))

    if hard:
        lines.append("HARD ISSUES (must fix)")
        for path, iss in hard:
            lines.append(f"- {path}: {iss}")
        lines.append("")

    if soft:
        lines.append("SOFT / REVIEW ISSUES")
        for path, iss in soft:
            lines.append(f"- {path}: {iss}")
        lines.append("")

    if SUMMARY_ONLY:
        return "\n".join(lines)

    # ---- full per-file overview (what you missed) ----
    lines.append("FILE OVERVIEW")
    for r in reports:
        lines.append("============================================================")
        lines.append(f"FILE: {r.path}")
        lines.append(f"LAYER: {r.layer}")
        lines.append(f"HEADER: {'OK' if r.header_ok else 'FAIL'}")
        lines.append("DOCSTRING:")
        lines.append(r.docstring)
        lines.append("")
        lines.append("IMPORTS:")
        if r.imports:
            for i in r.imports:
                lines.append(f"  - {i}")
        else:
            lines.append("  (none)")
        lines.append("")
        lines.append("TOP-LEVEL:")
        if r.funcs:
            for f in r.funcs:
                lines.append(f"  - {f}")
        if r.classes:
            for c in r.classes:
                dc = " @dataclass" if c.get("is_dataclass") else ""
                lines.append(f"  - class {c['name']}{dc}")
                for m in c.get("methods", []):
                    lines.append(f"      * {m}")
        if not r.funcs and not r.classes:
            lines.append("  (none)")
        lines.append("")
        lines.append("SIGNALS:")
        calls = r.signals.get("calls", {})
        substr = r.signals.get("substr", {})
        lines.append(f"  calls: {calls}")
        lines.append(f"  substr: {substr}")
        lines.append("")
        if r.issues:
            lines.append("ISSUES:")
            for iss in r.issues:
                lines.append(f"  - {iss}")
            lines.append("")
    return "\n".join(lines)

def render_json(reports: List[FileReport], meta: Dict[str, Any]) -> str:
    def to_dict(r: FileReport) -> Dict[str, Any]:
        return {
            "path": r.path,
            "layer": r.layer,
            "header_ok": r.header_ok,
            "header_issue": r.header_issue,
            "docstring": r.docstring,
            "imports": r.imports,
            "funcs": r.funcs,
            "classes": r.classes,
            "dataclasses": r.dataclasses,
            "signals": r.signals,
            "issues": r.issues,
        }
    payload = {"meta": meta, "files": [to_dict(r) for r in reports]}
    return json.dumps(payload, indent=2, ensure_ascii=False)

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    meta = {
        "generated": now,
        "root": str(ROOT),
        "python": sys.version.split()[0],
        "bvillage_version": load_bvillage_version(),
    }
    reports = scan_repo()
    if MODE == "--json":
        print(render_json(reports, meta))
    else:
        print(render_text(reports, meta))

if __name__ == "__main__":
    main()
PY
)"

if [[ -n "$OUT_PATH" ]]; then
  python3 - "$ROOT" "$MODE" "$SUMMARY_ONLY" <<<"$PY_SCAN" > "$OUT_PATH"
  echo "Wrote: $OUT_PATH" >&2
else
  python3 - "$ROOT" "$MODE" "$SUMMARY_ONLY" <<<"$PY_SCAN"
fi
