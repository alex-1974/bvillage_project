#!/usr/bin/env python3
# tools/architecture_audit.py

"""
BVILLAGE architecture audit.

Purpose
-------
Static architecture audit against the current BVILLAGE target architecture.

This tool checks:
- layer boundary violations
- plugin isolation violations
- policy leakage
- contract placement hints
- naming / path hygiene
- structural grammar boundaries

It is intentionally conservative:
- reports grounded findings only
- does not guess intent
- does not mutate repository files

Output
------
Writes a markdown report, default:
    generated/architecture_audit.md

Severity
--------
- HARD   architecture violation
- MEDIUM design weakness / likely migration target
- LOW    hygiene / naming / structure issue

Usage
-----
    python3 tools/architecture_audit.py
    python3 tools/architecture_audit.py --root . --out generated/architecture_audit.md
    python3 tools/architecture_audit.py --include-tests
"""

from __future__ import annotations

import argparse
import ast
import io
import re
import tokenize
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "build",
    "dist",
    "tmp",
    ".mypy_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
}

ROLE_PREFIXES = (
    "plan_",
    "derive_",
    "build_",
    "validate_",
    "audit_",
    "report_",
    "policy_",
    "schema_",
    "mesh_",
)

GENERIC_BAD_FILENAMES = {
    "utils.py",
    "helpers.py",
    "common.py",
    "check.py",
}

CONCRETE_ARCH_KEYWORDS = (
    "hallenhaus",
    "longhouse",
    "stadthaus",
    "townhouse",
    "ernhaus",
    "fachwerk",
    "cruck",
    "aisled",
    "box_frame",
    "storey_frame",
    "wall_grid_frame",
    "fw-",
    "fw_",
)

CTX_POLICY_FIELDS = (
    "region",
    "epoch_band",
    "settlement_type",
    "wealth",
    "climate_hint",
    "house_type",
    "grammar",
)

NOTES_SCHEMA_PATH = 'notes["domains"][domain][artifact]'

PATH_HEADER_RE = re.compile(r"^#\s+(.+\.py)\s*$")
FALLBACK_TOKEN_RE = re.compile(r"\bfallback\b", re.IGNORECASE)

REPORT_MODULE_PREFIXES = (
    "bvillage.core.report",
)

# STRUCT-001 should only trigger on grounded structural-emission patterns,
# not on comments, docstrings, TypedDict field names, or harmless prose.
STRUCTURAL_EMISSION_EVIDENCE_LABELS = (
    ("members = {", re.compile(r"\bmembers\s*=\s*\{")),
    ("members = dict(...)", re.compile(r"\bmembers\s*=\s*dict\s*\(")),
    ("members.append(...)", re.compile(r"\bmembers\.append\s*\(")),
    ("members.extend(...)", re.compile(r"\bmembers\.extend\s*\(")),
    ('"members": {...}', re.compile(r'["\']members["\']\s*:\s*\{')),
    ('"posts": ...', re.compile(r'["\']posts["\']\s*:\s*[\[{]')),
    ('"rails": ...', re.compile(r'["\']rails["\']\s*:\s*[\[{]')),
    ('"braces": ...', re.compile(r'["\']braces["\']\s*:\s*[\[{]')),
    ('"infills": ...', re.compile(r'["\']infills["\']\s*:\s*[\[{]')),
    ('"tid": "..."', re.compile(r'["\']tid["\']\s*:\s*["\'][^"\']+["\']')),
    ("Member(...)", re.compile(r"\bMember\s*\(")),
)

# Accepted signals that a domain file participates correctly in artifact
# production without directly spelling "members" in the current module.
FRAMEPLAN_DERIVATION_PATTERNS = (
    re.compile(r"\bderive_frameplan_[A-Za-z0-9_]+\s*\("),
    re.compile(r"\bset_domain_artifact\s*\("),
    re.compile(r'artifact\s*=\s*["\']frameplan["\']'),
)

