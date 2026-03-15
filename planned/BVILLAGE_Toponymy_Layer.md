# BVILLAGE – Toponymy Layer

---
tier: planned
authority: SPECIFICATION
status: elaborated — not yet implemented
change-rule: Änderungen erfordern explizite Entscheidung. Terminologie folgt SYS_CONCEPTS.md und ARCH_BAUGRAMMATIKEN_WISSENSCHAFT.md.
referenced-by: —
references: SYS_VISION.md §2–3, ARCH_MATERIALS.md §2, SYS_CONCEPTS.md §2
---

Dieses Dokument spezifiziert den **Toponymy Layer** — die Datenschicht, die
historisch plausible Siedlungs- und Ortsnamen für BVILLAGE erzeugt.

Es ist kein eigenständiges Subsystem. Es ist ein CultureMap-Layer, der über
den bestehenden spatiotemporalen Lookup-Mechanismus abgefragt wird und dessen
Datenschemas und Gewichtungslogik hier festgelegt werden.

---

## 1. Einordnung ins System

### 1.1 Kein neues Subsystem

Der Toponymy Layer führt keine neue Engine ein. Er nutzt den in `SYS_VISION.md §3`
definierten Lookup-Mechanismus:

```
query(lon, lat, year, layer) → [(candidate, score), ...]
```

Ein Ortsname ist ein Kandidat wie ein Holzartenname oder ein Herrschaftstitel.
Der Mechanismus ist identisch. Nur die Datenschicht `"toponym.settlement"` ist neu.

Neue Datendateien liegen in `data/culturemap/toponym/`.
Der Resolver ist unverändert.

### 1.2 Position in der Fünf-Ebenen-Hierarchie

Der Toponymy Layer operiert auf **Settlement-Ebene**. Er empfängt aufgelöste
Kontextparameter aus dem `SettlementPlan` und gibt einen kanonischen Namen zurück.

```
Landscape
  └── Region
        └── Cultural zone
              └── Settlement  ← Toponymy Layer greift hier ein
                    └── Plot
                          └── Building
```

Der Settlement-Name wird einmalig beim Erzeugen des `SettlementPlan` aufgelöst.
Er verändert sich danach nicht. Er ist ein Attribut des `SettlementPlan`, kein
dynamischer Parameter.

### 1.3 Deterministik

Die Namensauflösung ist vollständig deterministisch. Gleicher Seed + gleicher
Kontext = immer identischer Name. Der Seed fließt in alle gewichteten
Auswahlschritte ein. Stochastisches Sampling ist verboten.

---

## 2. Kernthese: Ortsnamen als stratigraphische Systeme

Ein historisch plausibler Ortsname ist keine Zufallskombination aus Präfix
und Suffix. Er ist verdichtete historische Information. Er trägt Spuren von:

- **Raum** — Sprachraum, Dialektraum, Herrschaftsraum, Kontaktzone
- **Zeit** — Siedlungsphase, Rodungsphase, Stadtgründungsphase
- **Semantik** — Gründer, Besitz, Topographie, Vegetation, Gewässer, Funktion
- **Kulturlogik** — regionale Personennamen, kirchliche und herrschaftliche Prägung

Die Generierungsformel lautet daher nicht:

```
beliebiges Bestimmungswort + beliebiges Grundwort
```

sondern:

```
Toponym = f(region, epoch, culture, settlement_function, landscape, local_lexicon)
```

In Systemterminologie:

```
query("toponym.settlement", context) → weighted_candidates → derive_toponym(seed)
```

---

## 3. Kontextmodell

Der Toponymy Layer empfängt einen `ToponymContext`. Dieser wird aus dem
`SettlementPlan` und dem aufgelösten `CultureMap`-Kontext zusammengestellt.

### 3.1 Pflichtfelder

