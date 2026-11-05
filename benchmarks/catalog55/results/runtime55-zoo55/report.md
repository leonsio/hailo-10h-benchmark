# Ergebnisse des Chat-Benchmarks

Aktualisiert: 2026-11-05 10:13:03 CET.
Status: abgeschlossen. Start: 2026-11-05T00:14:57+0100.
Runtime: `HailoRT-CLI version 5.5.0`. Modellartefakte: `v5.5.0`.
Drei Wiederholungen je Modell; maximal 128 Ausgabetokens. Hintergrunddownload: aktiviert.
Qwen3-4B ist in diesen Lauf integriert (3 Ladungen, 198 Antworten); seine Messungen erfolgten später ohne Hintergrunddownload. Herkunft und ursprünglicher Downloadfehler: `provenance/`.

| Modell | Datei GiB | Hailo-RAM GiB | Host-RSS GiB | Ladungen | Antworten | Ladezeit s | TTFT DE s | TTFT EN s | Decode DE Token/s | Decode EN Token/s | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Qwen3-4B-Instruct-2507 | 5.27 | 6.13 | 0.12 | 3 | 198 | 18.85 | 3.08 | 1.55 | 2.10 | 2.10 | abgeschlossen |
| Gemma4-E2B-Instruct | 3.11 | 3.78 | 0.08 | 3 | 198 | 13.48 | 0.52 | 0.45 | 5.68 | 5.66 | abgeschlossen |
| Qwen3-VL-4B-Instruct | 6.08 | 6.95 | 0.12 | 3 | 198 | 22.87 | 3.28 | 1.65 | 2.29 | 2.29 | abgeschlossen |
| DeepSeek-R1-Distill-Qwen-1.5B | 2.10 | 2.49 | 0.07 | 3 | 198 | 5.72 | 1.74 | 1.46 | 7.70 | 7.70 | abgeschlossen |
| Qwen2.5-Coder-1.5B-Instruct | 1.55 | 2.02 | 0.07 | 3 | 198 | 3.84 | 0.63 | 0.32 | 8.32 | 8.33 | abgeschlossen |
| Qwen2-1.5B-Instruct | 1.54 | 2.02 | 0.07 | 3 | 198 | 3.94 | 0.63 | 0.32 | 8.31 | 8.32 | abgeschlossen |
| Qwen2-VL-2B-Instruct | 2.91 | 3.50 | 0.08 | 3 | 198 | 8.10 | 0.55 | 0.28 | 7.75 | 7.75 | abgeschlossen |
| Qwen2.5-1.5B-Instruct | 2.32 | 2.81 | 0.07 | 3 | 198 | 5.22 | 0.73 | 0.37 | 7.40 | 7.40 | abgeschlossen |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 2.43 | 3.02 | 0.09 | 3 | 198 | 6.56 | 0.80 | 0.40 | 7.01 | 7.02 | abgeschlossen |
| Llama3.2-1B-Instruct | 1.26 | 1.74 | 0.07 | 3 | 198 | 3.60 | 0.67 | 0.39 | 10.10 | 10.08 | abgeschlossen |
| Qwen3-1.7B-Instruct | 2.75 | 3.40 | 0.08 | 3 | 198 | 7.02 | 1.25 | 0.63 | 4.77 | 4.76 | abgeschlossen |
| Qwen3-VL-2B-Instruct | 2.97 | 3.75 | 0.08 | 3 | 198 | 7.96 | 1.26 | 0.64 | 4.88 | 4.88 | abgeschlossen |
| gemma-4-E2B-it | 2.41 | — | 0.46 | 3 | 198 | 2.74 | 1.26 | 1.25 | 8.46 | 8.50 | abgeschlossen |

Die laufende Tabelle wird direkt aus den Einzelmessungen aktualisiert; Mittelwerte noch laufender Modelle sind vorläufig. `live_summary.csv/json` enthalten denselben aktuellen Stand. Erfolgreiche Antworten in der Leistungstabelle bedeuten technischen Erfolg. Die separate Richtigkeitsauswertung folgt weiter unten, soweit sie bereits vorliegt.

**Speicher:** Datei ist die tatsächliche Artefaktgröße, auch nach deren Löschung aus dem Testcache. Hailo-RAM ist die gesamte Gerätebelegung unmittelbar nach erfolgreichem Laden einschließlich Firmware/Linux. Host-RSS ist der residente Arbeitsspeicher des Worker-Prozesses einschließlich Runtime; beim CPU-Modell enthält er das geladene Modell. Beide RAM-Spalten zeigen Mittelwerte der vorhandenen Messungen. Es sind keine Spitzenwerte während der Inferenz. Zusätzlicher Verbrauch gegenüber dem Ausgangswert und die Zahl der RAM-Messungen stehen in `model_sizes.csv/json`. Frühere, nicht erfasste RAM-Werte und fehlgeschlagene Ladungen bleiben leer (—); sie werden nicht als null gewertet. 1 GiB = 1.073.741.824 Bytes.

