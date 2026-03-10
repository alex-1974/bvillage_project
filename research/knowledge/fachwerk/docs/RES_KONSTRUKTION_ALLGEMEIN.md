# RES_KONSTRUKTION_ALLGEMEIN
## Fachwerk-Konstruktionsgrammatik: Achsen, Vokabular und Policy-Schichten

---

```yaml
tier: 2
authority: REFERENCE
status: Freigegeben
version: 1.0
datum: 2026-03-07
bereich: FACHWERK/KONSTRUKTION
references: RES_FACHWERK_DEFINITION.md, RES_BAUGRAMMATIKEN.md, RES_BAUPRAXIS_QUANTITATIV.md
```

---

## Methodik und Evidenzgrade

- **[HART]** — durch mehrere unabhängige akademische Quellen gesichert
- **[MITTEL]** — durch eine Primärquelle oder übereinstimmende Sekundärquellen gestützt
- **[SCHWACH]** — aus experimenteller Archäologie, Analogieschlüssen oder Fachtradition

---

## Vorbemerkung: Grammatik ist nicht Stil

Konstruktionsgrammatik ist die Logik, wie Kräfte fließen. Sie definiert,
wie Ständer stehen, wie Geschosse zusammenhängen, wie Aussteifung
funktioniert und wie Verbindungen Lasten übertragen.

Stil ist, ob ein Gefach mit Lehm oder Ziegel gefüllt ist. Stil ist,
ob ein Balken beschnitzt ist. Stil ist die Farbe.

Diese Trennung ist architektonisch fundamental und bestimmt die
Policy-Zuordnung für jeden Parameter:

```
Grammatik-Wechsel   → ConstructionDomain oder CulturePolicy-Branch
Parameter-Verschiebung → CulturePolicy
Oberflächen-Variation  → StylePolicy
```

Die vier Grammatikachsen dieses Dokuments entsprechen direkt den
vier Parameterdimensionen der `CulturePolicy`.

---

## 1. Achse 1 — Ständerprinzip (Tragsystem-Grammatik)

Die wichtigste Grammatikachse. Sie bestimmt, wie Lasten aus dem Dach
in den Boden gelangen — und damit Länge, Verbindungslogik und Anzahl
aller vertikalen members.

Die Entwicklung G-PFOSTEN → G-FIRST → G-STAEND → G-STOCK ist eine
**Evolutionskette**, keine Stilvariation. Jede Stufe ist ein eigener
`construction_grammar`-Wert oder ein eigenständiger CulturePolicy-Branch.

### 1.1 Grammatik-IDs

| ID | Name | Kernprinzip | Ständerhöhe | epoch_band |
|---|---|---|---|---|
| G-PFOSTEN | Pfostenbau | Pfosten in Erde eingespannt; kein Schwellkranz | Bis Trauf, erdverankert | bis ~13. Jh. |
| G-FIRST | Firstsäulenbau | Mittelständer reicht bis zur Firstpfette; trägt Dach von innen | Vollhöhe (Boden bis First) | 10.–15. Jh. |
| G-STAEND | Ständerbau (Geschossbau) | Außenwandständer durchlaufen mehrere Geschosse; Deckenbalken eingeschossen | Mehrgeschossig durchlaufend | 13.–17. Jh. |
| G-STOCK | Stockwerksbau (Rähmbau) | Jedes Geschoss eigenständige Einheit (Schwelle→Rähm); stapelbar | Nur geschosshoch | ab 15./16. Jh. |
| G-BUND | Bundwerk | Innenverschaltes Fachwerk; Streben verdeckt; nur Alpenraum | Geschosshoch | 17.–19. Jh. Vorarlberg/Schweiz |

### 1.2 G-STAEND im Detail

Das entscheidende Prinzip: der Ständer **durchläuft alle Geschosse**
von der Schwelle bis zum Traufrähm. Deckenbalken sind in die Ständer
eingezapft, nicht aufgelegt. **[HART]**

Strukturelle Konsequenz:
- Lastpfad: Dach → Traufrähm → Ständer → Schwelle → Fundament
- Öffnungsbreiten sind durch Ständerabstand determiniert
- Auskragungen erfordern Kragbalken durch den Ständer
- Lange, durchgehende Hölzer nötig (6–10 m bei 2–3 Geschossen)

