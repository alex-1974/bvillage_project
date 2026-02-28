# BVILLAGE – System Contract

---
tier: 1
authority: CANONICAL
change-frequency: rare
change-rule: Every change requires an explicit architecture decision and schema review. Requires CHANGELOG entry.
referenced-by: ENG_BUILDER_CONTRACT.md, ARCH_POLICIES.md, DOCS_INDEX.md
references: SYS_PRINCIPLES.md, SYS_CONCEPTS.md
---

This document defines what every module in the system must and must not do. It contains rules and their consequences — not explanations of why the architecture is designed this way. For that, see SYS_PRINCIPLES.md and SYS_CONCEPTS.md.

Violations of this contract are architectural failures, not implementation bugs.

---

## 1. Structural truth

**1.1** The FramePlan is the single source of structural truth. All geometry derives from FramePlan data.

**1.2** Axes (axes_u, axes_z) are planning metadata. They are not geometry. No module may interpret axis data as geometry.

**1.3** The renderer builds from members exclusively. It may not derive members from axes, infer members from spans, or reconstruct structure from any source other than the members list.

**1.4** FramePlan must emit explicit members. `frameplan_to_dict()` must convert all planning data into members before the renderer receives it.

**1.5** Missing members is a contract failure. The renderer must abort if required members are absent. No fallback geometry is permitted for `schema_version >= 3`.

---

## 2. Layer boundaries

**2.1** Core modules must never import the renderer (bpy or equivalent).

**2.2** Domain-core must never import the renderer.

**2.3** Type modules must not contain renderer code.

**2.4** Renderer modules may read domain artifacts. They must not mutate them.

**2.5** The planner must operate exclusively on ResolvedPolicy. It must not contain embedded structural defaults, regional assumptions, or epoch-specific logic.

**2.6** Domain and CulturePolicy must not read region or epoch directly from context. They consume already-resolved policy data only.

**2.7** StylePolicy must not switch construction domains, replace archetypes, or inject structural members.

**2.8** The InteriorPlanner must not touch the FramePlan directly. It communicates opening demands to the TypePlanner. All exterior structural consequences of interior decisions pass through the planner boundary — never through direct FramePlan mutation.

---

## 3. Data model

**3.1** Core dataclasses are frozen and immutable after creation.

**3.2** StructurePlan, InteriorPlan, and OpeningsPlan must not be mutated by any stage after they are produced.

**3.3** Domain artifacts are stored and accessed exclusively via:
```
notes["domains"][domain][artifact]
```

**3.4** Legacy aliases are transitional only. New code must not write legacy aliases.

---

## 4. Policy system

**4.1** Policy resolution follows a single entry point: `resolve_policy_stack(ctx) → ResolvedPolicy`.

**4.2** Every policy is a delta — a set of overrides on the canonical parameter tree. Policies must not duplicate full parameter trees.

**4.3** Policies may only override defined canonical parameters. Patching an unknown key must produce a HARD Issue. Silent acceptance of unknown keys is forbidden.

**4.4** Silent fallback behavior anywhere in the policy stack is forbidden.

**4.5** Subtypes must be local to a specific archetype or implemented as optional patch axes. Subtypes must never become mandatory global fields. An unsupported subtype request must produce an explicit HARD or SOFT Issue — silent ignore is forbidden.

**4.6** ResolvedPolicy must pass invariant validation before planning begins. Invariant violations must be logged and deterministic.

---

## 5. Determinism

**5.1** Same seed + same policy produces an identical result, always.

**5.2** All iteration ordering must be explicit and stable. No module may rely on unordered dict iteration or set ordering.

**5.3** All random sampling must use a local RNG seeded from `ctx.seed`. No module may call a global random number generator.

---

## 6. Numerical stability

**6.1** All float tolerances are centralized in `geom_eps`. No module may define ad-hoc epsilon values.

**6.2** Geometry repairs must not silently change values. Any repair must be logged at WARNING level and appear in the planner report.

**6.3** Silent clamping is forbidden.

---

## 7. Validation

**7.1** All validators emit Issue objects. Validators must not mutate geometry.

**7.2** Core validation is type-agnostic. Type-specific validation stays inside type modules.

**7.3** Validation must not exist inside renderer modules.

