# BVILLAGE Material Cascade

*(Material Ontology, Resolution and Rendering Pipeline)*

This document describes the **material cascade** used in BVILLAGE.

The cascade defines:

1.  Where materials originate
2.  How a member receives a material
3.  How rendering properties are derived
4.  Which elements are authoritative

The cascade ensures that:

-   materials are defined once
-   material usage is deterministic
-   rendering variation is stable and reproducible

------------------------------------------------------------------------

# 1. Material Ontology (Foundation Layer)

The **MaterialRegistry** is the single source of truth for all
materials.

If a material is not defined in the registry, it does not exist in
BVILLAGE.

All components must reference materials through a `material_id`.

The registry defines two categories:

MaterialBase\
MaterialVariant

Source: bvillage/core/materials/material_registry.py

------------------------------------------------------------------------

## 1.1 MaterialBase

A **MaterialBase** represents a fundamental material category.

Examples:

-   timber.hardwood
-   brick.generic
-   stone.sandstone
-   mortar.lime
-   metal.wrought_iron

Each base defines:

### Physical properties

-   density
-   elastic modulus
-   bending strength
-   compressive strength
-   shear strength

These properties are used by:

-   structural logic
-   plausibility checks
-   simulation systems

### Render defaults

Render parameters define the visual appearance.

-   base_color
-   roughness
-   metallic
-   palette
-   jitters

These values provide default rendering characteristics for a material.

------------------------------------------------------------------------

## 1.2 MaterialVariant

Variants specialize a base material.

Examples:

-   timber.oak
-   timber.beech
-   brick.historic_low
-   stone.sandstone_strong

Variants may override:

-   physical properties
-   render parameters

Resolution merges base and variant.

------------------------------------------------------------------------

# 2. Material Resolution

When a material is requested, the registry returns a
**MaterialResolved** object.

MaterialResolved: - base - phys - render

Resolution rules:

-   if material_id is a variant → merge base + overrides
-   if material_id is a base → use base directly

------------------------------------------------------------------------

# 3. Member Material Assignment

Members may define a material explicitly:

member.material_id = "timber.oak"

If no material is specified, the system resolves one deterministically.

Resolution order:

1.  member.material_id
2.  member.material_family
3.  role-based policy default
4.  fallback default

------------------------------------------------------------------------

## 3.1 Policy Defaults

Domains may define role-based material defaults.

Example (Fachwerk domain):

-   PRIMARY_POST → timber.oak
-   BRACE → timber.oak
-   INFILL → brick.historic_low

These defaults must reference valid registry materials.

Policies cannot introduce new materials.

------------------------------------------------------------------------

# 4. Surface Specification

Surface characteristics are **not part of the material definition**.

They are separate modifiers.

Surface parameters:

-   condition
-   finish

Examples:

-   condition = fresh \| weathered \| aged
-   finish = sawn \| planed \| oiled \| painted \| whitewashed

Surface properties affect **rendering only**.

They do not modify the physical material.

------------------------------------------------------------------------

# 5. Render Sampling

Rendering values are derived from three inputs:

-   MaterialResolved.render
-   SurfaceSpec
-   Seed + member identifier

This produces a deterministic:

RenderSample: - base_color - roughness - metallic

------------------------------------------------------------------------

## 5.1 Deterministic Variation

Variation uses deterministic hashing.

seed + member_uid → stable hash

This ensures:

same seed → identical appearance

The renderer never uses non-deterministic randomness.

------------------------------------------------------------------------

# 6. Final Material Cascade

MaterialRegistry → MaterialBase / MaterialVariant → MaterialResolved →
Member Material Resolution → SurfaceSpec → Deterministic Render Sampling
→ RenderSample

------------------------------------------------------------------------

# 7. Architectural Principles

Single source of truth\
All materials originate from the registry.

Deterministic resolution\
Material assignment is reproducible.

Clear separation of concerns

Material → physics\
Surface → aging/finish\
Render sampling → visual variation

No implicit materials\
If a material_id is unknown, resolution fails.

------------------------------------------------------------------------

# 8. Developer Rules

When implementing new systems:

-   Always reference registry materials
-   Never invent new material_id values
-   Do not encode rendering logic in builders
-   Policies may choose materials but cannot define new ones
-   Surface is not material

------------------------------------------------------------------------

# 9. Summary

The BVILLAGE material cascade ensures that:

-   material definitions are centralized
-   material assignment is deterministic
-   rendering variation is controlled
-   domains cannot diverge from the global ontology

This guarantees consistency across the entire simulation pipeline.
