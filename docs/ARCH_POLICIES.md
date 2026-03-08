# BVILLAGE – Architectural Policy Axes

---
tier: 2
authority: REFERENCE
change-frequency: on-feature
change-rule: New axes added as optional patch slots only. No existing archetype, domain, or plugin may require modification. See expansion rules below.
referenced-by: DEV_ROADMAP.md, DOCS_INDEX.md
references: SYS_PRINCIPLES.md, SYS_CONCEPTS.md §2
status: axes defined and stable; axis contents under active research
---

## Purpose

The world does not offer a finite list of building types. It offers determinants — forces that shape buildings across time, geography, culture, and use. BVILLAGE models the determinants, not an exhaustive catalogue of results.

This document defines the policy axes through which those determinants enter the system. Each axis carries a specific kind of knowledge. Together they produce buildings that are historically plausible, regionally distinct, and structurally coherent — without encoding that knowledge in the Topology Planner, the Frame Producer, or the domain.

The axes defined here are stable. Their contents — the specific parameter values, ranges, and cultural data they carry — grow with research and are not fully specified here.

---

## 1. What drives building form

Before mapping axes to system layers, it helps to understand what actually shapes a building. Seven forces dominate.

**Structural system.** The fundamental question is how the building stands. Timber framing, load-bearing masonry, log construction, rammed earth, and steel frame each impose a different structural grammar — different members, different load paths, different constraints on spans and openings. This is the deepest determinant. It cannot be changed by style.

**Spatial organization.** The second question is how the building is arranged. A longhouse organizes space linearly along a central axis. A courtyard house organizes it around an enclosed interior. A tower house stacks it vertically. These organizational families persist across regions and epochs; what changes is how they are dressed.

**Function and use.** What the building does shapes its program fundamentally. Agricultural buildings integrate animal quarters, storage, and processing spaces with living areas. Trading buildings need street-facing commercial frontage. Workshop buildings integrate production and residence. A barn and a house of the same archetype are topologically identical but functionally disjoint — function is a first-class axis, not a style modifier.

**Household model.** Who occupies the building, and how, shapes its internal logic. A nuclear family, an extended multi-generational household, a craft workshop with live-in workers, a merchant compound with separate guest quarters — each produces a different room graph, different privacy requirements, different patterns of access and separation.

**Climate and environment.** Snow loads, wind exposure, rainfall, flooding risk, and solar orientation all leave marks on building form — roof pitch, overhang depth, opening size and placement, material choice, and sometimes footprint orientation.

**Plot and settlement fabric.** A narrow urban parcel produces a different building than a wide rural farmstead, even with the same archetype and domain. Corner lots, street edges, slope, and the density of surrounding structures all impose constraints and opportunities.

**Epoch.** Time changes what is possible and what is normal. Available materials, joinery techniques, glass production, and structural understanding all evolved. So did spatial conventions, symmetry preferences, and what counted as adequate shelter or appropriate display of wealth.

---

## 2. Primary axes — identity-defining

Primary axes define what a building fundamentally is. Changing a primary axis produces a categorically different building, not a variant.

### 2.1 Construction Domain

The construction domain defines how the building stands — its structural grammar, load paths, and member generation logic. Each domain is implemented by one or more Frame Producer plugins.

Current domain families (non-exhaustive):

- **timber_frame** — posts, rails, braces; infill is secondary and non-structural
- **log / blockbau** — stacked horizontal members; walls are structural
- **post_in_ground** — primary posts carry roof directly; walls are light and secondary
- **masonry_loadbearing** — walls are structural; spans and openings behave fundamentally differently
- **earth_architecture** — rammed earth or adobe; mass and moisture drive constraints
- **hybrid** — combinations, transitional forms, or systems that borrow from multiple grammars

Domain switching is not a style operation. If a regional variation requires a different structural grammar — different load paths, different member types, different validation logic — it is a new domain or a new CulturePolicy branch. It is never a StylePolicy variant.

### 2.2 Archetype

The archetype defines how the building is organized — its spatial family, room hierarchy, circulation logic, and opening demands. Each archetype is implemented by a Topology Planner plugin.

Current archetype families (non-exhaustive):

