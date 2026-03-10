# Achse 1 — Die physische Welt
## Klima, Geographie, Rohstoffe als Fundament des Bauens

```
Dokument-Typ:  Research Foundation
Achse:         1 von 7
Scope:         BVILLAGE — alle Domains, alle Haustypen
Status:        v1.0
Referenziert von:
  MEDIEVAL_WORLD_OVERVIEW.md
  ARCH_POLICIES.md (StylePolicy, MaterialPolicy)
  MEDIEVAL_04_ECONOMY_TRADE.md (Rohstoffflüsse)
  MEDIEVAL_07_EPOCHS_AND_BREAKS.md (Klimabrüche)
Evidenzgrade:
  [HART]   Direkt messbar, datierter Bestand, publizierte Messdaten
  [MITTEL] Wissenschaftlicher Konsens, erschlossen, nicht direkt messbar
  [SCHWACH] Analogieschluss, experimentelle Archäologie, Fachtradition
```

---

## Vorbemerkung

Die physische Welt ist die Schicht, die am wenigsten verhandelt. Klima,
Geologie und Waldbestand sind nicht kulturell konstruiert — sie sind die
Bedingungen, unter denen Kultur operiert. Für BVILLAGE bedeutet das:
Achse 1 liefert die Constraints, in denen alle anderen Achsen sich bewegen.

Gleichzeitig gilt: Die physische Welt ist nicht statisch. Das Klima des
Jahres 1050 unterscheidet sich messbar vom Klima des Jahres 1400. Wälder
verändern sich durch Rodung. Flüsse ändern ihre Läufe. Achse 1 muss
daher ebenso epochal differenziert werden wie die anderen Achsen.

---

## 1. Klima

### 1.1 Die Mittelalterliche Wärmeperiode (ca. 950–1250)

Die Mittelalterliche Wärmeperiode (Medieval Warm Period, MWP) ist
dendrochronologisch und durch Eiskerne dokumentiert. Jahresmitteltemperaturen
in Westeuropa lagen ca. 0,5–1,0 °C über dem vorindustriellen Mittel.
[HART — Lamb 1982; Mann et al. 2009; PAGES 2k Consortium 2013]

Konsequenzen für das Bauen:

**Holzverfügbarkeit**: Wärmere, feuchtere Sommer fördern Baumwachstum.
In der MWP sind Wälder dichter und schnellwüchsiger — Bauholz ist
abundanter als in den kühleren Jahrhunderten danach.
[MITTEL — Hoffmann 2014]

**Siedlungsausdehnung**: Die MWP erlaubt landwirtschaftliche Nutzung
höherer Lagen (Mittelgebirge, alpine Vorzone). Neue Siedlungen entstehen
in Randlagen, die später wieder aufgegeben werden. Das treibt den
Bauholzbedarf und — infolge der Rodungen — den Waldverlust.
[MITTEL — Hoffmann 2014; Le Goff 2004]

**Bevölkerungswachstum**: Bessere Ernten, niedrigere Wintersterblichkeit.
Die Bevölkerung Westeuropas verdreifacht sich von ca. 1000 bis 1300.
[MITTEL — Russell 1958; McEvedy/Jones 1978]

**BVILLAGE-Implikation**: Gebäude aus der MWP (ca. 1000–1250) entstehen
unter Bedingungen relativer Holzfülle. Großzügige Querschnitte sind nicht
nur Unsicherheitspuffer — sie sind auch Ausdruck verfügbarer Ressourcen.

### 1.2 Die Kleine Eiszeit (ca. 1300–1850, Kernphase ca. 1430–1850)

Der Übergang von der MWP zur Kleinen Eiszeit ist kein abrupter Bruch,
sondern ein mehrere Generationen dauernder Abkühlungsprozess. Die
dramatischsten Jahrzehnte: 1315–1322 (Große Hungersnot), 1430er,
1590er, 1680er–1710er (Maunderminimum). [HART — Lamb 1982; Büntgen et al. 2011]

