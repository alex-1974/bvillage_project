# BVILLAGE – Material System

---
tier: 2
authority: REFERENCE
change-frequency: on-feature
change-rule: MaterialClass list stays small (max 10). Species are expandable. No render logic in physics parameters, no physics logic in render parameters. Every used material must be registered here.
referenced-by: SYS_CONTRACT.md §14, DEV_ROADMAP.md (MAT-001)
references: SYS_CONTRACT.md §14, SYS_CONCEPTS.md §6
---

## Design principle

Material in BVILLAGE is not appearance and not geometry. It is a layered description of a physical substance — what it is, how it behaves structurally, how it looks, where it existed historically, and in what form it was used.

Every material used anywhere in the system must be registered in this document and in the MaterialRegistry. An unregistered material ID is a contract violation. There is no fallback, no default substitution.

Physics and rendering are carried by the same material node but must never influence one another. A renderer choosing a darker tone does not change load capacity. A validator checking deflection does not concern itself with surface finish.

---

## 1. Hierarchical model

Materials are organized in four taxonomic levels. Each level inherits from its parent. Parameters are only defined at the level where they diverge from the parent — everything else is inherited.

```
MaterialClass       timber, masonry, earth, metal, glass
  MaterialFamily    hardwood, softwood / brick, sandstone / ...
    MaterialSpecies quercus.robur, pinus.sylvestris / ...
      MaterialSubtype  old_growth, plantation, regional variant (where relevant)
```

Below the taxonomic hierarchy, two orthogonal dimensions apply:

```
ProductForm    log, beam, plank, board, rubble, ashlar, ...
Condition      fresh, weathered, aged, rotting, damaged
Finish         sawn, planed, oiled, painted, whitewashed, tarred, ...
```

ProductForm may override physics parameters — a sawn beam has different effective bending properties than a round log of the same species, because sawing interrupts grain continuity. Condition and Finish affect rendering only in the current phase. Neither creates a new material ID.

### Inheritance and override rule

A parameter defined at a lower level overrides the parent. A parameter not defined at a lower level is inherited from the parent unchanged. The threshold for defining a physics override at species or subtype level is a meaningful difference — roughly 10–15% from the parent value. Smaller differences fall into deterministic variation, not taxonomy.

### Parameter separation

Each node carries two independent parameter sets:

**Physics** — used by PhysicalPlausibilityValidator and DomainConstructor:
- `density_kg_m3`
- `E_modulus_GPa`
- `bending_strength_MPa`
- `compression_strength_MPa` *(where relevant)*
- `shear_strength_MPa` *(where relevant)*

**Render** — used by the renderer:
- `base_color_hex`
- `roughness` (0–1)
- `metallic` (0–1)
- `grain_direction` *(timber only)*
- `variation_palette` — list of hex values for deterministic color sampling
- `roughness_jitter` — range for seed-based roughness variation

Physics parameters never appear in Render. Render parameters never appear in Physics.

---

## 2. Spatiotemporal availability

Some materials have historically constrained availability — they existed only in certain regions and certain periods. This is most significant for timber species, less so for stone and brick which are broadly tied to local geology.

Availability data exists at Species or Subtype level. It informs `resolve_material()` about whether a requested material is plausible for a given region and epoch. An availability entry does not prohibit use outside its range — it informs ConstructionCulturePolicy and StylePolicy about what is plausible. Hard prohibition is a policy decision, not a registry decision.

### Availability entry format

Each availability entry is an `AvailabilityTrace` with three fields:

```
region: Polygon | MultiPolygon   # geographic extent (WGS84 coordinates)
period: (year_from, year_to)     # inclusive integer years; negative = BCE
confidence: "core" | "halo"      # core = well-documented; halo = plausible but sparse
```

`resolve_material()` queries availability by (lon, lat, year). It returns a membership score: `core` → 1.0, `halo` → 0.5, no entry → 0.0. The score feeds into ConstructionCulturePolicy and StylePolicy as a plausibility prior — it does not block generation.

Multiple entries per species are permitted and expected: the same oak species may have a core zone in the Rhine valley and a halo zone extending into the Alpine foothills. Entries for the same species do not overlap in confidence level — if regions overlap geographically, the higher confidence value applies.

Availability data is stored in `data/culturemap/` and loaded by the deterministic loader defined in SYS-005 (DEV_ROADMAP.md). The catalogue here records what availability data exists per species; the loader resolves it at generation time.

---

## 3. Timber (MaterialClass: timber)

Timber is the primary structural material for the current implementation domain. The catalogue below covers species historically relevant for central European construction. Other cultural regions will add species as research advances.

### 3.1 Hardwood family (timber.hardwood)

