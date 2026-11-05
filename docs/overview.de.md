# Hailo-10H-Benchmark: Gesamtbewertung

[Deutsch](overview.de.md) · [English](overview.en.md) · [Repository](../README.md)

Datengrundlage: 4 Kombinationen aus Runtime und Model Zoo sowie der erfolgreiche Qwen3-4B-Nachtest. Raspberry Pi CM5, etwa 15 GiB Host-RAM und Hailo-10H mit 8 GB. Alle hier dargestellten Hauptbewertungen verwenden **reference-checks-v1.3**; ältere Berichte/Archive können frühere Punktzahlen enthalten.

## Versuchsmatrix

| Runtime / firmware / driver | Model Zoo 5.4 | Model Zoo 5.5 |
|---|---|---|
| 5.4.0 | [Results](runs/runtime54-zoo54/README.de.md) | [Results](runs/runtime54-prefetch/README.de.md) |
| 5.5.0 | [Results](runs/runtime55-zoo54/README.de.md) | [Results](runs/runtime55-zoo55/README.de.md) + [Qwen3-4B retry](runs/runtime55-zoo55-qwen4b-persistent/README.de.md) |

„Runtime“ bezeichnet hier die gemeinsam aktualisierten Komponenten Firmware, Runtime, Python-Binding und PCIe-Treiber. Der Effekt des Treibers allein wurde nicht isoliert.

## Antwortbewertung über alle vier Kombinationen

| Model | RT5.4 / Zoo5.4 | RT5.4 / Zoo5.5 | RT5.5 / Zoo5.4 | RT5.5 / Zoo5.5 |
|---|---:|---:|---:|---:|
| Qwen3-4B-Instruct-2507 | — | — | — | 98/126 |
| Gemma4-E2B-Instruct | — | — | — | 79.5/126 |
| Qwen3-VL-4B-Instruct | — | — | — | 105.5/126 |
| DeepSeek-R1-Distill-Qwen-1.5B | 10.25/126 | 10.25/126 | 10.25/126 | 10.25/126 |
| Qwen2.5-Coder-1.5B-Instruct | 98.5/126 | 98.5/126 | 98.5/126 | 98.5/126 |
| Qwen2-1.5B-Instruct | 90.5/126 | 90.5/126 | 90.5/126 | 90.5/126 |
| Qwen2-VL-2B-Instruct | 64.5/126 | 84/126 | 64.5/126 | 84/126 |
| Qwen2.5-1.5B-Instruct | 72.5/126 | 72.5/126 | 72.5/126 | 72.5/126 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 63/126 | 68.5/126 | 63/126 | 68.5/126 |
| Llama3.2-1B-Instruct | 39/126 | 39/126 | 39/126 | 39/126 |
| Qwen3-1.7B-Instruct | 112.5/126 | 112.5/126 | 112.5/126 | 112.5/126 |
| Qwen3-VL-2B-Instruct | 77/126 | 107/126 | 77/126 | 107/126 |
| gemma-4-E2B-it | 108/126 | 108/126 | 108/126 | 108/126 |

Pro vollständigem Modelllauf sind 126 objektive Punkte möglich; 72 redaktionelle Aufgaben werden getrennt bewertet. Ähnliche und wiederholte Fragen machen dies nicht zu einer allgemeinen Modellgenauigkeit.

## Decode-Durchsatz über alle vier Kombinationen

| Model | RT5.4 / Zoo5.4 | RT5.4 / Zoo5.5 | RT5.5 / Zoo5.4 | RT5.5 / Zoo5.5 |
|---|---:|---:|---:|---:|
| Qwen3-4B-Instruct-2507 | — | — | — | 2.10 |
| Gemma4-E2B-Instruct | — | — | — | 5.67 |
| Qwen3-VL-4B-Instruct | — | — | — | 2.29 |
| DeepSeek-R1-Distill-Qwen-1.5B | 7.54 | 7.43 | 7.84 | 7.70 |
| Qwen2.5-Coder-1.5B-Instruct | 8.07 | 8.05 | 8.30 | 8.33 |
| Qwen2-1.5B-Instruct | 8.09 | 8.07 | 8.32 | 8.32 |
| Qwen2-VL-2B-Instruct | 7.01 | 7.55 | 7.20 | 7.75 |
| Qwen2.5-1.5B-Instruct | 7.12 | 7.16 | 7.37 | 7.40 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 6.72 | 6.77 | 6.86 | 7.01 |
| Llama3.2-1B-Instruct | 9.98 | 9.90 | 10.11 | 10.09 |
| Qwen3-1.7B-Instruct | 4.77 | 4.71 | 4.85 | 4.77 |
| Qwen3-VL-2B-Instruct | 4.70 | 4.81 | 4.77 | 4.88 |
| gemma-4-E2B-it | 8.42 | 8.36 | 8.37 | 8.48 |