Bis ca. 1470 war G-STAEND das vorherrschende Konstruktionsprinzip.
Der Übergang zu G-STOCK vollzog sich bis ca. 1580. Im fränkischen Raum
hielt sich G-STAEND bis ins 19. Jahrhundert. **[HART]**

### 1.3 G-STOCK im Detail

Das entscheidende Prinzip: die Ständer sind jeweils nur ein Stockwerk
hoch und reichen von der Schwelle bis zum jeweiligen horizontal
aufliegenden Rähm. Jedes Stockwerk wird separat abgebunden und
aufgerichtet. **[HART]**

Strukturelle Konsequenz:
- Jedes Geschoss ist ein eigenständiges Lasttragsystem
- Rähm und Schwelle sind tragende Ebenen, nicht nur Abschlüsse
- Deckenbalken liegen auf dem Rähm auf (nicht mehr eingezapft)
- Kürzere Einzelhölzer — bessere Transportierbarkeit, weniger Holzqualität nötig

Auslöser: vermutlich Holzmangel im Umfeld wachsender Städte und der Wunsch
nach höheren Gebäuden bei kürzeren Bauhölzern. Frühestes gesichertes
Beispiel: Bäckerhaus Eppingen, 1412. **[MITTEL]**

G-STOCK ermöglicht **Auskragung**: Deckenbalken kragen über den Rähm
hinaus und tragen die Schwelle des nächsten Geschosses. Unterstützt
durch Knaggen (Konsolen), die das statische Dreieck schließen.

### 1.4 Barockfachwerk als G-STOCK-Variante

Barockfachwerk (17.–18. Jh.) ist kein StylePolicy-Parameter.
Die Struktur bleibt G-STOCK, aber Auskragungen werden kleiner oder
verschwinden, Doppelständer entstehen (rhythmisierte Fensterachsen),
dekorative Hölzer ohne statische Funktion nehmen zu. Das verändert
Zapfenlängen, Ständerhöhen, Kragkonstruktionen — das ist
`CulturePolicy`, nicht `StylePolicy`.

### 1.5 BVILLAGE-Implikationen Achse 1

G-FIRST erfordert eine Firstsäule als zentrales member — G-STOCK kennt
das nicht. Ein G-STAEND-Haus hat andere member-Längen, andere Zapfentiefen
und andere Aussteifungslogik als ein G-STOCK-Haus.

Scheunen: Die Ständerbauweise G-STAEND blieb noch lange nach ihrer
Ablösung durch G-STOCK bei Scheunenbauten üblich, wo große Raumhöhen
erforderlich waren. **[MITTEL]** In BVILLAGE triggert
`economy_profile = agricultural_storage` deshalb G-STAEND unabhängig
vom `epoch_band`.

---

## 2. Achse 2 — Aussteifungsgrammatik (Streben-System)

Der sichtbarste, am stärksten regionalisierte Aspekt. Die Aussteifungsgrammatik
ist aber nicht rein regional — sie ist epochal und konstruktiv-logisch.
Die klassische Dreiteilung in niedersächsisches, fränkisches und
alemannisches Fachwerk gilt heute als wissenschaftlich überholt
(Carl Schäfer, 19. Jh.; abgelöst durch chronologisch-konstruktive Forschung).

Jedes Streben-System hat eine andere Kraftübertragungslogik und damit
andere member-Geometrien im `FramePlan`.

### 2.1 Streben-IDs