Base physics:
- density: 650–750 kg/m³
- E_modulus: 11–14 GPa
- bending_strength: 50–70 MPa

Base render:
- base_color: `#A0724A`
- roughness: 0.80
- grain_direction: longitudinal

---

**quercus.robur** — Pedunculate oak / Stieleiche

Physics override: density 680 kg/m³, E_modulus 13 GPa, bending_strength 60 MPa

Render override: base_color `#8B5E3C`, variation_palette [`#7A5230`, `#9C6B45`, `#6E4A2A`]


Subtype: `quercus.robur.old_growth`
- Physics override: density 720 kg/m³, bending_strength 68 MPa
- notes: Old-growth forest stock, common in early medieval construction. Increasingly scarce after 1400 due to deforestation.

---

**quercus.petraea** — Sessile oak / Traubeneiche

Physics override: density 660 kg/m³, E_modulus 12.5 GPa

Render override: base_color `#8A5D3B`


---

**fagus.sylvatica** — European beech / Rotbuche

Physics override: density 720 kg/m³, E_modulus 14 GPa, bending_strength 62 MPa

Render override: base_color `#C4956A`, variation_palette [`#B8845C`, `#D0A678`]


---

**fraxinus.excelsior** — European ash / Gemeine Esche

Physics override: density 690 kg/m³, E_modulus 12 GPa, bending_strength 58 MPa, shear_strength 9 MPa

Render override: base_color `#C8AA82`


---

**ulmus.glabra** — Wych elm / Bergulme

Physics override: density 670 kg/m³, bending_strength 55 MPa

Render override: base_color `#9C7248`


---

**alnus.glutinosa** — Black alder / Schwarzerle

Physics override: density 530 kg/m³, bending_strength 45 MPa

Render override: base_color `#B07840`


---

### 3.2 Softwood family (timber.softwood)

Base physics:
- density: 480–560 kg/m³
- E_modulus: 9–12 GPa
- bending_strength: 35–50 MPa

Base render:
- base_color: `#D4A96A`
- roughness: 0.75
- grain_direction: longitudinal

---

**pinus.sylvestris** — Scots pine / Waldkiefer

Physics override: density 520 kg/m³, E_modulus 10 GPa, bending_strength 40 MPa

Render override: base_color `#C8956A`, variation_palette [`#BA8558`, `#D4A57A`]


---

**pinus.nigra** — Black pine / Schwarzkiefer

Physics override: density 560 kg/m³, E_modulus 10.5 GPa, bending_strength 42 MPa

Render override: base_color `#B8854A`


---

**picea.abies** — Norway spruce / Gemeine Fichte

Physics override: density 470 kg/m³, E_modulus 11 GPa, bending_strength 38 MPa

Render override: base_color `#D4A870`, roughness: 0.70


---

**abies.alba** — Silver fir / Weißtanne

Physics override: density 450 kg/m³, E_modulus 11 GPa, bending_strength 36 MPa

Render override: base_color `#D8B07A`


---

**larix.decidua** — European larch / Europäische Lärche

Physics override: density 590 kg/m³, E_modulus 12 GPa, bending_strength 50 MPa

Render override: base_color `#C07848`, variation_palette [`#B06838`, `#D08858`]


---

### 3.3 ProductForm — timber

ProductForm modifies physics and render of the parent species. Only divergences from the species baseline are listed.

| ProductForm | Physics override | Render notes |
|-------------|-----------------|--------------|
| `log` | baseline — round section, full grain continuity | bark texture, round cross-section |
| `beam` | bending_strength ×0.90 — sawing interrupts grain | sawn faces, rectangular section |
| `plank` | bending_strength ×0.85 — thin section | wide sawn face visible |
| `board` | bending_strength ×0.80 — thin, narrow | fine-sawn surface |
| `half_log` | bending_strength ×0.92 | flat face + curved face |
| `squared_log` | bending_strength ×0.88 — adze-hewn | adze marks visible on faces |

---

## 4. Masonry (MaterialClass: masonry)

### 4.1 Brick family (masonry.brick)

Base physics:
- density: 1700–2000 kg/m³
- E_modulus: 3–8 GPa
- compression_strength: 5–25 MPa
- bending_strength: 0.5–2 MPa

Base render:
- base_color: `#B5624A`
- roughness: 0.85

---

**brick.historic_low** — Low-fired historic brick

Physics override: density 1700 kg/m³, compression_strength 5 MPa

Render override: base_color `#C07860`, variation_palette [`#B86848`, `#CC8868`]


---

**brick.historic_mid** — Medium-fired historic brick

Physics override: density 1850 kg/m³, compression_strength 12 MPa

Render override: base_color `#B05840`


---

