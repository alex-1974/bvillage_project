# BVILLAGE Generation Model
Version: 0.2
Status: Foundational Architecture Specification

---

# 1. Core Philosophy

BVILLAGE separates architectural generation into independent,
composable layers.

Physics is timeless.
Construction culture is historical.
Topology is typological.
Style is contextual.

These must never be merged into one layer.

---

# 2. Architectural Axes

Every building is defined along three primary axes:

1. Construction Domain (Bauweise)
2. Topological Archetype (Plan Type)
3. Style / Context Policy

---

## 2.1 Construction Domain

Examples:
- fachwerk
- mauerwerk
- blockbau
- hybrid

Responsibilities:
- Structural logic
- Load paths
- FramePlan generation
- WallPlan generation
- Structural artifacts stored in notes

The Domain defines *how* a building stands.

---

## 2.2 Topological Archetype

Examples:
- Hallenhaus
- Ernhaus
- Stadthaus
- Hofanlage
- Speicher
- Ackerbürgerhaus

Responsibilities:
- Volume logic
- Space program
- Circulation
- Opening demands
- Geometric intent (span ranges, not fixed sections)

Archetypes define spatial topology, not structural sizing.

---

## 2.3 Style / Context Policy

Parameters:
- Region
- Epoch
- Wealth
- Urban / Rural
- Climate

Influences:
- Parameter ranges
- Material selection
- Ornament density
- Roof pitch tendencies
- Window proportions

StylePolicy modulates — it does not redefine topology.

---

# 3. Structural Realism Model

## 3.1 PhysicalPlausibilityValidator (Timeless Physics Layer)

Represents universal mechanics.

Responsibilities:
- Beam bending checks
- Deflection limits
- Shear checks
- Buckling checks
- Bearing checks
- Basic load assumptions

Output:
- PASS
- WARNING
- FAIL

Answers:
"Would this structure hold in reality?"

This layer is independent of epoch or region.

---

## 3.2 ConstructionCulturePolicy (Historical Layer)

Models how builders historically handled risk.

Does NOT change physics.
Modulates dimensioning behavior.

Parameters may include:
- max_utilization_ratio
- overdimension_factor
- redundancy_preference
- preferred_span_limits
- support_density_preference

Answers:
"Would builders of this period build it that way?"

This creates epoch-specific structural character.

---

# 4. Structural Dimension Resolution Pipeline

Final structural dimensions are determined in this order:

1. Archetype defines geometric intent (span ranges).
2. Domain defines structural system.
3. Physics computes minimal required section.
4. ConstructionCulturePolicy scales dimension.
5. PhysicalPlausibilityValidator verifies final result.
6. Evaluator scores plausibility and cost.

This prevents:
- Anachronistic optimization
- Unrealistic slenderness
- Typological duplication across epochs

---

# 5. Unified Material System

Materials are defined in a global MaterialRegistry.

Each MaterialClass provides:

A) Physics parameters:
- E-modulus
- density
- allowable stresses

B) RenderProfile:
- base_color_hex
- roughness
- metallic
- deterministic variation palette
- roughness/value jitter

Important:
Physics values must never be altered for visual reasons.

Rendering must use the same material_id to ensure consistency.

This allows:
- Physics validation
- Domain sizing
- Blender shading
- Deterministic diversity

---

# 6. Variation System

Variation is controlled through:

- Soft ranges (low cost deviation)
- Hard ranges (expensive deviation)
- Absolute limits (forbidden)

Sampling must:
- Be seed-based
- Use distributions (not uniform randomness)
- Avoid identical repetition

Determinism:
world_seed + settlement_seed + house_salt

---

# 7. Role Model

## Order Provider
Defines requested parameters or defaults.

## Archetype Architect
Creates geometric and programmatic structure.

## Interior Planner
Resolves room layout.
May generate multiple candidates.

## Domain Engine
Generates structural artifacts.

## PhysicalPlausibilityValidator
Checks universal physics.

## ConstructionCultureValidator
Checks historical plausibility.

## Evaluator / Orchestrator
Scores candidates and selects final variant.

---

# 8. Scalability

The system supports:
- 50+ archetypes
- Multiple domains
- Multiple epochs
- Settlement-scale diversity

Core engine remains stable.
Knowledge expands via:
- Taxonomy
- Style policies
- Material registry
- Culture policies

---

# 9. Determinism Principle

All stochastic variation must be deterministic.

No hidden randomness.

This ensures:
- Reproducibility
- Debuggability
- Stable world generation

# 10. Canonical Role Model (Decision Boundaries)

This section defines strict responsibility separation.

No role may cross its boundary.

---

## 10.1 SettlementBuilder (Town / City Layer)

Responsibility:
- Decide which house type is built where.
- Select archetype or allow weighted selection.
- Provide HouseRequest.

Input:
- Plot geometry
- Budget / Wealth
- Region
- Epoch
- Climate
- Seed

Output:
HouseRequest {
  archetype_id,
  constraints,
  seed,
  context
}

May NOT:
- Define construction details (no bracing, no timber sizes)
- Define openings manually
- Override Domain logic

---

## 10.2 TypePlanner (Archetype Planner)

Example:
types/fachwerkhaus/hallenhaus/planner.py

Responsibility:
- Define spatial and semantic structure.

Plans:
- axis_x / axis_y grid
- axes_z (storey heights)
- walls (N/S/E/W)
- rooms / zones
- semantic tags (front, service, hearth zone)
- opening demands (type, wall, u-range, z-range)

Output:
Structure (semantic plan only)

May NOT:
- Define timber sections
- Define braces
- Define structural members
- Build Blender meshes

---

## 10.3 DomainConstructor (Construction Engine)

Example:
domains/fachwerk/core/frameplan.py

Responsibility:
- Translate Structure into structural truth.

Produces:
FramePlan {
  axes_u
  axes_z
  openings
  members {
    posts[]
    rails[]
    braces[]
    optional infill_cells[]
  }
}

Members are explicit structural elements.
Blender must build from members — not derive from axes.

May NOT:
- Generate Blender objects
- Modify semantic Structure

---

## 10.4 BlenderBuilder (Emitter Only)

Responsibility:
- Build exact geometry from FramePlan + Structure.

May NOT:
- Infer missing structural elements
- Modify FramePlan
- Invent bracing or posts
- Derive structure from grid

Builder is deterministic emitter only.

---

## 10.5 InteriorPlanner

Example:
types/fachwerkhaus/hallenhaus/interior.py

Responsibility:
- Plan interior objects.
- Place hearth, partitions, furniture.
- Request additional openings via Planner.

May NOT:
- Modify exterior structure
- Modify FramePlan
- Directly create exterior wall openings

---

## 10.6 Evaluator / Orchestrator

Responsibility:
- Score candidate variants.
- Enforce diversity.
- Balance cost vs plausibility.
- Decide acceptance or rejection.

May NOT:
- Change geometry.
- Repair structure.