| ID | Name | Geometrie | Kraftpfad | Epoche / Region |
|---|---|---|---|---|
| S-KOPF | Kopfband | Vom Ständer-Kopf zur Rähm/Decke, kurz | Schub am Kopf abgefangen | 13.–18. Jh. universal |
| S-FUSS | Fußband | Von Schwelle/Ständer-Fuß schräg aufwärts | Schub am Fuß eingeleitet | 13.–18. Jh. universal |
| S-KOPF-FUSS | Kopf- und Fußband kombiniert | Beide an einem Ständer | K-Figur symmetrisch | 14.–17. Jh. fränkisch |
| S-MANN | Mannfigur | Fußbänder + kreuzende Kopfbänder an Bundständer | Bündelaussteifung am Ständer | 1470–1550 Übergang; mitteldeutsch |
| S-MANN-H | Hessenmann | 3/4-hohe Fußstreben + verkürztes Kopfwinkelholz | Variante Mannfigur | 16.–17. Jh. Hessen |
| S-MANN-SW | Schwäbisches Männle | Lokale Proportionsvariante der Mannfigur | Wie Mannfigur | 16.–18. Jh. Württemberg |
| S-LANG | Langstrebe | Verbindet Schwelle und Rähm diagonal über ganzes Geschoss | Maximale Schubübertragung | 14.–16. Jh. |
| S-AND | Andreaskreuz | Zwei gekreuzte Langstreben im Gefach | Auskreuzung ganzes Gefach | ab 15. Jh. universal; Schmuckform ab 17. Jh. |
| S-K | K-Figur | Einseitige Streben ober- und unterhalb des Riegels | Asymmetrische Aussteifung | 16.–18. Jh. mitteldeutsch |
| S-WEITSAEND | Weite Ständerstellung + Kopf/Fußband | Große Spannweiten, wenige members pro Feld | Weicher Lastpfad | Alemannisch, 14.–17. Jh. |
| S-ENGSTUDD | Enge Ständerstellung (Close Studding) | Sehr viele dichte Ständer, Abstand ≈ Ständerbreite | Redundanter Lastpfad | England, elite, 15.–16. Jh. |
| S-FAECH | Fächerrosette | Fächerförmig ausstrahlende Zierstreben | **Statisch neutral** | Niederdeutsch, 16.–18. Jh. |
| S-FEUERBOCK | Feuerbock | Geschweifte Variante des Andreaskreuzes | Wie Andreaskreuz; Schmuckform | 16.–17. Jh. mitteldeutsch |

S-MANN ist konstruktiv anders als S-AND: Mannfigur bedeutet 4 Streben
an einem Ständer = 4 members. Andreaskreuz bedeutet 2 members im Gefach.
Verschiedene member-Topologien in `FramePlan`.

S-FAECH und S-FEUERBOCK sind reine StylePolicy — Schmuckmitglieder
ohne Einfluss auf den `PhysicalPlausibilityValidator`.

### 2.2 Strebeprogramm: strukturelle Wirksamkeit

| Strebenfigur | Aussteifungsrichtung | Effizienz | Holzmenge | Epoche |
|---|---|---|---|---|
| Einzelne Fußstrebe | Einseitig | Gering | Gering | 13.–14. Jh. |
| Langstrebe | Einseitig, volles Gefach | Mittel | Mittel | 13.–15. Jh. |
| K-Figur | Einseitig | Mittel | Mittel | Alle |
| Andreaskreuz | Beide Richtungen | Hoch | Mittel | ab 15. Jh. |
| Mannfigur | Beide Richtungen + Ständerstabilisierung | Sehr hoch | Hoch | ab 16. Jh. |
| Wilder Mann | Asymmetrisch, beide Richtungen | Hoch | Mittel-hoch | 15.–17. Jh. Franken |
| Thüringer Leiter | Horizontal (kein diagonal) | Schwach | Mittel | Regional |
| Feuerbock | Wie Andreaskreuz, geschwungen | Hoch | Mittel | 17.–19. Jh. |

### 2.3 Strebenwinkel und Kraftfluss

Die Last wird durch die Strebenstellung an das Fundament weitergeleitet.
Würde man die Strebe genau umgekehrt anordnen, müssten alle Bauteile
diese Kräfte abfangen.

CulturePolicy-Parameter:
- `brace_angle_preferred_deg`: 45–60° (optimaler Druckstab)
- `brace_angle_min_deg`: 30° (akzeptabel)
- `brace_angle_max_deg`: 70° (Grenzfall)

Abweichung: SOFT Issue. Starke Abweichung: HARD Issue.

---

## 3. Achse 3 — Verbindungsgrammatik

Weniger sichtbar, aber konstruktiv entscheidend. Verbindungstypen
bestimmen Kraftübertragungskapazitäten und damit die Dimensionierungslogik
der `ConstructionCulturePolicy`.

### 3.1 Verbindungs-IDs

| ID | Name | Prinzip | Belastbarkeit | Epoche |
|---|---|---|---|---|
| V-BLATT | Verblattung | Bündige Überlappung + Holznagel | Scherbeanspruchung; begrenzte Zugkraft | früh, bis 15. Jh.; alemannisch |
| V-ZAPF | Verzapfung | Zapfen greift in Loch; primär Druck + Schub | Druck gut, Zug begrenzt | ab 13. Jh.; ab 16. Jh. dominant |
| V-KAMM | Verkämmung | Kreuzende Hölzer, beide ausgeklinkt | Druckkraft; keine Zugkraft | Schwellenkreuzung, Rähm-Kreuzung |
| V-DURCHSCH | Durchschossen | Balken wird durch Ständerquerschnitt geführt | Hohe Schubkraft; Ständer geschwächt | Ständerbau; bis 16. Jh. |
| V-STURZ | Sturzriegel | Horizontaler Riegel über Öffnung; trägt Auflast | Biegung auf Riegel | universal |

