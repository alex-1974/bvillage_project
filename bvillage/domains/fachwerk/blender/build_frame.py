# bvillage/domains/fachwerk/blender/build_frame.py

import logging
from datetime import datetime
from typing import Any, Dict, Optional, Tuple
import inspect
import hashlib

import bpy
from mathutils import Vector

from bvillage.core.notes import get_domain_artifact
from bvillage.core.materials.material_registry import resolve_for_builder

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.build_frame")


def _call_compat(func, /, **kwargs):
    """Call `func` with only the kwargs it actually accepts."""
    sig = inspect.signature(func)
    for p in sig.parameters.values():
        if p.kind == inspect.Parameter.VAR_KEYWORD:
            return func(**kwargs)
    allowed = set(sig.parameters.keys())
    filtered = {k: v for k, v in kwargs.items() if k in allowed}
    return func(**filtered)


# ------------------------------------------------------------
# Materials (Builder-side, deterministic)
# ------------------------------------------------------------

def _ensure_bv_material(mat_name: str, sample):
    """
    Create/update a Blender material with deterministic Principled BSDF values.

    sample: RenderSample(base_color_hex, roughness, metallic)
    """
    mat = bpy.data.materials.get(mat_name)
    if mat is None:
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True

    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    if bsdf is None:
        bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")

    h = str(sample.base_color_hex).lstrip("#")
    try:
        r = int(h[0:2], 16) / 255.0
        g = int(h[2:4], 16) / 255.0
        b = int(h[4:6], 16) / 255.0
    except Exception:
        r, g, b = 0.8, 0.8, 0.8

    bsdf.inputs["Base Color"].default_value = (r, g, b, 1.0)
    bsdf.inputs["Roughness"].default_value = float(sample.roughness)
    bsdf.inputs["Metallic"].default_value = float(sample.metallic)

    return mat


def _assign_material(obj: bpy.types.Object, mat: bpy.types.Material) -> None:
    if obj is None or obj.data is None:
        return
    mats = obj.data.materials
    if len(mats) == 0:
        mats.append(mat)
    else:
        mats[0] = mat


def _assign_member_material(
    obj: Optional[bpy.types.Object],
    member: Dict[str, Any],
    ctx_view: Any,
    *,
    default_material_id: str,
) -> None:
    if obj is None:
        return
    try:
        resolved, surface, sample = resolve_for_builder(member, ctx_view, default_material_id=default_material_id)
        mat = _ensure_bv_material(f"BV_{resolved.id}", sample)
        _assign_material(obj, mat)
    except Exception:
        LOG.exception("Material assignment failed for obj=%s member=%s", getattr(obj, "name", "?"), member)


def _material_ctx_view(ctx: Any, *, house_name: str) -> dict:
    """
    ctx may be a frozen dataclass -> never mutate it.
    We provide a dict "view" for material resolution + seed-based variation.
    """
    seed = getattr(ctx, "seed", None)
    if seed is None:
        seed = int.from_bytes(
            hashlib.blake2b(str(house_name).encode("utf-8"), digest_size=8).digest(),
            "big",
            signed=False,
        ) & 0x7FFFFFFF

    return {
        "seed": int(seed.base),

        # MVP role → material
        "material_id_default_by_role": {
            # frame
            "PRIMARY_POST": "timber.oak",
            "HALL_POST": "timber.oak",
            "EAVES_PLATE_N": "timber.oak",
            "EAVES_PLATE_S": "timber.oak",
            "EAVES_PLATE_E": "timber.oak",
            "EAVES_PLATE_W": "timber.oak",

            # braces / diagonal timber
            "BRACE": "timber.spruce",

            # infill (future: these roles must exist in infills module)
            "INFILL_BRICK": "brick.historic_mid",
            "INFILL_MORTAR": "mortar.lime_weak",

            # opening frames
            "OPENING_FRAME": "timber.oak",

            # if ever modeled as members
            "GLASS": "glass.soda_lime",
            "IRON": "metal.wrought_iron",
        },

        # MVP role → surface
        "surface_default_by_role": {
            "PRIMARY_POST": {"condition": "aged", "finish": "planed"},
            "HALL_POST": {"condition": "aged", "finish": "planed"},
            "EAVES_PLATE_N": {"condition": "aged", "finish": "planed"},
            "EAVES_PLATE_S": {"condition": "aged", "finish": "planed"},
            "EAVES_PLATE_E": {"condition": "aged", "finish": "planed"},
            "EAVES_PLATE_W": {"condition": "aged", "finish": "planed"},
            "BRACE": {"condition": "aged", "finish": "sawn"},
            "INFILL_BRICK": {"condition": "weathered", "finish": "whitewashed"},
            "INFILL_MORTAR": {"condition": "weathered", "finish": "whitewashed"},
        },
    }


