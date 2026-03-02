# Achse 7 — Epochenstruktur und Brüche
## Der Zeitvektor des mittelalterlichen Bauens

```
Dokument-Typ:  Research Foundation
Achse:         7 von 7
Scope:         BVILLAGE — alle Domains, alle Haustypen
               Zeitraum: 500–1750 (Kern: 950–1500)
               Raum: Westeuropa und Byzanz
Status:        v2.0
Referenziert von:
  [MEDIEVAL_WORLD_OVERVIEW](MEDIEVAL_WORLD_OVERVIEW.md)
  ARCH_POLICIES.md (StylePolicy, CulturePolicy)
  DEV_ROADMAP.md (RES-001)
Referenziert:
  mittelalterliche_baupraxis_v2.md
  RESEARCH_FACHWERK_HISTORISCH.md
  RESEARCH_FACHWERKBAU.md
  [MEDIEVAL_05 — Wissen](MEDIEVAL_05_KNOWLEDGE_CRAFT.md#6-epochale-entwicklung-der-wissensinfrastruktur)
  [MEDIEVAL_01 — Physische Welt](MEDIEVAL_01_PHYSICAL_WORLD.md)
  [MEDIEVAL_04 — Wirtschaft](MEDIEVAL_04_ECONOMY_TRADE.md)
Evidenzgrade:
  [HART]   Direkt messbar, datierter Bestand, publizierte Messdaten
  [MITTEL] Wissenschaftlicher Konsens, erschlossen, nicht direkt messbar
  [SCHWACH] Analogieschluss, experimentelle Archäologie, Fachtradition
```

---

## Inhaltsverzeichnis

