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
# Default output:
# - text -> tmp/ARCH_SCAN.txt
# - json -> tmp/ARCH_SCAN.json
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
      sed -n '1,100p' "$0"
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
else
  if [[ -z "$OUT_PATH" ]]; then
    if [[ "$MODE" == "--json" ]]; then
      OUT_PATH="$ROOT/tmp/ARCH_SCAN.json"
    else
      OUT_PATH="$ROOT/tmp/ARCH_SCAN.txt"
    fi
  fi
  mkdir -p "$(dirname "$OUT_PATH")"
fi

PY_FILE="$(mktemp)"
cleanup() {
  rm -f "$PY_FILE"
}
trap cleanup EXIT

cat > "$PY_FILE" <<'PYEOF'
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
ROOT_ENTRY_FILES = ("run_in_blender.py",)

EXCLUDE_DIRS = {
    ".venv", ".git", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".tox", "build", "dist", ".eggs", "bvillage.egg-info", "bvillage_project.egg-info",
}
EXCLUDE_SUFFIXES = {".pyc"}

LEGACY_TYPING = {
    "typing.List", "typing.Dict", "typing.Tuple", "typing.Set",
    "typing.FrozenSet", "typing.Type", "typing.Optional", "typing.Union",
}
LEGACY_TYPING_MODERN = {
    "typing.List": "list[...]",
    "typing.Dict": "dict[...]",
    "typing.Tuple": "tuple[...]",
    "typing.Set": "set[...]",
    "typing.FrozenSet": "frozenset[...]",
    "typing.Type": "type[...]",
    "typing.Optional": "X | None",
    "typing.Union": "X | Y",
}


def relpath(p):
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except Exception:
        return p.as_posix()


def detect_layer(rp):
    if rp == "run_in_blender.py":
        return "entry"
    if rp.startswith("bvillage/core/"):
        return "core"
    if rp.startswith("bvillage/domains/") and "/contracts/" in rp:
        return "domain-contracts"
    if rp.startswith("bvillage/domains/") and "/validation/" in rp:
        return "domain-validation"
    if rp.startswith("bvillage/domains/") and "/blender/" in rp:
        return "domain-blender"
    if rp.startswith("bvillage/domains/") and "/core/" in rp:
        return "domain-core"
    if rp.startswith("bvillage/blender/"):
        return "blender"
    if rp.startswith("bvillage/types/") and "/contracts/" in rp:
        return "type-contracts"
    if rp.startswith("bvillage/types/"):
        return "type"
    if rp.startswith("tests/"):
        return "tests"
    if rp.startswith("tools/"):
        return "tools"
    if rp.startswith("bvillage/"):
        return "package"
    return "other"


def should_skip(p):
    if p.suffix in EXCLUDE_SUFFIXES:
        return True
    if any(part in EXCLUDE_DIRS for part in p.parts):
        return True
    return False


def first_line(text):
    return text.splitlines()[0] if text else ""


def second_line(text):
    lines = text.splitlines()
    return lines[1] if len(lines) > 1 else ""


def header_expected(rp):
    return f"# {rp}"


def check_header(rp, text):
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


def _ann(node):
    if node is None:
        return ""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_ann(node.value)}.{node.attr}"
    if isinstance(node, ast.Subscript):
        return f"{_ann(node.value)}[{_ann(node.slice)}]"
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return f"{_ann(node.left)} | {_ann(node.right)}"
    if isinstance(node, ast.Tuple):
        return ", ".join(_ann(e) for e in node.elts)
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if hasattr(ast, "Index") and isinstance(node, ast.Index):
        return _ann(node.value)
    try:
        return ast.unparse(node)
    except Exception:
        return "?"


def _arg(a):
    if a.annotation:
        return f"{a.arg}: {_ann(a.annotation)}"
    return a.arg


