#!/usr/bin/env python3
# tools/import_graph.py

"""
BVILLAGE Import Graph Generator

Erzeugt einen statischen Importgraphen des Engine-Codes und schreibt ihn
in eine TXT-Datei.

Default scan scope:
- run_in_blender.py
- bvillage/
- tests/   (abschaltbar)

Explizit ausgeschlossen:
- research/
- docs/
- .venv/
- build/
- dist/
- sonstige Nicht-Engine-Bereiche

Default output:
    tmp/IMPORT_GRAPH.txt
"""

from __future__ import annotations

import argparse
import ast
from collections import defaultdict
from pathlib import Path


ROOT = Path(".").resolve()

EXCLUDE = {
    ".git",
    "__pycache__",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    "build",
    "dist",
    ".eggs",
    "bvillage.egg-info",
    "bvillage_project.egg-info",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate static import graph for BVILLAGE engine code.")
    parser.add_argument(
        "--with-tests",
        dest="with_tests",
        action="store_true",
        default=True,
        help="Include tests/ in scan scope (default: on).",
    )
    parser.add_argument(
        "--no-tests",
        dest="with_tests",
        action="store_false",
        help="Exclude tests/ from scan scope.",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="generated",
        help="Output directory for IMPORT_GRAPH.txt (default: tmp). Ignored if --outfile is set.",
    )
    parser.add_argument(
        "--outfile",
        type=str,
        default="",
        help="Explicit output file path.",
    )
    return parser.parse_args()


def resolve_outfile(root: Path, outdir: str, outfile: str) -> Path:
    if outfile:
        out = Path(outfile)
        if not out.is_absolute():
            out = root / out
        return out
    return root / outdir / "IMPORT_GRAPH.txt"


def discover_python_files(root: Path, include_tests: bool = True) -> list[Path]:
    files: list[Path] = []

    root_entry = root / "run_in_blender.py"
    if root_entry.exists():
        files.append(root_entry)

    engine_dir = root / "bvillage"
    if engine_dir.exists():
        for path in engine_dir.rglob("*.py"):
            if any(part in EXCLUDE for part in path.parts):
                continue
            files.append(path)

    if include_tests:
        tests_dir = root / "tests"
        if tests_dir.exists():
            for path in tests_dir.rglob("*.py"):
                if any(part in EXCLUDE for part in path.parts):
                    continue
                files.append(path)

    return sorted(set(files), key=lambda p: p.as_posix())


def module_name(root: Path, file: Path) -> str:
    rel = file.relative_to(root)

    if rel.name == "__init__.py":
        rel = rel.parent
    else:
        rel = rel.with_suffix("")

    return ".".join(rel.parts)


def module_package_name(module: str) -> str:
    if "." not in module:
        return ""
    return module.rsplit(".", 1)[0]


def resolve_from_import_base(current_module: str, is_package: bool, level: int, module: str | None) -> str:
    if level == 0:
        return module or ""

    base_parts = current_module.split(".")
    if not is_package and base_parts:
        base_parts = base_parts[:-1]

    up = level - 1
    if up > 0:
        if up > len(base_parts):
            return ""
        base_parts = base_parts[:-up]

    if module:
        base_parts.extend(part for part in module.split(".") if part)

    return ".".join(base_parts)


def parse_imports(file: Path, current_module: str, is_package: bool) -> list[tuple[str, int, str]]:
    imports: list[tuple[str, int, str]] = []

    try:
        text = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = file.read_text(encoding="utf-8", errors="replace")

    try:
        tree = ast.parse(text, filename=str(file))
    except SyntaxError:
        return imports

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((alias.name, node.lineno, "import"))

        elif isinstance(node, ast.ImportFrom):
            base = resolve_from_import_base(
                current_module=current_module,
                is_package=is_package,
                level=node.level,
                module=node.module,
            )

            if any(alias.name == "*" for alias in node.names):
                if base:
                    imports.append((base, node.lineno, "from-import-*"))
                continue

            if base:
                imports.append((base, node.lineno, "from-import-base"))

            for alias in node.names:
                if base:
                    imports.append((f"{base}.{alias.name}", node.lineno, "from-import-name"))
                else:
                    imports.append((alias.name, node.lineno, "from-import-name"))

    return imports


def detect_layer(path: str) -> str:
    path = path.replace("\\", "/")

    if path == "run_in_blender.py":
        return "entry"

    if path.startswith("bvillage/core/"):
        return "core"

    if path.startswith("bvillage/domains/") and "/contracts/" in path:
        return "domain-contracts"

    if path.startswith("bvillage/domains/") and "/validation/" in path:
        return "domain-validation"

    if path.startswith("bvillage/domains/") and "/core/" in path:
        return "domain-core"

    if path.startswith("bvillage/domains/") and "/blender/" in path:
        return "domain-blender"

    if path.startswith("bvillage/types/") and "/contracts/" in path:
        return "type-contracts"

    if path.startswith("bvillage/types/"):
        return "type"

    if path.startswith("bvillage/blender/"):
        return "blender"

    if path.startswith("tests/"):
        return "tests"

    if path.startswith("tools/"):
        return "tools"

    if path.startswith("bvillage/"):
        return "package"

    return "other"


def resolve_internal_target(imp: str, modules: set[str]) -> str | None:
    if not imp:
        return None

    if imp in modules:
        return imp

    probe = imp
    while "." in probe:
        probe = probe.rsplit(".", 1)[0]
        if probe in modules:
            return probe

    return None


def find_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    visited: set[str] = set()
    stack: list[str] = []
    on_stack: set[str] = set()
    cycles: set[tuple[str, ...]] = set()

    def canonicalize(cycle: list[str]) -> tuple[str, ...]:
        core = cycle[:-1]
        if not core:
            return tuple()

        rotations = []
        for i in range(len(core)):
            rotated = core[i:] + core[:i]
            rotations.append(tuple(rotated))

        return min(rotations)

    def dfs(node: str) -> None:
        visited.add(node)
        stack.append(node)
        on_stack.add(node)

        for neigh in graph.get(node, []):
            if neigh not in visited:
                dfs(neigh)
            elif neigh in on_stack:
                i = stack.index(neigh)
                cycle = stack[i:] + [neigh]
                canon = canonicalize(cycle)
                if canon:
                    cycles.add(canon)

        stack.pop()
        on_stack.remove(node)

    for node in sorted(graph.keys()):
        if node not in visited:
            dfs(node)

    return [list(cycle) for cycle in sorted(cycles)]


def main() -> None:
    args = parse_args()

    files = discover_python_files(ROOT, include_tests=args.with_tests)
    outfile = resolve_outfile(ROOT, args.outdir, args.outfile)

    module_map: dict[str, Path] = {}
    package_modules: set[str] = set()

    for f in files:
        mod = module_name(ROOT, f)
        module_map[mod] = f
        if f.name == "__init__.py":
            package_modules.add(mod)

    modules = set(module_map.keys())

    imports_out: dict[str, list[str]] = defaultdict(list)
    imports_in: dict[str, list[str]] = defaultdict(list)
    import_details: dict[str, list[tuple[str, str, int, str]]] = defaultdict(list)
    unresolved_imports: dict[str, list[tuple[str, int, str]]] = defaultdict(list)
    external_imports: dict[str, list[tuple[str, int, str]]] = defaultdict(list)

    for mod, path in sorted(module_map.items()):
        parsed_imports = parse_imports(path, current_module=mod, is_package=(mod in package_modules))

        for raw_import, lineno, kind in parsed_imports:
            target = resolve_internal_target(raw_import, modules)

            if target is not None:
                imports_out[mod].append(target)
                imports_in[target].append(mod)
                import_details[mod].append((raw_import, target, lineno, kind))
            else:
                top = raw_import.split(".", 1)[0] if raw_import else ""
                if top in {"bvillage", "tests", "run_in_blender"}:
                    unresolved_imports[mod].append((raw_import, lineno, kind))
                else:
                    external_imports[mod].append((raw_import, lineno, kind))

    graph: dict[str, list[str]] = {}
    for mod in modules:
        graph[mod] = sorted(set(imports_out.get(mod, [])))

    cycles = find_cycles(graph)

    lines: list[str] = []
    lines.append("BVILLAGE IMPORT GRAPH")
    lines.append("")
    lines.append(f"root: {ROOT}")
    lines.append(f"modules: {len(modules)}")
    lines.append(f"include_tests: {args.with_tests}")
    lines.append(f"outfile: {outfile}")
    lines.append("")

    for mod in sorted(modules):
        path = module_map[mod]
        rel = path.relative_to(ROOT)
        layer = detect_layer(str(rel))

        lines.append("=" * 60)
        lines.append(f"FILE: {rel}")
        lines.append(f"MODULE: {mod}")
        lines.append(f"LAYER: {layer}")
        lines.append("")

        lines.append("IMPORTS:")
        details = sorted(import_details.get(mod, []), key=lambda x: (x[2], x[0], x[1], x[3]))
        if not details:
            lines.append("  (none)")
        else:
            for raw, target, lineno, kind in details:
                lines.append(f"  - {target}    [raw={raw}, line={lineno}, kind={kind}]")

        lines.append("")
        lines.append("IMPORTED BY:")
        incoming = sorted(set(imports_in.get(mod, [])))
        if not incoming:
            lines.append("  (none)")
        else:
            for src in incoming:
                lines.append(f"  - {src}")

        lines.append("")
        lines.append("UNRESOLVED INTERNAL IMPORTS:")
        unresolved = sorted(set(unresolved_imports.get(mod, [])), key=lambda x: (x[1], x[0], x[2]))
        if not unresolved:
            lines.append("  (none)")
        else:
            for raw, lineno, kind in unresolved:
                lines.append(f"  - {raw}    [line={lineno}, kind={kind}]")

        lines.append("")
        lines.append("EXTERNAL IMPORTS:")
        external = sorted(set(external_imports.get(mod, [])), key=lambda x: (x[1], x[0], x[2]))
        if not external:
            lines.append("  (none)")
        else:
            for raw, lineno, kind in external:
                lines.append(f"  - {raw}    [line={lineno}, kind={kind}]")

        lines.append("")
        lines.append("")

    lines.append("CYCLES")
    lines.append("")
    if not cycles:
        lines.append("(none)")
    else:
        for cycle in cycles:
            lines.append(" -> ".join(cycle + [cycle[0]]))

    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Import graph written to {outfile}")


if __name__ == "__main__":
    main()
