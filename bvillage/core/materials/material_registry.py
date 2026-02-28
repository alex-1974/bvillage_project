# bvillage/core/materials/material_registry.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping, Optional
import hashlib


# =============================================================================
# BVILLAGE v0.4.0 — MaterialRegistry
# -----------------------------------------------------------------------------
# Goals (MVP):
# - Single source of truth for materials: physics + render defaults
# - Stable IDs, deterministic render sampling (seed+salt), no global RNG
# - Condition/Finish are modifiers (NOT part of material_id)
# - ProductForm / SectionProfile live on member/geometry, not here
# =============================================================================


# -----------------------------------------------------------------------------
# TYPES
# -----------------------------------------------------------------------------

MaterialFamily = Literal["timber", "brick", "stone", "mortar", "concrete", "glass", "metal"]

Condition = Literal["fresh", "weathered", "aged"]
Finish = Literal["sawn", "planed", "oiled", "painted", "whitewashed", "tarred"]


@dataclass(frozen=True, slots=True)
class PhysProps:
    density_kg_m3: float
    E_GPa: float
    bend_MPa: float
    comp_MPa: Optional[float] = None
    shear_MPa: Optional[float] = None


@dataclass(frozen=True, slots=True)
class RenderProfile:
    base_color_hex: str
    roughness: float
    metallic: float = 0.0
    palette: tuple[str, ...] = ()
    jitters: Mapping[str, float] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class MaterialBase:
    id: str
    family: MaterialFamily
    phys: PhysProps
    render_default: RenderProfile


@dataclass(frozen=True, slots=True)
class MaterialVariant:
    id: str
    base_id: str
    phys_override: Optional[PhysProps] = None
    render: Optional[RenderProfile] = None


@dataclass(frozen=True, slots=True)
class MaterialResolved:
    id: str
    base: MaterialBase
    phys: PhysProps
    render: RenderProfile


@dataclass(frozen=True, slots=True)
class SurfaceSpec:
    condition: Condition = "fresh"
    finish: Finish = "planed"


@dataclass(frozen=True, slots=True)
class RenderSample:
    base_color_hex: str
    roughness: float
    metallic: float


# -----------------------------------------------------------------------------
# MVP MATERIAL CATALOG (v0.4.0)
# NOTE: These are plausible start values for pipeline stability.
#       Fine-tuning / region-era-wealth constraints belong to Policy later.
# -----------------------------------------------------------------------------

