#!/usr/bin/env python3
# tools/import_graph.py

"""
BVILLAGE Import Graph Scanner

Purpose
-------
Extract the import dependency graph of the productive BVILLAGE codebase.

This tool analyzes Python modules and extracts:

- internal module dependencies
- external imports
- module inventory
- dependency edges
- dependency cycles
- layer classification

Output
------
generated/IMPORT_GRAPH.md

Scope
-----
- bvillage package
- selected entry files (e.g. run_in_blender.py)

Excludes
--------
- caches
- build artifacts
- tests
- virtual environments
"""

from __future__ import annotations

import ast
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

PROJECT_ROOT = Path(".").resolve()

CODE_ROOT = PROJECT_ROOT / "bvillage"

OUT = PROJECT_ROOT / "generated" / "IMPORT_GRAPH.md"

EXTRA_FILES = [
    PROJECT_ROOT / "run_in_blender.py",
]

INCLUDE_PATTERNS = [
    "bvillage/**/*.py",
]

EXCLUDE_PATTERNS = [
    "**/__pycache__/**",
    "**/*.pyc",
    "**/.venv/**",
    "**/venv/**",
    "**/env/**",
    "**/generated/**",
    "**/build/**",
    "**/dist/**",
    "**/tests/**",
    "**/tmp/**",
]


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def relpath(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def module_name(path: Path) -> str:
    rel = path.relative_to(PROJECT_ROOT)

    if rel.name == "run_in_blender.py":
        return "run_in_blender"

    parts = list(rel.with_suffix("").parts)
    return ".".join(parts)


def layer_of_module(mod: str) -> str:

    if mod == "run_in_blender":
        return "entry"

    if mod.startswith("bvillage.core"):
        return "core"

    if mod.startswith("bvillage.types"):
        return "types"

    if mod.startswith("bvillage.domains"):

        if ".blender." in mod:
            return "domain-blender"

        if ".validation." in mod:
            return "domain-validation"

        if ".contracts." in mod:
            return "domain-contracts"

        return "domain-core"

    if mod.startswith("bvillage.blender"):
        return "blender"

    if mod.startswith("bvillage.tools"):
        return "tools"

    return "other"


def collect_files() -> List[Path]:

    files: Set[Path] = set()

    for pattern in INCLUDE_PATTERNS:
        for path in PROJECT_ROOT.glob(pattern):
            if path.is_file():
                files.add(path.resolve())

    for p in EXTRA_FILES:
        if p.exists():
            files.add(p.resolve())

    result = []

    for f in files:
        r = f.relative_to(PROJECT_ROOT)
        if any(r.match(p) for p in EXCLUDE_PATTERNS):
            continue
        result.append(f)

    result.sort()
    return result


# ------------------------------------------------------------
# Import extraction
# ------------------------------------------------------------

def extract_imports(path: Path):

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    internal = set()
    external = set()

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for alias in node.names:

                name = alias.name

                if name.startswith("bvillage"):
                    internal.add(name)
                else:
                    external.add(name.split(".")[0])

        elif isinstance(node, ast.ImportFrom):

            mod = node.module or ""

            if mod.startswith("bvillage"):
                internal.add(mod)
            else:
                if mod:
                    external.add(mod.split(".")[0])

    return internal, external


# ------------------------------------------------------------
# Graph utilities
# ------------------------------------------------------------

def detect_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:

    visited = set()
    stack = []
    cycles = []

    def visit(node):

        if node in stack:

            idx = stack.index(node)
            cycles.append(stack[idx:] + [node])
            return

        if node in visited:
            return

        visited.add(node)
        stack.append(node)

        for dep in graph.get(node, []):
            visit(dep)

        stack.pop()

    for n in graph:
        visit(n)

    return cycles


# ------------------------------------------------------------
# Scan
# ------------------------------------------------------------

def build_graph(files: List[Path]):

    module_by_path = {}
    graph = defaultdict(set)
    external = defaultdict(set)

    for path in files:

        mod = module_name(path)
        module_by_path[path] = mod

    for path in files:

        mod = module_by_path[path]

        internal, ext = extract_imports(path)

        for dep in internal:

            graph[mod].add(dep)

        for e in ext:

            external[mod].add(e)

    return graph, external


# ------------------------------------------------------------
# Markdown
# ------------------------------------------------------------

def render(graph, external, files):

    modules = sorted(graph.keys())

    cycles = detect_cycles(graph)

    lines = []

    lines.append("# IMPORT GRAPH")
    lines.append("")

    lines.append("## Summary")
    lines.append("")

    lines.append(f"- modules: {len(modules)}")

    edges = sum(len(v) for v in graph.values())
    lines.append(f"- internal edges: {edges}")

    ext = sum(len(v) for v in external.values())
    lines.append(f"- external imports: {ext}")

    lines.append(f"- cycles: {len(cycles)}")

    lines.append("")

    lines.append("## Module Inventory")
    lines.append("")

    for m in modules:

        lines.append(f"### {m}")
        lines.append("")

        layer = layer_of_module(m)

        lines.append(f"- layer: `{layer}`")
        lines.append("")

        lines.append("internal imports:")

        deps = sorted(graph[m])

        if deps:
            for d in deps:
                lines.append(f"- {m} -> {d}")
        else:
            lines.append("- none")

        lines.append("")

        lines.append("external imports:")

        ex = sorted(external[m])

        if ex:
            for e in ex:
                lines.append(f"- {e}")
        else:
            lines.append("- none")

        lines.append("")

    lines.append("## Dependency Edges")
    lines.append("")

    for src in sorted(graph):

        for dst in sorted(graph[src]):

            lines.append(f"- {src} -> {dst}")

    lines.append("")

    lines.append("## Cycles")
    lines.append("")

    if cycles:

        for c in cycles:

            lines.append("- " + " -> ".join(c))

    else:

        lines.append("no cycles detected")

    lines.append("")

    return "\n".join(lines)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    files = collect_files()

    graph, external = build_graph(files)

    OUT.parent.mkdir(exist_ok=True)

    md = render(graph, external, files)

    OUT.write_text(md)

    print("Import graph written:", OUT)
    print("modules:", len(graph))


if __name__ == "__main__":
    main()
