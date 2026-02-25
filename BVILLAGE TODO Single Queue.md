# BVILLAGE – TODO (Single Queue)
Status: Active
Rule: One entry per change. Keep it short, actionable, testable.

Legend:
- [P0] must-do now (blocks architecture)
- [P1] next important
- [P2] later / nice to have

------------------------------------------------------------
## P0 – Builder becomes FramePlan-driven (critical)
------------------------------------------------------------

- [ ] [P0] Require FramePlan artifact in fachwerk builder
  - Load: notes["domains"]["fachwerk"]["frameplan"] (via get_domain_artifact)
  - If missing: LOG.error + abort build (no fallback build)
  - Acceptance: build_frame refuses to run without fp

- [ ] [P0] Refactor posts: use fp["axes_u"][wall]["all"] (not axis_x)
  - N/S: u->x, y=±halfW ; E/W: u->y, x=±halfL
  - Post height: z0 -> z_plate (phase-1 target)
  - Acceptance: posts exist at opening edges u0/u1 and at secondary axes
  - Notes: keep deterministic naming/order (wall order N,S,E,W)

- [ ] [P0] Remove structural dependence on house["axis_x"]/["axis_y"]
  - house dict may keep only: profiles, debug flags, meta, etc.
  - Acceptance: structural placement does not read axis_x/axis_y

------------------------------------------------------------
## P1 – Stability & correctness
------------------------------------------------------------

- [ ] [P1] Clear behavior: FORCE_CLEAR_PREVIOUS default False
  - Runner controls clear_previous
  - Acceptance: builder respects runner flag unless explicitly overridden

- [ ] [P1] Roof API unify
  - Make roof build depend on fp["dims"] + explicit params only
  - Acceptance: build_frame calls roof with one stable signature; no mismatched kwargs

- [ ] [P1] Add REPRO case: “opening axes enforce posts”
  - Seed + dims + expected: posts at u0/u1 for gate and window
  
------------------------------------------------------------
## P1 – Naming & Structural Clarity
------------------------------------------------------------

- [ ] [P1] Introduce explicit naming convention for modules & functions
  - Replace generic names like validate.py / integrity.py
  - Use role-based naming: <role>_<aspect>.py
  - Examples:
      - frameplan_contract.py
      - planner_quality.py
      - builder_integrity.py
  - Acceptance:
      - No new generic validate/check modules
      - One documented naming pattern in ARCHITECTURE
      - Transitional aliases allowed (logged as deprecation)

------------------------------------------------------------
## P2 – Next constructive steps
------------------------------------------------------------

- [ ] [P2] Build horizontal rails from fp["axes_z"] (segmented by openings)
- [ ] [P2] Opening frames: jambs + lintel + sill (structural, no cuts)
- [ ] [P2] Roof depends on frame policy (historic variants)
- [ ] [P2] Materials / UV / join strategy (performance)

## TAX-001  Architectural Taxonomy Integration
Status: planned
Priority: high
Version Target: v0.3.0+

Goal:
Integrate historically grounded architectural taxonomy into
TypeProvider system.

Tasks:
- [ ] Formalize Topology Signature schema
- [ ] Map Fachwerk topologies to HouseTypeProviders
- [ ] Define Domain ↔ Archetype contract
- [ ] Implement StylePolicy parameter binding
- [ ] Add Taxonomy ID system (e.g. FW-LH-ND-16-M)

Rationale:
Ensure long-term historical consistency and scalability
across 50+ house types and multi-epoch simulation.

# ------------------------------------------------------------
# v0.2.0 – Typed Order & Offer Interface (DEFERRED)
# Activation: after Langhaus stabilization
# Purpose: Scalable type-specific ordering + city-builder readiness
# ------------------------------------------------------------

## Context

Current focus:  
Langhaus must be finalized as stable, fully FramePlan-driven construct.

This block MUST NOT be implemented before:

- Builder is fully FramePlan-driven (no structural axis_x dependence)
- Langhaus generation is deterministic and stable
- A reproducible Langhaus reference case exists

---

## P0 – Order Foundation (Type-Level, no City logic yet)

### Provider Contract

- [ ] Extend provider API:
  - `generate(ctx, order=None)`
  - Backwards compatible (`order=None` keeps current behavior)
  - Acceptance: existing Langhaus works unchanged

- [ ] Introduce `order_spec()`
  - Returns JSON-like dict
  - Must include:
    - `spec_id`
    - `version`
    - `fields`
  - Acceptance: CLI can print spec without generating house

- [ ] Introduce `presets(ctx)`
  - Returns list of `{preset_id, order}`
  - Deterministic
  - Acceptance: at least 3 presets for Langhaus

---

### Validation

- [ ] Implement generic `validate_order(spec, order)`
  - HARD error on:
    - unknown key
    - missing required field
    - enum/type mismatch
    - range violation
  - No silent fallback
  - Acceptance: invalid order fails before `generate()`

---

### Provenance

- [ ] Store order provenance in notes:
  - `structure.notes["domains"]["order"]`
  - Must include:
    - `spec_id`
    - `preset_id` (if used)
    - `order`
  - Acceptance: report displays order provenance

---

## P1 – Footprint & Offer Preparation (City-Ready Layer)

### Footprint Extension

- [ ] Extend `Footprint` with optional `outline`
  - If `outline=None` → rectangular footprint
  - If provided → polygon is authoritative
  - Acceptance: existing rectangular houses unaffected

---

### Offer Data Shape

- [ ] Define generic `Offer` structure:
  - `{ order, spec_id, metrics, tags }`
  - Metrics minimum:
    - footprint (bbox or outline)
    - height (eave/total)
  - Acceptance: Langhaus can emit Offer via preset

---

### CLI / Reporting

- [ ] Add `describe_type(type_id)`
  - Prints:
    - short description
    - presets
    - parameters
  - No Blender dependency
  - Acceptance: type can be described without generating a house

---

## Explicit Non-Goals (for v0.2.0)

- No full city-builder implementation
- No automatic sampling engine
- No optimization solver
- No feature ontology system

This version introduces interfaces only.

------------------------------------------------------------
## Bug Log (when something breaks)
------------------------------------------------------------

Template:
- ID:
- Date:
- Seed/Params:
- Symptom:
- Expected:
- Files:
- Notes:
