# BVILLAGE – Architectural Taxonomy

---
tier: 2
authority: REFERENCE
change-frequency: on-feature
change-rule: Expandable by adding new entries to the tables. Structural principles are not defined here — see SYS_PRINCIPLES.md and ARCH_POLICIES.md.
referenced-by: ARCH_POLICIES.md, DEV_ROADMAP.md, DOCS_INDEX.md
references: SYS_CONCEPTS.md §1, ARCH_POLICIES.md §2, ARCH_BAUGRAMMATIKEN_WISSENSCHAFT.md §4–6
---

This document is a research-driven catalogue. It records building types that have been studied, classified, and assigned IDs within the system. It grows as research advances. The classification criteria that govern it are defined in ARCH_POLICIES.md.

The current catalogue covers medieval central European timber framing. It is the starting point, not the boundary of the system.

---

## 1. What an archetype is — and what it is not

An archetype defines a spatial family: how a building organizes its zones, moves its occupants, places its openings, and relates its parts to one another. Two buildings belong to the same archetype if they share the same fundamental spatial logic — regardless of region, epoch, material, or size.

An archetype does not define beam sections, material choices, roof pitch, ornament level, or regional expression. Those are the domain of policies. An archetype defines topology, not appearance.

The practical consequence: building a Hallenhaus in Westphalia and building one in Mecklenburg produces two buildings with the same archetype ID and different StylePolicy configurations. Building a Hallenhaus and a Stadthaus on the same plot produces two buildings with different archetype IDs — because their spatial logic is fundamentally different, not because they look different.

**When a new building type gets its own archetype ID:**
Its spatial organization — zone arrangement, circulation logic, load hierarchy, opening program — is meaningfully different from all existing archetypes. A different roof pitch or a different regional expression is not sufficient. A different room hierarchy, a different relationship between served and service spaces, or a different structural load path that determines spatial organization — these are sufficient.

**When a new building type does not get its own archetype ID:**
It is a regional or epochal variant of an existing spatial family, expressible through StylePolicy, TopologyModifier, VerticalPolicy, or RoofPolicy. The test is simple: if two planners, working independently from the same archetype with different policies, would produce recognizably related buildings, it is the same archetype.

---

## 2. ID scheme

Archetype IDs follow a structured pattern:

```
<DOMAIN>-<FAMILY>-<VARIANT>
```

- **DOMAIN** — construction domain prefix (FW = Fachwerk, MB = Mauerwerk, BK = Blockbau, ...)
- **FAMILY** — spatial family abbreviation (LH = Langhaus/Hallenhaus, ER = Ernhaus, STG = Stadthaus, ...)
- **VARIANT** — distinguishing characteristic within the family (ND = Niederdeutsch, 2S = Zweiständer, GIE = Giebelständig, ...)

IDs are stable once assigned. They do not change when research refines the understanding of a type — a research update adds notes or splits into sub-entries; it does not reassign existing IDs.

### type_family

Each archetype belongs to a `type_family` — the plugin folder under `bvillage/types/<domain>/` that contains its Topology Planner. The `type_family` determines which `ITopologyProducer` implementation resolves the archetype. Multiple archetype IDs may share one `type_family` if their topological planning logic is identical or differs only in policy parameters.

The `type_family` is a plugin binding, not a scientific classification. It is assigned when the archetype is implemented, not when it is catalogued. Provisional entries may carry `type_family: TBD`.

### construction_grammar

Each archetype maps to a `construction_grammar` — the generative logic that produces its structural members. Current values: `BOX_FRAME`, `STOREY_FRAME`, `CRUCK_FRAME`, `AISLED_FRAME`, `WALL_GRID_FRAME`. The construction grammar determines which `IFrameProducer` implementation is dispatched. See `ARCH_BAUGRAMMATIKEN_WISSENSCHAFT.md §4` for the scientific basis of each grammar.

---

## 3. Fachwerk — timber frame (domain: FW)

The current implementation domain. All entries below are research-based and expandable.

### 3.1 Longhouse family (Hallenhaus / Langhaus)

Buildings organized along a single longitudinal axis, integrating living, agricultural, and storage functions under one roof. Load-bearing structure runs transversely across the short axis.