- [Vorbemerkung](#vorbemerkung-warum-achse-7-das-rückgrat-ist)
- [1. Das Grundmodell: Phasen und Brüche](#1-das-grundmodell-phasen-und-brüche)
- [2. Die Epochenphasen](#2-die-epochenphasen)
  - [Phase 0 — Spätantike und Frühmittelalter (ca. 500–950)](#phase-0--spätantike-und-frühmittelalter-ca-500950)
  - [Phase 1 — Hochmittelalter: Entstehung (ca. 950–1150)](#phase-1--hochmittelalter-entstehung-ca-9501150)
  - [Phase 2 — Hochmittelalter: Reife (ca. 1150–1300)](#phase-2--hochmittelalter-reife-ca-11501300)
  - [Phase 3 — Hochmittelalterliche Typenbildung (ca. 1300–1347)](#phase-3--hochmittelalterliche-typenbildung-ca-13001347)
  - [BRUCH 1 — Die Pest (1347–1353)](#bruch-1--die-pest-13471353)
  - [Phase 4 — Spätmittelalterliche Blüte (ca. 1360–1500)](#phase-4--spätmittelalterliche-blüte-ca-13601500)
  - [BRUCH 2 — Holzmangel und Bauordnungen (ca. 1400–1520)](#bruch-2--holzmangel-und-bauordnungen-ca-14001520)
  - [Phase 5 — Übergang: Renaissance und Reformation (ca. 1500–1618)](#phase-5--übergang-renaissance-und-reformation-ca-15001618)
  - [BRUCH 3 — Der Dreißigjährige Krieg (1618–1648)](#bruch-3--der-dreißigjährige-krieg-16181648)
  - [Phase 6 — Frühe Neuzeit: Rationalfachwerk (ca. 1650–1750)](#phase-6--frühe-neuzeit-rationalfachwerk-ca-16501750)
  - [BRUCH 4 — Statuswandel und Industrialisierung (ca. 1750–1900)](#bruch-4--statuswandel-und-industrialisierung-ca-17501900)
- [3. Die Epochenmatrix: Schnellreferenz](#3-die-epochenmatrix-schnellreferenz)
- [4. Regionale Schichtung der Zeitachse](#4-regionale-schichtung-der-zeitachse)
  - [4.1 Konstruktionssystemwechsel](#41-konstruktionssystemwechsel)
  - [4.2 Pestbetroffenheit (1347–1353)](#42-pestbetroffenheit-13471353)
  - [4.3 Dreißigjähriger Krieg (1618–1648)](#43-dreißigjähriger-krieg-16181648)
  - [4.4 Reformationsbruch: regionale Differenzierung](#44-reformationsbruch-regionale-differenzierung)
- [5. Zeitliche Schocks als BVILLAGE-Systemkonzept](#5-zeitliche-schocks-als-bvillage-systemkonzept)
- [6. Offene Forschungsfragen für BVILLAGE](#6-offene-forschungsfragen-für-bvillage)
- [7. Quellen und wissenschaftliche Grundlage](#7-quellen-und-wissenschaftliche-grundlage)

---

## Vorbemerkung: Warum Achse 7 das Rückgrat ist

Die sechs anderen Achsen (→ [Wissen als Zentrum](MEDIEVAL_05_KNOWLEDGE_CRAFT.md#vorbemerkung-warum-achse-5-das-zentrum-ist))
beschreiben Zustände — wie war die physische Welt, wie war die Gesellschaft,
wie funktionierte Handel. Achse 7 beschreibt die Bewegung: wie diese
Zustände sich veränderten, wann sie sprangen, was die Sprünge auslöste.

Für BVILLAGE ist das die kritischste Achse, weil sie die Zeitdimension aller
Policy-Parameter strukturiert. Ein `epoch_band`-Parameter ohne Kenntnis der
Brüche, die dieses Band durchziehen, ist eine Interpolation ins Leere.
Bauen im Jahr 1350 und Bauen im Jahr 1380 sind nicht zwei Punkte auf einer
Geraden — zwischen ihnen liegt die Pest.

Diese Achse liefert die Diskontinuitäten, die das System explizit modellieren
muss. Nicht als Sonderfälle, sondern als Strukturelement.

**Scope dieses Dokuments**: Gesamteuropa und Byzanz, 500–1750. Die
Phasierungen sind gesamteuropäisch formuliert; regionale Abweichungen —
und sie sind erheblich — werden in [Abschnitt 4](#4-regionale-schichtung-der-zeitachse)
differenziert. Die Epochenbezeichnungen folgen der wissenschaftlichen
Konvention: Frühmittelalter (ca. 500–1000), Hochmittelalter (ca. 1000–1250),
Spätmittelalter (ca. 1250–1500), Frühe Neuzeit (ca. 1500–1800).

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

**Wichtig**: Die Phasengrenzen sind gesamteuropäische Orientierungswerte.
Regional verschieben sich die Grenzen um Jahrzehnte. England 1066
(Normanneneinfall) ist ein lokaler BRUCH ohne kontinentaleuropäisches
Äquivalent. Die karolingische Renaissance um 800 ist ein Strukturmoment
für Westeuropa, ohne direkte Bedeutung für Byzanz. Achse 7 kartiert
das Gemeinsame; Abschnitt 4 hält die Differenzen fest.

---

## 2. Die Epochenphasen

### Phase 0 — Spätantike und Frühmittelalter (ca. 500–950)

*Hintergrundphase. Nicht BVILLAGE-Domain, aber Kontext für alles Folgende.*

#### Das Ende der antiken Bauordnung

Der Zusammenbruch des Weströmischen Reichs (476) ist kein Ereignis,
sondern ein Prozess, der sich über Jahrhunderte erstreckt. Für das Bauen
bedeutet er: der Verlust der antiken Wissensinfrastruktur — Architekturschulen,
Lehrtradition der Vitruv-Nachfolge, staatliche Bauprogramme, professionelle
Bauorganisation. [MITTEL — Ward-Perkins 2005; Wickham 2009]

Nicht alles geht verloren. Der Steinbau in Italien, Südfrankreich und der
Iberischen Halbinsel persistiert, getragen von der Kirche. Klöster werden
im 6.–8. Jahrhundert zu den wichtigsten Bauhütten Westeuropas — sie
bewahren antike Messtechniken, Mörtelmischungen, Gewölbewissen.
[MITTEL — Horn/Born 1979]

Im Norden und Osten dominiert der Holzbau. Germanische Hallenhäuser,
skandinavische Langhäuser, angelsächsische *halls* — alle in Pfostenbauweise.
Kein Mehrgeschossbau möglich, Lebensdauer 30–80 Jahre.
[HART — Beresford/Hurst 1990; Zimmermann 1998]

#### Das byzantinische Kontinuum

Byzanz ist in dieser Phase kein Übergang, sondern ein Kontinuum. Die
oströmische Tradition bricht nicht ab. Konstantinopel bleibt bis ins
13. Jahrhundert die größte Stadt Europas. Hagia Sophia (532–537) ist der
technologische Höhepunkt der Epoche — Pendentifkuppel über einem Quadrat,
bis dahin ohne Präzedenz. [HART — Krautheimer 1986; Mainstone 1988]

Byzantinische Baupraxis: kaiserlicher Auftrag, professionelle Architekten
(*mechanikoi*), keine Zünfte im westeuropäischen Sinne. Wissenstransfer
über kaiserliche Werkstätten. [MITTEL — Mango 1976]

#### Die karolingische Renaissance (ca. 750–900)

Karl der Große versucht eine bewusste Restituierung antiker Baukenntnisse.
Die Pfalzkapelle Aachen (792–805) kopiert explizit San Vitale in Ravenna —
einschließlich der Spolien (antike Säulen, direkt aus Italien importiert).
[HART — bauarchäologisch; Binding 1996]

Die karolingische Renaissance betrifft eine Handvoll Großbauten, hat aber
strukturelle Wirkung: Klosterschulen (Tours, Fulda, St. Gallen) werden
zu Knoten einer emergierenden Wissensinfrastruktur. Der St.-Galler
Klosterplan (820) ist das erste erhaltene maßstäbliche
Bauplanungsdokument Westeuropas. [HART — Horn/Born 1979]

#### Islamische Baukulturen als Kontaktzone

Ab dem 7. Jahrhundert verändert der islamische Aufstieg die Kontaktzonen
Europas. Die Iberische Halbinsel (ab 711 arabisch) und Sizilien
(ab 827 arabisch) werden zu Transferräumen: arabische Geometrie,
Bogentechnik, Gipsstuck-Tradition fließen in die europäischen Grenzregionen.
[MITTEL — Dodds 1990; Bloom/Blair 2009]

Al-Andalus produziert in dieser Phase die architektonisch ausgefeiltesten
Bauten der westlichen Hemisphäre — Mezquita Córdoba (784ff.), Medina
Azahara (936ff.). [HART für Bestand; MITTEL für Transferrichtung]

#### BVILLAGE-Status

Vorläuferphase. Kein Planer vorgesehen. Relevant als:
- Ausgangszustand für Parameterinitialisierung der Frühphase
- Quelle der Wissensinfrastruktur (Klosterschulen) für Phase 1
- Byzantinisches Referenzmodell für orthodoxe Baukulturen

---

### Phase 1 — Hochmittelalter: Entstehung (ca. 950–1150)

#### Bevölkerungswachstum als Bautreiber

Die Bevölkerung Westeuropas verdoppelt sich zwischen 950 und 1300 annähernd —
von ca. 25 auf ca. 55–60 Millionen. [MITTEL — Russell 1958; McEvedy/Jones 1978]
Dieser Druck erzeugt Bautätigkeit in einem Ausmaß, das in den Jahrhunderten
davor undenkbar war: neue Städte, Rodung, Kirchenneubau im Massenprogramm.

Romanischer Kirchenbau ist das Leitprogramm der Phase. In Frankreich,
Deutschland, England, Spanien und Italien entstehen innerhalb von zwei
Jahrhunderten Tausende von Kirchen — regional sehr verschieden: normannische
Schwere (England, Sizilien), rheinische Eleganz (Speyer, Worms, Mainz),
burgundische Klarheit (Cluny). [MITTEL — Conant 1959]

#### Der entscheidende Schritt im Holzbau

Der Ständer verlässt die Erde. Er steht auf Stein oder auf einer Schwelle.
Diese minimale Verschiebung hat maximale Konsequenz: keine Bodenfäulnis,
Mehrgeschossbau möglich, Verbindungen statt Einbettung als Stabilitätsprinzip.
[MITTEL — Zimmermann 1998]

Für England früher fassbar als auf dem Kontinent: Cressing Temple Barns,
Essex — Barley Barn 1205–1235, Wheat Barn 1257–1280.
[HART — dendrochronologisch: Hewett; VAG]

Auf dem Kontinent: Die ältesten erhaltenen deutschen Fachwerkhäuser datieren
auf 1262/63 (Heugasse 3, Esslingen) und 1266/67 (Webergasse 8, Esslingen).
[HART — Großmann 2009; Eißing/Furrer 2023]

England vollzieht den Schritt vom Pfostenbau zum Ständerbau ca. 50–80
Jahre früher als Deutschland. [MITTEL]

#### Romanik als Lernprozess

Frühe romanische Gewölbe kollabierten häufig. Die Reaktion war empirisch:
dickere Wände, kleinere Fenster. Romanische Schwere ist materialisierter
Sicherheitspuffer, kein Stilmittel. [MITTEL — Binding 1993; Fitchen 1961]

Ab ca. 1050 entstehen permanente Bauhütten an großen Baustellen —
Werkstatt, Schule, Archiv. Wissenstransfer beginnt sich zu institutionalisieren.
[MITTEL — Recht 1989; Binding 1993]

#### Normannische Synthese (England, Sizilien)

Der Normanneneinfall in England (1066) ist für die englische Baugeschichte
ein scharfer lokaler Bruch. Die Normannen bringen kontinentale Steinkauarchitektur
mit — massive Kathedralen und Burgen ersetzen angelsächsische Holzbauten.
Das englische Steinbauhandwerk entwickelt sich in der Folge schneller
als das kontinentale, weil der normannische Adel Steinbau als
Machtdemonstration einsetzt. [HART — Brown 1984]

In Sizilien entsteht unter normannischer Herrschaft (ab 1061) eine
einzigartige Synthese: arabische Geomerien, byzantinische Mosaike und
normannische Raumstruktur verbinden sich in Bauten wie der Cappella
Palatina in Palermo (1143). [HART für Bestand; MITTEL für Synthese-Deutung]

#### Reconquista und islamischer Transfer (Iberische Halbinsel)

In der Iberischen Halbinsel läuft die Reconquista — die sukzessive
christliche Rückeroberung maurischer Territorien. Maurische Handwerker
(Mudéjares) bauen für christliche Auftraggeber weiter in maurischer Technik.
Der Mudéjar-Stil — islamische Geometrie und Ornamentik in christlichem
Kontext — ist das Ergebnis. Er persistiert bis ins 16. Jahrhundert.
[MITTEL — Dodds 1990]

#### BVILLAGE-Parameter dieser Phase

| Parameter | Wert | Region | Evidenz |
|---|---|---|---|
| `construction_system` | Pfostenbau → Ständerbau | Nordwesteuropa | MITTEL |
| `construction_system` | Steinbau dominant | Südeuropa, Kirchenbauten | HART |
| `ornament_level` | 0 | Holzbau | HART |
| `ornament_level` | 1–3 | Kirchensteinbau | MITTEL |
| `section_overdimension` | 1.5–2.0× | Holzbau | MITTEL |
| `knowledge_tier` | Klöster + frühe Zünfte | alle | MITTEL |

---

### Phase 2 — Hochmittelalter: Reife (ca. 1150–1300)

#### Gotik als Wissensrevolution

Die Gotik ist nicht primär ein Stilwechsel, sondern eine konstruktive
Revolution: Kreuzrippengewölbe, Spitzbogen und Strebewerk ermöglichen es,
den Schub aus dem Gewölbe punktuell abzuleiten statt flächig in dicke Wände
zu verteilen. Das Ergebnis: höhere, schlankere, hellere Räume.
[HART — Fitchen 1961; Mark 1993]

Frankreich ist das Ursprungsland. Saint-Denis (1135–1144) gilt als erstes
gotisches Bauwerk. Chartres (1194ff.), Reims (1211ff.), Amiens (1220ff.)
vollziehen die Entwicklung in drei Generationen. [HART — Binding 1996]

Die Bauhütten dieser Kathedralen sind supraregionale Netzwerke. Villard de
Honnecourts Bauhüttenbuch (ca. 1230) dokumentiert Beobachtungen in Chartres,
Reims, Laon, Lausanne — direktes Zeugnis des Transfernetzwerks.
[HART — Hahnloser 1972]

#### Regionale Differenzierung der Gotik

Frankreich als Ursprung, England als erste Empfängerregion mit eigenständiger
Weiterentwicklung (Early English, Decorated, Perpendicular). Deutschland
adaptiert mit starkem lokalen Beitrag (Hallenkirche als Alternative zum
Querschiff). Italien nimmt die Gotik als importiertes System auf — die
toskanischen Stadtstaaten zeigen eine hybride Form, in der romanische
Tradition und gotische Struktur koexistieren. [MITTEL — Bony 1983; Crossley 1988]

Skandinavien übernimmt Gotik über norddeutsche und englische Vermittlung
mit erheblicher zeitlicher Verzögerung (50–100 Jahre) und starker lokaler
Adaption. Backsteinbau (Ziegelgotik) analog zur norddeutschen Tradition.
[MITTEL — Andersson 1991]

#### Städtewachstum und Holzbau

Die Stadtgründungswelle des 12.–13. Jahrhunderts erzeugt einen Bauboom.
Neue Städte brauchen Bürgerhäuser — schnell, aus lokalem Material.
Der Ständerbau etabliert sich als Standardlösung für den städtischen
Wohnbau nördlich der Alpen. [MITTEL — Schock-Werner 1999]

Klein (2012) belegt für den Grabungsbefund Romrod (Hessen, ca. 1170/80):
Blockbau, Rahmenbau und Ständerbau kommen nebeneinander vor.
Domänenreinheit ist eine spätere Entwicklung. [HART — Klein 2012]

#### Byzantinische Entwicklung: Komnenen-Blüte und Lateinisches Intermezzo

Byzanz erlebt unter den Komnenen (1081–1185) eine Glanzzeit.
Der Vierte Kreuzzug (1204) durchbricht das: Konstantinopel wird von
Kreuzfahrern besetzt; das Lateinische Kaiserreich besteht bis 1261.
Eine Generation Unterbrechung der kaiserlichen Bauprogramme,
Verlust von Werkzeug und Werkstätten. [HART — Harris 2003]

#### BVILLAGE-Parameter dieser Phase

| Parameter | Wert | Region | Evidenz |
|---|---|---|---|
| `construction_system` | Ständerbau etabliert | Nordwesteuropa | HART |
| `construction_system` | Gotischer Steinbau | überall für Kirchen | HART |
| `ornament_level` | 0 | städtischer Holzbau | HART |
| `ornament_level` | 3–5 | Kirchensteinbau | HART |
| `section_overdimension` | 1.4–1.8× | Holzbau | MITTEL |
| `knowledge_tier` | Zunft entstehend (N), Bauhütte aktiv | regional | MITTEL |

---

### Phase 3 — Hochmittelalterliche Typenbildung (ca. 1300–1347)

#### Stabilisierung und regionale Differenzierung

Die Ständerbaukonstruktion ist etabliert. Regionale Grammatiken
kristallisieren sich: Das norddeutsche Hallenhaus nimmt seine kanonische
dreischiffige Form an. Das mitteldeutsche Ernhaus differenziert sich.
In England kristallisieren sich *cruck frame* und *box frame* als die
beiden Hauptsysteme heraus. [MITTEL — Großmann 2009; Stiewe 2007; Alcock 1981]

In Frankreich entwickelt sich das *pan de bois* als Standardsystem für
den städtischen Bürgerhausbau — strukturell dem deutschen Fachwerk verwandt,
aber in Ornamentik und Gefügegeometrie eigenständig. Normandie und Elsass
sind die Kernregionen. [MITTEL — Chapelot/Fossier 1985]

#### Vorkrisensignale: Agrarkrise und Kleine Eiszeit

Die Phase endet nicht ruhig. Ab ca. 1315 trifft die Große Hungersnot
(1315–1322) weite Teile Nordwesteuropas — ausgelöst durch eine Serie
nasser, kalter Sommer, die den Beginn der Kleinen Eiszeit markieren.
Das ist kein Baubruch — aber eine demographische und ökonomische
Schwächung, die die Gesellschaft geschwächt in die Pest von 1347 führt.
[HART — Jordan 1996]

Gleichzeitig: Erste einfache Schmuckelemente im Holzbau — Knaggen,
Profilierungen, Ziegelinfill in Norddeutschland häufiger. Erste
Vorkragungen erscheinen. [MITTEL — Stiewe 2007; Großmann 2009]

#### BVILLAGE-Parameter dieser Phase

| Parameter | Wert | Region | Evidenz |
|---|---|---|---|
| `construction_system` | Ständerbau dominant | Nordwesteuropa | HART |
| `construction_system` | Stockwerksbau beginnend | Süddeutschland | MITTEL |
| `ornament_level` | 1 — einfach (Profilierung, Knaggen) | Städte | MITTEL |
| `infill_type` | Lehm + zunehmend Ziegel (regional) | HRR | MITTEL |
| `jetty_allowed` | ja, einfach | Städte | MITTEL |
| `section_overdimension` | 1.3–1.6× | Holzbau | MITTEL |
| `knowledge_tier` | städtische Zünfte etabliert | Nordwesteuropa | MITTEL |

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

England: 40–50 % (besser dokumentiert, da Kirchenregister erhalten).
Frankreich: 30–50 %. Italiens Städte: bis zu 60 % lokal (Florenz, Siena).
HRR: 25–40 %. Byzanz und der Balkan: früh betroffen — die Pest kommt
von Caffa (Krim) über Konstantinopel. [MITTEL — Herlihy 1997; Benedictow 2004]

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

**Regionaler Sonderfall Italien**: Florenz verliert ca. 50–60 %
der Bevölkerung. Die institutionalisierte Dombauhütte läuft weiter —
Kontinuität trotz hohem Personalverlust, weil die Institution die Personen
übersteht. [MITTEL — Goldthwaite 1980]

**Byzantinischer Sonderfall**: Byzanz ist bereits strukturell geschwächt
(osmanischer Druck, territoriale Verluste). Der Wiederaufbaueffekt bleibt
schwächer als in Westeuropa. [MITTEL — Nicol 1993]

→ Wissensinfrastruktur-Konsequenzen: [MEDIEVAL_05, Phase 3](MEDIEVAL_05_KNOWLEDGE_CRAFT.md#phase-3-pestschock-und-nachwirkung-1347ca-1430)

**Wichtig für BVILLAGE**: Die Pest ist kein `StylePolicy`-Gradient. Sie ist
ein Unstetigkeitspunkt. Parameter, die 1346 galten, gelten 1355 nicht mehr —
nicht wegen technischer Entwicklung, sondern wegen demographischer und
ökonomischer Disruption.

---

### Phase 4 — Spätmittelalterliche Blüte (ca. 1360–1500)

#### Der Wiederaufbau als Innovationsschub (HRR)

Die Jahrzehnte nach der Pest sind, paradoxerweise, eine Blütezeit des
städtischen Bauens in Nordwesteuropa. Konzentriertes Kapital bei weniger
Eigentümern, freie Bauplätze, erfahrene Handwerker mit höheren Löhnen.
[MITTEL — Boockmann 1987; Herlihy 1997]

#### Stockwerksbau setzt sich durch (Nordwesteuropa)

Jedes Stockwerk als eigenständige Rahmenkonstruktion — Schwelle, Ständer,
Rähm — wird zur dominanten Bauweise. Kurze Hölzer genügen; das erleichtert
Beschaffung in zunehmendem entwaldeten Stadtumland. Mehrgeschossige Gebäude
(4–8 Stockwerke) werden möglich. [HART — Klein 2012]

Vorkragungen nehmen zu: jedes Stockwerk leicht nach vorn auskragend,
Flächengewinn im Obergeschoss. Ab dem 15. Jahrhundert etablierte Praxis.
[MITTEL — Großmann 2009; Stiewe 2007]

#### Das ornamentale Zeitalter (HRR)

Das 15. und frühe 16. Jahrhundert ist die Hochphase der Fachwerkornamentik.
Andreaskreuze, Fächerrosetten, Treppenfriese — Ausdrucksmittel für
Reichtum, Zunftzugehörigkeit und Repräsentation.
Kanonische Beispiele: Knochenhaueramtshaus Hildesheim (1529), Hoppener
Haus Celle (1532). [HART — dendrochronologisch oder urkundlich datiert]

#### England: Perpendicular und *great rebuilding*

Der Perpendicular-Stil (ca. 1350–1550) ist eine rein englische Schöpfung —
strenge Vertikalität, große Fenster, flache Bögen. Kein kontinentales
Äquivalent. [HART — Harvey 1978]

Im ländlichen Holzbau beginnt in England ab ca. 1400 das *great rebuilding* —
ein Modernisierungsschub, bei dem ältere Häuser durch solidere *box-frame*-
Konstruktionen ersetzt werden. Dendrochronologisch gut dokumentiert.
[HART — Machin 1977; Dyer 1989]

#### Frankreich und Niederlande: Flamboyant und städtische Blüte

Frankreich erholt sich nach dem Hundertjährigen Krieg (1337–1453) langsamer.
Flamboyante Gotik — der letzte, ornamental reichste Stil der französischen
Gotik — datiert hauptsächlich in diese Phase. [MITTEL — Bony 1983]

Die Niederlande und Flandern entwickeln eine städtische Baukultur von hoher
Eigenständigkeit. Das flämische *vakwerkbouw* und die Backsteinarchitektur
der Hansestädte sind die Leitformen. Antwerpens Aufstieg als
Handelsmetropole (ab ca. 1450) erzeugt einen Bauboom mit europäischer
Ausstrahlung. [MITTEL — Meischke 1988]

#### Byzanz: Palaiologen-Renaissance und Fall

Die Palaiologen-Dynastie (1261–1453) erneuert Konstantinopel nach der
lateinischen Besatzung. Eine letzte künstlerische Blüte entsteht in einer
politisch eingeengten Gesellschaft. 1453 fällt Konstantinopel an die Osmanen.
Der Fall ist für Byzanz das Ende, nicht ein Bruch. Für Westeuropa ist er
eine Erschütterung und ein Wissenstransfer-Ereignis: griechische Gelehrte
fliehen nach Italien und tragen zur Renaissance bei. [HART — Nicol 1993]

#### BVILLAGE-Parameter dieser Phase

| Parameter | Wert | Region | Evidenz |
|---|---|---|---|
| `construction_system` | Stockwerksbau dominant | HRR, England, NL | HART |
| `ornament_level` | 2–4 (regional sehr unterschiedlich) | HRR | MITTEL |
| `ornament_level` | 1–2 | England, Frankreich | MITTEL |
| `jetty_allowed` | ja, mehrfach | Städte NW-Europa | MITTEL |
| `infill_type` | Ziegel zunehmend (N), Lehm (Mitte/S) | HRR | MITTEL |
| `section_overdimension` | 1.2–1.4× | Holzbau | MITTEL |
| `knowledge_tier` | städtische Zünfte vollentwickelt | NW-Europa | MITTEL |

---

### BRUCH 2 — Holzmangel und Bauordnungen (ca. 1400–1520, regional gestaffelt)

Kein einzelnes Ereignis — ein schleichender Strukturwandel, der in manchen
Städten früher, in anderen später zur Krise wird. Real und
dendrochronologisch nachweisbar als Veränderung der verwendeten Holzarten
und Querschnitte.

#### Holzmangel

Städtischer Wachstumsdruck entwaldet das Umland. Lange, gerade Stämme
für den Ständerbau werden knapper und teurer. Das beschleunigt den
Übergang zum Stockwerksbau (kürzere Ständer) und erhöht den Anteil
importierten Holzes. [HART — Eißing/Furrer 2023; Marstaller 2012]

In England belegen Rechnungsunterlagen Importe von Eichenholz aus der
Normandie und dem Baltikum. [HART — Salzman 1952]

#### Städtische Bauordnungen

Als Reaktion auf verheerende Stadtbrände erlassen Städte Bauordnungen:
Mindestabstände, Verbote für Strohdeckungen, Vorkragungsbeschränkungen.

England ist früher als das HRR: London reagiert nach Großbränden (1087,
1135, 1212) mit Bauordnungen, die Steinbau an Grundstücksgrenzen
vorschreiben. [HART — Salzman 1952]

**BVILLAGE-Implikation**: `ConstraintsPolicy` für städtische Kontexte
muss lokale Bauordnungen als Hard-Constraints abbilden können — mit
spatiotemporaler Gültigkeit, nicht als universelle Regel.

---

### Phase 5 — Übergang: Renaissance und Reformation (ca. 1500–1618)

#### Renaissance: Konstruktionssystem oder Ornament?

Die Renaissance beginnt in den italienischen Stadtstaaten des 14.–15.
Jahrhunderts. In Italien selbst ist sie primär ein Steinbauphänomen:
Brunelleschi, Alberti, Palladio entwickeln eine Architekturtheorie,
die erstmals seit der Antike wieder in Traktaten kodifiziert wird.
[HART — Wittkower 1971]

Nördlich der Alpen kommt die Renaissance als Ornamentmotiv, nicht als
Konstruktionssystem: Pilaster, Medaillons, antikisierende Friese erscheinen
auf Fachwerkhäusern, ohne deren Struktur zu verändern.
[MITTEL — Großmann 2009]

Frankreich adaptiert die Renaissance früher als Deutschland — direkter
Kontakt über Feldzüge Karls VIII. und Franz I. nach Italien.
Châteaux de la Loire (1490–1560) sind das früheste nordfranzösische
Renaissancekorpus. [HART — Babelon 1989]

#### Standardisierung und Rationalisierung (HRR)

Die ornamentale Hochphase klingt ab. An ihre Stelle tritt ein technischeres
Fachwerk: regelmäßigere Ständerabstände, klare Raster, reduzierte
Ornamentik. Die Wassersägemühle hat sich durchgesetzt — Querschnitte
werden normierter. In der Schweiz setzt sich das Riegelhaus durch:
Ornament tritt zurück, Präzision wächst. [MITTEL — Eißing/Furrer 2023]

#### Reformation als Baubruch: nur im protestantischen Raum

Die Reformation (ab 1517) ist für das Bauen ein asymmetrischer Bruch.
Sie betrifft den Kirchenbau massiv — und nur dort, und nur im
protestantischen Einflussbereich. Für den Profanholzbau ist sie kein Bruch.

Im protestantischen Raum: Klöster werden säkularisiert, Kathedralbauprogramme
verlieren ihre institutionelle Grundlage. Die Bauhütte verliert ihren
Auftraggeber. [MITTEL — Prak 2011]

Im katholischen Raum (Bayern, Österreich, Spanien, Italien, Frankreich):
kein Bruch. Kirchenbau läuft weiter, Bauhütten bleiben aktiv.

**BVILLAGE-Implikation**: Die Reformation erfordert eine `religion_context`-
Dimension in der `CulturePolicy` — als institutionellen Rahmenparameter
für Bauhüttenexistenz und Kirchenbaukapazität, nicht als Stilparameter.
Ausprägungen mindestens: `catholic`, `lutheran`, `reformed`, `anglican`.

#### England: Tudors und *great rebuilding* II

England unter den Tudors (1485–1603) erlebt eine zweite Phase des *great
rebuilding*. Wohlstand aus Wollhandel fließt in Landhausbau. Das *country
house* — das englische Landhaus — entwickelt sich als Typus. Die englische
Architektur dieser Phase zeigt eine eigenständige Mischung: Gotische
Struktur, flämische und italienische Ornamentmotive, einheimische
Holzbautradition. [MITTEL — Girouard 1978]

#### BVILLAGE-Parameter dieser Phase

| Parameter | Wert | Region | Evidenz |
|---|---|---|---|
| `construction_system` | Stockwerksbau, standardisiert | HRR, England | HART |
| `ornament_level` | 1–3 (reduziert, aber präziser) | HRR | MITTEL |
| `ornament_level` | 1–2 | England | MITTEL |
| `section_variation` | geringer (Säge normiert Querschnitte) | NW-Europa | MITTEL |
| `church_building_active` | ja / nein nach Konfession | regional | MITTEL |
| `knowledge_tier` | Zunftsystem vollentwickelt | NW-Europa | MITTEL |

---

### BRUCH 3 — Der Dreißigjährige Krieg (1618–1648)

Der schwerste politische Schock der frühen Neuzeit in Mitteleuropa.
Für die Baugeschichte der zweite große Diskontinuitätspunkt nach der Pest.

**Wichtig**: Der Dreißigjährige Krieg ist ein HRR-selektiver Schock.
England, Skandinavien (Heimatgebiet), Niederlande, Iberische Halbinsel,
Italien sind nicht oder nur randlich betroffen. Außerhalb des HRR kein
Sprung im Parameterraum.

#### Was geschah

Flächendeckende Kriegszüge, systematische Brandschatzung, Seuchenzüge.
Bevölkerungsverluste in Deutschland: regional 20–60 %.
Für Württemberg sind 57 % Bevölkerungsverlust belegt. [MITTEL — Wilson 2009]

#### Bauliche Konsequenzen

**Direkte Zerstörung**: Magdeburg 1631 (nahezu vollständige Vernichtung),
Heidelberg, zahlreiche kleinere Orte. [HART — historisch dokumentiert]

**Ressourcenknappheit**: Holz knapper, Kapital vernichtet, Arbeitskraft
dezimiert. Querschnitte werden schlanker, Ständerabstände größer,
Ornamentik massiv reduziert. [MITTEL — Stiewe 2007]

**Wiederaufbau**: Nach 1648 rationaler, schlichter. Das Rasterfachwerk
des späten 17. Jahrhunderts ist Effizienzfachwerk. [MITTEL — Stiewe 2007]

**BVILLAGE-Implikation**: Vorkrieg (Phase 5) und Nachkrieg (Phase 6) —
expliziter Sprung, nicht Gradient. Regional variiert der Schock stark:
Nordseeküste und Schweiz kaum betroffen; Mitteldeutschland am stärksten.

---

### Phase 6 — Frühe Neuzeit: Rationalfachwerk (ca. 1650–1750)

#### Schlankeres Bauen (HRR)

Die Konstruktion bleibt dieselbe. Aber das System wirtschaftet mit weniger
Material: Querschnitte schlanker, Ständerabstände größer, keine aufwendigen
Schnitzereien. Das technische Rasterfachwerk — regelmäßige Gefache,
zurückliegende Ziegelausfachung — setzt sich in Südwestdeutschland und der
Schweiz durch. [MITTEL — Stiewe 2007; Eißing/Furrer 2023]

Das Verputzen der Außenwände breitet sich aus: Witterungsschutz und
Statusanspruch (Putz wirkt wie Steinbau) gleichzeitig. [MITTEL — Stiewe 2007]

#### Barock in Westeuropa: Kirche und Residenz

Jenseits des HRR erlebt diese Phase eine andere Dynamik. Der Barock
erreicht Frankreich unter Ludwig XIV. als Staatsstil: Versailles (1661–1710)
prägt die europäische Residenzbaukultur für ein Jahrhundert.
[HART — Berger 1985]

In England ist die Phase durch den Wiederaufbau nach dem Großen Brand von
London (1666) definiert: Christopher Wren baut 51 Kirchen sowie St. Paul's
Cathedral. Die intensivste institutionalisierte Baukampagne der englischen
Baugeschichte des 17. Jahrhunderts. [HART — Summerson 1953]

#### BVILLAGE-Parameter dieser Phase

| Parameter | Wert | Region | Evidenz |
|---|---|---|---|
| `construction_system` | Stockwerksbau | HRR | HART |
| `ornament_level` | 0–1 | HRR | MITTEL |
| `section_overdimension` | 1.0–1.2× (Sparsamkeit) | HRR | MITTEL |
| `facade_treatment` | zunehmend verputzt | HRR, Süddt. | MITTEL |
| `infill_type` | Ziegel dominant | NW-Europa | MITTEL |
| `architectural_style` | Barock | Frankreich, England, Spanien | HART |

---

### BRUCH 4 — Statuswandel und Industrialisierung (ca. 1750–1900)

Kein einzelnes Ereignis, sondern ein kultureller und technologischer
Strukturwandel, der das Ende des historischen Fachwerkbaus herbeiführt.

**Statuswandel**: Im 18. und 19. Jahrhundert gilt sichtbares Fachwerk
als Rückständigkeit. Wer es sich leisten kann, verputzt oder baut in Stein.
[MITTEL — Stiewe 2007]

**Brandschutzgesetzgebung**: Stadtbrände (Hamburg 1842 u. a.) erzwingen
Verbote für Holzfassaden in Städten. [HART — gesetzlich dokumentiert]

**Industrialisierung**: Maschinell produzierter Ziegel, Portlandzement,
schließlich Stahl und Beton machen den Holzrahmenbau technisch überholbar.
Der letzte genuine städtische Fachwerkbau entsteht um 1900.
[HART — Großmann 2009; Stiewe 2007]

**BVILLAGE-Status**: Außerhalb des modellierten Zeitraums. Relevant als
obere Grenze der `epoch_band`-Parameter.

---

## 3. Die Epochenmatrix: Schnellreferenz
→ [↑ Epochenphasen](#2-die-epochenphasen) | [↓ Regionale Schichtung](#4-regionale-schichtung-der-zeitachse)

### Gesamteuropäische Phasierungsmatrix

| Epoche | Leitform Steinbau | Leitform Holzbau | Hauptregion | Trigger |
|---|---|---|---|---|
| 500–950 | Klosterbau / Byzantinisch | Pfostenbau | alle | Transformation der Antike |
| 950–1150 | Romanik entstehend | Ständerbau beginnend | W-Europa | Bevölkerungswachstum |
| 1150–1300 | Gotik (Frankreich → N) | Ständerbau etabliert | W-Europa | Städtewachstum |
| 1300–1347 | Spätgotik | Typenbildung, Ornament I | W-Europa | Reife |
| **BRUCH: PEST 1347** | | | **alle** | **−30–60 % Bevölkerung** |
| 1360–1500 | Flamboyant / Perpendicular | Stockwerksbau, Ornament II | W-Europa | Wiederaufbau |
| 1500–1618 | Renaissance (S nach N) | Standardisierung | W-Europa | Rationalisierung |
| **BRUCH: 30J. KRIEG 1618** | | | **HRR** | **−20–60 % regional** |
| 1650–1750 | Barock | Rationalfachwerk | HRR / Frankreich | Effizienz / Hofstil |
| >1750 | Klassizismus | Fachwerk auslaufend | — | Statuswandel |

### HRR-spezifische Holzbaumatrix

| Epoche | Construction | Ornament | Infill | Section | Jetty |
|---|---|---|---|---|---|
| ~1150–1300 | Ständer | 0 | Flechtwerk/Lehm | 1.5–2.0× | nein |
| 1300–1347 | Ständer→Stockwerk | 1 | Lehm+Ziegel | 1.3–1.6× | einfach |
| **BRUCH: PEST 1347** | | | | | |
| 1360–1520 | Stockwerk | 2–4 | Ziegel/Lehm | 1.2–1.4× | mehrfach |
| 1520–1618 | Stockwerk | 1–3 | Ziegel | norm. | mehrfach |
| **BRUCH: 30J. KRIEG 1618** | | | | | |
| 1650–1750 | Stockwerk | 0–1 | Ziegel | 1.0–1.2× | selten |
| >1750 | Stockwerk (auslauf.) | Revival | Ziegel/Putz | dünn | — |

---

## 4. Regionale Schichtung der Zeitachse

Die Epochenphasen verlaufen nicht uniform über Europa. Sie sind regional
geshiftet. Das ist kein Makel der Datenbasis — es ist historische Realität.

### 4.1 Konstruktionssystemwechsel

#### Holzbau: Pfostenbau → Ständerbau → Stockwerksbau

| Region | Ständerbau Beginn | Stockwerksbau Beginn | Quelle |
|---|---|---|---|
| England | ~1150–1200 | ~1250 | HART — VAG, Hewett |
| Frankreich (Normandie, Elsass) | ~1200 | ~1300 | MITTEL — Chapelot/Fossier |
| Niederlande / Flandern | ~1250 | ~1350 | MITTEL — Meischke 1988 |
| Süddeutschland (Esslingen, Ulm) | ~1250 | ~1300 | MITTEL — Klein 2012 |
| Mitteldeutschland (Hessen, Thüringen) | ~1270 | ~1350 | MITTEL |
| Norddeutschland (Städte) | ~1300 | ~1400 | MITTEL |
| Skandinavien (städtisch) | ~1350 | ~1450 | SCHWACH |
| Iberische Halbinsel | — | — | Steinbau dominant |
| Italien | — | — | Steinbau dominant |

Das niederdeutsche Hallenhaus behält den Ständerbau bis weit ins
19. Jahrhundert. Konstruktionssystemwechsel sind funktional motiviert,
nicht zeitlich deterministisch. [HART — Stiewe 2007]

### 4.2 Pestbetroffenheit (1347–1353)

| Region | Geschätzte Sterblichkeit | Quelle |
|---|---|---|
| Italienische Städte (Florenz, Siena) | 50–60 % | MITTEL — Benedictow 2004 |
| England | 40–50 % | MITTEL — Benedictow 2004 |
| Frankreich | 30–50 % | MITTEL |
| HRR, städtisch | 40–60 % | MITTEL |
| HRR, ländlich | 20–40 % | MITTEL |
| Iberische Halbinsel | 30–40 % | MITTEL |
| Skandinavien | 30–50 % | MITTEL |
| Byzantinisches Reich | 30–50 % | MITTEL — byzantinische Chroniken |
| Nordseeküste / Friesland | 15–25 % (geringer) | MITTEL |

### 4.3 Dreißigjähriger Krieg (1618–1648)

| Region | Betroffenheit | Baukonsequenz |
|---|---|---|
| Württemberg, Pfalz | sehr hoch (>50 % Verlust) | starke Schlankung |
| Sachsen, Thüringen | hoch (30–50 %) | deutliche Schlankung |
| Bayern | mittel (20–30 %) | moderate Schlankung |
| Nordseeküste, Schweiz | gering (<15 %) | kaum verändert |
| England | nicht betroffen | kein Sprung |
| Frankreich | randlich (ab 1635) | kein Sprung im Holzbau |
| Niederlande | Achtzigjähriger Krieg (1568–1648), anderer Charakter | Sonderfall |
| Skandinavien | militärisch aktiv (Schweden), Heimatgebiet wenig betroffen | kein Sprung |

[Alle Werte: MITTEL — Wilson 2009; Parker 1984]

### 4.4 Reformationsbruch: regionale Differenzierung

Der Reformationsbruch (ca. 1517–1560) ist der am stärksten regional
differenzierte Bruch des gesamten Zeitraums.

| Region | Konfession | Konsequenz für Kirchenbau |
|---|---|---|
| Norddeutschland, Skandinavien | lutherisch | Kathedralbau stoppt, Klöster säkularisiert |
| England | anglikanisch (ab 1534) | Klöster säkularisiert, Kathedralbau stoppt |
| Schweiz (Zürich, Basel, Genf) | reformiert | Bilderstürme, Kirchenneubau minimal |
| Süddeutschland, Österreich | katholisch (nach Rekatholisierung) | Jesuitenbarock ab ca. 1560 |
| Frankreich | kath. (Hugenottenkriege 1562–1598, dann Edikt Nantes) | Kirchenbau gestört, nicht gestoppt |
| Spanien, Portugal | streng katholisch | Gegenreformation intensiviert Kirchenbau |
| Italien | katholisch | Kirchenbau ungebrochen |

**BVILLAGE-Implikation**: `religion_context` als Parameter in `CulturePolicy`,
mindestens mit den Ausprägungen `catholic`, `lutheran`, `reformed`, `anglican`.
Dieser Parameter steuert `church_building_active` und `monastery_presence`.

---

## 5. Zeitliche Schocks als BVILLAGE-Systemkonzept

### Was ein Schock ist

Ein Schock im BVILLAGE-Sinne ist ein historisches Ereignis, das:

1. Innerhalb weniger Jahre messbar verändert, welche Gebäude gebaut werden
2. Nicht durch graduelle Parameterinterpolation abbildbar ist
3. Räumlich differenziert wirkt (nicht uniform über alle Regionen)
4. Dokumentiert und datierbar ist (keine Spekulation)

Die mittelalterlichen Hauptschocks erfüllen alle vier Kriterien:
Pest (gesamteuropäisch), Dreißigjähriger Krieg (HRR-selektiv),
Holzmangel des 15. Jahrhunderts (städtisch-selektiv),
Reformation (konfessionell-selektiv).

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

Die Schockzonen sind nicht scharf datiert — sie haben Unsicherheitsbänder.
Die Pest erreicht verschiedene Regionen zu verschiedenen Zeiten
(1347–1351 für den Kern, bis 1353 für die Peripherie). Das Modell
muss diese Unschärfe explizit repräsentieren, nicht weginterpolieren.

### Nachwirkungen

Schocks haben Nachwirkungen, die länger dauern als der Schock selbst.
Die Pest erzeugt 150 Jahre demographische Instabilität (Wiederholungsepidemien
bis ins 16. Jahrhundert). Der Dreißigjährige Krieg braucht in manchen
Regionen 100 Jahre, bis die Bevölkerung Vorkriegsniveau erreicht.

In Parametertermen: Die Rückkehr zu Vorschockwerten ist nicht linear
und nicht universell. Manche Regionen erholen sich schnell (Kapitalzufluss,
günstiger Wiederaufbau). Andere persistieren jahrzehntelang im
Nachschockzustand.

---

## 6. Offene Forschungsfragen für BVILLAGE

**Frage 1 — Regionale Datierung des Konstruktionswechsels außerhalb des HRR**
Klein (2012) liefert Orientierung für Deutschland. Für England existieren
gute VAG-Daten. Für Frankreich, die Niederlande und Skandinavien fehlen
vergleichbar dichte Studien.

**Frage 2 — Pestdemographie für Baukontexte**
Benedictow (2004) und andere liefern Gesamtsterblichkeit. Aber für die
Baupolitik relevant ist: Wie veränderte sich der Anteil der Handwerker?
Wie die Kapitalkonzentration? Das ist für die meisten Regionen
nicht direkt belegt.

**Frage 3 — Querschnittsentwicklung über Epochen, gesamteuropäisch**
Eißing/Furrer (2023) liefern Messpunkte für das HRR. Eine
regionsübergreifende Querschnittskurve fehlt.

**Frage 4 — Erste Bauordnungen: Wann, wo, mit welchen Konsequenzen?**
Bauordnungen sind stadtrechtlich dokumentiert, aber nicht systematisch
für alle relevanten Städte ausgewertet. Besonders für englische und
französische Städte fehlt eine BVILLAGE-taugliche Zusammenstellung.

**Frage 5 — Byzantinische Epochenstruktur als BVILLAGE-Parameter**
Die byzantinische Bautradition wird von den BVILLAGE-Policies noch nicht
abgedeckt. Wenn das System auf orthodoxe Baukulturen ausgeweitet wird,
braucht es eine eigene Epochenstruktur (Makedonische Renaissance,
Komnenen-Blüte, Palaiologen-Renaissance, Osmanische Nachfolge).

---

## 7. Quellen und wissenschaftliche Grundlage

### 7.1 Zitierte Werke

**Andersson, Aron:** Medieval Sculpture in Sweden. Stockholm: Almqvist, 1991.
[MITTEL]

**Babelon, Jean-Pierre:** Châteaux de France au siècle de la Renaissance.
Paris: Flammarion, 1989.
*Standardwerk zur französischen Renaissancearchitektur.*
[MITTEL]

**Benedictow, Ole J.:** The Black Death 1346–1353. The Complete History.
Woodbridge: Boydell Press, 2004. ISBN 978-0-85115-943-2.
*Umfassendste Studie zur Pestmortalität. Hauptreferenz für Bruch 1.*
[MITTEL — Schätzwerte, keine direkten Messungen]

**Berger, Robert W.:** Versailles: The Château of Louis XIV.
University Park: Penn State University Press, 1985.
[MITTEL]

**Binding, Günther:** Baubetrieb im Mittelalter. Darmstadt: WBG, 1993.

**Binding, Günther:** Architektonische Formenlehre. Darmstadt: WBG, 1996.

**Bloom, Jonathan; Blair, Sheila:** The Grove Encyclopedia of Islamic Art
and Architecture. Oxford: Oxford University Press, 2009.
[MITTEL]

**Bony, Jean:** French Gothic Architecture of the 12th and 13th Centuries.
Berkeley: University of California Press, 1983.
[MITTEL/HART]

**Boockmann, Hartmut:** Die Stadt im späten Mittelalter. München: Beck, 1987.

**Brown, R. Allen:** The Normans. Woodbridge: Boydell, 1984.
[MITTEL]

**Chapelot, Jean; Fossier, Robert:** The Village and House in the Middle Ages.
London: Batsford, 1985.
*Französische Siedlungs- und Hausgeschichte. Grundlegendes Werk für
pan-europäische Haustypenanalyse.*
[MITTEL]

**Conant, Kenneth J.:** Carolingian and Romanesque Architecture 800–1200.
Harmondsworth: Penguin, 1959.
[MITTEL]

**Crossley, Paul:** Gothic Architecture. London: Thames & Hudson, 1988.
[MITTEL]

**Dodds, Jerrilynn D.:** Architecture and Ideology in Early Medieval Spain.
University Park: Penn State University Press, 1990.
*Mudéjar-Architektur und islamisch-christliche Transferprozesse.*
[MITTEL]

**Dyer, Christopher:** Standards of Living in the Later Middle Ages.
Cambridge: Cambridge University Press, 1989.

**Eißing, Thomas; Furrer, Benno et al.:** Vorindustrieller Holzbau.
Terminologie und Systematik. 2. Aufl. Heidelberg: Propylaeum, 2023.
DOI: https://doi.org/10.11588/sbhbf.2023.1.99050
[HART]

**Epstein, Stephan R.:** Craft Guilds, Apprenticeship, and Technological
Change. In: Journal of Economic History 58 (1998), H. 3, S. 684–713.
[MITTEL]

**Fitchen, John:** The Construction of Gothic Cathedrals. Chicago:
University of Chicago Press, 1961.

**Girouard, Mark:** Life in the English Country House. New Haven: Yale
University Press, 1978.
[MITTEL]

**Goldthwaite, Richard A.:** The Building of Renaissance Florence.
Baltimore: Johns Hopkins University Press, 1980.
*Florentinische Baupraxis, Pestkonsequenzen.*
[MITTEL/HART]

**Großmann, G. Ulrich:** Der Fachwerkbau in Deutschland. Petersberg:
Imhof, 2009.
[MITTEL]

**Hahnloser, Hans Robert (Hrsg.):** Villard de Honnecourt. Graz:
Akademische Druck- und Verlagsanstalt, 1972.
[HART]

**Harris, Jonathan:** Byzantium and the Crusades. London: Hambledon, 2003.
[MITTEL]

**Harvey, John:** The Perpendicular Style 1330–1485. London: Batsford, 1978.
[MITTEL]

**Herlihy, David:** The Black Death and the Transformation of the West.
Cambridge: Harvard University Press, 1997.
[MITTEL]

**Horn, Walter; Born, Ernest:** The Plan of St. Gall. 3 Bde. Berkeley:
University of California Press, 1979.
[HART]

**Jordan, William Chester:** The Great Famine. Princeton: Princeton
University Press, 1996.
[MITTEL]

**Kaspar, Fred:** Fachwerkbauten des 14. bis 16. Jahrhunderts in Westfalen.
Münster: Coppenrath, 1986.
[MITTEL/HART]

**Klein, Ulrich:** Zum aktuellen Forschungsstand des hoch- und
spätmittelalterlichen Holzbaus in Deutschland. In: DGAMN-Mitteilungen,
Bd. 24. Paderborn 2012.
DOI: https://doi.org/10.11588/dgamn.2012.1.17131
[HART]

**Krautheimer, Richard:** Early Christian and Byzantine Architecture.
4. Aufl. Harmondsworth: Penguin, 1986.
[MITTEL/HART]

**Machin, R.:** The Great Rebuilding: A Reassessment. In: Past & Present
77 (1977), S. 33–56.
[MITTEL]

**Mainstone, Rowland J.:** Hagia Sophia. London: Thames & Hudson, 1988.
[HART]

**Mango, Cyril:** Byzantine Architecture. London: Faber, 1976.
[MITTEL]

**Mark, Robert (Hrsg.):** Architectural Technology up to the Scientific
Revolution. Cambridge: MIT Press, 1993.
[MITTEL/HART]

**Marstaller, Tilmann:** Zu Lande und zu Wasser. In: DGAMN-Mitteilungen,
Bd. 24. Paderborn 2012.
[HART]

**McEvedy, Colin; Jones, Richard:** Atlas of World Population History.
Harmondsworth: Penguin, 1978.
[MITTEL]

**Meischke, Rudolph et al.:** Huizen in Nederland. Zwolle: Waanders, 1988.
*Niederländische Hausgeschichte. Standardwerk.*
[MITTEL]

**Nicol, Donald M.:** The Last Centuries of Byzantium 1261–1453.
2. Aufl. Cambridge: Cambridge University Press, 1993.
[MITTEL]

**Parker, Geoffrey:** The Thirty Years' War. London: Routledge, 1984.
[MITTEL/HART]

**Prak, Maarten:** Guilds and the Development of the Art Market During
the Dutch Golden Age. In: Simiolus 30 (2011).
[MITTEL]

**Recht, Roland:** Les Bâtisseurs des cathédrales gothiques. Straßburg:
Éditions des Musées de Strasbourg, 1989.

**Russell, Josiah C.:** Late Ancient and Medieval Population. Philadelphia:
American Philosophical Society, 1958.
[MITTEL]

**Salzman, Louis F.:** Building in England Down to 1540.
Oxford: Clarendon Press, 1952.
*Fundamentales Quellenwerk für englisches mittelalterliches Bauen:
Materialien, Löhne, Verträge, Bauordnungen.*
[HART]

**Stiewe, Heinrich:** Fachwerkhäuser in Deutschland. Darmstadt: WBG, 2007.
[MITTEL]

**Summerson, John:** Architecture in Britain 1530–1830.
Harmondsworth: Penguin, 1953. Neuauflage 1993.
*Wren und Wiederaufbau nach Großem Brand.*
[MITTEL]

**Ward-Perkins, Bryan:** The Fall of Rome and the End of Civilization.
Oxford: Oxford University Press, 2005.
[MITTEL]

**Wickham, Chris:** The Inheritance of Rome. London: Allen Lane, 2009.
[MITTEL]

**Wilson, Peter H.:** The Thirty Years War. Cambridge: Belknap Press, 2009.
[MITTEL/HART]

**Wittkower, Rudolf:** Architectural Principles in the Age of Humanism.
4. Aufl. London: Academy, 1971.
[MITTEL]

**Zimmermann, W. Haio:** Pfosten, Ständer und Schwelle und der Übergang
vom Pfosten- zum Ständerbau. In: Probleme der Küstenforschung 25 (1998).
[MITTEL/HART]

**Ziegler, Philip:** The Black Death. London: Collins, 1969.

---

### 7.2 Weiterführende Literatur

**Aston, Trevor H. (Hrsg.):** The Brenner Debate.
Cambridge: Cambridge University Press, 1985.
*Feudalkrise, Bevölkerungsrückgang, agrarer Wandel.*

**Beresford, Maurice; Hurst, John G.:** Wharram Percy: Deserted Medieval
Village. London: Batsford, 1990.
*Archäologie des frühmittelalterlichen Holzbaus in England.*
[HART — Grabungsbefunde]

**Cohn, Samuel K. Jr.:** The Black Death Transformed. London: Arnold, 2002.
*Kritische Neubewertung. Kontrastpunkt zu Benedictow.*

**Dyer, Christopher:** Making a Living in the Middle Ages.
New Haven: Yale University Press, 2002.

**Goodwin, Godfrey:** A History of Ottoman Architecture.
London: Thames & Hudson, 1971.
*Osmanische Nachfolge byzantinischer Kuppeltradition.*
[MITTEL]

**Lamb, Hubert H.:** Climate, History and the Modern World.
London: Routledge, 1982.
*Historische Klimatologie. MWP und Kleine Eiszeit.*

---

### 7.3 Primärquellen und Datenbanken

**Dendrochronologische Datenbanken**

International Tree-Ring Data Bank (ITRDB):
https://www.ncei.noaa.gov/products/paleoclimatology/tree-ring

Vernacular Architecture Group (VAG) Index:
https://www.vag.org.uk
[HART]

Labor für Dendrochronologie, Universität Bamberg (T. Eißing):
Über 5.500 untersuchte historische Gebäude mit 45.000+ Proben.

**Primärquellen: Schriftliche Zeugnisse**

Villard de Honnecourt, Bauhüttenbuch (ca. 1230):
BnF Ms. fr. 19093. Faksimile: Hahnloser 1972.

**Stadtchroniken und Ratsprotokoll-Editionen**

- Quellen zur Geschichte der Stadt Köln
- Urkundenbuch der Stadt Lübeck
- Frankfurter Bürgerbuch
- Calendar of Close Rolls (England) [HART]
- Rotuli Hundredorum (England) [HART]

---

*BVILLAGE Research Foundation — Achse 7 — v2.0*