Jahresmitteltemperaturen: ca. 0,5–2,0 °C unter modernem Mittel,
je nach Dekade und Region. Für Mitteleuropa besonders relevant:
verlängerte Winter, kürzere Vegetationsperioden, häufigere Missernten.

**Große Hungersnot (1315–1322)**: Mehrjährige Missernten durch
Kälte und Nässe. Bevölkerungsverluste 10–15 % in betroffenen Regionen.
[MITTEL — Jordan 1996]
Baulücke: Diese Jahre sind bauwirtschaftlich eine Delle — kaum
Neubautätigkeit, Ressourcen werden für Nahrung gebraucht.

**Bauliche Konsequenzen der Abkühlung**:
- Härtere, weniger produktive Wälder → schlechteres Holzwachstum
- Schlechtere Ernte → weniger Kapital für Bauten
- Kältere Winter → höhere Anforderungen an Wärmespeicherung der Gebäude
- Längere Schneelasten → konstruktive Anpassungen bei Dachneigungen

[MITTEL — Hoffmann 2014; Lamb 1982]

**BVILLAGE-Implikation**: Ab ca. 1300 gelten andere Ressourcen-
constraints als in der MWP. Der `MaterialPolicy`-Lookup sollte
klimatische Epochenbänder berücksichtigen: Holzquerschnitte werden
knapper und tendenziell schlanker, nicht wegen technischer Reifung
allein, sondern auch wegen realer Materialknappheit.

### 1.3 Regionale Klimadifferenzierung

Das mittelalterliche Europa ist klimatisch stark differenziert. Vier
Großzonen sind für BVILLAGE relevant:

| Zone | Charakteristik | Bau-Implikation |
|---|---|---|
| Atlantische Küste | mild, feucht, windig | Steile Dächer, Steinbau häufiger, frühe Ziegelkultur (Niederlande) |
| Kontinentales Mitteleuropa | kalte Winter, warme Sommer | Lehm + Holz, Stroh gut geeignet |
| Alpenraum | kurze Sommer, Schneelast | Blockbau, steile Dächer, Nadelholz |
| Mediterran (Grenzzone) | trocken, heiß | Kalkstein, Terrakotta, flachere Dächer |

[MITTEL — Lamb 1982; Hoffmann 2014]

---

## 2. Geographie und Landschaft

### 2.1 Die drei Großlandschaften Mitteleuropas

Für die deutschen Baulandschaften, die BVILLAGE primär modelliert,
sind drei Großlandschaften prägend:

**Norddeutsche Tiefebene**
Flaches Gelände, lehmige Böden, Zugang zu Nord- und Ostsee. Kaum
Naturstein. Holz (Eiche, später Kiefer) und — ab dem Spätmittelalter —
Backstein sind die dominanten Materialien. Die Tiefebene ermöglicht
große Ackerflächen und damit Viehwirtschaft in großem Maßstab — das
erklärt das Hallenhaus als dominanten Haustyp.
[MITTEL — Stiewe 2007; Großmann 2009]

**Mittelgebirgszone**
Hessen, Thüringen, Franken, Teile Sachsens. Kupiertes Gelände, gemischte
Wälder (Eiche, Buche, Tanne), lokaler Sandstein und Kalkstein verfügbar.
Die Zone der größten Fachwerkvielfalt — viele Lokalkulturen auf engem Raum.
[MITTEL — Großmann 2009; Stiewe 2007]

**Alpenvorland und Alpen**
Nadelholz dominant (Fichte, Tanne, Lärche). Kalkstein und kristallines
Gestein lokal. Blockbau ist die historische Primärbauweise, Fachwerk
kommt erst spät und bleibt regional.
[MITTEL — Eißing/Furrer 2023]

### 2.2 Wasserläufe als Infrastruktur

