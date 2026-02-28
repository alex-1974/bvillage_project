# BVILLAGE – Development Roadmap

---
tier: 3
authority: OPERATIONAL
change-frequency: frequent
change-rule: Enthält nur Tasks und Milestones. Keine Architekturprinzipien. Bei Konflikt mit Tier 1/2 → Tier 1/2 gewinnt.
referenced-by: —
references: SYS_PRINCIPLES.md, SYS_CONTRACT.md (Schema), DOCS_INDEX.md
---

# HOW TO READ THIS DOCUMENT

This roadmap has four levels:

**v0.4.0** — What is being built now. Concrete, sequenced, completable.

**v0.4.x** — Preparation phase. Policy axes woven in, structural intelligence built, pipeline interfaces frozen. Everything v0.5.0 needs must be ready here.

**v0.5.0** — Second house: Fachwerk Stadthaus. This is the scalability proof. If the Stadthaus emerges without structural rewrites, the architecture holds.

**Vision** — Long-term ideas that influence today's architecture without creating delivery pressure. These are architectural guardrails, not commitments. Research findings may promote items from Vision into v0.4.x or beyond.

The roadmap is a living document. It accumulates knowledge.
New research findings, architectural insights, and pipeline experience
will change priorities and promote items between levels.

---

# COMPLETED

## ARC-000 — Members-Only Architecture (Schema v3)

Version: v0.3.0
Status: DONE

Delivered:
- Builder fully members-driven
- No axis-derived geometry
- No structural fallbacks
- Contract hardened (members mandatory)
- FramePolicy controls structural profiles
- Determinism preserved

Result: Canonical structural truth established.

---

# v0.4.0 — First House + Foundation

## Goal

A architecturally plausible Fachwerk Langhaus (Hallenhaus) emerges
deterministically through the full pipeline and is visible in Blender.

The structure must be verifiable by eye: posts, rails, braces, openings,
infills, roof — laid out correctly. Colors, surface quality, and material
detail are explicitly out of scope.

In parallel, the structural foundations are laid such that future house types,
regions, and epochs do not require rewrites.

This version is explicitly a learning phase. The pipeline will be explored,
the InteriorPlanner will be integrated earlier than anticipated, and research
findings will continuously inform architectural decisions.

---

## RES-001 — Historical Research (Ongoing)

Status: ACTIVE
Priority: CRITICAL

Research is a first-class task in v0.4.0, not a background activity.
Findings directly determine which policy axes are needed and how they are structured.

Open questions (not exhaustive):

- Which structural differences between regions and epochs require separate
  ConstructionDomains or CulturePolicy branches — and which are merely
  StylePolicy modulation?
- How does building use (agricultural, mercantile, residential) affect
  structural dimensions — not just floor plans?
- What did regional craft traditions enable or prevent? Which joinery,
  which spans, which bracing patterns were available where and when?
- Which aspects of medieval Fachwerk construction are still unknown
  or disputed in the literature?
- Roof construction: what is historically correct for the Hallenhaus?
  Kehlbalken, Firstpfette, Rofen, Sparren — which elements are present,
  in which combinations, in which regions and epochs?
  The current implementation shows open rafter framing; is this complete?

Deliverable:
A set of documented hypotheses that map observed historical phenomena
to policy axes (Domain / CulturePolicy / StylePolicy / Archetype).
This forms the basis for v0.4.x policy implementation.

Note:
Research findings are tracked separately (not in this roadmap).
This document reflects their architectural consequences.

---

## HOUSE-001 — Langhaus (Hallenhaus) through Full Pipeline

Status: ACTIVE
Priority: HIGH

Goal:
One complete, architecturally plausible Hallenhaus visible in Blender.
The result must be verifiable: correct structural members, plausible
opening positions, coherent roof, readable infills.

Scope:
- Planner generates StructurePlan + FramePlan
- InteriorPlanner integrated into pipeline (earlier than originally planned)
- FramePlan consumed by Blender builder
- Blender renders members-only result (no surface detail)
- No PPV gate (physics skeleton exists but does not block)

Not in scope:
- Material surfaces, textures, colors
- Physical validation as a hard gate
- Settlement-level placement

---

## ARC-001 — Three-Axis Separation (Planner Cleanup)

Status: ACTIVE
Priority: HIGH