BASES: dict[str, MaterialBase] = {
    # --- TIMBER BASES ---
    "timber.hardwood": MaterialBase(
        id="timber.hardwood",
        family="timber",
        phys=PhysProps(density_kg_m3=700.0, E_GPa=12.0, bend_MPa=90.0, comp_MPa=45.0, shear_MPa=10.0),
        render_default=RenderProfile(
            base_color_hex="#8A6B4F",
            roughness=0.65,
            palette=("#7B5A3E", "#8A6B4F", "#9A7A5C", "#6A4E36"),
            jitters={"roughness": 0.06, "value": 0.08},
        ),
    ),
    "timber.softwood": MaterialBase(
        id="timber.softwood",
        family="timber",
        phys=PhysProps(density_kg_m3=450.0, E_GPa=9.0, bend_MPa=65.0, comp_MPa=30.0, shear_MPa=7.0),
        render_default=RenderProfile(
            base_color_hex="#B28B62",
            roughness=0.70,
            palette=("#A37D56", "#B28B62", "#C39C73", "#8F6B47"),
            jitters={"roughness": 0.07, "value": 0.10},
        ),
    ),
    # --- BRICK / STONE BASES ---
    "brick.generic": MaterialBase(
        id="brick.generic",
        family="brick",
        phys=PhysProps(density_kg_m3=1800.0, E_GPa=10.0, bend_MPa=8.0, comp_MPa=20.0, shear_MPa=3.0),
        render_default=RenderProfile(
            base_color_hex="#8B4A3B",
            roughness=0.85,
            palette=("#7B3F33", "#8B4A3B", "#9B5A49", "#6E392F"),
            jitters={"roughness": 0.04, "value": 0.10},
        ),
    ),
    "stone.sandstone": MaterialBase(
        id="stone.sandstone",
        family="stone",
        phys=PhysProps(density_kg_m3=2200.0, E_GPa=25.0, bend_MPa=12.0, comp_MPa=60.0, shear_MPa=8.0),
        render_default=RenderProfile(
            base_color_hex="#C7B58F",
            roughness=0.90,
            palette=("#BFAE86", "#C7B58F", "#D2C29E", "#AFA07D"),
            jitters={"roughness": 0.03, "value": 0.07},
        ),
    ),
    "stone.granite": MaterialBase(
        id="stone.granite",
        family="stone",
        phys=PhysProps(density_kg_m3=2700.0, E_GPa=55.0, bend_MPa=15.0, comp_MPa=130.0, shear_MPa=12.0),
        render_default=RenderProfile(
            base_color_hex="#8C8C8C",
            roughness=0.80,
            palette=("#7E7E7E", "#8C8C8C", "#9A9A9A", "#6F6F6F"),
            jitters={"roughness": 0.03, "value": 0.06},
        ),
    ),
    # --- MORTAR / CONCRETE BASES ---
    "mortar.lime": MaterialBase(
        id="mortar.lime",
        family="mortar",
        phys=PhysProps(density_kg_m3=1600.0, E_GPa=2.5, bend_MPa=1.5, comp_MPa=3.0, shear_MPa=1.0),
        render_default=RenderProfile(
            base_color_hex="#D6D1C6",
            roughness=0.95,
            palette=("#CEC7BA", "#D6D1C6", "#E0DBD1", "#C2BCAE"),
            jitters={"roughness": 0.02, "value": 0.05},
        ),
    ),
    "mortar.hydraulic": MaterialBase(
        id="mortar.hydraulic",
        family="mortar",
        phys=PhysProps(density_kg_m3=1700.0, E_GPa=5.0, bend_MPa=2.5, comp_MPa=10.0, shear_MPa=2.0),
        render_default=RenderProfile(
            base_color_hex="#CFC9BD",
            roughness=0.93,
            palette=("#C6BFB3", "#CFC9BD", "#DAD4C9", "#BEB7AB"),
            jitters={"roughness": 0.02, "value": 0.05},
        ),
    ),
    "concrete.generic": MaterialBase(
        id="concrete.generic",
        family="concrete",
        phys=PhysProps(density_kg_m3=2400.0, E_GPa=30.0, bend_MPa=4.0, comp_MPa=30.0, shear_MPa=5.0),
        render_default=RenderProfile(
            base_color_hex="#B7B7B7",
            roughness=0.92,
            palette=("#AFAFAF", "#B7B7B7", "#C0C0C0", "#9F9F9F"),
            jitters={"roughness": 0.02, "value": 0.04},
        ),
    ),
    # --- GLASS / METAL BASES ---
    "glass.soda_lime": MaterialBase(
        id="glass.soda_lime",
        family="glass",
        phys=PhysProps(density_kg_m3=2500.0, E_GPa=70.0, bend_MPa=35.0, comp_MPa=1000.0, shear_MPa=30.0),
        render_default=RenderProfile(
            base_color_hex="#DFF4FF",
            roughness=0.02,
            metallic=0.0,
            palette=("#D8F0FF", "#DFF4FF", "#E6F7FF"),
            jitters={"roughness": 0.01, "value": 0.02},
        ),
    ),
    "metal.wrought_iron": MaterialBase(
        id="metal.wrought_iron",
        family="metal",
        phys=PhysProps(density_kg_m3=7800.0, E_GPa=200.0, bend_MPa=250.0, comp_MPa=250.0, shear_MPa=150.0),
        render_default=RenderProfile(
            base_color_hex="#3A3A3A",
            roughness=0.45,
            metallic=1.0,
            palette=("#2F2F2F", "#3A3A3A", "#4A4A4A"),
            jitters={"roughness": 0.05, "value": 0.05},
        ),
    ),
}