Token/s als arithmetische Mittelwerte. CPU-Gemma verwendet in jeder Spalte dasselbe LiteRT-Artefakt; die Zuordnung zu den Läufen macht es nicht zu einem Model-Zoo-Modell.

## Runtime 5.5 mit Zoo 5.5: Gesamtbild

| Modell | Antworten | Ladungen | Laden s | TTFT DE / EN s | Decode Token/s | Datei GiB | Hailo-RAM GiB | Host-RSS GiB | Objektive Punkte | Redaktionelle Punkte | Offen |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen3-4B-Instruct-2507 | 198 | 3 | 18.85 | 3.08 / 1.55 | 2.10 | 5.27 | 6.13 | 0.12 | 98/126 | 58/72 | 0 |
| Gemma4-E2B-Instruct | 198 | 3 | 13.48 | 0.52 / 0.45 | 5.67 | 3.11 | 3.78 | 0.08 | 79.5/126 | 59.25/72 | 0 |
| Qwen3-VL-4B-Instruct | 198 | 3 | 22.87 | 3.28 / 1.65 | 2.29 | 6.08 | 6.95 | 0.12 | 105.5/126 | 59/72 | 0 |
| DeepSeek-R1-Distill-Qwen-1.5B | 198 | 3 | 5.72 | 1.74 / 1.46 | 7.70 | 2.10 | 2.49 | 0.07 | 10.25/126 | 0/72 | 0 |
| Qwen2.5-Coder-1.5B-Instruct | 198 | 3 | 3.84 | 0.63 / 0.32 | 8.33 | 1.55 | 2.02 | 0.07 | 98.5/126 | 16/72 | 0 |
| Qwen2-1.5B-Instruct | 198 | 3 | 3.94 | 0.63 / 0.32 | 8.32 | 1.54 | 2.02 | 0.07 | 90.5/126 | 38/72 | 0 |
| Qwen2-VL-2B-Instruct | 198 | 3 | 8.10 | 0.55 / 0.28 | 7.75 | 2.91 | 3.50 | 0.08 | 84/126 | 30/72 | 0 |
| Qwen2.5-1.5B-Instruct | 198 | 3 | 5.22 | 0.73 / 0.37 | 7.40 | 2.32 | 2.81 | 0.07 | 72.5/126 | 31/72 | 0 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 198 | 3 | 6.56 | 0.80 / 0.40 | 7.01 | 2.43 | 3.02 | 0.09 | 68.5/126 | 7/72 | 0 |
| Llama3.2-1B-Instruct | 198 | 3 | 3.60 | 0.67 / 0.39 | 10.09 | 1.26 | 1.74 | 0.07 | 39/126 | 21/72 | 0 |
| Qwen3-1.7B-Instruct | 198 | 3 | 7.02 | 1.25 / 0.63 | 4.77 | 2.75 | 3.40 | 0.08 | 112.5/126 | 9/72 | 0 |
| Qwen3-VL-2B-Instruct | 198 | 3 | 7.96 | 1.26 / 0.64 | 4.88 | 2.97 | 3.75 | 0.08 | 107/126 | 0/72 | 0 |
| gemma-4-E2B-it | 198 | 3 | 2.74 | 1.26 / 1.25 | 8.48 | 2.41 | — | 0.46 | 108/126 | 66/72 | 0 |

## Einordnung

