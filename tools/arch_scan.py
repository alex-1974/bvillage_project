#!/usr/bin/env python3
# tools/arch_scan.py

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(".").resolve()
OUT = PROJECT_ROOT / "generated" / "ARCH_SCAN.md"

EXTRA_FILES = [
    PROJECT_ROOT / "run_in_blender.py",
]

INCLUDE_PATTERNS = [
    "bvillage/**/*.py",
]

EXCLUDE_PATTERNS = [
    "**/__pycache__/**",
    "**/*.pyc",
    "**/*.pyo",
    "**/*.pyd",
    "**/.pytest_cache/**",
    "**/.mypy_cache/**",
    "**/.ruff_cache/**",
    "**/.venv/**",
    "**/venv/**",
    "**/env/**",
    "**/site-packages/**",
    "**/dist-packages/**",
    "**/generated/**",
    "**/build/**",
    "**/dist/**",
    "**/tmp/**",
    "**/tests/**",
    "**/test/**",
    "**/research/**",
]

RELATIVE_PATHS = True
SORT_BY_PATH = True
MAX_DOCSTRING_LINES = 16


@dataclass(frozen=True, slots=True)
class FileScan:
    path: str
    module: str
    layer: str
    has_module_docstring: bool
    module_docstring: str
    has_all: bool
    all_names: tuple[str, ...]
    imports: tuple[str, ...]
    top_level: tuple[str, ...]


def relpath(path: Path) -> str:
    if RELATIVE_PATHS:
        return path.relative_to(PROJECT_ROOT).as_posix()
    return str(path)


def module_name(path: Path) -> str:
    rel = path.relative_to(PROJECT_ROOT)

    if rel.name == "run_in_blender.py":
        return "run_in_blender"

    if rel.name == "__init__.py":
        rel = rel.parent
    else:
        rel = rel.with_suffix("")

    return ".".join(rel.parts)


def detect_layer(mod: str) -> str:
    if mod == "run_in_blender":
        return "entry"

    if mod.startswith("bvillage.core"):
        return "core"

    if mod.startswith("bvillage.types"):
        if ".contracts." in mod:
            return "type-contracts"
        return "type"

    if mod.startswith("bvillage.domains"):
        if ".blender." in mod:
            return "domain-blender"
        if ".contracts." in mod:
            return "domain-contracts"
        if ".validation." in mod:
            return "domain-validation"
        return "domain-core"

    if mod.startswith("bvillage.blender"):
        return "blender"

    if mod.startswith("tools"):
        return "tools"

    if mod.startswith("bvillage"):
        return "package"

    return "other"


def collect_files() -> list[Path]:
    files: set[Path] = set()

    for pattern in INCLUDE_PATTERNS:
        for path in PROJECT_ROOT.glob(pattern):
            if path.is_file():
                files.add(path.resolve())

    for path in EXTRA_FILES:
        if path.exists() and path.is_file():
            files.add(path.resolve())

    filtered: list[Path] = []
    for path in files:
        rel = path.relative_to(PROJECT_ROOT)
        if any(rel.match(pattern) for pattern in EXCLUDE_PATTERNS):
            continue
        filtered.append(path)

    if SORT_BY_PATH:
        filtered.sort(key=lambda p: p.relative_to(PROJECT_ROOT).as_posix())

    return filtered


def trim_docstring(text: str | None) -> str:
    if not text:
        return ""
    lines = text.strip().splitlines()
    if len(lines) <= MAX_DOCSTRING_LINES:
        return "\n".join(lines)
    return "\n".join(lines[:MAX_DOCSTRING_LINES] + ["…"])


