# BVILLAGE – System Vision

---
tier: 2
authority: REFERENCE
change-frequency: on-insight
change-rule: This document grows with research and discussion. Insights are added as they are confirmed.
  Architectural consequences are extracted into Tier 1 documents when they stabilize.
  Nothing here is final. Nothing here is throwaway.
referenced-by: DEV_ROADMAP.md, DOCS_INDEX.md
references: SYS_PRINCIPLES.md, SYS_CONCEPTS.md
status: active — living document
---

This document holds the large picture. It records the conceptual decisions that govern
where BVILLAGE is going — not what it is building today. It is the place where vision
is articulated, discussed, and slowly hardened into architecture.

Read SYS_PRINCIPLES.md and SYS_CONCEPTS.md first. This document assumes both.

---

## 1. What BVILLAGE ultimately is

BVILLAGE is a deterministic engine for generating historically plausible worlds — visually
convincing, structurally coherent, culturally grounded. The output is Blender geometry.
The foundation is historical research.

The scope is not limited to medieval central European timber framing. That is the starting
point. The engine is designed to represent any building culture, any region, any epoch —
from a Mesopotamian mud-brick settlement to a nineteenth-century Rhineland market town.
The architecture must support this from the beginning, even when the content does not yet.

Scale is not a feature to be added later. It is a design requirement from the first line
of code. The same engine that generates one house must be capable — through extension,
not rewriting — of generating a street, a village, a town, a landscape.

The primary goal is visual conviction. Historical accuracy is the means, not the end.
A building must feel right. It need not be museum-documented. Where research is thin,
informed approximation is acceptable. Where physics is violated, it is not.

---

## 2. The five levels of scale

Every generated world in BVILLAGE is organized across five levels. They are hierarchical
and interdependent. Each level constrains the one below it. Each level is inhabited by
its own logic, its own parameters, its own generation rules.

```
Landscape
  └── Region  (geophysical layer)
        └── Cultural zone  (epoch-dependent layer)
              └── Settlement
                    └── Plot
                          └── Building
```

These levels are not implementation stages — they are conceptual strata that must be
architecturally present from the beginning, even as stubs. A building that does not
know it sits on a plot, in a settlement, in a cultural zone, cannot be placed correctly.
A settlement that does not know its region cannot select plausible materials.

### Landscape

The physical world into which everything is embedded. Terrain, water, vegetation, paths.
The landscape is the substrate — it does not generate buildings, but it constrains where
and how they can stand.

### Region

The region is the geophysical layer. It is stable across centuries. Topography, geology,
climate, hydrology, available raw materials. A Mittelgebirge remains a Mittelgebirge
regardless of who rules it or when. A region has no epoch.

The region can be defined in two ways that produce the same internal representation:
parametrically (hilly terrain, limestone geology, high rainfall) or imported from GIS
data. The system does not distinguish between the two sources.

### Cultural zone

Above the geophysical region sits the cultural zone — the epoch-dependent layer. The same
geography hosts different cultures at different times. The Rhineland of the twelfth century
is not the Rhineland of the sixteenth. Building traditions, political structures, trade
connections, religious influences, wealth distributions — all of these change with time.

The cultural zone is what CultureMap models: a polygon with a time interval and a
confidence level. It is queried spatiotemporally. The geophysical region does not change;
the cultural zone sitting above it does.

### Settlement

A coherent collection of plots with a shared character. A village, a market town, a
hamlet, a fortified borough. The settlement knows its type, its wealth level, its
relationship to the surrounding landscape. It imposes constraints on the plots it contains
and coordinates diversity across them.

### Plot

The interface between settlement and building. A plot has a form, a size, a position, an
orientation to the street. The building knows its plot. The plot knows the settlement.
Nothing about a building's relationship to its neighbors is handled at the building level —
that knowledge belongs to the plot and settlement.

### Building

What BVILLAGE builds today. The building is the leaf node of the hierarchy. It receives
constraints from above and produces geometry below.

---

## 3. The spatiotemporal lookup — one mechanism for everything contextual

Everything in BVILLAGE that is contextually distributed — that exists in some places and
times but not others — is resolved through a single mechanism:

```
query(lon, lat, year, layer) → [(candidate, score), ...]
```

`layer` identifies what is being queried. The mechanism is the same regardless of what
is queried. The data behind each layer differs; the interface does not.

Examples of layers:

