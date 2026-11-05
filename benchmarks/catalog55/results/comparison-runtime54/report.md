# Vergleich Model Zoo 5.4 und 5.5 auf HailoRT 5.4

Erstellt: 2026-11-05T09:22:59.518941+01:00. Beide technischen Läufe sind abgeschlossen und separat archiviert. Dieser Bericht ergänzt die Archive, ohne sie zu verändern.

## Geschwindigkeit und Laden

Mittelwerte von jeweils 198 Antworten und drei Ladungen. Positive Änderung bei Token/s bedeutet schneller mit Zoo 5.5; negative Änderung bei Ladezeit bedeutet kürzer.

| Modell | Token/s 5.4 | Token/s 5.5 | Änderung | Laden 5.4 s | Laden 5.5 s | Änderung |
|---|---:|---:|---:|---:|---:|---:|
| DeepSeek-R1-Distill-Qwen-1.5B | 7.54 | 7.43 | -1.4 % | 5.13 | 5.36 | +4.6 % |
| Qwen2.5-Coder-1.5B-Instruct | 8.07 | 8.05 | -0.3 % | 3.91 | 3.92 | +0.3 % |
| Qwen2-1.5B-Instruct | 8.09 | 8.07 | -0.3 % | 5.51 | 4.12 | -25.3 % |
| Qwen2-VL-2B-Instruct | 7.01 | 7.55 | +7.8 % | 12.80 | 12.31 | -3.9 % |
| Qwen2.5-1.5B-Instruct | 7.12 | 7.16 | +0.7 % | 11.56 | 8.77 | -24.1 % |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 6.72 | 6.77 | +0.8 % | 9.97 | 6.72 | -32.6 % |
| Llama3.2-1B-Instruct | 9.98 | 9.90 | -0.8 % | 3.65 | 3.61 | -1.2 % |
| Qwen3-1.7B-Instruct | 4.77 | 4.71 | -1.2 % | 9.38 | 7.99 | -14.9 % |
| Qwen3-VL-2B-Instruct | 4.70 | 4.81 | +2.3 % | 15.65 | 16.03 | +2.5 % |
| gemma-4-E2B-it | 8.42 | 8.36 | -0.7 % | 3.21 | 2.92 | -9.1 % |

## Speicher

Gesamte Hailo-Belegung unmittelbar nach Laden; keine Inferenzspitzen. GiB = 2^30 Bytes. CPU-RSS ist ebenfalls nur der Messpunkt nach dem Laden. Delta gegenüber Ausgangsbelegung steht zusätzlich in comparison.json.

| Modell | Datei GiB 5.4 → 5.5 | Hailo-RAM GiB 5.4 → 5.5 |
|---|---:|---:|
| DeepSeek-R1-Distill-Qwen-1.5B | 2.13 → 2.10 | 2.77 → 2.62 |
| Qwen2.5-Coder-1.5B-Instruct | 1.56 → 1.55 | 2.25 → 2.13 |
| Qwen2-1.5B-Instruct | 1.59 → 1.54 | 2.31 → 2.11 |
| Qwen2-VL-2B-Instruct | 3.03 → 2.91 | 3.80 → 3.59 |
| Qwen2.5-1.5B-Instruct | 2.30 → 2.32 | 2.94 → 2.90 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 3.17 → 2.43 | 3.91 → 3.10 |
| Llama3.2-1B-Instruct | 1.31 → 1.26 | 1.93 → 1.82 |
| Qwen3-1.7B-Instruct | 2.68 → 2.75 | 3.48 → 3.52 |
| Qwen3-VL-2B-Instruct | 2.97 → 2.97 | 3.86 → 3.85 |
| gemma-4-E2B-it | 2.41 → 2.41 | — → — |

## Antwortqualität

Der direkte Vergleich verwendet ausschließlich dieselben objektiven Aufgaben, die in beiden Läufen bereits bewertet sind. Dadurch verzerren offene Fälle nicht den Nenner. Punkte enthalten Teilgutschriften. Identische Rohantworten beziehen sich auf gleiche Frage, Sprache und Wiederholung.

| Modell | Gemeinsame Aufgaben | Punkte 5.4 | Punkte 5.5 | Gleiche Rohantworten /198 | Offene Prüfungen 5.4 / 5.5 |
|---|---:|---:|---:|---:|---:|
| DeepSeek-R1-Distill-Qwen-1.5B | 126 | 10.25 | 10.25 | 198 | 0 / 0 |
| Qwen2.5-Coder-1.5B-Instruct | 126 | 98.5 | 98.5 | 198 | 0 / 0 |
| Qwen2-1.5B-Instruct | 126 | 90.5 | 90.5 | 198 | 0 / 0 |
| Qwen2-VL-2B-Instruct | 126 | 64.5 | 84 | 45 | 0 / 0 |
| Qwen2.5-1.5B-Instruct | 126 | 72.5 | 72.5 | 198 | 0 / 0 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 126 | 63 | 68.5 | 75 | 0 / 0 |
| Llama3.2-1B-Instruct | 126 | 39 | 39 | 198 | 0 / 0 |
| Qwen3-1.7B-Instruct | 126 | 112.5 | 112.5 | 198 | 0 / 0 |
| Qwen3-VL-2B-Instruct | 126 | 77 | 107 | 51 | 0 / 0 |
| gemma-4-E2B-it | 126 | 108 | 108 | 198 | 0 / 0 |

