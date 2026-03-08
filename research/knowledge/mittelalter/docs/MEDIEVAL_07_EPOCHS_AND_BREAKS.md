# Achse 7 — Epochenstruktur und Brüche
## Der Zeitvektor des mittelalterlichen Bauens

```
Dokument-Typ:  Research Foundation
Achse:         7 von 7
Scope:         BVILLAGE — alle Domains, alle Haustypen
Status:        v1.0
Referenziert von:
  MEDIEVAL_WORLD_OVERVIEW.md
  ARCH_POLICIES.md (StylePolicy, CulturePolicy)
  DEV_ROADMAP.md (RES-001)
Referenziert:
  mittelalterliche_baupraxis_v2.md
  RESEARCH_FACHWERK_HISTORISCH.md
  RESEARCH_FACHWERKBAU.md
Evidenzgrade:
  [HART]   Direkt messbar, datierter Bestand, publizierte Messdaten
  [MITTEL] Wissenschaftlicher Konsens, erschlossen, nicht direkt messbar
  [SCHWACH] Analogieschluss, experimentelle Archäologie, Fachtradition
```

---

## Vorbemerkung: Warum Achse 7 das Rückgrat ist

Die sechs anderen Achsen beschreiben Zustände — wie war die physische Welt,
wie war die Gesellschaft, wie funktionierte Handel. Achse 7 beschreibt die
Bewegung: wie diese Zustände sich veränderten, wann sie sprangen, was die
Sprünge auslöste.

Für BVILLAGE ist das die kritischste Achse, weil sie die Zeitdimension aller
Policy-Parameter strukturiert. Ein `epoch_band`-Parameter ohne Kenntnis der
Brüche, die dieses Band durchziehen, ist eine Interpolation ins Leere.
Bauen im Jahr 1350 und Bauen im Jahr 1380 sind nicht zwei Punkte auf einer
Geraden — zwischen ihnen liegt die Pest.

Diese Achse liefert die Diskontinuitäten, die das System explizit modellieren
muss. Nicht als Sonderfälle, sondern als Strukturelement.

---

## 1. Das Grundmodell: Phasen und Brüche

Die mittelalterliche Baugeschichte folgt keinem linearen Fortschritt.
Sie folgt einem Muster aus langen Phasen relativer Stabilität, die durch
scharfe Brüche unterbrochen werden. Diese Brüche sind nicht gleichmäßig
verteilt — sie clustern um externe Schocks (Seuchen, Kriege, Klimawandel)
und interne Schwellenwerte (Holzmangel, Kapitalschwellen, Wissensreifung).

Das BVILLAGE-Zeitmodell muss dieses Muster abbilden können:

```
Parameterraum
     │
     │  PHASE A          ╱ PHASE B             PHASE C
     │  (stabil)        ╱  (stabil)   BRUCH 2  (stabil)
     │                 ╱             ╲
     │         BRUCH 1 ╱              ╲
     │                ╱                ╲
     └─────────────────────────────────────────────► Zeit
```

Innerhalb einer Phase: graduelle Parameter. Über einen Bruch: Sprung.
Die `StylePolicy`-Zeitachse ist kein Gradient — sie ist stückweise linear
mit definierten Unstetigkeitsstellen.

---

## 2. Die sieben Epochenphasen

### Phase 0 — Vorgeschichte: Pfostenbau (bis ca. 1150)
*Nicht BVILLAGE-Domain, aber Kontext für den Übergang*

Der Pfostenbau dominiert. Holzpfosten direkt in der Erde eingespannt,
keine Schwelle, keine laterale Aussteifung durch Streben. Lebensdauer
30–80 Jahre. Kein Mehrgeschossbau möglich.
[MITTEL — Zimmermann 1998; Klein 2012]

Was bleibt: lokales Handwerkswissen, Klöster als Wissensinseln,
Stabkirchen (Norwegen ab ca. 9. Jh.) als Beweis des holzbautechnisch
Möglichen. [HART für Stabkirchen — erhaltene Bauten; MITTEL für
Wissensinfrastruktur]

**BVILLAGE-Status**: Vorläufer der Domain. Kein Planer vorgesehen.
Relevant als Ausgangszustand für die Parameterinitialisierung der
Frühphase.

---

### Phase 1 — Frühphase: Entstehung des Ständerbaus (ca. 1150–1300)

#### Der entscheidende Schritt

Der Ständer verlässt die Erde. Er steht auf Stein oder auf einer Schwelle.
Diese minimale Verschiebung hat maximale Konsequenz: keine Bodenfäulnis,
Mehrgeschossbau möglich, Verbindungen statt Einbettung als Stabilitätsprinzip.
[MITTEL — Zimmermann 1998]

Dendrochronologisch fassbar: Die ältesten erhaltenen deutschen Fachwerkhäuser
datieren auf 1262/63 (Heugasse 3, Esslingen) und 1266/67 (Webergasse 8,
Esslingen). In Limburg an der Lahn sind sechs Häuser aus 1289–1296 bekannt.
[HART — dendrochronologisch: Großmann 2009; Eißing/Furrer 2023]

