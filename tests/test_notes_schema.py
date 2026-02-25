# tests/test_notes_schema.py

"""
tests.test_notes_schema
=======================

Tests for standardized notes schema + legacy alias compatibility.
"""

from __future__ import annotations

from bvillage.core.notes import ensure_domains, set_domain_artifact, get_domain_artifact


def test_notes_schema_set_and_get_with_legacy_aliases():
    notes = {}

    payload = {"hello": "world", "n": 1}
    set_domain_artifact(
        notes,
        domain="fachwerk",
        name="frameplan",
        payload=payload,
        legacy_aliases=("frameplan", "fachwerk.frameplan"),
    )

    # canonical schema exists
    domains = ensure_domains(notes)
    assert "fachwerk" in domains
    assert domains["fachwerk"]["frameplan"] == payload

    # legacy aliases exist
    assert notes["frameplan"] == payload
    assert notes["fachwerk.frameplan"] == payload

    # get prefers canonical, but legacy fallback works too
    got = get_domain_artifact(
        notes,
        domain="fachwerk",
        name="frameplan",
        legacy_aliases=("frameplan", "fachwerk.frameplan"),
    )
    assert got == payload


def test_notes_schema_get_returns_none_when_missing():
    notes = {}
    got = get_domain_artifact(
        notes,
        domain="fachwerk",
        name="frameplan",
        legacy_aliases=("frameplan", "fachwerk.frameplan"),
    )
    assert got is None
