# Achse 4 — Wirtschaft und Handel
## Märkte, Materialflüsse und ökonomische Logik des mittelalterlichen Bauens

```
Dokument-Typ:  Research Foundation
Achse:         4 von 7
Scope:         BVILLAGE — alle Domains, alle Haustypen
Status:        v1.0
Referenziert von:
  MEDIEVAL_WORLD_OVERVIEW.md
  ARCH_POLICIES.md (MaterialPolicy, EcoMap)
  MEDIEVAL_01_PHYSICAL_WORLD.md (Ressourcenverfügbarkeit)
  MEDIEVAL_02_POLITICAL_GEOGRAPHY.md (Handelsrecht)
  MEDIEVAL_03_SOCIETY_HOUSEHOLD.md (Kaufkraft)
Evidenzgrade:
  [HART]   Direkt messbar, datierter Bestand, publizierte Messdaten
  [MITTEL] Wissenschaftlicher Konsens, erschlossen, nicht direkt messbar
  [SCHWACH] Analogieschluss, experimentelle Archäologie, Fachtradition
```

---

## Vorbemerkung

Wirtschaft und Handel beantworten die Frage: Was kostet Bauen, und
was kommt woher? Achse 4 verbindet die physische Ressourcenwelt
(Achse 1) mit der sozialen Nachfrageseite (Achse 3) durch den
Marktmechanismus.

Für BVILLAGE ist das die Grundlage der `MaterialPolicy` in ihrer
ökonomischen Dimension: Ein Baumaterial ist nicht verfügbar, weil es
physisch existiert, sondern weil es bezahlbar, transportierbar und
handelbar ist. Diese drei Bedingungen variieren regional und epochal.

---

## 1. Die mittelalterliche Wirtschaftsstruktur

### 1.1 Keine Marktwirtschaft im modernen Sinne

Das mittelalterliche Europa kennt keine freie Marktwirtschaft.
Preise werden durch Gewohnheitsrecht, Zunftordnungen und kirchliche
Normen (Zinsverbot, Gerechter Preis) reguliert. Märkte sind
institutionell eingebettet — nicht anonym.
[MITTEL — Lopez 1976; Spufford 2002]

Das bedeutet für das Bauen: Materialpreise folgen nicht Angebot
und Nachfrage allein. Sie folgen Zunftpreislisten, herrschaftlichen
Festsetzungen und lokalen Gewohnheiten. Innovation ist nicht
automatisch preisgünstiger als Tradition.

### 1.2 Die drei Wirtschaftssphären

Für das Bauen sind drei Wirtschaftssphären relevant, die
unterschiedliche Logiken haben:

**Subsistenzwirtschaft (ländlich)**
Selbstversorgung dominiert. Holz kommt aus dem eigenen Wald oder dem
Gemeindewald. Handwerkliche Arbeit wird durch Nachbarschaftshilfe
und Gegenseitigkeit erbracht. Wenig Geldwirtschaft.
Konsequenz für Bauen: Materialauswahl ist fast ausschließlich
lokal und durch Verfügbarkeit bestimmt, nicht durch Preis.
[MITTEL — Duby 1962; Dyer 1989]

**Städtische Geldwirtschaft**
Professionalisierte Handwerker, Lohnarbeit, Marktpreise für
Materialien. Zunftordnungen regulieren Löhne und Preise.
Kapital kann akkumuliert und investiert werden.
Konsequenz für Bauen: Materialwahl nach Preis-Leistung innerhalb
lokaler Verfügbarkeit. Fernhandel für Luxusmaterial möglich.
[MITTEL — Lopez 1976; Epstein 1998]

**Fernhandel**
Kaufleute, Hansekaufleute, Kircheninstitutionen handeln über
große Distanzen. Luxusgüter und Spezialmaterialien (seltene
Holzarten, Naturstein, Metallerze) können über Hunderte
von Kilometern transportiert werden.
Konsequenz für Bauen: Für sehr reiche Auftraggeber entstehen
Handlungsräume, die die physische Lokalverfügbarkeit überschreiten.
[HART — Spufford 2002; Dollinger 1998]