```python
@dataclass
class ToponymContext:
    lon: float
    lat: float
    year: int
    region: str                  # geophysikalische Region, stabil über Epochen
    culture: str                 # CultureMap-Zone (epoch-dependent)
    settlement_type: str         # village | town | hamlet | borough | monastery
    settlement_function: str     # agrarian | trade_crossing | clearing |
                                 # market | fortress | ecclesiastical
    landscape: str               # valley | hilltop | river_terrace | forest_edge |
                                 # plain | wetland | mountain_slope
    seed: int
```

### 3.2 Optionale Felder

```python
    vegetation_zone: str | None  # beech_forest | oak_forest | mixed | pine | riparian
    hydrology: str | None        # major_river | minor_river | stream | lake | ford
    founder_class: str | None    # local_elite | church | nobility | free_settlers
    frontier_status: bool        # Kontaktzone / Grenzraum
    contact_language: str | None # slavic | romance | frisian | danish
    urbanity_level: float | None # 0.0–1.0
    ecclesiastical_influence: float | None  # 0.0–1.0
```

Optionale Felder, die nicht gesetzt sind, beeinflussen die Gewichtung nicht.
Sie öffnen keine Fallback-Pfade — sie sind schlicht inaktiv.

---

## 4. Datenschemas

### 4.1 MorphemeEntry — `data/culturemap/toponym/morphemes.yaml`

Jedes produktive Morphem trägt vollständige Metadaten.

```yaml
rode:
  type: suffix           # suffix | prefix | standalone
  semantics: clearing    # semantische Klasse (→ §5)
  epoch_band: [900, 1300]
  regions:
    - central_europe
    - bavaria
    - thuringia
    - saxony
  settlement_types:
    - village
    - clearing_settlement
  settlement_functions:
    - clearing
    - agrarian
  weight: 0.70
  confidence: core       # core | halo
  variants:              # regionale Lautvarianten
    - roda
    - roth
    - rath

reuth:
  type: suffix
  semantics: clearing
  epoch_band: [1050, 1350]
  regions:
    - bavaria
    - franconia
    - upper_palatinate
  settlement_types:
    - village
    - clearing_settlement
  settlement_functions:
    - clearing
    - agrarian
  weight: 0.75
  confidence: core
  variants:
    - reuth
    - reute
    - reith

heim:
  type: suffix
  semantics: early_settlement
  epoch_band: [500, 950]
  regions:
    - rhineland
    - franconia
    - swabia
    - alemannia
  settlement_types:
    - village
    - hamlet
  settlement_functions:
    - agrarian
    - founding_estate
  weight: 0.65
  confidence: core

burg:
  type: suffix
  semantics: fortified_settlement
  epoch_band: [800, 1400]
  regions:
    - all
  settlement_types:
    - borough
    - town
  settlement_functions:
    - fortress
    - market
  weight: 0.60
  confidence: core

furt:
  type: suffix
  semantics: river_crossing
  epoch_band: [700, 1300]
  regions:
    - rhineland
    - central_europe
    - saxony
  settlement_types:
    - village
    - town
  settlement_functions:
    - trade_crossing
  weight: 0.75
  confidence: core
  hydrology_requirement: [major_river, minor_river, ford]

itz:
  type: suffix
  semantics: slavic_settlement
  epoch_band: [800, 1300]
  regions:
    - silesia
    - lusatia
    - pomerania
    - bohemia_border
  settlement_types:
    - village
  settlement_functions:
    - agrarian
  weight: 0.80
  confidence: core
  contact_language_requirement: slavic
```

Das Schema ist erweiterbar. Neue Einträge folgen demselben Format.
Felder ohne Wert werden als inaktiv behandelt — kein Fallback, keine Standardannahme.

---

### 4.2 RegionalLexicon — `data/culturemap/toponym/lexicon_<region>.yaml`

Regionale Lexika sind nach Makroregion aufgeteilt. Jeder Eintrag trägt
semantische Klasse, Epochenband und Gewichtung.

Dateinamen-Konvention: `lexicon_bavaria.yaml`, `lexicon_rhineland.yaml`,
`lexicon_saxony.yaml`, `lexicon_silesia.yaml` usw.