- Das Upgrade verbessert vor allem Modellkompatibilität und Ladezeiten. Gemma4-E2B und Qwen3-VL-4B laufen jetzt; Qwen3-4B wurde im späteren Nachtest erfolgreich geprüft. Die Ladefehler unter Runtime 5.4 sind keine gültige Grundlage für einen Qualitätsvergleich dieser Modelle.
- Bei den neun gemeinsamen nativen Modellen und der CPU-Referenz sind alle 1.980 zugeordneten Rohantworten der Zoo-5.5-Läufe unter Runtime 5.4/5.5 identisch. Qualitätsänderungen entstehen damit durch Katalogartefakte oder geänderte Bewertungsregeln, nicht durch eine beobachtete Antwortänderung infolge des Runtime-Upgrades.
- Die meisten gemeinsamen nativen Modelle gewinnen mit Runtime 5.5 nur etwa 1–4 % Decode-Durchsatz; die CPU-Referenz schwankt selbst um etwa 1,5 %. Diese kleinen Gewinne vorsichtig bewerten. Deutlichere Ladezeitverkürzungen: Qwen3-VL-2B (16,03 → 7,96 s), Qwen2-VL-2B (12,31 → 8,10 s) und Qwen2.5-1.5B (8,77 → 5,22 s). Dateicaches und Hintergrunddownloads waren nicht kontrolliert.
- Zoo 5.5 verbessert insbesondere die objektiven Textchat-Ergebnisse von Qwen3-VL-2B gegenüber Zoo 5.4. Das 4B-VLM geht mit fehlendem Gerätezugriff vorsichtiger um und schreibt oft kohärentere Kurzgeschichten, ist aber langsamer und gewinnt nicht jede Sachaufgabe.
- Qwen3-1.7B erreicht unter den getesteten Hailo-Modellen die höchsten objektiven Punkte, hat aber eine niedrige redaktionelle Bewertung. Richtige Fakten garantieren weder ehrliche Gerätezustände noch gute kreative Antworten. Eine generierte Ausführungsbestätigung ist kein Nachweis einer ausgeführten Aktion.
- DeepSeek passt schlecht zum hier verwendeten 128-Token-Kurzantworttest: Der Denktext verbraucht oft das Budget. Die niedrige Bewertung ist keine allgemeine Bewertung unbegrenzt langer Denkaufgaben.

## Gemma4-E2B: CPU und Hailo getrennt bewertet

| Modell | Antworten | Ladungen | Laden s | TTFT DE / EN s | Decode Token/s | Datei GiB | Hailo-RAM GiB | Host-RSS GiB | Objektive Punkte | Redaktionelle Punkte | Offen |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemma-4-E2B-it | 198 | 3 | 2.74 | 1.26 / 1.25 | 8.48 | 2.41 | — | 0.46 | 108/126 | 66/72 | 0 |
| Gemma4-E2B-Instruct | 198 | 3 | 13.48 | 0.52 / 0.45 | 5.67 | 3.11 | 3.78 | 0.08 | 79.5/126 | 59.25/72 | 0 |

**CPU/LiteRT:** das ausgewogenste Ergebnis in diesem Test: 108/126 objektive und 66/72 redaktionelle Punkte bei etwa 8,48 Token/s. Erster Text nach etwa 1,26 s. Für allgemeinen Textchat auf diesem CM5 geeignet, wenn CPU-Ressourcen verfügbar sind. Kalenderfehler bleiben; es ist nicht allgemein fehlerfrei.

**Hailo/nativ:** früherer erster Text (etwa 0,52 s DE / 0,45 s EN), aber etwa 5,67 Token/s, 79,5/126 objektive und 59,25/72 redaktionelle Punkte. Mehrere Ausgaben enthalten Restmarker, Padding oder angehängtes `agma`; erkennbare richtige Antworten erhalten nach Nutzerregel 0,25 Punkte. Ob Tokenizer, Konvertierung oder Decoder die Ursache sind, wurde nicht isoliert. Vor Nutzung für exakte strukturierte Ausgaben sollten diese Artefakte untersucht werden.

Es handelt sich um unterschiedliche LiteRT- und HEF-Artefakte, nicht um ein bitgleiches Modell auf zwei Prozessoren. Der LiteRT-Export verwendet laut Modellkarte gemischte 2-/4-/8-Bit-Gewichte; eine gleiche native Quantisierung ist nicht nachgewiesen. Unterschiedliche Chat-Aufbereitung, Sampler und Rechenkerne können beitragen; ihr Einzeleffekt wurde nicht gemessen. Gleiche Seeds garantieren über Backends hinweg keine gleichen Stichproben.

[LiteRT model card](https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm)

Host-RSS nach dem Laden (etwa 0,46 GiB) ist nicht der gesamte Speicherverbrauch der CPU-Inferenz: Memory-Mapping und verzögertes Laden machen diesen Messpunkt besonders unvollständig. Hailo-RAM enthält die Geräte-Grundbelegung. Keiner der Werte ist ein Spitzenwert oder ein direkt vergleichbarer Gesamtspeicherbedarf. Stromverbrauch und CPU-Auslastung wurden nicht gemessen.

## Nutzungsempfehlungen für dieses System