### 3.2 Epochensignal Verbindungen

Die Blattverbindungen wurden weitgehend aufgegeben und von der
Zapfenverbindung abgelöst. Diese konstruktiven Entwicklungen des
Fachwerkbaus waren 1600 abgeschlossen. **[HART]**

V-BLATT (alemannische Frühphase) erzeugt andere Verbindungsknoten-
konfigurationen als V-ZAPF und beeinflusst minimale Querschnitte am
Verbindungspunkt. Verbindungstyp gehört in `ConstructionCulturePolicy`,
nicht in `StylePolicy`.

`max_utilization_ratio` hängt vom Verbindungstyp ab. V-BLATT: niedrigere
Kapazität → höherer `overdimension_factor`.

---

## 4. Achse 4 — Gefachgrammatik (Infill-System)

Ausfachung ist keine Konstruktionsgrammatik im engeren Sinne, aber sie
verändert die thermische und statische Gesamtwirkung des Wandsystems.

### 4.1 Gefach-IDs

| ID | Material | Grammatik-Implikation | Region / Epoche |
|---|---|---|---|
| I-LEHM | Flechtwerk + Lehmbewurf (Klaiben) | Leicht; feuchtesensibel | Universal bis 19. Jh. |
| I-ZIEG | Ausgemauert (sichtiger Backstein) | Schwerer; Schwellbalken-Auflagerlast steigt | ab 16./17. Jh.; norddeutsch früher |
| I-BOHL | Bohlenausfachung | Holzbohlen stehend/liegend; Wohnstube | Alemannisch; alpine Zone |
| I-SCHIEF | Schieferverkleidung | Trägt nicht; verkleidet nachträglich | 18.–19. Jh. Mittelgebirge |
| I-PUTZ | Verputzt | Barockfachwerk; Angleichung an Steinbau-Optik | 17.–18. Jh. Städte |

Infill-Material ist **MaterialRegistry-Entscheidung**, durch `CulturePolicy`
(`epoch_band` × `region` × `wealth`) gesteuert. Es verändert
Fensterproportionen (Sturz- und Brüstungsriegel-Abstände) und
Eigengewicht-Annahmen im `PhysicalPlausibilityValidator`.

---

## 5. Vollständiges Elementvokabular

### 5.1 Vertikale Elemente

| Element | Funktion | Epochen | Anmerkung |
|---|---|---|---|
| Pfosten | Senkrechtes Holz in Erde eingespannt | Pfostenbau | Kein Schwellkranz; Feuchtigkeitsrisiko |
| Eckständer | Ständer an Gebäudeecken | Alle Fachwerkepochen | Immer vorhanden; stärkstes vertikales Glied |
| Wandständer | Ständer in Wandfläche | Alle Fachwerkepochen | G-STAEND: bis zum Dach. G-STOCK: Geschosshöhe |
| Bundständer | Ständer an Wandkreuzung | G-STOCK | Dort, wo Innenwand in Außenwand bindet |
| Türstock | Ständer beidseitig einer Tür | Alle Fachwerkepochen | Trägt Sturz; definiert Öffnungsbreite |
| Doppelständer | Zwei eng beieinanderstehende Ständer | Barock, 17.–18. Jh. | Bilden Fensterachsrhythmus; ästhetische Funktion |

### 5.2 Horizontale Elemente

| Element | Lage | Funktion | BVILLAGE-Rolle |
|---|---|---|---|
| Schwelle | Unterster Horizontalbalken eines Geschosses | Trägt Ständer; überträgt Last | `rail` role=`sill` |
| Rähm | Oberster Horizontalbalken eines Geschosses | Schließt Ständer ab; trägt Deckenbalken auf | `rail` role=`top_rail` |
| Riegel | Horizontalholz zwischen Ständern | Gliedert Gefach; überträgt Querlasten | `rail` role=`mid_rail` |
| Brüstungsriegel | Riegel in Fensterbrüstungshöhe | Unterkante Fensteröffnung | `rail` role=`sill_rail` |
| Sturzriegel | Riegel in Fenstersturzhöhe | Oberkante Fensteröffnung | `rail` role=`lintel` |
| Saumschwelle | Parallel zum Rähm | Kantet Deckenbalken ein | `rail` role=`ledger` |
| Schwellriegel | Gleichzeitig Schwelle und Rähm (G-STAEND) | Doppelfunktion | `rail` role=`intermediate` |