ROOFPLAN_DERIVATION_PATTERNS = (
    re.compile(r"\bderive_roofplan_[A-Za-z0-9_]+\s*\("),
    re.compile(r"\bset_domain_artifact\s*\("),
    re.compile(r'artifact\s*=\s*["\']roofplan["\']'),
)

# Accepted renderer signals for artifact-driven geometry emission.
RENDER_ARTIFACT_PATTERNS = (
    re.compile(r"\bmembers\b"),
    re.compile(r"\broofplan\b"),
    re.compile(r"\bbuild_roof_from_plan\s*\("),
    re.compile(r"\bbuild_fachwerk_frame_from_structure_notes\s*\("),
    re.compile(r"\bget_domain_artifact\s*\("),
    re.compile(r'artifact\s*=\s*["\']frameplan["\']'),
    re.compile(r'artifact\s*=\s*["\']roofplan["\']'),
)

RENDER_INFERENCE_PATTERNS = (
    "axes_u",
    "axes_z",
    "vertical_axes",
    "compute_vertical_axes",
    "compute_z_axes",
    "wall_height",
    "infer",
)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class Violation:
    severity: str
    code: str
    file: str
    line: int
    message: str
    evidence: str = ""

    def sort_key(self) -> tuple[str, str, str, int, str]:
        sev_order = {"HARD": 0, "MEDIUM": 1, "LOW": 2}
        return (str(sev_order.get(self.severity, 9)), self.file, str(self.line), self.code, self.message)