**brick.historic_high** — High-fired brick / Klinker

Physics override: density 2000 kg/m³, compression_strength 25 MPa

Render override: base_color `#8A3A28`, roughness: 0.75


---

### 4.2 Stone family (masonry.stone)

**stone.sandstone_weak**

Physics: density 2000 kg/m³, E_modulus 4 GPa, compression_strength 20 MPa

Render: base_color `#D4B882`, roughness: 0.88


---

**stone.sandstone_strong**

Physics: density 2300 kg/m³, E_modulus 20 GPa, compression_strength 80 MPa

Render: base_color `#C8A86A`, roughness: 0.82


---

**stone.granite**

Physics: density 2700 kg/m³, E_modulus 50 GPa, compression_strength 200 MPa

Render: base_color `#A09088`, roughness: 0.78, variation_palette [`#907E7A`, `#B0A090`]


---

### 4.3 ProductForm — masonry

| ProductForm | Notes |
|-------------|-------|
| `rubble` | uncut field stone; lower effective strength due to irregular bonding |
| `ashlar` | cut and dressed; full strength values apply |
| `coursed_rubble` | intermediate; partial strength reduction |

---

## 5. Binder (MaterialClass: binder)

**binder.mortar_lime** — Lime mortar

Physics: density 1600 kg/m³, compression_strength 1–3 MPa

Render: base_color `#E8E0CC`, roughness: 0.92


---

**binder.mortar_hydraulic** — Hydraulic lime mortar

Physics: density 1750 kg/m³, compression_strength 5–10 MPa

Render: base_color `#D8D0BC`


---

## 6. Earth (MaterialClass: earth)

Placeholder for rammed earth, adobe, and cob construction. Full catalogue developed when the earth architecture domain is added.

---

## 7. Other materials

**glass.soda_lime** — Historic window glass

Physics: density 2500 kg/m³ *(not structurally loaded)*

Render: base_color `#C8E8D8`, roughness: 0.05, metallic: 0.0


---

**metal.wrought_iron** — Wrought iron

Physics: density 7700 kg/m³, E_modulus 190 GPa, bending_strength 250 MPa

Render: base_color `#4A4844`, roughness: 0.70


---

## 8. Condition modifiers

Condition is applied after material and ProductForm resolution. It affects rendering only in the current phase. It does not create a new material ID.

| Condition | Render effect |
|-----------|---------------|
| `fresh` | baseline render values |
| `weathered` | roughness +0.08, base_color darkened -0.05 |
| `aged` | roughness +0.15, base_color darkened -0.12, color desaturated |
| `rotting` | *(future)* strong color shift, surface disruption |
| `damaged` | *(future)* local geometry modification |

---

## 9. Finish modifiers

Finish is applied after Condition. It affects rendering only. It does not create a new material ID.

| Finish | Render effect |
|--------|---------------|
| `sawn` | roughness 0.65, fine parallel grain marks |
| `planed` | roughness 0.50, smooth face |
| `oiled` | roughness -0.10 from base, slight sheen |
| `painted` | base_color fully overridden by paint color |
| `whitewashed` | base_color `#F0EDE4`, partial coverage variation |
| `tarred` | base_color `#1A1008`, roughness 0.60 |
| `adze_hewn` | roughness 0.82, irregular surface marks |

---

## 10. Material ID format

```
<family>.<species>[.<subtype>]
```

Examples:
- `timber.oak` → quercus.robur, no subtype
- `timber.oak.old_growth` → quercus.robur, old_growth subtype
- `brick.historic_mid`
- `stone.granite`
- `binder.mortar_lime`

Condition and Finish are not encoded in the ID. They are separate member attributes.

---

## 11. Resolution

```
resolve_material(member, ctx) → MaterialVariant
```

Resolution checks in order:
1. ID exists in registry → if not: HARD Issue, generation stops.
2. Species availability is plausible for ctx.region and ctx.epoch → if not: SOFT Issue, logged.
3. ProductForm is valid for the species → if not: HARD Issue.

Visual variation after resolution:

```
sample_render(material, condition, finish, seed, salt) → RenderSample
```

`salt` is a stable member identifier. Same member, same seed always produces the same visual sample. No global RNG is involved.

---

## 12. Scope boundaries — current phase

Out of scope for the current phase:
- Timber moisture classes and grading
- Knot and grain modelling
- DIN or Eurocode classification
- Mechanical degradation through Condition
- Chemical aging
- Earth architecture materials (placeholder only)

Expanding within the current catalogue — adding a species, subtype, ProductForm entry, or Finish modifier — requires no architectural change. Expanding beyond the current scope, particularly adding mechanical degradation to Condition, requires an explicit architecture decision and a CHANGELOG entry.
