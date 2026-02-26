# bvillage/domains/fachwerk/core/frameplan.py

"""
bvillage.domains.fachwerk.core.frameplan
=======================================

Build a Fachwerk frameplan artifact.

Units: meters.

This module is pure planning/data:
- It computes normalized openings, vertical axes (u), and z-axes.
- It returns a FramePlan dataclass and dict payload for notes storage.

Schema
------
frameplan_to_dict() emits a stable schema used by Blender builders.

As of schema_version=2, the artifact contains:
- "members": MVP structural members (posts/rails/braces)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Tuple

from bvillage.core.geom_eps import EPS_MERGE
from bvillage.core.model import StructurePlan
from bvillage.domains.fachwerk.core.openings_norm import (
    OpeningFinal,
    normalize_openings_from_plan,
)
from bvillage.domains.fachwerk.core.axes_u import compute_vertical_axes
from bvillage.domains.fachwerk.core.axes_z import compute_z_axes
from bvillage.domains.fachwerk.core.wall_tags import compute_wall_tags, suggest_front_wall


WidthType = Literal["axis", "clear"]


@dataclass(frozen=True, slots=True)
class FramePolicy:
    """
    Fachwerk engine policy parameters.

    Units: meters.
    """
    b_max: float
    default_jamb_t: float = 0.20
    horizontal_axes_style: List[float] = None  # type: ignore[assignment]

    # z-axis post-processing parameters (merge, min band thickness, etc.)
    z_merge_tol: float = EPS_MERGE
    z_band_min: float = 0.15
    z_band_target_min: float = 0.25

    # How to interpret opening width (axis vs clear)
    width_type: WidthType = "axis"

    def __post_init__(self):
        if self.horizontal_axes_style is None:
            object.__setattr__(self, "horizontal_axes_style", [0.0, 0.9, 1.6, 2.2])


@dataclass(frozen=True, slots=True)
class FramePlan:
    """
    Derived planning artifact for the Fachwerk frame build.

    L/W: footprint dims
    H_e: wall/eaves height
    z0: ground base
    """
    L: float
    W: float
    H_e: float
    z0: float

    openings_final: List[OpeningFinal]

    vertical_axes: Dict[str, Dict[str, List[float]]]
    z_axes: List[float]
    z_clusters: List[List[float]]
    z_repair_log: List[str]

    wall_tags: Dict[str, List[str]]
    front_wall: str


def _infer_wall_height(structure: StructurePlan) -> Tuple[float, float]:
    """
    Infer z0 and H_e from structure plan.
    Falls back to conservative defaults if not present.
    """
    z0 = 0.0
    H_e = 2.6

    # Defensive: not all structure plans may carry these yet
    try:
        if getattr(structure, "z0", None) is not None:
            z0 = float(structure.z0)
    except Exception:
        pass

    try:
        if getattr(structure, "eaves_height", None) is not None:
            H_e = float(structure.eaves_height)
        elif getattr(structure, "wall_height", None) is not None:
            H_e = float(structure.wall_height)
    except Exception:
        pass

    return z0, H_e


def build_frameplan(*, structure: StructurePlan, openings: Any, policy: FramePolicy) -> FramePlan:
    """
    Build frameplan artifact for the given structure and openings.

    Returns
    -------
    FramePlan
    """
    L = float(structure.footprint.length)
    W = float(structure.footprint.width)

    z0, H_e = _infer_wall_height(structure)

    openings_final = normalize_openings_from_plan(
        openings,
        default_jamb_t=float(policy.default_jamb_t),
        width_type=policy.width_type,
    )

    vertical_axes = compute_vertical_axes(
        L=L,
        W=W,
        b_max=float(policy.b_max),
        openings=list(openings_final),
    )

    z_axes, z_clusters, z_repair_log = compute_z_axes(
        z0=z0,
        H_e=H_e,
        horizontal_axes_style=list(policy.horizontal_axes_style),
        z_merge_tol=float(policy.z_merge_tol),
        z_band_min=float(policy.z_band_min),
        z_band_target_min=float(policy.z_band_target_min),
        openings=list(openings_final),
    )

    wall_tags = compute_wall_tags(openings_final)
    front_wall = suggest_front_wall(wall_tags)

    return FramePlan(
        L=L,
        W=W,
        H_e=H_e,
        z0=z0,
        openings_final=list(openings_final),
        vertical_axes=vertical_axes,
        z_axes=z_axes,
        z_clusters=z_clusters,
        z_repair_log=z_repair_log,
        wall_tags=wall_tags,
        front_wall=front_wall,
    )


def frameplan_to_dict(fp: FramePlan) -> Dict[str, Any]:
    """
    Convert FramePlan to a JSON-like dict for notes storage (stable schema).

    schema_version=2 introduces "members".
    """
    # ---- Members v1: PRIMARY_POST + opening frames as structural truth ----
    primary_posts: List[Dict[str, Any]] = []
    for wall in ("N", "S", "E", "W"):
        w = fp.vertical_axes.get(wall, {})
        for u in w.get("primary", []):
            primary_posts.append(
                {
                    "role": "PRIMARY_POST",
                    "wall": wall,
                    "u": float(u),
                    "z0": float(fp.z0),
                    "z1": float(fp.H_e),
                    "profile": {"w": 0.20, "d": 0.20},
                }
            )

    opening_posts: List[Dict[str, Any]] = []
    opening_rails: List[Dict[str, Any]] = []

    for o in fp.openings_final:
        # jambs
        opening_posts.append(
            {
                "role": "OPENING_JAMB_L",
                "wall": o.wall,
                "u": float(o.u0),
                "z0": float(o.z0),
                "z1": float(o.z1),
                "profile": {"w": 0.18, "d": 0.18},
                "opening": o.name,
            }
        )
        opening_posts.append(
            {
                "role": "OPENING_JAMB_R",
                "wall": o.wall,
                "u": float(o.u1),
                "z0": float(o.z0),
                "z1": float(o.z1),
                "profile": {"w": 0.18, "d": 0.18},
                "opening": o.name,
            }
        )

        # lintel (gate vs window profile)
        if o.typ == "gate":
            lintel_prof = {"w": 0.20, "d": 0.20}
        else:
            lintel_prof = {"w": 0.16, "d": 0.18}

        opening_rails.append(
            {
                "role": "OPENING_LINTEL",
                "wall": o.wall,
                "u0": float(o.u0),
                "u1": float(o.u1),
                "z": float(o.z1),
                "profile": lintel_prof,
                "opening": o.name,
            }
        )

        # sill for windows
        if o.typ == "window":
            opening_rails.append(
                {
                    "role": "OPENING_SILL",
                    "wall": o.wall,
                    "u0": float(o.u0),
                    "u1": float(o.u1),
                    "z": float(o.z0),
                    "profile": {"w": 0.16, "d": 0.18},
                    "opening": o.name,
                }
            )

    return {
        "schema_version": 2,

        "dims": {"L": fp.L, "W": fp.W, "H_e": fp.H_e, "z0": fp.z0},

        "openings": [
            {
                "name": o.name,
                "type": o.typ,
                "wall": o.wall,
                "u0": o.u0,
                "u1": o.u1,
                "u_center": o.u_center,
                "width_axis": o.width_axis,
                "width_clear": o.width_clear,
                "z0": o.z0,
                "z1": o.z1,
                "jamb_t": o.jamb_t,
            }
            for o in fp.openings_final
        ],

        "axes_u": fp.vertical_axes,
        "axes_z": fp.z_axes,
        "z_repair_log": list(fp.z_repair_log),
        "wall_tags": fp.wall_tags,
        "front_wall": fp.front_wall,

        "members": {
            "posts": primary_posts + opening_posts,
            "rails": opening_rails,
            "braces": [],
        },
    }

def _flatten_numeric(x: Any) -> List[float]:
    """Collect all numeric values from nested lists/dicts, return sorted unique floats."""
    vals: List[float] = []

    def _collect(v: Any) -> None:
        if v is None:
            return
        if isinstance(v, (int, float)):
            vals.append(float(v))
            return
        if isinstance(v, str):
            try:
                vals.append(float(v))
            except Exception:
                return
            return
        if isinstance(v, (list, tuple)):
            for it in v:
                _collect(it)
            return
        if isinstance(v, dict):
            for it in v.values():
                _collect(it)
            return

    _collect(x)
    return sorted(set(vals))


def normalize_frameplan_dict(fp: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize/enrich a frameplan dict to a canonical schema.

    Adds:
      - fp["basis"]         : x_min,x_max,center_x,halfW
      - fp["axes_u_flat"]   : {wall: [u...]}  (sorted unique)
      - fp["axes_z_flat"]   : [z...]
      - fp["openings_norm"] : openings with guaranteed u0/u1/z0/z1 keys

    Keeps original keys untouched.
    """
    dims = fp.get("dims") or {}
    L = dims.get("L")
    W = dims.get("W")
    if L is None or W is None:
        raise ValueError("frameplan dict missing dims.L/dims.W")

    Lf = float(L)
    Wf = float(W)

    fp.setdefault("basis", {
        "x_min": 0.0,
        "x_max": Lf,
        "center_x": 0.5 * Lf,
        "halfW": 0.5 * Wf,
    })

    # axes_z_flat
    fp["axes_z_flat"] = _flatten_numeric(fp.get("axes_z"))

    # axes_u_flat per wall
    axes_u = fp.get("axes_u") or {}
    axes_u_flat: Dict[str, List[float]] = {}
    for wall in ("N", "S", "E", "W"):
        w = axes_u.get(wall)
        if w is None:
            axes_u_flat[wall] = []
            continue
        # Prefer canonical w["all"] if present (your current schema provides this)
        if isinstance(w, dict) and "all" in w:
            axes_u_flat[wall] = _flatten_numeric(w.get("all"))
        else:
            axes_u_flat[wall] = _flatten_numeric(w)

    fp["axes_u_flat"] = axes_u_flat

    # openings_norm
    openings = fp.get("openings") or []
    if isinstance(openings, dict):
        openings_list = list(openings.values())
    elif isinstance(openings, list):
        openings_list = openings
    else:
        openings_list = []

    openings_norm = []
    for op in openings_list:
        if not isinstance(op, dict):
            continue
        wall = op.get("wall")
        if wall is None:
            continue

        u0 = op.get("u0")
        u1 = op.get("u1")
        if u0 is None or u1 is None:
            ur = op.get("u")
            if isinstance(ur, (list, tuple)) and len(ur) == 2:
                u0, u1 = ur[0], ur[1]

        z0 = op.get("z0")
        z1 = op.get("z1")
        if z0 is None or z1 is None:
            zr = op.get("z")
            if isinstance(zr, (list, tuple)) and len(zr) == 2:
                z0, z1 = zr[0], zr[1]

        if u0 is None or u1 is None or z0 is None or z1 is None:
            continue

        o2 = dict(op)
        o2["u0"] = float(u0)
        o2["u1"] = float(u1)
        o2["z0"] = float(z0)
        o2["z1"] = float(z1)
        openings_norm.append(o2)

    fp["openings_norm"] = openings_norm
    return fp