VARIANTS: dict[str, MaterialVariant] = {
    # --- TIMBER SPECIES ---
    "timber.oak": MaterialVariant(
        id="timber.oak",
        base_id="timber.hardwood",
        phys_override=PhysProps(density_kg_m3=720.0, E_GPa=12.5, bend_MPa=95.0, comp_MPa=50.0, shear_MPa=11.0),
        render=RenderProfile(
            base_color_hex="#7A5A3E",
            roughness=0.62,
            palette=("#6B4D35", "#7A5A3E", "#8A6A4C", "#5C422E"),
            jitters={"roughness": 0.06, "value": 0.08},
        ),
    ),
    "timber.beech": MaterialVariant(
        id="timber.beech",
        base_id="timber.hardwood",
        phys_override=PhysProps(density_kg_m3=710.0, E_GPa=13.0, bend_MPa=100.0, comp_MPa=55.0, shear_MPa=11.0),
        render=RenderProfile(
            base_color_hex="#B18B6A",
            roughness=0.60,
            palette=("#A27D5F", "#B18B6A", "#C09A78", "#8E6A4F"),
            jitters={"roughness": 0.06, "value": 0.08},
        ),
    ),
    "timber.spruce": MaterialVariant(
        id="timber.spruce",
        base_id="timber.softwood",
        phys_override=PhysProps(density_kg_m3=430.0, E_GPa=10.0, bend_MPa=70.0, comp_MPa=33.0, shear_MPa=7.0),
        render=RenderProfile(
            base_color_hex="#C9A67E",
            roughness=0.72,
            palette=("#BC9A74", "#C9A67E", "#D6B590", "#A78661"),
            jitters={"roughness": 0.07, "value": 0.10},
        ),
    ),
    "timber.pine": MaterialVariant(
        id="timber.pine",
        base_id="timber.softwood",
        phys_override=PhysProps(density_kg_m3=500.0, E_GPa=9.0, bend_MPa=65.0, comp_MPa=32.0, shear_MPa=7.0),
        render=RenderProfile(
            base_color_hex="#B98C5E",
            roughness=0.70,
            palette=("#A97E55", "#B98C5E", "#C79B6A", "#946A42"),
            jitters={"roughness": 0.07, "value": 0.10},
        ),
    ),
    # --- BRICK QUALITY ---
    "brick.historic_low": MaterialVariant(
        id="brick.historic_low",
        base_id="brick.generic",
        phys_override=PhysProps(density_kg_m3=1750.0, E_GPa=8.0, bend_MPa=6.0, comp_MPa=12.0, shear_MPa=2.5),
        render=RenderProfile(
            base_color_hex="#7C3E33",
            roughness=0.88,
            palette=("#6F372D", "#7C3E33", "#8A4A3C", "#5E2E26"),
            jitters={"roughness": 0.04, "value": 0.12},
        ),
    ),
    "brick.historic_mid": MaterialVariant(
        id="brick.historic_mid",
        base_id="brick.generic",
        phys_override=PhysProps(density_kg_m3=1800.0, E_GPa=10.0, bend_MPa=8.0, comp_MPa=20.0, shear_MPa=3.0),
        render=None,  # use base render_default
    ),
    "brick.historic_high": MaterialVariant(
        id="brick.historic_high",
        base_id="brick.generic",
        phys_override=PhysProps(density_kg_m3=1850.0, E_GPa=12.0, bend_MPa=10.0, comp_MPa=35.0, shear_MPa=3.5),
        render=RenderProfile(
            base_color_hex="#9A5544",
            roughness=0.84,
            palette=("#8C4C3E", "#9A5544", "#A96450", "#764033"),
            jitters={"roughness": 0.04, "value": 0.10},
        ),
    ),
    # --- STONE STRENGTH SPLIT ---
    "stone.sandstone_weak": MaterialVariant(
        id="stone.sandstone_weak",
        base_id="stone.sandstone",
        phys_override=PhysProps(density_kg_m3=2150.0, E_GPa=18.0, bend_MPa=10.0, comp_MPa=40.0, shear_MPa=6.0),
        render=RenderProfile(
            base_color_hex="#D0C29B",
            roughness=0.92,
            palette=("#C7B78F", "#D0C29B", "#DACDA8", "#B6A77F"),
            jitters={"roughness": 0.03, "value": 0.07},
        ),
    ),
    "stone.sandstone_strong": MaterialVariant(
        id="stone.sandstone_strong",
        base_id="stone.sandstone",
        phys_override=PhysProps(density_kg_m3=2250.0, E_GPa=28.0, bend_MPa=13.0, comp_MPa=80.0, shear_MPa=9.0),
        render=None,  # base render_default
    ),
    "stone.granite": MaterialVariant(
        id="stone.granite",
        base_id="stone.granite",
        phys_override=None,
        render=None,
    ),
    # --- MORTAR VARIANTS ---
    "mortar.lime_weak": MaterialVariant(
        id="mortar.lime_weak",
        base_id="mortar.lime",
        phys_override=PhysProps(density_kg_m3=1550.0, E_GPa=2.0, bend_MPa=1.2, comp_MPa=2.5, shear_MPa=0.9),
        render=None,
    ),
    "mortar.hydraulic_mid": MaterialVariant(
        id="mortar.hydraulic_mid",
        base_id="mortar.hydraulic",
        phys_override=PhysProps(density_kg_m3=1700.0, E_GPa=5.0, bend_MPa=2.5, comp_MPa=10.0, shear_MPa=2.0),
        render=None,
    ),
}