---

## 2. Baumaterialien als Handelsgüter

### 2.1 Was gehandelt wird — und was nicht

Nicht alle Baumaterialien sind Handelsgüter im gleichen Sinne.
Die Entscheidung, ein Material zu importieren, hängt von
Wert-zu-Gewicht-Verhältnis und Transportmöglichkeiten ab.

| Material | Handelsfähigkeit | Transportweg | Distanz typisch |
|---|---|---|---|
| Holz (Massenware) | mittel — schwer, sperrlig | Fluss zwingend | bis 200 km flussabwärts |
| Eichenholz (Qualität) | gut | Fluss | bis 300 km |
| Naturstein (Bruchstein) | gering — sehr schwer | kaum | < 30 km |
| Naturstein (bearbeitet) | mittel | Fluss oder Schiff | bis 200 km |
| Rhenischer Tuff | gut (leicht) | Rhein, Mosel | bis 500 km |
| Backstein | mittel | Schiff in Hansegebiet | bis 300 km |
| Kalk (gebrannt) | gut | Fluss | bis 100 km |
| Schiefer (Dach) | gut (leicht) | Fluss | bis 300 km |
| Breton Slate (England) | gut | Schiff | bis 500 km |
| Dachziegel | mittel | Fluss | bis 100 km |
| Stroh, Reet | kaum | Land | < 20 km |
| Lehm, Ton | nicht — zu schwer | — | < 5 km |

[MITTEL — Binding 1993; Spufford 2002; für Rhenischen Tuff: HART —
archäologisch und schriftlich dokumentiert]

### 2.2 Holzhandel: Das wichtigste Handelsgut

Holz ist das volumenmäßig wichtigste Baumaterial und gleichzeitig
ein komplexes Handelsgut, weil seine Transportfähigkeit stark
von der Infrastruktur abhängt.

**Flößerei**: Langer Holztransport funktioniert nur auf Wasserläufen.
Eißing (2023) und Marstaller (2012) haben dendrochronologisch
nachgewiesen, dass Bauholz regulär über Flüsse über 100–200 km
transportiert wurde. [HART]

Bekannte Holzhandelsrouten:
- Schwarzwälder Tanne → Rhein → Niederrhein, Holland
- Thüringer Nadelholz → Saale, Elbe → norddeutsche Städte
- Baltisches/preußisches Holz → Ostsee → Hanse-Städte (Lübeck, Hamburg)
- Skandinavisches Mastholz → Nordsee → Niederlande, England

[HART für Hansehandel — Dollinger 1998; MITTEL für andere Routen]

**BVILLAGE-Implikation**: `timber.species` als Funktion von
`region` muss hydrographische Einzugsgebiete als Grundstruktur
verwenden. Ein Gebäude an der Weser kann Holz aus dem Thüringer
Wald haben. Eines ohne Flussanbindung nur lokales Material.

### 2.3 Stein und Spezialstein

Naturstein ist grundsätzlich schwer und teuer zu transportieren.
Ausnahmen:

**Rhenischer Tuff** (Vulkangestein aus der Eifel): Außergewöhnlich
leicht, gut bearbeitbar. Über Rhein und Mosel bis in die Niederlande,
nach England (Canterbury Cathedral, Kirchenbau) und Nordfrankreich
transportiert. [HART — archäologisch und historisch dokumentiert;
Binding 1993]

**Caen Stein** (Frankreich): Über Kanal nach England exportiert.
Verwendung in englischen Kathedralen und Burgen. [HART]

**Breton Slate** (Bretagne): Über Atlantikküste nach England.
Erscheint in englischen Dachdeckungen des 12.–14. Jahrhunderts.
[MITTEL — Rackham 1986]

**BVILLAGE-Implikation**: Für `stone.type` kann in seltenen Fällen
(sehr reicher Auftraggeber, Fluss- oder Seeanbindung) Fernstein
erscheinen. Das ist die Ausnahme, nicht die Regel — und muss als
Sonderfall mit hohem `wealth`-Trigger modelliert werden.

