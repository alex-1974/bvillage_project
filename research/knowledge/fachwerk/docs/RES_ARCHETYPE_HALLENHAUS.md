# RES_ARCHETYPE_HALLENHAUS
## Archetyp-Dokumentation: Niederdeutsches Hallenhaus und Hallenbau-Familie

---

```yaml
tier: 2
authority: REFERENCE
status: Freigegeben
version: 1.0
datum: 2026-03-07
bereich: FACHWERK/ARCHETYPEN
references:
  - RES_FACHWERK_DEFINITION.md
  - RES_BAUGRAMMATIKEN.md
  - RES_KONSTRUKTION_ALLGEMEIN.md
  - RES_BAUPRAXIS_QUANTITATIV.md
  - BVILLAGE_Structural_Grammar_Architecture.md
```

---

## Methodik und Evidenzgrade

- **[HART]** — durch mehrere unabhängige akademische Quellen gesichert
- **[MITTEL]** — durch eine Primärquelle oder übereinstimmende Sekundärquellen gestützt
- **[SCHWACH]** — aus experimenteller Archäologie, Analogieschlüssen oder Fachtradition

---

## 0. Zimmermannslogik als Ausgangspunkt

Dieses Dokument beschreibt keine Hübschheit, sondern
**Baufähigkeit**: die Regeln, die ein `HallGrammarArchitect` braucht,
um aus `(domain, archetype, epoch_band, region, wealth)` einen
montagefähigen `FramePlan` zu erzeugen.

Vier Axiome der Zimmermannslogik:

1. **Tragwerk vor Raum** — die Konstruktion erzwingt den Raum, nicht umgekehrt
2. **Rahmen vor Wand** — der Querrahmen (Binder) ist die primäre Einheit
3. **Modul vor Maß** — Bays, Gefache, Ständerreihen sind das Raster
4. **Abbund vor Baustelle** — der `FramePlan` ist der digitale Abbundriss: vollständig, explizit, montagefähig

---

## 1. Begriffsklärung

### 1.1 Binder (Querrahmen / Cross-frame)

Ein **Binder** ist ein tragender Querrahmen (quer zur Längsachse), der
Dach- und ggf. Deckenlasten über Ständer auf Schwelle/Fundament ableitet.
Er ist eine montagefähige Einheit: Abbund → Aufrichten.

### 1.2 Bay (Feld)

Ein **Bay** ist der Längsabschnitt zwischen zwei Bindern. Bay ist
die Wachstumsoperation: Hauslänge entsteht als Bay-Serie.

Definition nach Hewett (Structural Carpentry in Medieval Essex):
„length between two transverse frames". Das ist die Baseline für
BVILLAGE. **[HART]**

### 1.3 Ständerreihe (Support Row)

Eine **Ständerreihe** ist eine Längsreihe tragender Pfosten. Sie definiert
Hallenbreite, Seitenschiffe und Dachsystem-Zwänge.

### 1.4 Gefach

Das **Gefach** ist das Wandfeld zwischen Holzgliedern. Gefachlogik ist
Rasterlogik: Maße, Riegelhöhen, Aussteifung, Öffnungsintegration.

### 1.5 Diele (Deele, Del)

Die **Diele** ist der zentrale Dreschtennenboden des Hallenhauses.
Die große Einfahrtstür an der Giebelseite gibt dem Erntewagen Einfahrt.
Stallbögen rechts und links. Das Heu im Hochlager über allem.

---

## 2. Tragwerkslogik: Hall/Aisled Grammar

### 2.1 Grundprinzip

Hall/Aisled Grammar ist span-orientiert:

- Last dominiert vom Dach
- Tie-beams / Pfetten / Kehlbalken verteilen Kräfte
- **Innenstützen (Support Rows) sind zentral** — das Haus denkt von innen nach außen

Das unterscheidet das Hallenhaus fundamental vom Stadthaus (Ernhaus):
beim Stadthaus tragen die Außenwände das Dach; beim Hallenhaus tragen
die inneren Ständerreihen.

