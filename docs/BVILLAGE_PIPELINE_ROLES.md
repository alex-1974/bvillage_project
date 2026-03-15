# BVILLAGE – Pipeline Roles

---
tier: 2
authority: ARCHITECTURAL
change-frequency: on-role-change
change-rule: Changes require explicit architecture decision. Roles, inputs, outputs, and prohibitions are contractual. Requires CHANGELOG entry.
referenced-by: SYS_CONTRACT.md, DEV_ROADMAP.md, DOCS_INDEX.md
references: SYS_PRINCIPLES.md, SYS_CONTRACT.md
---

## Zweck

Dieses Dokument definiert die **Rollen, Artefakte und Verantwortlichkeiten** in der BVILLAGE-Generierungspipeline.

Ziele:

* klare Trennung der Verantwortlichkeiten
* stabile Architekturgrenzen
* deterministische Generierung
* Erweiterbarkeit für weitere Baugrammatiken und Archetypen

Das System folgt einer **mehrstufigen Baupipeline**, analog zum realen historischen Bauprozess.

---

# Rollenhierarchie

```
Core (baugrammatik-unabhängig)
└── Commissioner
└── SiteManager / Foreman

Plugin (baugrammatik-spezifisch)
└── Topology Planner
└── Frame Producer
└── Roof Producer
└── Joiner

Core
└── Inspector / Appraiser
└── Renderer
```

# Übersicht der Pipeline

```text
Commissioner         ← Core
    ↓ BuildingOrder (mit ResolvedPolicy)
Foreman              ← Plugin
    ↓
Topology Planner     ← Plugin
    ↓ SemanticPlan (inkl. OpeningsPlan)
Frame Producer       ← Plugin
    ↓ FramePlan
Roof Producer        ← Plugin
    ↓ RoofPlan
Joiner               ← Plugin
    ↓ InteriorPlan
Inspector / Appraiser  ← Core
    ↓
Renderer             ← Core
```

Jede Rolle besitzt klar definierte **Inputs**, **Outputs** und **Verbote**.

---

# 1 Commissioner

**Lage:** Core — baugrammatik-unabhängig

## Aufgabe

Initiiert den Bauauftrag. Versammelt den rohen Kontext (Raum, Zeit, Umgebung, Klima, Topographie) und löst den vollständigen Policy-Stack auf. Übergibt `BuildingOrder` an den zuständigen `Foreman`.

Der Commissioner kennt **keine Baugrammatik**. Er weiß, was gebaut werden soll und wo — nicht wie.

## Input

extern (User, Settlement Generator)

## Output

```
BuildingOrder
  ├── archetype_id
  ├── world_seed
  ├── settlement_seed
  ├── house_salt
  ├── plot_constraints
  └── ResolvedPolicy
```

---

# 2 Foreman

**Lage:** Plugin — baugrammatik-spezifisch

## Aufgabe

Empfängt `BuildingOrder` vom Commissioner. Kennt seine Baugrammatik vollständig. Legt Dispatch-Reihenfolge und Abhängigkeiten fest (`pipeline_mode`), koordiniert alle Spezialisten und löst Konflikte zwischen ihren Outputs — innerhalb der durch den Policy-Stack gesetzten Grenzen.

Alle Konflikte zwischen Spezialisten werden über den Foreman gelöst. Kein Spezialist kommuniziert direkt mit einem anderen.

## Input

```
BuildingOrder (mit ResolvedPolicy)
```

## Output

Kein eigener Plan. Der Foreman koordiniert — er produziert nicht.
Die Pläne sind Outputs der jeweiligen Spezialisten.

## Interface

```python
class IForeman(Protocol):
    pipeline_mode: PipelineMode
    def dispatch(self, order: BuildingOrder) -> Plans: ...
    def resolve(self, escalation: EscalationRequest) -> AdjustmentResult: ...
```

`pipeline_mode` wird von der Baugrammatik bestimmt, nicht vom Archetyp:

| `construction_grammar` | `pipeline_mode` |
|---|---|
| `BOX_FRAME` | `STRUCTURE_FIRST` |
| `STOREY_FRAME` | `FUNCTION_FIRST` |
| `CRUCK_FRAME` | `STRUCTURE_FIRST` |
| `AISLED_FRAME` | `STRUCTURE_FIRST` |
| `WALL_GRID_FRAME` | `FUNCTION_FIRST` |
| `HYBRID` | `ITERATIVE` |

Der Foreman besitzt **keine domänen-agnostische Logik**. Neue Baugrammatik → neues Foreman-Plugin. Kein Core-Eingriff.

---

# 3 Topology Planner

## Aufgabe

Erzeugt die räumliche Grundorganisation des Gebäudes — einschließlich Öffnungsbedarf.

## Input

```
BuildingOrder
ResolvedPolicy
```

## Output

```
SemanticPlan
  ├── footprint
  ├── grid
  ├── frames
  ├── walls
  ├── zones
  └── OpeningsPlan
        ├── Türpositionen
        ├── Fensterpositionen
        └── Torpositionen
```

Der `OpeningsPlan` ist eine **Phase innerhalb des Topology Planners**, kein eigenständiger Pipeline-Schritt. Öffnungspositionen, -typen und -maße werden hier festgelegt. Die konstruktive Umsetzung (Torpfosten, Sturz, Aussteifungsanpassung) obliegt dem Frame Producer.

