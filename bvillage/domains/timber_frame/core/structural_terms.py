# bvillage/domains/timber_frame/core/structural_terms.py

"""
Fachwerk Structural Terms (frozen ontology)

Purpose
- Provide stable, explicit term IDs (TIDs) for structural members.
- Decouple FramePlan semantics from ad-hoc role strings.
- Guarantee long-term naming stability across archetypes and policies.

Rules
- TIDs are stable once introduced (never rename, never delete).
- New semantics => new TID.
- YAML term docs (timber_frame_terms.v2.yaml) are *research*, not runtime authority.

Member contract
- Every structural member dict MUST have:
    - tid: str  (one of VALID_TIDS)
- Additional selector fields are allowed and sometimes required:
    - side: "L"|"R" (for opening jambs)
    - floor: int (future SYS-003)
    - span_kind, joinery_hint, etc. (future)
"""

from __future__ import annotations

from typing import Final, Literal

__all__ = [
    # Core sets
    "VALID_TIDS",
    "TidKind",
    "tid_kind",
    # Post TIDs
    "POST_PRIMARY",
    "POST_JAMB",
    "POST_INTERIOR_HALL",
    # Rail/beam TIDs
    "BEAM_EAVES_PLATE",
    "BEAM_LINTEL",
    "BEAM_WINDOW_SILL",
    # Brace TIDs
    "BRACE_DIAGONAL",
    # Infill TIDs
    "INFILL_CELL",
    # Helpers
    "JambSide",
]

TidKind = Literal["post", "rail", "brace", "infill", "other"]
JambSide = Literal["L", "R"]

# ---------------------------
# Posts
# ---------------------------

POST_PRIMARY: Final[str] = "post.primary"
POST_JAMB: Final[str] = "post.opening_jamb"
POST_INTERIOR_HALL: Final[str] = "post.interior_hall"

# ---------------------------
# Rails / Beams
# ---------------------------

BEAM_EAVES_PLATE: Final[str] = "beam.eaves_plate"
BEAM_LINTEL: Final[str] = "beam.opening_lintel"
BEAM_WINDOW_SILL: Final[str] = "beam.opening_sill"

# ---------------------------
# Braces
# ---------------------------

BRACE_DIAGONAL: Final[str] = "brace.diagonal"

# ---------------------------
# Infills
# ---------------------------

INFILL_CELL: Final[str] = "infill.cell"

# ---------------------------
# Registry
# ---------------------------

VALID_TIDS: Final[set[str]] = {
    # posts
    POST_PRIMARY,
    POST_JAMB,
    POST_INTERIOR_HALL,
    # rails/beams
    BEAM_EAVES_PLATE,
    BEAM_LINTEL,
    BEAM_WINDOW_SILL,
    # braces
    BRACE_DIAGONAL,
    # infills
    INFILL_CELL,
}


def tid_kind(tid: str) -> TidKind:
    """Fast kind classifier for validators/builders."""
    if tid.startswith("post."):
        return "post"
    if tid.startswith("beam.") or tid.startswith("rail."):
        return "rail"
    if tid.startswith("brace."):
        return "brace"
    if tid.startswith("infill."):
        return "infill"
    return "other"