Flüsse sind die Autobahnen des Mittelalters. Ihre Bedeutung für den
Baustofftransport ist dendrochronologisch nachgewiesen:

Eißing (2023) und Marstaller (2012) belegen, dass Gebäudestandort und
Waldstandort regelmäßig nicht identisch sind. Holztransporte über
Wasserläufe waren die Regel für größere Mengen. Landtransport blieb
auf kurze Distanzen (< 20–30 km) beschränkt.
[HART — Eißing/Furrer 2023; Marstaller 2012]

Konsequenz: Die `MaterialPolicy` für Holzarten muss nicht nur nach
Kilometerradius vom Gebäude, sondern nach Flussnetz-Erreichbarkeit
modellieren. Ein Gebäude am Rhein kann mit Holz aus dem Schwarzwald
gebaut sein. Eines im Binnenland ohne Flussanbindung fast nie.

**BVILLAGE-Implikation**: Die `region`-Dimension der `MaterialPolicy`
sollte hydrographische Einzugsgebiete als Primärstruktur verwenden,
nicht Luftliniendistanzen.

### 2.3 Höhenlage

Höhenlage moduliert Klima, Materialverfügbarkeit und Siedlungscharakter:

| Höhe | Charakter | Baurelevanz |
|---|---|---|
| < 200 m | Tiefland | Tiefland-Haustypen, Lehm/Ton, ggf. Backstein |
| 200–500 m | Hügelland | Gemischter Wald, Mischkonstruktionen |
| 500–1000 m | Mittelgebirge | Nadelholz zunehmend, Schneelast relevant |
| > 1000 m | Hochlagen | Blockbau, kurze Bausaison, extreme Schneelast |

[MITTEL — Hoffmann 2014; Lamb 1982]

---

## 3. Rohstoffe

### 3.1 Holz

Holz ist der primäre Baustoff des mittelalterlichen Mitteleuropas. Kein
anderes Material ist so universell einsetzbar, so lokal verfügbar, so gut
mit handwerklichen Mitteln bearbeitbar.

#### Holzarten und ihre Eigenschaften

**Eiche (Stiel- und Traubeneiche)**
Verbreitung: Tieflagen, Mittelgebirgsränder, Norddeutschland.
Eigenschaften: Druckfestigkeit ~50–55 MPa [HART], Biegefestigkeit ~80–100 MPa
[HART], Dichte frisch ~900 kg/m³, trocken ~680–720 kg/m³ [HART].
Dauerhaftigkeit: sehr hoch (Klasse 2 nach EN 350). Ideal für Schwellen,
Ständer, Verbindungen, Holznägel.
Schwindmaß beim Trocknen: 4–6 % in der Querschnittsfläche [HART —
Eißing/Furrer 2023]. Zapfen wurden mit Übermaß gefertigt, damit die
Verbindung im Trockenzustand noch hält — historisches "Arbeiten" war
erwartetes, nicht problematisches Verhalten.

**Tanne (Weißtanne)**
Verbreitung: Süddeutschland, Alpenraum, Vogesen, Schwarzwald.
Eigenschaften: Druckfestigkeit ~40 MPa [HART], Dichte trocken ~460 kg/m³
[HART]. Leichter zu bearbeiten als Eiche. Für Dachwerke bevorzugt
(Biegeelastizität). Geringere Dauerhaftigkeit im Außenbereich.
[MITTEL — Eißing/Furrer 2023]

**Fichte**
Verbreitung: Mittel- und Hochgebirge, Alpen.
Eigenschaften: ähnlich Tanne, etwas harzhaltiger, daher etwas
witterungsbeständiger. Im Alpenraum häufig Substitut für Tanne.
[MITTEL — Eißing/Furrer 2023]

**Lärche**
Verbreitung: Alpen, Alpenvorland.
Eigenschaften: Hart wie Eiche, harzreich, sehr witterungsbeständig.
Regional der Eiche gleichgestellt für Außenbauteile.
[MITTEL]

