# BVILLAGE TODO Single Queue
Version: 0.3.0 (Draft)
Purpose: Single strategic and operational task list for architectural evolution.

---

# CORE ARCHITECTURE

## ARC-001  Three-Axis Architectural System
Status: active
Priority: high

Goal:
Stabilize Domain / Archetype / StylePolicy separation.

Tasks:
- [ ] Ensure Archetype defines topology only
- [ ] Ensure Domain defines structural logic only
- [ ] Ensure StylePolicy modulates parameters only
- [ ] Prevent cross-layer leakage

Rationale:
Scalable to 50+ archetypes without duplication.

---

## ARC-003  Plot & Envelope Foundation

Status: planned  
Priority: high  
Target: pre v0.2.0 groundwork  

Goal:

Introduce polygon-based Plot and minimal 3D envelope model
without breaking current Langhaus stability.

Tasks:

- [ ] Add Plot dataclass (polygon boundary + terrain plane MVP)
- [ ] Add Footprint.polygon_local (retain rect helper for compatibility)
- [ ] Add Placement abstraction (world transform)
- [ ] Implement deterministic polygon containment validator
- [ ] Implement buildable polygon inset (simple miter/bevel policy)
- [ ] Implement terrain_z() for plane model
- [ ] Implement Δz slope analysis utility
- [ ] Keep Grid rectangular internally (masked by footprint)

Rationale:

Prepares support for:

- hanglage
- basements
- corner logic
- future bridge/tower expansion

without touching Domain or Builder contracts.

---

## ARC-004  3D Envelope MVP

Status: planned  
Priority: medium  

Goal:

Allow multi-level and below-ground modeling using constraint logic,
not procedural special cases.

Tasks:

- [ ] Add levels abstraction (positive + negative)
- [ ] Add vertical_rules (max_height, max_depth)
- [ ] Implement 3D fit validator (horizontal + vertical checks)
- [ ] Define FFL heuristic (street-aligned)
- [ ] Log envelope violations as Issue objects
- [ ] Add simple support_zones + clearance_zones schema

Rationale:

Basements, partial underground, bridges, and height limits
become constraint-based instead of special-case logic.

## ARC-002  Role-Based Generation Pipeline
Status: active
Priority: high

Goal:
Formalize role separation.

Pipeline:
1. OrderProvider
2. ArchetypeArchitect
3. InteriorPlanner
4. DomainEngine
5. PhysicalPlausibilityValidator
6. ConstructionCultureValidator
7. Evaluator

Tasks:
- [ ] Define clear API contracts between stages
- [ ] Ensure stages do not mutate previous logic silently
- [ ] Allow multi-candidate interior proposals

Rationale:
Prevent monolithic generation logic.

---

# STRUCTURAL SYSTEM

## STR-001  Structural Dimension Resolution Pipeline
Status: planned
Priority: high
Target: v0.3+

Goal:
Replace fixed beam dimensions with dynamic resolution.

Pipeline:
1. Archetype defines span range
2. Domain defines structural scheme
3. Physics computes minimal section
4. ConstructionCulturePolicy scales section
5. Validator verifies

Tasks:
- [ ] Move fixed beam sizes out of HouseTypes
- [ ] Introduce span ranges instead of constants
- [ ] Implement dimension resolution step
- [ ] Log structural utilization

---

## STR-002  Physics & Construction Culture Separation
Status: planned
Priority: high
Target: v0.3+

Goal:
Separate universal physics from historical building behavior.

Tasks:
- [ ] Implement PhysicalPlausibilityValidator
- [ ] Define ConstructionCulturePolicy schema
- [ ] Introduce utilization thresholds
- [ ] Add redundancy preference
- [ ] Prevent anachronistic optimization

Rationale:
Ensure historical realism and physical plausibility.

---

# PHYSICAL VALIDATION

## PHY-001  PhysicalPlausibilityValidator (MVP)
Status: planned
Priority: high

Checks:
- [ ] Beam bending
- [ ] Deflection limits
- [ ] Shear plausibility
- [ ] Post slenderness heuristic
- [ ] Bearing length minimum
- [ ] Geometry sanity checks

Output:
- PASS
- WARNING
- FAIL
- Suggestion issues

Notes:
Validator does NOT repair geometry.

---

# MATERIAL SYSTEM

## MAT-001  Unified MaterialRegistry (Physics + Rendering)
Status: planned
Priority: high
Target: v0.3+

Goal:
Create unified material classes used by both:
- Physical validation
- Blender rendering

Tasks:
- [ ] Implement MaterialClass
- [ ] Implement RenderProfile
- [ ] Add timber materials:
      oak, beech, pine, spruce
- [ ] Add brick materials:
      historic low/mid/high
- [ ] Add stone materials:
      sandstone weak/strong, granite
- [ ] Add mortar materials:
      lime weak, hydraulic mid
- [ ] Add resolve_material(member, ctx)
- [ ] Domain default material policies

Rationale:
Keep physics and visuals coherent.
Prevent material duplication logic.

---

## MAT-002  Deterministic Visual Variation
Status: planned
Priority: medium

Goal:
Avoid identical houses while preserving identity.