def _func_sig(node):
    args = node.args
    parts = []

    for a in args.posonlyargs:
        parts.append(_arg(a))
    if args.posonlyargs:
        parts.append("/")

    n = len(args.args)
    nd = len(args.defaults)
    offset = n - nd
    for i, a in enumerate(args.args):
        s = _arg(a)
        di = i - offset
        if di >= 0:
            try:
                s += f"={ast.unparse(args.defaults[di])}"
            except Exception:
                s += "=..."
        parts.append(s)

    if args.vararg:
        parts.append(f"*{_arg(args.vararg)}")
    elif args.kwonlyargs:
        parts.append("*")

    for i, a in enumerate(args.kwonlyargs):
        s = _arg(a)
        if args.kw_defaults[i] is not None:
            try:
                s += f"={ast.unparse(args.kw_defaults[i])}"
            except Exception:
                s += "=..."
        parts.append(s)

    if args.kwarg:
        parts.append(f"**{_arg(args.kwarg)}")

    sig = f"({', '.join(parts)})"
    ret = f" -> {_ann(node.returns)}" if node.returns else ""
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    return f"{prefix} {node.name}{sig}{ret}"


def _dc_fields(node):
    fields = []
    for item in node.body:
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            name = item.target.id
            typ = _ann(item.annotation) if item.annotation else "?"
            if item.value is not None:
                try:
                    default = ast.unparse(item.value)
                except Exception:
                    default = "..."
                fields.append(f"{name}: {typ} = {default}")
            else:
                fields.append(f"{name}: {typ}")
    return fields


def _dc_decorator_args(node):
    for d in node.decorator_list:
        if isinstance(d, ast.Call):
            func = d.func
            is_dc = (
                (isinstance(func, ast.Name) and func.id == "dataclass") or
                (isinstance(func, ast.Attribute) and func.attr == "dataclass")
            )
            if is_dc:
                try:
                    s = ast.unparse(d)
                    idx = s.find("(")
                    return s[idx:] if idx >= 0 else ""
                except Exception:
                    return "(...)"
    return ""


def is_dataclass_decorated(node):
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


def module_docstring(tree):
    try:
        return ast.get_docstring(tree)
    except Exception:
        return None


def parse_imports(tree):
    out = []
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


def top_defs(tree):
    funcs = []
    classes = []
    for node in getattr(tree, "body", []):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append(_func_sig(node))
        elif isinstance(node, ast.ClassDef):
            is_dc = is_dataclass_decorated(node)
            entry = {
                "name": node.name,
                "is_dataclass": is_dc,
                "decorator_args": _dc_decorator_args(node) if is_dc else "",
                "fields": _dc_fields(node) if is_dc else [],
                "methods": [_func_sig(m) for m in node.body
                            if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))],
            }
            classes.append(entry)
    return funcs, classes


def find_calls(tree, names):
    counts = {n: 0 for n in names}
    class V(ast.NodeVisitor):
        def visit_Call(self, node):
            fn = node.func
            if isinstance(fn, ast.Name) and fn.id in counts:
                counts[fn.id] += 1
            elif isinstance(fn, ast.Attribute) and fn.attr in counts:
                counts[fn.attr] += 1
            self.generic_visit(node)
    V().visit(tree)
    return counts


def find_substrings(text, subs):
    return {s: text.count(s) for s in subs}


def check_layer_import_rules(layer, imports):
    issues = []
    has_bpy = any(i == "bpy" or i.startswith("bpy.") for i in imports)
    has_bmesh = any(i == "bmesh" or i.startswith("bmesh.") for i in imports)
    if layer in ("core", "domain-core", "type", "domain-contracts", "type-contracts", "domain-validation") and (has_bpy or has_bmesh):
        issues.append("Forbidden Blender import in non-Blender layer (bpy/bmesh).")
    return issues


def check_print_statements(tree, layer):
    issues = []
    if layer in ("core", "domain-core", "domain-blender", "type", "domain-contracts", "type-contracts", "domain-validation"):
        class V(ast.NodeVisitor):
            found = 0
            def visit_Call(self, node):
                if isinstance(node.func, ast.Name) and node.func.id == "print":
                    self.found += 1
                self.generic_visit(node)
        v = V()
        v.visit(tree)
        if v.found:
            issues.append(f"print() used ({v.found}x). Prefer logging.")
    return issues


def check_notes_schema(text):
    issues = []
    if "notes[" in text and '"domains"' not in text and "'domains'" not in text:
        issues.append("Notes accessed but 'domains' schema not visible here (review).")
    return issues