# ------------------------------------------------------------
# Collections & clearing
# ------------------------------------------------------------

def _count_objects(col: bpy.types.Collection) -> int:
    try:
        return len(list(col.all_objects))
    except Exception:
        try:
            return len(col.objects)
        except Exception:
            return 0


def _ensure_collection(name: str, parent: Optional[bpy.types.Collection] = None) -> bpy.types.Collection:
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)

    if parent is None:
        root = bpy.context.scene.collection
        if col.name not in root.children:
            root.children.link(col)
    else:
        if col.name not in parent.children:
            parent.children.link(col)

    return col


def _unlink_and_remove_collection(col: bpy.types.Collection) -> None:
    # 1) Recursively remove children first
    for child in list(col.children):
        _unlink_and_remove_collection(child)

    # 2) Remove objects directly in this collection
    try:
        for obj in list(col.objects):
            try:
                bpy.data.objects.remove(obj, do_unlink=True)
            except Exception:
                pass
    except Exception:
        pass

    # 3) Unlink from parent collections (best-effort)
    try:
        parents = list(getattr(col, "users_collection", []))
        for p in parents:
            try:
                p.children.unlink(col)
            except Exception:
                pass
    except Exception:
        pass

    # 4) Unlink from scene root if linked there
    try:
        root = bpy.context.scene.collection
        if col.name in root.children:
            root.children.unlink(col)
    except Exception:
        pass

    # 5) Remove collection datablock
    try:
        bpy.data.collections.remove(col)
    except Exception:
        pass


def _clear_fachwerk_subtree(col_fachwerk: bpy.types.Collection) -> int:
    removed = 0

    try:
        for obj in list(col_fachwerk.objects):
            try:
                bpy.data.objects.remove(obj, do_unlink=True)
                removed += 1
            except Exception:
                pass
    except Exception:
        pass

    for child in list(col_fachwerk.children):
        try:
            removed += _count_objects(child)
        except Exception:
            pass
        _unlink_and_remove_collection(child)

    return removed


def _ensure_subcollections(root_collection: bpy.types.Collection) -> Dict[str, bpy.types.Collection]:
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


# ------------------------------------------------------------
# House coercion (must provide axis_x/axis_y)
# ------------------------------------------------------------

def _coerce_house(ctx: Any, structure: Any) -> Dict[str, Any]:
    def _is_house(d: Any) -> bool:
        return isinstance(d, dict) and bool(d.get("axis_x")) and bool(d.get("axis_y"))

    def _get_notes(obj: Any) -> Optional[dict]:
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

    raise RuntimeError(
        "House metadata missing: need house with axis_x/axis_y (from ctx/structure notes OR derivable from structure.grid)."
    )


def _require_house_keys(house: Dict[str, Any]) -> None:
    if not house.get("axis_x") or not house.get("axis_y"):
        raise RuntimeError("Invalid house: axis_x/axis_y missing or empty")

    house.setdefault("z0", 0.0)
    house.setdefault("z_plate", 2.2)
    house.setdefault("roof_pitch_deg", 45.0)
    house.setdefault("roof_overhang", 0.35)
    house.setdefault("profile_post", (0.20, 0.20))
    house.setdefault("profile_plate", (0.18, 0.18))