## Darf

* Frame-Sequenzen definieren
* Grid-Strukturen erzeugen
* Wandsegmente definieren
* Gebäudeflächen bestimmen
* Öffnungsbedarf (Position, Typ, Maß) festlegen

## Darf nicht

* Posts, Beams, Braces erzeugen
* Blender-Geometrie erzeugen
* Öffnungen konstruktiv umsetzen (Jambs, Lintels)

---

# 4 Frame Producer

## Aufgabe

Erzeugt das tragende Holzskelett. Setzt Öffnungsbedarf konstruktiv um.

## Input

```
SemanticPlan (inkl. OpeningsPlan)
ResolvedPolicy
```

## Output

```
FramePlan
  ├── basis
  ├── members
  └── notes
```

### Members — Beispiele

```
post.primary
post.hall
beam.plate
brace.knee
post.opening_jamb
beam.opening_lintel
```

Der Frame Producer ist der **Zimmermann**. Er erzeugt alle tragenden Member — einschließlich Torpfosten, Stürze und Aussteifungsanpassungen an Öffnungen.

```
members = strukturelle Wahrheit
```

---

# 5 Roof Producer

## Aufgabe

Erzeugt das Dachsystem.

## Input

```
FramePlan
ResolvedPolicy
```

## Output

```
RoofPlan
  ├── roof_type
  ├── pitch
  ├── rafters
  ├── purlins
  └── ridge
```

Der Roof Producer darf **FramePlan nicht verändern**.

---

# 6 Joiner

## Aufgabe

Plant Innenräume, Nutzungszonen und Erschließung. Kommuniziert Öffnungsbedarf zurück an den Topology Planner — niemals durch direkte Plan-Mutation.

## Input

```
SemanticPlan
FramePlan
ResolvedPolicy
```

## Output

```
InteriorPlan
  ├── rooms
  ├── zones
  ├── circulation
  └── functional_areas
```

## Darf

* Raumaufteilung definieren
* Nutzungszonen definieren
* Öffnungsbedarf kommunizieren (über Foreman → Topology Planner)

## Darf nicht

* `SemanticPlan`, `FramePlan` oder `RoofPlan` direkt verändern
* Tragende Elemente erzeugen
* Direkt mit anderen Spezialisten kommunizieren

---

# 7 Inspector / Appraiser

## Aufgabe

**Inspector:** Prüft universelle Physik — würde dieses Tragwerk halten? Operiert auf zeitlosen mechanischen Prinzipien (Biegesteifigkeit, Schlankheit, Auflager, Druck). Gibt `Issue`-Objekte zurück. Mutiert nichts.

**Appraiser:** Bewertet und wählt unter mehreren Kandidaten. Wertet `ConstraintsPolicy`-Gewichte aus. Verändert keine Geometrie.

## Input

```
FramePlan
RoofPlan
InteriorPlan
SemanticPlan
```

## Output

```
ValidationReport   ← Inspector
CandidateScore     ← Appraiser
```

---

# 8 Renderer

## Aufgabe

Erzeugt Blender-Geometrie aus fertigen Plänen.

## Input

```
FramePlan
RoofPlan
InteriorPlan
```

## Output

```
Blender Geometry
```

Der Renderer ist ein **Emitter** — kein Planer. Er rekonstruiert keine Struktur aus Grid, Axes oder Walls. Er baut ausschließlich, was in `FramePlan.members` steht.

---

# Wichtigste Architekturregel

Die strukturelle Wahrheit liegt ausschließlich in:

```
FramePlan.members
```

Der Renderer darf niemals Struktur aus folgenden Daten rekonstruieren:

```
grid
axes
walls
frames
```

---

# Artefaktfluss

```text
BuildingOrder (mit ResolvedPolicy)
  ↓
SemanticPlan (inkl. OpeningsPlan)
  ↓
FramePlan
  ↓
RoofPlan
  ↓
InteriorPlan
  ↓
Blender Geometry
```

---

# Ontologie

Die Pipeline basiert auf drei orthogonalen Achsen.

## Baugrammatik

```
BOX_FRAME
STOREY_FRAME
CRUCK_FRAME
AISLED_FRAME
WALL_GRID_FRAME
```

Bestimmt die **Frame Producer Logik**.

## Archetyp

```
FW-LH-ND
FW-WLD
FW-STG-GIE
```

Bestimmt die **Topologie** (Topology Planner).

## Policy

Policy moduliert Parameter:

```
bay_width
plate_height
brace_rules
```

Policy verändert **nicht die grundlegende Baugrammatik** und **nicht den Archetyp**.

---

# Architekturprinzip

BVILLAGE implementiert eine **members-first Architektur**.

```
FramePlan.members → einzige strukturelle Wahrheit
```

Alle Renderer arbeiten ausschließlich auf dieser Basis.

---

# Bedeutung für zukünftige Erweiterungen

Diese Rollenarchitektur erlaubt:

* neue Baugrammatiken
* neue Archetypen
* neue Dachsysteme
* neue Innenraumlogiken

ohne Änderungen am Core.