**Kiefer**
Verbreitung: Norddeutsche Tiefebene, Sandböden.
Eigenschaften: Weicher als Eiche, aber im Norddeutschen Raum oft der
einzige verfügbare Laubholzersatz. Dauerhaftigkeit geringer.
[MITTEL]

#### Verfügbarkeitskarte (vereinfacht)

| Region | Primärholz | Sekundärholz |
|---|---|---|
| Norddeutsche Tiefebene | Eiche | Kiefer |
| Niederrhein, Westfalen | Eiche | Buche |
| Hessen, Thüringen | Eiche, Buche | Tanne |
| Franken | Eiche, Kiefer | Tanne |
| Baden, Elsass | Tanne, Eiche | Fichte |
| Bayern, Österreich | Fichte, Tanne | Lärche |
| Alpen | Lärche, Fichte | Tanne |

[MITTEL — Eißing/Furrer 2023; Großmann 2009; regionale Dendrochronologie]

**BVILLAGE-Implikation**: Die `MaterialPolicy` für `timber.species`
ist primär eine Funktion von `region` — nicht von `wealth` oder `epoch`.
Reiche Bauherren verwenden Eiche auch in Tannengebieten (Importaufwand),
aber der Normalfall folgt der lokalen Verfügbarkeit. Wealth modifiziert,
Region bestimmt.

#### Grünholzverbau

In 90 % aller dendrochronologisch untersuchten Fälle liegen Fälljahr
und Einbau maximal 2 Jahre auseinander. [HART — Hollstein, zitiert nach
Eißing/Furrer 2023; Pressler GmbH Dendrolabor]

Das bedeutet: Holz wurde grün (frisch gefällt, nicht ausgetrocknet)
verbaut. Das war kein Mangel — es war bewusstes Vorgehen, das die
Konstruktion erlaubte, sich im Einbauzustand zu setzen. Zapfen mit
Übermaß, Holznagel, der beim Schwinden fester wird.

#### Holzressourcen und Waldverlust

Der mittelalterliche Holzverbrauch für Bauten war erheblich. Ein
mittleres Fachwerkhaus (6×10 m, zweigeschossig) benötigte ca. 15–25
Festmeter Holz — den Abholzungsertrag von 0,5–1,0 Hektar Wald.
[MITTEL — Schätzung auf Basis von Querschnittsdaten aus Eißing/Furrer 2023]

In Städten mit 200+ Neubauten pro Jahrzehnt: dauerhafter Walddruck
im Umkreis von 20–50 km. Holzmangel ab ca. 1350–1400 in städtischen
Zentren ist dendrochronologisch fassbar: Importholz aus anderen Regionen
nimmt zu, Querschnitte werden tendenziell schlanker.
[HART für Importnachweis — Marstaller 2012; MITTEL für Querschnittstrend]

### 3.2 Stein

Stein ist der zweite große Baustoff, aber in seiner Verfügbarkeit
fundamental ungleicher verteilt als Holz.

#### Gesteinstypen und Verbreitung

**Sandstein**
Verbreitung: Weser-Bergland, Thüringer Wald, Franken, Schwarzwald,
Elsass (Vogesensandstein).
Eigenschaften: gut spaltbar, gut bearbeitbar, mittlere Festigkeit.
Für Fundamente, Schwellsteine, Fenstergewände, Türstürze.
[MITTEL — Binding 1993]

**Kalkstein**
Verbreitung: Schwäbische und Fränkische Alb, Thüringer Becken,
Eifel, Rheinland.
Eigenschaften: hohe Druckfestigkeit (50–100 MPa) [HART], gut
bearbeitbar in weichem Zustand (Muschelkalk), hart wenn ausgehärtet.
Für Fundamente und — bei Verfügbarkeit — als Mauerwerk.

