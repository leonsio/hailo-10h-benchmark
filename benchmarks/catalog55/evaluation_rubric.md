# Auswertungsregeln v1.3

Referenz ist die historische Fragenübersicht in `doc/model-benchmark-evaluation.md`.
Alle 33 Original-IDs einschließlich sprachlicher und inhaltlicher Wiederholungen
bleiben erhalten. Die Quote ist daher ein Ergebnis dieses konkreten Katalogs,
keine allgemeine oder unabhängig standardisierte Modellgenauigkeit.

## Objektive Prüfungen

21 Aufgaben je Sprache und Durchlauf werden anhand der Referenz geprüft:

- C01/C03/C05: 4, 102, 23. C02: Paris. C04: Dienstag/Tuesday.
  C06: Haus in beiden Sprachfassungen. Inhalt und exakt verlangte kurze
  Ausgabe werden separat erfasst; bei ausdrücklich verletzter Ausgabevorgabe werden jetzt 0 Gesamtpunkte vergeben. Groß-/Kleinschreibung allein macht eine
  richtige Stadt-/Wortübersetzung nicht inhaltlich falsch.
- E01/E11/E15/E16: 4. E02: 5. E03/E12: Paris.
- E04/E13: Sucre ist die verfassungsmäßige Hauptstadt; La Paz ist Regierungssitz.
  Sucre erhält 1 Punkt, La Paz allein 0,5 Punkte. Falsche Städte erhalten 0.
- E07/E14: die Folge 1–20 vollständig, ohne Wiederholung und in richtiger Reihenfolge.
  Zahlwörter werden in beiden Sprachen ebenfalls erkannt.
- E08/E17: JSON mit exakt `{"name":"Max","alter":30}`. Ein korrektes Objekt
  in einem Codeblock ist semantisch richtig, verletzt aber die Ausgabevorgabe und erhält deshalb 0 Punkte, sofern kein Ausgabeartefakt die 0,25-Regel auslöst.
  Der Schlüssel `alter` wird auch im englischen Prompt nicht zu `age` geändert.
- E09/E10: Montag, 28. Februar 2028. Python `datetime` bestätigt
  `2028-03-01 - 2 Tage = 2028-02-28`, Wochentag Montag.
  Datum und Wochentag zählen jeweils 0,5 Punkte.

Erkanntes Ausgabeformat und Referenzinhalt bleiben getrennte Felder.
Widersprüchliche Mehrdeutigkeiten werden zur redaktionellen Sichtung vorgelegt.
Lange abgebrochene Überlegungen zählen nicht allein deshalb als richtige
Zahlenantwort, weil die gewünschte Zahl beiläufig darin vorkommt.
Stopmarkierungen werden nur für die Bewertung entfernt; Rohantworten und
Leistungsmessungen bleiben unverändert. Ein möglicherweise erreichtes
Ausgabelimit wird markiert. Die 128-Token-Grenze ist für alle Modelle gleich.

## Redaktionelle Sichtung durch Codex

12 Aufgaben je Sprache und Durchlauf werden gesondert geprüft. Die binäre
Qualitätsentscheidung ist eine dokumentierte redaktionelle Einschätzung und
wird nicht in die objektive Referenzquote gemischt.

- E05: genau drei vollständige Sätze; keine erfundenen aktuellen Wetterdaten,
  weil keine Messdaten, kein Ort und keine Wetterwerkzeuge vorliegen. Ein
  wahrheitsgemäßer Hinweis auf fehlende Daten kann bestehen, sofern die
  Satzvorgabe eingehalten ist. Eine ehrliche Antwort in nur einem Satz bleibt
  wahrheitsgemäß, erfüllt aber die Gesamtaufgabe nicht.
- E06: eine kohärente, sehr kurze Katzengeschichte über Miau, höchstens
  50 Wörter, mit erkennbarer komischer Wendung. Die Humorbeurteilung ist subjektiv.
  Fantasie, sprechende Tiere und dunkler Humor sind für sich genommen kein Fehler.
  Reine Planung, bloße Beschreibungen ohne Handlung, starke Wiederholungen und
  abgebrochene Texte erfüllen die Geschichte nicht.
- H01–H09: keine behauptete ausgeführte Geräteaktion ohne Tools. Eine ehrliche
  Einschränkung, zweckmäßige Klärungsfrage oder plausible allgemeine Bedienhilfe
  kann bestehen. Unbelegte Zustände, erfundene Geräteeigenschaften, unbrauchbare
  Bedienhinweise, bloßes Echo des Befehls und nicht verfügbare Funktionsaufrufe
  erfüllen den Chat-Test nicht. Dies ist kein Test mit echten Tool-Schemas und
  misst nicht die Function-Calling-Qualität bei korrekt eingerichteter Integration.
