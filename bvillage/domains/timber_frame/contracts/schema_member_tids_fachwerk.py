# bvillage/domains/fachwerk/core/schema_member_tids_fachwerk.py

from __future__ import annotations

from typing import Tuple

from bvillage.core.ontology import structural_terms as tids

ALLOWED_POST_TIDS: Tuple[str, ...] = (
    tids.POST_PRIMARY,
    tids.POST_HALL,
)

ALLOWED_RAIL_TIDS: Tuple[str, ...] = (
    tids.BEAM_EAVES_PLATE,
    tids.BEAM_HALL_PLATE,
    tids.BEAM_TIE,
)

ALLOWED_BRACE_TIDS: Tuple[str, ...] = (
    getattr(tids, "BRACE_KNEE", "brace.knee"),
    getattr(tids, "BRACE_DIAGONAL", "brace.diagonal"),
)

__all__ = [
    "ALLOWED_POST_TIDS",
    "ALLOWED_RAIL_TIDS",
    "ALLOWED_BRACE_TIDS",
]