**Basalt und Vulkanite**
Verbreitung: Eifel, Vogelsberg, Siebengebirge.
Eigenschaften: sehr hart, schwer zu bearbeiten, schwer.
Verwendung: Fundamente, Pflaster, Bruchsteinmauerwerk.

**Backstein (gebrannter Ziegel)**
Verbreitung: Norddeutsche Tiefebene (kein Naturstein), Niederrhein,
Hansegebiet, Ostseeküste.
Produktionsbeginn: massenhaft ab ca. 12.–13. Jahrhundert in Norddeutschland.
[HART — archäologisch, historisch dokumentiert]
Eigenschaften: standardisierter als Naturstein, wasserfest,
feuerbeständiger als Holz. Im Norddeutschen die wichtigste
Steinalternative für Mauerwerk und Gefachinfill.

**Lehm und Ton**
Verbreitung: überall, aber lokal unterschiedliche Qualität.
Verwendung: Gefachfüllung (Lehmwellerflechtwand), Lehmbau (selten
im deutschen Fachwerkraum als Primärkonstruktion), Mörtelmischung.
Kein Transportgut — immer aus der nächsten Umgebung.
[HART — überall nachgewiesen; Eißing/Furrer 2023]

#### Naturstein-Verfügbarkeitskarte

| Region | Primärstein | Konsequenz |
|---|---|---|
| Norddeutsche Tiefebene | keiner (Geschiebe, Findlinge) | Backstein dominant ab 12. Jh. |
| Niederrhein | Tuff (aus Eifel, Transport via Rhein) | Mischkonstruktionen |
| Hessen, Thüringen | Sandstein, Buntsandstein | Fundamente, Fenstergewände |
| Franken | Kalkstein, Sandstein | Fundamente, Sockel, Kellerbau |
| Baden, Elsass | Vogesensandstein | Häufiger Steinbau als im Norden |
| Bayern | Kalkstein, Nagelfluh | Fundamente, Kellerbau |

[MITTEL — Binding 1993; Großmann 2009]

**BVILLAGE-Implikation**: Stein für Fundamente und Gewände ist immer
lokal. Die `MaterialPolicy` für `stone.type` ist eine direkte Funktion
von `region` ohne Ausnahme — kein Transportaufwand rechtfertigt
Fremdstein für Fundamente.

### 3.3 Dachdeckungsmaterialien

Dachdeckung ist stark standortabhängig und beeinflusst direkt die
Dachneigung — ein primärer geometrischer Parameter.

| Material | Region / Epoche | Neigung | Last (kg/m²) | Evidenz |
|---|---|---|---|---|
| Stroh / Reet | überall bis 16. Jh., danach zurückgehend | 45–60° | 35–80 | HART |
| Holzschindeln (gespalten) | Mittelgebirge, Alpen | 30–50° | 15–25 | HART |
| Biberschwanz-Ziegel | Süddeutschland ab 13. Jh. | 35–60° | 40–55 | HART |
| Mönch-Nonne (romanisch) | Rheinland, Süden | 25–40° | 50–70 | HART |
| Naturschiefer | Rheinland, Mittelgebirge | 25–45° | 30–40 | HART |
| Sandsteinplatten | Franken, Württemberg | 30–50° | 60–90 | HART |
| Cotswold Kalkstein | England (Cotswolds) | 45–55° | 100+ | HART |

[HART — Messwerte aus Materialuntersuchungen: Eißing/Furrer 2023;
mittelalterliche_baupraxis_v2.md]

**BVILLAGE-Implikation**: `roof.pitch` ist nicht frei wählbar.
Es ist eine Funktion von `roof.material`, das wiederum eine Funktion
von `region` und `epoch` ist. Die Validierungskette:
`region` → `roof.material_available` → `roof.pitch_min`.

### 3.4 Bindemittel

