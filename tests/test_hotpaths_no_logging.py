# tests/test_hotpaths_no_logging.py

from __future__ import annotations

import ast
import inspect

from bvillage.core.materials.material_registry import resolve_for_builder
from bvillage.core.constraints import sample_soft, penalty_soft, eval_range


HOT_PATH_FUNCS = (
    resolve_for_builder,
    sample_soft,
    penalty_soft,
    eval_range,
)

FORBIDDEN_NAMES = {"print", "breakpoint"}
FORBIDDEN_ATTR_ROOTS = {"logging", "LOG", "logger", "log"}


def _attr_root(node: ast.AST) -> str | None:
    # returns root name for calls like LOG.warning(...), logging.info(...), logger.debug(...)
    if isinstance(node, ast.Attribute):
        cur = node
        while isinstance(cur, ast.Attribute):
            cur = cur.value
        if isinstance(cur, ast.Name):
            return cur.id
    return None


def test_hotpaths_do_not_print_or_log():
    for fn in HOT_PATH_FUNCS:
        src = inspect.getsource(fn)
        tree = ast.parse(src)

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            # print(...)
            if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_NAMES:
                raise AssertionError(f"{fn.__module__}.{fn.__name__}: forbidden {node.func.id}()")

            # LOG.warning(...), logging.info(...)
            root = _attr_root(node.func)
            if root in FORBIDDEN_ATTR_ROOTS:
                raise AssertionError(f"{fn.__module__}.{fn.__name__}: forbidden logging via {root}.*()")