- **linear / longhouse** — space organized along a single axis; single or double-loaded
- **hall-based** — central hall as organizing element; variants by aisle count and use
- **rowhouse / townhouse** — narrow urban parcel; deep plan; gable or eaves to street
- **courtyard / hofhaus** — space organized around an enclosed interior court
- **compound / cluster** — multiple structures forming a household unit
- **tower** — vertical stacking; often defensive
- **collective courtyard** — inward-facing, restricted access; communal or fortified

Archetype selection is explicit and stable. Style modulates within an archetype; it does not replace it. If a discovered building type has a fundamentally different spatial organization, it is a new archetype or a TopologyModifier applied to an existing one — not a style variant.

---

## 3. Secondary axes — planning layer

Secondary axes shape how a building is built within the identity established by the primary axes. They affect the Topology Planner and Frame Producer directly and produce measurable differences in geometry.

### 3.1 TopologyModifier

Modifies the footprint form of an archetype without changing its organizational family.

- rectangle (default — no modification)
- L-form (two wings at a corner)
- T-form (central block with lateral wing)
- U-form (three sides of a courtyard)
- additive wings and incremental extensions

TopologyModifier is reactive to plot constraints. A courtyard archetype on a narrow urban parcel may apply a U-form modifier to fit the available depth. The archetype remains a courtyard house; its footprint adapts.

### 3.2 VerticalPolicy

Controls how the building develops vertically.

- storey count
- attic use and height
- cantilevered upper floors (where culturally and structurally permitted)

### 3.3 RoofPolicy

Controls the roof system independently of the structural frame below. The Roof Producer implements the selected roof type within the constraints the Frame Producer has established.

- roof type (gable, hip, half-hip, shed, mansard, and others)
- pitch range
- overhang depth
- eaves height

Roof type is not always determined by domain or archetype alone. The same Hallenhaus archetype appears with gable roofs in some regions and half-hip roofs in others; the difference is cultural and climatic, expressed through RoofPolicy. The construction grammar constrains which roof types are structurally possible — RoofPolicy selects within that space.

### 3.4 OpeningsPolicy

Controls the semantic opening program — what openings the building demands and where.

- entry types and counts (main, service, barn gate)
- window count and size bands
- privacy-to-light bias
- defensive bias (reduced ground-floor openings)

OpeningsPolicy expresses intent. The domain and Topology Planner translate that intent into specific member configurations that frame the openings.

### 3.5 FunctionPolicy

Controls building use and social type. This is a first-class axis — not a modifier. A barn and a residential longhouse of the same archetype are topologically identical but functionally disjoint. Without an explicit function axis, the system cannot distinguish them.

- `building_use` — `RESIDENTIAL | AGRICULTURAL | STORAGE | CIVIC | RELIGIOUS | MIXED`
- `representation_direction` — `STREET_FACING | COURTYARD_FACING | NONE`
- `livestock_integration` — boolean; true for buildings integrating humans and animals under one roof
- `storage_ratio` — 0.0–1.0; proportion of total volume allocated to storage
- `commercial_frontage` — boolean; true for buildings with street-facing trade use

Default: `building_use = RESIDENTIAL`, all other fields neutral.

FunctionPolicy is a mandatory field in every `BuildingOrder`. See SYS_CONTRACT §5.7.

### 3.6 Growth Pattern

Controls how the building may expand over time or how its massing is composed.

- bay addition (linear extension along the main axis)
- wing addition (L- and U-form development)
- courtyard closure (progressive enclosure of an open court)
- modular units arranged around a court or cluster

---

## 4. Tertiary axes — contextual modulation

Tertiary axes modulate parameters within the space established by the primary and secondary axes. They never redefine topology and never switch domain.

### 4.1 StylePolicy

StylePolicy carries the intersection of region, epoch, wealth, and settlement type. It is the broadest modulator — it touches nearly every parameter range in the system — but it operates entirely within the boundaries set by domain and archetype.

StylePolicy adjusts: material selection within available options, parameter ranges for dimensions and proportions, ornament density, roof pitch tendencies, window proportions, and finish preferences.

StylePolicy must not switch construction domains. It must not replace archetypes. It must not encode functional differences — those belong in FunctionPolicy. If a regional variation requires a different structural grammar, that is a domain or CulturePolicy question. StylePolicy answers: given this structural grammar, this spatial organization, and this function, how would builders in this place and time have expressed it?

