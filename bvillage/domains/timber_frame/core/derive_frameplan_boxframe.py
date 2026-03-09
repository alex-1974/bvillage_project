# bvillage/domains/timber_frame/core/derive_frameplan_boxframe.py
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from bvillage.core.errors import SchemaError
from bvillage.core.model import StructurePlan
from bvillage.core.ontology.structural_terms import (
    BEAM_OPENING_LINTEL,
    BRACE_KNEE,
    POST_OPENING_JAMB,
)
from bvillage.domains.timber_frame.contracts.schema_frameplan_fachwerk import (
    FramePlanFachwerk,
    SCHEMA_VERSION_FACHWERK,
)

__all__ = ["derive_frameplan_boxframe"]


def derive_frameplan_boxframe(
    ctx: Any,
    structure: StructurePlan,
) -> FramePlanFachwerk:
    """
    Derive a members-first timber-frame FramePlan from StructurePlan.

    Architecture
    ------------
    Domain layer:
        StructurePlan -> FramePlan

    Constraints
    -----------
    - no type-layer imports
    - no Blender imports
    - no hidden side-effects
    - no mutation of StructurePlan
    """
    _ = ctx

    xs = _extract_x_frames(structure)
    row_ys = _extract_row_positions(structure)
    frame_roles = _extract_frame_roles(structure)
    z0, z_plate = _extract_vertical_basis(structure)
    basis = _extract_basis(structure)

    posts: List[Dict[str, Any]] = []
    rails: List[Dict[str, Any]] = []
    braces: List[Dict[str, Any]] = []

    # --------------------------------------------------
    # Primary posts
    # --------------------------------------------------
    for i, x in enumerate(xs):
        role = frame_roles[i]

        posts.append(
            {
                "id": f"P_{i}_S",
                "tid": "post.primary",
                "role": "post.outer",
                "p0": (x, row_ys[0], z0),
                "p1": (x, row_ys[0], z_plate),
                "tags": ("ROW_WALL", f"FRAME_{i}", f"FrameRole.{role}", "WALL_S"),
            }
        )
        posts.append(
            {
                "id": f"P_{i}_H",
                "tid": "post.hall",
                "role": "post.hall",
                "p0": (x, row_ys[1], z0),
                "p1": (x, row_ys[1], z_plate),
                "tags": ("ROW_HALL", f"FRAME_{i}", f"FrameRole.{role}"),
            }
        )
        posts.append(
            {
                "id": f"P_{i}_N",
                "tid": "post.primary",
                "role": "post.outer",
                "p0": (x, row_ys[2], z0),
                "p1": (x, row_ys[2], z_plate),
                "tags": ("ROW_WALL", f"FRAME_{i}", f"FrameRole.{role}", "WALL_N"),
            }
        )

    # --------------------------------------------------
    # Eaves plates
    # --------------------------------------------------
    for i in range(len(xs) - 1):
        x0 = xs[i]
        x1 = xs[i + 1]

        rails.append(
            {
                "id": f"PL_S_{i}",
                "tid": "beam.plate",
                "role": "plate.eaves",
                "p0": (x0, row_ys[0], z_plate),
                "p1": (x1, row_ys[0], z_plate),
                "tags": ("WALL_S",),
            }
        )
        rails.append(
            {
                "id": f"PL_N_{i}",
                "tid": "beam.plate",
                "role": "plate.eaves",
                "p0": (x0, row_ys[2], z_plate),
                "p1": (x1, row_ys[2], z_plate),
                "tags": ("WALL_N",),
            }
        )

    # --------------------------------------------------
    # Minimal knee braces (baseline)
    # --------------------------------------------------
    brace_id = 0
    for i in range(len(xs) - 1):
        x0 = xs[i]
        x1 = xs[i + 1]

        braces.append(
            {
                "id": f"BR_{brace_id}",
                "tid": BRACE_KNEE,
                "role": "brace.knee",
                "p0": (x0, row_ys[0], z_plate * 0.30),
                "p1": (x1, row_ys[0], z_plate * 0.80),
                "tags": ("WALL_S",),
            }
        )
        brace_id += 1

    # --------------------------------------------------
    # MVP gate at east gable
    # --------------------------------------------------
    gate_x = max(xs)
    gate_width = 3.0
    gate_half = 0.5 * gate_width
    gate_height = 2.2

    posts.append(
        {
            "id": "OJ_GATE_L",
            "tid": POST_OPENING_JAMB,
            "role": "opening.jamb",
            "p0": (gate_x, -gate_half, z0),
            "p1": (gate_x, -gate_half, gate_height),
            "tags": ("OPENING_GATE", "GABLE_END", "WALL_E"),
        }
    )
    posts.append(
        {
            "id": "OJ_GATE_R",
            "tid": POST_OPENING_JAMB,
            "role": "opening.jamb",
            "p0": (gate_x, +gate_half, z0),
            "p1": (gate_x, +gate_half, gate_height),
            "tags": ("OPENING_GATE", "GABLE_END", "WALL_E"),
        }
    )
    rails.append(
        {
            "id": "OL_GATE",
            "tid": BEAM_OPENING_LINTEL,
            "role": "opening.lintel",
            "p0": (gate_x, -gate_half, gate_height),
            "p1": (gate_x, +gate_half, gate_height),
            "tags": ("OPENING_GATE", "GABLE_END", "WALL_E"),
        }
    )

    frame_layout = {
        "x_frames": list(xs),
        "y_rows": list(row_ys),
        "frame_roles": list(frame_roles),
    }

    frameplan: FramePlanFachwerk = {
        "schema_version": SCHEMA_VERSION_FACHWERK,
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
            "z0": z0,
            "z_plate": z_plate,
            "x_min": basis["x_min"],
            "x_max": basis["x_max"],
            "center_x": basis["center_x"],
            "halfW": basis["halfW"],
        },
        "frame_layout": frame_layout,
        "zimmermann": _zimmermann_payload(frame_roles, xs, row_ys),
        "members": {
            "posts": posts,
            "rails": rails,
            "braces": braces,
            "infills": [],
        },
        "openings": [],
        "notes": {
            "mvp": True,
            "gate": {
                "placement": "gable_end",
                "wall": "W_E_0",
            },
        },
    }

    return frameplan