Goal:
Eliminate the parallel policy system in planner.py.
`_hallenhaus_policy(ctx)` is replaced by `resolve_policy_stack(ctx)`.
FramePolicy is populated from ResolvedPolicy.

This is the single most important structural cleanup for v0.4.0.
Without it, the policy system has two sources of truth.

Tasks:
- [ ] Remove `_hallenhaus_policy(ctx)` from planner
- [ ] Wire planner to `resolve_policy_stack(ctx)`
- [ ] Populate FramePolicy from `resolved_policy.fachwerk`
- [ ] Verify determinism after switch
- [ ] Document allowed cross-layer data flow

---

## ARC-001A — PolicyStack Foundation

Status: ACTIVE
Priority: CRITICAL

Existing:
`policy_stack.py` and `policy_types.py` exist and are well-structured.
`resolve_policy_stack(ctx)` is implemented for Hallenhaus.

Goal:
The PolicyStack is the single entry point for all policy resolution.
No planner or domain may invent structural defaults independently.

Remaining tasks:
- [ ] Enforce that planner uses ResolvedPolicy exclusively (ARC-001 above)
- [ ] Add HARD error for unknown patch keys (forward-guard)
- [ ] Add invariant validation hook (empty allowed for now)
- [ ] Add resolver-level reporting (for diagnostics)
- [ ] Ensure policy slots exist for axes identified in RES-001
  (even if content is minimal — slots must not be absent)

Note:
The exact set of policy axes is still informed by research (RES-001).
Slots are added as hypotheses are confirmed.

---

## INT-001 — InteriorPlanner Pipeline Integration

Status: ACTIVE
Priority: HIGH

Goal:
InteriorPlanner must enter the pipeline earlier than originally planned.
Without it, the Hallenhaus cannot be correctly generated — room zones,
opening demands, and interior structure are interdependent.

This version is exploratory. The exact integration point will be
determined during v0.4.0 work.

Tasks:
- [ ] Determine correct pipeline position for InteriorPlanner
- [ ] Define data contract between Planner and InteriorPlanner
- [ ] Ensure InteriorPlanner cannot modify exterior FramePlan directly
- [ ] Document findings for pipeline interface freeze (v0.4.x)

---

## QLT-001 — Issue Schema Standardization

Status: ACTIVE
Priority: HIGH

Goal:
All validators emit Issue objects with consistent schema.
This must be in place before PPV and the pipeline report are wired together.

Tasks:
- [ ] Standardize Issue schema across all validators
- [ ] Severity levels: HARD / SOFT / SUGGEST
- [ ] Aggregate report (per stage)
- [ ] Domain-specific issue categories (fachwerk namespace)

---

## PPV-001 — PhysicalPlausibilityValidator (Skeleton)

Status: PLANNED
Priority: MEDIUM

Goal:
PPV exists and runs. It does not block the build in v0.4.0.
It emits Issues for informational use only.

Existing:
`physical_plausibility_validator.py` exists with MVP checks.

Remaining:
- [ ] Wire PPV into pipeline (non-blocking)
- [ ] PPV report visible in generation output
- [ ] Verify PPV does not alter geometry

Note:
Full structural validation requires completed physics engine.
That is explicitly a post-v0.4.0 concern.

---

## HYGIENE-001 — Layer Boundary Cleanup

Status: PLANNED
Priority: LOW (does not block house generation)

Goal:
Remove known boundary violations before they multiply.

Tasks:
- [ ] Move `OpeningProfilePolicy` out of Blender layer into domain-core or policy
- [ ] Remove legacy `axis_x` / `axis_y` fallback from `opening_frames.py`
  (members-first path already exists; legacy path to be removed once verified)
- [ ] Add path header to `tests/test_constraints.py` (trivial scan issue)

---

## Definition of Done — v0.4.0

v0.4.0 is complete when:

1. A Hallenhaus is generated deterministically through the full pipeline
2. Blender renders the result: posts, rails, braces, openings, infills, roof
3. The result is verifiable by eye as architecturally plausible
4. `resolve_policy_stack(ctx)` is the single source of policy truth
5. All validators emit standardized Issue objects
6. PPV runs but does not block
7. Research findings are documented as policy-axis hypotheses
8. Determinism is confirmed (same seed → identical result)

---