def frameplan_report(fp: FramePlan) -> str:
    """Human-readable planner report."""
    lines: List[str] = []
    lines.append("========== PLANNER REPORT ==========")
    lines.append(f"[Dims] L={fp.L:.3f} W={fp.W:.3f} H_e={fp.H_e:.3f} z0={fp.z0:.3f}")
    lines.append("[Z Axes] " + ", ".join(f"{z:.3f}" for z in fp.z_axes))

    if fp.z_repair_log:
        lines.append("[Z Repair Log]")
        for msg in fp.z_repair_log:
            lines.append(f"  - {msg}")

    lines.append(f"[Openings Final] n={len(fp.openings_final)}")
    for o in fp.openings_final:
        lines.append(
            f"  {o.name:>4} {o.typ:<6} wall={o.wall} "
            f"u_axis=[{o.u0:+.3f},{o.u1:+.3f}] (axis={o.width_axis:.3f} clear={o.width_clear:.3f}) "
            f"z=[{o.z0:.3f},{o.z1:.3f}]"
        )

    lines.append("[Axes Summary]")
    for wall in ("N", "S", "E", "W"):
        w = fp.vertical_axes[wall]
        lines.append(
            f"  Wall {wall}: primary={len(w['primary'])} opening={len(w['opening'])} "
            f"secondary={len(w['secondary'])} all={len(w['all'])}"
        )

    lines.append(f"[Front Wall] {fp.front_wall}")
    return "\n".join(lines)