Für England früher: Cressing Temple Barns, Essex — Barley Barn 1205–1235,
Wheat Barn 1257–1280. [HART — dendrochronologisch: Cecil Hewett; VAG]

#### Konstruktiver Charakter der Phase

- Ständerbau: Ständer laufen von Schwelle bis Traufrähm durch, über
  alle Geschosse. [HART — Klein 2012]
- Kein Schmuck. Keine Bemalung. Konstruktion pur.
- Massive Querschnitte: Unsicherheit über Materialverhalten erzeugt
  Überdimensionierung. [MITTEL — Eißing/Furrer 2023]
- Klein (2012) belegt für den Grabungsbefund Romrod (Hessen, ca. 1170/80):
  Blockbau, Rahmenbau und Ständerbau kommen nebeneinander vor.
  Domänenreinheit ist eine spätere Entwicklung. [HART — Klein 2012]

#### Gleichzeitigkeit: Romanik als Lernprozess

Frühe romanische Gewölbe kollabierten häufig. Die Reaktion war empirisch:
dickere Wände, kleinere Fenster. Romanische Schwere ist materialisierter
Sicherheitspuffer, kein Stilmittel. [MITTEL — Binding 1993; Fitchen 1961]

Ab ca. 1150: permanente Bauhütten an großen Baustellen — Werkstatt, Schule,
Archiv. Wissenstransfer beginnt sich zu institutionalisieren.
[MITTEL — Recht 1989; Binding 1993]

#### BVILLAGE-Parameter dieser Phase

| Parameter | Wert | Evidenz |
|---|---|---|
| `construction_system` | Ständerbau, Pfostenbau koexistierend | HART |
| `post_height_mode` | durchgehend (geschossübergreifend) | HART |
| `ornament_level` | 0 — keine Ornamentik | HART |
| `infill_type` | Flechtwerk + Lehmbewurf dominant | MITTEL |
| `section_overdimension` | 1.5–2.0× (hoher Sicherheitspuffer) | MITTEL |
| `knowledge_tier` | rural vernacular / frühe Zunftansätze | MITTEL |

---

### Phase 2 — Hochmittelalterliche Reife: Typenbildung (ca. 1300–1350)

#### Stabilisierung und Differenzierung

Die Ständerbaukonstruktion ist etabliert. Regionale Grammatiken beginnen
sich herauszubilden: Das norddeutsche Hallenhaus nimmt seine kanonische
dreischiffige Form an. Das mitteldeutsche Ernhaus differenziert sich.
Der städtische Giebelständer entwickelt sich zur dominanten Stadtform
auf schmalen Parzellen. [MITTEL — Großmann 2009; Stiewe 2007]

Der Übergang zum Stockwerksbau beginnt — regional unterschiedlich, im
Süden früher als im Norden. Klein (2012) datiert den Prozess ins
Spätmittelalter; bis ins 16. Jahrhundert wird das Gebindeprinzip
beibehalten. [HART — Klein 2012]

Erste Vorkragungen erscheinen. Zunächst konstruktiv begründbar
(mehr Wohnfläche), bald repräsentativ. [MITTEL — Großmann 2009]

Erste einfache Schmuckelemente: Knaggen, Profilierungen, Ziegelinfill
in Norddeutschland häufiger. [MITTEL — Stiewe 2007]

Wassersägemühlen ab ca. 13.–14. Jahrhundert regional verfügbar —
standardisiertere Querschnitte, höheres Volumen, aber strukturell
schwächeres Holz (Schnitt quer zur Faser). Kompensiert durch leichte
Überdimensionierung. [MITTEL — Eißing/Furrer 2023]

#### BVILLAGE-Parameter dieser Phase

| Parameter | Wert | Evidenz |
|---|---|---|
| `construction_system` | Ständerbau dominant, Stockwerksbau beginnend | HART |
| `ornament_level` | 1 — einfach (Profilierung, Knaggen) | MITTEL |
| `infill_type` | Lehm + zunehmend Ziegel (regional) | MITTEL |
| `jetty_allowed` | ja, einfach | MITTEL |
| `section_overdimension` | 1.3–1.6× | MITTEL |
| `knowledge_tier` | städtische Zünfte etabliert | MITTEL |

---

### BRUCH 1 — Die Pest (1347–1353)

Dies ist der schärfste Einzelbruch in der mittelalterlichen Baugeschichte
Westeuropas. Er verändert nicht die Konstruktionstechnik — er verändert
alles andere, woraus Bauen entsteht: Bevölkerung, Kapital, Arbeitskraft,
Eigentumsstruktur.

#### Was geschah

Die Pest erreicht Westeuropa 1347 über sizilianische Häfen. Bis 1353
ist sie durch den Kontinent gezogen. Sterblichkeit: 30–60 % der Bevölkerung.
[MITTEL — Benedictow 2004 für obere Grenze; breite Debatte]

Für Deutschland und die deutschsprachigen Gebiete gilt eine Sterblichkeit
von ca. 25–40 % als Konsens. [MITTEL — Herlihy 1997; Ziegler 1969]