- **Ausgewogener allgemeiner Textchat: Gemma4-E2B mit LiteRT auf CPU.** In diesem Katalog das beste Verhältnis von Sach-/Formatpunkten und redaktionellen Ergebnissen bei etwa 8,5 Token/s. Host-Auslastung berücksichtigen und Fakten weiterhin prüfen.
- **Sachliche/strukturierte Kurzantworten auf Hailo: Qwen3-1.7B mit Zoo 5.5 und Runtime 5.5.** Höchste objektive Hailo-Bewertung (112,5/126), etwa 4,77 Token/s. JSON validieren und erfundene Aktionen/Zustände ablehnen; 9/72 redaktionelle Punkte erlauben keine uneingeschränkte Chatempfehlung.
- **Hailo mit schneller Generierung: Qwen2.5-Coder-1.5B.** Etwa 8,33 Token/s und 98,5/126 objektive Punkte. Das ist ein Kurzantwort-/JSON-Ergebnis, kein Programmierbenchmark; redaktionell bleibt es schwach (16/72). Qwen2-1.5B ist bei ähnlichem Tempo redaktionell ausgewogener (38/72), hat aber weniger objektive Punkte (90,5/126).
- **Hailo-Chat mit besserem Umgang mit fehlenden Zugriffsmöglichkeiten: Qwen3-VL-4B erproben.** 105,5/126 objektive und 59/72 redaktionelle Punkte; etwa 2,29 Token/s und 6,95 GiB belegter Gerätespeicher. Nur sinnvoll, wenn Latenz und Speicherbedarf passen. Bildqualität wurde nicht geprüft.
- **Qwen3-VL-2B für weniger Speicher und mehr Tempo als 4B, mit strenger Absicherung.** 107/126 objektive Punkte und etwa 4,88 Token/s; 0/72 redaktionelle Punkte in diesem Katalog sprechen gegen einen ungeprüften Einsatz als Gerätesteuerungsassistent.
- **Qwen3-4B nicht allein wegen der Größe bevorzugen.** Der erfolgreiche Nachtest liefert 98/126 objektive und 58/72 redaktionelle Punkte, aber nur etwa 2,10 Token/s. Dieser Test rechtfertigt keinen generellen Wechsel von kleineren Modellen.
- **Gemma auf Hailo: zuerst Ausgabeartefakte untersuchen.** Der erste Text kommt früher als beim CPU-Export, die weitere Generierung ist aber langsamer und die Bewertung niedriger. Für aktuellen allgemeinen Textchat den CPU-Export bevorzugen; eine Energieeffizienzempfehlung ist nicht durch Messungen gedeckt.
- **Llama und DeepSeek:** Llama ist am schnellsten (~10 Token/s), aber in diesem Katalog schwach (39/126). DeepSeek wird durch die kurze Ausgabelänge eingeschränkt. Für diese Aufgaben sind beide keine Standardempfehlung.

## Methodik und Grenzen

Je vollständigem Modell: 3 Ladungen in frischen Prozessen, 33 Fragen × 2 Sprachen × 3 = 198 Anfragen mit frischem Kontext. Temperatur 0,1; Seeds 1/2/3; Ausgabelimit 128; Kontextlimit 2048 soweit konfiguriert. Keine Bilder, echten Tools oder externen Wetterdaten. Das nächste Artefakt kann im Hintergrund geladen werden; nie zwei Hailo-Modelle gleichzeitig.

Nutzerregel v1.3: erkennbare richtige Antworten mit beschädigten Ausgabe-Artefakten = 0,25 Punkte und Format 0; zusätzliche Erklärung bei ausdrücklicher Kurzantwortvorgabe = 0. Ohne diese Vorgabe ist ein richtiger Satz erlaubt. Reguläre erkannte Stopmarker werden ohne Abzug entfernt. Rohantworten bleiben unverändert. Objektive Punkte und redaktionelle Codex-Sichtung werden nicht zu einer erfundenen Gesamtgenauigkeit vermischt.

Nur drei Wiederholungen, ähnliche Fragen, nicht kontrollierte Temperatur-/Cache-/Lastbedingungen und zeitlich aufeinanderfolgende Experimente. Die Werte sind beschreibend, keine statistisch abgesicherten Ranglisten. TTFT ist der erste nichtleere Textchunk; Ausgaben werden nachtokenisiert, daher ist Token/s nicht zwingend der interne Decoder-Durchsatz. Download sowie native Imports/Geräteerzeugung sind von der Ladezeit ausgenommen.

[Bewertungsregeln](../benchmarks/catalog55/evaluation_rubric.md) · [Fragenkatalog](../benchmarks/catalog55/questions.md) · [Alle Testlaufseiten](runs/index.de.md)
