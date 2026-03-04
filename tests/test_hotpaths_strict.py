"""
Strict hot path audit for @hot functions.

Rules (strict):
- no IO (print/logging)
- no dynamic runtime typing (isinstance)
- no exception control-flow (try/except)
- avoid hidden allocations (comprehensions, generator expressions)
- avoid explicit allocation-heavy builtins (list/dict/set/tuple, sorted)
- no RNG / time inside hot paths

Allowlist exists for carefully justified exceptions.
"""

from __future__ import annotations

import ast
import inspect
from dataclasses import dataclass

import pytest

from bvillage.core.hot_path import collect_hot_functions_in_package


# Automatically collect all @hot functions in bvillage.core
HOT_FUNCS = collect_hot_functions_in_package(
    "bvillage.core",
    fail_on_import_error=True,  # set False if some core modules can't be imported in CI
)


def test_at_least_one_hot_function_found():
    assert HOT_FUNCS, "No @hot functions detected"


@dataclass(frozen=True)
class Violation:
    code: str
    message: str


# --- policy knobs ------------------------------------------------------------

# Builtins / calls that strongly imply allocations or heavy work
BANNED_BUILTIN_CALLS = {
    "print",
    "isinstance",
    "sorted",
    "list",
    "dict",
    "set",
    "tuple",
}

# Module roots that should not be used from strict hot paths
# (bans `random.Random(...)` and `random.*`, and `time.*`)
BANNED_MODULE_ROOTS = {
    "logging",
    "random",
    "time",
}

# Per-function allowlist for specific calls/attributes, identified as "qualname".
# Examples:
#   - "hashlib.blake2b"
#   - "math.fsum"
ALLOW_CALLS_BY_FUNC: dict[str, set[str]] = {
    # constraints._stable_u32 uses hashlib.blake2b for stable hashing
    "_stable_u32": {"hashlib.blake2b"},
}


# --- AST helpers -------------------------------------------------------------

def _qualname_from_call(node: ast.Call) -> str | None:
    """
    Return a dotted qualname for a call, if it is a simple Name or Attribute chain.
    Examples:
      print(...)              -> "print"
      logging.info(...)       -> "logging.info"
      random.Random(...)      -> "random.Random"
      hashlib.blake2b(...)    -> "hashlib.blake2b"
    """
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


def _audit_hot_function(fn) -> list[Violation]:
    src = inspect.getsource(fn)
    tree = ast.parse(src)

    allow = ALLOW_CALLS_BY_FUNC.get(fn.__name__, set())
    violations: list[Violation] = []

    for node in ast.walk(tree):

        # Ban try/except (exception-driven control flow)
        if isinstance(node, ast.Try):
            violations.append(
                Violation(
                    "TRY",
                    f"{fn.__name__}:{_lineno(node)} uses try/except in @hot function",
                )
            )

        # Ban comprehensions + generator expressions (hidden allocations / overhead)
        if isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
            violations.append(
                Violation(
                    "COMP",
                    f"{fn.__name__}:{_lineno(node)} uses comprehension/generator in @hot function",
                )
            )

        # Calls
        if isinstance(node, ast.Call):
            qn = _qualname_from_call(node)
            if not qn:
                continue

            # Allowlist exceptions
            if qn in allow:
                continue

            # Banned builtins
            if qn in BANNED_BUILTIN_CALLS:
                violations.append(
                    Violation(
                        "CALL",
                        f"{fn.__name__}:{_lineno(node)} calls banned builtin {qn}(...)",
                    )
                )
                continue

            # Banned modules (logging.*, random.*, time.*)
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


def test_hot_paths_strict_have_no_forbidden_ops():
    all_violations: list[Violation] = []

    for fn in HOT_FUNCS:
        all_violations.extend(_audit_hot_function(fn))

    if all_violations:
        msg = "\n".join(f"[{v.code}] {v.message}" for v in all_violations)
        pytest.fail("Strict hot path violations:\n" + msg)