Rückfälle: 1360–1363, 1374, 1400, 1438, weitere bis ins 16. Jahrhundert.
Die Pest ist kein einmaliges Ereignis — sie ist ein demographisches Regime,
das 150 Jahre anhält. [HART — dokumentiert in Stadtchroniken; Benedictow 2004]

#### Bauliche Konsequenzen

**Baulücken und Erbschaften**: In wenigen Jahren ändern massenhaft Häuser
den Eigentümer. Erben ohne Baukenntnis, Häuser ohne Unterhalt. Das erklärt
den Verfall großer Bestände in der zweiten Hälfte des 14. Jahrhunderts.
[MITTEL — Herlihy/Klapisch-Zuber 1985 für Florenz; übertragbar]

**Wiederaufbauboom ab ca. 1360–1380**: Überlebende erben Kapital, Grundstücke
werden frei, Neubaudruck entsteht. Dendrochronologisch nachweisbar: eine
Häufung von Bauakten aus den 1360er–1390er Jahren.
[HART — Eißing/Furrer 2023; Großmann 2009]

**Arbeitskraftmangel**: Weniger Zimmerleute, höhere Löhne, Druck zur
Rationalisierung. Das beschleunigt die Verbreitung von Vorfertigung
(Abbund) und effizienter Konstruktionsgrammatik. [MITTEL — Epstein 1998]

**Wichtig für BVILLAGE**: Die Pest ist kein `StylePolicy`-Gradient. Sie ist
ein Unstetigkeitspunkt. Parameter, die 1346 galten, gelten 1355 nicht mehr —
nicht weil sich Technik entwickelt hat, sondern weil die soziale Trägermasse
zusammengebrochen ist und neu aufgebaut wird.

---

### Phase 3 — Spätmittelalterliche Blüte: Stockwerksbau und Ornament (ca. 1360–1520)

#### Der Wiederaufbau als Innovationsschub

Die Jahrzehnte nach der Pest sind, paradoxerweise, eine Blütezeit des
städtischen Bauens. Konzentriertes Kapital bei weniger Eigentümern,
freie Bauplätze, erfahrene Handwerker mit höheren Löhnen — die Bedingungen
für ambitioniertere Bauten sind günstig. [MITTEL — Boockmann 1987; Herlihy 1997]

#### Stockwerksbau setzt sich durch

Jedes Stockwerk als eigenständige Rahmenkonstruktion — Schwelle, Ständer,
Rähm — wird zur dominanten Bauweise. Kurze Hölzer genügen; das erleichtert
Beschaffung in zunehmend entwaldetem Stadtumland. Mehrgeschossige Gebäude
(4–8 Stockwerke) werden problemlos möglich. [HART — Klein 2012]

Vorkragungen nehmen zu: jedes Stockwerk leicht nach vorn auskragend,
Flächengewinn im Obergeschoss. Großmann (2009) und Stiewe (2007)
dokumentieren dies als etablierte Praxis ab dem 15. Jahrhundert.
[MITTEL — Großmann 2009; Stiewe 2007]

#### Das ornamentale Zeitalter

Das 15. und frühe 16. Jahrhundert ist die Hochphase der Fachwerkornamentik.
Andreaskreuze, Fächerrosetten, Treppenfriese, Kettenbänder, Heiligenfiguren
an Knaggen — das Fachwerk dieses Jahrhunderts ist Ausdrucksmittel für
Reichtum, Zunftzugehörigkeit und Repräsentation.
[MITTEL — Großmann 2009; Kaspar 1986]

In Franken — dem mitteldeutschen Fachwerk — erreicht die Ornamentik ihren
Höhepunkt. In Braunschweig, Hildesheim, Wernigerode entstehen die
prachtvollsten erhaltenen Bürgerhäuser. [HART für Bestand; MITTEL für Deutung]

Kanonische Beispiele: Hoppener Haus, Celle (1532); Baumannsches Haus,
Eppingen (1582); Knochenhaueramtshaus, Hildesheim (1529).
[HART — dendrochronologisch oder urkundlich datiert]

#### BVILLAGE-Parameter dieser Phase

| Parameter | Wert | Evidenz |
|---|---|---|
| `construction_system` | Stockwerksbau dominant | HART |
| `post_height_mode` | geschossweise | HART |
| `ornament_level` | 2–4 (regional sehr unterschiedlich) | MITTEL |
| `jetty_allowed` | ja, mehrfach | MITTEL |
| `jetty_depth_m` | 0.3–0.8 (bis 1.0 in Extremfällen) | MITTEL |
| `infill_type` | Ziegel zunehend dominant (Nord), Lehm (Mitte/Süd) | MITTEL |
| `section_overdimension` | 1.2–1.4× | MITTEL |
| `knowledge_tier` | städtische Zünfte vollentwickelt | MITTEL |
| `storey_count_max` | 7–8 (Patrizier), 2–4 (Handwerker) | MITTEL |

---

