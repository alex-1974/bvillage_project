# BVILLAGE – System Concepts

---
tier: 1
authority: CANONICAL
change-frequency: low
change-rule: Change only when the conceptual model changes. Implementation detail does not belong here.
referenced-by: SYS_CONTRACT.md, ARCH_POLICIES.md, ARCH_TAXONOMY.md, ARCH_MATERIALS.md
references: SYS_PRINCIPLES.md
---

This document describes the conceptual model of BVILLAGE — what the system is, how it thinks, and how its parts work together. It assumes the principles in SYS_PRINCIPLES.md and explains how they translate into a concrete system model.

The current implementation covers medieval central European timber framing. The examples reflect that starting point. The model is not limited to it.

---

## 1. The three axes

Every building in BVILLAGE is defined along three primary axes. They are independent of one another and answer different questions.

**Construction domain** answers: how does the building stand? It defines the structural grammar — which members are generated, how loads flow, which joinery or bonding types are possible. Timber frame, log construction, masonry, rammed earth, and steel frame are different domains. Each generates different members, has different validation rules, different material constraints. Switching domain is not a style operation — it is a structural break.

**Topological archetype** answers: how is the building organized? It defines spatial logic — zones, circulation, opening requirements, geometric intent. Two buildings with the same construction domain but different spatial organization are different archetypes. A longhouse and a courtyard house may both be timber-framed — they are not the same archetype. Conversely, the same archetype in two different regions remains the same archetype; what changes is the policy that shapes it.

**Style and context policy** answers: in what context does the building stand? It modulates — region, epoch, wealth, urban or rural setting, climate, function. It adjusts parameter ranges, material selection, roof pitches, window densities, ornament levels. It does not change topology. It does not switch domain.

These three axes are orthogonal. Knowledge belonging to one axis must never migrate to another.

---

## 2. The policy system

Policies are the mechanism through which the system scales. Without them, every new combination of region, epoch, culture, and type would have to be encoded in the planner — making the system unmanageable by the third or fourth extension. With policies, every new historical or cultural insight enters as a new configuration, without touching the core.

The same engine that generates a fourteenth-century north German Hallenhaus can generate a seventeenth-century Anatolian courtyard house — different domains, different archetypes, different policies, same pipeline.

### What policies are

Policies are parameter packages that the planner receives from outside. They do not tell the planner how to plan — they tell it with which values to plan. The planner receives a resolved policy. It does not ask where it came from.

Each policy layer is a delta — a set of overrides on a canonical parameter tree. Layers that contribute nothing are empty. Empty layers change nothing.

### The policy stack

Policies resolve in a defined stack, from generic to specific:

1. **BaseTypePolicy** — the archetype's defaults. What holds when no context is known?
2. **TopologyModifierPolicy** — optional footprint modifications: L-form, T-form, U-form.
3. **VerticalPolicy** — storey count, attic use, cantilevered floors.
4. **RoofPolicy** — roof type, pitch ranges, eaves heights.
5. **OpeningsPolicy** — opening demands, light and privacy preferences.
6. **FunctionPolicy** — building use and social type: residential, agricultural, storage, civic, religious. Controls zone program, opening character, representation direction, livestock integration. Default: residential.
7. **StylePolicy** — region × epoch × wealth × settlement type.
8. **CulturePolicy** — domain-specific construction culture: member spacing, structural grammar, infill logic.
9. **ConstraintsPolicy** — hard and soft constraints with deviation cost weights.
10. **NoisePolicy** — deterministic micro-variation within allowed bands.

Later layers can override earlier ones. No layer may operate outside its domain of responsibility.

### What policies may not do

StylePolicy may not switch construction domain and may not replace an archetype. It modulates — it does not redefine. If a regional variation requires a different structural grammar, that is a new domain or a new CulturePolicy branch, not a StylePolicy variant.

CulturePolicy and domain do not read region and epoch directly. They consume already-resolved policy data. What "northern Germany, sixteenth century" means has already been processed by StylePolicy before the domain sees it.