---

## 3. Arbeitskosten: Der größte Kostenfaktor

### 3.1 Lohnstruktur

In der mittelalterlichen Bauwirtschaft sind Arbeitskosten der
dominante Kostenfaktor, nicht Materialkosten. Das gilt besonders
für den Profanbau, wo keine großen Steinmengen anfallen.
[MITTEL — Dyer 1989; Epstein 1998]

Lohnhierarchie (vereinfacht):
- Wandernder Tagelöhner (ungelernt): Basiswert
- Maurer, Zimmerer (gelernt): ca. 1,5–2× Tagelöhner
- Meister (Zunftmitglied): ca. 2–3× Tagelöhner
- Spezialist (Schreiner, Bildschnitzer): 3–5× Tagelöhner

[SCHWACH — Lohnlisten fragmentarisch; Dyer 1989 für England;
übertragbar mit Vorbehalt]

### 3.2 Saisonalität der Bautätigkeit

Bauen ist saisonal. Holzfällung: Winter (saftarmes Holz, geringerer
Schädlingsbefall). Abbund: Frühjahr (Zimmerplatz, gutes Wetter).
Aufrichtung: Sommer (Trockenheit, lange Arbeitstage). Verfugung
und Verputz: Herbst (vor dem Frost).
[MITTEL — Binding 1993; Eißing/Furrer 2023]

Dendrochronologisch ist die Saisonalität in vielen Fällen nachweisbar:
Waldkante (letzter Jahrring) gibt die Fällsaison an.
[HART — Eißing/Furrer 2023]

Konsequenz: Ein großes Gebäude dauert über mehrere Jahre. Planung
und Kapital müssen entsprechend saisonal vorgehalten werden.

### 3.3 Post-Pest-Lohneffekte

Nach der Pest von 1347–1353 steigen Löhne dramatisch. Weniger
Arbeitskräfte, gleiche (oder höhere) Nachfrage = Preisdruck.
[HART für England: Dyer 1989; MITTEL für Deutschland]

Für das Bauen bedeutet das: Die Wirtschaftlichkeit des Bauens
verschiebt sich. Materialoptimierung wird wichtiger (weniger Holz
durch Stockwerksbau), Rationalisierung der Abläufe (Vorfertigung)
wird ökonomisch attraktiver.

**BVILLAGE-Implikation**: Der Übergang zum Stockwerksbau ist nicht
nur konstruktiv motiviert (kürzere Ständer, Holzknappheit). Er ist
auch ökonomisch motiviert: weniger Arbeitszeit pro Gebäude durch
modulare Vorfertigung. Beides verstärkt sich.

---

## 4. Das Zunftsystem als Wirtschaftsregulierung

### 4.1 Zünfte als Marktakteure

Zünfte sind nicht nur Berufsorganisationen — sie sind Kartelle,
die Preise, Qualitäten und Wettbewerb regulieren. Das hat direkte
Konsequenzen für die Bauwirtschaft:

- **Preisfixierung**: Zunftordnungen legen Mindestlöhne und
  Mindestpreise fest. Billigkonkurrenz durch Nichtmitglieder
  ist illegal.
- **Qualitätskontrolle**: Meisterstücke und Zunftprüfungen
  sichern ein Mindestniveau. Schlechte Arbeit kann zum
  Zunftausschluss führen.
- **Innovationsfilter**: Neue Techniken müssen durch den
  sozialen Filter der Zunft. Das verlangsamt Innovation,
  sichert aber auch Qualität.

[MITTEL — Epstein 1998; Schulz 2010]

### 4.2 Zünfte und Materialhandel

Viele Zünfte kontrollieren auch den Materialhandel in ihrem
Gewerbebereich. Zimmerererzünfte können Holzeinkauf regeln.
Maurerzünfte können Steinlieferanten binden.

Das erzeugt lokale Monopole auf Materialketten — und begrenzt den
Wettbewerb zwischen lokalen und auswärtigen Lieferanten.
[MITTEL — Schulz 2010; Epstein 1998]

---

