# tests/test_registry.py

"""
tests.test_registry
===================

Registry discovery smoke tests.

Goals
-----
- discovery runs without errors
- hallenhaus type registers
- discover_types() is idempotent
"""

from __future__ import annotations

from bvillage.core.registry import discover_types, get_house_type, list_house_types


def test_discover_types_registers_hallenhaus():
    discover_types(force=True)
    provider = get_house_type("fachwerkhaus.hallenhaus")
    assert provider.type_id == "fachwerkhaus.hallenhaus"


def test_discovery_idempotent_and_listable():
    discover_types(force=True)
    a = list_house_types()
    discover_types(force=False)
    b = list_house_types()
    assert a == b
    assert "fachwerkhaus.hallenhaus" in a