### BRUCH 2 — Holzmangel und Bauordnungen (ca. 1400–1520, regional gestaffelt)

Kein einzelnes Ereignis — ein schleichender Strukturwandel, der in manchen
Städten früher, in anderen später zur Krise wird. Aber er ist real und
dendrochronologisch nachweisbar als Veränderung der verwendeten Holzarten
und Querschnitte.

#### Holzmangel

Städtische Wachstumsdruck entwaldet das Umland. Lange, gerade Stämme
für den Ständerbau werden knapper und teurer. Das beschleunigt den
Übergang zum Stockwerksbau (kürzere Ständer) und erhöht den Anteil
importierten Holzes. [HART — Eißing/Furrer 2023; Marstaller 2012]

Eißing (2023) belegt Holztransporte über weite Distanzen auf Wasserläufen
als normale Praxis — Gebäudestandort und Waldstandort divergieren
zunehmend. [HART]

#### Städtische Bauordnungen

Als Reaktion auf verheerende Stadtbrände — Lübeck 1251, Wien 1258,
und zahllose kleinere im 14.–15. Jahrhundert — erlassen Städte
Bauordnungen: Mindestabstände, Verbote für Strohdeckungen,
Vorkragungsbeschränkungen. [MITTEL — Stiewe 2007; Boockmann 1987]

Diese Normen variieren stark zwischen Städten und entwickeln sich
langsam. Sie sind kein uniformer Bruch, sondern lokale Diskontinuitäten.

**BVILLAGE-Implikation**: `ConstraintsPolicy` für städtische Kontexte
muss lokale Bauordnungen als Hard-Constraints abbilden können — mit
spatiotemporaler Gültigkeit, nicht als universelle Regel.

---

### Phase 4 — Renaissance und Frühbarock: Technisches Fachwerk (ca. 1520–1618)

#### Standardisierung und Rationalisierung

Die ornamentale Hochphase klingt ab. An ihre Stelle tritt ein technischeres
Fachwerk: regelmäßigere Ständerabstände, klare Raster, reduzierte aber
präzisere Ornamentik. Die Wassersägemühle hat sich durchgesetzt —
Querschnitte werden normierter. [MITTEL — Eißing/Furrer 2023; Klein 2012]

Renaissance-Einflüsse erreichen das Fachwerk über Ornamentmotive
(Pilaster, Medaillons, antikisierende Friese), weniger über Konstruktion.
Das Baumansche Haus in Eppingen (1582) zeigt diese Verbindung.
[MITTEL — Großmann 2009]

In der Schweiz: das Riegelhaus als schlichtes, konstruktionsbetontes
Fachwerk setzt sich durch. Ornament tritt zurück, Präzision wächst.
[MITTEL — Eißing/Furrer 2023]

#### BVILLAGE-Parameter dieser Phase

| Parameter | Wert | Evidenz |
|---|---|---|
| `construction_system` | Stockwerksbau, vollständig standardisiert | HART |
| `ornament_level` | 1–3 (reduziert, aber präziser) | MITTEL |
| `section_variation` | geringer (Säge normiert Querschnitte) | MITTEL |
| `knowledge_tier` | Zunftsystem vollentwickelt, erste Regelwerke | MITTEL |

---

### BRUCH 3 — Der Dreißigjährige Krieg (1618–1648)

Der schwerste politische Schock der frühen Neuzeit in Mitteleuropa.
Für die Baugeschichte ist er der zweite große Diskontinuitätspunkt
nach der Pest — und in seinen Baukonsequenzen präzise dokumentiert.

#### Was geschah

Flächendeckende Kriegszüge, systematische Brandschatzung, Seuchenzüge
in der Folge. Bevölkerungsverluste in Deutschland: regional 20–60 %.
Manche Landstriche verloren mehr als die Hälfte ihrer Einwohner.
[MITTEL — Brzezinski 2001; Parker 1984]

Für Württemberg sind 57 % Bevölkerungsverlust belegt. Für Pommern,
Mecklenburg, Teile Thüringens ähnliche Größenordnungen.
[MITTEL — Wilson 2009]

#### Bauliche Konsequenzen

**Direkte Zerstörung**: Viele Städte brennen vollständig nieder —
Magdeburg 1631 (nahezu vollständige Vernichtung), Heidelberg, zahlreiche
kleinere Orte. [HART — historisch dokumentiert]

**Ressourcenknappheit**: Holz knapper, Kapital vernichtet, Arbeitskraft
dezimiert. Das Fachwerk reagiert sichtbar: Querschnitte werden schlanker,
Ständerabstände größer, Ornamentik massiv reduziert.
[MITTEL — Stiewe 2007; Großmann 2009]

**Wiederaufbau unter anderen Bedingungen**: Nach 1648 entsteht vieles
neu — aber rationaler, schlichter. Das Rasterfachwerk des späten
17. Jahrhunderts ist Effizienzfachwerk. [MITTEL — Stiewe 2007]