### 5.3 Diagonale Elemente

| Element | Geometrie | Funktion | Epoche | BVILLAGE-Rolle |
|---|---|---|---|---|
| Fußstrebe | Von Schwelle schräg aufwärts zum Ständer | Drucklast in Richtung Fundament | Alle Epochen | `brace` role=`foot_brace` |
| Kopfstrebe | Vom Rähm schräg abwärts zum Ständer | Ergänzt Fußstrebe; Zuglast oben | ab 15. Jh. | `brace` role=`head_brace` |
| Langstrebe | Von Schwelle diagonal bis Rähm | Volle Geschosshöhe überbrückend | 13.–16. Jh. | `brace` role=`long_brace` |
| Schwertung | Schräg, variierter Winkel | Frühe, ungeregelte Aussteifung | 13.–14. Jh. | `brace` role=`schwertung` |
| Knagge | Konsole am Rähm unter Kragbalken | Statisches Dreieck bei Auskragung | G-STOCK | `brace` role=`corbel_brace` |
| Andreaskreuz | Zwei sich kreuzende Streben (X) | Aussteifung in beide Richtungen | ab 15. Jh. | zwei `brace`-Objekte |
| Mannfigur | Fußstrebe + Kopfstrebe beidseitig eines Ständers | Vollständige Stabilisierung | 16.–18. Jh. | vier `brace`-Objekte |
| K-Figur | Einseitige Strebe ober- und unterhalb | Teilstabilisierung | Alle Epochen | zwei `brace`-Objekte |
| Wilder Mann | Asymmetrische Strebenkombination (fränkisch) | Komplexe Aussteifung | 15.–17. Jh. Franken | mehrere `brace`-Objekte |
| Raute | Vier Streben als Rautenmuster im Gefach | Aussteifung + Schmuck | 15.–17. Jh. | vier `brace`-Objekte |
| Thüringer Leiter | Mehrere Horizontalhölzer zwischen zwei Ständern | Leiterartiges Muster | 15.–18. Jh. Thüringen | `rail`-Reihe ohne Streben |
| Feuerbock | Gebogenes Andreaskreuz | Wie Andreaskreuz, geschwungen | 17.–19. Jh. | StylePolicy; parametrisch |
| Fächerrosette | Fächerförmig ausstrahlende Zierstreben | **Statisch neutral** | Niederdeutsch | StylePolicy |

---

## 6. Kragzonen-Grammatik

Auskragung ist kein Dekorationselement — sie ist eine konstruktive
Strategie.

**Primäre Funktion:** Witterungsschutz der Erdgeschosszone.
**Sekundär:** Raumgewinn in oberen Geschossen bei engen Stadtparzellen.
**Tertiär:** Lastverteilung (auskragende Balken übertragen Auflast nach innen).

| Typ | Mechanismus | Epoche | Max. Kragtiefe |
|---|---|---|---|
| Einfacher Kragbalken | Deckenbalken kragen über Rähm; tragen Schwelle OG | ab 15. Jh. | ~40 cm |
| Knaggen-gestützt | Konsole unter Kragbalken; statisches Dreieck | ab 15. Jh. | ~50 cm |
| Stichgebälk | Zusätzliche kurze Kragbalken zwischen Hauptbalken | 15.–17. Jh. | ~60 cm |
| Doppelte Auskragung | Zwei aufeinanderfolgende Geschosse kragen aus | 15.–17. Jh. | 80–120 cm gesamt |
| Geschlossener Kragfries | Durchgehender Fries ohne sichtbare Balkenenden | 16.–17. Jh. | ~30 cm |

Regionale Verteilung:
- **Stark:** Fränkisch (Nürnberg, Miltenberg), Hessisch (Marburg)
- **Moderat:** Norddeutsch, Westfälisch
- **Selten:** Alemannisch ländlich, Altbayern

Das Recht zur Vorkragung war in Städten stadtrechtlich geregelt —
nicht selbstverständlich. **[MITTEL]**