```yaml
# lexicon_bavaria.yaml

person_names:
  - form: Adal
    epoch_band: [600, 1000]
    weight: 0.70
    confidence: core
  - form: Arn
    epoch_band: [700, 1100]
    weight: 0.65
    confidence: core
  - form: Konrad
    epoch_band: [900, 1300]
    weight: 0.55
    confidence: core
  - form: Ulrich
    epoch_band: [1000, 1350]
    weight: 0.50
    confidence: core
  - form: Percht
    epoch_band: [800, 1200]
    weight: 0.40
    confidence: halo

plant_names:
  - form: Buchen
    vegetation_zones: [beech_forest, mixed]
    weight: 0.80
    confidence: core
  - form: Linden
    vegetation_zones: [mixed, oak_forest]
    weight: 0.70
    confidence: core
  - form: Eichen
    vegetation_zones: [oak_forest, mixed]
    weight: 0.75
    confidence: core
  - form: Erlen
    vegetation_zones: [riparian]
    weight: 0.65
    confidence: core

topography_terms:
  - form: Stein
    landscape: [hilltop, mountain_slope, rocky]
    weight: 0.70
  - form: Berg
    landscape: [hilltop, mountain_slope]
    weight: 0.65
  - form: Tal
    landscape: [valley]
    weight: 0.75
  - form: Au
    landscape: [river_terrace, wetland, riparian]
    weight: 0.70

hydronyms:
  - form: Bach
    hydrology: [stream, minor_river]
    weight: 0.80
  - form: See
    hydrology: [lake]
    weight: 0.70
  - form: Regen       # regionaler Flussname als Präfix-Quelle
    hydrology: [major_river]
    weight: 0.60
    confidence: halo

ecclesiastical_lexemes:
  - form: Münster
    ecclesiastical_influence_min: 0.6
    weight: 0.55
  - form: Kirchen
    ecclesiastical_influence_min: 0.3
    weight: 0.45
```

---

### 4.3 GrammarRules — `data/culturemap/toponym/rules_<region>.yaml`

Regelmengen definieren, welche semantischen Klassen mit welchen Morphemklassen
kombinierbar sind. Regeln sind regional und zeitlich begrenzt.

```yaml
# rules_bavaria.yaml

rules:

  - id: person_early_settlement
    pattern: [person_name, early_settlement_suffix]
    allowed_regions: [bavaria, franconia, swabia, rhineland]
    epoch_band: [500, 950]
    settlement_functions: [agrarian, founding_estate]
    weight: 0.80

  - id: plant_clearing
    pattern: [plant_name, clearing_suffix]
    allowed_regions: [bavaria, franconia, thuringia, saxony]
    epoch_band: [900, 1350]
    settlement_functions: [clearing, agrarian]
    weight: 0.85

  - id: topography_settlement
    pattern: [topography_term, settlement_suffix]
    allowed_regions: [all]
    epoch_band: [600, 1400]
    settlement_functions: [agrarian, trade_crossing, fortress]
    weight: 0.60

  - id: hydronym_crossing
    pattern: [hydronym, crossing_suffix]
    allowed_regions: [all]
    epoch_band: [700, 1300]
    settlement_functions: [trade_crossing]
    hydrology_requirement: [major_river, minor_river, ford]
    weight: 0.75

  - id: function_urban
    pattern: [function_term, urban_suffix]
    allowed_regions: [all]
    epoch_band: [1000, 1400]
    settlement_types: [town, borough]
    settlement_functions: [market, trade_crossing, fortress]
    weight: 0.70

  - id: ecclesiastical
    pattern: [ecclesiastical_lexeme, settlement_suffix]
    allowed_regions: [all]
    epoch_band: [700, 1400]
    settlement_functions: [ecclesiastical]
    ecclesiastical_influence_min: 0.4
    weight: 0.65
```

---

## 5. Semantische Klassen