**BVILLAGE-Implikation**: Der Dreißigjährige Krieg erzeugt zwei
voneinander zu trennende Parameterzustände: Vorkrieg (Phase 4) und
Nachkrieg (Phase 5) — mit einem expliziten Sprung, nicht einem Gradient.
Regional variiert der Schock stark: Nordseeküste und Schweiz weniger
betroffen; Mitteldeutschland am stärksten.

---

### Phase 5 — Wiederaufbau und Rationalfachwerk (ca. 1650–1750)

#### Schlankeres Bauen

Die Konstruktion bleibt dieselbe. Aber das System wirtschaftet mit weniger
Material. Querschnitte schlanker. Ständerabstände größer. Keine aufwendigen
Schnitzereiarbeiten. Das Fachwerk wird zum Zweckbau.
[MITTEL — Stiewe 2007; Großmann 2009]

In manchen Regionen — besonders Südwestdeutschland, Schweiz — entsteht
nach dem Krieg das technische Rasterfachwerk: regelmäßige Gefache,
zurückliegende Sichtziegelausfachung, kein Schmuck. [MITTEL — Eißing/Furrer 2023]

#### Verputzen als Statusgeste

Das Verputzen der Außenwände beginnt sich zu verbreiten — aus zwei
unterschiedlichen Gründen gleichzeitig: Witterungsschutz für das
geschädigte Gefüge und Statusanspruch (Putz wirkt wie Steinbau).
[MITTEL — Stiewe 2007]

#### BVILLAGE-Parameter dieser Phase

| Parameter | Wert | Evidenz |
|---|---|---|
| `construction_system` | Stockwerksbau | HART |
| `ornament_level` | 0–1 | MITTEL |
| `section_overdimension` | 1.0–1.2× (Sparsamkeit) | MITTEL |
| `facade_treatment` | zunehmend verputzt | MITTEL |
| `infill_type` | Ziegel dominant | MITTEL |

---

### BRUCH 4 — Statuswandel und Industrialisierung (ca. 1750–1900)

Kein einzelnes Ereignis, sondern ein kultureller und technologischer
Strukturwandel, der das Ende des historischen Fachwerkbaus herbeiführt.

**Statuswandel**: Im 18. und 19. Jahrhundert gilt sichtbares Fachwerk
als Zeichen von Armut und Rückständigkeit. Wer es sich leisten kann,
verputzt oder baut in Stein. [MITTEL — Stiewe 2007]

**Brandschutzgesetzgebung**: Stadtbrände (Hamburg 1842 u. a.) erzwingen
Verbote für Holzfassaden in Städten. [HART — gesetzlich dokumentiert]

**Industrialisierung**: Maschinell produzierter Ziegel, Portlandzement,
schließlich Stahl und Beton machen den Holzrahmenbau technisch überholbar.
Der letzte genuine städtische Fachwerkbau entsteht um 1900.
[HART — Großmann 2009; Stiewe 2007]

**BVILLAGE-Status**: Außerhalb des modellierten Zeitraums. Relevant als
obere Grenze der `epoch_band`-Parameter.

---

## 3. Die Epochenmatrix: Schnellreferenz für Policy-Parameter

Diese Matrix fasst die wichtigsten Parametersprünge zusammen. Sie ist
keine vollständige Parametertabelle — die liegt in den Domain- und
Policy-Dokumenten. Sie ist eine Navigationshilfe: Wo sind die
Diskontinuitäten, die explizit modelliert werden müssen?

| Epoche | Construction | Ornament | Infill | Section | Jetty | Trigger |
|---|---|---|---|---|---|---|
| ~1150–1300 | Ständer | 0 | Flechtwerk/Lehm | 1.5–2.0× | nein | — |
| 1300–1347 | Ständer→Stockwerk | 1 | Lehm+Ziegel | 1.3–1.6× | einfach | Wachstum |
| **BRUCH: PEST 1347** | | | | | | **−30–60% Bevölkerung** |
| 1360–1520 | Stockwerk | 2–4 | Ziegel/Lehm | 1.2–1.4× | mehrfach | Wiederaufbau |
| 1520–1618 | Stockwerk | 1–3 | Ziegel | norm. | mehrfach | Rationalisierung |
| **BRUCH: 30J. KRIEG 1618** | | | | | | **−20–60% regional** |
| 1650–1750 | Stockwerk | 0–1 | Ziegel | 1.0–1.2× | selten | Effizienz |
| >1750 | Stockwerk (auslauf.) | Revival | Ziegel/Putz | dünn | — | Statuswandel |

**Lesehinweis**: Die Brüche sind keine Parameterübergänge — sie sind
Unstetigkeitsstellen. Ein Gebäude, das 1346 gebaut wurde, hat andere
Parameter als eines, das 1355 gebaut wurde — nicht wegen technischer
Entwicklung, sondern wegen demographischer und ökonomischer Disruption.

---

## 4. Regionale Schichtung der Zeitachse

Die Epochenphasen verlaufen nicht uniform über Europa. Sie sind regional
geshiftet. Das ist kein Makel der Datenbasis — es ist historische Realität.

### Konstruktionssystemwechsel (Ständer → Stockwerk)