# ------------------------------------------------------------
# Geometry helpers
# ------------------------------------------------------------

def _log_build_header(house_name: str, house: Dict[str, Any]) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
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


def _house_basis(house: Dict[str, Any]) -> Tuple[float, float, float, float]:
    axis_x = house["axis_x"]
    axis_y = house["axis_y"]
    x_min = min(axis_x)
    x_max = max(axis_x)
    center_x = 0.5 * (x_min + x_max)
    y_min = min(axis_y)
    y_max = max(axis_y)
    halfW = 0.5 * (y_max - y_min)
    return x_min, x_max, center_x, halfW


def _map_post_member(member: Dict[str, Any], *, house: Dict[str, Any], z1_cap: Optional[float] = None) -> Tuple[Vector, Vector]:
    x_min, x_max, center_x, halfW = _house_basis(house)
    wall = member["wall"]
    u = float(member["u"])
    z0 = float(member.get("z0", house.get("z0", 0.0)))
    z1 = float(member.get("z1", house.get("z_plate", 2.2)))
    if z1_cap is not None:
        z1 = min(z1, float(z1_cap))

    if wall == "N":
        return Vector((center_x + u, -halfW, z0)), Vector((center_x + u, -halfW, z1))
    if wall == "S":
        return Vector((center_x + u, +halfW, z0)), Vector((center_x + u, +halfW, z1))
    if wall == "E":
        return Vector((x_max, u, z0)), Vector((x_max, u, z1))
    if wall == "W":
        return Vector((x_min, u, z0)), Vector((x_min, u, z1))
    raise ValueError(f"Unknown wall '{wall}'")


def _map_rail_member(member: Dict[str, Any], *, house: Dict[str, Any]) -> Tuple[Vector, Vector]:
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
    raise ValueError(f"Unknown wall '{wall}'")


# ------------------------------------------------------------
# Phase 1/2: members-only posts + plates (NO LEGACY)
# ------------------------------------------------------------

def _build_primary_posts_from_members(fp: Dict[str, Any], house: Dict[str, Any], col_frame: bpy.types.Collection, ctx_view: Any) -> int:
    from .timber import make_beam_rect

    members = fp.get("members")
    if not isinstance(members, dict):
        return 0

    posts = members.get("posts") or []
    if not isinstance(posts, list):
        return 0

    primary = [m for m in posts if isinstance(m, dict) and m.get("role") == "PRIMARY_POST"]
    if not primary:
        return 0

    z_plate = float(house["z_plate"])

    by_wall: Dict[str, list] = {"N": [], "S": [], "E": [], "W": []}
    for m in primary:
        w = m.get("wall")
        if w in by_wall:
            by_wall[w].append(m)

    built = 0
    for wall, arr in by_wall.items():
        if not arr:
            continue
        arr_sorted = sorted(arr, key=lambda mm: float(mm.get("u", 0.0)))
        for i, mm in enumerate(arr_sorted):
            try:
                p0, p1 = _map_post_member(mm, house=house, z1_cap=z_plate)
            except Exception:
                LOG.exception("Phase1/2: invalid PRIMARY_POST member: %s", mm)
                continue

            prof = mm.get("profile") or {}
            w = float(prof.get("w", house["profile_post"][0]))
            d = float(prof.get("d", house["profile_post"][1]))

            name = f"Post_{wall}_{i:02d}"
            make_beam_rect(
                name,
                p0,
                p1,
                width=w,
                depth=d,
                collection=col_frame,
            )
            obj = col_frame.objects.get(name)
            _assign_member_material(obj, mm, ctx_view, default_material_id="timber.oak")
            built += 1

    return built