| Layer | What it resolves |
|-------|-----------------|
| `timber.species` | Which tree species were available here and when |
| `masonry.stone` | Which stone types were quarried in this region |
| `culture.fachwerk` | Whether timber-frame construction was practiced here |
| `culture.guild` | Whether urban guild systems were present |
| `geology.sandstone` | Sandstone availability by region |
| `political.duchy` | Political entity governing this location |
| `climate.snowload` | Expected snow load by region and season |

The confidence model is already established in ARCH_MATERIALS.md for timber species:
`core` (well-documented) → score 1.0, `halo` (plausible but sparse) → score 0.5,
no data → score 0.0.

This model extends to all layers. Data quality varies by layer and by region. The system
represents that uncertainty explicitly rather than hiding it.

New layers cost no architecture. A new layer is a new data file in `data/culturemap/`
and a registration entry. The resolver is unchanged.

---

## 4. The two kinds of constraint

BVILLAGE operates with two categorically different kinds of constraint. They must never
be conflated.

### Universal constraints — physics

Physics applies always. A beam of given cross-section and span carries a given load or
it does not. This is true in the thirteenth century, in the seventeenth, and today. The
PhysicalPlausibilityValidator operates on timeless mechanics. It knows no region, no
epoch, no culture.

Physical constraints are absolute. A building that violates physics is never generated.
There is no epoch in which a 50-meter oak beam spanning unsupported is acceptable.
This is the hard limit below which no generation result may fall.

### Contextual constraints — culture, availability, practice

Everything above the physical floor is contextual. What materials were available here?
What did builders of this time and place actually know how to build? How close to the
physical limit did they operate? What spans were considered normal, what excessive?

These constraints are resolved spatiotemporally. They do not block generation absolutely —
they shape it, score it, penalize deviation from historical plausibility.

The principle that governs the relationship between these two kinds of constraint:

**Geophysics constrains what is possible. Culture decides what is built within those
constraints. Physics determines what can stand at all.**

---

## 5. The semantic layer — from human intent to system parameters

A user does not think in parameters. A user thinks in qualities: a wealthy village, a
modest farmstead, a steep-roofed house, a wide gate. The system must accept both —
precise numerical parameters where the user provides them, and qualitative intent where
they do not.

The semantic layer translates human language into system parameters. It does not replace
the parameter system — it feeds it. Canonical parameters remain metric and unchanged
inside the engine.

This layer operates at every scale:

At building level: "large house", "low roof", "many windows"

At settlement level: "prosperous village", "densely built town", "scattered farmsteads"

At landscape level: "fertile valley", "exposed hilltop", "river crossing"

The semantic layer is already sketched in the roadmap as SEM-002. Its scope is larger
than currently described — it applies across all five levels of the hierarchy, not only
to individual building parameters.

---

## 6. Diversity and the settlement problem

A generated settlement of twenty identical houses is not a settlement. It is a stamp.
Avoiding this requires active diversity management — not noise at building level, but
coordination across a population of buildings.

The diversity problem has two dimensions.

Within-type diversity: twenty Hallenhaus buildings in the same village must look like
twenty different Hallenhaus buildings built by different people at different times, not
twenty instances of the same template. This is what NoisePolicy and SEM-003 address
at building level.

Cross-type diversity: a real village contains buildings of different ages, different
uses, different wealth levels, different states of repair. The settlement must coordinate
this distribution intentionally — not leave it to chance.

This is a settlement-level responsibility. The building does not manage it. The settlement
assigns diversity targets to plots, and plots constrain the buildings they receive.

---

## 7. What must be in the architecture now — even as stubs

The following concepts are structurally inevitable. Regardless of what research reveals
about content — how a Norman village is organized, what a medieval Rhineland plot looks
like — these structural facts will not change. They must be architecturally present now,
because adding them later forces rewrites.

**The five-level hierarchy must be explicit.** A building that does not know it sits on
a plot cannot later be given one without changing its interface. Plot, settlement, and
region must exist as defined concepts with defined data contracts — even if those contracts
are initially minimal.

**The spatiotemporal lookup must be a single, shared mechanism.** If each domain invents
its own way to query historical availability, the system fractures. One resolver, one
interface, many data layers.

**The physical floor must be enforced at the lowest level.** Physics validation is not
a feature of the building generator — it is a property of the entire system. Every
generated artifact at every scale must be physically possible.

**The semantic layer must be designed to span all levels.** A semantic layer built only
for buildings cannot later be extended to settlements without redesign. The translation
mechanism must be scale-agnostic from the beginning.

---

## 8. What research must answer before architecture can proceed

The following questions are open. They are not obstacles — they are the work. Architecture
waits for answers here rather than encoding premature assumptions.

How is a medieval settlement spatially organized? What determines street layout, plot
arrangement, the position of the church or market? How does this vary by region and epoch?