### Expansion rule

New axes enter as optional patch slots. The default is neutral — no effect. Existing archetypes and domains require no modification when a new axis is added. If adding a new axis would require changes to existing code, that is a design failure, not a feature.

---

## 3. The generation pipeline

A building emerges through an ordered pipeline of roles. Each role has a defined responsibility and a defined boundary.

The pipeline follows a construction site metaphor. The roles map directly onto historical building practice — not as decoration, but because the division of labour on a medieval building site reflects a genuinely sound separation of concerns.

---

### Commissioner

The Commissioner initiates construction. It decides which building is placed where, assembles the raw context — archetype ID, world seed, settlement seed, house salt, plot constraints — and resolves the full policy stack into a `ResolvedPolicy`. It produces a `BuildingOrder` and hands it to the Foreman.

The Commissioner makes no constructive decisions. It does not know how a building stands or how it is organized. It knows what is wanted and where.

---

### Foreman

The Foreman coordinates the construction site. It receives the `BuildingOrder` with its `ResolvedPolicy`, consults the plugin registry to determine which specialists are needed, and dispatches them in order. It resolves conflicts between specialists when their outputs are incompatible — within the bounds of the constraints already established by the policy stack.

The Foreman does not plan topology. It does not generate members. It does not evaluate physics. It knows the interfaces of all specialists and the registry that maps archetypes to implementations. It knows nothing about how any specialist does its work.

---

### Topology Planner

The Topology Planner translates the `BuildingOrder` into a spatial plan: axis grid, wall definitions, zones, opening demands. It generates no structural members. It knows how a building type is spatially organized — not how it structurally stands.

The Topology Planner is domain-aware in one sense only: it must produce a `SemanticPlan` that the domain's frame producer can consume. It does not reach into domain logic.

Each topological family — longhouse, townhouse, courtyard, cruck, aisled — has its own Topology Planner implementation. Multiple archetype IDs may share a single implementation when their spatial logic is equivalent.

---

### Frame Producer

The Frame Producer translates the `SemanticPlan` into constructive truth. It generates the `FramePlan` with explicit members. This is where structural reality is created.

The Frame Producer is domain-specific and construction-grammar-specific. One implementation per construction grammar per domain. In timber framing, the current grammars are:

- **Box Frame** — full-height posts carrying roof load directly; primary unit is the bent
- **Storey Frame** — stacked autonomous floor units; primary unit is the storey frame
- **Cruck Frame** — curved blade pairs forming the primary structure; roof and wall unified
- **Aisled Frame** — internal arcade rows defining nave and aisles; primary unit is the arcade
- **Wall Grid Frame** — regular post-and-rail facade grid; primary unit is the wall surface

Core knows only the `IFrameProducer` interface — not the names or implementations of any Frame Producer. Domain plugins register their implementations against that interface.

---

### Roof Producer

The Roof Producer builds the roof. It receives the `FramePlan` and the resolved `RoofPolicy` and produces a `RoofPlan` with explicit roof members.

The Roof Producer is domain-specific. Multiple roof types may exist within a single domain — gable, hip, half-hip, shed, mansard — and the construction grammar of the wall structure constrains which roof types are structurally possible. A Cruck frame implies a specific roof logic; a Storey Frame allows more variation. The `RoofPolicy` selects within the possible space; the Roof Producer implements the construction.

Core knows only the `IRoofProducer` interface.

---

### Joiner

The Joiner resolves interior spatial organization: partitions, hearth or furnace placement, interior openings, furniture zones. It communicates with the Topology Planner through opening demands but never touches the `FramePlan` or `RoofPlan` directly. All exterior structural consequences of interior decisions pass through the Topology Planner — never through direct plan mutation.

Core knows only the `IJoiner` interface.

---

### Inspector

The Inspector checks universal physics: would this structure hold? It operates on timeless mechanical principles — bending stiffness, slenderness, bearing, compression — independent of epoch, region, or construction culture. It returns `Issue` objects. It mutates nothing.

