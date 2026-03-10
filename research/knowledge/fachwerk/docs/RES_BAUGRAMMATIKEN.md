# RES_BAUGRAMMATIKEN
## Baugrammatiken des europäischen Fachwerks — Klassifikation, Inventar und Systemzuordnung

---

```yaml
tier: 2
authority: REFERENCE
status: Freigegeben
version: 1.0
datum: 2026-03-07
bereich: FACHWERK/SYSTEMATIK
references: RES_FACHWERK_DEFINITION.md, ARCH_TAXONOMY.md, SYS_PRINCIPLES.md §3, ARCH_POLICIES.md
```

---

## Methodik und Evidenzgrade

- **[HART]** — durch mehrere unabhängige akademische Quellen gesichert
- **[MITTEL]** — durch eine Primärquelle oder übereinstimmende Sekundärquellen gestützt
- **[SCHWACH]** — plausibel, aber noch nicht durch Primärliteratur verifiziert

Code-Bezeichner durchgehend Englisch. Quellenkürzel in Fußnoten.

---

## 1. Epochale Entwicklung

Die konstruktive Entwicklung verlief nicht linear, sondern in unterscheidbaren
Epochen mit regional unterschiedlicher Geschwindigkeit:

- **Pfostenbau** bis ca. 1250 — Vorläufer, kein Fachwerk im engeren Sinn.
- **Ständerbau** ab ca. 1250 als erste vollständige Fachwerkform:
  Ständer durchgehend von Schwelle bis Dachgebälk. **[HART]**[^hessenpark]
- **Übergang zum Stockwerkbau** in Mittel- und Oberdeutschland
  ca. 1470–1580. **[HART]**[^hessenpark] Auslöser: vermutlich Holzmangel
  im Umfeld wachsender Städte sowie der Wunsch nach kürzeren, leichter
  transportierbaren Hölzern. **[MITTEL]**[^wiki-fachwerk]
  Das älteste bekannte Stockwerkbaubeispiel: Bäckerhaus Eppingen, 1412.
  **[HART]**[^wiki-fachwerk]
- **Regionale Persistenz des Ständerbaus** bis ins 19. Jahrhundert,
  etwa im fränkischen Fachwerk und im Scheunenbau. **[HART]**[^wiki-ständerbauweise]
- **Ende des Fachwerkbaus** mit der Industrialisierung: Mineralische und
  metallische Baustoffe verdrängten Holz. **[HART]**[^wiki-fachwerk-haus]

Diese Epochen funktionieren in BVILLAGE als harte Diskontinuitäten in den
`epoch_band`-Policy-Parametern, nicht als Gradienten. Der Übergang zwischen
Ständerbau und Stockwerkbau ist kein Gradient — er ist ein Grammatikbruch.

---

## 2. Entscheidungsregel: Wann ist eine neue Baugrammatik nötig?

Eine neue Baugrammatik — und damit ein neuer `IFrameProducer` — ist genau
dann erforderlich, wenn sich mindestens eines der folgenden Merkmale ändert:

| Merkmal | Erläuterung |
|---|---|
| Primäre Tragstruktur | Was ist die strukturelle Primäreinheit? |
| Lastpfad | Wie fließen Lasten durch das Gebäude? |
| Generierungsreihenfolge | Womit beginnt der Architekt? |
| Definition der strukturellen Einheit | Binder, Geschoss, Cruck-Paar, Arkade? |

Wenn nur Parameter variieren (Ständerabstand, Geschosszahl, Strebenmuster),
reicht eine Policy. Regionale Varianten sind grundsätzlich `StylePolicy`-
oder `CulturePolicy`-Konfigurationen, keine neuen Baugrammatiken.

---

## 3. Die fünf Baugrammatiken

### 3.1 `BOX_FRAME` — Ständerbau

**Primärstruktur:** `binder_sequence` — durchgehende Ständer, gebäudehoch.

Beim Ständerbau laufen die Wandständer von der Schwelle bis zum Traufrähm
durch. Deckenbalken sind in die Ständer eingezapft oder überblattet. Die
Dachlast wird über diese Ständer direkt zur Schwelle und zum Fundament
geleitet. **[HART]**[^rdklabor] Das Haus entsteht als Sequenz tragender
Querrahmen. **[HART]**[^rdklabor]

