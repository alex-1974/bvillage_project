```markdown
# BVILLAGE v0.4.0 — STABILIZATION

---
tier: 3  
authority: OPERATIONAL  
scope: v0.4.0 only  
goal: Architectural stabilization before scalability  
---

# PURPOSE

v0.4.0 STABILIZATION is not a feature phase.

It is a structural hardening phase.

The objective is to ensure that:

- Terminology is frozen.
- Policy resolution has a single source of truth.
- Layer boundaries are enforced.
- The pipeline is deterministic and testable.
- The Hallenhaus is architecturally plausible and reproducible.
- No silent fallbacks exist.

No new archetypes.  
No structural expansion.  
No scalability work.  

Only stabilization.

---

# PHASE 1 — TERMINOLOGY FREEZE

## ENG-003 — Atomic Naming Commit

**Status: DONE**

44 Rename-Operationen über 19 Dateien. Tests grün. Determinismus bestätigt.
Zwei dokumentierte Spec-Abweichungen: `binder_max` statt `max_bay_width`,
`width_range` statt `width_between_posts` — beide fachlich begründet.
Delivery record: DEV_ROADMAP COMPLETED-Sektion.

---

# PHASE 2 — SINGLE SOURCE OF TRUTH

## ARC-001A — PolicyStack Hardening

**Priority:** CRITICAL  
**Blocks:** ARC-001

### Goal

PolicyStack becomes structurally robust.  
No silent policy drift allowed.

### Tasks

- HARD error for unknown patch keys
- Add invariant validation hook
- Add resolver-level reporting
- Ensure placeholder slots exist for future axes
- Confirm deterministic resolution

### Definition of Done

- No silent fallback inside PolicyStack
- Policy resolution is auditable

---

## ARC-001 — Three-Axis Separation

**Priority:** CRITICAL  

### Goal

Eliminate parallel policy logic in `architect.py`.

`resolve_policy_stack(ctx)` becomes the single policy authority.

### Tasks

- Remove `_hallenhaus_policy(ctx)`
- Architect exclusively consumes `ResolvedPolicy`
- FramePolicy derived only from resolved policy
- Cross-layer data flow documented
- Determinism verified after refactor

### Definition of Done

- No policy logic exists outside PolicyStack
- No structural defaults invented in architect layer

---

# PHASE 3 — PIPELINE INTEGRITY

## INT-001 — Architect / Planner Integration

**Priority:** HIGH  

### Goal

Define and freeze the structural relationship between Architect and Planner.

### Decisions

- Architect owns StructurePlan + FramePlan
- Planner produces InteriorPlan only
- Planner cannot mutate FramePlan
- Openings resolved via declared demands, not direct geometry edits

### Tasks

- Fix pipeline order
- Define data contracts
- Document integration decision
- Verify deterministic behavior

### Definition of Done

- Clear ownership model
- No ambiguous cross-layer mutation

---

## QLT-001 — Issue Schema Standardization

**Priority:** HIGH  

### Goal

All validators emit a unified Issue object.

### Tasks

- Standard Issue schema
- Severity levels: HARD / SOFT / SUGGEST
- Stage-level aggregation
- Fachwerk namespace convention

### Definition of Done

- All validation output uniform
- Reporting deterministic and structured

---

## PPV-001 — PhysicalPlausibilityValidator Wiring

**Priority:** MEDIUM  

### Goal

PPV runs in the pipeline but does not block build.

### Tasks

- Integrate into pipeline
- Ensure no geometry mutation
- Display PPV report
- Verify determinism unaffected

### Definition of Done

- PPV fully wired
- Informational only
- No hidden geometry adjustments

---

# PHASE 4 — LAYER HYGIENE

## HYGIENE-001

**Priority:** LOW  

### Goal

Remove known boundary violations before scaling.

### Tasks

- Move OpeningProfilePolicy out of Blender layer
- Remove legacy axis fallback paths
- Fix minor scan warnings
- Clean up test metadata

### Definition of Done

- No known layer violations remain
- Builders are pure renderers

---

# PHASE 5 — DETERMINISM LOCK

## Snapshot & Reproducibility

**Priority:** CRITICAL (final gate)

### Tasks

- Golden snapshot for seed=123
- Multi-run reproducibility test
- No non-seeded randomness
- Confirm same result across repeated builds

### Definition of Done

- Same seed → identical FramePlan
- Identical Blender output
- Snapshot locked

---

# FINAL DEFINITION OF DONE — v0.4.0 STABILIZED

v0.4.0 is stabilized when:

1. Hallenhaus generates deterministically.
2. Blender renders structurally correct output.
3. PolicyStack is the only policy source.
4. Terminology is frozen.
5. No silent fallbacks exist.
6. All validators use unified Issue schema.
7. PPV runs (non-blocking).
8. Layer boundaries are clean.
9. Golden snapshot is stable.
10. Pipeline data ownership is documented.

---

# EXPLICITLY OUT OF SCOPE

The following belong to v0.4.x or later:

- Role architecture (ROL-001+)
- Type-agnostic planner
- Stadthaus implementation
- Multi-candidate search
- Span-driven dimension solver
- Semantic preference layer
- CultureMap / EcoMap
- Structural intelligence extensions
- Settlement-level logic

---

# STRATEGIC OUTCOME

After v0.4.0 STABILIZATION:

- Architecture is internally consistent.
- Policy resolution is singular and auditable.
- Terminology will not shift during scaling.
- The system is ready for role architecture.
- No rewrite will be required to add a second archetype.

---

# GUIDING PRINCIPLE

The project is allowed to be incomplete.  
It is not allowed to be inconsistent.
```