FAMILY_DEFAULT_VARIANT: dict[MaterialFamily, str] = {
    "timber": "timber.oak",
    "brick": "brick.historic_mid",
    "stone": "stone.sandstone_strong",
    "mortar": "mortar.lime_weak",
    "concrete": "concrete.generic",
    "glass": "glass.soda_lime",
    "metal": "metal.wrought_iron",
}


# -----------------------------------------------------------------------------
# INTERNAL HELPERS
# -----------------------------------------------------------------------------

def _clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


def _is_hex_color(s: str) -> bool:
    if not isinstance(s, str):
        return False
    if len(s) != 7 or not s.startswith("#"):
        return False
    try:
        int(s[1:], 16)
        return True
    except ValueError:
        return False


def stable_u64(seed: int, salt: str) -> int:
    """
    Stable 64-bit hash for deterministic sampling.
    - independent of Python's randomized hash()
    - stable across runs/platforms
    """
    h = hashlib.blake2b(digest_size=8)
    h.update(str(int(seed)).encode("utf-8"))
    h.update(b"|")
    h.update(str(salt).encode("utf-8"))
    return int.from_bytes(h.digest(), "big", signed=False)


def rand01(seed: int, salt: str) -> float:
    """Deterministic uniform [0,1)."""
    x = stable_u64(seed, salt)
    # 53-bit mantissa mapping
    return ((x >> 11) & ((1 << 53) - 1)) / float(1 << 53)


def _pick_palette_color(profile: RenderProfile, seed: int, salt: str) -> str:
    pal = profile.palette or ()
    if pal:
        idx = int(stable_u64(seed, salt + "|pal") % len(pal))
        c = pal[idx]
        return c if _is_hex_color(c) else profile.base_color_hex
    return profile.base_color_hex


def _apply_value_jitter_hex(hex_color: str, jitter: float, u: float) -> str:
    """
    Simple value jitter in sRGB space:
    - jitter is amplitude in [0..1] (typical 0.02..0.12)
    - u is uniform [0..1)
    """
    if not _is_hex_color(hex_color) or jitter <= 0.0:
        return hex_color

    r = int(hex_color[1:3], 16) / 255.0
    g = int(hex_color[3:5], 16) / 255.0
    b = int(hex_color[5:7], 16) / 255.0

    mul = 1.0 + (u * 2.0 - 1.0) * jitter
    r = _clamp(r * mul, 0.0, 1.0)
    g = _clamp(g * mul, 0.0, 1.0)
    b = _clamp(b * mul, 0.0, 1.0)

    return "#{:02X}{:02X}{:02X}".format(int(r * 255.0), int(g * 255.0), int(b * 255.0))


def _merge_phys(base: PhysProps, override: Optional[PhysProps]) -> PhysProps:
    return override if override is not None else base


