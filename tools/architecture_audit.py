#!/usr/bin/env python3
# tools/architecture_audit.py

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(".").resolve()
OUT = PROJECT_ROOT / "generated" / "ARCHITECTURE_AUDIT.md"

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


@dataclass(frozen=True, slots=True)
class FileInfo:
    path: Path
    relpath: str
    module: str
    layer: str
    imports: tuple[str, ...]
    source: str
    tree: ast.AST | None


@dataclass(frozen=True, slots=True)
class Violation:
    severity: str
    code: str
    file: str
    message: str
    evidence: str = ""

    def sort_key(self) -> tuple[str, str, str, str]:
        return (self.severity, self.code, self.file, self.message)


def relpath(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


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

    filtered.sort(key=lambda p: p.relative_to(PROJECT_ROOT).as_posix())
    return filtered


def read_python_file(path: Path) -> FileInfo:
    source = path.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(source, filename=relpath(path))
    except SyntaxError:
        tree = None

    imports: list[str] = []
    if tree is not None:
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                mod = "." * node.level + (node.module or "")
                imports.append(mod)

    mod = module_name(path)
    return FileInfo(
        path=path,
        relpath=relpath(path),
        module=mod,
        layer=detect_layer(mod),
        imports=tuple(sorted(set(imports))),
        source=source,
        tree=tree,
    )


def audit_parse(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []
    for f in files:
        if f.tree is None:
            out.append(
                Violation(
                    severity="HARD",
                    code="SYNTAX",
                    file=f.relpath,
                    message="File does not parse.",
                )
            )
    return out


def audit_import_layers(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []

    for f in files:
        for imp in f.imports:
            if not imp.startswith("bvillage"):
                continue

            if f.layer == "core":
                if imp.startswith("bvillage.types"):
                    out.append(
                        Violation(
                            severity="HARD",
                            code="CORE_IMPORTS_TYPE",
                            file=f.relpath,
                            message="Core imports type layer.",
                            evidence=imp,
                        )
                    )
                if imp.startswith("bvillage.domains"):
                    out.append(
                        Violation(
                            severity="HARD",
                            code="CORE_IMPORTS_DOMAIN",
                            file=f.relpath,
                            message="Core imports domain layer.",
                            evidence=imp,
                        )
                    )
                if imp.startswith("bvillage.blender"):
                    out.append(
                        Violation(
                            severity="HARD",
                            code="CORE_IMPORTS_BLENDER",
                            file=f.relpath,
                            message="Core imports blender layer.",
                            evidence=imp,
                        )
                    )

            if f.layer == "type":
                if imp.startswith("bvillage.domains") and ".blender." in imp:
                    out.append(
                        Violation(
                            severity="HARD",
                            code="TYPE_IMPORTS_DOMAIN_BLENDER",
                            file=f.relpath,
                            message="Type layer imports domain-blender.",
                            evidence=imp,
                        )
                    )
                if imp.startswith("bvillage.blender"):
                    out.append(
                        Violation(
                            severity="HARD",
                            code="TYPE_IMPORTS_BLENDER",
                            file=f.relpath,
                            message="Type layer imports blender.",
                            evidence=imp,
                        )
                    )

            if f.layer == "domain-core":
                if imp.startswith("bvillage.blender") or ".blender." in imp:
                    out.append(
                        Violation(
                            severity="HARD",
                            code="DOMAIN_CORE_IMPORTS_BLENDER",
                            file=f.relpath,
                            message="Domain-core imports blender code.",
                            evidence=imp,
                        )
                    )

    return out


def audit_bpy_imports(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []

    for f in files:
        if f.layer in {"blender", "domain-blender", "entry"}:
            continue

        for imp in f.imports:
            if imp == "bpy" or imp.startswith("bpy."):
                out.append(
                    Violation(
                        severity="HARD",
                        code="NON_BLENDER_IMPORTS_BPY",
                        file=f.relpath,
                        message="Non-blender file imports bpy.",
                        evidence=imp,
                    )
                )
    return out


def audit_core_arch_knowledge(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []
    forbidden_tokens = (
        "FW-LH-",
        "BOX_FRAME",
        "STOREY_FRAME",
        "CRUCK_FRAME",
        "AISLED_FRAME",
        "WALL_GRID_FRAME",
        "longhouse",
        "fachwerk",
    )

    for f in files:
        if f.layer != "core":
            continue
        for token in forbidden_tokens:
            if token in f.source:
                out.append(
                    Violation(
                        severity="MEDIUM",
                        code="CORE_ARCH_KNOWLEDGE",
                        file=f.relpath,
                        message="Core appears to contain domain/archetype knowledge.",
                        evidence=token,
                    )
                )
    return out


def audit_renderer_fallbacks(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []
    suspicious = (
        "derive_frameplan",
        "derive_roofplan",
        "frameplan_to_dict",
        "if not fp",
        "if not frameplan",
        "missing members",
        "fallback",
        "reconstruct",
    )

    for f in files:
        if f.layer not in {"blender", "domain-blender"}:
            continue

        lowered = f.source.lower()
        for token in suspicious:
            if token.lower() in lowered:
                out.append(
                    Violation(
                        severity="MEDIUM",
                        code="RENDERER_FALLBACK_REVIEW",
                        file=f.relpath,
                        message="Renderer may contain structural fallback or derivation logic. Review manually.",
                        evidence=token,
                    )
                )
    return out


def audit_notes_schema(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []

    for f in files:
        if f.tree is None:
            continue
        if 'notes["domains"]' in f.source or "notes['domains']" in f.source:
            continue
        if "structure.notes" in f.source and "set_domain_artifact" not in f.source and "get_domain_artifact" not in f.source:
            out.append(
                Violation(
                    severity="MEDIUM",
                    code="NOTES_SCHEMA_REVIEW",
                    file=f.relpath,
                    message="Direct notes access without notes helpers detected. Review schema usage.",
                )
            )
    return out


def render_markdown(files: list[FileInfo], violations: list[Violation]) -> str:
    layer_counts: dict[str, int] = {}
    for f in files:
        layer_counts[f.layer] = layer_counts.get(f.layer, 0) + 1

    violations = sorted(violations, key=lambda v: v.sort_key())

    lines: list[str] = []
    lines.append("# ARCHITECTURE AUDIT")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- files scanned: {len(files)}")
    lines.append(f"- violations: {len(violations)}")
    lines.append("")

    lines.append("## Layers")
    lines.append("")
    for layer in sorted(layer_counts):
        lines.append(f"- `{layer}`: {layer_counts[layer]}")
    lines.append("")

    lines.append("## Violations")
    lines.append("")
    if not violations:
        lines.append("No violations detected.")
        lines.append("")
        return "\n".join(lines)

    by_code: dict[str, list[Violation]] = {}
    for v in violations:
        by_code.setdefault(v.code, []).append(v)

    for code in sorted(by_code):
        lines.append(f"### {code}")
        lines.append("")
        for v in by_code[code]:
            lines.append(f"- severity: `{v.severity}`")
            lines.append(f"- file: `{v.file}`")
            lines.append(f"- message: {v.message}")
            if v.evidence:
                lines.append(f"- evidence: `{v.evidence}`")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    files = [read_python_file(path) for path in collect_files()]

    violations: list[Violation] = []
    violations.extend(audit_parse(files))
    violations.extend(audit_import_layers(files))
    violations.extend(audit_bpy_imports(files))
    violations.extend(audit_core_arch_knowledge(files))
    violations.extend(audit_renderer_fallbacks(files))
    violations.extend(audit_notes_schema(files))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render_markdown(files, violations), encoding="utf-8")

    print(f"Wrote {OUT}")
    print(f"Files scanned: {len(files)}")
    print(f"Violations: {len(violations)}")

    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
