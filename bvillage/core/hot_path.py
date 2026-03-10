# bvillage/core/hot_path.py

from __future__ import annotations

import inspect
import importlib
import pkgutil
from types import ModuleType
from typing import Iterable, Callable


def hot(func: Callable) -> Callable:
    func.__bv_hot__ = True
    return func


def hot_api(func: Callable) -> Callable:
    func.__bv_hot_api__ = True
    return func


def is_hot(func: Callable) -> bool:
    return getattr(func, "__bv_hot__", False) is True


def is_hot_api(func: Callable) -> bool:
    return getattr(func, "__bv_hot_api__", False) is True


def collect_hot_functions(modules: Iterable[ModuleType]) -> list[Callable]:
    out: list[Callable] = []
    for module in modules:
        for _, obj in inspect.getmembers(module):
            if callable(obj) and is_hot(obj):
                out.append(obj)
    return out


def collect_hot_api_functions(modules: Iterable[ModuleType]) -> list[Callable]:
    out: list[Callable] = []
    for module in modules:
        for _, obj in inspect.getmembers(module):
            if callable(obj) and is_hot_api(obj):
                out.append(obj)
    return out


def _import_all_modules_in_package(
    package_name: str,
    *,
    fail_on_import_error: bool,
) -> list[ModuleType]:
    pkg = importlib.import_module(package_name)
    modules: list[ModuleType] = [pkg]

    if hasattr(pkg, "__path__"):
        for modinfo in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
            name = modinfo.name
            try:
                modules.append(importlib.import_module(name))
            except Exception:
                if fail_on_import_error:
                    raise
                # else: skip modules that can't be imported in this env
                continue

    return modules


def collect_hot_functions_in_package(
    package_name: str,
    *,
    fail_on_import_error: bool = True,
) -> list[Callable]:
    modules = _import_all_modules_in_package(package_name, fail_on_import_error=fail_on_import_error)
    return collect_hot_functions(modules)


def collect_hot_api_functions_in_package(
    package_name: str,
    *,
    fail_on_import_error: bool = True,
) -> list[Callable]:
    modules = _import_all_modules_in_package(package_name, fail_on_import_error=fail_on_import_error)
    return collect_hot_api_functions(modules)
