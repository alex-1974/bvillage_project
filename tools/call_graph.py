#!/usr/bin/env python3
# tools/call_graph.py

from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path
from typing import Any


# ------------------------------------------------------------
# BVILLAGE CALL GRAPH SCAN
#
# Extracts for productive code:
# - module inventory
# - function / method inventory
# - outgoing calls
# - incoming calls
# - unresolved call names
#
# Output:
#   generated/CALL_GRAPH.md
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
#
# Important limitation
# --------------------
# This is a static AST-based call graph.
# It resolves:
# - direct function calls by name
# - method calls on self / cls inside classes
# - simple imported aliases
#
# It does not fully resolve:
# - dynamic dispatch
# - monkey patching
# - reflection
# - runtime-generated callables
# - arbitrary attribute calls on unknown objects
# ------------------------------------------------------------


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

PROJECT_ROOT = Path(".").resolve()

CODE_ROOT = PROJECT_ROOT / "bvillage"

OUT = PROJECT_ROOT / "generated" / "CALL_GRAPH.md"

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
]

RELATIVE_PATHS = True
SORT_BY_PATH = True
INCLUDE_PRIVATE_FUNCTIONS = True
INCLUDE_PRIVATE_METHODS = True


# ------------------------------------------------------------
# PATH / MODULE HELPERS
# ------------------------------------------------------------

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

    if mod.startswith("tools"):
        return "tools"

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


# ------------------------------------------------------------
# AST HELPERS
# ------------------------------------------------------------

def unparse_safe(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return "?"


def should_include_function(name: str, *, include_private: bool) -> bool:
    if name.startswith("__") and name.endswith("__"):
        return True
    if name.startswith("_") and not include_private:
        return False
    return True


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
        part = a.arg
        if a.annotation is not None:
            part += f": {unparse_safe(a.annotation)}"
        if default is not None:
            part += f" = {unparse_safe(default)}"
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


# ------------------------------------------------------------
# SYMBOL COLLECTION
# ------------------------------------------------------------

def module_aliases(tree: ast.Module) -> tuple[dict[str, str], dict[str, str]]:
    """
    Returns:
    - imported_names: alias/name -> module or module.symbol
    - imported_modules: alias/name -> module
    """
    imported_names: dict[str, str] = {}
    imported_modules: dict[str, str] = {}

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules[alias.asname or alias.name] = alias.name
        elif isinstance(node, ast.ImportFrom):
            mod = "." * node.level + (node.module or "")
            for alias in node.names:
                if alias.name == "*":
                    continue
                imported_names[alias.asname or alias.name] = f"{mod}.{alias.name}".strip(".")
    return imported_names, imported_modules


def collect_definitions(
    tree: ast.Module,
    mod: str,
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, str],
    dict[str, dict[str, str]],
]:
    """
    Returns:
    - defs_by_qualname
    - top_level_name_to_qualname
    - class_method_name_to_qualname[class_name][method_name]
    """
    defs_by_qualname: dict[str, dict[str, Any]] = {}
    top_level_name_to_qualname: dict[str, str] = {}
    class_method_name_to_qualname: dict[str, dict[str, str]] = defaultdict(dict)

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not should_include_function(node.name, include_private=INCLUDE_PRIVATE_FUNCTIONS):
                continue
            qual = f"{mod}.{node.name}"
            defs_by_qualname[qual] = {
                "kind": "function",
                "module": mod,
                "class": None,
                "name": node.name,
                "qualname": qual,
                "signature": format_signature(node),
                "lineno": node.lineno,
                "node": node,
            }
            top_level_name_to_qualname[node.name] = qual

        elif isinstance(node, ast.ClassDef):
            class_qual = f"{mod}.{node.name}"
            defs_by_qualname[class_qual] = {
                "kind": "class",
                "module": mod,
                "class": node.name,
                "name": node.name,
                "qualname": class_qual,
                "signature": f"class {node.name}",
                "lineno": node.lineno,
                "node": node,
            }

            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not should_include_function(item.name, include_private=INCLUDE_PRIVATE_METHODS):
                        continue
                    method_qual = f"{mod}.{node.name}.{item.name}"
                    defs_by_qualname[method_qual] = {
                        "kind": "method",
                        "module": mod,
                        "class": node.name,
                        "name": item.name,
                        "qualname": method_qual,
                        "signature": format_signature(item),
                        "lineno": item.lineno,
                        "node": item,
                    }
                    class_method_name_to_qualname[node.name][item.name] = method_qual

    return defs_by_qualname, top_level_name_to_qualname, dict(class_method_name_to_qualname)


# ------------------------------------------------------------
# CALL RESOLUTION
# ------------------------------------------------------------

