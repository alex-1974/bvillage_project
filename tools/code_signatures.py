#!/usr/bin/env python3
# tools/code_signatures.py

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

# ------------------------------------------------------------
# BVILLAGE CODE SIGNATURE SCAN
#
# Extracts for productive code:
# - file docstrings
# - __all__
# - imports
# - constants
# - classes
# - dataclass fields
# - methods
# - top-level functions
#
# Output:
#   generated/CODE_SIGNATURES.md
#
# Scope:
# - package code in bvillage/
# - selected root-level productive entry files such as run_in_blender.py
#
# Excludes:
# - caches
# - generated/build artifacts
# - virtual environments
# - tests
# ------------------------------------------------------------

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

PROJECT_ROOT = Path(".").resolve()

# productive package root
CODE_ROOT = PROJECT_ROOT / "bvillage"

# output
OUT = PROJECT_ROOT / "generated" / "CODE_SIGNATURES.md"

# productive root-level files outside the package
EXTRA_FILES = [
    PROJECT_ROOT / "run_in_blender.py",
]

# include patterns relative to PROJECT_ROOT
INCLUDE_PATTERNS = [
    "bvillage/**/*.py",
]

# exclude patterns relative to PROJECT_ROOT
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
]

RELATIVE_PATHS = True
SORT_BY_PATH = True
MAX_DOCSTRING_LINES = 20
INCLUDE_PRIVATE_FUNCTIONS = True
INCLUDE_PRIVATE_METHODS = True
INCLUDE_CLASS_BASES = True
INCLUDE_MODULE_CONSTANTS = True
MAX_CONSTANT_REPR = 120


# ------------------------------------------------------------
# AST helpers
# ------------------------------------------------------------

def unparse_safe(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return "?"


def trim_docstring(text: str | None, max_lines: int = MAX_DOCSTRING_LINES) -> str:
    if not text:
        return ""
    lines = text.strip().splitlines()
    if len(lines) <= max_lines:
        return "\n".join(lines)
    kept = lines[:max_lines]
    kept.append("…")
    return "\n".join(kept)


def format_arg(arg: ast.arg, default: ast.AST | None = None) -> str:
    part = arg.arg
    if arg.annotation is not None:
        part += f": {unparse_safe(arg.annotation)}"
    if default is not None:
        part += f" = {unparse_safe(default)}"
    return part


def format_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args = node.args
    parts: list[str] = []

    posonly = list(args.posonlyargs)
    normal = list(args.args)
    defaults = list(args.defaults)

    pos_defaults_offset = len(posonly) + len(normal) - len(defaults)

    all_pos = posonly + normal
    for i, a in enumerate(all_pos):
        default = None
        if i >= pos_defaults_offset:
            default = defaults[i - pos_defaults_offset]
        parts.append(format_arg(a, default=default))
        if posonly and i == len(posonly) - 1:
            parts.append("/")

    if args.vararg is not None:
        vararg = "*" + format_arg(args.vararg)
        parts.append(vararg)
    elif args.kwonlyargs:
        parts.append("*")

    for kwarg, kwdefault in zip(args.kwonlyargs, args.kw_defaults):
        parts.append(format_arg(kwarg, default=kwdefault))

    if args.kwarg is not None:
        kwarg = "**" + format_arg(args.kwarg)
        parts.append(kwarg)

    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    sig = f"{prefix} {node.name}({', '.join(parts)})"
    if node.returns is not None:
        sig += f" -> {unparse_safe(node.returns)}"
    return sig


def is_dataclass(cls: ast.ClassDef) -> bool:
    for dec in cls.decorator_list:
        if isinstance(dec, ast.Name) and dec.id == "dataclass":
            return True
        if isinstance(dec, ast.Attribute) and dec.attr == "dataclass":
            return True
        if isinstance(dec, ast.Call):
            func = dec.func
            if isinstance(func, ast.Name) and func.id == "dataclass":
                return True
            if isinstance(func, ast.Attribute) and func.attr == "dataclass":
                return True
    return False


def class_bases(cls: ast.ClassDef) -> list[str]:
    return [unparse_safe(base) for base in cls.bases]


def extract_dataclass_fields(cls: ast.ClassDef) -> list[str]:
    fields: list[str] = []

    for node in cls.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            name = node.target.id
            typ = unparse_safe(node.annotation)
            if node.value is not None:
                fields.append(f"{name}: {typ} = {unparse_safe(node.value)}")
            else:
                fields.append(f"{name}: {typ}")
        elif isinstance(node, ast.Assign):
            if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
                continue
            name = node.targets[0].id
            fields.append(f"{name} = {unparse_safe(node.value)}")

    return fields


def is_constant_assign(node: ast.Assign | ast.AnnAssign) -> bool:
    if isinstance(node, ast.Assign):
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            return False
        return node.targets[0].id.isupper()
    if isinstance(node, ast.AnnAssign):
        return isinstance(node.target, ast.Name) and node.target.id.isupper()
    return False


def extract_constant(node: ast.Assign | ast.AnnAssign) -> tuple[str, str]:
    if isinstance(node, ast.Assign):
        name = node.targets[0].id  # type: ignore[union-attr]
        value = unparse_safe(node.value)
        return name, value
    name = node.target.id  # type: ignore[union-attr]
    if node.value is None:
        if node.annotation is not None:
            return name, f": {unparse_safe(node.annotation)}"
        return name, ""
    return name, unparse_safe(node.value)


def shorten_value(text: str, max_len: int = MAX_CONSTANT_REPR) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 1] + "…"