Die semantischen Klassen sind die Verbindungsschicht zwischen `settlement_function`,
`landscape`, `vegetation_zone` und den Morphem-Lexika. Sie sind keine freien Tags,
sondern ein geschlossenes Vokabular.

| Klasse | Bedeutungsfeld | Typische Morpheme |
|---|---|---|
| `early_settlement` | Sippe, Hof, frühe Ansiedlung | -heim, -ingen, -dorf, -hausen |
| `clearing` | Rodung, Neusiedlung im Wald | -rode, -reuth, -rath, -schwand |
| `agrarian` | Feld, Feldlage, Bauernsiedlung | -feld, -au, -wiesen |
| `river_crossing` | Furt, Brücke, Flussübergang | -furt, -brück, -au |
| `fortified_settlement` | Burg, befestigter Ort | -burg, -berg, -stein |
| `market` | Markt, städtische Funktion | -markt, -stadt, -neustadt |
| `ecclesiastical` | Kirche, Kloster, Patrozinium | -münster, -kirchen, -zell |
| `slavic_settlement` | Slawische Schicht, Kontaktzone | -itz, -ow, -in, -witz |
| `person_founding` | Gründer- / Besitzername | Personenname als Determinans |

Neue Klassen dürfen nur durch explizite Entscheidung hinzugefügt werden.
Keine implizite Erweiterung durch Dateieinträge.

---

## 6. Auflösungspipeline

Die Namensauflösung folgt einer geordneten Pipeline. Jeder Schritt hat
genau eine Aufgabe. Kein Schritt greift in den nächsten ein.

```
ToponymContext
  → 1. Regelauswahl         — welche GrammarRules sind für Raum/Zeit/Funktion aktiv?
  → 2. Morphemgewichtung    — welche Suffixe und Präfixklassen sind plausibel?
  → 3. Lexemauswahl         — welche regionalen Lexeme passen zur aktiven Klasse?
  → 4. Kombinationsauswahl  — seeded Auswahl aus gewichteten Kandidaten
  → 5. Phonologische Form   — Fugenbildung, Vokalglättung (→ §7)
  → 6. Kanonischer Name     — Ausgabe an SettlementPlan
```

### Schritt 1 — Regelauswahl

Alle `GrammarRules` werden gegen den `ToponymContext` geprüft:

- Liegt `year` im `epoch_band`?
- Liegt `region` in `allowed_regions`?
- Passt `settlement_function`?
- Sind optionale Anforderungen (`hydrology_requirement`, `ecclesiastical_influence_min`) erfüllt?

Ergebnis: eine gewichtete Liste aktiver Regeln.

### Schritt 2 — Morphemgewichtung

Für jede aktive Regel werden passende Morpheme aus `morphemes.yaml` geladen.
Die Morphem-Gewichtung wird mit dem Regel-Gewicht multipliziert.
`core`-Morpheme erhalten Faktor 1.0, `halo`-Morpheme Faktor 0.5.

### Schritt 3 — Lexemauswahl

Das Determinans (Präfix) wird aus dem regionalen Lexikon gezogen.
Die semantische Klasse der aktiven Regel bestimmt, aus welchem Lexikon-Abschnitt
gewählt wird. Optionale Felder (`vegetation_zone`, `hydrology`, `landscape`) schärfen
die Gewichtung.

### Schritt 4 — Kombinationsauswahl

Aus den gewichteten Kandidaten-Paaren (Determinans + Grundwort) wird
**seeded deterministisch** ein Paar ausgewählt. Mehrere Kandidaten können
für Varianten-Ausgabe behalten werden.

### Schritt 5 — Phonologische Form

Minimale Regelmenge (→ §7). Kein Schritt ohne explizite Regel. Kein Fallback.

### Schritt 6 — Ausgabe

Der kanonische Name wird als `str` an den `SettlementPlan` übergeben.
Optional: Liste historischer Varianten als `list[str]`.

---

## 7. Phonologie und Orthographie

Für die erste Implementierung genügt eine begrenzte, explizite Regelmenge.
Vollständige historische Lautentwicklung ist explizit außerhalb des Scope.

