# bvillage/domains/fachwerk/core/derive_frameplan.py
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from bvillage.core.notes import set_domain_artifact
from bvillage.core.model import StructurePlan
from bvillage.core.ontology.structural_terms import (
    POST_OPENING_JAMB,
    BEAM_OPENING_LINTEL,
    BRACE_KNEE,
)
from bvillage.types.timber_frame.longhouse.contracts.schema_frameplan_langhaus import (
    SCHEMA_VERSION_LANGHAUS,
)


# -----------------------------------------------------------------------------
# Small helpers
# -----------------------------------------------------------------------------

def _member_id(prefix: str, *parts: object) -> str:
    return prefix + "_" + "_".join(str(p) for p in parts)


def _zimmermann_payload(
    seq: Tuple[str, ...],
    xs: Tuple[float, ...],
    cs: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "schema": 1,
        "x_frames": tuple(float(x) for x in xs),
        "cross_section_rows": tuple(
            {"row_kind": r["row_kind"], "y": float(r["y"])}
            for r in cs["rows"]
        ),
        "frame_roles": tuple(
            {"bay_index": int(i), "role": str(role)}
            for i, role in enumerate(seq)
        ),
    }


# -----------------------------------------------------------------------------
# FramePlan v4: members-first XYZ skeleton (writes artifact)
# -----------------------------------------------------------------------------

def derive_frameplan(
    ctx: Any,
    structure: StructurePlan,
    seq: Tuple[str, ...],
    xs: Tuple[float, ...],
    cs: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Emits:
      - fachwerk.frameplan artifact
      - includes zimmermann block required by downstream builders
    """
    width = float(cs["width"])
    z_plate = float(cs["plate_height"])
    halfW = 0.5 * width
    z0 = 0.0

    posts: List[Dict[str, Any]] = []
    rails: List[Dict[str, Any]] = []
    braces: List[Dict[str, Any]] = []

    # --- Primary posts (3 rows per frame: S wall, hall, N wall) ---
    for i, x in enumerate(xs):
        role = seq[i]

        posts.append(
            {
                "id": _member_id("P", i, "S"),
                "tid": "post.primary",
                "role": "post.outer",
                "p0": (float(x), -halfW, z0),
                "p1": (float(x), -halfW, z_plate),
                "tags": ("ROW_WALL", f"FRAME_{i}", f"FrameRole.{role}"),
            }
        )
        posts.append(
            {
                "id": _member_id("P", i, "H"),
                "tid": "post.hall",
                "role": "post.hall",
                "p0": (float(x), 0.0, z0),
                "p1": (float(x), 0.0, z_plate),
                "tags": ("ROW_HALL", f"FRAME_{i}", f"FrameRole.{role}"),
            }
        )
        posts.append(
            {
                "id": _member_id("P", i, "N"),
                "tid": "post.primary",
                "role": "post.outer",
                "p0": (float(x), +halfW, z0),
                "p1": (float(x), +halfW, z_plate),
                "tags": ("ROW_WALL", f"FRAME_{i}", f"FrameRole.{role}"),
            }
        )

    # --- Eaves plates along long walls (N/S) ---
    for i in range(len(xs) - 1):
        x0 = float(xs[i])
        x1 = float(xs[i + 1])

        rails.append(
            {
                "id": _member_id("PL", "S", i),
                "tid": "beam.plate",
                "role": "plate.eaves",
                "p0": (x0, -halfW, z_plate),
                "p1": (x1, -halfW, z_plate),
                "tags": ("WALL_S",),
            }
        )
        rails.append(
            {
                "id": _member_id("PL", "N", i),
                "tid": "beam.plate",
                "role": "plate.eaves",
                "p0": (x0, +halfW, z_plate),
                "p1": (x1, +halfW, z_plate),
                "tags": ("WALL_N",),
            }
        )

    # --- Minimal primary knee braces (debug baseline) ---
    # (Later: proper bracing per bay, gate frame reinforcement, gable-specific bracing)
    bid = 0
    for i in range(len(xs) - 1):
        x0 = float(xs[i])
        x1 = float(xs[i + 1])
        braces.append(
            {
                "id": _member_id("BR", bid),
                "tid": BRACE_KNEE,
                "role": "brace.knee",
                "p0": (x0, -halfW, z_plate * 0.30),
                "p1": (x1, -halfW, z_plate * 0.80),
                "tags": ("WALL_S",),
            }
        )
        bid += 1

    # --- Gate on gable end (MVP): jamb posts + lintel on W_E_0 ---
    # Convention: gable end wall "E" is at x = max(xs) (positive x end).
    # Opening runs along y (local transverse axis).
    gate_x = float(max(xs))
    gate_clear_w = 3.0
    gate_half = 0.5 * gate_clear_w
    gate_z1 = 2.2

    posts.append(
        {
            "id": _member_id("OJ", "GATE", "L"),
            "tid": POST_OPENING_JAMB,
            "role": "opening.jamb",
            "p0": (gate_x, -gate_half, z0),
            "p1": (gate_x, -gate_half, gate_z1),
            "tags": ("OPENING_GATE", "GABLE_END", "WALL_E"),
        }
    )
    posts.append(
        {
            "id": _member_id("OJ", "GATE", "R"),
            "tid": POST_OPENING_JAMB,
            "role": "opening.jamb",
            "p0": (gate_x, +gate_half, z0),
            "p1": (gate_x, +gate_half, gate_z1),
            "tags": ("OPENING_GATE", "GABLE_END", "WALL_E"),
        }
    )
    rails.append(
        {
            "id": _member_id("OL", "GATE"),
            "tid": BEAM_OPENING_LINTEL,
            "role": "opening.lintel",
            "p0": (gate_x, -gate_half, gate_z1),
            "p1": (gate_x, +gate_half, gate_z1),
            "tags": ("OPENING_GATE", "GABLE_END", "WALL_E"),
        }
    )

    frame_layout = {
        "x_frames": [float(x) for x in xs],
        "y_rows": [float(r["y"]) for r in cs["rows"]],
        "frame_roles": [str(role) for role in seq],
    }

    frameplan: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION_LANGHAUS,
        "coordinate_system": {
            "origin": "building_center_ground",
            "axes": {
                "x": "longitudinal_forward",
                "y": "right_when_facing_positive_x",
                "z": "up",
            },
            "units": "meters",
        },
        "basis": {
            "z0": float(z0),
            "z_plate": float(z_plate),
        },
        "frame_layout": frame_layout,
        "zimmermann": _zimmermann_payload(seq, xs, cs),
        "members": {
            "posts": posts,
            "rails": rails,
            "braces": braces,
            "infills": [],
        },
        "openings": [],
        "notes": {
            "mvp": True,
            "gate": {"placement": "gable_end", "wall": "W_E_0"},
        },
    }

    set_domain_artifact(
        structure.notes,
        domain="fachwerk",
        artifact="frameplan",
        payload=frameplan,
    )
    set_domain_artifact(
        structure.notes,
        domain="fachwerk",
        artifact="zimmermann",
        payload=frameplan["zimmermann"],
    )

    return frameplan