### 2.2 BVILLAGE-Invarianten (Hall-Grammar)

- `support_rows >= 2` (Außenreihen), plus Innenreihen nach cross_section_type
- `bay_extension` ist die primäre Wachstumsoperation
- Große Öffnungen beeinflussen `FrameRole` (End-/Gate-Frames)

### 2.3 FrameRole-Typen

| FrameRole | Beschreibung |
|---|---|
| `END_FRAME_FRONT` | Giebelabschluss vorn |
| `END_FRAME_REAR` | Giebelabschluss hinten |
| `INTERMEDIATE_FRAME` | Normaler Binder dazwischen |
| `SPECIAL_GATE_FRAME` | Torrahmen am Giebel |
| `SPECIAL_HEARTH_FRAME` | Binder mit Herdlogik |
| `SPECIAL_FLETT_FRAME` | Binder mit Flett-Abgrenzung |
| `SPECIAL_BRACING_FRAME` | Verstärkter stiff frame |

Historische Häuser zeigen, dass einzelne Frames oft verstärkt oder
anders organisiert sind, um Wind- und Längsaussteifung zu sichern.
**[MITTEL]**

### 2.4 Binder-Zusammensetzung (member-Liste)

Ein historischer Querrahmen besteht typischerweise aus:

- Ständer (post)
- Ankerbalken / Deckenbalken (tie beam)
- Rähm / Trauflinie (top plate / wall plate)
- Kopfbänder (knee braces) zur Knotensteifigkeit
- ggf. zusätzliche Streben / Schwertstreben
- definierte Anschlussstellen für Dach (Sparren / Pfetten / Kehlbalken)

Jeder dieser Teile ist ein `StructuralMember` mit expliziter Rolle.
Blender darf nicht raten.

---

## 3. Querschnittstypen (Ständerreihen)

### 3.1 Zweiständerhaus (FW-LH-2S)

Zwei innere Ständerreihen. Minimales System, geringere Breite.
Längsbalken liegen auf Ständerköpfen.

| Parameter | Wert |
|---|---|
| Innenreihen | 2 |
| Gesamtbreite | 6–10 m |
| Verbreitung | Niedersachsen, Westfalen |
| Epoche | 15.–18. Jh. |

### 3.2 Dreiständerhaus (FW-LH-ND — Leittyp)

Drei Schiffsbreiten: Mitteldiele + zwei Seitenschiffe. Das ist die
kanonische Form des niederdeutschen Hallenhauses. **[HART]**

| Parameter | Wert |
|---|---|
| Innenreihen | 2 (je ca. 3–4 m von Außenwand) |
| Gesamtbreite | 10–14 m |
| Hallbreite (Mitteldiele) | 3,0–4,5 m |
| Seitenschiffbreite | 1,6–2,8 m |
| Verbreitung | Norddeutsche Tiefebene, Niederrhein bis Pommern |
| Epoche | 13.–19. Jh. (erhaltene Bauten ab spätem 15. Jh.) |

Asymmetrie ist historisch plausibel: Seitenschiffe können unterschiedlich
breit sein (Nutzung, Bauphase, Gelände). Frames bleiben konstruktiv sauber.

### 3.3 Vierständerhaus (FW-LH-4S)

Vier Innenreihen, zwei Mittelschiffe. Maximale Spannweite.

| Parameter | Wert |
|---|---|
| Innenreihen | 4 |
| Gesamtbreite | 12–18 m |
| Verbreitung | Niedersachsen, Holstein |
| Epoche | 16.–19. Jh. |

### 3.4 Wichtig: Innenständer stehen im Raum

Innenreihen stehen in der Diele — der Raum ist nicht frei wie im
modernen Grundriss. BVILLAGE: Interior darf das nicht wegplanen.
Räume sind Zonen um Ständerachsen.

---

## 4. Maßtabellen (operative Policy-Ranges)