## 5. Investition in Bauen: Kapitallogik

### 5.1 Warum man mehr baut als nötig

Überinvestition in Gebäude ist ein rationales Verhalten in einer
Gesellschaft ohne moderne Finanzinstrumente. Das Gebäude ist:
- Kapitalanlage (steigt im Wert, vererbt sich)
- Kreditsicherheit (Grundpfand)
- Werbung (Repräsentation zieht Kunden und Partner)
- Soziale Investition (Prestige öffnet Türen)

[MITTEL — Boockmann 1987; Schulz 2010]

Das erklärt, warum Handwerker mehr bauen als sie zum Leben brauchen,
und Patrizier deutlich mehr als technisch erforderlich wäre. Der
Mehraufwand ist Investition in zukünftige Erträge, nicht Verschwendung.

### 5.2 Bauen als Marktindikator

Bautätigkeit ist ein Indikator für wirtschaftliche Gesundheit.
Booms und Krisen schreiben sich direkt in Bauvolumen und Bauqualität.

Bekannte Baubooms:
- Staufische Blüte (12.–13. Jh.): Stadtgründungen, Burgenbau
- Post-Pest-Boom (1360–1400): Konzentriertes Erbschaftskapital
- Hanseblüte (14.–15. Jh.): Norddeutsche Speicher und Kaufmannshäuser
- Reformationszeit (16. Jh.): Reichsstädtische Bürgerhäuser

Bekannte Baueinbrüche:
- Große Hungersnot (1315–1322): fast kein Neubau
- Schwarzer Tod (1347–1353): Baustillstand
- Dreißigjähriger Krieg (1618–1648): Baukollaps in betroffenen Regionen

[MITTEL — Herlihy 1997; Wilson 2009; Boockmann 1987]

---

## 6. Handelsrouten und ihre Baukulturdiffusion

Handelsrouten sind nicht nur Materialwege — sie sind auch Wissens-
und Technologiewege. Wo Kaufleute gehen, gehen auch Handwerker.
Wo Handwerker gehen, geht Bautechnik.

Wichtige Diffusionsachsen für Bautechnologie:

**Rheinachse**: Von Basel nach Köln. Verbindet alemannischen
Fachwerkraum mit Niederrhein und den Niederlanden. Technologie-
und Materialtransfer in beide Richtungen.

**Elbeachse**: Von Böhmen und Sachsen nach Hamburg. Verbindet
mitteldeutschen Fachwerkraum mit der Hanse.

**Ostseeachse**: Von Lübeck nach Danzig, Riga, Reval. Hansisches
Netz, Backsteingotik-Diffusion, Holzimport aus dem Baltikum.

**Alpentransversalen** (Brenner, Gotthard, Mont Cenis): Verbinden
deutschsprachigen Raum mit Oberitalien. Renaissance-Einflüsse
kommen über diese Routen.

[MITTEL — Spufford 2002; Dollinger 1998; Binding 1993]

**BVILLAGE-Implikation**: Bautechnologie-Diffusion folgt diesen
Achsen. Neue Konstruktionselemente breiten sich entlang von
Handelsrouten aus, nicht flächig. Die `StylePolicy`-Zeitachse
für Innovationsübernahme ist längs dieser Achsen früher als
quer dazu.

---

## 7. Offene Forschungsfragen

**Frage 1 — Preisindizes für Baumaterialien**
Historische Preislisten für Bauholz, Ziegel und Handwerkerlöhne
existieren punktuell (besonders für England gut dokumentiert).
Für Deutschland sind systematische Preisreihen selten und
regionsspezifisch. Für genaue `wealth`-Kalibrierung wäre das
wünschenswert.

**Frage 2 — Marktreichweiten für Spezialholz**
Wie weit war Eichenimport in Tannengebieten üblich — und ab
welchem `wealth`-Niveau? Das ist aus Dendrochronologie
grundsätzlich rekonstruierbar, aber noch nicht systematisch.