# v0.4.x — Policy Weaving + Structural Intelligence

## Purpose

v0.4.x translates the research findings and architectural preparations
from v0.4.0 into concrete implementations. The policy axes identified
in RES-001 are woven into the system. Structural dimensions become
span-driven. The pipeline interfaces are frozen.

Every item in v0.4.x is a prerequisite for v0.5.0.
The test question for each task: *Would the Stadthaus work without this?*
If no — it belongs here. If yes — it may be deferred.

Items in this section are candidates. Their exact scope and sequencing
depend on v0.4.0 experience and research outcomes.

Prerequisites for v0.5.0 that must be completed in v0.4.x:

- `resolve_policy_stack(ctx)` handles multiple archetypes without branching on type
- Fachwerk planner is type-agnostic — Hallenhaus and Stadthaus share the same engine
- FramePlan schema supports vertical stacking and façade-oriented topology
- InteriorPlanner contract is frozen and supports different room programs
- Policy axes cover Stadthaus parameters (narrow parcel, multi-storey, potential jetties)
- All structural constants replaced by span-driven resolution
- Pipeline interfaces frozen — no stage rewrites needed for a new type

---

## Prefix Legend

| Prefix | Domain |
|--------|--------|
| RES-   | Research |
| SYS-   | System Architecture & Schema |
| STR-   | Structural Physics |
| MAT-   | Material System |
| SEM-   | Semantics & Variation |
| ENG-   | Engineering & Tooling |
| CR-    | Crossroad |

---

## Crossroads

A Crossroad is a point where parallel work streams converge and a new
direction becomes possible. It is not a deadline — it is a state.
Work that depends on a Crossroad may not begin until that state is reached.

Three Crossroads structure v0.4.x:

| ID    | Name                  | Reached when                                      | Unlocks |
|-------|-----------------------|---------------------------------------------------|---------|
| CR-1  | Research Converged    | RES-001 + RES-002 deliver documented hypotheses   | SYS-001, SYS-002, SYS-003, STR-003 |
| CR-2  | Architecture Stable   | SYS-001 + SYS-002 + SYS-003 complete           | STR-001, STR-002, MAT-001, SEM-001, SYS-004 |
| CR-3  | Engine Complete       | STR-001, STR-002, MAT-001, SEM-001, SYS-004, ENG-002 complete | SEM-002, SEM-003, ENG-003, v0.5.0 |

ENG-001 and ENG-002 are independent of all Crossroads and may begin immediately.

---

## CR-1 — Research Converged

Reached when:
- RES-001 has delivered documented hypotheses mapping Hallenhaus phenomena
  to policy axes (Domain / CulturePolicy / StylePolicy / Archetype)
- RES-002 has delivered documented hypotheses for the Stadthaus,
  including construction grammar, room program, and schema implications
- The boundary between Domain, CulturePolicy, and StylePolicy
  is explicitly decided for at least the Hallenhaus and Stadthaus cases

This Crossroad does not require complete historical certainty.
Documented hypotheses are sufficient. Decisions can be revised —
but they must be explicit before architecture begins.

Unlocks: SYS-001, SYS-002, SYS-003, STR-003

---

## CR-2 — Architecture Stable

Reached when:
- SYS-001: Policy axes implemented, PolicyStack is multi-archetype entry point
- SYS-002: Fachwerk planner is type-agnostic, Hallenhaus generates identically
- SYS-003: FramePlan schema has slots for multi-storey and jetties,
  backward compatible with Hallenhaus

At this point the engine can accept a second archetype without structural rewrites.
This is the architectural proof-of-concept before the Stadthaus is built.

Unlocks: STR-001, STR-002, MAT-001, SEM-001, SYS-004, SYS-005

---

## CR-3 — Engine Complete

Reached when:
- STR-001: Span-driven dimension resolution replaces fixed constants
- STR-002: Physics and CulturePolicy are separated
- MAT-001: MaterialRegistry drives both physics and rendering
- SEM-001: Soft/Hard parameter ranges in place
- SYS-004: Pipeline interfaces frozen
- ENG-002: Golden snapshot for seed=123 passes

At this point the engine is structurally complete for v0.5.0.
The Stadthaus can be built. Semantic variation and multi-candidate search
can be wired in without structural interference.

Unlocks: SEM-002, SEM-003, ENG-003, v0.5.0