### 7.1 Minimalregeln

**Fugen-s**
Zwischen bestimmten Determinantia und Grundwörtern wird ein Fugen-s eingeschoben.

```
Konrad + dorf   → Konradsdorf
Karl   + heim   → Karls-heim   (historisch: Karlsheim)
```

Regeln sind als explizite Liste gespeichert, nicht inferiert.

**Vokalglättung**
Aufeinandertreffende gleiche Vokale werden zu einem reduziert.

```
Erle + en + au  → Erlenau  (kein Erlenau→Erleau)
```

**Endungsreduktion**
Determinantia enden im toponymischen Kontext häufig auf -en statt auf -e.

```
Buche  → Buchen-reuth
Linde  → Linden-rode
Eiche  → Eichen-bach
```

### 7.2 Variantenbildung

Für jeden generierten Namen können historische Varianten ausgegeben werden,
die auf `morphemes.yaml → variants` basieren.

```
Buchenreuth → [Buchenreuth, Buchenroda, Buchreuth]
```

Diese Varianten sind Ausgabe, nicht Eingabe in weitere Verarbeitung.

---

## 8. Konfidenzmodell

Das Konfidenzmodell folgt dem in `ARCH_MATERIALS.md §2` definierten Schema.

| Konfidenz | Score | Bedeutung |
|---|---|---|
| `core` | 1.0 | Morphem / Lexem ist für Region und Epoche gut belegt |
| `halo` | 0.5 | Morphem / Lexem ist plausibel, aber dünn belegt |
| kein Eintrag | 0.0 | Keine Plausibilitätsbasis — nicht verwendet |

Score 0.0-Kandidaten werden aus der Auswahl ausgeschlossen.
`halo`-Kandidaten sind wählbar, haben aber gegenüber `core`-Kandidaten
systematisch niedrigere Gesamtgewichtung.

---

## 9. Fehlerverhalten

Das Fehlerverhalten folgt `SYS_CONTRACT.md`. Keine stillen Fallbacks.

| Situation | Verhalten |
|---|---|
| Keine aktive Regel für Kontext | HARD Issue — kein Name generiert |
| Alle Morphem-Scores 0.0 | HARD Issue — kein Name generiert |
| Seed fehlt | HARD Issue — kein Aufruf ohne Seed erlaubt |
| Lexikon für Region nicht vorhanden | HARD Issue — kein Fallback auf Generallexikon |
| `contact_language_requirement` nicht erfüllt | Regel inaktiv — kein Fehler |

Ein fehlender Name ist ein strukturelles Signal, keine lästige Ausnahme.
Er zeigt, dass der Kontext unvollständig ist oder eine Datenlücke besteht.

---

## 10. Kontaktzonen

Deutsch-slawische und andere Kontaktzonen erfordern eine eigene Logik.
Sie werden nicht durch einen einzelnen `allowed_regions`-Eintrag abgedeckt.

### 10.1 Kontaktzonenregel

Wenn `frontier_status: true` und `contact_language` gesetzt:

- Regeln beider Sprachschichten werden geladen
- Slawische Morpheme erhalten ihre eigene Gewichtung aus `morphemes.yaml`
- Mischformen sind explizit als eigene Regelklasse modellierbar

```yaml
  - id: slavic_german_hybrid
    pattern: [slavic_stem, german_suffix]
    allowed_regions: [silesia, lusatia, pomerania, bohemia_border]
    epoch_band: [950, 1300]
    contact_language_requirement: slavic
    frontier_status_required: true
    weight: 0.60
```

### 10.2 Sprachschichten-Priorisierung

In Kontaktzonen gilt keine automatische Präferenz für eine Schicht.
Die Gewichtung entscheidet. Sie spiegelt die historische Dominanz wider,
die in den Datendateien abgebildet ist.

---

## 11. Notwendige Datendateien (Minimum Viable Data)

Für eine erste funktionsfähige Implementierung werden mindestens benötigt:

