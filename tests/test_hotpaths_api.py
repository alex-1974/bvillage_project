"""
API hot path audit for @hot_api functions.

Rules (API-hot):
- no IO (print/logging)
- no RNG (random.* / Random)
- no time usage (time.*)

Unlike strict hot paths, @hot_api functions may:
- allocate (dict/list/tuple)
- use comprehensions
- raise exceptions
- contain complex control flow

The goal is to prevent accidental debugging / nondeterminism in frequently-called code.
"""

from __future__ import annotations

import ast
import inspect
from dataclasses import dataclass

import pytest

from bvillage.core.hot_path import collect_hot_api_functions_in_package


# Automatically collect all @hot_api functions in bvillage.core
HOT_API_FUNCS = collect_hot_api_functions_in_package(
    "bvillage.core",
    fail_on_import_error=True,  # set False if some core modules can't be imported in CI
)


def test_at_least_one_hot_api_function_found():
    # If you want this optional (not required yet), change to:
    # if not HOT_API_FUNCS: pytest.skip("No @hot_api functions detected")
    assert HOT_API_FUNCS, "No @hot_api functions detected"


@dataclass(frozen=True)
class Violation:
    code: str
    message: str


# --- policy knobs ------------------------------------------------------------

BANNED_BUILTIN_CALLS = {
    "print",
}

BANNED_MODULE_ROOTS = {
    "logging",
    "random",
    "time",
}

# Per-function allowlist for specific calls/attributes, identified as "qualname".
ALLOW_CALLS_BY_FUNC: dict[str, set[str]] = {}


# --- AST helpers -------------------------------------------------------------

def _qualname_from_call(node: ast.Call) -> str | None:
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        parts: list[str] = []
        while isinstance(f, ast.Attribute):
            parts.append(f.attr)
            f = f.value
        if isinstance(f, ast.Name):
            parts.append(f.id)
            return ".".join(reversed(parts))
    return None


def _lineno(node: ast.AST) -> int:
    return int(getattr(node, "lineno", 0) or 0)


def _audit_hot_api_function(fn) -> list[Violation]:
    src = inspect.getsource(fn)
    tree = ast.parse(src)

    allow = ALLOW_CALLS_BY_FUNC.get(fn.__name__, set())
    violations: list[Violation] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            qn = _qualname_from_call(node)
            if not qn:
                continue

            if qn in allow:
                continue

            # banned builtin calls (print)
            if qn in BANNED_BUILTIN_CALLS:
                violations.append(
                    Violation(
                        "CALL",
                        f"{fn.__name__}:{_lineno(node)} calls banned builtin {qn}(...)",
                    )
                )
                continue

            # banned modules (logging.*, random.*, time.*)
            root = qn.split(".", 1)[0]
            if root in BANNED_MODULE_ROOTS:
                violations.append(
                    Violation(
                        "MOD",
                        f"{fn.__name__}:{_lineno(node)} calls banned module {qn}(...)",
                    )
                )
                continue

    return violations


def test_hot_paths_api_have_no_io_rng_time():
    all_violations: list[Violation] = []

    for fn in HOT_API_FUNCS:
        all_violations.extend(_audit_hot_api_function(fn))

    if all_violations:
        msg = "\n".join(f"[{v.code}] {v.message}" for v in all_violations)
        pytest.fail("API hot path violations:\n" + msg)