---

## Research

### RES-002 — Stadthaus Research

Priority: HIGH
Requires: RES-001 (partially — roof and culture axis questions overlap)
Unlocks: SYS-001 (Stadthaus policy axes), SYS-002 (planner factoring), SYS-003 (schema extension)
Must complete before v0.5.0 begins.

Research into the Fachwerk Stadthaus is a prerequisite for v0.5.0.
Implementation must not begin before these questions are answered.

Open questions:

- Which Stadthaus variants are most representative and tractable as a first implementation?
  (Giebelständiges vs. Traufenständiges, single vs. multi-bay)
- When and where did jetties (Vorkragung) appear, and what drove their adoption?
  Are they CulturePolicy or a separate ConstructionDomain branch?
- How did urban plot constraints shape construction grammar differently from rural practice?
- What is the minimal Stadthaus room program, and how does it differ
  structurally from the Hallenhaus?
- Which bracing patterns and member rhythms are characteristic of urban Fachwerk?

Deliverable:
Documented hypotheses mapping Stadthaus observations to policy axes,
ready to feed into SYS-001 and SYS-003.

---

> **⊕ CR-1 — Research Converged**
> RES-001 + RES-002 complete. Hypotheses documented. Domain/CulturePolicy/StylePolicy
> boundary decided for Hallenhaus and Stadthaus cases.
> Architecture work may begin.

---

## System Architecture & Schema

### SYS-001 — Policy Axes Implementation

Priority: HIGH
Requires: SYS-002 (type-agnostic planner), RES-001, RES-002
Unlocks: STR-001, STR-002, MAT-001, SEM-001, SYS-004, SYS-005
Parallel: SYS-003, ENG-001, ENG-002 can run in parallel

Goal:
The policy axes identified in v0.4.0 research are woven into the system.
The PolicyStack becomes the single, multi-archetype entry point.

Candidate axes (hypotheses — subject to RES-001 confirmation):
- CulturePolicy: construction grammar, member spacing, bracing rules
- RoofPolicy: pitch ranges, overhang, eaves height
- OpeningsPolicy: opening counts, preferred walls, z-bands
- StyleContext: region × epoch × wealth modulation

Principle:
Each axis is added as an optional patch slot.
No existing archetype or domain requires modification when a new axis is added.
Unknown patch keys produce a HARD Issue.

Dependency: SYS-002 (planner type-agnosticity) must be complete first.

---

### SYS-002 — Fachwerk Planner Type-Agnosticity

Priority: HIGH
Requires: ARC-001 (v0.4.0 — planner on PolicyStack), RES-002
Unlocks: SYS-001

Goal:
The Fachwerk planner must serve multiple Fachwerk types without
type-specific branching in shared code.

Today the planner is implicitly Hallenhaus-specific — dimensions,
opening logic, and room programs are woven into a single flow.
Before a Stadthaus can be built, this must be factored out.

Tasks:
- [ ] Identify all Hallenhaus-specific assumptions in the shared planner path
- [ ] Extract type-specific logic into archetype modules
- [ ] Define the minimal shared interface that any Fachwerk type must implement
- [ ] Verify Hallenhaus still generates identically after refactor (determinism check)
- [ ] Document the extension contract for new Fachwerk archetypes

Dependency: ARC-001 (planner on PolicyStack, v0.4.0) must be complete first.

---

### SYS-003 — FramePlan Schema: Multi-Storey + Façade Topology

Priority: HIGH
Requires: RES-002
Unlocks: v0.5.0 (directly — Stadthaus cannot be built without this)
Parallel: SYS-002 (independent, can run simultaneously)

Goal:
The FramePlan schema must support constructs the Stadthaus requires
that the Hallenhaus does not: vertical stacking, floor-level
differentiation, and potential jetties.

This does not mean implementing these features — it means ensuring
the schema has slots for them, so no breaking change is needed in v0.5.0.

Tasks:
- [ ] Analyse what multi-storey framing requires in the members schema
- [ ] Define floor-level annotation on members (which storey does this member belong to?)
- [ ] Design jetty/Vorkragung representation (member role + geometry contract)
- [ ] Add schema_version guard for new fields
- [ ] Verify Hallenhaus FramePlan is unaffected (backward compatible)