class CallVisitor(ast.NodeVisitor):
    def __init__(
        self,
        *,
        module: str,
        current_owner_qualname: str,
        current_class_name: str | None,
        top_level_name_to_qualname: dict[str, str],
        class_method_name_to_qualname: dict[str, dict[str, str]],
        imported_names: dict[str, str],
        imported_modules: dict[str, str],
        module_defs_by_name: dict[str, list[str]],
        known_modules: set[str],
    ) -> None:
        self.module = module
        self.current_owner_qualname = current_owner_qualname
        self.current_class_name = current_class_name
        self.top_level_name_to_qualname = top_level_name_to_qualname
        self.class_method_name_to_qualname = class_method_name_to_qualname
        self.imported_names = imported_names
        self.imported_modules = imported_modules
        self.module_defs_by_name = module_defs_by_name
        self.known_modules = known_modules

        self.resolved_calls: list[str] = []
        self.unresolved_calls: list[str] = []

    def visit_Call(self, node: ast.Call) -> None:
        target = self._resolve_call_target(node.func)
        if target is not None:
            self.resolved_calls.append(target)
        else:
            raw = self._raw_call_name(node.func)
            if raw:
                self.unresolved_calls.append(raw)
        self.generic_visit(node)

    def _resolve_call_target(self, func: ast.AST) -> str | None:
        # direct function call: foo(...)
        if isinstance(func, ast.Name):
            name = func.id

            if name in self.top_level_name_to_qualname:
                return self.top_level_name_to_qualname[name]

            if name in self.imported_names:
                return self.imported_names[name]

            if name in self.imported_modules:
                imported_mod = self.imported_modules[name]
                if imported_mod in self.known_modules:
                    return imported_mod

            # unique global definition by bare name across scanned modules
            cands = self.module_defs_by_name.get(name, [])
            if len(cands) == 1:
                return cands[0]

            return None

        # method or attribute call: something.foo(...)
        if isinstance(func, ast.Attribute):
            attr = func.attr

            # self.foo(...)
            if isinstance(func.value, ast.Name) and func.value.id == "self":
                if self.current_class_name is not None:
                    return self.class_method_name_to_qualname.get(self.current_class_name, {}).get(attr)

            # cls.foo(...)
            if isinstance(func.value, ast.Name) and func.value.id == "cls":
                if self.current_class_name is not None:
                    return self.class_method_name_to_qualname.get(self.current_class_name, {}).get(attr)

            # imported_module.foo(...)
            if isinstance(func.value, ast.Name):
                base = func.value.id
                if base in self.imported_modules:
                    return f"{self.imported_modules[base]}.{attr}"

            # imported symbol object style is not reliably statically resolvable
            # e.g. provider.plan(...)
            return None

        return None

    def _raw_call_name(self, func: ast.AST) -> str:
        if isinstance(func, ast.Name):
            return func.id
        if isinstance(func, ast.Attribute):
            return unparse_safe(func)
        return unparse_safe(func)


# ------------------------------------------------------------
# ANALYSIS
# ------------------------------------------------------------

def parse_module(path: Path) -> ast.Module | None:
    try:
        source = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        source = path.read_text(encoding="utf-8", errors="replace")

    try:
        return ast.parse(source, filename=relpath(path))
    except SyntaxError:
        return None


def analyze(files: list[Path]) -> dict[str, Any]:
    module_trees: dict[str, ast.Module] = {}
    defs_by_qualname: dict[str, dict[str, Any]] = {}
    top_level_name_to_qualname_by_module: dict[str, dict[str, str]] = {}
    class_method_name_to_qualname_by_module: dict[str, dict[str, dict[str, str]]] = {}
    imported_names_by_module: dict[str, dict[str, str]] = {}
    imported_modules_by_module: dict[str, dict[str, str]] = {}
    file_by_module: dict[str, Path] = {}

    for path in files:
        mod = module_name(path)
        tree = parse_module(path)
        if tree is None:
            continue

        module_trees[mod] = tree
        file_by_module[mod] = path

        imported_names, imported_modules = module_aliases(tree)
        imported_names_by_module[mod] = imported_names
        imported_modules_by_module[mod] = imported_modules

        defs, top_names, method_names = collect_definitions(tree, mod)
        defs_by_qualname.update(defs)
        top_level_name_to_qualname_by_module[mod] = top_names
        class_method_name_to_qualname_by_module[mod] = method_names

    known_modules = set(module_trees.keys())

    module_defs_by_name: dict[str, list[str]] = defaultdict(list)
    for qual, meta in defs_by_qualname.items():
        if meta["kind"] in {"function", "method"}:
            module_defs_by_name[meta["name"]].append(qual)

    call_out: dict[str, set[str]] = defaultdict(set)
    call_in: dict[str, set[str]] = defaultdict(set)
    unresolved_out: dict[str, set[str]] = defaultdict(set)

    for qual, meta in defs_by_qualname.items():
        node = meta["node"]
        if meta["kind"] not in {"function", "method"}:
            continue

        mod = meta["module"]
        visitor = CallVisitor(
            module=mod,
            current_owner_qualname=qual,
            current_class_name=meta["class"],
            top_level_name_to_qualname=top_level_name_to_qualname_by_module.get(mod, {}),
            class_method_name_to_qualname=class_method_name_to_qualname_by_module.get(mod, {}),
            imported_names=imported_names_by_module.get(mod, {}),
            imported_modules=imported_modules_by_module.get(mod, {}),
            module_defs_by_name=module_defs_by_name,
            known_modules=known_modules,
        )
        visitor.visit(node)

        for dst in visitor.resolved_calls:
            call_out[qual].add(dst)
            call_in[dst].add(qual)

        for raw in visitor.unresolved_calls:
            unresolved_out[qual].add(raw)

    return {
        "defs_by_qualname": defs_by_qualname,
        "call_out": call_out,
        "call_in": call_in,
        "unresolved_out": unresolved_out,
        "file_by_module": file_by_module,
    }


