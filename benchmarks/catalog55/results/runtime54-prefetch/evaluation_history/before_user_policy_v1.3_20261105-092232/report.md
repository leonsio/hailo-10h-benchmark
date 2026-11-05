# Ergebnisse des Chat-Benchmarks

Aktualisiert: 2026-11-05 09:10:36 CET.
Status: abgeschlossen. Start: 2026-11-04T14:57:48+0100.
Runtime: `HailoRT-CLI version 5.4.0`. Modellartefakte: `v5.5.0`.
Drei Wiederholungen je Modell; maximal 128 Ausgabetokens. Hintergrunddownload: aktiviert.

| Modell | Datei GiB | Hailo-RAM GiB | Host-RSS GiB | Ladungen | Antworten | Ladezeit s | TTFT DE s | TTFT EN s | Decode DE Token/s | Decode EN Token/s | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Qwen3-4B-Instruct-2507 | 5.27 | — | — | 0 | 0 | — | — | — | — | — | HAILO_RESOURCE_EXHAUSTED(81) |
| Gemma4-E2B-Instruct | 3.11 | — | — | 0 | 0 | — | — | — | — | — | HAILO_TIMEOUT(4) |
| Qwen3-VL-4B-Instruct | 6.08 | — | — | 0 | 0 | — | — | — | — | — | HAILO_RESOURCE_EXHAUSTED(81) |
| DeepSeek-R1-Distill-Qwen-1.5B | 2.10 | 2.62 | 0.08 | 3 | 198 | 5.36 | 1.78 | 1.49 | 7.43 | 7.43 | abgeschlossen |
| Qwen2.5-Coder-1.5B-Instruct | 1.55 | 2.13 | 0.07 | 3 | 198 | 3.92 | 0.64 | 0.33 | 8.05 | 8.05 | abgeschlossen |
| Qwen2-1.5B-Instruct | 1.54 | 2.11 | 0.08 | 3 | 198 | 4.12 | 0.64 | 0.33 | 8.06 | 8.07 | abgeschlossen |
| Qwen2-VL-2B-Instruct | 2.91 | 3.59 | 0.08 | 3 | 198 | 12.31 | 0.56 | 0.28 | 7.56 | 7.55 | abgeschlossen |
| Qwen2.5-1.5B-Instruct | 2.32 | 2.90 | 0.08 | 3 | 198 | 8.77 | 0.74 | 0.38 | 7.16 | 7.16 | abgeschlossen |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 2.43 | 3.10 | 0.10 | 3 | 198 | 6.72 | 0.81 | 0.41 | 6.77 | 6.78 | abgeschlossen |
| Llama3.2-1B-Instruct | 1.26 | 1.82 | 0.07 | 3 | 198 | 3.61 | 0.68 | 0.40 | 9.91 | 9.89 | abgeschlossen |
| Qwen3-1.7B-Instruct | 2.75 | 3.52 | 0.08 | 3 | 198 | 7.99 | 1.26 | 0.64 | 4.71 | 4.70 | abgeschlossen |
| Qwen3-VL-2B-Instruct | 2.97 | 3.85 | 0.08 | 3 | 198 | 16.03 | 1.27 | 0.64 | 4.81 | 4.80 | abgeschlossen |
| gemma-4-E2B-it | 2.41 | — | 0.46 | 3 | 198 | 2.92 | 1.30 | 1.27 | 8.29 | 8.43 | abgeschlossen |

Die laufende Tabelle wird direkt aus den Einzelmessungen aktualisiert; Mittelwerte noch laufender Modelle sind vorläufig. `live_summary.csv/json` enthalten denselben aktuellen Stand. Erfolgreiche Antworten in der Leistungstabelle bedeuten technischen Erfolg. Die separate Richtigkeitsauswertung folgt weiter unten, soweit sie bereits vorliegt.

**Speicher:** Datei ist die tatsächliche Artefaktgröße, auch nach deren Löschung aus dem Testcache. Hailo-RAM ist die gesamte Gerätebelegung unmittelbar nach erfolgreichem Laden einschließlich Firmware/Linux. Host-RSS ist der residente Arbeitsspeicher des Worker-Prozesses einschließlich Runtime; beim CPU-Modell enthält er das geladene Modell. Beide RAM-Spalten zeigen Mittelwerte der vorhandenen Messungen. Es sind keine Spitzenwerte während der Inferenz. Zusätzlicher Verbrauch gegenüber dem Ausgangswert und die Zahl der RAM-Messungen stehen in `model_sizes.csv/json`. Frühere, nicht erfasste RAM-Werte und fehlgeschlagene Ladungen bleiben leer (—); sie werden nicht als null gewertet. 1 GiB = 1.073.741.824 Bytes.

