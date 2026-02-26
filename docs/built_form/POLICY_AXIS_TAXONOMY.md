# POLICY AXIS TAXONOMY (Global, time+space) — BVILLAGE Anchor

Purpose
- Capture the broad, deep "determinant axes" of vernacular housing systems.
- Provide a stable policy-layer decomposition to avoid later rewrites.
- Balanced goals: historical accuracy, combinatoric variety, system stability.

Core idea
- The world does not offer a finite list of "all house types".
- It offers families + determinants (axes) that generate types and variants.
- BVILLAGE models the determinants, not an exhaustive list.

============================================================
1. DETERMINANT AXES (WHAT DRIVES HOUSE FORM)
============================================================

1.1 ConstructionDomain (Structural System) — PRIMARY
Defines load paths and construction grammar.

Examples (non-exhaustive families):
- timber_frame / fachwerk (posts+rails+braces; infill secondary)
- blockbau / log (stacked logs/planks; walls are structural)
- post_in_ground / early post-frame (primary posts carry roof; walls light)
- masonry_loadbearing (walls structural; spans/openings behave differently)
- earth_architecture (rammed earth / adobe; mass + moisture constraints)
- hybrid systems (e.g. frame + log combinations, transitional forms)

Policy implication:
- Different domains require different member generation and validation.
- Domain switching is NOT a style operation.

1.2 Archetype (Plan Topology Family) — PRIMARY
Defines organizational family independent of style.

Families:
- linear / longhouse family
- hall-based family (central hall variants)
- rowhouse / townhouse family (urban parcels)
- courtyard / hofhaus family (inward-facing)
- compound / cluster family (multi-building household units)
- towerhouse / vertical defensive family
- collective courtyard/fortified family (restricted access, inward life)

Policy implication:
- Archetype selection is explicit and stable.
- Style modulates within archetype; does not replace it.

1.3 Household Model (Social Unit) — STRONG MODULATOR
- nuclear family
- extended family / multi-generation
- multi-family collective
- hierarchy / segregation needs (privacy, gendered zones, purity rules)

Policy implication:
- strongly affects zoning/intended room graph/openings strategy.

1.4 Economy & Functional Coupling — STRONG MODULATOR
- agriculture vs herding vs trade vs craft
- storage intensity (granaries, lofts)
- co-habitation with animals (wohnstall coupling)
- workshop + living integration

Policy implication:
- affects zone set and growth pattern.

1.5 Environment / Climate — STRONG MODULATOR
- snow, wind, rain, temperature
- moisture / flooding risk
- solar orientation preferences

Policy implication:
- modulates roof pitch/overhang, openings, materials, sometimes footprint.

1.6 Plot / Terrain / Settlement Fabric — STRONG MODULATOR
- parcel width/depth
- street edge, corner lots
- slope/hillside building
- rural vs village vs town

Policy implication:
- drives footprint modifiers (L/T/U), entry placement, facade orientation.

1.7 Time (Epoch) — GLOBAL MODULATOR
Epoch modifies many parameters:
- available technology/materials (glass, joinery)
- typical story count
- regularity/symmetry preferences
- normative spatial arrangements

Policy implication:
- epoch is expressed via StylePolicy + CulturePolicy, not by rewriting archetypes.

============================================================
2. GEOMETRIC / PLANNING AXES (WHAT THE GENERATOR BUILDS)
============================================================

2.1 TopologyModifier (Footprint Form)
- rectangle
- L-form (two wings)
- T-form
- U-form / courtyard closure
- additive wings / incremental extensions

2.2 VerticalModel
- stories count (1, 1½, 2+)
- attic use
- jetties/overhang floors (where culturally allowed)

2.3 RoofSystem
- roof type (gable, hip, half-hip, shed, etc.)
- pitch ranges
- overhang ranges
- eaves height ranges

2.4 OpeningsStrategy (semantic)
- entry types and counts (main/service)
- window counts/size bands
- privacy vs light bias
- defensive bias (few openings ground floor)

2.5 Growth Pattern
- bay-addition (linear)
- wing-addition (L/U forms)
- courtyard closure
- modular units around court/cluster

============================================================
3. POLICY LAYER MAPPING (BVILLAGE IMPLEMENTATION)
============================================================

3.1 Selection Layer (IDs only)
- house_archetype_id
- construction_domain_id
- ctx.region, ctx.epoch_band, ctx.wealth, ctx.settlement_type
- optional: household_model_id, economy_profile_id, climate_profile_id, plot_profile_id

3.2 BaseTypePolicy (Archetype defaults)
- provides canonical parameter tree defaults + allowed envelopes
- no region/epoch specifics

3.3 TopologyModifierPolicy
- footprint form modifications (L/T/U), wing ratios, placement rules
- optional; defaults to "no modifier"

3.4 VerticalPolicy
- stories/attic/jetty preferences and constraints

3.5 RoofPolicy
- roof type + pitch/overhang/eaves ranges

3.6 OpeningsPolicy
- semantic opening demands (counts, preferred walls, z-bands)

3.7 StylePolicy (Region × Epoch × Wealth × Settlement)
- modifies ranges/bias across nearly all planning parameters
- MUST NOT switch construction domains or archetypes

3.8 CulturePolicy (Domain-specific construction culture)
- domain grammar: member spacing, bracing rules, infill logic, opening framing roles
- derived from ctx, but lives domain-specific
- feeds domain-core member generation

3.9 ConstraintsPolicy (Hard/Soft + cost weights)
- defines deviation cost model and feasibility checks
- supports late addition of new axes without refactoring planners

3.10 NoisePolicy (Deterministic micro-variation)
- small perturbations within allowed bands
- used to avoid cloned houses in settlements

============================================================
4. EXPANSION RULES (NO REWRITES)
============================================================

4.1 Add new axis as optional patch slot.
- default is empty patch
- resolver composes it if available

4.2 Never add global required fields without schema bump.
- avoid "everyone must understand subtype"

4.3 When a discovered variation changes structural grammar:
- it is a new ConstructionDomain or new CulturePolicy branch, not Style

4.4 When a discovered variation changes plan family:
- it is a new Archetype or TopologyModifier, not Style

============================================================
5. CHECKLIST (DESIGN REVIEW)
============================================================

Before implementing a new "variant":
- Does it change load paths / construction grammar?
  -> Domain/Culture
- Does it change plan family / topology?
  -> Archetype or TopologyModifier
- Does it change story/roof/openings preferences?
  -> Vertical/Roof/Openings
- Is it region/epoch/wealth modulation within same archetype/domain?
  -> Style
- Is it just micro variety (jitter within constraints)?
  -> Noise

End of document.