**Evidenz:** [HART] für Messwerte aus dendrodatierten Bauten; [MITTEL]
für erschlossene Normalbereiche. Die ältesten erhaltenen Hallenhäuser
mit Innenständergerüst beginnen im **ausgehenden 15. Jahrhundert** —
frühere Existenz des Typus ist archäologisch wahrscheinlich, aber nicht
an erhaltenen Objekten belegbar. **[HART]** nach Klein (2012).

### 4.1 Längsraster (Bay)

| Parameter | Minimalwert | Normalbereich | Maximalwert | Evidenz |
|---|---|---|---|---|
| `bay_width_m` | 1,8 m | 2,3–2,7 m | 4,5 m | [MITTEL] |
| `bay_count` | 2 | 3–6 | 10+ | [MITTEL] |
| `end_zone_depth_factor` | 0,3 | 0,4–0,6 | 0,7 | [SCHWACH] |

### 4.2 Querschnitt (Dreiständer-Default)

| Parameter | Minimalwert | Normalbereich | Maximalwert | Evidenz |
|---|---|---|---|---|
| `hall_width_m` (Mitteldiele) | 2,5 m | 3,0–4,5 m | 6,0 m | [HART] |
| `aisle_width_m` (Seitenschiff) | 1,2 m | 1,6–2,8 m | 3,5 m | [HART] |
| `overall_width_m` | 6 m | 8–12 m | 16 m | [HART] |
| `overall_length_m` | 12 m | 15–30 m | 45 m | [HART] |

### 4.3 Vertikale Maße

| Parameter | Minimalwert | Normalbereich | Maximalwert | Evidenz |
|---|---|---|---|---|
| `eaves_height_m` | 2,0 m | 2,2–2,8 m | 3,2 m | [MITTEL] |
| `first_height_m` | 6,5 m | 7–10 m | 12 m | [HART] |
| `roof_pitch_deg` | 40° | 45–55° (Reet/Stroh steiler) | 65° | [MITTEL] |
| `inner_post_height_m` | 3,5 m | 4,0–6,0 m | 8,0 m | [MITTEL] |

### 4.4 Wandraster und Öffnungen

| Parameter | Minimalwert | Normalbereich | Maximalwert | Evidenz |
|---|---|---|---|---|
| `stud_spacing_m` | 0,6 m | 0,9–1,2 m | 1,5 m | [MITTEL] |
| `gefach_width_m` | 0,6 m | 0,9–1,5 m | 2,0 m | [MITTEL] |
| `door_width_m` | 0,7 m | 0,8–1,2 m | 1,6 m | [MITTEL] |
| `gate_width_m` | 1,8 m | 2,0–3,5 m | 4,5 m | [MITTEL] |
| `window_sill_z_m` | 0,6 m | 0,7–1,0 m | 1,2 m | [MITTEL] |
| `lintel_z_m` | 1,6 m | 1,8–2,2 m | 2,4 m | [MITTEL] |

### 4.5 Querschnitte der Haupthölzer

| Element | Normalbereich | Evidenz |
|---|---|---|
| Innenständer (Hauptpfosten) | 20×20–30×30 cm | [HART] |
| Außenwandständer | 16×16–22×22 cm | [MITTEL] |
| Ankerbalken (tie beam) | 18×24–25×30 cm | [HART] |
| Deckenbalken | 16×20–22×26 cm | [MITTEL] |
| Pfetten | 18×22–24×28 cm | [MITTEL] |
| Sparren | 12×16–16×20 cm | [MITTEL] |
| Schwelle | 18×20–22×24 cm | [MITTEL] |

Extremwert: Cressing Temple Barns (1205d/1235d), Hauptständer ca.
30×25 cm. **[HART]**

---

## 5. Dachsystemlogik

Für BVILLAGE ist das Dachsystem kein Blender-Parameter, sondern ein
Grammar-Parameter, der Statik und FramePlan bestimmt.

