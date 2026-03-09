# bvillage/domains/timber_frame/blender/materials_adapter.py
from __future__ import annotations

import hashlib
import logging
from dataclasses import asdict, is_dataclass
from typing import Any

import bpy

LOG = logging.getLogger(__name__)

__all__ = ["apply_material_to_object"]


_MATERIAL_CACHE: dict[str, bpy.types.Material] = {}


def _seed_fingerprint(ctx: Any) -> str:
    """
    Extract a stable, reproducible seed fingerprint from ctx.

    Supports:
    - ctx.seed where seed may be int or object with .base
    - dict ctx with key "seed"
    """
    seed = None
    try:
        seed = getattr(ctx, "seed", None)
    except Exception:
        seed = None

    if seed is None and isinstance(ctx, dict):
        seed = ctx.get("seed", None)

    if seed is None:
        return ""

    base = getattr(seed, "base", None)
    if base is not None:
        return str(base)

    return str(seed)


def _sample_fingerprint(sample: Any) -> str:
    """
    Serialize a RenderSample-like object into a stable string.
    """
    base = str(getattr(sample, "base_color_hex", ""))
    rough = getattr(sample, "roughness", 0.0)
    metal = getattr(sample, "metallic", 0.0)

    try:
        rough_f = float(rough)
    except Exception:
        rough_f = 0.0
    try:
        metal_f = float(metal)
    except Exception:
        metal_f = 0.0

    return f"base={base}|rough={rough_f:.6f}|metal={metal_f:.6f}"


def _surface_fingerprint(surface: Any) -> str:
    """
    SurfaceSpec-like fingerprint (best effort).
    """
    if surface is None:
        return ""

    sid = getattr(surface, "id", None)
    if sid is not None:
        return str(sid)

    name = getattr(surface, "name", None)
    if name is not None:
        return str(name)

    if is_dataclass(surface):
        try:
            return str(asdict(surface))
        except Exception:
            return surface.__class__.__name__

    if isinstance(surface, dict):
        items = "|".join(f"{k}={surface[k]!r}" for k in sorted(surface.keys()))
        return items

    return surface.__class__.__name__


def _resolved_fingerprint(resolved: Any) -> str:
    """
    MaterialResolved-like fingerprint (best effort).
    """
    if resolved is None:
        return ""
    rid = getattr(resolved, "id", None)
    if rid is not None:
        return str(rid)
    return str(resolved)


def _material_cache_key(
    *,
    resolved: Any,
    surface: Any,
    sample: Any,
    ctx: Any,
    member: dict[str, Any],
) -> str:
    """
    Deterministic cache key for bpy.material reuse.

    Includes:
    - resolved material id
    - surface spec id
    - sample params
    - seed fingerprint
    - member role + explicit material_id
    """
    seed_fp = _seed_fingerprint(ctx)
    resolved_fp = _resolved_fingerprint(resolved)
    surface_fp = _surface_fingerprint(surface)
    sample_fp = _sample_fingerprint(sample)

    role = str(member.get("role", ""))
    material_id = str(member.get("material_id", ""))

    key_version = "v1"
    payload = f"{key_version}|{resolved_fp}|{surface_fp}|{sample_fp}|seed={seed_fp}|role={role}|mid={material_id}"
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def _hex_to_rgb01(hex_str: str) -> tuple[float, float, float]:
    """
    Parse '#RRGGBB' or 'RRGGBB' into [0..1] floats.
    """
    s = hex_str.strip()
    if s.startswith("#"):
        s = s[1:]
    if len(s) != 6:
        raise ValueError(f"Invalid hex color: {hex_str!r}")

    r = int(s[0:2], 16) / 255.0
    g = int(s[2:4], 16) / 255.0
    b = int(s[4:6], 16) / 255.0
    return r, g, b


def _ensure_principled_material(
    *,
    name: str,
    sample: Any,
) -> bpy.types.Material:
    """
    Create/update a Principled-BSDF material from RenderSample-like fields.
    """
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    principled = None
    output = None
    for n in nodes:
        if n.type == "BSDF_PRINCIPLED":
            principled = n
        elif n.type == "OUTPUT_MATERIAL":
            output = n

    if principled is None:
        principled = nodes.new(type="ShaderNodeBsdfPrincipled")
        principled.location = (0, 0)

    if output is None:
        output = nodes.new(type="ShaderNodeOutputMaterial")
        output.location = (300, 0)

    for l in list(output.inputs["Surface"].links):
        links.remove(l)
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])

    base_hex = str(getattr(sample, "base_color_hex", "#b0b0b0") or "#b0b0b0")
    try:
        r, g, b = _hex_to_rgb01(base_hex)
    except Exception:
        r, g, b = (0.69, 0.69, 0.69)

    rough = getattr(sample, "roughness", 0.5)
    metal = getattr(sample, "metallic", 0.0)
    try:
        rough_f = float(rough)
    except Exception:
        rough_f = 0.5
    try:
        metal_f = float(metal)
    except Exception:
        metal_f = 0.0

    principled.inputs["Base Color"].default_value = (r, g, b, 1.0)
    principled.inputs["Roughness"].default_value = max(0.0, min(1.0, rough_f))
    principled.inputs["Metallic"].default_value = max(0.0, min(1.0, metal_f))

    return mat


def apply_material_to_object(
    *,
    obj: bpy.types.Object | None,
    resolved: Any,
    surface: Any,
    sample: Any,
    ctx: Any,
    member: dict[str, Any],
    name_hint: str | None = None,
) -> None:
    """
    Assign a deterministic material to obj based on
    (resolved, surface, sample, ctx, member).

    This module is the only place that:
    - computes cache keys
    - caches bpy.materials
    - builds node graphs
    """
    if obj is None:
        return

    cache_key = _material_cache_key(
        resolved=resolved,
        surface=surface,
        sample=sample,
        ctx=ctx,
        member=member,
    )

    mat = _MATERIAL_CACHE.get(cache_key)
    if mat is None:
        material_name = name_hint or f"BV_MAT_{cache_key[:12]}"
        mat = _ensure_principled_material(
            name=material_name,
            sample=sample,
        )
        _MATERIAL_CACHE[cache_key] = mat

    if obj.data is None or not hasattr(obj.data, "materials"):
        return

    mats = obj.data.materials
    if mats:
        mats[0] = mat
    else:
        mats.append(mat)