Note:
Schema slots must exist in v0.4.x even if content is empty.
The Stadthaus must not require a schema_version bump at v0.5.0.

---

### SYS-004 — Pipeline Interface Freeze

Priority: HIGH
Requires: SYS-001, INT-001 (v0.4.0 — InteriorPlanner integration point documented)
Unlocks: SEM-003
Note: Must not be frozen before INT-001 findings are incorporated.
Stage interfaces are frozen. Immutability between stages is enforced.
Multi-candidate support is scaffolded.

The InteriorPlanner integration point determined in INT-001 (v0.4.0)
must be reflected here before the interfaces are frozen.
Freezing without this would require a later unfreeze.

Tasks:
- [ ] Incorporate InteriorPlanner position from INT-001 findings
- [ ] Freeze stage interfaces (OrderProvider → Planner → InteriorPlanner → Domain → Validator → Evaluator)
- [ ] Enforce immutability between stages
- [ ] Add stage-level reporting
- [ ] Scaffold multi-candidate support (no full implementation yet)

---

### SYS-005 — CultureMap MVP

Priority: MEDIUM
Requires: SYS-001 (policy axes must exist to receive culture candidates as prior)
Parallel: STR-001, STR-002, MAT-001 (independent once SYS-001 is stable)

Goal:
Lightweight data-driven mapping from (location × time) → building culture candidates.
Enables world-scale expansion without hardcoding geography into archetypes or domains.

Core concept:
- CultureTrace = (Polygon/MultiPolygon × TimeInterval) with fuzzy core/halo
- Output: top-k candidates with membership scores (0..1)
- Used as prior for PolicyStack

Tasks:
- [ ] Define CultureTrace data schema
- [ ] Add `data/culturemap/` with minimal seed catalog (Fachwerk first)
- [ ] Implement deterministic loader
- [ ] Implement point-in-polygon query
- [ ] Implement fuzzy scoring (core=1.0, halo=0.5)
- [ ] Add `culture_candidates(lon, lat, year, top_k)` resolver
- [ ] Unit tests: geometry membership, time membership, deterministic sort

Non-goals:
- No full historical boundary library
- No distance-decay fields
- No mandatory lat/lon in Context

---

> **⊕ CR-2 — Architecture Stable**
> SYS-001 + SYS-002 + SYS-003 complete. PolicyStack is multi-archetype.
> Planner is type-agnostic. FramePlan schema has Stadthaus slots.
> Structural intelligence and materials work may begin.

---

## Structural Physics

### STR-001 — Structural Dimension Resolution

Priority: HIGH
Requires: SYS-001
Unlocks: STR-002 (can run in parallel once SYS-001 is stable)
Parallel: MAT-001, STR-002
Replace fixed beam dimensions with span-driven section resolution.

Pipeline:
Archetype span → Domain scheme → Physics minimal section
→ CulturePolicy scaling → Validator verification

Dependency: SYS-001 (policy axes) must be stable first.

Tasks:
- [ ] Remove fixed section constants
- [ ] Introduce span ranges per archetype
- [ ] Implement dimension solver
- [ ] Log utilization ratios

---

### STR-002 — Physics vs. Construction Culture Separation

Priority: HIGH
Requires: SYS-001
Parallel: STR-001, MAT-001
Universal physics (timeless) is separated from historical construction behavior (epoch-dependent).

Tasks:
- [ ] PhysicalPlausibilityValidator operates on timeless mechanics only
- [ ] ConstructionCulturePolicy defines overdimensioning, redundancy preference, span limits
- [ ] Anachronistic optimization prevented

---

### STR-003 — Roof Construction: Historical Completeness

Priority: MEDIUM
Requires: RES-001 (roof question answered)
Parallel: SYS-002, SYS-003, ENG-001 (independent of policy work)

Goal:
The current roof implementation shows open rafter framing (Sparrenwerk).
Research (RES-001) must determine whether this is historically complete
for the Hallenhaus, and what additional elements are required.

Candidates for investigation:
- Kehlbalken (collar beams): present? at which height? in which epochs?
- Firstpfette (ridge purlin): continuous ridge or rafter-to-rafter?
- Rofen / Pfetten: intermediate purlins on the rafter slope?
- Dachstuhl vs. Sparrendach: which construction type for which region/epoch?

