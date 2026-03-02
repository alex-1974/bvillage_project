# bvillage/domains/fachwerk/blender/build_frame.py

"""
Fachwerk frame builder (Blender layer).

This module is a *consumer* of a validated FramePlan and house metadata.

Contracts / Layer rules
- Planning happens upstream (planner / frameplan generator).
- This builder must not invent structure; it renders members-first geometry.
- Contract gate: `audit_frameplan_contract(fp, house, strict=False)`.

Materials
- Material *policy* (role -> default material_id) lives in `core.materials.policies`.
- Builder never carries role->material maps; it passes an empty fallback to
  `resolve_for_builder(...)` so policy can decide.

Phases (stable IDs; ordering may change without renumbering)
- STRUCT_BASE   : posts + plates from members
- ROOF          : roof members
- HALL_SUPPORT  : hall posts / ridge supports
- FP_NORMALIZE  : normalize/compat (no expected geometry delta)
- OPENINGS      : opening frames
- BRACES        : braces (corner bands, etc.)
- INFILLS       : infill panels/cells
"""

from __future__ import annotations

import hashlib
import inspect
import logging
import math
from datetime import datetime
from typing import Any, Optional

import bpy
from mathutils import Vector

from bvillage.core.errors import InvariantError, MaterialResolveError, SchemaError
from bvillage.domains.fachwerk.blender.materials_adapter import apply_material_to_object
from bvillage.core.notes import get_domain_artifact

from bvillage.domains.fachwerk.core.frameplan_contract import audit_frameplan_contract
from bvillage.domains.fachwerk.core.frameplan import normalize_frameplan_dict

LOG = logging.getLogger(__name__)

__all__ = [
    "build_fachwerk_frame",
    "build_fachwerk_frame_from_structure_notes",
]


# -----------------------------------------------------------------------------
# Compatibility helper (stable against internal API drift)
# -----------------------------------------------------------------------------

def _call_compat(func: Any, /, **kwargs: Any) -> Any:
    """Call `func` with only the kwargs it actually accepts.

    This keeps build_frame resilient against signature drift in domain blender modules
    (opening_frames / braces / infills), while remaining explicit about what we *intend*
    to pass.
    """
    sig = inspect.signature(func)
    for p in sig.parameters.values():
        if p.kind == inspect.Parameter.VAR_KEYWORD:
            return func(**kwargs)
    allowed = set(sig.parameters.keys())
    filtered = {k: v for k, v in kwargs.items() if k in allowed}
    return func(**filtered)


# -----------------------------------------------------------------------------
# Materials
# -----------------------------------------------------------------------------


def _material_ctx_view(ctx: Any, *, house_name: str) -> dict[str, Any]:
    """ctx may be a frozen dataclass -> never mutate it.

    Provide a dict "view" for material resolution + seed-based variation.

    Important:
      - Role/material defaults are resolved by `core.materials` (policy).
      - The *Blender* material cache & node graphs live in `materials_adapter`.
        This builder never caches `bpy.types.Material` objects.
    """
    seed_any = getattr(ctx, "seed", None)
    if seed_any is None:
        # stable seed derived from house name when ctx.seed absent
        seed_any = int.from_bytes(
            hashlib.blake2b(str(house_name).encode("utf-8"), digest_size=8).digest(),
            "big",
            signed=False,
        ) & 0x7FFFFFFF

    seed_val = getattr(seed_any, "base", seed_any)
    try:
        seed_int = int(seed_val)
    except Exception:
        seed_int = 0

    return {"seed": seed_int}


def _assign_member_material(
    obj: Optional[bpy.types.Object],
    member: dict[str, Any],
    ctx_view: Any,
) -> None:
    """Resolve deterministic material for a member and assign to Blender object.

    Canonical path:
      resolve_for_builder(...) -> materials_adapter.apply_material_to_object(...)

    Builder provides no override; it passes empty fallback so policy decides defaults.
    """
    if obj is None:
        return

    from .materials_assign import assign_member_material

    assign_member_material(
        obj=obj,
        member=member,
        ctx_view=ctx_view,
        default_material_id="",
        name_hint=str(getattr(member, "id", None) or member.get("id") or getattr(obj, "name", "material")),
    )
    