def should_include_function(name: str, *, include_private: bool) -> bool:
    if name.startswith("__") and name.endswith("__"):
        return True
    if name.startswith("_") and not include_private:
        return False
    return True


def module_public_api(tree: ast.Module) -> list[str]:
    names: list[str] = []

    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "__all__":
                try:
                    value = ast.literal_eval(node.value)
                except Exception:
                    return [unparse_safe(node.value)]
                if isinstance(value, (list, tuple)):
                    return [str(x) for x in value]
                return [repr(value)]
    return names


def module_imports(tree: ast.Module) -> list[str]:
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

    return imports


# ------------------------------------------------------------
# Scan
# ------------------------------------------------------------

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


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def relpath(path: Path) -> str:
    if RELATIVE_PATHS:
        return path.relative_to(PROJECT_ROOT).as_posix()
    return str(path)


def scan_file(path: Path) -> dict[str, Any]:
    source = read_file(path)
    tree = ast.parse(source, filename=relpath(path))

    module_doc = trim_docstring(ast.get_docstring(tree))
    all_names = module_public_api(tree)
    imports = module_imports(tree)

    constants: list[tuple[str, str]] = []
    functions: list[dict[str, Any]] = []
    classes: list[dict[str, Any]] = []

    for node in tree.body:
        if INCLUDE_MODULE_CONSTANTS and isinstance(node, (ast.Assign, ast.AnnAssign)) and is_constant_assign(node):
            name, value = extract_constant(node)
            if name != "__all__":
                constants.append((name, shorten_value(value)))

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not should_include_function(node.name, include_private=INCLUDE_PRIVATE_FUNCTIONS):
                continue
            functions.append(
                {
                    "name": node.name,
                    "signature": format_signature(node),
                    "docstring": trim_docstring(ast.get_docstring(node)),
                }
            )

        elif isinstance(node, ast.ClassDef):
            cls_doc = trim_docstring(ast.get_docstring(node))
            methods: list[dict[str, Any]] = []
            nested_classes: list[str] = []

            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not should_include_function(item.name, include_private=INCLUDE_PRIVATE_METHODS):
                        continue
                    methods.append(
                        {
                            "name": item.name,
                            "signature": format_signature(item),
                            "docstring": trim_docstring(ast.get_docstring(item)),
                        }
                    )
                elif isinstance(item, ast.ClassDef):
                    nested_classes.append(item.name)

            classes.append(
                {
                    "name": node.name,
                    "docstring": cls_doc,
                    "is_dataclass": is_dataclass(node),
                    "bases": class_bases(node) if INCLUDE_CLASS_BASES else [],
                    "fields": extract_dataclass_fields(node) if is_dataclass(node) else [],
                    "methods": methods,
                    "nested_classes": nested_classes,
                }
            )

    return {
        "path": relpath(path),
        "docstring": module_doc,
        "__all__": all_names,
        "imports": imports,
        "constants": constants,
        "classes": classes,
        "functions": functions,
    }