### 5.1 Sparrendach (rafter_pairs)

Sparrenpaare tragen Last direkt in Querrahmen / Rähm. Tie-beam /
Kehlbalken stabilisieren gegen Spreizen. Geeignet für kleinere
Spannweiten oder zusätzliche Stützen. Pro Bay kann ein Sparrenpaar-Muster
entstehen.

### 5.2 Kehlbalkendach (collar)

Kehlbalken reduziert Sparrenspreizung, erlaubt höhere Dachräume.
Beeinflusst Innenraum (Loft) und Öffnungslogik. BVILLAGE: Kehlbalken
ist member-Klasse mit `collar_height_ratio` als Policy-Parameter.

### 5.3 Pfettendach (purlin)

Pfetten laufen längs und werden von Ständerreihen / Innenstützen getragen.
Verteilt Lasten entlang der Längsachse. Passt primär zur Hall/Aisled-Grammar:
„tie beams / purlins → interior supports" (BVILLAGE-Projektdefinition).

BVILLAGE: Pfetten sind longitudinale members und brauchen regelmäßige
Auflager (Frames oder Ständerreihen). Sie bestimmen, wo stiff frames
sinnvoll sind.

### 5.4 Mischsysteme

Historisch plausibel (Übergänge, regionale Praktiken). BVILLAGE:
`roof_system = mixed` als kontrollierte Variante, nicht als Zufall.

| Dachsystem | Typische Spannweite | Regionale Tendenz | Evidenz |
|---|---|---|---|
| Sparrendach | bis 8 m | Universell, früh | [MITTEL] |
| Kehlbalkendach | 6–12 m | Norddeutsch | [MITTEL] |
| Pfettendach | 8–18 m | Norddeutsch, Hallenhaus | [MITTEL] |

---

## 6. Bay-Logik und Endzonen

### 6.1 Bay als Längenmodul

Ein Hallenhaus wird als „N Bays" gebaut. Die Bay-Sprache ist in England
explizit (3-bay house, 4-bay house) und in Deutschland implizit in der
Binderfolge. **[MITTEL]**

BVILLAGE: `bay_width[i]` ist eine Range, nicht konstant. Variation ist
klein und seed-deterministisch. Harte Constraint: Anschlussfähigkeit Dach /
Pfettenlauf.

### 6.2 Endzonen

Reale Häuser haben Endbereiche, die nicht als voller Bay funktionieren:
Giebelabschluss, Vorzone am Tor, rückseitige Arbeits-/Lagervorzone.

BVILLAGE-Regel:
- `end_zone_depth = bay_width × k`, mit `k ∈ [0.3, 0.7]` (Policy)
- `end_zone_kind`: `gable_wall_only` | `end_frame` | `gate_end_frame`

---

## 7. Wand- und Gefachlogik

### 7.1 Wand als System

Außenwand besteht aus: Schwelle (Sohlholz) → Wandständer (Raster) →
Riegel (horizontale Bänder) → Rähm → Gefache (Füllfelder).

### 7.2 Vertikale Riegel-Ebenen (parametrisierbar)

| Ebene | Zweck | BVILLAGE-Rolle |
|---|---|---|
| `sill` (z=0) | Unterster Abschluss | `rail role=sill` |
| `mid_rail` (Brüstungsriegel) | Arbeitsriegel, Fensterunterkante | `rail role=sill_rail` |
| `lintel_rail` (Sturzriegel) | Fenstersturz | `rail role=lintel` |
| `wall_plate` (Rähm/Traufe) | Oberer Abschluss | `rail role=top_rail` |

Öffnungen binden an Riegelebenen: Fenster zwischen Brüstung und Sturz;
Türen/Tore brauchen Sturz-member.

---

## 8. Aussteifungslogik

### 8.1 Problem

Holzrahmen müssen gegen Windlast quer, Windlast längs, Verformung beim
Aufrichten und Racking (Scheren) in Wandfeldern ausgesteift werden.