# -----------------------------------------------------------------------------
# Collections & clearing
# -----------------------------------------------------------------------------

def _ensure_collection(name: str, parent: Optional[bpy.types.Collection] = None) -> bpy.types.Collection:
    if parent is None:
        parent = bpy.context.scene.collection

    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)

    # Link into tree if not linked yet
    if col.name not in parent.children:
        parent.children.link(col)

    return col


def _ensure_subcollections(root_collection: bpy.types.Collection) -> dict[str, bpy.types.Collection]:
    col_fachwerk = _ensure_collection("Fachwerk", parent=root_collection)
    col_frame = _ensure_collection("BayFrame", parent=col_fachwerk)
    col_roof = _ensure_collection("Roof", parent=col_fachwerk)
    col_openings = _ensure_collection("Openings", parent=col_fachwerk)
    col_braces = _ensure_collection("Braces", parent=col_fachwerk)
    col_infills = _ensure_collection("Infills", parent=col_fachwerk)
    col_debug = _ensure_collection("Debug", parent=col_fachwerk)

    return {
        "fachwerk": col_fachwerk,
        "frame": col_frame,
        "roof": col_roof,
        "openings": col_openings,
        "braces": col_braces,
        "infills": col_infills,
        "debug": col_debug,
    }


def _count_objects(cols: dict[str, bpy.types.Collection]) -> dict[str, int]:
    return {
        "frame": len(cols["frame"].objects),
        "roof": len(cols["roof"].objects),
        "openings": len(cols["openings"].objects),
        "braces": len(cols["braces"].objects),
        "infills": len(cols["infills"].objects),
        "debug": len(cols["debug"].objects),
    }


def _delta(before: dict[str, int], after: dict[str, int]) -> dict[str, int]:
    return {k: int(after.get(k, 0)) - int(before.get(k, 0)) for k in before.keys()}


def _log_phase(phase: str, before: dict[str, int], after: dict[str, int]) -> dict[str, int]:
    d = _delta(before, after)
    LOG.debug("PHASE %-12s | delta=%s | after=%s", phase, d, after)
    return d


def _require_delta(phase: str, d: dict[str, int], key: str, *, min_delta: int = 1) -> None:
    if int(d.get(key, 0)) < min_delta:
        LOG.error("PHASE FAIL | %s produced %s delta=%d (<%d)", phase, key, int(d.get(key, 0)), min_delta)
        raise InvariantError(f"Phase {phase} produced insufficient {key} objects")


def _clear_fachwerk_subtree(root_collection: bpy.types.Collection) -> int:
    removed = 0
    col = bpy.data.collections.get("Fachwerk")
    if col is None:
        return 0

    # Remove objects in subtree
    for obj in list(col.all_objects):
        try:
            bpy.data.objects.remove(obj, do_unlink=True)
            removed += 1
        except Exception:
            pass

    # Remove child collections
    for child in list(col.children):
        try:
            col.children.unlink(child)
        except Exception:
            pass
        try:
            bpy.data.collections.remove(child)
        except Exception:
            pass

    # Unlink + remove the Fachwerk collection block
    try:
        if col.name in root_collection.children:
            root_collection.children.unlink(col)
    except Exception:
        pass
    try:
        bpy.data.collections.remove(col)
    except Exception:
        pass

    return removed


# -----------------------------------------------------------------------------
# House coercion / mapping helpers (members-first)
# -----------------------------------------------------------------------------