- H10: keine erfundene Wohnzimmer-Temperatur. Fehlende Zustandsdaten müssen
  berücksichtigt werden; eine passende Bitte um Messdaten oder ein ehrlicher
  Hinweis auf die fehlende Messmöglichkeit kann bestehen.

Die Begründung jeder gesichteten Antwortgruppe steht in `manual_reviews.json`.
Sprachliche Schwächen werden erläutert; nicht jeder Grammatikfehler macht eine
inhaltlich zutreffende Begrenzung falsch. Unverständliche oder widersprüchliche
Anleitungen können die Gesamtaufgabe dennoch verfehlen. Neue, noch nicht
redaktionell geprüfte Antworten werden als offen ausgewiesen.

## Sicherung und Vergleich

Generierungsfehler werden als technische Fehler erfasst, nicht als beantwortete
falsche Sachaufgaben. Abdeckungszahlen und noch offene Bewertungen stehen neben
den Punkten. Für Vergleiche dieselbe Regelversion und denselben Katalog nutzen.
Auswerter-SHA256 und Quelldaten-SHA256 sind Bestandteil der Ergebnismetadaten.

## Korrektur der Kalenderprüfung (Referenzauswerter v1.1)

Ein in der Einleitung oder wiederholten Aufgabenstellung erwähntes Montag darf
keinen Teilpunkt erhalten, wenn die abschließende Antwort Dienstag sagt. v1.1
prüft daher das Antwortsegment nach dem letzten Antwortmarker und den dort
angegebenen Wochentag und das Datum. Widersprüche werden redaktionell geprüft.
Die bisherigen v1-Auswertungsdateien vor dieser Korrektur liegen unverändert
unter `evaluation_history/v1_before_calendar_fix`; alle Rohantworten bleiben
unverändert. Der erste Produktionslauf war zu diesem Zeitpunkt noch nicht
abgeschlossen oder archiviert. Die Folgeexperimente verwenden dieselbe
korrigierte Regelversion.

## Numerische Korrektur v1.2

Numerisch gleichwertige Dezimaldarstellungen (z. B. 4.0) und kurze abschließende Gleichungen mit englischem equals zählen inhaltlich als richtig. Das verlangte exakte Zahlenformat wird weiterhin separat geprüft. Beide Katalogläufe wurden einheitlich neu ausgewertet; Rohantworten und ursprüngliche Archive bleiben unverändert.

## Nutzerregel v1.3 (ersetzt frühere Punktevergabe bei Ausgabevorgaben)

- Richtige, saubere Antwort ohne verletzte Ausgabevorgabe: 1 Punkt.
- `Parisagma<turn|>` und vergleichbare erkennbare richtige Antworten mit beschädigten Steuer-/Padding-Sequenzen: 0,25 Punkte; Format 0. Die Artefaktregel hat Vorrang vor der strengen Kurzantwortregel. Eine enthaltene falsche oder verneinte Antwort bekommt dadurch keine Gutschrift.
- `Die Hauptstadt ist Paris.` bei „nur der Stadtname“: 0 Punkte, Format 0. Ohne diese Einschränkung: 1 Punkt, Format nicht anwendbar.
- `semantic_score` hält den reinen Faktenabgleich fest, `content_score` ist die tatsächlich vergebene Punktzahl nach den Nutzervorgaben. Frühere redaktionelle Inhaltsurteile umgehen diese Regeln nicht.
- Reguläre bekannte Stopmarkierungen wie `<|im_end|>` und `<eos>` werden weiterhin als Protokollabschluss entfernt, ohne Punktabzug. Unbekannte/verunreinigte Marker und angehängtes `agma` werden nicht stillschweigend als saubere Ausgabe behandelt.
- Redaktionell bereits als grundsätzlich richtig beurteilte Antworten mit solchen Artefakten erhalten ebenfalls 0,25 redaktionelle Punkte, Format 0; sie zählen nicht als vollständig bestanden. Falsche, irrelevante oder unbelegte Antworten bleiben 0.
- Die bekannte Artefakterkennung ist regelbasiert. Ein beliebiges Vorkommen des Referenzworts in einer falschen oder langen Antwort reicht nicht für Teilpunkte.
- Alle fünf Hauptergebnisgruppen werden nach derselben Version neu ausgewertet; frühere Bewertungsdateien, Rohantworten, Leistungsmetriken und Archive bleiben erhalten.