| ID | Name | Structural signature | Region | Period | `construction_grammar` | `type_family` |
|---|---|---|---|---|---|---|
| FW-LH-ND | Niederdeutsches Hallenhaus | Longitudinal threshing floor (Längsdiele), three-aisled | Northern Germany | 13–19c | `BOX_FRAME` | `longhouse` |
| FW-LH-2S | Hallenhaus Zweiständer | Two interior post rows | Northern Germany | 15–18c | `BOX_FRAME` | `longhouse` |
| FW-LH-3S | Hallenhaus Dreiständer | Asymmetric post rows | Northern Germany | 16–18c | `BOX_FRAME` | `longhouse` |
| FW-LH-4S | Hallenhaus Vierständer | Four post rows | Northern Germany | 16–19c | `BOX_FRAME` | `longhouse` |
| FW-GULF | Gulfhaus | Large central volume (Gulf), posts at periphery | North Sea coast | 16–19c | `BOX_FRAME` | `longhouse` |
| FW-HAUB | Haubarg | Central post structure, large collective barn | North Frisia | 17–19c | `BOX_FRAME` | `longhouse` |
| FW-MITT | Mittertennhaus | Central threshing floor (Tenn) | Alpine region | 15–19c | `BOX_FRAME` | `longhouse` |
| FW-LH-EN | English Longhouse *(prov.)* | Living and byre under one roof, cross-passage entry | England, Wales | 12–16c | `BOX_FRAME` | `longhouse` |

### 3.2 Ernhaus family

Buildings with a transverse entry hall (Ern) separating living and agricultural zones. Load and circulation organized across the short axis differently from the Hallenhaus.

| ID | Name | Structural signature | Region | Period | `construction_grammar` | `type_family` |
|---|---|---|---|---|---|---|
| FW-ER-MD | Mitteldeutsches Ernhaus | Transverse hall (Ern) | Central / Southern Germany | 14–18c | `STOREY_FRAME` | `ern_house` |
| FW-HARZ | Harzer Haus | Ernhaus variant, mountain adaptation | Harz region | 16–19c | `STOREY_FRAME` | `ern_house` |

### 3.3 Hybrid structural family

Buildings that combine timber framing with a secondary structural system in a way that defines a distinct spatial and structural type.

| ID | Name | Structural signature | Region | Period | `construction_grammar` | `type_family` |
|---|---|---|---|---|---|---|
| FW-UMG | Umgebindehaus | Log living cell (Blockstube) within timber frame surround (Umgebinde) | Upper Lusatia | 15–19c | `HYBRID` | TBD |

### 3.4 Urban types (Stadthaus)

Buildings designed for narrow urban parcels. Structural logic runs differently from rural longhouse types: the short axis faces the street, and load paths adapt to the constrained plot width.

| ID | Name | Structural signature | Region | Period | `construction_grammar` | `type_family` |
|---|---|---|---|---|---|---|
| FW-STG-GIE | Giebelständiges Stadthaus | Gable end to street, narrow parcel, deep plan | Towns | 14–18c | `STOREY_FRAME` | `townhouse` |
| FW-STG-TRF | Traufenständiges Stadthaus | Eaves side to street, broader frontage | Towns | 15–18c | `STOREY_FRAME` | `townhouse` |
| FW-ACK | Ackerbürgerhaus | Urban plot with agricultural annex | Small towns | 15–19c | `STOREY_FRAME` | `townhouse` |
| FW-SPC | Speicherhaus | Storage building, minimal living program | Towns | 15–18c | `STOREY_FRAME` | `townhouse` |
| FW-MER | Merchant House | Projecting upper storeys, commercial ground floor | England, Low Countries | 14–17c | `STOREY_FRAME` | `townhouse` |

### 3.5 Compound types (Hofanlage)

Multi-wing arrangements enclosing a yard. Spatial logic is defined by the relationship between wings rather than a single building volume.

| ID | Name | Structural signature | Region | Period | `construction_grammar` | `type_family` |
|---|---|---|---|---|---|---|
| FW-HOF | Fachwerk-Hofanlage | Multi-wing yard enclosure | Central / Southern Germany | 16–19c | `STOREY_FRAME` | `courtyard` |

### 3.6 English hall types

Open-hall buildings with a central, roof-open living space. Structurally distinct from the Hallenhaus: no agricultural integration; spatial hierarchy centers on the hall itself.

| ID | Name | Structural signature | Region | Period | `construction_grammar` | `type_family` |
|---|---|---|---|---|---|---|
| FW-WLD | Wealden House | Open hall flanked by two-storey jetted bays under continuous roof; flying wall plate | South-east England | 14–16c | `BOX_FRAME` | `longhouse` |
| FW-OHALL | Open Hall House | Single-storey central open hall, unjetted | England | 13–16c | `BOX_FRAME` | `longhouse` |
| FW-AIS | Aisled Hall House | Internal arcade rows carry roof; nave + aisles | England, Low Countries | 12–16c | `AISLED_FRAME` | `aisled` |

