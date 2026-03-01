# ============================================================
# BVILLAGE – v0.4.0 STABILIZATION PHASE
# ============================================================

version: 0.4.0
goal: Architectural closure of members-only system (schema v3)
status: active

---

## Definition of 0.4.0 Done

A complete Hallenhaus generation run:

- uses resolve_policy_stack() exclusively
- produces a members-only FramePlan (no axis-derived geometry)
- resolves all materials via MaterialRegistry
- runs PPV (non-blocking)
- is fully deterministic (same seed → identical output)
- passes golden snapshot tests

No silent fallbacks. No layer violations. No global RNG usage.

---

# PHASE A – Determinism Lock (MANDATORY FIRST)

### DET-001 – Remove global RNG (openings)

Files:
- bvillage/types/fachwerkhaus/hallenhaus/openings.py

Tasks:
- Replace random.* with local Random(ctx.seed.derive("openings.*"))
- Ensure stable ordering before sampling

DoD:
- Same seed produces identical openings across runs
- No direct import/use of global random


### DET-002 – Remove global RNG (FramePlan derivation)

Files:
- bvillage/domains/fachwerk/core/frameplan.py

Tasks:
- All randomness via local RNG from ctx.seed
- No ordering dependence on dict/set iteration

DoD:
- Golden snapshot stabilizes
- FramePlan identical across repeated runs

---

# PHASE B – Policy System Closure

### ARC-001 – Remove local hallenhaus policy

Files:
- bvillage/types/fachwerkhaus/hallenhaus/planner.py

Tasks:
- Delete _hallenhaus_policy(ctx)
- Use resolve_policy_stack(ctx) exclusively
- Populate FramePolicy from ResolvedPolicy only

DoD:
- No structural defaults inside planner
- PolicyStack is single source of truth


### ARC-001A-1 – Strict patch key validation

Files:
- bvillage/core/policy_stack.py
- bvillage/core/policy_types.py

Tasks:
- Unknown patch key → HARD Issue / PolicyError
- No silent acceptance

DoD:
- Unit test: unknown key reliably detected


### ARC-001A-2 – Policy invariant hook

Files:
- bvillage/core/policy_stack.py

Tasks:
- Implement validate_policy_invariants(resolved_policy)
- Hook always runs (even if empty)

DoD:
- Deterministic issue reporting
- No policy resolution without invariant check


### ARC-001A-3 – Policy resolution diagnostics

Files:
- bvillage/core/policy_stack.py
- bvillage/core/report.py

Tasks:
- Report applied layers
- Report overridden keys (old → new)
- Stable sorted output

DoD:
- Snapshot-stable resolver report

---

# PHASE C – Issue System + PPV Integration

### QLT-001 – Issue schema unification

Files:
- bvillage/core/model.py
- bvillage/core/validate.py

Tasks:
- Enforce HARD / SOFT / SUGGEST everywhere
- Add category namespace (e.g., fachwerk.*)
- Ensure aggregation works pipeline-wide

DoD:
- Consistent issue output across all stages


### PPV-001 – PhysicalPlausibilityValidator in pipeline

Files:
- bvillage/core/quality/physical_plausibility_validator.py
- Runner/Orchestrator integration

Tasks:
- PPV runs automatically
- Issues reported in final output
- Non-blocking for 0.4.0

DoD:
- PPV visible in run log
- Generation continues despite HARD PPV issue

---

# PHASE D – Members-Only Enforcement

### HYGIENE-001A – Remove axis fallback in opening builder

Files:
- bvillage/domains/fachwerk/blender/opening_frames.py

Tasks:
- No reconstruction from axes
- Use explicit members only
- Missing members → abort / Issue

DoD:
- Renderer builds exclusively from FramePlan members


---

# PHASE E – Material System Wiring (MVP)

### MAT-001-MVP – Resolve material before render

Files:
- bvillage/core/materials/material_registry.py
- Fachwerk FramePlan generation
- Blender builder assignment

Tasks:
- Every member has material_id
- resolve_material(member, ctx) called
- Unregistered material → HARD Issue
- sample_render(material, condition, finish, seed, salt) used for variation

DoD:
- No implicit material defaults
- Deterministic visual sampling


---

# PHASE F – Regression Lock

### ENG-002-Lite – Golden snapshot (seed=123)

Files:
- tests/test_golden_reports.py

Tasks:
- Snapshot FramePlan dict
- Snapshot resolver report
- Stable sorted format (no timestamps)

DoD:
- Changing output requires explicit snapshot update
- Protects 0.4.0 architecture baseline


---

# Explicitly NOT in 0.4.0

- New archetypes
- New construction domains
- Earth architecture
- Settlement-level multiprocessing
- Mechanical material degradation
- Complex interior optimization loops

These belong to 0.5.x and later.