---

## 7. Epoche × Grammatik-Matrix

Die wichtigste Tabelle für den `ConstructionCulturePolicy`-Resolver.
Keine harten Grenzen, sondern Wahrscheinlichkeitsverteilungen.

| epoch_band | Ständer-Grammatik | Streben-Grammatik | Verbindung | Infill |
|---|---|---|---|---|
| `early_medieval` (10.–12. Jh.) | G-PFOSTEN, G-FIRST | S-KOPF einfach; kaum Aussteifung | V-BLATT | I-LEHM |
| `high_medieval` (13.–14. Jh.) | G-STAEND früh | S-KOPF, S-FUSS; Einzelverstrebung | V-ZAPF + V-BLATT Übergang | I-LEHM |
| `late_medieval` (14.–15. Jh.) | G-STAEND reif; G-STOCK Beginn | S-KOPF-FUSS, Langstrebe | V-ZAPF zunehmend | I-LEHM; I-ZIEG Anfang |
| `transition_1500` (1470–1550) | G-STOCK Übergangsphase | S-MANN (Übergangsmerkmal) | V-ZAPF dominant | I-ZIEG zunehmend |
| `early_modern` (1550–1620) | G-STOCK etabliert | S-AND häufig; Schmuckformen | V-ZAPF standard | I-ZIEG / I-LEHM |
| `baroque` (1620–1720) | G-STOCK dominant | S-AND dekorativ; S-FEUERBOCK | V-ZAPF | I-ZIEG / I-PUTZ |
| `enlightenment` (1720–1820) | G-STOCK; Rückgang | S-AND vereinfacht; Reduktion | V-ZAPF | I-PUTZ; I-SCHIEF |
| `historicism` (1820–1880) | G-STOCK letzter | Kaum Schmuck | V-ZAPF | I-ZIEG |

---

## 8. Regionale Grammatik-Profile (CulturePolicy-Cluster)

### 8.1 Profile-Übersicht

| CulturePolicy-ID | Region | Ständerabstand | Primäre Streben | Verbindung |
|---|---|---|---|---|
| CP-OBER | Oberdeutsch / Alemannisch | Weit | S-KOPF-FUSS (weite Felder) | V-BLATT früh → V-ZAPF |
| CP-MITT | Mitteldeutsch / Fränkisch | Eng bis mittel (unregelmäßig) | S-MANN, S-K, S-AND; reich | V-ZAPF |
| CP-NIEDER | Niederdeutsch / Niedersächsisch | Regelmäßig (= Balkenabstand) | S-KOPF, S-FUSS; S-FAECH (Schmuck) | V-ZAPF |
| CP-ENG-CS | Englisch Close Studding | Sehr eng (≈ Ständerbreite) | Keine Kreuzstreben nötig | Englische Zapfentechnik |
| CP-ENG-SP | Englisch Square Panel | Quadratische Felder | Dekorative Figuren (keine Tragfunktion) | Englische Technik |
| CP-FR-NORM | Französisch Normandie | Mittel-eng, unregelmäßig | Keine standardisierten Figuren | Französische Technik |
| CP-ALSA | Elsässisch | Mittel; fränkisch-alemannische Mischung | S-AND + S-KOPF-FUSS | V-ZAPF |

### 8.2 Regionale Grammatiken im Detail

**CP-NIEDER — Niederdeutsch/Niedersächsisch:**
Regelmäßige Ständerstellung im Abstand der Deckenbalken, typischerweise
80–120 cm. Fußbänder häufig als Fächerrosetten ausgebildet — regional
charakteristisch. Wenig Andreaskreuze in der Fassade; stattdessen
Fensterband und Eck-Verstrebung. Auskragungen moderat. **[MITTEL]**

`post_spacing_m`: 0.8–1.2 (regelmäßig)
`bracing_pattern`: foot_band_dominant
`ornament_level`: high (Fächerrosetten, Schnitzwerk)
`jetty_tendency`: moderate

**CP-MITT — Mitteldeutsch/Fränkisch:**
Engere, unregelmäßige Ständerstellung — Abstand folgt programmatischen
Anforderungen, nicht einem Rastermodul. Stockwerksbau setzt sich früher
durch als im Norden. Wilder Mann: asymmetrische Strebenkombination,
regional charakteristisch. G-STAEND bleibt in ländlichen Bereichen bis
ins 19. Jahrhundert. **[MITTEL]**