**Luftkalkmörtel**
Der Normalfall im mittelalterlichen Profanbau.
Druckfestigkeit: 0,5–3,0 MPa. [HART — Gediminas Castle Hill Study,
PMC 2019; mehrfach repliziert]
Keine Zugfestigkeit. Konsequenz: Gewölbe erfordern geometrisch präzise
Druckbögen — Zugspannungen würden den Mörtel zerstören.
Herstellung: auf der Baustelle gebrannt oder geliefert, idealerweise
Wochen bis Monate vor Verwendung gelöscht. Härtung langsam;
Winterbau problematisch (Frost verhindert Abbindung).

**Hydraulischer Kalk**
Regional und für Sonderaufgaben (Kathedralen, Burgen, Zisternen).
Druckfestigkeit: bis 8,5 MPa; mit Ziegelmehlzusatz bis 10,2 MPa.
[HART — Gediminas Castle Hill, 13./14. Jh., gemessen an Bohrkernen]

**BVILLAGE-Implikation**: Im `MaterialRegistry` muss unterschieden
werden zwischen `binder.mortar_lime` (Profanbau-Standard) und
`binder.mortar_hydraulic` (Sonderbau). Der `PhysicalPlausibilityValidator`
muss für Mauerwerk nicht nur Druckfestigkeit prüfen, sondern auch
fehlende Zugfestigkeit — das erzwingt Überprüfung der Gewölbegeometrie.

---

## 4. Räumliche Scales der physischen Differenzierung

Die physische Welt wirkt auf unterschiedlichen Maßstabsebenen. Für
BVILLAGE ist es wichtig zu wissen, welche Skala welchen Parameter steuert:

| Skala | Phänomen | Gesteuerte Parameter |
|---|---|---|
| 10–50 km | Lokale Geologie, Bodentyp, Waldbestand | `stone.type`, `timber.species`, `infill.material` |
| 50–150 km | Klimazone, Großlandschaft | `roof.pitch`, `wall.thickness`, `foundation.depth` |
| 200+ km | Holzhandelseinzugsgebiet | Importholz, Sonderholzarten für Reiche |
| Kontinent | Klimaepoche (MWP / Kleine Eiszeit) | Epochale Ressourcenconstraints |

[MITTEL — aus Achse 1 und MEDIEVAL_WORLD_OVERVIEW.md; Eißing/Furrer 2023
für Transportdistanzen]

---

## 5. Schneelast: Ein unterschätzter Parameter

Schneelast ist in der Bauforschung oft unterschätzt, weil sie unsichtbar
ist — das Haus steht noch, der Schnee ist weg. Aber Dachversagen durch
Schneelast ist ein reales mittelalterliches Risiko, das Konstruktionen
beeinflusst hat.

Schneelast Mitteleuropa: 0,5–2,0 kN/m² (50–200 kg/m²), Berglagen höher.
Effektive Verdopplung der Dachlast im Winter möglich. [HART —
physikalisch ableitbar; Eißing/Furrer 2023]

Konsequenz: Steilere Dächer in schneereichen Lagen (Schnee rutscht ab),
stärkere Pfetten und Sparren in Berglagen.

**BVILLAGE-Implikation**: `roof.snow_load` ist eine Funktion von
`region.altitude` und `region.climate_zone`. Der
`PhysicalPlausibilityValidator` muss Dachkonstruktionen gegen diese
Last prüfen — regional differenziert, nicht uniform.

---

## 6. Was die physische Welt nicht erklärt

Achse 1 liefert Constraints — keine Determinanten. Innerhalb der
physischen Möglichkeiten entscheiden Achsen 2–6, was gebaut wird.

Beispiele:
- Backstein war in Norddeutschland verfügbar. Warum trotzdem Fachwerk?
  → Achse 4 (Kosten), Achse 5 (Wissen), Achse 3 (soziale Norm)
- Eichenholz war schwerer als Tannenholz. Warum trotzdem Eiche?
  → Achse 5 (Konstruktionswissen: Eiche dauerhafter) und
    Achse 3 (soziale Norm: Eiche prestigereicher)