@dataclass(slots=True)
class FileInfo:
    path: Path
    relpath: str
    layer: str
    module_name: str
    source: str
    tree: ast.AST | None
    imports: list[tuple[int, str]] = field(default_factory=list)
    import_froms: list[tuple[int, str]] = field(default_factory=list)
    function_defs: list[ast.FunctionDef | ast.AsyncFunctionDef] = field(default_factory=list)
    class_defs: list[ast.ClassDef] = field(default_factory=list)
    assign_strings: list[tuple[int, str]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def detect_layer(relpath: str) -> str:
    p = relpath.replace("\\", "/")
    if "/tests/" in f"/{p}/" or p.startswith("tests/"):
        return "tests"
    if p.startswith("bvillage/core/"):
        return "core"
    if p.startswith("bvillage/foreman/"):
        return "foreman"
    if p.startswith("bvillage/policies/"):
        return "policies"
    if p.startswith("bvillage/types/"):
        return "types"
    if p.startswith("bvillage/domains/") and "/blender/" in p:
        return "domain-blender"
    if p.startswith("bvillage/domains/"):
        return "domain-core"
    if p.startswith("bvillage/blender/"):
        return "blender-root"
    return "other"


def rel_to_module(relpath: str) -> str:
    no_suffix = relpath[:-3] if relpath.endswith(".py") else relpath
    parts = no_suffix.replace("\\", "/").split("/")
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def read_python_file(path: Path, root: Path) -> FileInfo | None:
    try:
        source = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        source = path.read_text(encoding="latin-1")

    relpath = path.relative_to(root).as_posix()
    layer = detect_layer(relpath)
    module_name = rel_to_module(relpath)

    try:
        tree = ast.parse(source, filename=relpath)
    except SyntaxError:
        return FileInfo(
            path=path,
            relpath=relpath,
            layer=layer,
            module_name=module_name,
            source=source,
            tree=None,
        )

    info = FileInfo(
        path=path,
        relpath=relpath,
        layer=layer,
        module_name=module_name,
        source=source,
        tree=tree,
    )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                info.imports.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if node.level > 0:
                mod = "." * node.level + mod
            info.import_froms.append((node.lineno, mod))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            info.function_defs.append(node)
        elif isinstance(node, ast.ClassDef):
            info.class_defs.append(node)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            lineno = getattr(node, "lineno", 0)
            info.assign_strings.append((lineno, node.value))

    return info


def iter_python_files(root: Path, include_tests: bool) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        parts = set(path.parts)
        if parts & DEFAULT_EXCLUDE_DIRS:
            continue
        rel = path.relative_to(root).as_posix()
        if not include_tests and (rel.startswith("tests/") or "/tests/" in rel):
            continue
        yield path


def first_line(text: str) -> str:
    return text.splitlines()[0] if text.splitlines() else ""


def has_arch_keyword(text: str) -> bool:
    low = text.lower()
    return any(k in low for k in CONCRETE_ARCH_KEYWORDS)


def is_relative_import(mod: str) -> bool:
    return mod.startswith(".")


def md_escape(text: str) -> str:
    return text.replace("|", "\\|")


def non_comment_lines(source: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for lineno, line in enumerate(source.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        out.append((lineno, line))
    return out


def source_without_comments_and_docstrings(source: str, tree: ast.AST | None) -> str:
    """
    Return source with comments and docstrings removed.

    WHY:
    Structural grammar checks must inspect executable / declarative code,
    not prose in comments or docstrings.
    """
    lines = source.splitlines()
    docstring_lines: set[int] = set()

    if tree is not None:
        for node in ast.walk(tree):
            body = getattr(node, "body", None)

            # Only module / class / function-like nodes with a statement list
            # can legally start with a docstring expression.
            if not isinstance(body, list) or not body:
                continue

            first = body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = getattr(first, "lineno", None)
                end = getattr(first, "end_lineno", start)
                if start is not None and end is not None:
                    docstring_lines.update(range(start, end + 1))

    token_lines: dict[int, list[str]] = {}
    try:
        tok_stream = tokenize.generate_tokens(io.StringIO(source).readline)
        for tok in tok_stream:
            tok_type = tok.type
            tok_str = tok.string
            start_line = tok.start[0]

            if start_line in docstring_lines:
                continue
            if tok_type == tokenize.COMMENT:
                continue
            if tok_type in {
                tokenize.STRING,
                tokenize.NL,
                tokenize.NEWLINE,
                tokenize.INDENT,
                tokenize.DEDENT,
                tokenize.ENDMARKER,
            }:
                continue

            token_lines.setdefault(start_line, []).append(tok_str)
    except tokenize.TokenError:
        # Fall back to a simple line-based removal if tokenization fails.
        cleaned_lines: list[str] = []
        for lineno, line in enumerate(lines, start=1):
            if lineno in docstring_lines:
                continue
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            cleaned_lines.append(line)
        return "\n".join(cleaned_lines)

    cleaned_lines = []
    for lineno in sorted(token_lines.keys()):
        cleaned_lines.append(" ".join(token_lines[lineno]))

    return "\n".join(cleaned_lines)


def detect_structural_emission(clean_source: str) -> list[str]:
    hits: list[str] = []
    for label, pattern in STRUCTURAL_EMISSION_EVIDENCE_LABELS:
        if pattern.search(clean_source):
            hits.append(label)
    return hits


def matches_any(clean_source: str, patterns: tuple[re.Pattern[str], ...]) -> bool:
    return any(p.search(clean_source) for p in patterns)


def collect_token_hits(clean_source: str, tokens: tuple[str, ...]) -> list[str]:
    hits: list[str] = []
    for tok in tokens:
        if tok in clean_source:
            hits.append(tok)
    return hits


# ---------------------------------------------------------------------------
# AST visitors
# ---------------------------------------------------------------------------

class CtxPolicyAccessVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.hits: list[tuple[int, str]] = []

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if isinstance(node.value, ast.Name) and node.value.id == "ctx" and node.attr in CTX_POLICY_FIELDS:
            self.hits.append((node.lineno, f"ctx.{node.attr}"))
        self.generic_visit(node)


class FrameplanMutationVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.hits: list[tuple[int, str]] = []

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr in {"append", "extend", "insert", "pop", "remove", "clear"}:
            root = func.value
            name = self._name_of(root)
            if name and any(x in name for x in ("frameplan", "members", "posts", "rails", "braces", "infills")):
                self.hits.append((node.lineno, f"{name}.{func.attr}(...)"))
        self.generic_visit(node)

    def _name_of(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            base = self._name_of(node.value)
            return f"{base}.{node.attr}" if base else node.attr
        if isinstance(node, ast.Subscript):
            base = self._name_of(node.value)
            return base
        return None


class NotesSchemaVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.structured_calls: list[int] = []
        self.flat_frameplan_lookups: list[tuple[int, str]] = []

    def visit_Call(self, node: ast.Call) -> None:
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        if func_name in {"get_domain_artifact", "set_domain_artifact"}:
            self.structured_calls.append(node.lineno)

        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        text = ast.unparse(node)
        if '["frameplan"]' in text or "['frameplan']" in text or '["fachwerk.frameplan"]' in text:
            self.flat_frameplan_lookups.append((node.lineno, text))
        self.generic_visit(node)


# ---------------------------------------------------------------------------
# Audit rules
# ---------------------------------------------------------------------------

def audit_syntax(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []
    for fi in files:
        if fi.tree is None:
            out.append(
                Violation(
                    severity="HARD",
                    code="PARSE-001",
                    file=fi.relpath,
                    line=1,
                    message="Python file cannot be parsed.",
                    evidence=first_line(fi.source),
                )
            )
    return out


def audit_path_headers(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []
    for fi in files:
        lines = fi.source.splitlines()
        if not lines:
            continue
        m = PATH_HEADER_RE.match(lines[0])
        if not m:
            out.append(
                Violation(
                    severity="LOW",
                    code="HDR-001",
                    file=fi.relpath,
                    line=1,
                    message="Missing canonical path header as first line.",
                    evidence=lines[0] if lines else "",
                )
            )
            continue
        header_path = m.group(1).strip()
        if header_path != fi.relpath:
            out.append(
                Violation(
                    severity="LOW",
                    code="HDR-002",
                    file=fi.relpath,
                    line=1,
                    message="Path header does not match repository path.",
                    evidence=f"header={header_path!r} actual={fi.relpath!r}",
                )
            )
    return out


def audit_filenames(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []
    for fi in files:
        name = fi.path.name
        if name == "__init__.py":
            continue
        if name in GENERIC_BAD_FILENAMES:
            out.append(
                Violation(
                    severity="LOW",
                    code="NAME-001",
                    file=fi.relpath,
                    line=1,
                    message="Generic filename violates naming policy.",
                    evidence=name,
                )
            )
            continue

        if fi.layer in {"core", "foreman", "types", "domain-core", "domain-blender", "policies"}:
            if not name.startswith(ROLE_PREFIXES):
                out.append(
                    Violation(
                        severity="LOW",
                        code="NAME-002",
                        file=fi.relpath,
                        line=1,
                        message="Filename does not follow <role>_<aspect>.py convention.",
                        evidence=name,
                    )
                )
    return out


def audit_import_layers(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []

    for fi in files:
        imports = fi.imports + fi.import_froms
        for lineno, mod in imports:
            if not mod or is_relative_import(mod):
                continue

            if fi.layer == "core":
                if mod.startswith("bvillage.domains") or mod.startswith("bvillage.types") or mod.startswith("bvillage.blender"):
                    out.append(
                        Violation(
                            severity="HARD",
                            code="LAYER-CORE-001",
                            file=fi.relpath,
                            line=lineno,
                            message="Core imports domain/type/blender code.",
                            evidence=mod,
                        )
                    )

            elif fi.layer == "domain-core":
                if mod.startswith("bvillage.types"):
                    out.append(
                        Violation(
                            severity="HARD",
                            code="LAYER-DOMAIN-001",
                            file=fi.relpath,
                            line=lineno,
                            message="Domain-core imports type code.",
                            evidence=mod,
                        )
                    )
                if mod == "bpy" or mod.startswith("bpy"):
                    out.append(
                        Violation(
                            severity="HARD",
                            code="LAYER-DOMAIN-002",
                            file=fi.relpath,
                            line=lineno,
                            message="Domain-core imports Blender.",
                            evidence=mod,
                        )
                    )

            elif fi.layer == "types":
                if mod == "bpy" or mod.startswith("bpy"):
                    out.append(
                        Violation(
                            severity="HARD",
                            code="LAYER-TYPE-001",
                            file=fi.relpath,
                            line=lineno,
                            message="Type layer imports Blender.",
                            evidence=mod,
                        )
                    )

    return out


def audit_core_arch_knowledge(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []
    for fi in files:
        if fi.layer != "core":
            continue

        for lineno, text in fi.assign_strings:
            if has_arch_keyword(text):
                out.append(
                    Violation(
                        severity="MEDIUM",
                        code="CORE-ARCH-001",
                        file=fi.relpath,
                        line=lineno,
                        message="Core contains concrete architectural keywords.",
                        evidence=text[:120],
                    )
                )

        for lineno, mod in fi.imports + fi.import_froms:
            if has_arch_keyword(mod):
                out.append(
                    Violation(
                        severity="HARD",
                        code="CORE-ARCH-002",
                        file=fi.relpath,
                        line=lineno,
                        message="Core references concrete architectural concepts in imports.",
                        evidence=mod,
                    )
                )

        for lineno, line in non_comment_lines(fi.source):
            if has_arch_keyword(line):
                out.append(
                    Violation(
                        severity="MEDIUM",
                        code="CORE-ARCH-003",
                        file=fi.relpath,
                        line=lineno,
                        message="Core source contains concrete building/domain knowledge.",
                        evidence=line.strip()[:120],
                    )
                )
                break

    return out


def audit_policy_leakage(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []

    for fi in files:
        if (
            fi.module_name == "bvillage.core.policy_stack"
            or fi.module_name.startswith("bvillage.policies")
            or fi.module_name.startswith("bvillage.domains.timber_frame.policies")
        ):
            continue
        if fi.module_name.startswith(REPORT_MODULE_PREFIXES):
            continue
        if fi.tree is None:
            continue

        visitor = CtxPolicyAccessVisitor()
        visitor.visit(fi.tree)

        for lineno, expr in visitor.hits:
            if fi.layer in {"core", "domain-core", "types"}:
                out.append(
                    Violation(
                        severity="HARD",
                        code="POL-001",
                        file=fi.relpath,
                        line=lineno,
                        message="Context policy field accessed outside policy resolution layer.",
                        evidence=expr,
                    )
                )

    return out


def audit_type_generates_structure(files: list[FileInfo]) -> list[Violation]:
    # Deprecated: folded into audit_structural_grammar().
    return []


def audit_renderer_fallbacks(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []

    for fi in files:
        if fi.layer not in {"domain-blender", "blender-root"}:
            continue

        clean = source_without_comments_and_docstrings(fi.source, fi.tree)
        low = clean.lower()

        if not matches_any(low, RENDER_ARTIFACT_PATTERNS):
            out.append(
                Violation(
                    severity="MEDIUM",
                    code="RENDER-001",
                    file=fi.relpath,
                    line=1,
                    message="Renderer does not obviously consume artifact-driven payload.",
                    evidence="members/roofplan/artifact access not found",
                )
            )

        for lineno, line in non_comment_lines(fi.source):
            if FALLBACK_TOKEN_RE.search(line):
                out.append(
                    Violation(
                        severity="HARD",
                        code="RENDER-002",
                        file=fi.relpath,
                        line=lineno,
                        message="Renderer contains fallback path.",
                        evidence=line.strip()[:120],
                    )
                )
                break

        axis_hits = collect_token_hits(low, ("axes_u", "axes_z", "vertical_axes"))
        if axis_hits:
            out.append(
                Violation(
                    severity="MEDIUM",
                    code="RENDER-003",
                    file=fi.relpath,
                    line=1,
                    message="Renderer references planning axes; verify no structural inference occurs.",
                    evidence=", ".join(axis_hits),
                )
            )

    return out


def audit_frameplan_mutation(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []
    for fi in files:
        if fi.relpath.startswith("tools/"):
            continue
        if fi.tree is None:
            continue
        if fi.layer in {"domain-core", "blender-root", "domain-blender"}:
            continue

        visitor = FrameplanMutationVisitor()
        visitor.visit(fi.tree)
        for lineno, expr in visitor.hits:
            out.append(
                Violation(
                    severity="HARD",
                    code="MUT-001",
                    file=fi.relpath,
                    line=lineno,
                    message="Non-domain layer mutates frameplan/member structures.",
                    evidence=expr,
                )
            )
    return out


def audit_notes_schema(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []
    for fi in files:
        if fi.tree is None:
            continue
        visitor = NotesSchemaVisitor()
        visitor.visit(fi.tree)

        for lineno, text in visitor.flat_frameplan_lookups:
            out.append(
                Violation(
                    severity="MEDIUM",
                    code="NOTE-001",
                    file=fi.relpath,
                    line=lineno,
                    message="Flat notes frameplan lookup found; structured notes schema preferred.",
                    evidence=text,
                )
            )
    return out


def audit_folder_structure(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []
    for fi in files:
        p = fi.relpath.replace("\\", "/")
        if fi.layer == "types" and "/blender/" in p:
            out.append(
                Violation(
                    severity="LOW",
                    code="FOLDER-001",
                    file=fi.relpath,
                    line=1,
                    message="Type path contains blender subtree; likely wrong architectural layer.",
                    evidence=p,
                )
            )
        if fi.layer == "core" and fi.path.name.startswith("schema_"):
            if "/contracts/" not in p:
                out.append(
                    Violation(
                        severity="LOW",
                        code="FOLDER-002",
                        file=fi.relpath,
                        line=1,
                        message="Core schema file not located in contracts-oriented subtree.",
                        evidence=p,
                    )
                )
    return out


def audit_plugin_registration(files: list[FileInfo]) -> list[Violation]:
    out: list[Violation] = []
    for fi in files:
        if fi.layer != "types":
            continue
        if fi.path.name != "__init__.py":
            continue
        low = fi.source.lower()
        if "register" not in low:
            out.append(
                Violation(
                    severity="MEDIUM",
                    code="PLUGIN-001",
                    file=fi.relpath,
                    line=1,
                    message="Type package __init__.py does not appear to register plugin/provider.",
                    evidence="register not found",
                )
            )
    return out


def audit_structural_grammar(files: list[FileInfo]) -> list[Violation]:
    """
    Verify BVILLAGE structural grammar boundaries.

    Architecture rules
    ------------------
    Type layer:
        must NOT generate structural members

    Domain layer:
        should generate FramePlan / RoofPlan artifacts

    Renderer:
        should consume artifacts rather than infer structure
    """
    out: list[Violation] = []

    for fi in files:
        if fi.tree is None:
            continue

        clean = source_without_comments_and_docstrings(fi.source, fi.tree)
        low = clean.lower()

        if fi.layer == "types":
            hits = detect_structural_emission(low)
            if hits:
                out.append(
                    Violation(
                        severity="HARD",
                        code="STRUCT-001",
                        file=fi.relpath,
                        line=1,
                        message="Type layer generates structural members.",
                        evidence=", ".join(hits[:4]),
                    )
                )

        if fi.layer == "domain-core":
            mentions_frameplan = "frameplan" in low
            mentions_roofplan = "roofplan" in low
            has_members = "members" in low

            accepted_frameplan = matches_any(low, FRAMEPLAN_DERIVATION_PATTERNS)
            accepted_roofplan = matches_any(low, ROOFPLAN_DERIVATION_PATTERNS)

            if mentions_frameplan and not has_members and not accepted_frameplan:
                out.append(
                    Violation(
                        severity="MEDIUM",
                        code="STRUCT-002",
                        file=fi.relpath,
                        line=1,
                        message="Domain layer does not obviously generate FramePlan members or delegate to a Frame Producer.",
                        evidence="frameplan found without members/derive_frameplan/set_domain_artifact(frameplan)",
                    )
                )

            if mentions_roofplan and not accepted_roofplan:
                out.append(
                    Violation(
                        severity="MEDIUM",
                        code="STRUCT-004",
                        file=fi.relpath,
                        line=1,
                        message="Domain layer does not obviously generate RoofPlan or delegate to a Roof Producer.",
                        evidence="roofplan found without derive_roofplan/set_domain_artifact(roofplan)",
                    )
                )

        if fi.layer in {"domain-blender", "blender-root"}:
            hits = collect_token_hits(low, RENDER_INFERENCE_PATTERNS)
            if hits:
                out.append(
                    Violation(
                        severity="MEDIUM",
                        code="STRUCT-003",
                        file=fi.relpath,
                        line=1,
                        message="Renderer may infer structure instead of consuming artifact-driven plans.",
                        evidence=", ".join(hits[:3]),
                    )
                )

    return out


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def summarize(files: list[FileInfo], violations: list[Violation]) -> str:
    by_sev: dict[str, int] = {"HARD": 0, "MEDIUM": 0, "LOW": 0}
    for v in violations:
        by_sev[v.severity] = by_sev.get(v.severity, 0) + 1

    layers: dict[str, int] = {}
    for fi in files:
        layers[fi.layer] = layers.get(fi.layer, 0) + 1

    lines: list[str] = []
    lines.append("# Architecture Audit")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- Python files scanned: **{len(files)}**")
    lines.append(f"- HARD violations: **{by_sev['HARD']}**")
    lines.append(f"- MEDIUM violations: **{by_sev['MEDIUM']}**")
    lines.append(f"- LOW violations: **{by_sev['LOW']}**")
    lines.append("")
    lines.append("## Layer distribution")
    lines.append("")
    lines.append("| Layer | Files |")
    lines.append("|---|---:|")
    for layer in sorted(layers):
        lines.append(f"| {md_escape(layer)} | {layers[layer]} |")
    lines.append("")

    if not violations:
        lines.append("## Result")
        lines.append("")
        lines.append("No violations found.")
        lines.append("")
        return "\n".join(lines)

    lines.append("## Findings")
    lines.append("")
    lines.append("| Severity | Code | File | Line | Message | Evidence |")
    lines.append("|---|---|---|---:|---|---|")
    for v in sorted(violations, key=lambda x: x.sort_key()):
        lines.append(
            f"| {v.severity} | {v.code} | {md_escape(v.file)} | {v.line} | "
            f"{md_escape(v.message)} | {md_escape(v.evidence[:120])} |"
        )
    lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("- **HARD**: architecture violation; should block stabilization completion")
    lines.append("- **MEDIUM**: likely migration target or design weakness")
    lines.append("- **LOW**: naming / folder / path hygiene")
    lines.append("")
    lines.append("## Audit intent")
    lines.append("")
    lines.append(
        "This report is static and conservative. It flags grounded structural risks. "
        "Every finding still needs human review before refactoring."
    )
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="BVILLAGE architecture audit")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--out", default="generated/architecture_audit.md", help="Markdown report output path")
    parser.add_argument("--include-tests", action="store_true", help="Include tests/ in scan")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = root / out_path

    files: list[FileInfo] = []
    for py in sorted(iter_python_files(root, include_tests=args.include_tests)):
        info = read_python_file(py, root)
        if info is not None:
            files.append(info)

    violations: list[Violation] = []
    violations.extend(audit_syntax(files))
    violations.extend(audit_path_headers(files))
    violations.extend(audit_filenames(files))
    violations.extend(audit_import_layers(files))
    violations.extend(audit_core_arch_knowledge(files))
    violations.extend(audit_policy_leakage(files))
    violations.extend(audit_type_generates_structure(files))
    violations.extend(audit_renderer_fallbacks(files))
    violations.extend(audit_frameplan_mutation(files))
    violations.extend(audit_notes_schema(files))
    violations.extend(audit_folder_structure(files))
    violations.extend(audit_plugin_registration(files))
    violations.extend(audit_structural_grammar(files))

    report = summarize(files, violations)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")

    print(f"[OK] wrote audit report: {out_path}")
    print(
        f"[INFO] files={len(files)} "
        f"hard={sum(v.severity == 'HARD' for v in violations)} "
        f"medium={sum(v.severity == 'MEDIUM' for v in violations)} "
        f"low={sum(v.severity == 'LOW' for v in violations)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
