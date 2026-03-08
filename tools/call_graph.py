#!/usr/bin/env python3
# tools/call_graph.py

import argparse
import ast
from pathlib import Path
from collections import defaultdict

ROOT = Path(".").resolve()

EXCLUDE = {
    ".git",
    "__pycache__",
    ".venv",
    ".pytest_cache",
    ".mypy_cache",
    "build",
    "dist",
}


# ----------------------------------------------------------
# CLI
# ----------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--with-tests", dest="with_tests", action="store_true", default=True)
    parser.add_argument("--no-tests", dest="with_tests", action="store_false")
    parser.add_argument("--outdir", default="tmp")
    parser.add_argument("--outfile", default="")
    return parser.parse_args()


def resolve_outfile(root, outdir, outfile):
    if outfile:
        path = Path(outfile)
        if not path.is_absolute():
            path = root / path
        return path
    return root / outdir / "CALL_GRAPH.txt"


# ----------------------------------------------------------
# Scanbereich
# ----------------------------------------------------------

def discover_files(root, include_tests=True):

    files = []

    entry = root / "run_in_blender.py"
    if entry.exists():
        files.append(entry)

    engine = root / "bvillage"
    if engine.exists():
        for p in engine.rglob("*.py"):
            if any(part in EXCLUDE for part in p.parts):
                continue
            files.append(p)

    if include_tests:
        tests = root / "tests"
        if tests.exists():
            for p in tests.rglob("*.py"):
                if any(part in EXCLUDE for part in p.parts):
                    continue
                files.append(p)

    return sorted(files)


# ----------------------------------------------------------
# Modulname
# ----------------------------------------------------------

def module_name(root, path):

    rel = path.relative_to(root)

    if rel.name == "__init__.py":
        rel = rel.parent
    else:
        rel = rel.with_suffix("")

    return ".".join(rel.parts)


# ----------------------------------------------------------
# Call extractor
# ----------------------------------------------------------

class CallVisitor(ast.NodeVisitor):

    def __init__(self, module):
        self.module = module
        self.current_func = None
        self.calls = defaultdict(list)

    def visit_FunctionDef(self, node):
        prev = self.current_func
        self.current_func = f"{self.module}.{node.name}"
        self.generic_visit(node)
        self.current_func = prev

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_Call(self, node):

        if self.current_func is None:
            return

        name = None

        if isinstance(node.func, ast.Name):
            name = node.func.id

        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr

        if name:
            self.calls[self.current_func].append(name)

        self.generic_visit(node)


# ----------------------------------------------------------
# Analyse
# ----------------------------------------------------------

def analyze(files):

    call_out = defaultdict(list)
    call_in = defaultdict(list)

    for file in files:

        mod = module_name(ROOT, file)

        try:
            tree = ast.parse(file.read_text(encoding="utf-8"))
        except Exception:
            continue

        visitor = CallVisitor(mod)
        visitor.visit(tree)

        for src, targets in visitor.calls.items():
            for tgt in targets:

                call_out[src].append(tgt)
                call_in[tgt].append(src)

    return call_out, call_in


# ----------------------------------------------------------
# Ausgabe
# ----------------------------------------------------------

def build_output(call_out, call_in):

    lines = []

    lines.append("BVILLAGE CALL GRAPH\n")

    funcs = sorted(set(call_out.keys()) | set(call_in.keys()))

    for f in funcs:

        lines.append("=" * 60)
        lines.append(f"FUNCTION: {f}\n")

        lines.append("CALLS")

        outs = sorted(set(call_out.get(f, [])))

        if not outs:
            lines.append("  (none)")
        else:
            for o in outs:
                lines.append(f"  - {o}")

        lines.append("\nCALLED BY")

        ins = sorted(set(call_in.get(f, [])))

        if not ins:
            lines.append("  (none)")
        else:
            for i in ins:
                lines.append(f"  - {i}")

        lines.append("")

    return "\n".join(lines)


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

def main():

    args = parse_args()

    files = discover_files(ROOT, args.with_tests)

    call_out, call_in = analyze(files)

    text = build_output(call_out, call_in)

    outfile = resolve_outfile(ROOT, args.outdir, args.outfile)

    outfile.parent.mkdir(parents=True, exist_ok=True)

    outfile.write_text(text, encoding="utf-8")

    print(f"Call graph written to {outfile}")


if __name__ == "__main__":
    main()