What is the relationship between plot size, building footprint, and settlement density
across different settlement types and historical periods?

How did buildings within a settlement vary from one another? What drove the diversity —
age, wealth, use, owner identity, incremental growth?

At what scale does cultural zone transition occur? Is the boundary between two building
cultures a sharp line or a gradient? How does the fuzzy core/halo model apply at
settlement scale?

These questions inform the content of the five-level hierarchy. They do not change its
existence.

---

## 9. Detail depth — what the system computes and what Blender shows

The system computes more than it renders. This is a fundamental architectural decision.

The full architectural truth of a building — every room, every wall, every structural
member, every light source, every piece of furniture — exists in the system model
regardless of what the camera sees. Blender receives a projection of that truth, not
the truth itself. What is rendered depends on camera position, visibility, level of
detail, and rendering budget. What is computed does not.

The practical consequence: interiors are fully computed even when the camera is outside.
When a door opens, the room behind it already exists. When a camera moves through a
settlement, every building it passes is architecturally complete — not a facade.

This two-layer principle — architectural model and rendering projection — must be
explicit in the system from the beginning. A building modeled only as an exterior shell
cannot later be given an interior without redesign.

---

## 10. The six dimensions of visual depth

Beyond structure, six dimensions give generated scenes their conviction. All six follow
the same principle as everything else in the system: the user may specify any parameter,
or leave it to context. What is not specified is resolved deterministically from
archetype, region, epoch, wealth, and use.

### 10.1 Light

Light is the most powerful instrument of visual conviction — more than geometry, more
than texture. A medieval hall by firelight is a different world than the same hall at
noon.

Light sources are architectural objects, not renderer decoration. A wall torch, an oil
lamp, a hearth, a candle cluster — each has a position in the building model, an
intensity, a color temperature, and a historical context. The system places them; the
renderer executes them.

Light sources are spatiotemporally constrained. Candles, oil lamps, rushes, torches,
and hearths — what existed when and where, how bright, what spectral character. Time
of day and season modulate the result. A static rendering selects a moment. An animated
sequence can move through the day.

### 10.2 Vegetation

Vegetation is already spatiotemporally anchored through the timber species database.
The step from "which trees existed here" to "where do they stand in the scene" is
conceptually small.

Two layers of vegetation exist. Wild vegetation — forests, hedgerows, verges, field
margins — follows landscape and regional logic. Cultivated vegetation — kitchen gardens,
orchards, herb plots, field crops — follows plot logic. Both are contextually resolved.
Both are epoch-dependent. The garden of a twelfth-century monastery differs from the
kitchen garden of a sixteenth-century burgher house in a Hanseatic town.

Blender Geometry Nodes provide the procedural mechanism. The system provides the
contextual parameters.

### 10.3 Material weathering

Weathering is already established in ARCH_MATERIALS.md as `Condition` — `fresh`,
`weathered`, `aged`. The deeper possibility is spatially differentiated weathering:
not a uniform global state, but a distribution across the building.

The north gable weathers more than the south face. The lower timbers suffer more than
the upper. A repaired section shows newer material against older. Sun exposure,
prevailing wind, drainage — all modulate weathering spatially. The result is seed-based
and deterministic, informed by orientation, material type, and building age.

### 10.4 Animated objects

Animated objects fall into two categories with different architectural representations.

Cyclic animation — mill wheel, flame flicker, pendulum, waterwheel — is defined by a
motion formula. The object knows its axis, its speed, its range. The renderer executes
the formula.

State-based animation — doors, gates, window shutters, drawbridges — is defined by
states and transitions. The object knows it can be open or closed, the axis of movement,
the extent of travel. A door that cannot open is not modeled the same way as one that
can.

Both types must be marked as animatable in the building model with their parameters.
The renderer reads this and generates the animation — it does not invent it.

### 10.5 Gardens and plot-level outdoor space

A garden is a floor plan, not decoration. It has structure — beds, paths, enclosures,
wells, trellises, compost, tool storage. That structure is architecturally derived from
context: who lives here, what do they do, what period is it, how wealthy are they.

Garden logic sits at plot level, not building level. The plot contains the building and
its outdoor environment as a unified spatial composition. This is one more reason the
Plot concept must be architecturally present from the beginning.

### 10.6 Construction history — layered time within a building

A building completed in 1280 and one built in 1480 look different not just in style but
in the way time has accumulated in them. A building standing since 1280 shows traces of
interventions — an extension added in 1340, a repair after a fire in 1390, an upper
storey raised in 1450. The phases are legible: in the materials, in the proportions, in
the joints between old and new work, in the slight discontinuities where one campaign
meets another.