Tasks:
- [ ] Research findings from RES-001 feed into this task
- [ ] Define RoofPolicy parameters based on findings
- [ ] Implement missing roof members as explicit FramePlan members
- [ ] Verify roof is structurally legible in Blender

Dependency: RES-001 (roof question) must be answered first.

---

## Material System

### MAT-001 — MaterialRegistry Completion

Priority: HIGH
Requires: SYS-001
Unlocks: MAT-002
Parallel: STR-001, STR-002
Single material definition drives both structural physics and rendering.
No region/epoch/wealth logic inside Blender builders.

Tasks:
- [ ] Timber classes: oak, beech, pine, spruce
- [ ] Masonry classes: brick historic low/mid/high
- [ ] Stone classes: sandstone weak/strong, granite
- [ ] Mortar classes: lime weak, hydraulic mid
- [ ] `resolve_material(member, ctx, resolved_policy)` is pure and deterministic

---

### MAT-002 — Deterministic Visual Variation

Priority: MEDIUM
Requires: MAT-001
Controlled material diversity without breaking determinism.

Tasks:
- [ ] Palette variation per material
- [ ] Roughness and brightness jitter
- [ ] Seed-driven sampling only

---

## Semantics & Variation

### SEM-001 — Parameter Ranges (Soft / Hard)

Priority: HIGH
Requires: SYS-001
Unlocks: SEM-002, SEM-003
All structural parameters have soft/hard ranges with deviation cost scoring.
No magic constants remain.

Tasks:
- [ ] Replace fixed constants with RangeSoft / RangeHard
- [ ] Implement deviation scoring
- [ ] Integrate into Evaluator

---

### SEM-002 — Semantic Preference Layer (Fuzzy)

Priority: MEDIUM
Requires: SEM-001
Parallel: SEM-003 (can be built in parallel — integration happens at scoring)
Note: Limited impact without SEM-003. Meaningful only once multi-candidate search exists.
Rewrite Risk: LOW (Evaluator-only)

Goal:
Introduce a qualitative intent layer that allows user-friendly inputs such as:
- large house
- wide gates
- steep roof
- intensity modifiers: very, somewhat, barely

All canonical parameters remain metric and unchanged.

Architectural position:
- Lives in the Evaluator only
- Does not modify Domain or Archetype logic
- Does not soften HARD constraints
- Fully deterministic and seed-stable
- Fully reportable in generation output

Concept:

1. IntentPreferences Container
   Optional request-level object containing qualitative labels mapped
   to canonical parameter targets. Empty by default.

2. Fuzzy Membership Derivation
   For numeric parameters: hard_min ≤ soft_min ≤ soft_max ≤ hard_max
   Construct fuzzy terms (small, medium, large) directly from Soft/Hard ranges.
   Optional: Ruspini normalization (Partition of Unity) for stable membership sums.

3. Linguistic Hedges
   Intensity modifiers as deterministic power transforms:
   - very(A):      μ²
   - extremely(A): μ³
   - somewhat(A):  √μ
   - barely(A):    k·μ

4. Score Integration
   Preference contribution added to Evaluator score as additional component.
   No parameter mutation occurs.

Non-goals:
- No fuzzy rule base (no IF–THEN inference system)
- No domain-core changes
- No hard constraint relaxation
- No natural language parsing

Deliverable:
- Membership derivation utility
- Deterministic normalization
- Evaluator hook for preference scoring
- Reporting section for intent diagnostics

Note: SEM-002 requires SEM-003 to have meaningful optimization impact.

---

### SEM-003 — Multi-Candidate Search & Selection

Priority: HIGH (enables SEM-002 usefulness)
Requires: SEM-001, SYS-004 (pipeline interfaces frozen before multi-candidate can be wired in)
Parallel: SEM-002
Rewrite Risk: LOW–MEDIUM (Orchestrator expansion only)

Goal:
Enable deterministic generation of multiple candidates and selection based on:
- Hard constraints
- Soft penalties
- Semantic Preference Score (SEM-002)
- Diversity control

Architectural position:
- Extends Orchestrator and Evaluator only
- Domain remains untouched
- Builder remains emitter-only
- Fully seeded and reproducible

Concept:

1. Candidate Sampling
   Generate N deterministic candidates using seeded sampling within soft ranges.
   No global randomness.