def _require_house_keys(house: dict[str, Any]) -> None:
    """Contract gate for house metadata.

    ARC-001A hardened:
      - The Blender layer must not set defaults.
      - All required parameters must be provided upstream (core.house_params + structure.grid).
    """
    required = (
        "axes_u",
        "axes_v",
        "L",
        "W",
        "z0",
        "z_plate",
        "roof_pitch_deg",
        "roof_overhang",
        "post_section",
        "plate_section",
    )
    for k in required:
        if k not in house:
            raise SchemaError(f"House metadata missing required key '{k}'")

    axes_u = house.get("axes_u")
    axes_v = house.get("axes_v")
    if not axes_u or not axes_v:
        raise SchemaError("Invalid house: axes_u/axes_v missing or empty")

    # sanity
    if float(house["L"]) <= 0.0 or float(house["W"]) <= 0.0:
        raise SchemaError(f"Invalid house dims: L={house['L']!r} W={house['W']!r}")
    if float(house["roof_pitch_deg"]) <= 0.0:
        raise SchemaError(f"Invalid roof_pitch_deg: {house['roof_pitch_deg']!r}")



def _log_build_header(house_name: str, house: dict[str, Any]) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("BVILLAGE FACHWERK BUILD START")
    lines.append(f"House      : {house_name}")
    try:
        W = float(house["W"])
        z_plate = float(house["z_plate"])
        fields = house.get("fields", "?")
        lines.append(f"Dims      : fields={fields} | W={W:.3f}m | plate={z_plate:.3f}m")
    except Exception:
        pass
    lines.append(f"Timestamp  : {ts}")
    lines.append("=" * 70)
    LOG.info("\n" + "\n".join(lines))


def _coerce_house(ctx: Any, structure: Any) -> dict[str, Any]:
    """Build the `house` dict required by the Blender builder.

    ARC-001A hardened:
      - All policy/renderer parameters must come from the upstream artifact `core.house_params`.
      - Axes come from `structure.grid` (truth of plan discretization).
      - No fallback defaults are allowed here.
    """
    notes = getattr(structure, "notes", None)
    if not isinstance(notes, dict):
        raise SchemaError("StructurePlan.notes missing/invalid (expected dict)")

    hp = get_domain_artifact(
        notes,
        domain="core",
        artifact="house_params",
        legacy_aliases=("house_params", "core.house_params"),
    )
    if not isinstance(hp, dict):
        raise SchemaError("Missing required artifact: core.house_params")

    grid = getattr(structure, "grid", None)
    if grid is None or not hasattr(grid, "axes_u") or not hasattr(grid, "axes_v"):
        raise SchemaError("StructurePlan.grid missing/invalid (axes_u/axes_v required)")

    axes_u = list(getattr(grid, "axes_u"))
    axes_v = list(getattr(grid, "axes_v"))
    if not axes_u or not axes_v:
        raise SchemaError("StructurePlan.grid axes_u/axes_v missing or empty")

    # Merge into the contract object used by audit + builder
    house: dict[str, Any] = dict(hp)
    house["axes_u"] = axes_u
    house["axes_v"] = axes_v

    # Optional, for logs only
    fields = getattr(grid, "fields", None)
    if isinstance(fields, (list, tuple)):
        house["fields"] = len(fields)
    else:
        n_fields = getattr(grid, "n_fields", None)
        if n_fields is not None:
            house["fields"] = n_fields

    return house



def _house_basis(house: dict[str, Any]) -> tuple[float, float, float, float]:
    axes_u = list(house["axes_u"])
    axes_v = list(house["axes_v"])
    x_min = float(min(axes_u))
    x_max = float(max(axes_u))
    center_x = 0.5 * (x_min + x_max)
    halfW = 0.5 * float(max(axes_v) - min(axes_v))
    return x_min, x_max, center_x, halfW


def _map_post_member(member: dict[str, Any], *, house: dict[str, Any]) -> tuple[Vector, Vector]:
    x_min, x_max, center_x, halfW = _house_basis(house)
    wall = member["wall"]
    u = float(member["u"])
    z0 = float(member["z0"])
    z1 = float(member["z1"])

    if wall == "N":
        return Vector((center_x + u, -halfW, z0)), Vector((center_x + u, -halfW, z1))
    if wall == "S":
        return Vector((center_x + u, +halfW, z0)), Vector((center_x + u, +halfW, z1))
    if wall == "E":
        return Vector((x_max, u, z0)), Vector((x_max, u, z1))
    if wall == "W":
        return Vector((x_min, u, z0)), Vector((x_min, u, z1))
    raise SchemaError(f"Unknown wall '{wall}'")