Ladezeiten und Antwortmetriken sind arithmetische Mittelwerte erfolgreicher Versuche. Fehlgeschlagene Starts liefern keine gültigen Leistungswerte. TTFT ist die Zeit bis zum ersten Textchunk. Die Tokenzahlen werden mit dem jeweiligen Modelltokenizer aus der vollständigen Rohantwort ermittelt. Decode-Token/s schließen den ersten Textchunk aus; bei nur einem Chunk ist diese Metrik nicht verfügbar. `summary.csv` enthält zusätzlich Token/s einschließlich TTFT.

Bisherige Fehler anderer Konfigurationen und die separaten Hardware-Probeläufe sind nicht in diese Mittelwerte eingemischt. Der Betriebssystem-Dateicache wurde nicht geleert. Bei aktivem Vorladen können Netzwerk- und Datenträgerlast die Messungen beeinflussen.

Details: `answers.jsonl`, `loads.jsonl`, `events.jsonl`, `question_means.json`, `metadata.json` sowie native Modelllogs.

## Richtigkeit der Antworten

Automatische Referenzprüfung und gesonderte redaktionelle Sichtung durch Codex. Noch offene Fälle sind nicht als richtig bestätigt. Technische Generierungsfehler werden separat erfasst.

| Modell | C DE Inhalt / Format | C EN Inhalt / Format | Sachaufgaben DE Punkte | Sachaufgaben EN Punkte | Redaktionell geprüft | Offen |
|---|---|---|---|---|---:|---:|
| Qwen3-4B-Instruct-2507 | — | — | — | — | 0 | 0 |
| Gemma4-E2B-Instruct | — | — | — | — | 0 | 0 |
| Qwen3-VL-4B-Instruct | — | — | — | — | 0 | 0 |
| DeepSeek-R1-Distill-Qwen-1.5B | 2/18 / 0/18 | 3/18 / 0/18 | 9/63 | 7/63 | 72 | 0 |
| Qwen2.5-Coder-1.5B-Instruct | 15/18 / 15/18 | 18/18 / 18/18 | 51.5/63 | 56/63 | 72 | 0 |
| Qwen2-1.5B-Instruct | 12/18 / 12/18 | 15/18 / 15/18 | 49.5/63 | 54/63 | 72 | 0 |
| Qwen2-VL-2B-Instruct | 12/18 / 12/18 | 15/18 / 15/18 | 48/63 | 51/63 | 72 | 0 |
| Qwen2.5-1.5B-Instruct | 12/18 / 11/18 | 11/18 / 8/18 | 37.5/63 | 41/63 | 72 | 0 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 11/18 / 11/18 | 8/18 / 8/18 | 41.5/63 | 30/63 | 72 | 0 |
| Llama3.2-1B-Instruct | 6/18 / 4/18 | 9/18 / 9/18 | 30/63 | 33/63 | 72 | 0 |
| Qwen3-1.7B-Instruct | 18/18 / 15/18 | 18/18 / 18/18 | 58.5/63 | 57/63 | 72 | 0 |
| Qwen3-VL-2B-Instruct | 18/18 / 15/18 | 18/18 / 18/18 | 53/63 | 57/63 | 72 | 0 |
| gemma-4-E2B-it | 18/18 / 18/18 | 18/18 / 18/18 | 57/63 | 63/63 | 72 | 0 |

C: sechs kontrollierte Aufgaben je Sprache und Durchlauf. Inhalt und Format werden separat bewertet. Sachaufgaben: 21 objektive Aufgaben pro Sprache und Durchlauf; La Paz allein erhält 0,5 Punkte, Kalenderdatum und Wochentag jeweils 0,5. Kreativtexte, Wetterantworten und Aussagen über nicht ausgeführte Geräteaktionen werden redaktionell nach dokumentierten Kriterien geprüft und nicht in die objektive Trefferquote gemischt. Einzelurteile und Begründungen stehen in `answer_checks.jsonl`; offene Antworten in `review_queue.json`.