def _build_plates_from_members(fp: Dict[str, Any], house: Dict[str, Any], col_frame: bpy.types.Collection, ctx_view: Any) -> int:
    from .timber import make_beam_rect

    members = fp.get("members")
    if not isinstance(members, dict):
        return 0

    rails = members.get("rails") or []
    if not isinstance(rails, list):
        return 0

    plate_roles = {"EAVES_PLATE_S", "EAVES_PLATE_N", "EAVES_PLATE_E", "EAVES_PLATE_W"}
    plates = [m for m in rails if isinstance(m, dict) and m.get("role") in plate_roles]
    if not plates:
        return 0

    built = 0
    for m in plates:
        try:
            p0, p1 = _map_rail_member(m, house=house)
        except Exception:
            LOG.exception("Phase1/2: invalid plate member: %s", m)
            continue

        prof = m.get("profile") or {}
        w = float(prof.get("w", house["profile_plate"][0]))
        d = float(prof.get("d", house["profile_plate"][1]))

        wall = str(m.get("wall", "?"))
        name = f"Plate_{wall}"
        make_beam_rect(
            name,
            p0,
            p1,
            width=w,
            depth=d,
            collection=col_frame,
        )
        obj = col_frame.objects.get(name)
        _assign_member_material(obj, m, ctx_view, default_material_id="timber.oak")
        built += 1

    return built


def _build_posts_and_plates(house: Dict[str, Any], fp: Dict[str, Any], col_frame: bpy.types.Collection, ctx_view: Any) -> None:
    built_primary = _build_primary_posts_from_members(fp, house, col_frame, ctx_view)
    if built_primary <= 0:
        raise RuntimeError("members-first required: missing/empty members.posts PRIMARY_POST")

    built_plates = _build_plates_from_members(fp, house, col_frame, ctx_view)
    if built_plates <= 0:
        raise RuntimeError("members-first required: missing/empty members.rails EAVES_PLATE_*")

    LOG.info("Phase1/2: members-first posts=%d plates=%d", built_primary, built_plates)


# ------------------------------------------------------------
# Phase 3: roof, Phase 3.5 hall posts
# ------------------------------------------------------------

def _build_roof(house: Dict[str, Any], col_roof: bpy.types.Collection) -> Dict[str, Any]:
    from .roof import build_roof_per_field

    axis_x = house["axis_x"]
    axis_y = house["axis_y"]
    half_width = 0.5 * (max(axis_y) - min(axis_y))

    return build_roof_per_field(
        axis_x=axis_x,
        half_width=half_width,
        z_plate=float(house["z_plate"]),
        roof_pitch_deg=float(house["roof_pitch_deg"]),
        col_roof=col_roof,
    )


def _build_hall_posts_to_ridge(ctx_view: Any, house: Dict[str, Any], col_frame: bpy.types.Collection, z_ridge: float) -> None:
    from .timber import make_beam_rect

    axis_y = house["axis_y"]
    if 0.0 not in axis_y:
        return

    y = 0.0
    z0 = float(house["z0"])
    w_p, d_p = house["profile_post"]

    for i, x in enumerate(house["axis_x"]):
        name = f"HallPost_{i:02d}"
        make_beam_rect(
            name,
            Vector((x, y, z0)),
            Vector((x, y, z_ridge)),
            width=w_p,
            depth=d_p,
            collection=col_frame,
        )

        # synthetic member for deterministic material/surface
        member = {"role": "HALL_POST", "id": name, "wall": "MID", "u": float(x)}
        obj = col_frame.objects.get(name)
        _assign_member_material(obj, member, ctx_view, default_material_id="timber.oak")


# ------------------------------------------------------------
# Main builder
# ------------------------------------------------------------