def _map_rail_member(member: dict[str, Any], *, house: dict[str, Any]) -> tuple[Vector, Vector]:
    x_min, x_max, center_x, halfW = _house_basis(house)
    wall = member["wall"]
    u0 = float(member["u0"])
    u1 = float(member["u1"])
    z = float(member["z"])

    if wall == "N":
        return Vector((center_x + u0, -halfW, z)), Vector((center_x + u1, -halfW, z))
    if wall == "S":
        return Vector((center_x + u0, +halfW, z)), Vector((center_x + u1, +halfW, z))
    if wall == "E":
        return Vector((x_max, u0, z)), Vector((x_max, u1, z))
    if wall == "W":
        return Vector((x_min, u0, z)), Vector((x_min, u1, z))
    raise SchemaError(f"Unknown wall '{wall}'")


# -----------------------------------------------------------------------------
# Primitive beam creation
# -----------------------------------------------------------------------------

def _member_name(member: dict[str, Any], *, fallback: str) -> str:
    return str(member.get("id") or member.get("name") or fallback)


def _add_beam(
    collection: bpy.types.Collection,
    *,
    name: str,
    p0: Vector,
    p1: Vector,
    profile: Any,
) -> bpy.types.Object:
    """Create a simple beam as an edge-based mesh (placeholder geometry)."""
    mesh = bpy.data.meshes.new(name=name + "_mesh")
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)

    # Minimal geometry: a 2-vertex edge (profiles handled elsewhere in v0.4.0+)
    mesh.from_pydata([p0, p1], [(0, 1)], [])
    mesh.update()

    # profile currently unused here; kept for future extrusion / beam profiles
    _ = profile
    return obj


# -----------------------------------------------------------------------------
# Phase builders (members-first)
# -----------------------------------------------------------------------------

def _build_primary_posts_from_members(fp: dict[str, Any], house: dict[str, Any], col_frame: bpy.types.Collection, ctx_view: Any) -> int:
    built = 0
    members = fp.get("members") or {}
    posts = members.get("posts") or []
    for mm in posts:
        if str(mm.get("role")) != "PRIMARY_POST":
            continue
        p0, p1 = _map_post_member(mm, house=house)
        obj = _add_beam(col_frame, name=_member_name(mm, fallback="Post"), p0=p0, p1=p1, profile=mm.get("profile") or house["post_section"])
        _assign_member_material(obj, mm, ctx_view)
        built += 1
    return built


def _build_plates_from_members(fp: dict[str, Any], house: dict[str, Any], col_frame: bpy.types.Collection, ctx_view: Any) -> int:
    built = 0
    members = fp.get("members") or {}
    rails = members.get("rails") or []
    for m in rails:
        role = str(m.get("role") or "")
        if not role.startswith("EAVES_PLATE_"):
            continue
        p0, p1 = _map_rail_member(m, house=house)
        obj = _add_beam(col_frame, name=_member_name(m, fallback="Plate"), p0=p0, p1=p1, profile=m.get("profile") or house["plate_section"])
        _assign_member_material(obj, m, ctx_view)
        built += 1
    return built