Varianten (Zwei-, Drei-, Vierständer) unterscheiden sich durch die Anzahl
innerer Stützenreihen und die Spannweiten — diese sind `policy_parameters`,
keine separaten Baugrammatiken. **[MITTEL]**[^wiki-timber-framing]

**Generierungsreihenfolge:**

1. `derive_binder_sequence()` — Querrahmen ableiten
2. `derive_post_rows()` — Ständerreihen bestimmen
3. `derive_longitudinals()` — Längsverbände einziehen
4. `fit_openings_into_bays()` — Öffnungen in Gefache einpassen

> **`frame_producer_class`:** `BoxFrameProducer`
> **`construction_grammar`:** `BOX_FRAME`
> **`entry_point`:** `derive_binder_sequence(frame_plan: FramePlan) -> BoundFrame`

---

### 3.2 `STOREY_FRAME` — Stockwerkbau

**Primärstruktur:** `storey_frames` — gestapelte, autonome Geschosseinheiten.

Beim Stockwerkbau bildet jedes Geschoss eine in sich geschlossene Einheit
aus Schwelle, Ständern und Rähm. Diese Einheiten werden gestapelt; jedes
Geschoss wird separat abgebunden und aufgerichtet. **[HART]**[^rdklabor][^hessenpark]
Vorkragungen (`jettying`) entstehen durch vorstehende Deckenbalken —
eine typische konstruktive Konsequenz dieser Baugrammatik.
**[HART]**[^stockwerkbau]

Der Begriff *Rähmbau* ist veraltet. Korrekt: **Stockwerkbau** oder
**Stockwerkbauweise**. Das *Bildwörterbuch der Architektur* (Koepf/Binding 2005)
und die einschlägige Wikipedia-Artikel führen dies explizit aus.
**[HART]**[^raehm] Der interne Klassenname `StoreyFrameProducer` folgt dem
korrekten englischen Fachbegriff.

**Generierungsreihenfolge:**

1. `derive_storey_frames()` — Geschossrahmen ableiten
2. `derive_jetty_offsets()` — Vorkragungen bestimmen
3. `derive_facade_grid()` — Fassadenraster ableiten
4. `stack_frames()` — Geschosse stapeln

> **`frame_producer_class`:** `StoreyFrameProducer`
> **`construction_grammar`:** `STOREY_FRAME`
> **`entry_point`:** `derive_storey_frames(frame_plan: FramePlan) -> BoundStoreyStack`

---

### 3.3 `CRUCK_FRAME` — Cruck-System

**Primärstruktur:** `cruck_pairs` — Dachtragwerk als Primärrahmen.

Zwei gebogene oder gerade Hölzer (`cruck_blades`) bilden einen A-Rahmen,
der von nahe Bodenniveau bis zum Dachfirst reicht. Dach- und Wandtragwerk
sind in einem einzigen Member vereint. Die Außenwände sind strukturell
sekundär. **[HART]**[^cruck-northhouse]

Der Lastpfad ist invertiert gegenüber allen anderen Baugrammatiken:
Dach → Boden, nicht Wand → Boden. Dies macht `CRUCK_FRAME` zu einer
konstruktiv eigenständigen Baugrammatik. **[HART]**[^cruck-northhouse]

Historische Varianten unterscheiden sich in der Ansatzhöhe der `blades`,
nicht in der grundlegenden Logik: **[HART]**

| Variante | Beschreibung | Kontext |
|---|---|---|
| Full Cruck | Blades von Bodenniveau bis First | Standard |
| Jointed Cruck | Gespleißte Blades aus mehreren Hölzern | Westengland |
| Raised Cruck | Blades beginnen oberhalb Wandfuß | Fast ausschließlich in Steinwandgebäuden **[MITTEL]**[^bard-glossary] |

Geographische Eingrenzung: England und Wales gesichert. Westfrankreich
peripher. Kanonisches Standardwerk: N. W. Alcock, *Cruck Construction*,
CBA 1981. **[HART]**[^timber-framers-guild]

**Generierungsreihenfolge:**