def build_frame(
    *,
    ctx: Any,
    structure: Any,
    frameplan: Dict[str, Any],
    root_collection: bpy.types.Collection,
    clear_previous: bool,
) -> bpy.types.Collection:
    cols = _ensure_subcollections(root_collection)

    if clear_previous:
        removed = _clear_fachwerk_subtree(cols["fachwerk"])
        LOG.info("clear_previous=True -> cleared fachwerk subtree, removed_objects=%d", removed)
        cols = _ensure_subcollections(root_collection)

    house = _coerce_house(ctx, structure)
    _require_house_keys(house)

    # NEVER mutate ctx (ctx may be frozen dataclass)
    ctx_view = _material_ctx_view(ctx, house_name=root_collection.name)

    _log_build_header(root_collection.name, house)
    LOG.info("build_frame() ENTER")

    # Contract is now an actual gate (members-first cut)
    from bvillage.domains.fachwerk.core.frameplan_contract import audit_frameplan_contract
    report = audit_frameplan_contract(frameplan, house, strict=False)
    if report.hard:
        print("=== FRAMEPLAN HARD ERRORS ===")
    for h in report.hard:
        print(h)
    if not report.ok:
        raise RuntimeError(f"FramePlan contract failed: hard={len(report.hard)}")

    # Phase1/2 (members-only)
    _build_posts_and_plates(house, frameplan, cols["frame"], ctx_view)
    LOG.info("Phase1/2 posts+plates done")

    # Phase3
    roof_res = _build_roof(house, cols["roof"])
    LOG.info("Phase3 roof done")

    # Phase3.5
    try:
        z_ridge = float(roof_res.get("z_ridge"))
    except Exception:
        z_ridge = float(house["z_plate"]) + 1.0
    _build_hall_posts_to_ridge(ctx_view, house, cols["frame"], z_ridge)
    LOG.info("Hall posts through to ridge done")

    from bvillage.domains.fachwerk.core.frameplan import normalize_frameplan_dict
    frameplan = normalize_frameplan_dict(frameplan)

    # Phase4 modules (members-only inside their modules)
    from .opening_frames import build_opening_frames
    from .braces import build_braces_corner_band
    from .infills import build_infills
    from .integrity import check_integrity

    _call_compat(build_opening_frames, fp=frameplan, house=house,
             collection=cols["openings"], ctx_view=ctx_view)
    LOG.info("Phase4B opening frames done")

    _call_compat(build_braces_corner_band, fp=frameplan, house=house,
             collection=cols["braces"], ctx_view=ctx_view)
    LOG.info("Phase4C braces done")

    _call_compat(build_infills, fp=frameplan, house=house,
             collection=cols["infills"], ctx_view=ctx_view)
    LOG.info("Phase4A infills done")

    LOG.info(
        "BUILD SUMMARY | cols: frame=%d roof=%d openings=%d braces=%d infills=%d debug=%d",
        _count_objects(cols["frame"]),
        _count_objects(cols["roof"]),
        _count_objects(cols["openings"]),
        _count_objects(cols["braces"]),
        _count_objects(cols["infills"]),
        _count_objects(cols["debug"]),
    )
    LOG.info("scene objects total=%d", len(bpy.data.objects))

    ok = check_integrity(fp=frameplan, house=house, collections=cols)
    if not ok:
        raise RuntimeError("Integrity check failed (see previous errors)")

    return cols["fachwerk"]


# ------------------------------------------------------------
# Public API (explicit)
# ------------------------------------------------------------

def build_fachwerk_frame(
    *,
    ctx: Any,
    structure: Any,
    frameplan: Dict[str, Any],
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


# ------------------------------------------------------------
# Legacy wrapper (artifact fetch only; NOT geometry legacy)
# ------------------------------------------------------------

def build_fachwerk_frame_from_structure_notes(
    *,
    ctx: Any,
    structure: Any,
    root_collection: bpy.types.Collection,
    clear_previous: bool = True,
) -> bpy.types.Collection:
    notes = getattr(structure, "notes", None)
    if not isinstance(notes, dict):
        raise RuntimeError("StructurePlan.notes missing/invalid; cannot read fachwerk.frameplan")

    fp_dict = get_domain_artifact(
        notes,
        domain="fachwerk",
        artifact="frameplan",
        legacy_aliases=("frameplan", "fachwerk.frameplan"),
    )
    if fp_dict is None:
        raise RuntimeError("Missing required artifact: fachwerk.frameplan")

    return build_fachwerk_frame(
        ctx=ctx,
        structure=structure,
        frameplan=fp_dict,
        root_collection=root_collection,
        clear_previous=clear_previous,
    )