2. Validation
   - HARD issues → reject candidate
   - SOFT issues → penalty applied in scoring

3. Scoring
   Each candidate receives a composite score:
   - plausibility
   - usability
   - semantic preference contribution (SEM-002)
   - soft deviation penalties
   - diversity penalties

4. Diversity Control
   Maintain structural fingerprints (dimensions, pitch, bay counts, opening density).
   Apply similarity penalty to avoid near-duplicates within a settlement context.

5. Selection Strategy
   v0.4.x: Best-of-N deterministic selection
   v0.5.x: Top-K beam search, stage-wise refinement

Why separate from SEM-002:
Without multi-candidate search, semantic preference has limited impact —
intent remains mostly cosmetic, no real optimization space exists.
SEM-003 enables preference to function as an actual objective.

---

## Engineering & Tooling

### ENG-001 — World Mapping Documentation

Priority: MEDIUM
Requires: nothing — can start immediately
Parallel: all other v0.4.x items
Note: Earlier is better. Undocumented coordinate assumptions compound during SYS-002 and SYS-003.

Goal:
The coordinate system and wall-to-world mapping used across all
Blender builders must be explicitly documented and testable.

Today `_house_basis()` and its equivalents in multiple builder modules
contain implicit knowledge about how local wall coordinates map to
Blender world space. This works for one house type. For two types
with different orientations and topologies, undocumented assumptions
become bugs.

Tasks:
- [ ] Document the canonical coordinate system (local → wall-local → world)
- [ ] Extract `_house_basis()` into a shared, tested utility
- [ ] Add unit tests for wall coordinate mapping (N/S/E/W, center_x, halfW)
- [ ] Verify Stadthaus gable-facing orientation is handled without special-casing

---

### ENG-002 — Snapshot Tests + Regression Protection

Priority: MEDIUM
Requires: nothing hard — but most useful once SYS-002 is stable (snapshot captures the refactored state)
Parallel: all other items
Note: Add the golden snapshot for seed=123 early. Every subsequent refactor can then be verified mechanically.

Goal:
Determinism guarantees must be mechanically enforced, not just asserted
in principles. Refactors — especially SYS-002 and SYS-003 — must be
verifiable without manual inspection.

Tasks:
- [ ] Define snapshot format for FramePlan dict (stable, human-readable)
- [ ] Add golden snapshot for Hallenhaus seed=123 (the reference house)
- [ ] CI check: snapshot must not change without explicit update
- [ ] Document snapshot update procedure (when is a change intentional?)

---

> **⊕ CR-3 — Engine Complete**
> STR-001, STR-002, MAT-001, SEM-001, SYS-004, ENG-002 complete.
> Span-driven dimensions. Frozen pipeline. Golden snapshot green.
> Semantic variation, multi-candidate search, and v0.5.0 may begin.

---

### ENG-003 — Naming Refactor Window

Priority: LOW
Requires: all structural intelligence tasks complete, determinism confirmed, no open structural refactors
Note: Last item in v0.4.x by definition. Activation is conditional, not scheduled.
- All structural intelligence tasks complete
- Determinism confirmed
- No open structural refactors

Constraints:
- No functional changes
- Single atomic rename branch
- Determinism unchanged

---

# v0.5.0 — Second House: Fachwerk Stadthaus

## Goal

A Fachwerk Stadthaus emerges deterministically through the same pipeline
that built the Hallenhaus — without structural rewrites.

This is the scalability proof. Two fundamentally different house types,
same engine, same policy system, same builder.

If v0.5.0 requires a structural rewrite anywhere in the pipeline,
that rewrite should have happened in v0.4.x. The Stadthaus is therefore
also a retrospective quality check on everything v0.4.x delivered.

---

## What Makes the Stadthaus Different

The Stadthaus is not a smaller Hallenhaus. It is a different spatial grammar:

**Topology.** Narrow parcel, deep floor plan, gable facing the street.
The load-bearing logic runs across the short axis, not the long axis.
This is a different Archetype, not a StylePolicy variation.

**Vertical.** Multiple storeys are common. Potential jetties (Vorkragung)
on upper floors. The FramePlan schema must support vertical stacking
and floor-level differentiation.

**Interior.** No Längsdiele. Different room hierarchy, staircase logic,
merchant or craft zones. InteriorPlanner must handle a structurally
different program.