| Region | Beginn | Dominanz | Quelle |
|---|---|---|---|
| Süddeutschland (Esslingen, Ulm) | ~1300 | ~1400 | MITTEL — Klein 2012 |
| Mitteldeutschland (Hessen, Thüringen) | ~1350 | ~1450 | MITTEL |
| Norddeutschland (Städte) | ~1400 | ~1500 | MITTEL |
| Norddeutschland (ländlich) | ~1450 | ~1600 | MITTEL |
| Niederdeutsches Hallenhaus (ländlich) | persistiert bis 19. Jh. | — | HART |

Das niederdeutsche Hallenhaus ist ein Sonderfall: Es behält den Ständerbau
(hier als Bauweise für Großräume, nicht als Rückständigkeit) bis weit ins
19. Jahrhundert. Das zeigt, dass Konstruktionssystemwechsel funktional
motiviert sind, nicht zeitlich deterministisch. [HART — Stiewe 2007]

### Pestbetroffenheit (1347–1353)

| Region | Geschätzte Sterblichkeit | Quelle |
|---|---|---|
| Städtische Zentren | 40–60 % | MITTEL |
| Ländliche Gebiete | 20–40 % | MITTEL |
| Nordseeküste/Friesland | 15–25 % (geringer) | MITTEL |
| Skandinavien | 30–50 % | MITTEL |

### Dreißigjähriger Krieg (1618–1648)

| Region | Betroffenheit | Baukonsequenz |
|---|---|---|
| Württemberg, Pfalz | sehr hoch (>50% Verlust) | starke Schlankung | 
| Sachsen, Thüringen | hoch (30–50%) | deutliche Schlankung |
| Bayern | mittel (20–30%) | moderate Schlankung |
| Nordseeküste, Schweiz | gering (<15%) | kaum verändert |
| Österreich | mittel | — |

[Alle Werte: MITTEL — Wilson 2009; Parker 1984]

**BVILLAGE-Implikation**: Der `epoch_band`-Parameter allein reicht nicht.
Er braucht eine `region`-Dimension, um die regionale Schichtung
abzubilden. Die `StylePolicy`-Lookup-Logik muss `(epoch, region)` als
kombiniertes Tupel auflösen, nicht als unabhängige Parameter.

---

## 5. Zeitliche Schocks als BVILLAGE-Systemkonzept

### Was ein Schock ist

Ein Schock im BVILLAGE-Sinne ist ein historisches Ereignis, das:

1. Innerhalb weniger Jahre messbar verändert, welche Gebäude gebaut werden
2. Nicht durch graduelle Parameterinterpolation abbildbar ist
3. Räumlich differenziert wirkt (nicht uniform über alle Regionen)
4. Dokumentiert und datierbar ist (keine Spekulation)

Die drei mittelalterlichen Hauptschocks erfüllen alle vier Kriterien:
Pest, Dreißigjähriger Krieg, und — schwächer, aber real — der Holzmangel
des 15. Jahrhunderts.

### Wie Schocks in Policies abgebildet werden

Schocks sind keine `StylePolicy`-Parameter. Sie sind Zustandswechsel,
die den Parameterraum umschalten. Das Modell:

```
resolve_policy(epoch, region) →
  if epoch in SHOCK_ZONES[(region)]:
    return SHOCK_STATE[(epoch, region)]
  else:
    return interpolate(PHASE_BEFORE, PHASE_AFTER, t)
```

Die Schockzonen sind nicht scharf datiert — sie haben Unsicherheits-
bänder. Die Pest erreicht verschiedene Regionen zu verschiedenen Zeiten
(1347–1351 für den Kern, bis 1353 für die Peripherie). Das Modell
muss diese Unschärfe explizit repräsentieren, nicht weginterpolieren.

### Nachwirkungen

Schocks haben Nachwirkungen, die länger dauern als der Schock selbst.
Die Pest erzeugt 150 Jahre demographische Instabilität (Wiederholungsepidemien
bis ins 16. Jahrhundert). Der Dreißigjährige Krieg braucht in manchen
Regionen 100 Jahre, bis die Bevölkerung vorkiegsniveau erreicht.

In Parametertermen: Die Rückkehr zu Vorschockwerten ist nicht linear
und nicht universell. Manche Regionen erholen sich schnell (Kapitalzufluss,
günstiger Wiederaufbau). Andere persistieren jahrzehntelang im
Nachschockzustand.

---

## 6. Offene Forschungsfragen für BVILLAGE

Diese Fragen sind aus dem aktuellen Wissensstand nicht vollständig
beantwortbar. Sie markieren die Grenzen der Datenbasis.

**Frage 1 — Regionale Datierung des Konstruktionswechsels**
Klein (2012) liefert Orientierung, aber keine vollständige regionale
Karte. Für viele Regionen (Schleswig-Holstein, Bayern, Österreich) fehlen
dendrochronologische Studien in ausreichender Dichte. Die MITTEL-Einstufung
der regionalen Schichtungstabelle reflektiert das.

