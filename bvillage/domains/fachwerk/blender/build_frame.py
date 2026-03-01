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
from datetime import datetime
from typing import Any, Optional

import bpy
from mathutils import Vector

from bvillage.core.errors import InvariantError, MaterialResolveError, SchemaError
from bvillage.core.materials.material_registry import resolve_for_builder
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
# Material cache (avoid thousands of duplicate Blender materials)
# -----------------------------------------------------------------------------

_MATERIAL_CACHE: dict[str, bpy.types.Material] = {}


def _ensure_bv_material(name: str, sample: Any) -> bpy.types.Material:
    """Create/return a deterministic BV_ material based on a RenderSample."""
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nt = mat.node_tree
    if nt is None:
        return mat

    nodes = nt.nodes
    links = nt.links

    bsdf = nodes.get("Principled BSDF")
    if bsdf is None:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")

    out = nodes.get("Material Output")
    if out is None:
        out = nodes.new("ShaderNodeOutputMaterial")

    # ensure link exists
    linked = any(lk.from_node == bsdf and lk.to_node == out for lk in links)
    if not linked:
        links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    # Assign sampled parameters (minimal deterministic shader)
    col_hex = getattr(sample, "base_color_hex", "#808080").lstrip("#")
    try:
        r = int(col_hex[0:2], 16) / 255.0
        g = int(col_hex[2:4], 16) / 255.0
        b = int(col_hex[4:6], 16) / 255.0
    except Exception:
        r, g, b = 0.5, 0.5, 0.5

    bsdf.inputs["Base Color"].default_value = (r, g, b, 1.0)
    bsdf.inputs["Roughness"].default_value = float(getattr(sample, "roughness", 0.6))
    bsdf.inputs["Metallic"].default_value = float(getattr(sample, "metallic", 0.0))

    return mat


def _assign_material(obj: bpy.types.Object, mat: bpy.types.Material) -> None:
    """Assign material to an object's first material slot (if mesh-like)."""
    if obj.data is None:
        return
    mats = getattr(obj.data, "materials", None)
    if mats is None:
        return
    if len(mats) == 0:
        mats.append(mat)
    else:
        mats[0] = mat


def _material_ctx_view(ctx: Any, *, house_name: str) -> dict[str, Any]:
    """ctx may be a frozen dataclass -> never mutate it.

    Provide a dict "view" for material resolution + seed-based variation.
    Material policy is resolved inside core.materials, not here.
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

    Raises MaterialResolveError on failure (no silent partial builds).
    """
    if obj is None:
        return

    resolved, surface, sample = resolve_for_builder(
        member,
        ctx_view,
        # empty fallback -> role policy decides; explicit member.material_id still wins
        default_material_id="",
    )

    # deterministic cache key (resolved id + appearance-affecting fields)
    mat_key = f"{resolved.id}|{getattr(surface, 'condition', '')}|{getattr(surface, 'finish', '')}|{sample.base_color_hex}|{float(sample.roughness):.4f}|{float(sample.metallic):.4f}"
    mat_hash = hashlib.blake2b(mat_key.encode("utf-8"), digest_size=4).hexdigest()
    mat_name = f"BV_{resolved.id}_{mat_hash}"

    mat = _MATERIAL_CACHE.get(mat_name)
    if mat is None:
        mat = _ensure_bv_material(mat_name, sample)
        _MATERIAL_CACHE[mat_name] = mat

    try:
        _assign_material(obj, mat)
    except Exception as e:
        raise MaterialResolveError(f"Failed to assign Blender material '{mat_name}' to obj='{obj.name}'") from e


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
    col_frame = _ensure_collection("Frame", parent=col_fachwerk)
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
    if not house.get("axis_x") or not house.get("axis_y"):
        raise SchemaError("Invalid house: axis_x/axis_y missing or empty")

    house.setdefault("z0", 0.0)
    house.setdefault("z_plate", 2.2)
    house.setdefault("roof_pitch_deg", 45.0)
    house.setdefault("roof_overhang", 0.35)
    house.setdefault("profile_post", (0.20, 0.20))
    house.setdefault("profile_plate", (0.18, 0.18))


def _log_build_header(house_name: str, house: dict[str, Any]) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("BVILLAGE FACHWERK BUILD START")
    lines.append(f"House      : {house_name}")
    try:
        W = float(house.get("W", 0.0))
        z_plate = float(house.get("z_plate", 2.2))
        fields = house.get("fields", "?")
        lines.append(f"Dims      : fields={fields} | W={W:.3f}m | plate={z_plate:.3f}m")
    except Exception:
        pass
    lines.append(f"Timestamp  : {ts}")
    lines.append("=" * 70)
    LOG.info("\n" + "\n".join(lines))