1. `derive_cruck_pairs()` — Cruck-Paare ableiten
2. `derive_roof_geometry()` — Dachstruktur ableiten
3. `attach_walls()` — Wände sekundär einfügen

> **`frame_producer_class`:** `CruckFrameProducer`
> **`construction_grammar`:** `CRUCK_FRAME`
> **`entry_point`:** `derive_cruck_pairs(frame_plan: FramePlan) -> BoundCruckFrame`

---

### 3.4 `AISLED_FRAME` — Aisled-System

**Primärstruktur:** `arcade_rows` — innere Stützenreihen als struktureller Kern.

Aisled-Konstruktionen schaffen große Hallenräume, indem innere Stützenreihen
(`arcade_posts`) die Dachspannweite unterteilen. Das Mittelschiff (`nave`)
bestimmt die Primärspannweite; die Seitenschiffe (`aisles`) werden davon
abgeleitet. **[HART]**[^wiki-timber-framing]

Die VAG Aisled Buildings Database dokumentiert 391 aisled halls und
2.127 aisled barns in England und Wales. Das älteste bekannte Beispiel
(Cressing Temple barn) datiert auf 1205–1235. **[HART]**[^vag-aisled]

Die Arkadenreihe, nicht der einzelne Binder, ist die Primäreinheit der
Generierung — das ist der konstruktive Unterschied zu `BOX_FRAME`. Obwohl
beide Baugrammatiken Stützenreihen verwenden, denkt Box Frame in Querrahmen
(`frame`), Aisled Frame in Längsachsen (`arcade_row`).
**[HART]**[^vag-aisled]

Hybridfall: Kombinierte Cruck-Aisled-Konstruktionen sind belegt
(Plas Uchaf, Wales, 1435). Dies ist ein `hybrid_archetype`, kein
Widerspruch zur Baugrammatiktrennung. **[HART]**[^hall-house-wiki]

**Generierungsreihenfolge:**

1. `derive_arcade_rows()` — Arkadenreihen ableiten
2. `derive_aisles()` — Seitenschiffe ableiten
3. `derive_roof()` — Dachstruktur ableiten

> **`frame_producer_class`:** `AisledFrameProducer`
> **`construction_grammar`:** `AISLED_FRAME`
> **`entry_point`:** `derive_arcade_rows(frame_plan: FramePlan) -> BoundAisledFrame`

---

### 3.5 `WALL_GRID_FRAME` — Wandrastersystem *(Phase 2)*

**Primärstruktur:** `frame_grid` — selbstausgesteiftes Wandraster.

Das Wandrastersystem strukturiert den Bau durch ein gleichmäßiges
Fassadenraster aus Pfosten (*poteaux*), Horizontalen (*sablières*) und
Diagonalen (*décharges*). Jede Ebene ist eine autonome, selbstausgesteifte
Einheit. **[HART]**[^pufr-alsace]

Abgrenzung zu `STOREY_FRAME`: Beide denken in Schichten. Die `primary_unit`
beim Stockwerkbau ist der Geschossrahmen; beim Wandrastersystem ist es die
Wandfläche. Die Eigenständigkeit ist durch die elsässische Forschung
wissenschaftlich dokumentiert. **[HART]**[^pufr-alsace]

Terminologie: *pan de bois* bezeichnet das Konstruktionssystem;
*colombage* ist heute ein Sammelbegriff. Für BVILLAGE:
`WALL_GRID_FRAME` als `construction_grammar`-Bezeichner,
`pan de bois` als regionale Ausprägung. **[MITTEL]**[^wiki-colombages]

**Generierungsreihenfolge:**

1. `derive_frame_grid()` — Fassadenraster ableiten
2. `derive_facade_openings()` — Öffnungen einpassen
3. `stack_frames()` — Geschosse koppeln

> **`frame_producer_class`:** `WallGridFrameProducer` *(Phase 2)*
> **`construction_grammar`:** `WALL_GRID_FRAME`
> **`entry_point`:** `derive_frame_grid(frame_plan: FramePlan) -> BoundWallGrid`

---

## 4. Zuordnung Baugrammatik → Frame Producer