Tasks:
- [ ] Implement palette-based color variation
- [ ] Roughness jitter
- [ ] Brightness/value jitter
- [ ] Seed-based sampling
- [ ] Ensure reproducibility

Rationale:
Controlled diversity without texture dependency.

---

# VARIATION & DIVERSITY

## VAR-001  Soft / Hard Parameter Ranges
Status: planned
Priority: high

Goal:
Introduce cost-weighted parameter ranges.

Types:
- Soft range (low cost)
- Hard range (high cost)
- Absolute bounds (forbidden)

Tasks:
- [ ] Replace fixed constants with parameter ranges
- [ ] Implement deviation cost scoring
- [ ] Integrate into Evaluator

---

## VAR-002  Settlement-Level Diversity Control
Status: planned
Priority: medium

Goal:
Prevent visual cloning across multiple houses.

Tasks:
- [ ] Settlement seed system
- [ ] Diversity scoring
- [ ] Avoid identical span/material combos
- [ ] Penalize repetition

---

# TAXONOMY

## TAX-001  Architectural Taxonomy Integration
Status: planned
Priority: high
Target: v0.4+

Goal:
Integrate historically grounded taxonomy system.

Tasks:
- [ ] Implement Topology Signature schema
- [ ] Map Fachwerk topologies to providers
- [ ] Maintain ID format (e.g. FW-LH-ND-16-M)
- [ ] Allow taxonomy expansion without engine change

---

# INTERIOR SYSTEM

## INT-001  InteriorPlanner Iteration Model
Status: planned
Priority: medium

Goal:
Allow InteriorPlanner to:
- Propose multiple layouts
- Attach cost
- Return alternatives

Tasks:
- [ ] Define room requirement schema
- [ ] Conflict detection (chimney, window-wall conflict)
- [ ] Multi-candidate return format
- [ ] Integration with Evaluator

---

# QUALITY SYSTEM

## QLT-001  Issue-Based Validation Framework
Status: active

Goal:
All validators produce Issue objects.

Tasks:
- [ ] Standardize Issue structure
- [ ] Severity levels (HARD / SOFT / SUGGEST)
- [ ] Aggregate reporting
- [ ] Domain-specific issue categories

---

# FUTURE EXTENSIONS

## FUT-001  Advanced Physics Extensions
- [ ] Climate load models (snow zones)
- [ ] Roof pitch snow reduction
- [ ] Moisture plausibility
- [ ] Fire resistance modeling

---

## FUT-002  Blender Material Adapter
- [ ] Principled BSDF mapping
- [ ] Material caching
- [ ] Node group template
- [ ] Asset-ready extension

---

# GUIDING PRINCIPLES

- Physics is universal.
- Construction culture is epoch-dependent.
- Archetypes define topology, not dimensions.
- Domains define structural logic.
- Materials unify physics and rendering.
- Variation must be deterministic.
- No anachronistic optimization.
- Scalability over duplication.

# TODO – Naming Refactor Phase
Status: PLANNED  
Priority: HIGH  
Target: Next structural stabilization window  

---

## 🎯 Goal

Align all existing files and public functions with the  
**BVILLAGE Naming Policy v0.1 (Nadine Policy)**.

Ensure consistent usage of:

- `derive_` → domain-core artifact computation  
- `build_`  → Blender emission only  
- `plan_`   → type-layer semantic planning  
- `validate_` / `audit_` → checks  
- `policy_` / `schema_` / `mesh_` where applicable  

No mixed conventions allowed in new modules.

---

## 📦 Scope

### 1️⃣ Domain-Core Renames

- `axes_u.py` → `derive_axes_u.py`
- `axes_z.py` → `derive_axes_z.py`
- `frameplan.py` → `derive_frameplan.py`
- `openings_norm.py` → `normalize_openings.py`
- `wall_tags.py` → `derive_wall_tags.py`
- `frameplan_contract.py` → `audit_frameplan_contract.py`

---

### 2️⃣ Domain-Blender Renames

- `braces.py` → `build_braces.py`
- `infills.py` → `build_infills.py`
- `roof.py` → `build_roof.py`
- `opening_frames.py` → `build_opening_frames.py`
- `integrity.py` → `audit_integrity.py`
- `timber.py` → `mesh_timber.py`

---

### 3️⃣ Optional Type-Layer Renames (Consistency Upgrade)

- `planner.py` → `plan_structure.py`
- `interior.py` → `plan_interior.py`
- `openings.py` → `plan_openings.py`

---

## 🔁 Migration Steps

1. Create dedicated branch: `refactor/naming-policy-v0.1`
2. Rename files
3. Update all imports
4. Update test imports
5. Run full test suite
6. Confirm deterministic outputs unchanged
7. Merge in one controlled commit

---

## ⚠️ Constraints

- ❌ No functional changes during rename
- ❌ No silent structural changes
- ✅ Determinism must remain intact
- ✅ All tests must pass
- ✅ No leftover legacy names in new modules

---

## 📌 Definition of Done

- No file violating `<role>_<aspect>.py` pattern
- No ambiguous role names across layers
- No generic file names (`utils.py`, `helpers.py`, `common.py`)
- All public functions follow role verb convention
- Repository grep for old names returns zero results

---

Naming clarity is part of architectural stability.
