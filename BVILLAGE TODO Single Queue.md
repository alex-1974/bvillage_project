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
