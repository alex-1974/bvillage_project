# bvillage/core/ontology/structural_terms.py
"""
BVILLAGE Structural Ontology (runtime)

Stable term identifiers (TIDs) for structural elements used across BVILLAGE.

Design goals
- Domain-neutral: works for timber frame, masonry, log, hybrid, etc.
- Stable ABI: TIDs are part of the FramePlan contract surface.
- No YAML runtime dependency: research ontologies may evolve independently.

Conventions
- TIDs are lowercase, dot-separated: "post.primary", "beam.lintel", ...
- Orientation, side, placement, wall, and geometry live in member attributes
  (e.g. wall="N", side="L") rather than exploding the TID space.
"""

from __future__ import annotations

from typing import Final, FrozenSet, Mapping, Optional

STRUCTURAL_TERMS_VERSION: Final[str] = "structural_terms.v0.4.0"

# Posts
POST_PRIMARY: Final[str] = "post.primary"
POST_SECONDARY: Final[str] = "post.secondary"
POST_CORNER: Final[str] = "post.corner"
POST_JAMB: Final[str] = "post.jamb"          # opening jamb post; requires side="L|R"
POST_INTERIOR: Final[str] = "post.interior"  # interior support post (hall posts etc.)

# Beams / rails / plates
BEAM_SILL: Final[str] = "beam.sill"
BEAM_PLATE: Final[str] = "beam.plate"
BEAM_EAVES_PLATE: Final[str] = "beam.eaves_plate"
BEAM_LINTEL: Final[str] = "beam.lintel"
BEAM_WINDOW_SILL: Final[str] = "beam.window_sill"
BEAM_THRESHOLD: Final[str] = "beam.threshold"
BEAM_TIE: Final[str] = "beam.tie"
BEAM_COLLAR: Final[str] = "beam.collar"

# Bracing
BRACE_DIAGONAL: Final[str] = "brace.diagonal"
BRACE_KNEE: Final[str] = "brace.knee"
BRACE_CROSS: Final[str] = "brace.cross"

# Roof members
ROOF_RAFTER: Final[str] = "roof.rafter"
ROOF_PURLIN: Final[str] = "roof.purlin"
ROOF_RIDGE: Final[str] = "roof.ridge"

# Infill / panels
INFILL_CELL: Final[str] = "infill.cell"
INFILL_PANEL: Final[str] = "infill.panel"

# Foundation (optional future)
FOUNDATION_PAD: Final[str] = "foundation.pad"
FOUNDATION_STRIP: Final[str] = "foundation.strip"

# Kinds
KIND_POST: Final[str] = "post"
KIND_BEAM: Final[str] = "beam"
KIND_BRACE: Final[str] = "brace"
KIND_ROOF: Final[str] = "roof"
KIND_INFILL: Final[str] = "infill"
KIND_FOUNDATION: Final[str] = "foundation"

TID_KIND: Final[Mapping[str, str]] = {
    # posts
    POST_PRIMARY: KIND_POST,
    POST_SECONDARY: KIND_POST,
    POST_CORNER: KIND_POST,
    POST_JAMB: KIND_POST,
    POST_INTERIOR: KIND_POST,
    # beams
    BEAM_SILL: KIND_BEAM,
    BEAM_PLATE: KIND_BEAM,
    BEAM_EAVES_PLATE: KIND_BEAM,
    BEAM_LINTEL: KIND_BEAM,
    BEAM_WINDOW_SILL: KIND_BEAM,
    BEAM_THRESHOLD: KIND_BEAM,
    BEAM_TIE: KIND_BEAM,
    BEAM_COLLAR: KIND_BEAM,
    # braces
    BRACE_DIAGONAL: KIND_BRACE,
    BRACE_KNEE: KIND_BRACE,
    BRACE_CROSS: KIND_BRACE,
    # roof
    ROOF_RAFTER: KIND_ROOF,
    ROOF_PURLIN: KIND_ROOF,
    ROOF_RIDGE: KIND_ROOF,
    # infill
    INFILL_CELL: KIND_INFILL,
    INFILL_PANEL: KIND_INFILL,
    # foundation
    FOUNDATION_PAD: KIND_FOUNDATION,
    FOUNDATION_STRIP: KIND_FOUNDATION,
}

VALID_TIDS: Final[FrozenSet[str]] = frozenset(TID_KIND.keys())

def is_valid_tid(tid: object) -> bool:
    return isinstance(tid, str) and tid in VALID_TIDS

def tid_kind(tid: object) -> Optional[str]:
    if not isinstance(tid, str):
        return None
    return TID_KIND.get(tid)

def assert_valid_tid(tid: object, *, where: str = "unknown") -> str:
    if not isinstance(tid, str) or not tid:
        raise ValueError(f"{where}: member missing required string field 'tid'")
    if tid not in VALID_TIDS:
        raise ValueError(f"{where}: unknown tid '{tid}' (not in structural ontology)")
    return tid

__all__ = [
    "STRUCTURAL_TERMS_VERSION",
    "KIND_POST","KIND_BEAM","KIND_BRACE","KIND_ROOF","KIND_INFILL","KIND_FOUNDATION",
    "POST_PRIMARY","POST_SECONDARY","POST_CORNER","POST_JAMB","POST_INTERIOR",
    "BEAM_SILL","BEAM_PLATE","BEAM_EAVES_PLATE","BEAM_LINTEL","BEAM_WINDOW_SILL","BEAM_THRESHOLD","BEAM_TIE","BEAM_COLLAR",
    "BRACE_DIAGONAL","BRACE_KNEE","BRACE_CROSS",
    "ROOF_RAFTER","ROOF_PURLIN","ROOF_RIDGE",
    "INFILL_CELL","INFILL_PANEL",
    "FOUNDATION_PAD","FOUNDATION_STRIP",
    "TID_KIND","VALID_TIDS",
    "is_valid_tid","tid_kind","assert_valid_tid",
]