**Policy.** Urban context, narrow plot, different wealth curve, later
epochs more likely. `resolve_policy_stack(ctx)` must produce a valid,
distinct policy for this type without special-casing in the planner.

**Construction culture.** Städtisches Fachwerk has different bracing
patterns, different member rhythms, and different opening densities
than rural Hallenhaus construction. CulturePolicy must reflect this.

---

## Definition of Done — v0.5.0

v0.5.0 is complete when:

1. A Stadthaus is generated deterministically through the full pipeline
2. Blender renders the result: correct gable orientation, multi-storey
   structure, urban opening density, plausible roof
3. No structural rewrite was required in the pipeline, planner, or domain
4. `resolve_policy_stack(ctx)` produces a correct, distinct policy
   for the Stadthaus without branching on type inside the stack
5. The Fachwerk domain engine handles both types from the same codebase
6. Determinism confirmed for both house types simultaneously

---

## Research Required Before v0.5.0

The Stadthaus introduces new research questions that must feed into
policy and archetype design before implementation begins:

- Which Stadthaus variants are most representative?
  (Giebelständiges vs. Traufenständiges, single vs. multi-bay)
- When and where did jetties appear, and what drove their adoption?
- How did urban plot constraints shape construction grammar differently
  from rural practice?
- What is the minimal Stadthaus room program, and how does it
  differ structurally from the Hallenhaus?

These questions inform v0.4.x policy axis design.
The Stadthaus must not be started before they are answered.

---

# Vision — Architectural Reserves

These items influence today's design without creating delivery pressure.
They are guardrails, not commitments.
Research findings may promote items from Vision into v0.4.x or later.

---

## VAR-003 — Semantic Preference Layer (Fuzzy)

Qualitative intent inputs ("large house", "steep roof", "very wide gates")
mapped to canonical parameters via fuzzy membership.

Architectural position: Evaluator only. No domain or archetype changes.

Concept:
- IntentPreferences container (optional, empty by default)
- Fuzzy terms derived from Soft/Hard ranges
- Linguistic hedges: very(μ²), extremely(μ³), somewhat(√μ), barely(k·μ)
- Preference score added to Evaluator composite

Non-goals:
- No fuzzy rule base
- No natural language parsing
- No hard constraint relaxation

Note: VAR-003 requires VAR-004 to have meaningful optimization impact.

---

## ARC-001C — EcoMap / ResourceMap

Spatio-temporal resource distribution (oak, spruce, sandstone, clay, ...)
influences material selection via Policy without hardcoding geography into builders.

Core concept:
- ResourceTrace = (Polygon × TimeInterval × fuzzy core/halo)
- Output: ranked material candidates with abundance/confidence scores
- Policy layer converts to material bias only

Principle: `resolve_material(...)` remains the single material resolution point.

Long-term potential:
- CultureMap + EcoMap + TradeMap combined
- Regionally plausible timber species
- Historically consistent stone/brick distribution

---

## ARC-003 — Plot & Envelope Foundation

Polygon-based plot system. Buildings placed within real plot boundaries.

Tasks (future):
- Plot dataclass (polygon + terrain plane)
- Footprint containment validator
- Terrain plane MVP

---

## ARC-004 — 3D Envelope

Constraint-based multi-level modeling.
Vertical rules, max height, 3D fit validation.

---

## INT-002 — InteriorPlanner Full Iteration Model

Multi-proposal interior planning with conflict detection and alternative scoring.
Depends on pipeline interface freeze (ARC-002) and research into
historical room programs.

---

## VAR-002 — Settlement-Level Diversity

Prevent cloned houses at settlement scale.
Diversity scoring, repetition penalties, structural fingerprinting.

---

## Future Extensions (Frozen)

- Climate load models
- Roof pitch snow reduction
- Moisture and fire resistance modeling
- Advanced structural simulation
- TradeMap (material availability by trade routes)

---

# Guiding Principles

Physics is universal.
Construction culture is epoch-dependent.
Archetypes define topology, not dimensions.
Domains define structural logic, not style.
Members are canonical structural truth.
Policies are the single source of parameter truth.
Variation must be deterministic.
No anachronistic optimization.
Research informs architecture. Architecture does not precede understanding.
The project is allowed to be incomplete. It is not allowed to be inconsistent.