# ------------------------------------------------------------
# MARKDOWN RENDERING
# ------------------------------------------------------------

def anchor_for_name(text: str) -> str:
    out = text.lower()
    repl = []
    for ch in out:
        if ch.isalnum():
            repl.append(ch)
        elif ch in {"/", ".", "_", "-", " "}:
            repl.append("-")
    text2 = "".join(repl)
    while "--" in text2:
        text2 = text2.replace("--", "-")
    return text2.strip("-")


def render_toc(functions: list[dict[str, Any]]) -> list[str]:
    lines = ["# CALL GRAPH", "", "## Table of Contents", ""]
    for meta in functions:
        qual = meta["qualname"]
        lines.append(f"- [{qual}](#{anchor_for_name(qual)})")
    lines.append("")
    return lines


def render_markdown(analysis: dict[str, Any]) -> str:
    defs_by_qualname = analysis["defs_by_qualname"]
    call_out = analysis["call_out"]
    call_in = analysis["call_in"]
    unresolved_out = analysis["unresolved_out"]

    function_defs = [
        meta
        for meta in defs_by_qualname.values()
        if meta["kind"] in {"function", "method"}
    ]
    function_defs.sort(key=lambda x: x["qualname"])

    total_edges = sum(len(v) for v in call_out.values())
    total_unresolved = sum(len(v) for v in unresolved_out.values())

    lines: list[str] = []
    lines.extend(render_toc(function_defs))

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- scanned callables: {len(function_defs)}")
    lines.append(f"- resolved call edges: {total_edges}")
    lines.append(f"- unresolved call names: {total_unresolved}")
    lines.append("")

    lines.append("## Callable Inventory")
    lines.append("")

    modules_seen: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for meta in function_defs:
        modules_seen[meta["module"]].append(meta)

    for mod in sorted(modules_seen):
        lines.append(f"### {mod}")
        lines.append("")
        lines.append(f"- layer: `{layer_of_module(mod)}`")
        lines.append("")
        for meta in sorted(modules_seen[mod], key=lambda x: x["qualname"]):
            lines.append(f"- `{meta['qualname']}`")
        lines.append("")

    lines.append("## Calls by Callable")
    lines.append("")

    for meta in function_defs:
        qual = meta["qualname"]

        lines.append(f"### {qual}")
        lines.append("")
        lines.append(f"- module: `{meta['module']}`")
        lines.append(f"- layer: `{layer_of_module(meta['module'])}`")
        lines.append(f"- kind: `{meta['kind']}`")
        if meta["class"] is not None:
            lines.append(f"- class: `{meta['class']}`")
        lines.append(f"- line: `{meta['lineno']}`")
        lines.append("")
        lines.append("**Signature**")
        lines.append("")
        lines.append(f"- `{meta['signature']}`")
        lines.append("")

        lines.append("**Calls**")
        outs = sorted(call_out.get(qual, set()))
        if outs:
            for dst in outs:
                lines.append(f"- `{qual}` -> `{dst}`")
        else:
            lines.append("_None_")
        lines.append("")

        lines.append("**Called by**")
        ins = sorted(call_in.get(qual, set()))
        if ins:
            for src in ins:
                lines.append(f"- `{src}` -> `{qual}`")
        else:
            lines.append("_None_")
        lines.append("")

        lines.append("**Unresolved calls**")
        unresolved = sorted(unresolved_out.get(qual, set()))
        if unresolved:
            for raw in unresolved:
                lines.append(f"- `{raw}`")
        else:
            lines.append("_None_")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main() -> None:
    files = collect_files()
    analysis = analyze(files)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render_markdown(analysis), encoding="utf-8")

    defs_by_qualname = analysis["defs_by_qualname"]
    function_defs = [
        meta
        for meta in defs_by_qualname.values()
        if meta["kind"] in {"function", "method"}
    ]

    print(f"Wrote {OUT}")
    print(f"Files scanned: {len(files)}")
    print(f"Callables scanned: {len(function_defs)}")


if __name__ == "__main__":
    main()
