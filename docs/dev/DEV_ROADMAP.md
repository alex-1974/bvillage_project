# BVILLAGE TODO – Single Strategic Queue

Version: 0.3.0 (Active)
Purpose: Architectural evolution roadmap.

---

# 0. STABILIZATION LAYER (Completed)

## ARC-000 Members-Only Architecture (Schema v3)

Status: DONE
Version: v0.3.0

**Delivered:**

* Builder fully members-driven
* No axis-derived geometry
* No structural fallbacks
* Contract hardened (members mandatory)
* FramePolicy controls structural profiles
* Determinism preserved

**Result:** Canonical structural truth established.

---

# 1. CORE ARCHITECTURE EVOLUTION

## ARC-001 Three-Axis Architectural System

Status: ACTIVE
Priority: HIGH

**Goal:**
Stabilize separation between:

* Archetype → topology only
* Domain → structural logic only
* StylePolicy → parameter modulation only

**Tasks:**

* [ ] Formalize Archetype interface
* [ ] Prevent Domain from leaking style logic
* [ ] Ensure StylePolicy contains no geometry logic
* [ ] Document allowed cross-layer data flow

---

## ARC-001A Policy Axis Foundation (Rewrite Guard)

Status: ACTIVE
Priority: CRITICAL
Target: v0.4.x (foundation only)

Goal:
Freeze the minimal structural foundation for the Policy Axis System
without implementing full historical detail yet.

This prevents later architectural rewrites.

Scope (MVP only, no deep content yet):

[ ] Introduce canonical PolicyStack structure
[ ] Implement resolve_policy_stack(ctx) (empty-slot compatible)
[ ] Define Canonical Parameter Tree (minimal skeleton only)
[ ] Enforce patch-based merge discipline
[ ] Add HARD error for unknown patch keys
[ ] Add invariant validation hook (empty allowed)
[ ] Ensure optional axes do not require changes in existing archetypes
[ ] Add resolver-level reporting (for future diagnostics)

Non-goals (for now):
- No full StylePolicy library
- No deep CulturePolicy content
- No historical exhaustiveness
- No combinatorial expansion

Deliverable:
Stable structural slots for future expansion.

Rationale:
Architectural axes must exist before large-scale variation begins.
Otherwise future subtype or domain discoveries will require rewrites.

## ARC-002 Role-Based Generation Pipeline

Status: ACTIVE
Priority: HIGH

**Pipeline:**

1. OrderProvider
2. ArchetypeArchitect
3. InteriorPlanner
4. DomainEngine
5. PhysicalPlausibilityValidator
6. ConstructionCultureValidator
7. Evaluator

**Tasks:**

* [ ] Freeze stage interfaces
* [ ] Enforce immutability between stages
* [ ] Add multi-candidate support
* [ ] Add stage-level reporting

---

# 2. STRUCTURAL INTELLIGENCE

## STR-001 Structural Dimension Resolution

Status: PLANNED
Priority: HIGH
Target: v0.4.x

**Goal:**
Replace fixed beam dimensions with resolved sections.

**Dependency:**
- Must consume inputs from ResolvedPolicy (via resolve_policy_stack(ctx)).
- No new hardcoded "magic section constants" outside policy/culture defaults.

Non-goal (until ARC-001A is stable):
- No region/epoch branching inside solver.

**Pipeline:**

Archetype span → Domain scheme → Physics minimal section
→ ConstructionCulture scaling → Validator verification

**Tasks:**

* [ ] Remove fixed section constants
* [ ] Introduce span ranges
* [ ] Implement dimension solver
* [ ] Log utilization ratios

---

## STR-002 Physics vs Construction Culture Separation

Status: PLANNED
Priority: HIGH
Target: v0.4.x

**Goal:**
Separate universal physics from historical realism.

**Tasks:**

* [ ] Implement PhysicalPlausibilityValidator
* [ ] Define ConstructionCulturePolicy
* [ ] Add redundancy preference
* [ ] Prevent anachronistic optimization

---

# 3. MATERIAL SYSTEM

## MAT-001 Unified MaterialRegistry

Status: PLANNED
Priority: HIGH
Target: v0.4.x

**Goal:**
Single material definition for:

* Physics
* Rendering

**Dependency:**
- Material selection must be driven by ResolvedPolicy + domain CulturePolicy.
- No region/epoch/wealth logic inside blender builders.

Contract:
- resolve_material(member, ctx, resolved_policy) is pure + deterministic.

**Tasks:**