### 4.2 CulturePolicy

CulturePolicy carries domain-specific construction culture — the tacit knowledge of how builders in a given tradition actually worked within their structural system.

This is distinct from StylePolicy. StylePolicy operates across domains; CulturePolicy is domain-specific. A CulturePolicy for timber framing carries: typical member spacing, preferred bracing patterns, infill logic, redundancy preferences, how close to physical limits builders operated, and what spans were considered normal or excessive in a given tradition.

CulturePolicy does not change physics. It modulates how the domain exercises its structural grammar within the bounds that physics permits.

### 4.3 ConstraintsPolicy

Hard and soft constraints with deviation cost weights. Hard constraints block generation. Soft constraints impose a scored penalty that the Appraiser weighs during candidate selection.

### 4.4 NoisePolicy

Deterministic micro-variation within allowed parameter bands. Its sole purpose is to prevent visually identical buildings within a settlement. It produces no structural variation — only controlled surface-level diversity within constraints already established by all other axes.

---

## 5. The complete policy stack

Policies resolve in this order, from generic to specific. Later layers override earlier ones.

| Position | Policy | Scope |
|---|---|---|
| 1 | `BaseTypePolicy` | Archetype defaults |
| 2 | `TopologyModifierPolicy` | Footprint modification |
| 3 | `VerticalPolicy` | Storey count, cantilevers |
| 4 | `RoofPolicy` | Roof type, pitch, eaves |
| 5 | `OpeningsPolicy` | Opening program |
| 6 | `FunctionPolicy` | Building use, social type |
| 7 | `StylePolicy` | Region × epoch × wealth × settlement |
| 8 | `CulturePolicy` | Domain construction culture |
| 9 | `ConstraintsPolicy` | Hard and soft constraint weights |
| 10 | `NoisePolicy` | Deterministic micro-variation |

No layer may operate outside its defined scope. A layer that contributes nothing is empty. An empty layer changes nothing.

---

## 6. Boundary decisions — where to classify a variation

The hardest design decisions involve classifying a newly discovered building variation. The following questions guide that decision.

**Does it change load paths or structural grammar?**
If a variation requires different member types, different load paths, or different structural validation — it is a new construction domain or a new CulturePolicy branch. It is not a StylePolicy variant, regardless of how regionally specific it appears.

**Does it change spatial organization?**
If a variation has a fundamentally different room hierarchy, circulation logic, or zone arrangement — it is a new archetype or a TopologyModifier applied to an existing one. It is not a StylePolicy variant.

**Does it change building use or social type?**
If a variation serves a fundamentally different function — barn vs. house, warehouse vs. merchant residence — that is FunctionPolicy. It is not a StylePolicy variant and it is not a new archetype, as long as the spatial organization is equivalent.

**Does it change storey count, roof type, or opening program?**
These are secondary axes — VerticalPolicy, RoofPolicy, OpeningsPolicy. They modulate geometry significantly but do not redefine spatial organization or structural grammar.

**Is it region, epoch, or wealth modulation within the same structure, organization, and function?**
That is StylePolicy.

**Is it surface-level diversity within otherwise identical parameters?**
That is NoisePolicy.

When in doubt, classify at the higher level. Promoting a variation from Style to Domain is a clean architectural decision. Demoting it later — discovering that what was encoded as Style actually requires structural grammar changes — causes rewrites.

---

## 7. Expansion rules

New axes enter the system as optional patch slots. The default for any new slot is neutral — no effect on existing behavior. Adding a new axis must not require modification of any existing archetype, domain, Topology Planner, or Frame Producer plugin.

New required global fields are prohibited without a schema version increment. If a new axis needs to be understood by all archetypes to function, the design is wrong — the axis should be expressible as an optional delta, or the schema version must be bumped explicitly.

When research reveals a variation that changes structural grammar, it enters as a new domain or CulturePolicy branch — never as a style extension. When research reveals a variation that changes plan topology, it enters as a new archetype or TopologyModifier — never as a style extension. When research reveals a variation that changes building use or social type, it enters as a FunctionPolicy variant — never as a new archetype or a style extension. Encoding structural, topological, or functional differences at the wrong level is the primary source of long-term architectural debt in this system.
