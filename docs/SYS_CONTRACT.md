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

**1.1** The `FramePlan` is the single source of structural truth. All geometry derives from `FramePlan` data.

**1.2** Axes (`axes_u`, `axes_z`) are planning metadata. They are not geometry. No module may interpret axis data as geometry.

**1.3** The Renderer builds from members exclusively. It may not derive members from axes, infer members from spans, or reconstruct structure from any source other than the members list.

**1.4** `FramePlan` must emit explicit members. `frameplan_to_dict()` must convert all planning data into members before the Renderer receives it.

**1.5** Missing members is a contract failure. The Renderer must abort if required members are absent. No fallback geometry is permitted for `schema_version >= 3`.

---

## 2. Layer boundaries

**2.1** Core modules must never import the renderer (`bpy` or equivalent).

**2.2** Domain-core must never import the renderer.

**2.3** Type modules must not contain renderer code.

**2.4** Renderer modules may read domain artifacts. They must not mutate them.

**2.5** The Topology Planner must operate exclusively on `ResolvedPolicy`. It must not contain embedded structural defaults, regional assumptions, or epoch-specific logic.

**2.6** The Frame Producer and `CulturePolicy` must not read region or epoch directly from context. They consume already-resolved policy data only.

**2.7** `StylePolicy` must not switch construction domains, replace archetypes, or inject structural members.

**2.8** The Joiner must not touch the `FramePlan` or `RoofPlan` directly. It communicates opening demands to the Topology Planner. All exterior structural consequences of interior decisions pass through the Topology Planner boundary — never through direct plan mutation.

**2.9** The Roof Producer receives the `FramePlan` and `ResolvedPolicy`. It must not modify the `FramePlan`. It produces a `RoofPlan` as a separate artifact.

**2.10** The Inspector operates on abstracted structural data only. It must not read `FramePlan` members directly. The domain is responsible for translating `FramePlan` into the Inspector's input format.

**2.11** The Foreman dispatches by interface. It must not import concrete plugin implementations. All specialist access is mediated through the plugin registry.

---

## 3. Plugin system

**3.1** Every pipeline role above the Foreman level is expressed as a Python `Protocol` in `core/`. Plugins implement these protocols under domain-specific names.

**3.2** The plugin registry maps `ArchetypeBinding` entries — `(archetype_id, type_family, domain, construction_grammar)` — to interface implementations. The registry is the single source of dispatch truth.

**3.3** Every plugin registers its `ArchetypeBinding` entries via a `register(registry)` function in its `__init__.py`. The Core does not know concrete archetype IDs.

**3.4** Requesting an unregistered archetype ID must produce a HARD Issue. Silent fallback to a default archetype is forbidden.

**3.5** Removing a plugin must not require changes to Core or to any other plugin.

**3.6** Adding a plugin must not require changes to Core or to any other plugin.

---

## 4. Data model

**4.1** Core dataclasses are frozen and immutable after creation.

**4.2** `SemanticPlan`, `FramePlan`, `RoofPlan`, and `InteriorPlan` must not be mutated by any stage after they are produced.

**4.3** Domain artifacts are stored and accessed exclusively via:
```
notes["domains"][domain][artifact]
```

**4.4** Legacy aliases are transitional only. New code must not write legacy aliases.

---

## 5. Policy system

**5.1** Policy resolution follows a single entry point: `resolve_policy_stack(ctx) → ResolvedPolicy`.

**5.2** Every policy is a delta — a set of overrides on the canonical parameter tree. Policies must not duplicate full parameter trees.

**5.3** Policies may only override defined canonical parameters. Patching an unknown key must produce a HARD Issue. Silent acceptance of unknown keys is forbidden.

**5.4** Silent fallback behavior anywhere in the policy stack is forbidden.

**5.5** Subtypes must be local to a specific archetype or implemented as optional patch axes. Subtypes must never become mandatory global fields. An unsupported subtype request must produce an explicit HARD or SOFT Issue — silent ignore is forbidden.

**5.6** `ResolvedPolicy` must pass invariant validation before planning begins. Invariant violations must be logged and deterministic.

**5.7** `FunctionPolicy` is a mandatory field in every `BuildingOrder`. Default value: `building_use=RESIDENTIAL`. A missing `FunctionPolicy` is a contract violation.

---

## 6. Determinism

**6.1** Same seed + same policy produces an identical result, always.

**6.2** All iteration ordering must be explicit and stable. No module may rely on unordered dict iteration or set ordering.

**6.3** All random sampling must use a local RNG seeded from `ctx.seed`. No module may call a global random number generator.

---

## 7. Numerical stability

**7.1** All float tolerances are centralized in `geom_eps`. No module may define ad-hoc epsilon values.

**7.2** Geometry repairs must not silently change values. Any repair must be logged at WARNING level and appear in the planner report.

**7.3** Silent clamping is forbidden.

---

## 8. Validation

**8.1** All validators emit `Issue` objects. Validators must not mutate geometry.

**8.2** Core validation is type-agnostic. Type-specific validation stays inside type modules.

**8.3** Validation must not exist inside Renderer modules.