def _coerce_house(ctx: Any, structure: Any) -> dict[str, Any]:
    """Extract `house` dict from ctx/structure notes or derive from StructurePlan grid."""
    def _is_house(d: Any) -> bool:
        return isinstance(d, dict) and bool(d.get("axis_x")) and bool(d.get("axis_y"))

    def _get_notes(obj: Any) -> Optional[dict[str, Any]]:
        n = getattr(obj, "notes", None)
        return n if isinstance(n, dict) else None

    n = _get_notes(structure)
    if n and _is_house(n.get("house")):
        return n["house"]

    n = _get_notes(ctx)
    if n and _is_house(n.get("house")):
        return n["house"]

    if isinstance(structure, dict):
        nn = structure.get("notes")
        if isinstance(nn, dict) and _is_house(nn.get("house")):
            return nn["house"]
        if _is_house(structure.get("house")):
            return structure["house"]
        if _is_house(structure):
            return structure

    if isinstance(ctx, dict):
        nn = ctx.get("notes")
        if isinstance(nn, dict) and _is_house(nn.get("house")):
            return nn["house"]
        if _is_house(ctx.get("house")):
            return ctx["house"]
        if _is_house(ctx):
            return ctx

    h = getattr(structure, "house", None)
    if _is_house(h):
        return h
    h = getattr(ctx, "house", None)
    if _is_house(h):
        return h

    # derive from structure.grid where possible
    grid = getattr(structure, "grid", None)
    footprint = getattr(structure, "footprint", None)
    if grid is not None and hasattr(grid, "axis_x") and hasattr(grid, "axis_y") and footprint is not None:
        axis_x = list(getattr(grid, "axis_x"))
        axis_y = list(getattr(grid, "axis_y"))
        if axis_x and axis_y:
            z0 = 0.0
            H_e = 2.6
            walls = getattr(structure, "walls", None)
            if walls:
                try:
                    z0 = min(float(w.z[0]) for w in walls)   # type: ignore[attr-defined]
                    H_e = max(float(w.z[1]) for w in walls)  # type: ignore[attr-defined]
                except Exception:
                    pass

            fields = getattr(grid, "fields", None)
            fields_n = len(fields) if isinstance(fields, (list, tuple)) else getattr(grid, "n_fields", None)

            return {
                "axis_x": axis_x,
                "axis_y": axis_y,
                "fields": fields_n if fields_n is not None else "?",
                "L": float(getattr(footprint, "length", max(axis_x) - min(axis_x))),
                "W": float(getattr(footprint, "width", max(axis_y) - min(axis_y))),
                "z0": z0,
                "H_e": H_e,
                "z_plate": 2.2,
                "roof_pitch_deg": 45.0,
                "roof_overhang": 0.35,
                "profile_post": (0.20, 0.20),
                "profile_plate": (0.18, 0.18),
            }

    raise SchemaError(
        "House metadata missing: need house with axis_x/axis_y (from ctx/structure notes OR derivable from structure.grid)."
    )


def _house_basis(house: dict[str, Any]) -> tuple[float, float, float, float]:
    axis_x = list(house["axis_x"])
    axis_y = list(house["axis_y"])
    x_min = float(min(axis_x))
    x_max = float(max(axis_x))
    center_x = 0.5 * (x_min + x_max)
    halfW = 0.5 * float(max(axis_y) - min(axis_y))
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
        obj = _add_beam(col_frame, name=_member_name(mm, fallback="Post"), p0=p0, p1=p1, profile=mm.get("profile") or house.get("profile_post"))
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
        obj = _add_beam(col_frame, name=_member_name(m, fallback="Plate"), p0=p0, p1=p1, profile=m.get("profile") or house.get("profile_plate"))
        _assign_member_material(obj, m, ctx_view)
        built += 1
    return built


def _build_hall_posts_to_ridge(fp: dict[str, Any], house: dict[str, Any], col_frame: bpy.types.Collection, ctx_view: Any) -> int:
    built = 0
    members = fp.get("members") or {}
    posts = members.get("posts") or []
    for mm in posts:
        if str(mm.get("role")) != "HALL_POST":
            continue
        # hall posts may lack z0/z1 in some schemas; tolerate and default to house
        mm2 = dict(mm)
        mm2.setdefault("z0", float(house.get("z0", 0.0)))
        mm2.setdefault("z1", float(house.get("H_e", 2.6)))
        p0, p1 = _map_post_member(mm2, house=house)
        obj = _add_beam(col_frame, name=_member_name(mm2, fallback="HallPost"), p0=p0, p1=p1, profile=mm2.get("profile") or house.get("profile_post"))
        _assign_member_material(obj, mm2, ctx_view)
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
    halfW = 0.5 * float(house.get("W", 0.0))
    return build_roof_per_field(
        axis_x=list(house["axis_x"]),
        half_width=halfW,
        z_plate=float(house.get("z_plate", 2.2)),
        roof_pitch_deg=float(house.get("roof_pitch_deg", 45.0)),
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
        float(house.get("L", 0.0)),
        float(house.get("W", 0.0)),
        float(house.get("z0", 0.0)),
        float(house.get("z_plate", 0.0)),
        float(house.get("roof_pitch_deg", 0.0)),
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