* [ ] Implement MaterialClass
* [ ] Implement RenderProfile
* [ ] Add timber classes (oak, beech, pine, spruce)
* [ ] Add masonry classes (brick historic low/mid/high)
* [ ] Add stone classes (sandstone weak/strong, granite)
* [ ] Add mortar classes (lime weak, hydraulic mid)
* [ ] Implement resolve_material(member, ctx)

---

## MAT-002 Deterministic Visual Variation

Status: PLANNED
Priority: MEDIUM

**Goal:**
Controlled diversity without breaking determinism.

**Tasks:**

* [ ] Palette variation
* [ ] Roughness jitter
* [ ] Brightness jitter
* [ ] Seed-driven sampling

---

# 4. VARIATION SYSTEM

## VAR-001 Parameter Ranges (Soft / Hard)

Status: PLANNED
Priority: HIGH

**Goal:**
Introduce cost-weighted deviation ranges.

**Tasks:**

* [ ] Replace fixed constants with parameter ranges
* [ ] Implement deviation scoring
* [ ] Integrate into Evaluator

---

## VAR-002 Settlement-Level Diversity

Status: PLANNED
Priority: MEDIUM

**Goal:**
Prevent cloned houses.

**Tasks:**

* [ ] Settlement seed logic
* [ ] Diversity scoring
* [ ] Repetition penalty

---

# 5. PLOT & ENVELOPE FOUNDATION

## ARC-003 Plot & Envelope Foundation

Status: PLANNED
Priority: HIGH

**Goal:**
Introduce polygon-based plot system without breaking domain logic.

**Tasks:**

* [ ] Plot dataclass (polygon boundary + terrain plane MVP)
* [ ] Footprint.polygon_local
* [ ] Placement abstraction
* [ ] Deterministic containment validator
* [ ] Terrain plane MVP

---

## ARC-004 3D Envelope MVP

Status: PLANNED
Priority: MEDIUM

**Goal:**
Constraint-based multi-level modeling.

**Tasks:**

* [ ] Levels abstraction
* [ ] Vertical rules (max_height, max_depth)
* [ ] 3D fit validation
* [ ] Envelope issue logging

---

# 6. INTERIOR SYSTEM

## INT-001 InteriorPlanner Iteration Model

Status: PLANNED
Priority: MEDIUM

**Goal:**
Multi-proposal interior planning.

**Tasks:**

* [ ] Room requirement schema
* [ ] Conflict detection
* [ ] Alternative scoring

---

# 7. QUALITY SYSTEM

## QLT-001 Issue-Based Validation Framework

Status: ACTIVE

**Goal:**
All validators produce Issue objects.

**Tasks:**

* [ ] Standardize Issue schema
* [ ] Severity levels (HARD / SOFT / SUGGEST)
* [ ] Aggregate reporting
* [ ] Domain-specific issue categories

---

# 8. NAMING REFACTOR (Controlled Window)

Status: PLANNED
Priority: HIGH

**Activation condition:**

* No structural refactor active
* Variation layer stabilized

**Constraints:**

* ❌ No functional changes
* ❌ No silent structural modifications
* ✅ Determinism unchanged
* ✅ Single atomic rename branch

---

# 9. FUTURE EXTENSIONS (Frozen)

* Climate load models
* Roof pitch snow reduction
* Moisture plausibility
* Fire resistance modeling
* Advanced structural simulation

---

# GUIDING PRINCIPLES

* Physics is universal.
* Construction culture is epoch-dependent.
* Archetypes define topology, not dimensions.
* Domains define structural logic.
* Materials unify physics and rendering.
* Variation must be deterministic.
* No anachronistic optimization.
* Scalability over duplication.

---

## MILESTONE v0.4.0 – Structural Intelligence

Status: PLANNED
Priority: HIGH

Tasks:

### STR-001
- [ ] Implement span → section resolution
- [ ] Add minimal section solver
- [ ] Add utilization logging

### MAT-001
- [ ] Implement MaterialClass
- [ ] Implement RenderProfile
- [ ] Add resolve_material(member, ctx)

### PHY-001
- [ ] Implement PhysicalPlausibilityValidator (MVP)

### FUTURE-PROOF SKELETONS
- [ ] Add Plot dataclass (optional, unused)
- [ ] Add InteriorPlan dataclass (empty allowed)
- [ ] Standardize Issue object across validators

### NR-0.4.0 Naming Window
Activation condition:
- All above tasks stable
- Determinism confirmed