def check_determinism_smells(text, layer):
    issues = []
    if layer != "tests":
        if "import random" in text or "random." in text:
            if "random.Random(" not in text and "Random(" not in text:
                issues.append("random used without local Random(seed) (review determinism).")
    return issues


def check_legacy_typing(imports, layer):
    if layer == "tools":
        return []
    found = [i for i in imports if i in LEGACY_TYPING]
    if not found:
        return []
    suggestions = ", ".join(f"{f} -> {LEGACY_TYPING_MODERN.get(f, 'builtin')}" for f in found)
    return [f"Legacy typing aliases (use builtins): {suggestions}"]


def check_dataclass_flags(tree, layer):
    issues = []
    if layer not in ("core", "domain-core", "type"):
        return issues
    for node in getattr(tree, "body", []):
        if not isinstance(node, ast.ClassDef) or not is_dataclass_decorated(node):
            continue
        dec = _dc_decorator_args(node)
        missing = []
        if "frozen=True" not in dec:
            missing.append("frozen=True")
        if "slots=True" not in dec:
            missing.append("slots=True")
        if missing:
            issues.append(
                f"Dataclass '{node.name}' missing {', '.join(missing)} "
                f"(required in {layer} layer)."
            )
    return issues


def check_logger_name(tree, text, layer=""):
    if layer == "tests":
        return []
    if "logging.getLogger" not in text:
        return []

    CONFIG_METHODS = {"setLevel", "addHandler", "removeHandler", "setFormatter"}

    class V(ast.NodeVisitor):
        getlogger_vars = []
        configured_vars = set()

        def visit_Assign(self, node):
            if (len(node.targets) == 1 and
                    isinstance(node.targets[0], ast.Name) and
                    isinstance(node.value, ast.Call)):
                call = node.value
                fn = call.func
                is_gl = (
                    (isinstance(fn, ast.Attribute) and fn.attr == "getLogger") or
                    (isinstance(fn, ast.Name) and fn.id == "getLogger")
                )
                if is_gl and call.args:
                    arg = call.args[0]
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        self.getlogger_vars.append((arg.value, node.targets[0].id))
            self.generic_visit(node)

        def visit_Call(self, node):
            fn = node.func
            if isinstance(fn, ast.Attribute) and fn.attr in CONFIG_METHODS:
                if isinstance(fn.value, ast.Name):
                    self.configured_vars.add(fn.value.id)
            self.generic_visit(node)

    v = V()
    v.visit(tree)

    offenders = [
        repr(name)
        for name, var in v.getlogger_vars
        if var not in v.configured_vars
    ]
    if offenders:
        return [f"Hardcoded logger name(s): {', '.join(offenders)}. Use logging.getLogger(__name__)."]
    return []


def check_fstring_in_log(tree):
    LOG_METHODS = {"debug", "info", "warning", "error", "critical", "exception"}
    class V(ast.NodeVisitor):
        count = 0
        def visit_Call(self, node):
            fn = node.func
            if isinstance(fn, ast.Attribute) and fn.attr in LOG_METHODS:
                if node.args and isinstance(node.args[0], ast.JoinedStr):
                    self.count += 1
            self.generic_visit(node)
    v = V()
    v.visit(tree)
    if v.count:
        return [
            f"f-string in log call ({v.count}x). "
            f"Use log.debug('msg %s', value) to avoid eager string construction."
        ]
    return []


def check_all_defined(tree, layer, funcs):
    if layer in ("tools", "tests", "package", "entry"):
        return []
    public = [f for f in funcs if not f.startswith("def _") and not f.startswith("async def _")]
    if not public:
        return []
    has_all = any(
        isinstance(node, ast.Assign) and
        any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets)
        for node in getattr(tree, "body", [])
    )
    if not has_all:
        return ["__all__ not defined. Declare public API explicitly."]
    return []


def load_bvillage_version():
    try:
        sys.path.insert(0, str(ROOT))
        import bvillage
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