Ladezeiten und Antwortmetriken sind arithmetische Mittelwerte erfolgreicher Versuche. Fehlgeschlagene Starts liefern keine gültigen Leistungswerte. TTFT ist die Zeit bis zum ersten Textchunk. Die Tokenzahlen werden mit dem jeweiligen Modelltokenizer aus der vollständigen Rohantwort ermittelt. Decode-Token/s schließen den ersten Textchunk aus; bei nur einem Chunk ist diese Metrik nicht verfügbar. `summary.csv` enthält zusätzlich Token/s einschließlich TTFT.

Bisherige Fehler anderer Konfigurationen und die separaten Hardware-Probeläufe sind nicht in diese Mittelwerte eingemischt. Der Betriebssystem-Dateicache wurde nicht geleert. Bei aktivem Vorladen können Netzwerk- und Datenträgerlast die Messungen beeinflussen.

Details: `answers.jsonl`, `loads.jsonl`, `events.jsonl`, `question_means.json`, `metadata.json` sowie native Modelllogs.

## Richtigkeit der Antworten

Automatische Referenzprüfung und gesonderte redaktionelle Sichtung durch Codex. E05: Bei einem klaren Hinweis auf fehlende Wetterdaten entfällt die Drei-Satz-Vorgabe (v1.4). Noch offene Fälle sind nicht als richtig bestätigt. Technische Generierungsfehler werden separat erfasst.

| Modell | C DE Punkte / Format | C EN Punkte / Format | Sachaufgaben DE Punkte | Sachaufgaben EN Punkte | Redaktionell geprüft | Offen |
|---|---|---|---|---|---:|---:|
| Qwen3-4B-Instruct-2507 | 15.0/18 / 15/18 | 18.0/18 / 18/18 | 48/63 | 50/63 | 72 | 0 |
| Gemma4-E2B-Instruct | 15.75/18 / 15/18 | 15.75/18 / 15/18 | 34.5/63 | 45/63 | 72 | 0 |
| Qwen3-VL-4B-Instruct | 18.0/18 / 18/18 | 18.0/18 / 18/18 | 54/63 | 51.5/63 | 72 | 0 |
| DeepSeek-R1-Distill-Qwen-1.5B | 0/18 / 0/18 | 0.25/18 / 0/18 | 6/63 | 4.25/63 | 72 | 0 |
| Qwen2.5-Coder-1.5B-Instruct | 15.0/18 / 15/18 | 18.0/18 / 18/18 | 48.5/63 | 50/63 | 72 | 0 |
| Qwen2-1.5B-Instruct | 12.0/18 / 12/18 | 15.0/18 / 15/18 | 45.5/63 | 45/63 | 72 | 0 |
| Qwen2-VL-2B-Instruct | 12.0/18 / 12/18 | 15.0/18 / 15/18 | 42/63 | 42/63 | 72 | 0 |
| Qwen2.5-1.5B-Instruct | 11.0/18 / 11/18 | 8.0/18 / 8/18 | 36.5/63 | 36/63 | 72 | 0 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 11.0/18 / 11/18 | 8.0/18 / 8/18 | 38.5/63 | 30/63 | 72 | 0 |
| Llama3.2-1B-Instruct | 4.0/18 / 4/18 | 9.0/18 / 9/18 | 13/63 | 26/63 | 72 | 0 |
| Qwen3-1.7B-Instruct | 15.0/18 / 15/18 | 18.0/18 / 18/18 | 55.5/63 | 57/63 | 72 | 0 |
| Qwen3-VL-2B-Instruct | 15.0/18 / 15/18 | 18.0/18 / 18/18 | 50/63 | 57/63 | 72 | 0 |
| gemma-4-E2B-it | 18.0/18 / 18/18 | 18.0/18 / 18/18 | 51/63 | 57/63 | 72 | 0 |

C: sechs kontrollierte Aufgaben je Sprache und Durchlauf. Ausgabevorgaben gehen in die Punkte ein: erkennbare richtige Antwort mit Ausgabeartefakten 0,25 Punkte und Format 0; zusätzliche Erklärung bei ausdrücklich verlangter Kurzantwort 0 Punkte. Ohne Einschränkung sind Erklärungen zulässig. Bekannte reguläre Stopmarkierungen werden weiterhin entfernt. Sachaufgaben: 21 objektive Aufgaben pro Sprache und Durchlauf; La Paz allein erhält 0,5 Punkte, Kalenderdatum und Wochentag jeweils 0,5. Kreativtexte, Wetterantworten und Aussagen über nicht ausgeführte Geräteaktionen werden redaktionell nach dokumentierten Kriterien geprüft und nicht in die objektive Trefferquote gemischt. Einzelurteile und Begründungen stehen in `answer_checks.jsonl`; offene Antworten in `review_queue.json`.