- Steile Dächer wären in Norddeutschland schneelasttechnisch unnötig.
  Trotzdem kommen sie vor.
  → Achse 6 (Bauen als Akt: regionale Formensprache) und
    Achse 5 (übertragene Grammatik aus anderen Regionen)

Die physische Welt setzt das Möglichkeitsfeld. Die anderen Achsen
bestimmen die Auswahl innerhalb dieses Feldes.

---

## 7. Offene Forschungsfragen für BVILLAGE

**Frage 1 — Regionale Holzartenverteilung quantitativ**
Die Verfügbarkeitskarte in Abschnitt 3.1 ist qualitativ. Für eine
präzise `MaterialPolicy` bräuchte es quantitative Wahrscheinlichkeiten:
Mit welcher Häufigkeit wurde in Region X Holzart Y verwendet?
Das ist aus der dendrochronologischen Datenbasis (Eißing/Furrer 2023)
grundsätzlich ableitbar, aber noch nicht für alle Regionen systematisiert.

**Frage 2 — Klimaepocheneffekte auf Holzqualität**
MWP-Holz vs. Kleine-Eiszeit-Holz: Unterscheiden sich die Jahrringe
(und damit die mechanischen Eigenschaften) messbar? Dendrochronologisch
könnte das direkt belegt werden. Für BVILLAGE wäre das ein
epochenabhängiger `timber.quality`-Parameter.

**Frage 3 — Transportkosten als Proxy für Materialwahl**
Wann lohnte sich Ferntransport für Stein oder Spezialholz? Das ist eine
ökonomische Frage (Achse 4), die aber auf physischer Geographie basiert.
Die Schwelle "lokal vs. import" ist regional und epochal verschieden.

---

## 8. Quellen und wissenschaftliche Grundlage

### 8.1 Zitierte Werke

**Binding, Günther:** Baubetrieb im Mittelalter. Darmstadt: WBG, 1993.
ISBN 978-3-534-07204-9.
*Bauorganisation und Materialien. Steintypen, Mörtelmischungen, Dachdeckungen.*
[MITTEL/HART]

**Büntgen, Ulf et al.:** 2500 Years of European Climate Variability and
Human Susceptibility. In: Science 331 (2011), S. 578–582.
DOI: https://doi.org/10.1126/science.1197175
*Dendrochronologische Klimarekonstruktion für Europa. Belegt die
Temperaturschwankungen zwischen MWP und Kleiner Eiszeit mit hoher
zeitlicher Auflösung.*
[HART — dendrochronologisch]

**Eißing, Thomas; Furrer, Benno; Kayser, Christian et al.:**
Vorindustrieller Holzbau. Terminologie und Systematik. 2. Aufl.
Heidelberg: Propylaeum, 2023. ISBN 978-3-96929-223-5.
DOI: https://doi.org/10.11588/sbhbf.2023.1.99050 — PDF frei zugänglich.
*Verbindliches Terminologiewerk. Holzarten, Holzeigenschaften,
Transportnachweise, Grünholzverbau. Primärquelle für Achse 1.*
[HART]

**Großmann, G. Ulrich:** Der Fachwerkbau in Deutschland.
Petersberg: Imhof, 2009. ISBN 978-3-86568-449-2.
*Regionale Materialverteilung, Holzartenverwendung.*
[MITTEL]

**Hoffmann, Richard C.:** An Environmental History of Medieval Europe.
Cambridge: Cambridge University Press, 2014. ISBN 978-0-521-70737-7.
*Umfassende Umweltgeschichte. Klima, Wälder, Rodung, Ressourcennutzung.
Standardwerk für Achse 1.*
[MITTEL/HART]

**Jordan, William Chester:** The Great Famine. Northern Europe in the
Early Fourteenth Century. Princeton: Princeton University Press, 1996.
ISBN 978-0-691-01134-7.
*Standardwerk zur Großen Hungersnot 1315–1322. Klimatische Ursachen,
demographische Folgen.*
[MITTEL]