# ------------------------------------------------------------
# Markdown rendering
# ------------------------------------------------------------

def anchor_for_path(path_str: str) -> str:
    out = path_str.lower()
    repl = []
    for ch in out:
        if ch.isalnum():
            repl.append(ch)
        elif ch in {"/", ".", "_", "-"}:
            repl.append("-")
    text = "".join(repl)
    while "--" in text:
        text = text.replace("--", "-")
    return text.strip("-")


def fenced_text(text: str) -> list[str]:
    if not text:
        return ["_None_"]
    return ["```text", text, "```"]


def render_toc(file_infos: list[dict[str, Any]]) -> list[str]:
    lines = ["# CODE SIGNATURES", "", "## Table of Contents", ""]
    for info in file_infos:
        path = info["path"]
        lines.append(f"- [{path}](#{anchor_for_path(path)})")
    lines.append("")
    return lines


def render_file(info: dict[str, Any]) -> list[str]:
    lines: list[str] = []

    lines.append(f"## {info['path']}")
    lines.append("")

    lines.append("### Docstring")
    lines.extend(fenced_text(info["docstring"]))
    lines.append("")

    lines.append("### `__all__`")
    if info["__all__"]:
        for name in info["__all__"]:
            lines.append(f"- `{name}`")
    else:
        lines.append("_None_")
    lines.append("")

    lines.append("### Imports")
    if info["imports"]:
        for imp in info["imports"]:
            lines.append(f"- `{imp}`")
    else:
        lines.append("_None_")
    lines.append("")

    lines.append("### Constants")
    if info["constants"]:
        for name, value in info["constants"]:
            if value:
                lines.append(f"- `{name}` = `{value}`")
            else:
                lines.append(f"- `{name}`")
    else:
        lines.append("_None_")
    lines.append("")

    lines.append("### Classes")
    if info["classes"]:
        for cls in info["classes"]:
            lines.append(f"#### `{cls['name']}`")
            lines.append("")

            if cls["bases"]:
                lines.append("**Bases**")
                for base in cls["bases"]:
                    lines.append(f"- `{base}`")
                lines.append("")

            lines.append("**Docstring**")
            lines.extend(fenced_text(cls["docstring"]))
            lines.append("")

            lines.append(f"**Dataclass**: `{'yes' if cls['is_dataclass'] else 'no'}`")
            lines.append("")

            if cls["fields"]:
                lines.append("**Fields**")
                for field in cls["fields"]:
                    lines.append(f"- `{field}`")
                lines.append("")

            if cls["nested_classes"]:
                lines.append("**Nested classes**")
                for nested in cls["nested_classes"]:
                    lines.append(f"- `{nested}`")
                lines.append("")

            lines.append("**Methods**")
            if cls["methods"]:
                for method in cls["methods"]:
                    lines.append(f"- `{method['signature']}`")
                    if method["docstring"]:
                        lines.append("")
                        lines.append("  Docstring:")
                        lines.append("")
                        for doc_line in fenced_text(method["docstring"]):
                            if doc_line == "_None_":
                                lines.append("  _None_")
                            else:
                                lines.append(f"  {doc_line}")
                        lines.append("")
            else:
                lines.append("_None_")
                lines.append("")
    else:
        lines.append("_None_")
        lines.append("")

    lines.append("### Top-level Functions")
    if info["functions"]:
        for func in info["functions"]:
            lines.append(f"- `{func['signature']}`")
            if func["docstring"]:
                lines.append("")
                lines.append("  Docstring:")
                lines.append("")
                for doc_line in fenced_text(func["docstring"]):
                    if doc_line == "_None_":
                        lines.append("  _None_")
                    else:
                        lines.append(f"  {doc_line}")
                lines.append("")
    else:
        lines.append("_None_")
        lines.append("")

    lines.append("---")
    lines.append("")
    return lines


def render_markdown(file_infos: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    lines.extend(render_toc(file_infos))

    for info in file_infos:
        lines.extend(render_file(info))

    return "\n".join(lines).rstrip() + "\n"


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main() -> None:
    files = collect_files()
    infos = [scan_file(path) for path in files]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render_markdown(infos), encoding="utf-8")

    print(f"Wrote {OUT}")
    print(f"Files scanned: {len(files)}")


if __name__ == "__main__":
    main()