Epochensignal: 1556 wurde beim Melsunger Rathaus erstmals die vollendete
Mannform als Strebefigur verwendet. **[HART]**

`post_spacing_m`: 0.6–1.0 (unregelmäßig)
`bracing_pattern`: mann_figur_dominant
`ornament_level`: medium_to_high
`jetty_tendency`: strong
`standerbau_persistence`: late

**CP-OBER — Alemannisch/Schwäbisch:**
Weitständige Fachwerke bis 250 cm lichte Weite erfordern Mannfiguren
und St.-Andreaskreuze als notwendige Aussteifung. In der Schweiz:
strohgedeckte Steildächer im Flachland; schindelgedeckte Tätschdächer
in den Voralpen. **[MITTEL]**

`post_spacing_m`: 0.9–1.3
`bracing_pattern`: corner_band_with_cross
`ornament_level`: low_to_medium
`jetty_tendency`: strong (Städte), low (ländlich)

---

## 9. CulturePolicy: vollständige Parameter-Dimensionen

Die Konstruktionsgrammatik definiert die Parameter, die `CulturePolicy`
pro `(domain, region, epoch_band)` liefert:

```python
@dataclass(slots=True)
class ConstructionCulturePolicy:
    # Achse 1: Ständersystem
    post_system: str           # "standerbau" | "stockwerksbau"
    post_height_m: float       # Geschosshöhe (G-STOCK) oder Gesamthöhe (G-STAEND)
    post_spacing_m: float      # Modul
    post_spacing_mode: str     # "regular" | "irregular"

    # Achse 2: Aussteifung
    bracing_program: str       # "foot_band" | "mann_figur" | "wilder_mann"
                               # | "cross" | "corner_band" | "schwertung"
    brace_angle_deg: float     # bevorzugter Strebenwinkel (45–60°)
    brace_density: str         # "sparse" | "moderate" | "dense"

    # Achse 3: Verbindungen
    joint_type: str            # "blatt" | "zapfen" | "mixed"
    joint_complexity_level: int  # steuert overdimension_factor

    # Achse 4: Infill
    infill_material: str       # "wattle_daub" | "rubble" | "brick" | "plank" | "plaster"
    infill_epoch_transitions: list  # [{year, material}]

    # Auskragung
    jetty_tendency: str        # "none" | "low" | "moderate" | "strong"
    jetty_depth_m: float
    corbel_type: str           # "plain" | "profiled" | "carved"

    # Dimensionierung
    overdimension_factor: float    # kultureller Sicherheitsüberschuss
    max_utilization_ratio: float   # wie nah ans physikalische Limit
```

**Was NICHT in `CulturePolicy` gehört:**

| Parameter | gehört in ... |
|---|---|
| Schnitzwerk-Motiv | StylePolicy (Ornament-Ebene) |
| Farbgebung | StylePolicy |
| Dachneigung | RoofPolicy |
| Fensteranzahl | OpeningsPolicy |
| Gebäudegröße | ArchetypePlanner |
| Querschnittsdimension (mm) | Dimension Solver (aus CulturePolicy abgeleitet) |

---

## 10. Architektonische Entscheidungsmatrix

Checkliste für jeden neuen Parameter: welche Policy-Schicht ist betroffen?

```
Ändert sich der Lastpfad fundamental (Innenständer vs. Außenwände)?
  → ConstructionDomain

Ändert sich die Ständerhöhe über Geschossgrenzen?
  → ConstructionDomain-Branch (G-STAEND vs. G-STOCK)

Ändert sich die Streben-Konfiguration (Anzahl, Figur, Position)?
  → CulturePolicy.bracing_program

Ändert sich der Ständerabstand innerhalb derselben Logik?
  → CulturePolicy.post_spacing_m

Hat die Änderung keine Auswirkung auf Kraftfluss (nur Optik)?
  → StylePolicy

Ist es Mikro-Variation innerhalb erlaubter Grenzen?
  → NoisePolicy
```

---

## 11. Domain-Taxonomie gesamt