This requires a time model for the building itself. Building elements carry individual
construction dates. Materials, weathering, and stylistic details are resolved per phase,
not globally. A building is not a single object from a single moment — it is a
accumulation of moments.

The same control principle applies here as everywhere in the system. The user may specify
phases explicitly — "three campaigns, first around 1280, second around 1340" — and the
system fills what is not specified. Or the user specifies nothing, and the system
decides whether phases are plausible based on building type, apparent age, location, and
wealth. A building in a prosperous town that contextually dates to 1280 has a high
probability of showing later interventions. A freshly built rural farmhouse does not.

Construction history is resolved through the same spatiotemporal logic as everything
else — not "what existed here" but "what plausibly happened to this building over time."

---

## 11. The construction site — roles, boundaries, and conflict

Every building in BVILLAGE is produced by a team of specialized roles coordinated by a
single authority. The roles are modeled on historical construction practice — not as
historical simulation, but because the vocabulary is precise and immediately understood.

This architecture is fully generic. The same role structure produces a timber-framed
Hallenhaus, a masonry Stadthaus, a log-construction farmhouse, or a high-rise. What
changes between building types is the content each role carries — not the roles
themselves, not the coordination mechanism.

---

### 11.1 The roles

```
Foreman       — master of the site. Last authority. Knows the plot and all
                context constraints. Coordinates the team, resolves conflicts
                that roles cannot resolve themselves. Builds nothing.

Architect     — the structural exterior. Load-bearing frame, outer shell,
                openings, vertical elements that penetrate all floors
                (stairs, chimneys, shafts). Floor dimensions may vary
                per storey. Underground floors are floors with different rules.

Roofer        — everything from eave height upward. Roof type, pitch,
                ridge direction, roof structure, overhang. Receives wall
                geometry from Architect.

Planner       — interior space. Room arrangement, zoning, circulation,
                room function. Plans within what Architect declares.
                Never touches load-bearing structure.

Furnisher     — room contents. Furniture, lighting, equipment. Plans within
                what Planner defines. Never touches room boundaries.

Landscaper    — everything outside the building envelope. Garden, paths,
                enclosures, vegetation, outdoor structures. Receives
                opening positions from Architect.
```

Each role owns exactly one decision domain. What falls within that domain is decided
by that role alone — without consultation. What falls outside is not its concern.
Conflicts arise only when two roles place legitimate demands on the same physical space
or element.

---

### 11.2 Role boundaries

The boundaries are the architecture. Without them, every element becomes a negotiation
and the system has no stable foundation.

```
Foreman      owns:  plot boundary, context constraints, conflict resolution
Architect    owns:  load-bearing structure, outer shell, opening positions,
                    vertical penetrating elements, floor-by-floor geometry
Roofer       owns:  everything above eave height
Planner      owns:  room arrangement, zoning, room function, circulation
Furnisher    owns:  room contents — furniture, lighting, equipment
Landscaper   owns:  everything outside the building envelope
```

The boundary between Architect and Planner is the most active. The Architect thinks in
structural possibility — what can be built. The Planner thinks in spatial requirement —
what is needed. When a structural element occupies space the Planner needs, that is a
genuine conflict between two legitimate demands. Neither is wrong.

The boundary between Architect and Roofer is eave height. Below it: Architect. Above
it: Roofer. Roof pitch and ridge height affect total building height, which the Foreman
constrains — this is the primary escalation path from Roofer to Foreman.

The boundary between Planner and Furnisher is the room boundary. The Planner defines
the room; the Furnisher works within it. Conflicts here are rare and typically soft —
a room too small for its required furnishing is scored, not blocked.

The boundary between Architect and Landscaper is the building envelope. The Landscaper
receives opening positions from the Architect as fixed inputs and works outward from
there.

---

### 11.3 The Declaration Register

Many structural elements have spatial consequences that cross role boundaries. A
staircase is structural — Architect — but it consumes floor area in every storey the
Planner must respect. A chimney is structural — Architect — but its footprint appears
in every room it passes through. A window is structural — Architect — but it removes
wall area the Planner may need.

The solution is not a new role for each cross-boundary element. The solution is a
Declaration Register — a formal record produced by the Architect during the briefing
phase that declares the spatial consequences of every element with cross-boundary effect.

