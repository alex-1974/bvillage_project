# BVILLAGE PROJECT MASTER

Status: Active
Current Version: 0.3.0
Architecture Status: Members-Only (schema_version = 3)

---

# ============================================================

# 1. PROJECT IDENTITY

# ============================================================

BVILLAGE is a deterministic architectural generation system.

Core characteristics:

* Physics-aware
* Historically plausible
* Deterministic by seed
* Strictly layered
* Members-first structural truth

The system must scale from single-house generation
to settlement-level simulation without architectural rewrites.

---

# ============================================================

# 2. ARCHITECTURAL FOUNDATION (Locked in v0.3.0)

# ============================================================

## Members-Only Architecture (schema_version = 3)

Structural truth is defined exclusively by:

members = {
posts,
rails,
braces,
infills
}

Blender is a pure renderer.

No structural inference.
No axis-derived geometry.
No fallback paths.

FramePolicy drives structural parameters.
Contract enforces completeness.
Determinism is mandatory.

This boundary is frozen.

---

# ============================================================

# 3. LAYER SEPARATION (Non-Negotiable)

# ============================================================

Archetype → topology only
Domain → structural logic only
StylePolicy → parameter modulation only
Blender → rendering only

Core modules must never depend on Blender.

Blender modules must never generate structural logic.

Structural boundaries must not change in minor releases.

---

# ============================================================

# 4. CURRENT PHASE – v0.4.0 Structural Intelligence

# ============================================================

Purpose:
Introduce structural intelligence without breaking
members-first architecture.

v0.4.0 expands capability, not architecture.

---

## 4.1 Scope of v0.4.0

### A) Structural Dimension Resolution

Replace fixed beam dimensions with span-based resolution.

Pipeline:

Span → minimal required section → culture scaling → validation

Goals:

* Remove magic section constants
* Log utilization ratios
* Maintain determinism

---

### B) MaterialRegistry

Introduce unified material system:

MaterialClass:

* density
* bending strength
* modulus
* render profile reference

RenderProfile:

* base_color_hex
* roughness
* metallic
* variation palette
* deterministic jitter

Member → resolve_material(member, ctx)

Material drives both physics and rendering.

---

### C) PhysicalPlausibilityValidator (MVP)

Must detect:

* Overstressed bending members
* Slenderness extremes
* Bearing length issues

Returns Issue objects only.
No direct geometry modification.

---

### D) Future-Proof Skeleton Interfaces (No Enforcement Yet)

The following interfaces must exist in v0.4.0,
even if not fully active:

1. Plot

   * polygon boundary (2D)
   * optional terrain plane

2. InteriorPlan

   * room list
   * circulation
   * openings_int

3. Issue (standard validation object)

These interfaces must not alter domain logic yet.
They exist to prevent future architectural rewrites.

---

## 4.2 Non-Goals of v0.4.0

The following are explicitly excluded:

* Plot enforcement
* 3D envelope constraints
* City builder
* Settlement-level zoning logic
* Full interior optimization
* Naming-wide refactor (except controlled window)

---

## 4.3 Definition of Done for v0.4.0

A deterministic house must:

* Generate members-only FramePlan
* Resolve structural dimensions from span
* Assign materials via registry
* Pass contract validation
* Pass integrity validation
* Pass basic physical plausibility checks
* Render deterministically in Blender

If these conditions are met,
v0.4.0 is complete.

---

# ============================================================

# 5. NAMING STRATEGY

# ============================================================

New modules must follow naming policy immediately.

Global rename window:

NR-0.4.0 (post stabilization window)

Conditions for rename:

* All structural intelligence tasks complete
* Determinism verified
* No open structural refactors

Rename branch must:

* Contain no functional changes
* Preserve determinism
* Be atomic

---

# ============================================================

# 6. FUTURE EXPANSION (Post v0.4.x)

# ============================================================

Only after structural intelligence is stable:

* Plot enforcement
* Geo zoning
* 3D envelope logic
* Interior optimization
* Settlement diversity engine
* Climate loads
* Construction culture deep modeling

Expansion must not alter:
Members-first structural truth.

---

# ============================================================

# 7. VERSIONING RULES

# ============================================================

Minor version increment:

* Structural intelligence improvements
* Validator extensions
* Material system expansion
* Policy refinement

Major version increment:

* Schema change
* Members structure change
* Layer boundary change
* Contract semantics change

---

# ============================================================

# 8. GUIDING PRINCIPLES

# ============================================================

Physics is universal.
Construction culture is historical.
Archetypes define topology, not dimensions.
Domains define structure, not style.
Members are canonical structural truth.
Variation must be deterministic.
No anachronistic optimization.
Scalability over duplication.

---

End of Project Master.