## Einordnung

Der stärkste Geschwindigkeitsgewinn liegt bei Qwen2-VL-2B: rund 8 % mehr Decode-Token/s und rund 19 % kürzere TTFT in beiden Sprachen. Zugleich steigen die objektiven Punkte gemäß der aktuellen Bewertung (siehe Punktetabelle). Qwen3-VL-2B verbessert seine objektiven Punkte deutlich (siehe Punktetabelle), während der Durchsatz nur rund 2 % steigt; die Ladezeit steigt leicht. Beide Ergebnisse betreffen Textchat, nicht Bildverstehen.

Die Function-Calling-Variante benötigt mit Zoo 5.5 erheblich weniger Datei- und Gerätespeicher und lädt schneller. Die objektiven Aufgaben verbessern sich im gemeinsamen bewerteten Teil. Das ist kein Nachweis zuverlässiger Werkzeugaufrufe: Es wurden keine echten Tool-Schemata und Geräteaktionen getestet, und redaktionelle Prüfungen sind teilweise offen.

Bei DeepSeek, Coder, Qwen2, Qwen2.5, Llama und Qwen3 bleiben die objektiven Punktzahlen gleich. Geschwindigkeit ändert sich meist um weniger als 2 %. Diese kleinen Abweichungen werden angesichts der CPU-Referenz und fehlender randomisierter Laufreihenfolge nicht als belastbare Verbesserungen gewertet. Qwen2 und Qwen2.5 laden mit Zoo 5.5 deutlich schneller.

Die Gemma4-CPU-Referenz verwendet in beiden Durchgängen dasselbe Artefakt und ist kein Zoo-Versionsvergleich. Ihre Schwankungen liefern einen Hinweis auf Messvariabilität: rund 1 % beim Durchsatz und rund 9 % bei der Ladezeit. Bei sechs gemeinsamen Hailo-Modellen und der CPU-Referenz sind sämtliche 198 Rohantworten je Modell sogar wortgleich. Unterschiede bestehen bei Qwen2-VL, Qwen3-VL und Function-Calling. Bei der CPU-Referenz liegen die einzelnen Ladezeiten zwischen etwa 0,41 und 8,80 Sekunden; der Mittelwert verdeckt hier starke Cache-/Initialisierungseffekte.

Drei neue Zoo-5.5-Hailo-Modelle (Qwen3-4B, Qwen3-VL-4B, Gemma4-E2B) scheiterten beim Laden. Sie besitzen keine Zoo-5.4-Vergleichszeile und werden nicht in Qualitäts- oder Geschwindigkeitsranglisten eingerechnet.

## Grenzen und Reproduzierbarkeit

Beide Läufe nutzen HailoRT/Firmware 5.4.0, denselben Fragen-Hash, drei Wiederholungen, Temperatur 0,1, 128 Ausgabetokens und neuen Kontext je Frage. Diese Metadaten wurden automatisch auf Übereinstimmung geprüft. Unterschiede können Modellgewichte, Kompilierung und Artefaktkonfiguration betreffen; die Ursache ist aus diesen Messungen nicht isolierbar.

Die Modelle wurden zeitlich nacheinander und nicht in zufällig wechselnder Reihenfolge getestet. Dateicache wurde nicht geleert; Hintergrunddownloads können Last erzeugen. Ladezeiten sind deshalb keine kontrollierten Kaltstarts. Drei Wiederholungen und ähnliche Fragen erlauben keine abgesicherte allgemeine Rangfolge. TTFT ist der erste Textchunk; Token/s basieren auf nachträglicher Tokenisierung. DeepSeek wird durch das kurze Ausgabelimit stark eingeschränkt.

Die Referenzprüfung verwendet die Nutzerregel v1.3: erkennbar richtige Antworten mit Ausgabeartefakten erhalten 0,25 Punkte und Format 0. Zusätzliche Erklärung bei ausdrücklich verlangter Kurzantwort ergibt 0 Punkte; ohne Einschränkung bleibt eine richtige Erklärung zulässig. Der semantische Abgleich bleibt separat gespeichert. Die alten Bewertungen bleiben in evaluation_history und den ursprünglichen Archiven erhalten. Deshalb ändern sich einige absolute Punktzahlen gegenüber früheren Statusmeldungen. Die automatische Referenzprüfung ist regelbasiert; offene und redaktionelle Fälle sind nicht automatisch richtig. Ein vollständiger semantischer Qualitätsvergleich steht für Teile der VLM-, Function-Calling- und CPU-Antworten noch aus. Ausgewählte Antwortänderungen stehen unverändert in changed_objective_answers.json. Originalquellen sind über SHA256 in provenance.json referenziert. Nach einem HailoRT-5.5-Upgrade müssen beide Katalogversionen erneut getestet werden.
