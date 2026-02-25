# bvillage/core/materials/material_registry.py

"""
BVILLAGE Material Registry
Version: 0.2
Status: Active

This module defines material classes used consistently across:

1. PhysicalPlausibilityValidator (mechanical properties)
2. Domain logic (structural reasoning)
3. Blender shading (RenderProfile)

Physics parameters are timeless.
Cultural modifiers belong to ConstructionCulturePolicy.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple


# ============================================================
# Render Profile (engine-agnostic PBR hints)
# ============================================================

@dataclass(frozen=True)
class RenderProfile:
    base_color_hex: str
    roughness: float
    metallic: float = 0.0
    normal_strength: float = 0.0
    ao_strength: float = 0.0

    # Deterministic variation (seed-based later)
    variation_palette: Tuple[str, ...] = ()
    roughness_jitter: float = 0.0
    value_jitter: float = 0.0


# ============================================================
# Material Class (Physics + Render)
# ============================================================

@dataclass(frozen=True)
class MaterialClass:
    id: str
    category: str  # timber | brick | stone | mortar

    # Elastic properties
    E_N_mm2: float
    density_kg_m3: float

    # Allowable stresses (conservative plausibility-level values)
    fb_allow_N_mm2: float
    fv_allow_N_mm2: float
    fc0_allow_N_mm2: float
    fc90_allow_N_mm2: float
    ft_allow_N_mm2: float

    render: RenderProfile


# ============================================================
# Helper Builders
# ============================================================

def _timber(
    *,
    id: str,
    E_GPa: float,
    density: float,
    fb: float,
    fv: float,
    fc0: float,
    fc90: float,
    ft: float,
    render: RenderProfile,
) -> MaterialClass:
    return MaterialClass(
        id=id,
        category="timber",
        E_N_mm2=E_GPa * 1000.0,
        density_kg_m3=density,
        fb_allow_N_mm2=fb,
        fv_allow_N_mm2=fv,
        fc0_allow_N_mm2=fc0,
        fc90_allow_N_mm2=fc90,
        ft_allow_N_mm2=ft,
        render=render,
    )


def _masonry_like(
    *,
    id: str,
    category: str,
    E_GPa: float,
    density: float,
    fc: float,
    render: RenderProfile,
    ft: float = 0.2,
    fb: float = 0.2,
    fv: float = 0.2,
) -> MaterialClass:
    return MaterialClass(
        id=id,
        category=category,
        E_N_mm2=E_GPa * 1000.0,
        density_kg_m3=density,
        fb_allow_N_mm2=fb,
        fv_allow_N_mm2=fv,
        fc0_allow_N_mm2=fc,
        fc90_allow_N_mm2=max(0.5, 0.25 * fc),
        ft_allow_N_mm2=ft,
        render=render,
    )


# ============================================================
# Render Presets
# ============================================================

RENDER = {

    # --- Timber ---

    "oak": RenderProfile(
        base_color_hex="#9A6B3F",
        roughness=0.55,
        variation_palette=("#8B5E34", "#9A6B3F", "#A87A4C", "#7C5430"),
        roughness_jitter=0.06,
        value_jitter=0.06,
    ),

    "beech": RenderProfile(
        base_color_hex="#C6A57A",
        roughness=0.52,
        variation_palette=("#B99266", "#C6A57A", "#D1B089", "#A8845B"),
        roughness_jitter=0.05,
        value_jitter=0.05,
    ),

    "pine": RenderProfile(
        base_color_hex="#C8A56A",
        roughness=0.58,
        variation_palette=("#B88F56", "#C8A56A", "#D3B47C", "#A47D49"),
        roughness_jitter=0.07,
        value_jitter=0.06,
    ),

    "spruce": RenderProfile(
        base_color_hex="#D0B27A",
        roughness=0.60,
        variation_palette=("#C0A56E", "#D0B27A", "#D8BE8A", "#AE945F"),
        roughness_jitter=0.08,
        value_jitter=0.06,
    ),

    # --- Brick ---

    "brick_low": RenderProfile(
        base_color_hex="#8E3E2F",
        roughness=0.82,
        variation_palette=("#7A3629", "#8E3E2F", "#A24733", "#6C2F24"),
        roughness_jitter=0.05,
        value_jitter=0.05,
    ),

    "brick_mid": RenderProfile(
        base_color_hex="#A54A35",
        roughness=0.78,
        variation_palette=("#8E3E2F", "#A54A35", "#B4553A", "#7E3629"),
        roughness_jitter=0.05,
        value_jitter=0.05,
    ),

    "brick_high": RenderProfile(
        base_color_hex="#B3543A",
        roughness=0.74,
        variation_palette=("#A54A35", "#B3543A", "#C06041", "#94412F"),
        roughness_jitter=0.04,
        value_jitter=0.04,
    ),

    # --- Stone ---

    "sandstone_weak": RenderProfile(
        base_color_hex="#B9A37B",
        roughness=0.85,
        variation_palette=("#A89068", "#B9A37B", "#C5B08A", "#967E59"),
        roughness_jitter=0.04,
        value_jitter=0.04,
    ),

    "sandstone_strong": RenderProfile(
        base_color_hex="#BFA77F",
        roughness=0.83,
        variation_palette=("#B0976E", "#BFA77F", "#CCB58F", "#9E845F"),
        roughness_jitter=0.04,
        value_jitter=0.04,
    ),

    "granite": RenderProfile(
        base_color_hex="#7A7C80",
        roughness=0.65,
        variation_palette=("#6B6D70", "#7A7C80", "#8A8C90", "#5F6063"),
        roughness_jitter=0.03,
        value_jitter=0.03,
    ),

    # --- Mortar ---

    "mortar_lime_weak": RenderProfile(
        base_color_hex="#D6D2C7",
        roughness=0.92,
        variation_palette=("#CFCABE", "#D6D2C7", "#DDD9CF", "#C6C1B5"),
        roughness_jitter=0.03,
        value_jitter=0.02,
    ),

    "mortar_hydraulic_mid": RenderProfile(
        base_color_hex="#CFCBC1",
        roughness=0.90,
        variation_palette=("#C6C1B7", "#CFCBC1", "#D7D3CA", "#BDB8AF"),
        roughness_jitter=0.03,
        value_jitter=0.02,
    ),
}


# ============================================================
# Registry
# ============================================================

MATERIALS: Dict[str, MaterialClass] = {

    # --- Timber ---

    "timber_oak_structural": _timber(
        id="timber_oak_structural",
        E_GPa=12.0,
        density=700.0,
        fb=14.0, fv=1.5, fc0=20.0, fc90=3.0, ft=10.0,
        render=RENDER["oak"],
    ),

    "timber_beech_structural": _timber(
        id="timber_beech_structural",
        E_GPa=13.5,
        density=720.0,
        fb=13.0, fv=1.4, fc0=22.0, fc90=3.0, ft=10.0,
        render=RENDER["beech"],
    ),

    "timber_pine_structural": _timber(
        id="timber_pine_structural",
        E_GPa=10.0,
        density=520.0,
        fb=10.0, fv=1.2, fc0=18.0, fc90=2.5, ft=8.0,
        render=RENDER["pine"],
    ),

    "timber_spruce_structural": _timber(
        id="timber_spruce_structural",
        E_GPa=10.0,
        density=470.0,
        fb=9.0, fv=1.1, fc0=17.0, fc90=2.3, ft=7.0,
        render=RENDER["spruce"],
    ),

    # --- Brick ---

    "brick_historic_low": _masonry_like(
        id="brick_historic_low",
        category="brick",
        E_GPa=4.0,
        density=1650.0,
        fc=7.0,
        render=RENDER["brick_low"],
    ),

    "brick_historic_mid": _masonry_like(
        id="brick_historic_mid",
        category="brick",
        E_GPa=6.0,
        density=1750.0,
        fc=15.0,
        render=RENDER["brick_mid"],
    ),

    "brick_historic_high": _masonry_like(
        id="brick_historic_high",
        category="brick",
        E_GPa=8.0,
        density=1850.0,
        fc=25.0,
        render=RENDER["brick_high"],
    ),

    # --- Stone ---

    "stone_sandstone_weak": _masonry_like(
        id="stone_sandstone_weak",
        category="stone",
        E_GPa=10.0,
        density=2200.0,
        fc=40.0,
        render=RENDER["sandstone_weak"],
    ),

    "stone_sandstone_strong": _masonry_like(
        id="stone_sandstone_strong",
        category="stone",
        E_GPa=25.0,
        density=2300.0,
        fc=120.0,
        render=RENDER["sandstone_strong"],
    ),

    "stone_granite_typical": _masonry_like(
        id="stone_granite_typical",
        category="stone",
        E_GPa=40.0,
        density=2650.0,
        fc=140.0,
        render=RENDER["granite"],
    ),

    # --- Mortar ---

    "mortar_lime_weak": _masonry_like(
        id="mortar_lime_weak",
        category="mortar",
        E_GPa=1.0,
        density=1700.0,
        fc=1.2,
        render=RENDER["mortar_lime_weak"],
    ),

    "mortar_hydraulic_lime_mid": _masonry_like(
        id="mortar_hydraulic_lime_mid",
        category="mortar",
        E_GPa=2.5,
        density=1800.0,
        fc=6.0,
        render=RENDER["mortar_hydraulic_mid"],
    ),
}