```
Architect declares:
  post at u=2.4              → Planner: this position is structurally fixed
  stair at u=3.2, 1.2×2.4m  → Planner: reserve this footprint on all connected floors
  chimney at u=5.0, 0.6×0.6 → Planner: reserve this footprint through all floors
  window south face, 1.2m   → Planner: this wall section is open
  bay window south, +0.8m   → Landscaper: this area is covered at floor 1 height
  balcony east, floor 2     → Landscaper: this area is covered, has access from floor 2
```

The Declaration Register is produced before construction begins. Every role reads it
before planning their own domain. Most conflicts are prevented here — not resolved after
they occur.

---

### 11.4 The three-phase construction process

**Phase 1 — Briefing**

The Foreman convenes all roles. Each role submits a Proposal: what it requires, what it
prefers, what variants it can offer, and the cost of each variant. The Architect also
produces the initial Declaration Register.

The Foreman reviews all proposals for feasibility and selects the variant combination
that minimizes total cost within hard constraints. The result is the BuildingBrief —
a binding document all roles receive before construction begins.

No construction happens in this phase. Only planning and negotiation.

**Phase 2 — Construction**

Roles build sequentially, each reading all prior outputs. Within their domain, each
role may vary autonomously within its soft constraints to resolve minor tensions without
escalation. Only genuine conflicts — where no autonomous resolution is possible —
escalate to the Foreman.

Every conflict that reaches the Foreman is documented as a Conflict record with the
positions of both roles and the cost of each resolution option. The Foreman decides
by minimizing total building cost. The resolution is recorded.

**Phase 3 — Refinement**

Details that only become visible after construction is complete. Weathering distribution,
light source placement, garden details, furnishing adjustments. Each role reads the
completed outputs of all others and writes only its own refinement layer.

---

### 11.5 Conflict resolution — the cost principle

Every conflict between roles is resolved by the same mechanism regardless of which
roles are involved or what element is contested.

Each role states its position and the cost of conceding. Cost is a score reduction on
the overall candidate quality — expressed in the same units the Evaluator uses.

```
Example: window position conflict

Architect position:  window at u=3.6 — optimal for facade rhythm
  Cost if conceded:  facade rhythm broken, -0.08 score

Planner position:    wall needed at u=3.0–4.2 — room partition required
  Cost if conceded:  room loses partition, must be reorganized, -0.15 score

Foreman decision:    Architect concedes — lower total cost
  Resolution:        window moved to u=2.8, facade rhythm slightly compromised
  Total cost:        -0.08 recorded against this candidate
```

Roles first attempt autonomous resolution within their soft constraint ranges. Only
when neither role can move without violating its own hard constraints does the Foreman
intervene.

The Foreman decides by one principle: minimize total cost to the building. Not who
asked first. Not who has higher rank. Total cost.

All conflict resolutions are recorded and visible to the Evaluator. A candidate with
many small-cost conflicts may score better than one with a single large-cost conflict.
This feeds directly into multi-candidate search — the system can generate multiple
candidates and select the one with the lowest accumulated conflict cost.

---

### 11.6 Genericity — one architecture for all building types

The Foreman mechanism is fully generic. It knows nothing about timber framing, masonry,
or log construction. It knows roles, proposals, declarations, conflicts, and costs.

What is building-type-specific is the content each role carries — not the role itself.
A timber-frame Architect knows post spacing, bracing patterns, and jettying. A masonry
Architect knows wall thickness, lintel spans, and bonding. Both implement the same
interface. The Foreman coordinates both identically.

New building types require new role implementations — not new coordination architecture.
Optional roles — those that only exist for certain building types — register themselves
during briefing or remain silent. The Foreman does not ask for them.

```python
class Architect(Protocol):
    def propose(self, context: BuildContext) -> RoleProposal: ...
    def declare(self, brief: BuildingBrief) -> DeclarationRegister: ...
    def build(self, brief: BuildingBrief, declarations: DeclarationRegister) -> FramePlan: ...
    def resolve(self, conflict: Conflict) -> Resolution: ...

# Domain-specific implementations
class TimberFrameArchitect: ...   # knows posts, bracing, jettying
class MasonryArchitect: ...       # knows walls, lintels, bonding
class LogConstructionArchitect: ... # knows courses, corner joints, settlement
```

The Foreman receives any implementation of Architect. It never branches on type.

---

## 12. The guiding principle for vision work

Vision without constraint is fantasy. Constraint without vision is local optimization.

Every item in this document must eventually connect to a concrete architectural decision
or be discarded. Items that cannot be connected after sustained research are removed —
they are not architecture, they are wishful thinking.

Every architectural decision must eventually connect to something in this document or in
the principles. Decisions that cannot be connected are accidents — they will cause
incoherence.

The project is allowed to be incomplete. It is not allowed to be inconsistent.