| Datei | Inhalt |
|---|---|
| `data/culturemap/toponym/morphemes.yaml` | Suffixe und Grundwörter mit Metadaten |
| `data/culturemap/toponym/lexicon_bavaria.yaml` | Regionales Lexikon Bayern |
| `data/culturemap/toponym/lexicon_rhineland.yaml` | Regionales Lexikon Rheinland |
| `data/culturemap/toponym/lexicon_saxony.yaml` | Regionales Lexikon Sachsen |
| `data/culturemap/toponym/rules_central_europe.yaml` | Übergreifende Regelmengen |
| `data/culturemap/toponym/rules_bavaria.yaml` | Bayerische Regelmengen |
| `data/culturemap/toponym/phonology_mhg.yaml` | Phonologische Minimalregeln (mittelhochdeutsch) |

Diese Dateien sind Voraussetzung für den ersten Testlauf.
Weitere Regionen werden nach identischem Schema ergänzt.

---

## 12. Systemintegration

### 12.1 Anbindung an SettlementPlan

```python
@dataclass
class SettlementPlan:
    ...
    toponym: str                        # kanonischer Name
    toponym_variants: list[str]         # historische Varianten, optional
    toponym_context: ToponymContext     # für Audit und Reproduzierbarkeit
```

### 12.2 Aufruf

```python
# In der Settlement-Planungslogik:
context = ToponymContext(
    lon=lon, lat=lat, year=year,
    region=resolved_region,
    culture=resolved_culture,
    settlement_type=plan.settlement_type,
    settlement_function=plan.settlement_function,
    landscape=plan.landscape,
    seed=plan.seed,
    # optionale Felder aus aufgelöstem Kontext:
    vegetation_zone=plan.vegetation_zone,
    hydrology=plan.hydrology,
)
toponym, variants = derive_toponym(context)
```

### 12.3 Modulverortung

```
bvillage/domains/settlement/core/derive_toponym.py
```

Rollenpräfix `derive_` — korrekt: erzeugt ein deterministisches Artefakt
aus gegebenem Kontext. Kein Blender-Import. Keine Seiteneffekte.

---

## 13. Abgrenzung: Was dieser Layer nicht tut

- **Keine Straßennamen**, Flurnamen oder Hausnamen — eigene zukünftige Layer
- **Keine diachrone Namensentwicklung** — Umbenennungen durch Herrschaftswechsel sind außerhalb des Scope
- **Keine Latinisierungen** — Urkundenformen sind Ausgabe-Varianten, keine Generierungslogik
- **Keine Eigennamen für Personen** — Personennamen sind Determinantia, keine Ausgabe
- **Keine vollständige Lautgeschichte** — Phonologie bleibt auf Minimalregeln beschränkt
- **Keine freie Namenserfindung** — jeder generierte Name hat eine nachvollziehbare historische Regelgrundlage

---

## 14. Erweiterungsachsen

Das System ist erweiterbar ohne Architekturänderungen. Neue Schichten
kosten lediglich neue Datendateien und Regeleinträge.

| Erweiterung | Mechanismus |
|---|---|
| Neue Region | Neue `lexicon_<region>.yaml` + Einträge in `morphemes.yaml` |
| Neue Epoche | Erweiterung der `epoch_band`-Werte bestehender Einträge |
| Neue Sprachschicht | Neue Morpheme, neue Regelklasse in `rules_*.yaml` |
| Neue Siedlungsfunktion | Neue semantische Klasse + passende Morphem-Zuordnung |
| Patrozinien und Heiligennamen | Neue Lexikon-Sektion `ecclesiastical_names` |
| Statistische Kalibrierung | Gewichtungs-Overrides über separates Kalibrierungsfile |

---

## 15. Kompaktformel

```
Toponym = regionale Lexik
        + epochengerechte Morphemik
        + semantische Ortslogik
        + spatiotemporale Gewichtung
        + deterministischer Seed
```

In Systemterminologie:

```
derive_toponym(ToponymContext) → (str, list[str])
```