def _merge_render(base_render: RenderProfile, override: Optional[RenderProfile]) -> RenderProfile:
    if override is None:
        return base_render
    pal = override.palette if override.palette else base_render.palette
    jit = dict(base_render.jitters)
    jit.update(dict(override.jitters or {}))
    base_hex = override.base_color_hex if override.base_color_hex else base_render.base_color_hex
    return RenderProfile(
        base_color_hex=base_hex,
        roughness=override.roughness,
        metallic=override.metallic,
        palette=pal,
        jitters=jit,
    )


def _get_attr_or_key(obj: Any, name: str) -> Any:
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def _member_uid(member: Any) -> str:
    """
    Deterministic per-member salt:
    prefer stable IDs if present, else derive from common fields.
    """
    for k in ("id", "uid", "name", "member_id", "key"):
        v = _get_attr_or_key(member, k)
        if v:
            return str(v)
    role = _get_attr_or_key(member, "role") or _get_attr_or_key(member, "kind") or "member"
    wall = _get_attr_or_key(member, "wall") or ""
    idx = _get_attr_or_key(member, "index") or _get_attr_or_key(member, "i") or ""
    return f"{role}:{wall}:{idx}"


# -----------------------------------------------------------------------------
# REGISTRY
# -----------------------------------------------------------------------------

class MaterialRegistry:
    """
    Single source of truth: physics + render defaults.

    Condition/Finish are applied *after* resolution (render sampling).
    """

    def __init__(
        self,
        bases: Mapping[str, MaterialBase],
        variants: Mapping[str, MaterialVariant],
        family_default_variant: Mapping[MaterialFamily, str],
    ) -> None:
        self._bases = dict(bases)
        self._variants = dict(variants)
        self._family_default_variant = dict(family_default_variant)

    def has(self, material_id: str) -> bool:
        return material_id in self._variants or material_id in self._bases

    def get_base(self, base_id: str) -> MaterialBase:
        b = self._bases.get(base_id)
        if b is None:
            raise KeyError(f"Unknown MaterialBase id='{base_id}'")
        return b

    def get_variant(self, variant_id: str) -> MaterialVariant:
        v = self._variants.get(variant_id)
        if v is None:
            raise KeyError(f"Unknown MaterialVariant id='{variant_id}'")
        return v

    def get(self, material_id: str) -> MaterialResolved:
        """
        Accepts either:
          - Variant id (preferred): e.g. "timber.oak"
          - Base id: e.g. "timber.hardwood"
        """
        if material_id in self._variants:
            v = self._variants[material_id]
            base = self.get_base(v.base_id)
            phys = _merge_phys(base.phys, v.phys_override)
            render = _merge_render(base.render_default, v.render)
            return MaterialResolved(id=v.id, base=base, phys=phys, render=render)

        if material_id in self._bases:
            base = self._bases[material_id]
            return MaterialResolved(id=base.id, base=base, phys=base.phys, render=base.render_default)

        raise KeyError(f"Unknown material_id='{material_id}'")

    def family_default(self, family: MaterialFamily) -> str:
        mid = self._family_default_variant.get(family)
        if not mid:
            raise KeyError(f"No family default for '{family}'")
        return mid


# -----------------------------------------------------------------------------
# RESOLUTION (member -> material)
# -----------------------------------------------------------------------------

def resolve_material_id(member: Any, ctx: Any, registry: MaterialRegistry, default: str) -> str:
    """
    Deterministic resolution order:
    1) member.material_id
    2) member.material_family -> registry.family_default(family)
    3) ctx.material_id_default_by_role.get(role)   (if present)
    4) default
    """
    mid = _get_attr_or_key(member, "material_id")
    if mid:
        return str(mid)

    fam = _get_attr_or_key(member, "material_family")
    if fam:
        try:
            return registry.family_default(str(fam))  # type: ignore[arg-type]
        except Exception:
            pass

    role = _get_attr_or_key(member, "role") or _get_attr_or_key(member, "kind")
    by_role = _get_attr_or_key(ctx, "material_id_default_by_role")
    if isinstance(by_role, dict) and role in by_role:
        return str(by_role[role])

    return str(default)