```
ConstructionDomain:
  ├── fachwerk.standerbau      (G-STAEND) — Ständer mehrgeschossig
  ├── fachwerk.stockwerksbau   (G-STOCK)  — aktueller BVILLAGE-Core
  ├── fachwerk.firstsaeule     (G-FIRST)  — Firstsäule als Pflicht-member
  ├── fachwerk.cruck           (ENG-CRUCK) — englisch; Wand + Sparren = 1 Holz
  └── fachwerk.hybrid_umgebinde           — zwei simultane Domains

CulturePolicy (moduliert innerhalb einer Domain):
  ├── post_spacing:      weit / mittel / eng / sehr_eng
  ├── bracing_program:   kopf_fuss / mann / andreaskreuz / close_stud
  ├── joint_type:        blattung / zapfung
  ├── utilization_ratio: 0.4–0.7 je Epoche/Region
  └── ornament_level:    strukturell / gemischt / dekorativ / neutral

StylePolicy (ändert keine Lastpfade):
  ├── infill_material:   lehm / ziegel / bohlen / schiefer / putz
  ├── ornament_figures:  faecherrosette / feuerbock / schnitzereien
  └── color_treatment:   sichtholz / verputzt / gefasst
```

---

## 12. Sonderfälle

### 12.1 Hybride Epochen

Einzelne Gebäude zeigen Mischgrammatiken: Reparaturen, Umbauten,
regionale Verzögerungen, konservative Baumeister. Gemischte Grammatik
ist kein HARD Issue, sondern ein SOFT Issue.

### 12.2 Altbayern

In Altbayern (südlich der Donau) sind Fachwerkbauten traditionell
nahezu unbekannt. **[HART]** Das ist eine Region-Domain-Exclusion:
`region = altbayern` → `domain = fachwerk` nicht verfügbar.

### 12.3 Osmanisches Fachwerk

Fachwerkbauten aus den holzreichen Gegenden des ehemaligen Osmanischen
Reichs (Bulgarien bis Syrien) sind eine eigenständige Tradition —
andere Detailgrammatik, aber gleiche Grundlogik (Skelett + Ausfachung).
**[SCHWACH]** Zurückgestellt auf `RES_FACHWERK_OSMANISCH.md`.

---

## 13. Offene Forschungsfelder

| ID | Thema | Status | Zieldokument |
|---|---|---|---|
| KON-001 | Verbindungstechnik: datierte Sequenz für deutschsprachigen Raum analog Hewett (englisch) | Forschungslücke | `RES_VERBINDUNGSTECHNIK.md` |
| KON-002 | Dachsysteme: Neigungswinkel-Dominanzen regional und epochal kartieren | Unvollständig | `RES_DACHSYSTEME.md` |
| KON-003 | Öffnungsgrammatik: Fenster- und Türproportionen nach Epoche und region systematisch | Unvollständig | `RES_OEFFNUNGEN_INNENRAUM.md` |
| KON-004 | Gründung und Schwelle: regionale und epochale Differenzierung | Unvollständig | `RES_GRUNDUNG_SCHWELLE.md` |
| KON-005 | G-FIRST (Firstsäulenbau): member-Topologie vollständig beschreiben | Offen | Dieses Dokument §1 |
| KON-006 | G-BUND (Bundwerk, Vorarlberg/Schweiz): eigene CulturePolicy-Branch definieren | Offen | `RES_BAUGRAMMATIKEN.md` §6 |

---

## 14. Quellen

**Eißing, Thomas; Furrer, Benno; Kayser, Christian et al.:** Vorindustrieller
Holzbau. Terminologie und Systematik für Südwestdeutschland und die
deutschsprachige Schweiz. 2. Aufl. Propylaeum, Heidelberg 2023.
DOI: https://doi.org/10.11588/sbhbf.2023.1.99050

**Klein, Ulrich:** Zum aktuellen Forschungsstand des hoch- und
spätmittelalterlichen Holzbaus in Deutschland. DGAMN-Mitteilungen Bd. 24.
Paderborn 2012. DOI: https://doi.org/10.11588/dgamn.2012.1.17131

**Gerner, Manfred:** Fachwerk. Instandsetzung, Sanierung, Neubau.
DVA, München 2007.

**Großmann, G. Ulrich:** Der Fachwerkbau in Deutschland. Imhof, 2009.

Kompetenzzentrum Fachwerk / Freilichtmuseum Hessenpark.
Denkmalstiftung Baden-Württemberg (Forschungsgeschichte Schäfer / Münsteraner Kreis).
Arbeitsgemeinschaft Deutsche Fachwerkstädte.

---

*Status: Freigegeben als REFERENCE-Dokument. Version 1.0.*
*© 2026 Alexander Bernardi — CC-BY-SA 4.0*