### 8.2 Bracing-Elemente

- **Kopfbänder**: Knotensteifigkeit (Ständer↔Rähm / Ständer↔Balken)
- **Wanddiagonalen**: Aussteifung in Längsrichtung
- **Rahmendiagonalen**: Verstärkung einzelner Frames (stiff frames)

### 8.3 Bracing-Regeln

- Mindestens ein aussteifendes Bay pro N Bays (Policy: `bracing_period`)
- Keine Strebe durch Tor / Fenster
- Bracing bevorzugt symmetrisch, aber nicht zwingend
- Stiff frame nahe Tor und/oder nahe Endzonen historisch plausibel

Bracing ist deterministisch (seed). Bracing hat Keep-out-Zonen für Öffnungen.

---

## 9. Öffnungslogik

### 9.1 Torlage bestimmt Eingriffsebene

- **Giebeltor**: Tor im Endrahmen → `SPECIAL_GATE_FRAME`
- **Längstor**: Tor im Bay zwischen zwei Frames → Wandraster-Eingriff

### 9.2 Konstruktionspflichten bei Öffnungen

Für jede Öffnung zwingend:
- Torpfosten (jamb posts) als tragende members
- Sturz (lintel) als member
- Bracing muss Öffnung freihalten

**BVILLAGE Hard Rules:**
- Keine Öffnung ohne `jamb + lintel + Anschlüsse`
- Bracing darf Öffnungen nicht schneiden
- Tore brauchen zusätzliche Aussteifung (Policy: `gate_reinforcement_level`)

---

## 10. Raumlogik

### 10.1 Basiszonen

Der Hallenhaus-Innenraum gliedert sich in Zonen, nicht in Zimmer:

| Zone | Lage | Funktion |
|---|---|---|
| Diele / Halle | Zentral, Längsachse | Dreschtenne, Durchfahrt für Erntewagen |
| Stallzone | Seitenschiffe | Tiere, Stallboxen |
| Hochlager | Über Stallzonen | Heu- und Strohlager |
| Wohnzone (Flett) | Hinterer Teil, manchmal seitlich | Herdstelle, Schlafbereich |
| Kammern | An der Rückwand | Vorratshaltung, kleine Schlafräume |

Das Erleben eines Hallenhauses — Diele und Flett ohne trennende Zwischenwände —
ist der typische Eindruck in musealen Rekonstruktionen. **[MITTEL]**

### 10.2 Abgrenzung der Zonen

Primär: durch Ständerreihen (Support rows).
Sekundär: durch leichte Innenwände (Bohlen-/Fachwerkwände) und Einbauten.

BVILLAGE: `InteriorPlanner` erzeugt Zones (topologisch, tragwerkskompatibel)
und optional Partitions (nicht tragend, später modifizierbar).

---

## 11. Bauprozess → BVILLAGE-Pipeline

### 11.1 Material als frühester Constraint

Zimmermannslogik beginnt vor Geometrie: verfügbare Holzdimensionen,
Qualität, Geradwuchs und Feuchte bestimmen maximale Spannweiten,
notwendige Ständerreihen, `bay_width`-Korridor und Dachsystemwahl.

`Policy(material + epoch_band + region) → structural_capabilities → Architect(FramePlan)`

### 11.2 Montagereihenfolge (historisch → Pipeline)

1. Schwellen / Auflager
2. Erster stabiler Rahmen (Binder)
3. Rahmenserie (Binderfolge)
4. Längsverbindungen
5. Dachtragwerk
6. Aussteifung finalisieren

BVILLAGE: Der Architect muss ein Skelett liefern, das sich logisch stellen
lässt. Frames sind diskrete Einheiten. Längsverbindungen sind explizite
members. Bracing ist explizit, keine Blender-Heuristik.

---

## 12. FramePlan-Spezifikation

### 12.1 Inputs (Policy + Context)

