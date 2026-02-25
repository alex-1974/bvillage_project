# bvillage/domains/fachwerk/blender/build_frame.py
#
# Fachwerk Hallenhaus — Frame builder (Phase 3/4)
#
# Phases:
# - Phase1/2: posts + plates (basic wall scaffold)
# - Phase3  : roof per field (ridge/rafters/collars)
# - Phase3.5: hall posts through to ridge
# - Phase4B : opening frames (module opening_frames.py)
# - Phase4C : knee braces (corner-only) (module braces.py)
# - Phase4A : infills (Gefache) (module infills.py)
#
# Quality:
# - Pre-flight: FramePlan contract audit (data-only) before building.
# - Post-flight: Build integrity check (scene vs plan) after building.
#
# Logging:
# - No prints. All through logger.
# - End-of-build summary logs per collection counts.
#
# Clearing:
# - Robust clear_previous: deletes whole fachwerk subtree under House_* collection.
# - FORCE_CLEAR_PREVIOUS overrides runner argument.

import logging
from datetime import datetime
from typing import Any, Dict, Optional

import bpy
from mathutils import Vector

from bvillage.core.notes import get_domain_artifact
from .roof import build_roof_per_field
from .timber import make_beam_rect

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.build_frame")

# If you ALWAYS want clean rebuilds, keep this True.
# If you want to respect the runner's clear_previous argument, set to False.
FORCE_CLEAR_PREVIOUS = True


# ------------------------------------------------------------
# Small helpers (module level, no scope surprises)
# ------------------------------------------------------------

def _count_objects(col: bpy.types.Collection) -> int:
    """Count objects in a collection (including children)."""
    try:
        return sum(1 for _ in col.all_objects)
    except Exception:
        try:
            return len(col.objects)
        except Exception:
            return 0


def _log_build_header(house_name: str, meta: Optional[dict] = None) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append("=" * 70)
    lines.append("BVILLAGE FACHWERK BUILD START")
    lines.append(f"House      : {house_name}")

    if meta:
        order = ["type", "region", "epoch", "wealth", "seed", "dims"]
        for k in order:
            v = meta.get(k)
            if v is None:
                continue
            label = (k.capitalize() if k != "dims" else "Dims").ljust(10)
            lines.append(f"{label}: {v}")

    lines.append(f"Timestamp  : {ts}")
    lines.append("=" * 70)

    LOG.info("\n" + "\n".join(lines))


def _resolve_root_collection(root_collection):
    """
    root_collection may be:
      - None -> scene root collection
      - str  -> collection name
      - bpy.types.Collection
    """
    if root_collection is None:
        return bpy.context.scene.collection
    if isinstance(root_collection, str):
        return bpy.data.collections.get(root_collection) or bpy.context.scene.collection
    return root_collection


def _ensure_collection(name: str, parent: bpy.types.Collection) -> bpy.types.Collection:
    """Ensure collection exists and is linked under parent."""
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)

    # Ensure linked under parent
    if col.name not in [c.name for c in parent.children]:
        parent.children.link(col)

    return col


def _clear_collection_tree(col: bpy.types.Collection) -> int:
    """
    Recursively delete all objects in the subtree of collection `col`
    and remove child collections. Returns number of removed objects.
    """
    removed = 0

    # Collect objects recursively
    objs = set(col.objects)
    for child in col.children_recursive:
        objs.update(child.objects)

    # Remove objects
    for obj in list(objs):
        try:
            for c in list(obj.users_collection):
                c.objects.unlink(obj)
            bpy.data.objects.remove(obj, do_unlink=True)
            removed += 1
        except Exception:
            LOG.exception("Failed to remove object: %s", getattr(obj, "name", "?"))

    # Remove child collections (bottom-up)
    for child in list(col.children_recursive):
        try:
            bpy.data.collections.remove(child)
        except Exception:
            LOG.exception("Failed to remove collection: %s", child.name)

    return removed


def _best_root_house_name(root_collection) -> str:
    """
    Try to determine intended instance name from root_collection.
    Prefer names like "House_42".
    """
    if root_collection is None:
        return "House"
    if isinstance(root_collection, str):
        return root_collection
    if hasattr(root_collection, "name"):
        return str(root_collection.name)
    return "House"