def scan_file(p):
    rp = relpath(p)
    layer = detect_layer(rp)
    text = p.read_text(encoding="utf-8", errors="ignore")

    header_issue = check_header(rp, text)
    header_ok = header_issue is None

    try:
        tree = ast.parse(text)
    except Exception as e:
        issues = []
        if header_issue:
            issues.append(header_issue)
        issues.append("AST parse error.")
        return FileReport(
            path=rp,
            layer=layer,
            header_ok=header_ok,
            header_issue=header_issue,
            docstring="(parse error)",
            imports=[],
            funcs=[],
            classes=[],
            dataclasses=[],
            signals={"parse_error": str(e)},
            issues=issues,
        )

    doc = (module_docstring(tree) or "(no module docstring)").strip()
    imps = parse_imports(tree)
    funcs, classes = top_defs(tree)
    dcs = [c["name"] for c in classes if c.get("is_dataclass")]

    calls = find_calls(tree, ("set_domain_artifact", "get_domain_artifact", "configure_logging"))
    substr = find_substrings(text, [
        "notes[",
        'notes["domains"]',
        "notes['domains']",
        "structure.notes",
        "axes_u",
        "axes_v",
        "axes_z",
        "frameplan",
        "logging.getLogger",
    ])

    issues = []
    if header_issue:
        issues.append(header_issue)
    issues.extend(check_layer_import_rules(layer, imps))
    issues.extend(check_print_statements(tree, layer))
    issues.extend(check_determinism_smells(text, layer))
    issues.extend(check_notes_schema(text))
    issues.extend(check_legacy_typing(imps, layer))
    issues.extend(check_dataclass_flags(tree, layer))
    issues.extend(check_logger_name(tree, text, layer))
    issues.extend(check_fstring_in_log(tree))
    issues.extend(check_all_defined(tree, layer, funcs))

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


def iter_repo_files():
    seen = set()

    for entry_name in ROOT_ENTRY_FILES:
        p = ROOT / entry_name
        if p.exists() and p.suffix == ".py" and not should_skip(p):
            rp = relpath(p)
            if rp not in seen:
                seen.add(rp)
                yield p

    for top in INCLUDE_TOP:
        base = ROOT / top
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.py"), key=lambda x: x.as_posix()):
            if should_skip(p):
                continue
            rp = relpath(p)
            if rp in seen:
                continue
            seen.add(rp)
            yield p


def scan_repo():
    reports = [scan_file(p) for p in iter_repo_files()]
    reports.sort(key=lambda r: r.path)
    return reports


def render_text(reports, meta):
    total = len(reports)
    bad_headers = [r for r in reports if not r.header_ok]
    files_with_issues = [r for r in reports if r.issues]

    layer_counts = {}
    for r in reports:
        layer_counts[r.layer] = layer_counts.get(r.layer, 0) + 1

    lines = []
    lines.append("BVILLAGE - ARCHITECTURE SCAN")
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
        lines.append("HEADER MISMATCHES")
        for r in bad_headers:
            lines.append(f"- {r.path}: {r.header_issue}")
        lines.append("")

    def is_hard(issue):
        return any(k in issue for k in ["Forbidden Blender import", "AST parse error"])

    hard = []
    soft = []
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

    lines.append("FILE OVERVIEW")
    for r in reports:
        lines.append("=" * 60)
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
                dc_tag = " @dataclass" if c.get("is_dataclass") else ""
                dec_args = c.get("decorator_args", "")
                lines.append(f"  - class {c['name']}{dc_tag}{dec_args}")
                for field in c.get("fields", []):
                    lines.append(f"      field  {field}")
                for m in c.get("methods", []):
                    lines.append(f"      method {m}")
        if not r.funcs and not r.classes:
            lines.append("  (none)")
        lines.append("")
        lines.append("SIGNALS:")
        lines.append(f"  calls: {r.signals.get('calls', {})}")
        lines.append(f"  substr: {r.signals.get('substr', {})}")
        lines.append("")
        if r.issues:
            lines.append("ISSUES:")
            for iss in r.issues:
                lines.append(f"  - {iss}")
            lines.append("")
    return "\n".join(lines)


def render_json(reports, meta):
    def to_dict(r):
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
PYEOF

if [[ -n "$OUT_PATH" ]]; then
  python3 "$PY_FILE" "$ROOT" "$MODE" "$SUMMARY_ONLY" > "$OUT_PATH"
  echo "Wrote: $OUT_PATH" >&2
else
  python3 "$PY_FILE" "$ROOT" "$MODE" "$SUMMARY_ONLY"
fi