**Frage 2 — Pestdemographie für Baukontexte**
Benedictow (2004) und andere liefern Gesamtsterblichkeit. Aber für die
Baupolitik relevant ist: Wie veränderte sich der Anteil der Handwerker?
Wie die Kapitalkonzentration? Das ist für die meisten Regionen
nicht direkt belegt.

**Frage 3 — Querschnittsentwicklung über Epochen**
Eißing/Furrer (2023) und Klein (2012) liefern Messpunkte. Aber eine
vollständige, regionsübergreifende Querschnittskurve über die Epochen
fehlt. Die Schlankungs-These für den Nachkriegskontext ist gut begründet,
aber quantitativ noch nicht dicht belegt.

**Frage 4 — Erste Bauordnungen: Wann, wo, mit welchen Konsequenzen?**
Bauordnungen sind stadtrechtlich dokumentiert, aber nicht systematisch
für alle relevanten Städte ausgewertet. Die `ConstraintsPolicy` bräuchte
hier eine eigene Forschungsgrundlage.

---

## 7. Quellen und wissenschaftliche Grundlage

### 7.1 Zitierte Werke

**Benedictow, Ole J.:** The Black Death 1346–1353. The Complete History.
Woodbridge: Boydell Press, 2004. ISBN 978-0-85115-943-2.
*Umfassendste Studie zur Pestmortalität. Argumentiert für ca. 60 %
Gesamtsterblichkeit in Westeuropa. Wissenschaftlich kontrovers, methodisch
am gründlichsten. Hauptreferenz für Bruch 1.*
[MITTEL — Schätzwerte, keine direkten Messungen]

**Binding, Günther:** Baubetrieb im Mittelalter. Darmstadt: WBG, 1993.
*Bauorganisation, Maßsysteme, Bauhütten. Relevant für Phasen 1 und 2.*

**Boockmann, Hartmut:** Die Stadt im späten Mittelalter. München: Beck, 1987.
*Sozialgeschichte der spätmittelalterlichen Stadt. Relevant für Phasen 2–4.*

**Brzezinski, Richard:** The Army of Gustavus Adolphus. Oxford: Osprey, 2001.
*Für Dreißigjährigen Krieg: militärhistorischer Hintergrund.*
[MITTEL]

**Eißing, Thomas; Furrer, Benno; Kayser, Christian et al.:** Vorindustrieller
Holzbau. Terminologie und Systematik für Südwestdeutschland und die
deutschsprachige Schweiz. 2. Aufl. Heidelberg: Propylaeum, 2023.
ISBN 978-3-96929-223-5.
DOI: https://doi.org/10.11588/sbhbf.2023.1.99050 — PDF frei zugänglich.
*Verbindliches Terminologiewerk. Dendrochronologische Methodik und Befunde.
Primärquelle für Holztransport, Querschnittsentwicklung, Grünholzverbau.*
[HART]

**Epstein, Stephan R.:** Craft Guilds, Apprenticeship, and Technological
Change in Preindustrial Europe. In: Journal of Economic History 58 (1998),
H. 3, S. 684–713.
*Zunftsystem als Wissenstransfer-Institution. Relevant für Arbeitskraft-
reaktion nach Pestschock.*
[MITTEL]

**Fitchen, John:** The Construction of Gothic Cathedrals. Chicago: University
of Chicago Press, 1961. Neuauflage 1981.
*Ingenieurwissenschaftliche Analyse mittelalterlicher Bautechnik.
Relevant für Phase 1 (Romanik als Lernprozess).*

**Großmann, G. Ulrich:** Der Fachwerkbau in Deutschland. Petersberg: Imhof,
2009. ISBN 978-3-86568-449-2.
*Maßgebendes Überblickswerk. Konstruktionsgeschichte, Ornamentik, Regional-
ausprägungen. Vorkragung als Repräsentationsmerkmal. Relevant für alle Phasen.*
[MITTEL]

**Herlihy, David:** The Black Death and the Transformation of the West.
Cambridge: Harvard University Press, 1997.
*Kompakte Synthese der Pestfolgen für Wirtschaft und Gesellschaft.
Beste Einführung für den thematischen Überblick.*
[MITTEL]

**Hewett, Cecil A.:** English Historic Carpentry. Fresno: Linden Publishing,
1997 (Erstaufl. 1980). ISBN 978-0-941936-41-5.
*Typologische Referenz für englischen Holzbau. Cressing Temple Barns.*
[MITTEL — metrisch eingeschränkt belastbar]

**Kaspar, Fred:** Fachwerkbauten des 14. bis 16. Jahrhunderts in Westfalen.
Münster: Coppenrath, 1986. ISBN 3-88547-298-8.
*Regionalmonographie mit Bestandsaufnahme. Ornamentik und Konstruktion
im Westfalenkontext. Relevant für Phasen 2–4.*
[MITTEL/HART]