**Lamb, Hubert H.:** Climate, History and the Modern World.
London: Routledge, 1982. 2. Aufl. 1995. ISBN 978-0-415-12735-6.
*Klassische historische Klimatologie. MWP und Kleine Eiszeit als
Konzepte. Methodisch überholt in Teilen (neuere Studien präziser),
aber konzeptionell grundlegend.*
[MITTEL — neuere Studien (Büntgen 2011, PAGES 2k 2013) sind präziser]

**Mann, Michael E. et al.:** Global Signatures and Dynamical Origins of
the Little Ice Age and Medieval Climate Anomaly. In: Science 326 (2009),
S. 1256–1260.
DOI: https://doi.org/10.1126/science.1177303
*Globale Klimarekonstruktion. Belegt MWP und Kleine Eiszeit auf globaler
Skala mit Proxy-Daten.*
[HART — multiproxy, peer-reviewed]

**Marstaller, Tilmann:** Zu Lande und zu Wasser. Bauholzimporte des 12.–17.
Jahrhunderts im mittleren Neckarraum. In: DGAMN-Mitteilungen Bd. 24.
Paderborn 2012, S. 39–56.
*Dendrochronologischer Nachweis überregionaler Holztransporte.
Schlüsselbeleg für Fluss-als-Infrastruktur.*
[HART]

**PAGES 2k Consortium:** Continental-scale temperature variability during
the past two millennia. In: Nature Geoscience 6 (2013), S. 339–346.
DOI: https://doi.org/10.1038/ngeo1797
*Aktuelle Klimarekonstruktion mit regionaler Auflösung für Europa.
Ersetzt ältere Globalstudien für europäische Fragestellungen.*
[HART — multiproxy, peer-reviewed]

**Stiewe, Heinrich:** Fachwerkhäuser in Deutschland. Darmstadt: WBG, 2007.
ISBN 978-3-534-18714-1.
*Regionale Materialverteilung im deutschen Fachwerkbau.*
[MITTEL]

---

### 8.2 Weiterführende Literatur

**Rackham, Oliver:** The History of the Countryside. London: Dent, 1986.
*Englische Landschafts- und Forstgeschichte. Holzarten, Waldnutzung,
Transportwege. Für England-bezogene Research und komparative Studien.*

**Wickham, Chris:** Framing the Early Middle Ages. Europe and the
Mediterranean 400–800. Oxford: Oxford University Press, 2005.
*Ressourcenwirtschaft im frühen Mittelalter. Hintergrund für die
Ausgangslagen von Achse 1.*

**Schweingruber, Fritz H.:** Tree Rings. Basics and Applications of
Dendrochronology. Dordrecht: Reidel, 1988.
*Methodisches Grundlagenwerk zur Dendrochronologie. Für Verständnis
der Forschungsmethode.*

---

### 8.3 Primärquellen und Datenbanken

**International Tree-Ring Data Bank (ITRDB)**:
https://www.ncei.noaa.gov/products/paleoclimatology/tree-ring
*Globale Sammlung dendrochronologischer Referenzchronologien.
Für Holzartenverteilung und klimatische Rekonstruktionen.*

**PANGAEA — Publisher for Earth & Environmental Science**:
https://www.pangaea.de
*Datenbank für paläoklimatische Proxydaten. Eiskerne, Pollendaten,
Sedimentkerne — Grundlage für Klimarekonstruktionen.*

**Freilichtmuseen als Materialquellen**:
Freilichtmuseen dokumentieren originale Baumaterialien mit regionaler
Provenienz. Für Holzartenbestimmung und Steinidentifikation:
- Freilichtmuseum Detmold: https://www.lwl-freilichtmuseum-detmold.de
- LVR-Freilichtmuseum Kommern: https://www.kommern.lvr.de

---

*BVILLAGE Research Foundation — Achse 1 — v1.0*