def _build_hall_posts_to_ridge(fp: dict[str, Any], house: dict[str, Any], col_frame: bpy.types.Collection, ctx_view: Any) -> int:
    """Build hall posts on the midline up to ridge/roof support.

    Important: In current FramePlan schema, hall posts are not necessarily present
    in fp.members.posts. Historically, Hallenhaus requires a row of interior
    posts (Ständer) along the building length. The builder therefore generates
    these members deterministically from house.axes_u.

    If future schemas provide explicit HALL_POST members, those will be built in
    addition to (or instead of) generated posts depending on policy. For now we
    generate one per axes_u entry.
    """
    built = 0

    axes_u = list(house.get("axes_u") or [])
    if not axes_u:
        return 0

    z0 = float(house["z0"])
    # Prefer explicit ridge/hall height if present; otherwise fall back to H_e.
    z1 = float(house.get("z_ridge") if ("z_ridge" in house) else (float(house["z_plate"]) + math.tan(math.radians(float(house["roof_pitch_deg"]))) * (0.5 * float(house["W"]))))

    # Midline y=0 in house coordinates; x runs along axes_u.
    for i, x in enumerate(axes_u):
        mm: dict[str, Any] = {
            "role": "HALL_POST",
            "id": f"HallPost_{i:02d}",
            "wall": "MID",
            "u": float(x),  # interpreted as absolute x for MID
            "z0": z0,
            "z1": z1,
            # allow profile override if present on house
            "profile": {"w": float(house["post_section"][0]),
                        "d": float(house["post_section"][1])},
        }
        p0 = Vector((float(x), 0.0, z0))
        p1 = Vector((float(x), 0.0, z1))
        obj = _add_beam(
            col_frame,
            name=mm["id"],
            p0=p0,
            p1=p1,
            profile=mm.get("profile") or house["post_section"],
        )
        _assign_member_material(obj, mm, ctx_view)
        built += 1

    return built


def _build_posts_and_plates(house: dict[str, Any], fp: dict[str, Any], col_frame: bpy.types.Collection, ctx_view: Any) -> None:
    built_posts = _build_primary_posts_from_members(fp, house, col_frame, ctx_view)
    if built_posts <= 0:
        raise SchemaError("members-first required: missing/empty members.posts PRIMARY_POST")
    built_plates = _build_plates_from_members(fp, house, col_frame, ctx_view)
    if built_plates <= 0:
        raise SchemaError("members-first required: missing/empty members.rails EAVES_PLATE_*")
    LOG.info("Phase STRUCT_BASE: members-first posts=%d plates=%d", built_posts, built_plates)


def _build_roof(house: dict[str, Any], col_roof: bpy.types.Collection) -> dict[str, Any]:
    from .roof import build_roof_per_field
    halfW = 0.5 * float(house["W"])
    return build_roof_per_field(
        axes_u=list(house["axes_u"]),
        half_width=halfW,
        z_plate=float(house["z_plate"]),
        roof_pitch_deg=float(house["roof_pitch_deg"]),
        col_roof=col_roof,
    )


# -----------------------------------------------------------------------------
# Public API
# -----------------------------------------------------------------------------