def unparse_safe(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return "?"


def format_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args = node.args
    parts: list[str] = []

    posonly = list(args.posonlyargs)
    normal = list(args.args)
    defaults = list(args.defaults)
    pos_defaults_offset = len(posonly) + len(normal) - len(defaults)

    all_pos = posonly + normal
    for i, a in enumerate(all_pos):
        part = a.arg
        if a.annotation is not None:
            part += f": {unparse_safe(a.annotation)}"
        if i >= pos_defaults_offset:
            part += f" = {unparse_safe(defaults[i - pos_defaults_offset])}"
        parts.append(part)
        if posonly and i == len(posonly) - 1:
            parts.append("/")

    if args.vararg is not None:
        part = "*" + args.vararg.arg
        if args.vararg.annotation is not None:
            part += f": {unparse_safe(args.vararg.annotation)}"
        parts.append(part)
    elif args.kwonlyargs:
        parts.append("*")

    for kwarg, kwdefault in zip(args.kwonlyargs, args.kw_defaults):
        part = kwarg.arg
        if kwarg.annotation is not None:
            part += f": {unparse_safe(kwarg.annotation)}"
        if kwdefault is not None:
            part += f" = {unparse_safe(kwdefault)}"
        parts.append(part)

    if args.kwarg is not None:
        part = "**" + args.kwarg.arg
        if args.kwarg.annotation is not None:
            part += f": {unparse_safe(args.kwarg.annotation)}"
        parts.append(part)

    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    sig = f"{prefix} {node.name}({', '.join(parts)})"
    if node.returns is not None:
        sig += f" -> {unparse_safe(node.returns)}"
    return sig


def extract_all_names(tree: ast.Module) -> tuple[bool, tuple[str, ...]]:
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    try:
                        value = ast.literal_eval(node.value)
                    except Exception:
                        return True, (unparse_safe(node.value),)
                    if isinstance(value, (list, tuple)):
                        return True, tuple(str(x) for x in value)
                    return True, (repr(value),)
    return False, ()


def extract_imports(tree: ast.Module) -> tuple[str, ...]:
    imports: list[str] = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    imports.append(f"import {alias.name} as {alias.asname}")
                else:
                    imports.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            mod = "." * node.level + (node.module or "")
            names = []
            for alias in node.names:
                if alias.asname:
                    names.append(f"{alias.name} as {alias.asname}")
                else:
                    names.append(alias.name)
            imports.append(f"from {mod} import {', '.join(names)}")

    return tuple(imports)


def extract_top_level(tree: ast.Module) -> tuple[str, ...]:
    items: list[str] = []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            items.append(format_signature(node))
        elif isinstance(node, ast.ClassDef):
            items.append(f"class {node.name}")
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id != "__all__":
                    if target.id.isupper():
                        items.append(f"CONST {target.id}")
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id.isupper():
                items.append(f"CONST {node.target.id}")

    return tuple(items)


def scan_file(path: Path) -> FileScan:
    source = path.read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(source, filename=relpath(path))
    module_doc = trim_docstring(ast.get_docstring(tree))
    has_all, all_names = extract_all_names(tree)

    return FileScan(
        path=relpath(path),
        module=module_name(path),
        layer=detect_layer(module_name(path)),
        has_module_docstring=bool(module_doc),
        module_docstring=module_doc,
        has_all=has_all,
        all_names=all_names,
        imports=extract_imports(tree),
        top_level=extract_top_level(tree),
    )


def render_markdown(scans: list[FileScan]) -> str:
    layer_counts: dict[str, int] = {}
    for scan in scans:
        layer_counts[scan.layer] = layer_counts.get(scan.layer, 0) + 1

    lines: list[str] = []
    lines.append("# ARCH SCAN")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- files: {len(scans)}")
    lines.append("")

    lines.append("## Layers")
    lines.append("")
    for layer in sorted(layer_counts):
        lines.append(f"- `{layer}`: {layer_counts[layer]}")
    lines.append("")

    lines.append("## File Inventory")
    lines.append("")
    for scan in scans:
        lines.append(f"### {scan.path}")
        lines.append("")
        lines.append(f"- module: `{scan.module}`")
        lines.append(f"- layer: `{scan.layer}`")
        lines.append(f"- module docstring: `{'yes' if scan.has_module_docstring else 'no'}`")
        lines.append(f"- __all__: `{'yes' if scan.has_all else 'no'}`")
        lines.append("")

        lines.append("**Docstring**")
        lines.append("")
        if scan.module_docstring:
            lines.append("```text")
            lines.append(scan.module_docstring)
            lines.append("```")
        else:
            lines.append("_None_")
        lines.append("")

        lines.append("**`__all__`**")
        lines.append("")
        if scan.all_names:
            for name in scan.all_names:
                lines.append(f"- `{name}`")
        else:
            lines.append("_None_")
        lines.append("")

        lines.append("**Imports**")
        lines.append("")
        if scan.imports:
            for imp in scan.imports:
                lines.append(f"- `{imp}`")
        else:
            lines.append("_None_")
        lines.append("")

        lines.append("**Top-level**")
        lines.append("")
        if scan.top_level:
            for item in scan.top_level:
                lines.append(f"- `{item}`")
        else:
            lines.append("_None_")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    files = collect_files()
    scans = [scan_file(path) for path in files]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render_markdown(scans), encoding="utf-8")

    print(f"Wrote {OUT}")
    print(f"Files scanned: {len(scans)}")


if __name__ == "__main__":
    main()