**Klein, Ulrich:** Zum aktuellen Forschungsstand des hoch- und
spätmittelalterlichen Holzbaus in Deutschland. In: DGAMN-Mitteilungen,
Bd. 24. Paderborn 2012, S. 9–38.
DOI: https://doi.org/10.11588/dgamn.2012.1.17131 — PDF frei zugänglich.
*Schlüsselpublikation. Dendrochronologische Datierung des Konstruktions-
systemwechsels. Coexistenz der Baudomänen im 12./13. Jh.*
[HART]

**Marstaller, Tilmann:** Zu Lande und zu Wasser. Bauholzimporte des 12.–17.
Jahrhunderts im mittleren Neckarraum. In: DGAMN-Mitteilungen Bd. 24.
Paderborn 2012, S. 39–56.
*Dendrochronologische Nachweise für überregionalen Holztransport.
Relevant für Bruch 2 (Holzmangel).*
[HART]

**Parker, Geoffrey:** The Thirty Years' War. London: Routledge, 1984.
2. Aufl. 1997. ISBN 978-0-415-12883-4.
*Standardwerk zum Dreißigjährigen Krieg. Militärischer Verlauf,
demographische Konsequenzen. Relevant für Bruch 3.*
[MITTEL/HART]

**Recht, Roland:** Les Bâtisseurs des cathédrales gothiques. Straßburg:
Éditions des Musées de Strasbourg, 1989.
*Bauhüttenorganisation, Meistermigration, Wissenstransfer.*

**Stiewe, Heinrich:** Fachwerkhäuser in Deutschland. Darmstadt: WBG, 2007.
ISBN 978-3-534-18714-1.
*Konstruktionsgeschichte und Sozialgeschichte. Niedergang und Statuswandel.
Relevant für Phasen 4 und 5.*

**Wilson, Peter H.:** The Thirty Years War. Europe's Tragedy. Cambridge:
Belknap Press, 2009. ISBN 978-0-674-03634-5.
*Umfassendste neuere Darstellung des Dreißigjährigen Krieges.
Demographische Daten, regionale Differenzierung.*
[MITTEL/HART]

**Zimmermann, W. Haio:** Pfosten, Ständer und Schwelle und der Übergang
vom Pfosten- zum Ständerbau. Eine Studie zu Innovation und Beharrung im
Hausbau. In: Probleme der Küstenforschung im südlichen Nordseegebiet,
Bd. 25. Oldenburg 1998, S. 9–241.
*Grundlegende Studie zum Übergang vom Pfostenbau zum Ständerbau.
Relevant für Phase 0 → Phase 1.*
[MITTEL/HART]

**Ziegler, Philip:** The Black Death. London: Collins, 1969. Neuauflage
Penguin 2003. ISBN 978-0-14-027524-7.
*Klassische englischsprachige Darstellung der Pest. Narrativer Zugang,
gut zugänglich. Als Einstieg geeignet; für Quantitatives: Benedictow.*

---

### 7.2 Weiterführende Literatur

**Aston, Trevor H. (Hrsg.):** The Brenner Debate. Agrarian Class Structure
and Economic Development in Pre-Industrial Europe.
Cambridge: Cambridge University Press, 1985.
*Kontroverse um Feudalkrise, Bevölkerungsrückgang, agraren Wandel
im Spätmittelalter. Strukturgeschichtlicher Hintergrund für Phase 3.*

**Cohn, Samuel K. Jr.:** The Black Death Transformed.
London: Arnold, 2002.
*Kritische Neubewertung. Kontrastpunkt zu Benedictow.*

**Dyer, Christopher:** Standards of Living in the Later Middle Ages.
Cambridge: Cambridge University Press, 1989.
*Lebensstandards, Haushaltsgrößen, materielle Kultur nach der Pest.
Quantitativer Ansatz.*

**Lamb, Hubert H.:** Climate, History and the Modern World.
London: Routledge, 1982. 2. Aufl. 1995.
*Historische Klimatologie. Mittelalterliche Wärmeperiode und
Kleine Eiszeit als Hintergrund für Ressourcenveränderungen.*

---

### 7.3 Primärquellen und Datenbanken

**Dendrochronologische Datenbanken**

International Tree-Ring Data Bank (ITRDB):
https://www.ncei.noaa.gov/products/paleoclimatology/tree-ring
*Referenzchronologien für epochale Klimarekonstruktionen.*

Labor für Dendrochronologie und Gefügekunde, Universität Bamberg (T. Eißing):
Über 5.500 untersuchte historische Gebäude mit 45.000+ Proben.
*Direkte Quelle für Datierungen und Holztransportnachweise.*

**Stadtchroniken und Ratsprotokoll-Editionen**

Die Quellengrundlage für lokale Bauordnungen liegt in städtischen
Archiven und deren Editionen. Einschlägige Reihen:
- Quellen zur Geschichte der Stadt Köln
- Urkundenbuch der Stadt Lübeck
- Frankfurter Bürgerbuch

Diese Quellen sind für `ConstraintsPolicy`-Forschung (Bauordnungen,
Vorkragungsrechte, Brandschutzregeln) die primäre Datenbasis.

---

*BVILLAGE Research Foundation — Achse 7 — v1.0*