def resolve_surface(member: Any, ctx: Any) -> SurfaceSpec:
    """
    Deterministic resolution order:
    1) member.surface (as SurfaceSpec or dict)
    2) ctx.surface_default_by_role.get(role) (if present)
    3) fallback: fresh/planed
    """
    s = _get_attr_or_key(member, "surface")
    if isinstance(s, SurfaceSpec):
        return s
    if isinstance(s, dict):
        cond = s.get("condition", "fresh")
        fin = s.get("finish", "planed")
        return SurfaceSpec(condition=cond, finish=fin)  # type: ignore[arg-type]

    role = _get_attr_or_key(member, "role") or _get_attr_or_key(member, "kind")
    by_role = _get_attr_or_key(ctx, "surface_default_by_role")
    if isinstance(by_role, dict) and role in by_role:
        v = by_role[role]
        if isinstance(v, SurfaceSpec):
            return v
        if isinstance(v, dict):
            return SurfaceSpec(
                condition=v.get("condition", "fresh"),
                finish=v.get("finish", "planed"),
            )

    return SurfaceSpec()


def resolve_material(member: Any, ctx: Any, registry: MaterialRegistry, default: str) -> MaterialResolved:
    mid = resolve_material_id(member, ctx, registry, default=default)
    return registry.get(mid)


# -----------------------------------------------------------------------------
# RENDER SAMPLING (deterministic)
# -----------------------------------------------------------------------------

_FINISH_ROUGHNESS_DELTA: dict[Finish, float] = {
    "sawn": +0.10,
    "planed": -0.05,
    "oiled": -0.15,
    "painted": -0.10,
    "whitewashed": -0.05,
    "tarred": -0.10,
}

_CONDITION_VALUE_JITTER_BONUS: dict[Condition, float] = {
    "fresh": 0.00,
    "weathered": 0.05,
    "aged": 0.08,
}


def sample_render(
    resolved: MaterialResolved,
    surface: SurfaceSpec,
    *,
    seed: int,
    salt: str,
) -> RenderSample:
    """
    Produces a final render sample (color/roughness/metallic) from:
      - resolved.render (base/variant)
      - surface condition/finish
      - deterministic palette pick + jitters
    """
    rp = resolved.render

    # base color pick (palette)
    base_hex = _pick_palette_color(rp, seed, salt)

    # value jitter (brightness)
    base_value_j = float(rp.jitters.get("value", 0.0)) + _CONDITION_VALUE_JITTER_BONUS.get(surface.condition, 0.0)
    u_val = rand01(seed, salt + "|val")
    final_hex = _apply_value_jitter_hex(base_hex, base_value_j, u_val)

    # roughness jitter
    r_j = float(rp.jitters.get("roughness", 0.0))
    u_r = rand01(seed, salt + "|rough")
    rough = rp.roughness + (u_r * 2.0 - 1.0) * r_j

    # finish delta
    rough += _FINISH_ROUGHNESS_DELTA.get(surface.finish, 0.0)

    rough = _clamp(rough, 0.02, 0.98)

    return RenderSample(
        base_color_hex=final_hex,
        roughness=rough,
        metallic=_clamp(float(rp.metallic), 0.0, 1.0),
    )


# -----------------------------------------------------------------------------
# DEFAULT SINGLETON + BUILDER CONVENIENCE
# -----------------------------------------------------------------------------

DEFAULT_REGISTRY = MaterialRegistry(BASES, VARIANTS, FAMILY_DEFAULT_VARIANT)


def resolve_for_builder(
    member: Any,
    ctx: Any,
    *,
    default_material_id: str,
) -> tuple[MaterialResolved, SurfaceSpec, RenderSample]:
    """
    One-stop helper for Blender builder:
      - resolve material (physics+render)
      - resolve surface
      - sample deterministic render

    Requirements:
      - ctx.seed (int) for determinism (fallbacks to 0 if absent)
      - member stable identifier for salt (member.id/uid/name/member_id/key)
    """
    seed = int(_get_attr_or_key(ctx, "seed") or 0)
    resolved = resolve_material(member, ctx, DEFAULT_REGISTRY, default=default_material_id)
    surface = resolve_surface(member, ctx)
    salt = _member_uid(member)
    sample = sample_render(resolved, surface, seed=seed, salt=salt)
    return resolved, surface, sample