# ------------------------------------------------------------
# House adapter (structure notes -> internal house dict)
# ------------------------------------------------------------

def _coerce_house(structure, fallback_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Adapter from BVILLAGE structure object/dict -> internal dict used by build_frame().

    - axis_x/axis_y directly, else structure.grid.axis_x/axis_y
    - if axis_y missing but width W exists: axis_y = [-W/2, 0, +W/2]
    - name: structure.name -> overridden if placeholder -> fallback_name -> "House"
    - adds "_meta" dict for header display (best effort)
    """

    def _ctx_get(ctx, key, default=None):
        if ctx is None:
            return default
        if isinstance(ctx, dict):
            return ctx.get(key, default)
        return getattr(ctx, key, default)

    # -------- extract ----------
    if isinstance(structure, dict):
        axis_x = structure.get("axis_x")
        axis_y = structure.get("axis_y")

        grid = structure.get("grid")
        if axis_x is None and isinstance(grid, dict):
            axis_x = grid.get("axis_x")
        if axis_y is None and isinstance(grid, dict):
            axis_y = grid.get("axis_y")

        dims = structure.get("dims")
        W = None
        if isinstance(dims, dict):
            W = dims.get("W") or dims.get("width")
        if W is None:
            W = structure.get("W") or structure.get("width")

        z0 = structure.get("z0", 0.0)
        z_plate = structure.get("z_plate") or structure.get("plate_z") or 2.2

        roof_pitch_deg = structure.get("roof_pitch_deg") or structure.get("roof_pitch") or 50.0
        kehl_frac = structure.get("kehl_frac") or structure.get("collar_frac") or 0.58

        name = structure.get("name") or structure.get("house_name") or None
        meta = structure.get("_meta") or structure.get("meta") or {}
    else:
        axis_x = _ctx_get(structure, "axis_x", None)
        axis_y = _ctx_get(structure, "axis_y", None)

        grid = _ctx_get(structure, "grid", None)
        if axis_x is None and grid is not None:
            axis_x = _ctx_get(grid, "axis_x", None)
        if axis_y is None and grid is not None:
            axis_y = _ctx_get(grid, "axis_y", None)

        footprint = _ctx_get(structure, "footprint", None)
        W = None
        if footprint is not None:
            W = _ctx_get(footprint, "width", None) or _ctx_get(footprint, "W", None)
        if W is None:
            W = _ctx_get(structure, "W", None) or _ctx_get(structure, "width", None)

        z0 = float(_ctx_get(structure, "z0", 0.0))
        z_plate = float(_ctx_get(structure, "z_plate", _ctx_get(structure, "plate_z", 2.2)))

        roof_pitch_deg = float(_ctx_get(structure, "roof_pitch_deg", _ctx_get(structure, "roof_pitch", 50.0)))
        kehl_frac = float(_ctx_get(structure, "kehl_frac", _ctx_get(structure, "collar_frac", 0.58)))

        name = _ctx_get(structure, "name", None) or _ctx_get(structure, "house_name", None)
        meta = _ctx_get(structure, "_meta", None) or _ctx_get(structure, "meta", None) or {}

    if axis_x is None:
        raise ValueError("structure must provide axis_x (or structure.grid.axis_x)")
    if axis_y is None:
        if W is None:
            raise ValueError("structure must provide axis_y (or width W to derive axis_y)")
        W = float(W)
        axis_y = [-W / 2.0, 0.0, +W / 2.0]

    axis_x = [float(x) for x in axis_x]
    axis_y = [float(y) for y in axis_y]

    # name selection (avoid placeholder "Structure")
    placeholder_names = {"structure", "struct", "house", "bldg", "building", "object", "data"}
    name_norm = str(name).strip().lower() if name is not None else ""
    fb_norm = str(fallback_name).strip() if fallback_name else ""

    if (not name_norm) or (name_norm in placeholder_names):
        name = fallback_name or "House"
    else:
        # prefer House_XX if provided by runner
        if fallback_name and fb_norm.lower().startswith("house_") and not name_norm.startswith("house_"):
            name = fallback_name

    # Meta best effort
    meta_out: Dict[str, Any] = {}
    if isinstance(meta, dict):
        meta_out.update(meta)
    if "dims" not in meta_out:
        try:
            meta_out["dims"] = f"fields={len(axis_x)-1} | W={abs(axis_y[0])*2:.3f}m | plate={z_plate:.3f}m"
        except Exception:
            pass

    # Profiles (meters) — phase3 defaults
    profile_post = (0.18, 0.18)         # w,d
    profile_plate = (0.16, 0.20)        # w,d
    profile_post_hall = (0.20, 0.20)    # for posts reaching ridge
    profile_rafter = (0.12, 0.18)

    return {
        "name": str(name),
        "axis_x": axis_x,
        "axis_y": axis_y,
        "z0": float(z0),
        "z_plate": float(z_plate),
        "roof_pitch_deg": float(roof_pitch_deg),
        "kehl_frac": float(kehl_frac),
        "profile_post": profile_post,
        "profile_plate": profile_plate,
        "profile_post_hall": profile_post_hall,
        "profile_rafter": profile_rafter,
        "_meta": meta_out,
    }


# ------------------------------------------------------------
# Phase 1/2: posts + plates
# ------------------------------------------------------------

def _build_posts_and_plates(house: Dict[str, Any], col_frame: bpy.types.Collection) -> None:
    axis_x = house["axis_x"]
    axis_y = house["axis_y"]
    z0 = house["z0"]
    z_plate = house["z_plate"]

    w_p, d_p = house["profile_post"]
    w_pl, d_pl = house["profile_plate"]

    # perimeter posts at each axis_x for both walls (S/N)
    for i, x in enumerate(axis_x):
        # South wall (axis_y[0])
        make_beam_rect(
            f"Post_S_{i:02d}",
            Vector((x, axis_y[0], z0)),
            Vector((x, axis_y[0], z_plate)),
            width=w_p,
            depth=d_p,
            collection=col_frame,
        )
        # North wall (axis_y[-1])
        make_beam_rect(
            f"Post_N_{i:02d}",
            Vector((x, axis_y[-1], z0)),
            Vector((x, axis_y[-1], z_plate)),
            width=w_p,
            depth=d_p,
            collection=col_frame,
        )

    # Plates (Rähm) along S/N
    make_beam_rect(
        "Plate_S",
        Vector((axis_x[0], axis_y[0], z_plate)),
        Vector((axis_x[-1], axis_y[0], z_plate)),
        width=w_pl,
        depth=d_pl,
        collection=col_frame,
    )
    make_beam_rect(
        "Plate_N",
        Vector((axis_x[0], axis_y[-1], z_plate)),
        Vector((axis_x[-1], axis_y[-1], z_plate)),
        width=w_pl,
        depth=d_pl,
        collection=col_frame,
    )


# ------------------------------------------------------------
# Phase 3: roof
# ------------------------------------------------------------

def _build_roof(house: Dict[str, Any], col_roof: bpy.types.Collection) -> Dict[str, Any]:
    axis_x = house["axis_x"]
    axis_y = house["axis_y"]
    z_plate = house["z_plate"]
    roof_pitch_deg = house["roof_pitch_deg"]
    kehl_frac = house["kehl_frac"]

    # roof expects half_width (W/2)
    half_width = abs(float(axis_y[0]))

    profiles = {
        "ridge": (0.18, 0.22),
        "rafter": tuple(house.get("profile_rafter", (0.10, 0.16))),
        "collar": (0.12, 0.16),
    }

    roof_res = build_roof_per_field(
        axis_x=axis_x,
        half_width=half_width,
        z_plate=z_plate,
        roof_pitch_deg=roof_pitch_deg,
        kehl_frac=kehl_frac,
        col_roof=col_roof,
        profiles=profiles,
    )
    return roof_res


# ------------------------------------------------------------
# Phase 3.5: Hall posts up to ridge
# ------------------------------------------------------------

def _build_hall_posts_to_ridge(house: Dict[str, Any], col_frame: bpy.types.Collection, z_ridge: float) -> None:
    axis_x = house["axis_x"]
    z0 = house["z0"]
    w_h, d_h = house["profile_post_hall"]

    for i, x in enumerate(axis_x):
        make_beam_rect(
            f"Post_HALL_{i:02d}",
            Vector((x, 0.0, z0)),
            Vector((x, 0.0, z_ridge)),
            width=w_h,
            depth=d_h,
            collection=col_frame,
        )


# ------------------------------------------------------------
# Main internal entry
# ------------------------------------------------------------

def build_frame(house: Dict[str, Any], root_collection=None, clear_previous: bool = False) -> Dict[str, Any]:
    LOG.info("build_frame() ENTER")

    root = _resolve_root_collection(root_collection)
    house_name = house.get("name", "House")

    col_fachwerk = _ensure_collection(f"{house_name}_Fachwerk", root)

    # Phase collections
    col_frame = _ensure_collection("Frame", col_fachwerk)
    col_roof = _ensure_collection("Roof", col_fachwerk)
    col_openings = _ensure_collection("Openings", col_fachwerk)
    col_braces = _ensure_collection("Braces", col_fachwerk)
    col_infills = _ensure_collection("Infills", col_fachwerk)
    col_debug = _ensure_collection("Debug", col_fachwerk)

    if clear_previous:
        removed = _clear_collection_tree(col_fachwerk)
        LOG.info("clear_previous=True -> cleared fachwerk subtree, removed_objects=%d", removed)

        # recreate children after wipe
        col_frame = _ensure_collection("Frame", col_fachwerk)
        col_roof = _ensure_collection("Roof", col_fachwerk)
        col_openings = _ensure_collection("Openings", col_fachwerk)
        col_braces = _ensure_collection("Braces", col_fachwerk)
        col_infills = _ensure_collection("Infills", col_fachwerk)
        col_debug = _ensure_collection("Debug", col_fachwerk)

    # FramePlan artifact attached by wrapper
    fp_dict = house.get("_frameplan")

    # --------------------------------------------------------
    # Pre-flight: FramePlan contract audit (data-only)
    # --------------------------------------------------------
    if isinstance(fp_dict, dict):
        try:
            from bvillage.domains.fachwerk.core.frameplan_contract import audit_frameplan_contract
            audit_frameplan_contract(fp_dict, house, strict=False)
        except Exception:
            # keep building, but make it extremely visible
            LOG.exception("FramePlan contract audit failed unexpectedly")
    else:
        LOG.info("FramePlan contract audit skipped (no frameplan artifact found)")

    _build_posts_and_plates(house, col_frame)
    LOG.info("Phase1/2 posts+plates done")

    roof_res = _build_roof(house, col_roof)
    LOG.info("Phase3 roof done")

    _build_hall_posts_to_ridge(house, col_frame, roof_res["z_ridge"])
    LOG.info("Hall posts through to ridge done")

    # --------------------------------------------------------
    # Phase 4B: Opening frames
    # --------------------------------------------------------
    if isinstance(fp_dict, dict):
        try:
            from .opening_frames import build_opening_frames
            build_opening_frames(
                fp=fp_dict,
                house=house,
                collection=col_openings,
            )
            LOG.info("Phase4B opening frames done")
        except ModuleNotFoundError:
            LOG.info("Phase4B opening frames skipped (opening_frames.py not present)")
        except Exception:
            LOG.exception("Phase4B opening frames failed")

    # --------------------------------------------------------
    # Phase 4C: Knee braces (corner-only)
    # --------------------------------------------------------
    if isinstance(fp_dict, dict):
        try:
            from .braces import build_knee_braces_corner_only, BraceConfig
            build_knee_braces_corner_only(
                fp=fp_dict,
                house=house,
                collection=col_braces,
                config=BraceConfig(debug=True),
                debug_collection=col_debug,
            )
            LOG.info("Phase4C braces done")
        except ModuleNotFoundError:
            LOG.info("Phase4C braces skipped (braces.py not present)")
        except Exception:
            LOG.exception("Phase4C braces failed")

    # --------------------------------------------------------
    # Phase 4A: Infills (Gefache)
    # --------------------------------------------------------
    if isinstance(fp_dict, dict):
        try:
            from .infills import build_infills, InfillConfig
            build_infills(
                fp=fp_dict,
                house=house,
                collection=col_infills,
                config=InfillConfig(debug=True),
                debug_collection=col_debug,
            )
            LOG.info("Phase4A infills done")
        except Exception:
            LOG.exception("Phase4A infills failed")
    else:
        LOG.info("Phase4A infills skipped (no frameplan artifact found)")

    # --------------------------------------------------------
    # End summary (IMPORTANT: must be inside build_frame scope)
    # --------------------------------------------------------
    LOG.info(
        "BUILD SUMMARY | cols: frame=%d roof=%d openings=%d braces=%d infills=%d debug=%d",
        _count_objects(col_frame),
        _count_objects(col_roof),
        _count_objects(col_openings),
        _count_objects(col_braces),
        _count_objects(col_infills),
        _count_objects(col_debug),
    )

    # Optional: keep your old roof count (scene-wide) if you like
    try:
        names = [o.name for o in bpy.context.scene.objects]
        roof_count = sum(n.startswith(("Rafter_", "Kehlbalken_", "Firstpfette")) for n in names)
        LOG.info("scene objects total=%d", len(names))
        LOG.info("roof=%d", roof_count)
    except Exception:
        LOG.exception("Failed to compute scene stats")

    # --------------------------------------------------------
    # Post-flight: Build integrity audit (scene vs plan)
    # --------------------------------------------------------
    if isinstance(fp_dict, dict):
        try:
            # Current module name: integrity.py (we can rename later to build_contract.py)
            from .integrity import run_integrity_checks, IntegrityConfig
            run_integrity_checks(
                fp=fp_dict,
                house=house,
                col_frame=col_frame,
                col_roof=col_roof,
                col_openings=col_openings,
                col_braces=col_braces,
                col_infills=col_infills,
                col_debug=col_debug,
                config=IntegrityConfig(strict=False, tol_plane=0.03),
            )
        except ModuleNotFoundError:
            LOG.info("Post-flight integrity skipped (integrity.py not present)")
        except Exception:
            LOG.exception("Post-flight integrity failed unexpectedly")
    else:
        LOG.info("Post-flight integrity skipped (no frameplan artifact)")

    return {
        "z_ridge": roof_res.get("z_ridge"),
        "z_kehl": roof_res.get("z_kehl"),
        "y_kehl": roof_res.get("y_kehl"),
    }


# ------------------------------------------------------------
# BVILLAGE expected symbol (public API)
# ------------------------------------------------------------

def build_fachwerk_frame_from_structure_notes(*args, **kwargs) -> Dict[str, Any]:
    """
    BVILLAGE runner entrypoint.
    Typically called with:
      structure=..., root_collection=..., clear_previous=True/False
    """
    LOG.info("wrapper ENTER keys=%s", list(kwargs.keys()))

    structure = kwargs.get("structure") or kwargs.get("structure_notes") or (args[0] if args else None)
    if structure is None:
        raise TypeError("build_fachwerk_frame_from_structure_notes: missing structure")

    rc = kwargs.get("root_collection")
    house_instance_name = _best_root_house_name(rc)
    house = _coerce_house(structure, fallback_name=house_instance_name)

    # Attach FramePlan artifact from notes (optional)
    fp_dict = None
    try:
        notes = getattr(structure, "notes", None)
        if isinstance(structure, dict):
            notes = structure.get("notes") or notes
        if isinstance(notes, dict):
            fp_dict = get_domain_artifact(
                notes,
                domain="fachwerk",
                name="frameplan",
                legacy_aliases=("frameplan", "fachwerk.frameplan"),
            )
    except Exception:
        fp_dict = None

    if isinstance(fp_dict, dict):
        house["_frameplan"] = fp_dict

    # Clear behavior
    runner_clear = bool(kwargs.get("clear_previous", False))
    clear_effective = True if FORCE_CLEAR_PREVIOUS else runner_clear
    LOG.info(
        "clear_previous runner=%s effective=%s (FORCE_CLEAR_PREVIOUS=%s)",
        runner_clear,
        clear_effective,
        FORCE_CLEAR_PREVIOUS,
    )

    _log_build_header(house["name"], meta=house.get("_meta"))

    return build_frame(
        house,
        root_collection=rc,
        clear_previous=clear_effective,
    )