**7.4** Issue severity levels: HARD (blocks generation), SOFT (scored penalty), SUGGEST (informational).

---

## 8. Tests

**8.1** If a test encodes behavior, that behavior is part of the contract.

**8.2** Golden output snapshots must not change without a documented reason and a CHANGELOG entry.

**8.3** Any structural change requires a new reproduction case.

---

## 9. Schema versioning

**9.1** `schema_version = 3` defines the members-only architecture.

**9.2** For `schema_version >= 3`: members are mandatory, legacy geometry paths are forbidden, renderer fallback logic is prohibited.

**9.3** Any change to the members structure, layer boundaries, or contract semantics requires a schema version increment.

---

## 10. File identity

**10.1** Every `.py` file must declare its canonical project path as the very first line:
```python
# bvillage/domains/fachwerk/blender/roof.py
```

**10.2** The path must match the repository structure exactly. No docstring may precede it.

**10.3** During refactors, this line must be updated to match the new location.

---

## 11. Naming

**11.1** File names follow the pattern `<role>_<aspect>.py`. Generic names (utils.py, helpers.py, check.py) are forbidden.

**11.2** Allowed roles: `plan_`, `derive_`, `build_`, `validate_`, `audit_`, `report_`, `policy_`, `schema_`, `mesh_`.

**11.3** Function names follow `<verb>_<object>_<qualifier>()`. Verb meanings:
- `build_*` — emits geometry
- `derive_*` — computes data
- `normalize_*` — transforms data
- `audit_*` — returns a report, does not raise
- `assert_*` — enforces an invariant, may raise

**11.4** Naming must reflect architectural layer. Core modules use no renderer terms. Renderer modules use no constructive inference terms.

**11.5** New files and functions must follow this policy immediately. Full repository rename is deferred to the controlled window defined in the roadmap.

Role semantics, review criteria, and the rationale behind each naming rule are documented in SYS_NAMING_POLICY.md.

---

## 12. Experimentation boundaries

The following may change freely during development:
- Domain heuristics and parameters
- Policy tuning and content
- Interior layout logic
- Roof detailing
- Infill generation

The following must not change without an explicit architecture decision:
- Layer boundaries
- Notes schema
- Determinism guarantees
- Logging discipline
- Contract semantics

---

## 13. Known failure modes

These are the most common ways this contract is violated. Each has been observed to cause real problems.

**Builder derives members from axes instead of the members list.** Consequence: elements appear through openings; geometry is unreproducible.

**FramePlan stores axes but not members.** Consequence: constructive logic duplicates into the renderer, creating two sources of truth.

**Interior modifies exterior walls directly.** Consequence: role boundary violation; exterior and interior logic become entangled.

**Renderer reconstructs structure from axes.** Consequence: members-first architecture is violated; structural decisions migrate to the wrong layer.

**FramePlan emits incomplete members.** Consequence: contract breach; renderer either fails or invents structure.

**Planner contains embedded regional or epochal defaults.** Consequence: new regions or epochs require planner changes instead of policy additions; scalability collapses.

**StylePolicy encodes structural grammar differences.** Consequence: variations that require different member generation are invisible to validation; structural errors accumulate silently.

---

## 14. Material system

**14.1** Every material ID used anywhere in the system must be registered in the MaterialRegistry. An unregistered material ID is a contract violation. There is no fallback and no default substitution. Generation stops with a HARD Issue.

**14.2** Physics parameters and render parameters are carried by the same material node but must never influence one another. Physics parameters must not be changed for visual reasons. Render parameters must not be changed for physics reasons.

**14.3** Visual variation is produced exclusively via:
```
sample_render(material, condition, finish, seed, salt) → RenderSample
```
`salt` is a stable member identifier. The same member with the same seed always produces the same visual sample. No module involved in rendering may call a global random number generator.

**14.4** `resolve_material(member, ctx) → MaterialVariant` is the single material resolution point. No renderer module may select or construct a material variant by any other means.

**14.5** ProductForm, Condition, and Finish are not material IDs. They are separate member attributes passed to `resolve_material()` and `sample_render()`. They must not be encoded in the material ID string.

The material catalogue and resolution logic are defined in ARCH_MATERIALS.md. This section states the contractual obligations — ARCH_MATERIALS.md provides the content.