```python
@dataclass(slots=True)
class HallGrammarInput:
    cross_section_type: int        # 2 | 3 | 4
    bay_count: int
    bay_width_range: tuple[float, float]
    end_zone_kind_front: str       # "gable_wall_only" | "end_frame" | "gate_end_frame"
    end_zone_kind_rear: str
    entrance: str                  # "gable_gate" | "side_gate" | "none"
    roof_system: str               # "rafter_pair" | "collar" | "purlin" | "mixed"
    bracing_density: str           # "low" | "medium" | "high"
    material_capabilities: dict    # span limits, section ranges
```

### 12.2 Output (FramePlan — kanonisch)

```python
@dataclass(slots=True)
class FramePlan:
    frames: list       # u_position, FrameRole, support_row_layout
    members: list      # posts, beams, plates, braces, purlins, rafters, collars
    openings: list     # resolved + constraints + structural parts
    cells: list        # Gefache als explizite Rasterzellen (optional)
```

### 12.3 Hard Invariants (Fehler = Abbruch)

- Members-first: keine Ableitung im Builder
- Öffnung ohne `jamb + lintel` verboten
- Bracing darf Öffnungen nicht schneiden
- Support rows gemäß `cross_section_type` müssen konsistent sein
- Determinismus: gleicher Seed → identisches FramePlan

---

## 13. Hallenbau-Familie gesamt

| ID | Name | Innenreihen | Gesamtbreite | Besonderheit | Epoche |
|---|---|---|---|---|---|
| `FW-LH-ND` | Niederdeutsches Hallenhaus (Dreiständer) | 2 | 10–14 m | Leittyp; Diele zentral | 13.–19. Jh. |
| `FW-LH-2S` | Zweiständerhaus | 2 | 6–10 m | Kleines System | 15.–18. Jh. |
| `FW-LH-3S` | Dreiständer asymmetrisch | 2 | 8–12 m | Asymmetrische Seitenschiffe | 16.–18. Jh. |
| `FW-LH-4S` | Vierständerhaus | 4 | 12–18 m | Zwei Mittelschiffe | 16.–19. Jh. |
| `FW-GULF` | Gulfhaus | 1 zentral | 14–20 m | Gulf bis 12 m hoch | 16.–19. Jh. |
| `FW-HAUB` | Haubarg | Umgebinde | 18–24 m | Quadratischer Grundriss; allseitiger Walm | 17.–19. Jh. |
| `GH-GEEST` | Geesthardenhaus | 0 | 8–12 m | Keine Innenständer; quergeteilte Räume | 17.–19. Jh. |
| `ENG-AISL` | Aisled Frame (englisch) | 2 | 10–16 m | Scheunentypus; Cressing Temple | 13.–15. Jh. |

> **[AUSSTEHEND]** `FW-GULF` und `FW-HAUB`: Klassifikation als eigenständiger
> `archetype` oder `policy_variant` von `FW-LH-ND` ist nicht entschieden.
> Primärquellen zu Spannweiten und Stützenlogik fehlen.
> Siehe `RES_ARCHETYPE_SONDERFAELLE.md`.

---

## 14. Kanonische Bestände

| Ort | Bestand | Evidenzwert |
|---|---|---|
| Freilichtmuseum Detmold (Westfälisches Freilichtmuseum) | Vollständige Hallenhäuser verschiedener Epochen, abgebaut und wieder aufgebaut | Primär |
| Museumsdorf Cloppenburg | Zwei- und Vierständerhäuser | Primär |
| Schleswig-Holsteinisches Freilichtmuseum Kiel-Molfsee | Norddeutsche Hallenhäuser | Primär |
| Cressing Temple, Essex (1205d/1235d) | Barley Barn + Wheat Barn; älteste erhaltene Holzrahmenscheunen Europas | **[HART]** |
| Weald & Downland Living Museum, Chichester | Bayleaf Farmhouse (ca. 1405) | Primär (englisch) |

---