**Frage 3 — Zunftwirtschaft und Marktpreise**
Wie stark wichen tatsächliche Marktpreise von Zunft-Fixpreisen ab?
Das ist eine wirtschaftshistorische Frage, die die
`MaterialPolicy`-Preismodellierung direkt beeinflusst.

---

## 8. Quellen und wissenschaftliche Grundlage

### 8.1 Zitierte Werke

**Binding, Günther:** Baubetrieb im Mittelalter. Darmstadt: WBG, 1993.
*Materialketten, Lohnstruktur, Saisonalität des Bauens.*

**Dollinger, Philippe:** Die Hanse. Stuttgart: Kröner, 1998.
ISBN 978-3-520-37105-4.
*Handelsnetzwerke, Materialtransporte, Holzhandel.*
[HART/MITTEL]

**Duby, Georges:** L'économie rurale et la vie des campagnes dans
l'Occident médiéval. Paris: Aubier, 1962. Deutsche Ausgabe:
Krieger und Bauern. Frankfurt: Suhrkamp, 1977.
*Subsistenzwirtschaft, Grundherrschaft, ländliche Ökonomie.*
[MITTEL]

**Dyer, Christopher:** Standards of Living in the Later Middle Ages.
Cambridge: Cambridge University Press, 1989.
*Lohnstruktur, Lebensstandard, Post-Pest-Lohneffekte. Für England —
methodisch vorbildhaft.*
[MITTEL/HART für England]

**Eißing, Thomas; Furrer, Benno et al.:** Vorindustrieller Holzbau.
Heidelberg: Propylaeum, 2023.
DOI: https://doi.org/10.11588/sbhbf.2023.1.99050
*Holztransportnachweise, Flößerei als Infrastruktur.*
[HART]

**Epstein, Stephan R.:** Craft Guilds, Apprenticeship, and
Technological Change in Preindustrial Europe. In: Journal of
Economic History 58 (1998), H. 3, S. 684–713.
*Zünfte als Wirtschaftsakteure und Wissenstransfer-Institutionen.*
[MITTEL]

**Herlihy, David:** The Black Death and the Transformation of the
West. Cambridge: Harvard University Press, 1997.
*Wirtschaftliche Folgen der Pest. Lohneffekte, Kapitalkonzentration.*
[MITTEL]

**Lopez, Robert S.:** The Commercial Revolution of the Middle Ages,
950–1350. Cambridge: Cambridge University Press, 1976.
*Entstehung der mittelalterlichen Geldwirtschaft. Kapitalmärkte,
Handelsnetzwerke.*
[MITTEL]

**Marstaller, Tilmann:** Zu Lande und zu Wasser. In: DGAMN-
Mitteilungen Bd. 24. Paderborn 2012, S. 39–56.
*Holzhandelsnachweise, Flussinfrastruktur.*
[HART]

**Schulz, Knut:** Handwerk, Zünfte und Gewerbe. Darmstadt: WBG, 2010.
*Zünfte als Marktakteure, Preisregulierung, Materialhandel.*
[MITTEL]

**Spufford, Peter:** Power and Profit. The Merchant in Medieval Europe.
London: Thames & Hudson, 2002. ISBN 978-0-500-25118-8.
*Fernhandel, Handelsnetzwerke, Güterströme. Standardwerk.*
[MITTEL/HART]

**Wilson, Peter H.:** The Thirty Years War. Europe's Tragedy.
Cambridge: Belknap Press, 2009.
*Wirtschaftliche Disruption, Baukollaps.*
[MITTEL/HART]

---

### 8.2 Weiterführende Literatur

**Pirenne, Henri:** Medieval Cities. Their Origins and the Revival
of Trade. Princeton: Princeton University Press, 1925. Neuauflage 2014.
*Fernhandel als Städtegründungsfaktor. Klassiker, historisch überholt
in Teilen, konzeptionell einflussreich.*

**Pounds, Norman J. G.:** An Economic History of Medieval Europe.
London: Longman, 1974. 2. Aufl. 1994.
*Breite ökonomische Gesamtdarstellung. Gut für Überblick.*

---

*BVILLAGE Research Foundation — Achse 4 — v1.0*