### 3.7 Cruck family

Buildings whose primary structure is formed by curved or straight cruck blades rising from near ground level to the ridge. Roof and wall load path are unified. Geographically confined to England and Wales (documented); West France (marginal).

| ID | Name | Structural signature | Region | Period | `construction_grammar` | `type_family` |
|---|---|---|---|---|---|---|
| FW-CRK | Cruck House (Full Cruck) | Blades from near ground to ridge | England, Wales | 12–17c | `CRUCK_FRAME` | `cruck` |
| FW-CRJ | Jointed Cruck House | Blades jointed at wall-head, not continuous | West England | 13–16c | `CRUCK_FRAME` | `cruck` |
| FW-CRR | Raised Cruck House | Blades begin above wall-head; stone wall base | England | 14–17c | `CRUCK_FRAME` | `cruck` |

### 3.8 Wall-grid types (pan de bois / Wandraster) *(Phase 2)*

Buildings whose primary organizing element is a self-braced facade grid of posts, rails, and diagonals. Each storey is a structurally autonomous unit. Concentrated in Alsace, Normandy, and Lorraine.

| ID | Name | Structural signature | Region | Period | `construction_grammar` | `type_family` |
|---|---|---|---|---|---|---|
| FW-PDC | Maison à pans de bois | Regular post-rail facade grid; superposed self-braced storeys | France, Alsace | 14–18c | `WALL_GRID_FRAME` | TBD |
| FW-COL | Colombage House | Wall-grid with regional ornamental diagonal pattern | Normandy, Lorraine | 14–18c | `WALL_GRID_FRAME` | TBD |

### 3.9 Provisional entries

Entries with insufficient primary source coverage. May be revised, merged into existing types, or promoted to full entries as research matures. IDs are reserved and stable.

| ID | Name | Note | `construction_grammar` | `type_family` |
|---|---|---|---|---|
| FW-STV | Stavkirke-Grundtypus | Core-post logic may not map to `BOX_FRAME`; primary literature lacking | `BOX_FRAME` (tentativ) | TBD |

---

## 4. Other domains — placeholder

As research expands beyond Fachwerk, new domain sections are added here following the same structure. Domain prefix assignments:

| Prefix | Domain | Directory |
|--------|--------|-----------|
| FW | Fachwerk / timber frame | `timber_frame` |
| MB | Mauerwerk / load-bearing masonry | `masonry` |
| BK | Blockbau / log building | `log_building` |
| EA | Earth architecture / rammed earth, adobe | `earth_construction` |
| PG | Post-in-ground / early post-frame | `post_in_ground` |

New domain prefixes are assigned when a domain is formally added to the system.

---

## 5. Reading the table

**Structural signature** describes the distinguishing constructive or spatial characteristic that justifies a separate ID — not the full description of the building type. It answers: what makes this different from its closest relative in the table?

**Region** is the primary historical distribution area. Buildings of the same type existed outside this area; region is a research anchor, not a boundary.

**Period** is the range of documented examples. It reflects available research, not absolute historical limits. Early examples may predate the listed start; the type may have persisted beyond the listed end in vernacular use.

**`construction_grammar`** is the generative logic dispatched by the Frame Producer. It is a code binding, not a scientific classification. See §2 and `ARCH_BAUGRAMMATIKEN_WISSENSCHAFT.md §4` for definitions.

**`type_family`** is the plugin folder under `bvillage/types/<domain>/` that provides the Topology Planner for this archetype. `TBD` indicates the archetype is catalogued but not yet implemented.

---

## 6. Expanding the taxonomy

Adding a new entry requires:

1. A documented research basis — at least one primary or secondary source describing the type.
2. A clear structural signature that distinguishes it from existing entries.
3. A decision on whether it warrants a new archetype ID or is better expressed as a policy variant of an existing one. See section 1 for the decision criteria and ARCH_POLICIES.md §6 for the broader classification logic.
4. Assignment of an ID following the scheme in section 2.
5. Assignment of a `construction_grammar` from the canonical list in `ARCH_BAUGRAMMATIKEN_WISSENSCHAFT.md §4`. If the grammar does not exist yet, flag it before creating the entry — new grammars require a full WISSENSCHAFT entry.
6. Assignment of a `type_family`. If the Topology Planner does not exist yet, set `TBD`. `TBD` entries are valid catalogue entries but cannot be dispatched by Foreman until implemented.

Entries marked as research-incomplete may be added with a `status: provisional` flag. Provisional entries may be revised or merged as research matures. They are never deleted — if a provisional entry turns out to be a policy variant of an existing type, it is reclassified and the original ID is retired with a note.