```
BoxFrameProducer        construction_grammar = BOX_FRAME
                        archetypes: FW-LH-ND, FW-LH-2S/3S/4S,
                                    FW-GULF, FW-HAUB, FW-MITT,
                                    FW-WLD, FW-OHALL, FW-LH-EN

StoreyFrameProducer     construction_grammar = STOREY_FRAME
                        archetypes: FW-ER-MD, FW-HARZ,
                                    FW-STG-GIE, FW-STG-TRF,
                                    FW-ACK, FW-SPC, FW-MER, FW-HOF

CruckFrameProducer      construction_grammar = CRUCK_FRAME
                        archetypes: FW-CRK, FW-CRJ, FW-CRR

AisledFrameProducer     construction_grammar = AISLED_FRAME
                        archetypes: FW-AIS

WallGridFrameProducer   construction_grammar = WALL_GRID_FRAME  [Phase 2]
                        archetypes: FW-PDC, FW-COL
```

---

## 5. Archetypen-Inventar

**Begriffsklärung:** Ein *Archetyp* ist ein kategorial stabiles Raummuster,
das Varianten zulässt, ohne seine Identität zu verlieren. In BVILLAGE ist
`archetype` ausschließlich topologisch definiert — Zonanordnung,
Raumhierarchie, Zirkulationslogik — unabhängig von Material, Region und
Epoche. Die Baugrammatik sagt, wie Member erzeugt werden; der Archetyp
sagt, in welcher räumlichen Ordnung sie angeordnet sind.

### 5.1 Korrektur: Wealden House

Das Wealden House ist ein Hallenhaus-Archetyp, kein Stockwerkbau.
Es besitzt eine zentrale, zur Dachzone offene Halle (`open_hall`)
flankiert von zweigeschossigen Endfeldern unter einem durchgehenden Dach.
**[HART]**[^vag-wealden][^oxford-wealden][^wiki-wealden]

Charakteristisch ist die `flying_wall_plate`: Da die Außenwand der
Mittelhalle nicht vorgekragt ist, läuft die Wandplatte über den
zurückgesetzten Hallenteil. Das ist strukturell unvereinbar mit
Stockwerklogik. **[HART]**[^vag-wealden]

> **Korrektur:** `FW-WLD` — `construction_grammar = BOX_FRAME`
> (nicht `STOREY_FRAME`). Anzupassen in `ARCH_TAXONOMY.md`.

### 5.2 Inventar

