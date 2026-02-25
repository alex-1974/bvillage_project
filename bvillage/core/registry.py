# bvillage/core/registry.py

"""
bvillage.core.registry
======================

Purpose
-------
Central registry for house type providers + deterministic discovery.

Key idea
--------
House types are plugins. Each plugin registers itself at import time:

    from bvillage.core.registry import register_house_type
    register_house_type(provider, origin=__name__)

Discovery loads those plugins by importing packages under `bvillage.types`.

Public API
----------
- register_house_type(provider, origin) -> None
- discover_types(force=False) -> None
- get_house_type(type_id) -> provider
- list_house_types() -> list[str]

Contracts
---------
HouseTypeProvider must provide:
- type_id: str
- generate(ctx) -> (structure, interior, openings)

Design choices
--------------
- Discovery is explicit and idempotent.
- Registry is process-local (no files).
- Failures are reported with actionable errors (which module failed, etc.).
"""

from __future__ import annotations

import importlib
import pkgutil
import threading
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Protocol, runtime_checkable


# ============================================================
# Provider Protocol + Errors
# ============================================================

@runtime_checkable
class HouseTypeProvider(Protocol):
    type_id: str

    def generate(self, ctx: Any):
        ...


class UnknownHouseTypeError(KeyError):
    pass


class RegistryConflictError(RuntimeError):
    pass


class DiscoveryError(RuntimeError):
    pass


# ============================================================
# Registry Storage (process-local)
# ============================================================

_lock = threading.RLock()
_registry: Dict[str, HouseTypeProvider] = {}
_origins: Dict[str, str] = {}
_discovered: bool = False


def register_house_type(provider: HouseTypeProvider, *, origin: str) -> None:
    """
    Register a house type provider.

    Parameters
    ----------
    provider:
        Object implementing HouseTypeProvider protocol.
    origin:
        Module name where this provider was registered from (use __name__).

    Raises
    ------
    RegistryConflictError
        If the same type_id is registered by a different origin.
    """
    if not isinstance(getattr(provider, "type_id", None), str) or not provider.type_id:
        raise ValueError("provider.type_id must be a non-empty str")

    type_id = provider.type_id

    with _lock:
        if type_id in _registry:
            prev_origin = _origins.get(type_id, "<unknown>")
            if prev_origin != origin:
                raise RegistryConflictError(
                    f"House type_id {type_id!r} already registered by {prev_origin!r}, "
                    f"cannot re-register from {origin!r}."
                )
            # same origin re-register -> ignore (idempotent import behavior)
            return

        _registry[type_id] = provider
        _origins[type_id] = origin


def get_house_type(type_id: str) -> HouseTypeProvider:
    """
    Retrieve a provider by type_id.

    Calls discover_types() lazily on first use (safe).
    """
    if not isinstance(type_id, str) or not type_id:
        raise ValueError("type_id must be a non-empty str")

    discover_types()

    with _lock:
        try:
            return _registry[type_id]
        except KeyError as exc:
            available = ", ".join(sorted(_registry.keys())) or "<none>"
            raise UnknownHouseTypeError(
                f"Unknown house type {type_id!r}. Available: {available}"
            ) from exc


def list_house_types() -> List[str]:
    """Return sorted list of registered type_ids."""
    discover_types()
    with _lock:
        return sorted(_registry.keys())


# ============================================================
# Discovery
# ============================================================

def discover_types(*, force: bool = False) -> None:
    """
    Discover and import all type packages under `bvillage.types`.

    Parameters
    ----------
    force:
        If True, runs discovery again (useful in Blender reload loops).
        Note: already-imported modules remain imported; registration is idempotent.

    Behavior
    --------
    Imports all packages recursively beneath `bvillage.types`.
    Each package may register providers during import.

    Raises
    ------
    DiscoveryError
        If importing a type package fails.
    """
    global _discovered

    with _lock:
        if _discovered and not force:
            return
        _discovered = True

    _import_all_subpackages("bvillage.types")


def _import_all_subpackages(root_pkg: str) -> None:
    """
    Recursively import all subpackages beneath root_pkg.

    Strategy
    --------
    - Import root package
    - Walk packages using pkgutil
    - Import only packages (not plain modules), because registration is expected
      from package __init__.py in our plugin architecture.

    If you later want module-level plugins, expand here.
    """
    try:
        root = importlib.import_module(root_pkg)
    except Exception as exc:
        raise DiscoveryError(f"Failed to import root package {root_pkg!r}: {exc}") from exc

    if not hasattr(root, "__path__"):
        # root is not a package; nothing to do
        return

    # pkgutil.walk_packages yields (module_finder, name, ispkg)
    for _, modname, ispkg in pkgutil.walk_packages(root.__path__, prefix=f"{root_pkg}."):
        if not ispkg:
            continue
        try:
            importlib.import_module(modname)
        except Exception as exc:
            raise DiscoveryError(f"Failed to import type package {modname!r}: {exc}") from exc