def build_frame(
    *,
    ctx: Any,
    structure: Any,
    frameplan: dict[str, Any],
    root_collection: bpy.types.Collection,
    clear_previous: bool = True,
) -> bpy.types.Collection:
    """Render a FramePlan into Blender collections."""
    if clear_previous:
        removed = _clear_fachwerk_subtree(root_collection)
        LOG.info("clear_previous=True -> cleared fachwerk subtree, removed_objects=%d", removed)

    cols = _ensure_subcollections(root_collection)
    before = _count_objects(cols)

    # normalize frameplan dict to current schema representation
    frameplan = normalize_frameplan_dict(frameplan)

    # house metadata
    house = _coerce_house(ctx, structure)
    _require_house_keys(house)

    ctx_view = _material_ctx_view(ctx, house_name=getattr(structure, "name", "Structure"))

    LOG.info("BUILD START | house=%s clear=%s", getattr(structure, "name", "Structure"), clear_previous)
    LOG.debug(
        "HOUSE | L=%.3f W=%.3f z0=%.3f z_plate=%.3f pitch=%.1f",
        float(house["L"]),
        float(house["W"]),
        float(house["z0"]),
        float(house["z_plate"]),
        float(house["roof_pitch_deg"]),
    )
    LOG.debug("CTX | seed=%s", ctx_view.get("seed"))

    members = frameplan.get("members") or {}
    LOG.debug(
        "MEMBERS | posts=%d rails=%d braces=%d infills=%d openings=%d schema=%s",
        len(members.get("posts") or []),
        len(members.get("rails") or []),
        len(members.get("braces") or []),
        len(members.get("infills") or []),
        len(frameplan.get("openings") or []),
        frameplan.get("schema"),
    )

    _log_build_header(getattr(structure, "name", "Structure"), house)
    LOG.info("build_frame() ENTER")

    # Contract gate
    rep = audit_frameplan_contract(frameplan, house, strict=False)
    if getattr(rep, "hard", None):
        LOG.error("CONTRACT FAIL | hard=%d soft=%d", len(rep.hard), len(getattr(rep, "soft", [])))
        raise SchemaError(f"FramePlan contract failed: hard={len(rep.hard)}")
    LOG.info("CONTRACT OK | hard=0 soft=%d", len(getattr(rep, "soft", [])))

    # STRUCT_BASE
    _build_posts_and_plates(house, frameplan, cols["frame"], ctx_view)
    after = _count_objects(cols)
    d = _log_phase("STRUCT_BASE", before, after)
    _require_delta("STRUCT_BASE", d, "frame", min_delta=1)
    LOG.info("PHASE OK | STRUCT_BASE")
    before = after

    # ROOF
    _build_roof(house, cols["roof"])
    after = _count_objects(cols)
    _log_phase("ROOF", before, after)
    LOG.info("PHASE OK | ROOF")
    before = after

    # HALL_SUPPORT
    _build_hall_posts_to_ridge(frameplan, house, cols["frame"], ctx_view)
    after = _count_objects(cols)
    _log_phase("HALL_SUPPORT", before, after)
    LOG.info("PHASE OK | HALL_SUPPORT")
    before = after

    # FP_NORMALIZE (no geometry delta)
    after = _count_objects(cols)
    _log_phase("FP_NORMALIZE", before, after)
    before = after

    # OPENINGS
    from .opening_frames import build_opening_frames
    _call_compat(build_opening_frames, fp=frameplan, house=house, collection=cols["openings"], policy=None, ctx_view=ctx_view, debug=False)
    after = _count_objects(cols)
    _log_phase("OPENINGS", before, after)
    LOG.info("PHASE OK | OPENINGS")
    before = after

    # BRACES
    from .braces import build_braces_corner_band
    _call_compat(build_braces_corner_band, fp=frameplan, house=house, collection=cols["braces"], ctx_view=ctx_view, debug=False)
    after = _count_objects(cols)
    _log_phase("BRACES", before, after)
    LOG.info("PHASE OK | BRACES")
    before = after

    # INFILLS
    from .infills import build_infills
    _call_compat(build_infills, fp=frameplan, house=house, collection=cols["infills"], ctx_view=ctx_view)
    after = _count_objects(cols)
    _log_phase("INFILLS", before, after)
    LOG.info("PHASE OK | INFILLS")
    before = after

    LOG.info("BUILD SUMMARY | %s", after)

    # Integrity gate
    from .integrity import check_integrity
    ok = check_integrity(fp=frameplan, house=house, collections=cols)
    if not ok:
        raise InvariantError("Integrity check failed (see previous errors)")

    LOG.info("BUILD OK")
    return cols["fachwerk"]


def build_fachwerk_frame(
    *,
    ctx: Any,
    structure: Any,
    frameplan: dict[str, Any],
    root_collection: bpy.types.Collection,
    clear_previous: bool = True,
) -> bpy.types.Collection:
    return build_frame(
        ctx=ctx,
        structure=structure,
        frameplan=frameplan,
        root_collection=root_collection,
        clear_previous=clear_previous,
    )


def build_fachwerk_frame_from_structure_notes(
    *,
    ctx: Any,
    structure: Any,
    root_collection: bpy.types.Collection,
    clear_previous: bool = True,
) -> bpy.types.Collection:
    notes = getattr(structure, "notes", None)
    if not isinstance(notes, dict):
        raise SchemaError("StructurePlan.notes missing/invalid; cannot read fachwerk.frameplan")

    fp_dict = get_domain_artifact(
        notes,
        domain="fachwerk",
        artifact="frameplan",
        legacy_aliases=("frameplan", "fachwerk.frameplan"),
    )
    if fp_dict is None:
        raise SchemaError("Missing required artifact: fachwerk.frameplan")

    return build_fachwerk_frame(
        ctx=ctx,
        structure=structure,
        frameplan=fp_dict,
        root_collection=root_collection,
        clear_previous=clear_previous,
    )