| `archetype_id` | Name | Region | Periode | `construction_grammar` | Evidenz |
|---|---|---|---|---|---|
| `FW-LH-ND` | Niederdeutsches Hallenhaus | Norddeutschland | 13.–19. Jh. | `BOX_FRAME` | HART |
| `FW-LH-2S` | Hallenhaus Zweiständer | Norddeutschland | 15.–18. Jh. | `BOX_FRAME` | HART |
| `FW-LH-3S` | Hallenhaus Dreiständer | Norddeutschland | 16.–18. Jh. | `BOX_FRAME` | HART |
| `FW-LH-4S` | Hallenhaus Vierständer | Norddeutschland | 16.–19. Jh. | `BOX_FRAME` | HART |
| `FW-GULF` | Gulfhaus | Nordseeküste | 16.–19. Jh. | `BOX_FRAME` | MITTEL |
| `FW-HAUB` | Haubarg | Nordfriesland | 17.–19. Jh. | `BOX_FRAME` | MITTEL |
| `FW-MITT` | Mittertennhaus | Alpenraum | 15.–19. Jh. | `BOX_FRAME` | MITTEL |
| `FW-ER-MD` | Mitteldeutsches Ernhaus | Mittel-/Süddeutschland | 14.–18. Jh. | `STOREY_FRAME` | MITTEL |
| `FW-HARZ` | Harzer Haus | Harzregion | 16.–19. Jh. | `STOREY_FRAME` | MITTEL |
| `FW-STG-GIE` | Giebelständiges Stadthaus | Städte (D) | 14.–18. Jh. | `STOREY_FRAME` | HART |
| `FW-STG-TRF` | Traufenständiges Stadthaus | Städte (D) | 15.–18. Jh. | `STOREY_FRAME` | HART |
| `FW-ACK` | Ackerbürgerhaus | Kleinstädte (D) | 15.–19. Jh. | `STOREY_FRAME` | MITTEL |
| `FW-SPC` | Speicherhaus | Städte | 15.–18. Jh. | `STOREY_FRAME` | MITTEL |
| `FW-WLD` *(korr.)* | Wealden House | Südostengland | 14.–16. Jh. | `BOX_FRAME` | HART |
| `FW-MER` | Merchant House | England, Niederlande | 14.–17. Jh. | `STOREY_FRAME` | MITTEL |
| `FW-AIS` | Aisled Hall House | England, Niederlande | 12.–16. Jh. | `AISLED_FRAME` | HART |
| `FW-OHALL` | Open Hall House | England | 13.–16. Jh. | `BOX_FRAME` | HART |
| `FW-CRK` | Cruck House (Full Cruck) | England, Wales | 12.–17. Jh. | `CRUCK_FRAME` | HART |
| `FW-CRJ` | Jointed Cruck House | Westengland | 13.–16. Jh. | `CRUCK_FRAME` | MITTEL |
| `FW-CRR` | Raised Cruck House | England | 14.–17. Jh. | `CRUCK_FRAME` | MITTEL |
| `FW-PDC` | Maison à pans de bois | Frankreich, Elsass | 14.–18. Jh. | `WALL_GRID_FRAME` | HART |
| `FW-COL` | Colombage House | Normandie, Lothringen | 14.–18. Jh. | `WALL_GRID_FRAME` | HART |
| `FW-UMG` | Umgebindehaus | Oberlausitz | 15.–19. Jh. | `HYBRID` | MITTEL |
| `FW-HOF` | Fachwerk-Hofanlage | Mittel-/Süddeutschland | 16.–19. Jh. | `STOREY_FRAME` | MITTEL |
| `FW-LH-EN` *(prov.)* | English Longhouse | England, Wales | 12.–16. Jh. | `BOX_FRAME` | MITTEL |
| `FW-STV` *(prov.)* | Stavkirke-Grundtypus | Skandinavien | 11.–14. Jh. | `BOX_FRAME` (tentativ) | SCHWACH |

*Provisional-Einträge (`prov.`) sind noch nicht Teil von `ARCH_TAXONOMY.md`.*

---

## 6. Offene Forschungsfelder

| ID | Thema | Status | Zieldokument |
|---|---|---|---|
| GRM-001 | Gulfhaus / Haubarg: `policy_variant` oder eigenständiger `archetype`? Spannweiten und Stützenlogik weichen erheblich ab. | Offen — Primärquellen nötig | `RES_ARCHETYPE_SONDERFAELLE.md` |
| GRM-002 | `hybrid_strategy` für `FW-UMG` (Blockbau-Kern + Fachwerk-Umgebinde) | Konzeptionell offen | `RES_ARCHETYPE_SONDERFAELLE.md` |
| GRM-003 | `FW-STV` Stabbau: Konstruktionslogik (Kernpfosten) weicht von `BOX_FRAME` ab; nur SCHWACH-Evidenz | Primärliteratur fehlt | `RES_ARCHETYPE_SONDERFAELLE.md` |
| GRM-004 | `FW-LH-EN` Abgrenzung zu `FW-OHALL` nicht vollständig belegt | Mercer 1975 als Ausgangspunkt | `RES_ARCHETYPE_SONDERFAELLE.md` |
| GRM-005 | Niederlande / Flandern: keine Primärquellen zu Dutch timber townhouse, Flemish guild house | Explizite Forschungslücke | `RES_ARCHETYPE_SONDERFAELLE.md` |
| GRM-006 | `FW-PDC` intern: zwei Subtypen (*poteaux de fond* vs. *étages superposés*) — für Phase 1 vereinfacht | Für Phase 2 zu differenzieren | `RES_BAUGRAMMATIKEN.md` §3.5 |
| GRM-007 | `AISLED_FRAME` vs. Zweiständerhaus: konzeptionelle Grenze zwischen deutschen Varianten und englischen Aisled Halls | Entscheidung ausstehend | `RES_ARCHETYPE_SONDERFAELLE.md` |

