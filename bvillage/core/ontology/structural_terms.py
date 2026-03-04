# bvillage/core/ontology/structural_terms.py
"""
BVILLAGE Structural Ontology

Stable runtime identifiers (TIDs) for structural members.

Rules
- TIDs are immutable once introduced.
- First segment defines structural class (post/beam/brace/infill/...).
- Used by builder, contract and policy systems.

Compatibility
- Provide alias constants for short names used across the codebase
  (e.g. POST_JAMB) to avoid widespread import churn.
"""

from __future__ import annotations

from typing import Final, FrozenSet, Mapping, Optional

# -------------------------------------------------------------
# Structural classes
# -------------------------------------------------------------

CLASS_POST: Final[str] = "post"
CLASS_BEAM: Final[str] = "beam"
CLASS_BRACE: Final[str] = "brace"
CLASS_INFILL: Final[str] = "infill"

STRUCTURAL_CLASSES: Final[FrozenSet[str]] = frozenset(
    {CLASS_POST, CLASS_BEAM, CLASS_BRACE, CLASS_INFILL}
)

# -------------------------------------------------------------
# Canonical TIDs
# -------------------------------------------------------------

# Posts
POST_PRIMARY: Final[str] = "post.primary"
POST_OPENING_JAMB: Final[str] = "post.opening_jamb"
POST_INTERIOR: Final[str] = "post.interior"

# Beams
BEAM_EAVES_PLATE: Final[str] = "beam.eaves_plate"
BEAM_OPENING_LINTEL: Final[str] = "beam.opening_lintel"
BEAM_OPENING_SILL: Final[str] = "beam.opening_sill"

# Braces
BRACE_DIAGONAL: Final[str] = "brace.diagonal"

# Infills
INFILL_CELL: Final[str] = "infill.cell"

# -------------------------------------------------------------
# Aliases (API stability across modules)
# -------------------------------------------------------------
# These are *names* compatibility; the values are canonical TIDs.

POST_JAMB: Final[str] = POST_OPENING_JAMB

BEAM_LINTEL: Final[str] = BEAM_OPENING_LINTEL
BEAM_WINDOW_SILL: Final[str] = BEAM_OPENING_SILL

# (optional convenience alias; keep if already used elsewhere)
BEAM_SILL: Final[str] = BEAM_OPENING_SILL

# -------------------------------------------------------------
# Registry
# -------------------------------------------------------------

VALID_TIDS: Final[FrozenSet[str]] = frozenset(
    {
        POST_PRIMARY,
        POST_OPENING_JAMB,
        POST_INTERIOR,
        BEAM_EAVES_PLATE,
        BEAM_OPENING_LINTEL,
        BEAM_OPENING_SILL,
        BRACE_DIAGONAL,
        INFILL_CELL,
    }
)

TID_CLASS: Final[Mapping[str, str]] = {
    POST_PRIMARY: CLASS_POST,
    POST_OPENING_JAMB: CLASS_POST,
    POST_INTERIOR: CLASS_POST,

    BEAM_EAVES_PLATE: CLASS_BEAM,
    BEAM_OPENING_LINTEL: CLASS_BEAM,
    BEAM_OPENING_SILL: CLASS_BEAM,

    BRACE_DIAGONAL: CLASS_BRACE,

    INFILL_CELL: CLASS_INFILL,
}


# -------------------------------------------------------------
# Helpers
# -------------------------------------------------------------

def tid_class(tid: object) -> Optional[str]:
    if not isinstance(tid, str) or not tid:
        return None
    return TID_CLASS.get(tid)


def validate_tid(tid: object) -> bool:
    return isinstance(tid, str) and tid in VALID_TIDS


def is_post(tid: object) -> bool:
    return tid_class(tid) == CLASS_POST


def is_beam(tid: object) -> bool:
    return tid_class(tid) == CLASS_BEAM


def is_brace(tid: object) -> bool:
    return tid_class(tid) == CLASS_BRACE


def is_infill(tid: object) -> bool:
    return tid_class(tid) == CLASS_INFILL


__all__ = [
    # classes
    "CLASS_POST", "CLASS_BEAM", "CLASS_BRACE", "CLASS_INFILL", "STRUCTURAL_CLASSES",
    # canonical tids
    "POST_PRIMARY", "POST_OPENING_JAMB", "POST_INTERIOR",
    "BEAM_EAVES_PLATE", "BEAM_OPENING_LINTEL", "BEAM_OPENING_SILL",
    "BRACE_DIAGONAL",
    "INFILL_CELL",
    # aliases
    "POST_JAMB",
    "BEAM_LINTEL",
    "BEAM_WINDOW_SILL",
    "BEAM_SILL",
    # registry/helpers
    "VALID_TIDS",
    "TID_CLASS",
    "tid_class",
    "validate_tid",
    "is_post",
    "is_beam",
    "is_brace",
    "is_infill",
]