**8.4** Issue severity levels: HARD (blocks generation), SOFT (scored penalty), SUGGEST (informational).

---

## 9. Tests

**9.1** If a test encodes behavior, that behavior is part of the contract.

**9.2** Golden output snapshots must not change without a documented reason and a CHANGELOG entry.

**9.3** Any structural change requires a new reproduction case.

---

## 10. Schema versioning

**10.1** `schema_version = 3` defines the members-only architecture.

**10.2** For `schema_version >= 3`: members are mandatory, legacy geometry paths are forbidden, Renderer fallback logic is prohibited.

**10.3** Any change to the members structure, layer boundaries, plugin contract, or contract semantics requires a schema version increment.

---

## 11. File identity

**11.1** Every `.py` file must declare its canonical project path as the very first line:
```python
# bvillage/domains/fachwerk/core/derive_frameplan_boxframe.py
```

**11.2** The path must match the repository structure exactly. No docstring may precede it.

**11.3** During refactors, this line must be updated to match the new location.

---

## 12. Naming

**12.1** File names follow the pattern `<role>_<aspect>.py`. Generic names (`utils.py`, `helpers.py`, `check.py`) are forbidden.

**12.2** Allowed file roles: `plan_`, `derive_`, `build_`, `validate_`, `audit_`, `report_`, `policy_`, `schema_`, `mesh_`.

**12.3** Function names follow `<verb>_<object>_<qualifier>()`. Verb meanings:
- `build_*` — emits geometry
- `derive_*` — computes data
- `normalize_*` — transforms data
- `audit_*` — returns a report, does not raise
- `assert_*` — enforces an invariant, may raise

**12.4** Naming must reflect architectural layer. Core modules use no renderer terms. Renderer modules use no constructive inference terms.

**12.5** New files and functions must follow this policy immediately. Full repository rename is deferred to the controlled window defined in the roadmap.

Role semantics, review criteria, and the rationale behind each naming rule are documented in `SYS_NAMING_POLICY.md`.

---

## 13. Experimentation boundaries

The following may change freely during development:
- Domain heuristics and parameters
- Policy tuning and content
- Interior layout logic
- Roof construction detail
- Infill generation

The following must not change without an explicit architecture decision:
- Layer boundaries
- Plugin registry contract
- Notes schema
- Determinism guarantees
- Logging discipline
- Contract semantics

AI-assisted contributions are governed by `ENG_AI_CONTRIBUTION_RULES.md`. That document defines integrity constraints, stop conditions, and session continuity protocol. Its rules have the same force as the conventions in `ENG_CODING_GUIDE.md`.

---

## 14. Known failure modes

These are the most common ways this contract is violated. Each has been observed to cause real problems.

**Renderer derives members from axes instead of the members list.** Consequence: elements appear through openings; geometry is unreproducible.

**`FramePlan` stores axes but not members.** Consequence: constructive logic duplicates into the Renderer, creating two sources of truth.

**Joiner modifies `FramePlan` or `RoofPlan` directly.** Consequence: role boundary violation; interior and structural logic become entangled.

**Renderer reconstructs structure from axes.** Consequence: members-first architecture is violated; structural decisions migrate to the wrong layer.

**`FramePlan` emits incomplete members.** Consequence: contract breach; Renderer either fails or invents structure.

**Topology Planner contains embedded regional or epochal defaults.** Consequence: new regions or epochs require planner changes instead of policy additions; scalability collapses.

**`StylePolicy` encodes structural grammar differences.** Consequence: variations that require different member generation are invisible to validation; structural errors accumulate silently.

**Foreman imports concrete plugin implementations.** Consequence: plugin isolation is broken; adding or removing a plugin requires Foreman changes.

**Frame Producer reads region or epoch directly from context.** Consequence: CulturePolicy is bypassed; historical plausibility becomes non-deterministic with policy changes.

**`FunctionPolicy` absent from `BuildingOrder`.** Consequence: building use is undefined; zone program, opening character, and representation direction resolve incorrectly.

---

## 15. Material system

**15.1** Every material ID used anywhere in the system must be registered in the `MaterialRegistry`. An unregistered material ID is a contract violation. There is no fallback and no default substitution. Generation stops with a HARD Issue.

**15.2** Physics parameters and render parameters are carried by the same material node but must never influence one another. Physics parameters must not be changed for visual reasons. Render parameters must not be changed for physics reasons.

**15.3** Visual variation is produced exclusively via:
```
sample_render(material, condition, finish, seed, salt) → RenderSample
```
`salt` is a stable member identifier. The same member with the same seed always produces the same visual sample. No module involved in rendering may call a global random number generator.

**15.4** `resolve_material(member, ctx) → MaterialVariant` is the single material resolution point. No Renderer module may select or construct a material variant by any other means.

**15.5** `ProductForm`, `Condition`, and `Finish` are not material IDs. They are separate member attributes passed to `resolve_material()` and `sample_render()`. They must not be encoded in the material ID string.

The material catalogue and resolution logic are defined in `ARCH_MATERIALS.md`. This section states the contractual obligations — `ARCH_MATERIALS.md` provides the content.