---

## 7. Empfohlene Primärliteratur

Noch nicht vollständig ausgewertet:

- **N. W. Alcock**: *Cruck Construction: An Introduction and Catalog.* CBA, 1981.
  → Pflichtlektüre für `CruckFrameProducer`.
- **E. Mercer**: *English Vernacular Houses.* RCHME, 1975.
- **R. W. Brunskill**: *Illustrated Handbook of Vernacular Architecture.* Faber, 1978.
- **C. A. Hewett**: *English Historic Carpentry.* Phillimore, 1980.
- **Heinrich Stiewe**: *Fachwerkhäuser in Deutschland.* Darmstadt, 2007.
- **Manfred Gerner**: *Fachwerk, Entwicklung, Gefüge, Instandsetzung.* DVA, 2007.
- **Hans Koepf / Günther Binding**: *Bildwörterbuch der Architektur.* Kröner, 2005.
  → Terminologiereferenz.
- **R. T. Mason**: *Framed Buildings of the Weald.* Coach Publishing, 1969.
- **W. H. Zimmermann**: Pfosten, Ständer und Schwelle und der Übergang vom
  Pfosten- zum Ständerbau. *Probleme der Küstenforschung* 25, 1998.

---

## 8. Quellen

[^wiki-fachwerk]: Fachwerkhaus. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Fachwerkhaus

[^rdklabor]: Fachwerk, Fachwerkbau. RDK Labor, März 2026.
  https://www.rdklabor.de/wiki/Fachwerk,_Fachwerkbau

[^hessenpark]: Freilichtmuseum Hessenpark / Kompetenzzentrum Fachwerk, März 2026.
  https://kompetenzzentrum-fachwerk.de/themenschwerpunkte/historische-konstruktionsweisen/

[^wiki-ständerbauweise]: Ständerbauweise. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Ständerbauweise

[^wiki-fachwerk-haus]: Fachwerkhaus (Industrialisierung). Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Fachwerkhaus

[^stockwerkbau]: Rähmbauweise. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Rähmbauweise

[^raehm]: Rähm. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Rähm

[^wiki-timber-framing]: Timber framing. Wikipedia (English), März 2026.
  https://en.wikipedia.org/wiki/Timber_framing

[^cruck-northhouse]: North House Folk School: Cruck Framing, 2020.
  https://northhouse.org/course-session/cruck-framing-8-5-2020

[^timber-framers-guild]: Timber Framers Guild: Review of N. W. Alcock,
  *Cruck Construction*, CBA 1981.
  https://www.tfguild.org/downloads/TF-136-book-review.pdf

[^bard-glossary]: BARD Illustrated Glossary (Tree-Ring Services, 2024).
  http://www.buildingarchaeology.com/wp-content/uploads/2024/03/BARD-Illustrated-Glossary.pdf

[^vag-aisled]: N. W. Alcock / VAG: A Database of Aisled Buildings in
  England and Wales. *Vernacular Architecture*, 2024.
  https://www.tandfonline.com/doi/full/10.1080/03055477.2024.2321373

[^hall-house-wiki]: Hall house. Wikipedia (English), März 2026.
  https://en.wikipedia.org/wiki/Hall_house

[^vag-wealden]: VAG Wealden Houses Database. Archaeology Data Service, 2025.
  https://archaeologydataservice.ac.uk/archives/view/vag_wealden/

[^oxford-wealden]: Oxford Reference: Wealden house. OUP, 2023.
  https://www.oxfordreference.com/display/10.1093/oi/authority.20110803121434465

[^wiki-wealden]: Wealden hall house. Wikipedia (English), März 2026.
  https://en.wikipedia.org/wiki/Wealden_hall_house

[^pufr-alsace]: La construction en pan de bois. Presses universitaires
  François-Rabelais, 2018.
  https://books.openedition.org/pufr/7902

[^wiki-colombages]: Maison à colombages. Wikipedia (français), März 2026.
  https://fr.wikipedia.org/wiki/Maison_à_colombages

---

*Status: Freigegeben als REFERENCE-Dokument. Version 1.0.*
*© 2026 Alexander Bernardi — CC-BY-SA 4.0*