# --------------------------------------------------
# Helpers
# --------------------------------------------------


def _extract_x_frames(structure: StructurePlan) -> Tuple[float, ...]:
    xs = tuple(float(x) for x in structure.grid.axes_u)
    if len(xs) < 2:
        raise SchemaError("BOX_FRAME requires at least 2 frame axes")
    return xs


def _extract_row_positions(structure: StructurePlan) -> Tuple[float, float, float]:
    ys = tuple(sorted(float(y) for y in structure.grid.axes_v))
    if len(ys) != 3:
        raise SchemaError(
            f"BOX_FRAME longhouse derivation requires exactly 3 row positions, got {len(ys)}"
        )
    return ys[0], ys[1], ys[2]


def _extract_frame_roles(structure: StructurePlan) -> Tuple[str, ...]:
    roles: List[str] = []

    for frame in structure.frames:
        role = None
        for tag in frame.tags:
            if tag.startswith("FrameRole."):
                role = tag.split(".", 1)[1]
                break

        if role is None:
            raise SchemaError(f"Frame {frame.id!r} missing FrameRole.* tag")

        roles.append(role)

    if not roles:
        raise SchemaError("BOX_FRAME derivation requires non-empty structure.frames")

    return tuple(roles)


def _extract_vertical_basis(structure: StructurePlan) -> Tuple[float, float]:
    if not structure.walls:
        raise SchemaError("BOX_FRAME derivation requires structure.walls")

    z0 = min(float(w.z_range[0]) for w in structure.walls)
    z1 = max(float(w.z_range[1]) for w in structure.walls)

    if z1 <= z0:
        raise SchemaError(f"Invalid wall z-range basis: z0={z0}, z1={z1}")

    return z0, z1


def _extract_basis(structure: StructurePlan) -> Dict[str, float]:
    length = float(structure.footprint.length)
    width = float(structure.footprint.width)

    if length <= 0.0:
        raise SchemaError("StructurePlan footprint.length must be > 0")
    if width <= 0.0:
        raise SchemaError("StructurePlan footprint.width must be > 0")

    x_min = 0.0
    x_max = length
    center_x = 0.5 * (x_min + x_max)
    half_w = 0.5 * width

    return {
        "x_min": x_min,
        "x_max": x_max,
        "center_x": center_x,
        "halfW": half_w,
    }


def _zimmermann_payload(
    frame_roles: Tuple[str, ...],
    xs: Tuple[float, ...],
    row_ys: Tuple[float, float, float],
) -> Dict[str, Any]:
    return {
        "schema": 1,
        "x_frames": tuple(float(x) for x in xs),
        "cross_section_rows": (
            {"row_kind": "WALL", "y": float(row_ys[0])},
            {"row_kind": "HALL", "y": float(row_ys[1])},
            {"row_kind": "WALL", "y": float(row_ys[2])},
        ),
        "frame_roles": tuple(
            {"bay_index": int(i), "role": str(role)}
            for i, role in enumerate(frame_roles)
        ),
    }
