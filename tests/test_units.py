# tests/test_units.py

"""
tests.test_units
================

Unit conversion/formatting tests.
"""

from __future__ import annotations

from bvillage.core.units import to_m, from_m, fmt_m, parse_length, approx_equal


def test_to_m_and_from_m_roundtrip():
    assert approx_equal(to_m(1000, "mm"), 1.0)
    assert approx_equal(to_m(100, "cm"), 1.0)
    assert approx_equal(to_m(1, "m"), 1.0)

    assert approx_equal(from_m(1.0, "mm"), 1000.0)
    assert approx_equal(from_m(1.0, "cm"), 100.0)
    assert approx_equal(from_m(1.0, "m"), 1.0)


def test_fmt_m_defaults():
    assert fmt_m(2.58) == "2.580 m"
    assert fmt_m(0.261, unit="mm", prec=0) == "261 mm"
    assert fmt_m(0.261, unit="cm", prec=1) == "26.1 cm"


def test_parse_length():
    assert approx_equal(parse_length("2.58m"), 2.58)
    assert approx_equal(parse_length("2.58 m"), 2.58)
    assert approx_equal(parse_length("261mm"), 0.261)
    assert approx_equal(parse_length("261 mm"), 0.261)
    assert approx_equal(parse_length("19.9 cm"), 0.199)