The Inspector lives in `core/`. It is not domain-specific. It receives abstracted structural data, not raw `FramePlan` members. The translation from `FramePlan` to the Inspector's input format is the domain's responsibility.

The Inspector checks whether the result holds. `CulturePolicy` determines what gets built in the first place — see §5.

---

### Appraiser

The Appraiser scores candidates and selects. Multiple `FramePlan` candidates may be generated from the same `BuildingOrder` with different noise seeds or policy variations. The Appraiser evaluates them against the constraint weights defined in `ConstraintsPolicy` and selects the best result. It changes no geometry and repairs no structure.

Core knows only the `IAppraiser` interface.

---

### Renderer

The Renderer receives a complete `FramePlan` and `RoofPlan` and emits geometry. It computes nothing, closes no gaps, makes no structural decisions. It is an emitter — precise, deterministic, without its own intelligence about the building. It builds what is in the plans. What is not in the plans does not exist.

---

## 4. Interface contracts and the plugin boundary

Core defines interfaces, not implementations. Every role above the Foreman level is expressed as a Python `Protocol` in `core/`. Plugins implement these protocols under domain-specific names.

The Foreman dispatches by interface. It does not import concrete implementations. The plugin registry maps `ArchetypeBinding` entries — `(archetype_id, type_family, domain, construction_grammar)` — to the correct interface implementations at runtime.

Adding a new construction system requires no changes to Core, no changes to the Foreman, and no changes to any existing plugin. A new plugin registers its `ArchetypeBinding` entries and implements the required interfaces. The pipeline picks it up automatically.

Removing a plugin is equally clean. Its archetype IDs are no longer registered. The system raises a structured error if those IDs are requested — no silent fallback, no invented geometry.

---

## 5. Structural truth and the members model

The `FramePlan` contains explicit members: discrete, named, positioned, role-assigned building elements. In a timber-framed building these are posts, rails, braces, and infill cells. In a masonry building they are courses, lintels, and piers. The abstraction is the same; the vocabulary differs by domain.

Axes (`axes_u`, `axes_z`) are planning metadata. They help the Frame Producer place members. They are not geometry. The Renderer sees axes as reference information — it builds members.

This distinction is absolute. A Renderer that derives elements from axes instead of reading the members list violates the contract — even if the result looks identical by coincidence. The violation is not in the output, it is in the mechanism.

---

## 6. Physics and construction culture

The system separates two kinds of structural knowledge that are often conflated.

**Universal physics** always applies. Bending stiffness, slenderness, bearing, compression — these laws know no epoch and no culture. The Inspector checks them.

**Construction culture** is historical and regional. How close to the physical limit did builders of a given time and place actually operate? How much did they overdimension? Which spans were common in their tradition, which were not? What did their available tools and joinery techniques enable or prevent? The `CulturePolicy` answers these questions.

Without this separation, the system produces anachronistically optimized buildings — structures that pass physics but are historically impossible. A medieval carpenter, a Roman engineer, and a nineteenth-century builder all operated within the same physics. They produced radically different structures because they worked within different cultural and technical constraints.

---

## 7. Materials

Materials serve two independent roles in the system. These roles must not be mixed.

As a **physical foundation**, materials provide the mechanical parameters — modulus, density, allowable stresses — for the Inspector and the Frame Producer.

As a **visual basis**, materials provide color palettes, roughness values, and deterministic variation parameters for the Renderer.

Physical values must not be changed for visual reasons. Visual values must not be changed for physical reasons. Both roles are linked through the same material identifier — the registry is the single source of truth for both.

---

## 8. Determinism

Determinism is not a technical property — it is a functional requirement. A non-deterministic system cannot be debugged, tested, or reproduced.

Every variation in the system is seed-based. The seed is composed of `world_seed`, `settlement_seed`, and `house_salt`. The same combination always produces the same building. Orderings are explicit and stable. No module calls a global random number generator.