## 15. QA-Checkliste: „Ist das ein Zimmermanns-Hallenhaus?"

1. Kann man die Binderfolge „stellen" (montagefähig)?
2. Ist die Bay-Logik als Modul erkennbar (keine willkürlichen Längen)?
3. Ist das Dachsystem strukturell konsistent zu den Support Rows?
4. Gibt es Aussteifung in Längs- und Querrichtung?
5. Sind Tore/Fenster konstruktiv aufgelöst (jamb / lintel / rails)?
6. Stimmen die Maßbereiche zur Policy (region / epoch_band / wealth)?
7. Entsteht Raum als Zone um Ständerachsen (nicht als moderner freier Grundriss)?

---

## 16. Offene Forschungsfelder

| ID | Thema | Status | Zieldokument |
|---|---|---|---|
| HAL-001 | Region/Epoche-spezifische Maßverteilungen aus VAG-Dendrodaten (nicht nur Ranges) | Laufend | Dieses Dokument §4 |
| HAL-002 | Dachsysteme: regionale Dominanzen (Pfetten vs. Sparren) für norddeutschen Raum | Unvollständig | `RES_DACHSYSTEME.md` |
| HAL-003 | Bracing-Pattern-Cluster: häufige Muster aus Bauaufnahme-Korpora | Unvollständig | `RES_KONSTRUKTION_ALLGEMEIN.md` §9 |
| HAL-004 | Gulfhaus (FW-GULF): Konstruktionslogik aus Primärquellen (Spannweiten, Stützenlogik) | Forschungslücke | `RES_ARCHETYPE_SONDERFAELLE.md` |
| HAL-005 | Haubarg (FW-HAUB): Primärquellen zur Vierkant-Konstruktion | Forschungslücke | `RES_ARCHETYPE_SONDERFAELLE.md` |
| HAL-006 | `cross_section_type = 2` vs. `= 3`: Grenzkriterien für Archetype-Zuweisung | Konzeptuell offen | ARCH_TAXONOMY.md |
| HAL-007 | Epochenvalidierung für Maßbereiche (13.–15. Jh.): keine erhaltenen Bauten → SOFT Issues definieren | Offen | PhysicalPlausibilityValidator |

---

## 17. Quellen

**Hewett, Cecil A.:** Structural Carpentry in Medieval Essex. Building
Archaeology. URL: https://www.buildingarchaeology.org/wp-content/uploads/2015/03/Structural-Carpentry-Hewett.pdf
*BAY definiert als Abschnitt zwischen zwei transverse frames. Grundlage
für BVILLAGE-Terminologie.*

**Klein, Ulrich:** Zum aktuellen Forschungsstand des hoch- und
spätmittelalterlichen Holzbaus in Deutschland. DGAMN-Mitteilungen Bd. 24.
Paderborn 2012. DOI: https://doi.org/10.11588/dgamn.2012.1.17131
*Älteste erhaltene Hallenhäuser: ausgehendes 15. Jahrhundert.*

**Stiewe, Heinrich:** Fachwerkhäuser in Deutschland. 2007.
URL (DNB): https://d-nb.info/984870083/04
*Ständer, Riegel, Balken, Bauprozess, Grundformen.*

**Brunskill, R. W.:** Traditional Buildings of Britain. Frame-and-bay
Logik im timber framing.

**IgB (Interessengemeinschaft Bauernhaus):** In großen Hütten, die man
Häuser nennt. PDF mit Literaturhinweisen Bedal/Baumgarten.
URL: https://www.igbauernhaus.de/de-wAssets/docs/Projekte-und-Aktionen/Hallenhaus_Stiewe.pdf

Freilichtmuseum Detmold. Museumsdorf Cloppenburg.
Schleswig-Holsteinisches Freilichtmuseum Kiel-Molfsee.

---

*Status: Freigegeben als REFERENCE-Dokument. Version 1.0.*
*© 2026 Alexander Bernardi — CC-BY-SA 4.0*
