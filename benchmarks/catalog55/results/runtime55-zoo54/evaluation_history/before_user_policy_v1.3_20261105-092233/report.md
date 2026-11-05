# Ergebnisse des Chat-Benchmarks

Aktualisiert: 2026-11-05 09:10:36 CET.
Status: abgeschlossen. Start: 2026-11-05T04:34:02+0100.
Runtime: `HailoRT-CLI version 5.5.0`. Modellartefakte: `v5.4.0`.
Drei Wiederholungen je Modell; maximal 128 Ausgabetokens. Hintergrunddownload: aktiviert.

| Modell | Datei GiB | Hailo-RAM GiB | Host-RSS GiB | Ladungen | Antworten | Ladezeit s | TTFT DE s | TTFT EN s | Decode DE Token/s | Decode EN Token/s | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| DeepSeek-R1-Distill-Qwen-1.5B | 2.13 | 2.69 | 0.07 | 3 | 198 | 4.97 | 1.75 | 1.47 | 7.83 | 7.84 | abgeschlossen |
| Qwen2.5-Coder-1.5B-Instruct | 1.56 | 2.18 | 0.07 | 3 | 198 | 3.78 | 0.63 | 0.32 | 8.29 | 8.30 | abgeschlossen |
| Qwen2-1.5B-Instruct | 1.59 | 2.21 | 0.07 | 3 | 198 | 3.83 | 0.63 | 0.32 | 8.32 | 8.33 | abgeschlossen |
| Qwen2-VL-2B-Instruct | 3.03 | 3.73 | 0.08 | 3 | 198 | 8.27 | 0.68 | 0.35 | 7.18 | 7.22 | abgeschlossen |
| Qwen2.5-1.5B-Instruct | 2.30 | 2.88 | 0.07 | 3 | 198 | 5.18 | 0.73 | 0.37 | 7.37 | 7.37 | abgeschlossen |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 3.17 | 3.83 | 0.09 | 3 | 198 | 8.05 | 0.79 | 0.40 | 6.85 | 6.88 | abgeschlossen |
| Llama3.2-1B-Instruct | 1.31 | 1.86 | 0.07 | 3 | 198 | 3.62 | 0.68 | 0.39 | 10.12 | 10.10 | abgeschlossen |
| Qwen3-1.7B-Instruct | 2.68 | 3.37 | 0.08 | 3 | 198 | 6.85 | 1.25 | 0.63 | 4.85 | 4.84 | abgeschlossen |
| Qwen3-VL-2B-Instruct | 2.97 | 3.79 | 0.08 | 3 | 198 | 8.05 | 1.25 | 0.63 | 4.77 | 4.77 | abgeschlossen |
| gemma-4-E2B-it | 2.41 | — | 0.46 | 3 | 198 | 2.61 | 1.28 | 1.27 | 8.29 | 8.46 | abgeschlossen |

Die laufende Tabelle wird direkt aus den Einzelmessungen aktualisiert; Mittelwerte noch laufender Modelle sind vorläufig. `live_summary.csv/json` enthalten denselben aktuellen Stand. Erfolgreiche Antworten in der Leistungstabelle bedeuten technischen Erfolg. Die separate Richtigkeitsauswertung folgt weiter unten, soweit sie bereits vorliegt.

**Speicher:** Datei ist die tatsächliche Artefaktgröße, auch nach deren Löschung aus dem Testcache. Hailo-RAM ist die gesamte Gerätebelegung unmittelbar nach erfolgreichem Laden einschließlich Firmware/Linux. Host-RSS ist der residente Arbeitsspeicher des Worker-Prozesses einschließlich Runtime; beim CPU-Modell enthält er das geladene Modell. Beide RAM-Spalten zeigen Mittelwerte der vorhandenen Messungen. Es sind keine Spitzenwerte während der Inferenz. Zusätzlicher Verbrauch gegenüber dem Ausgangswert und die Zahl der RAM-Messungen stehen in `model_sizes.csv/json`. Frühere, nicht erfasste RAM-Werte und fehlgeschlagene Ladungen bleiben leer (—); sie werden nicht als null gewertet. 1 GiB = 1.073.741.824 Bytes.

Ladezeiten und Antwortmetriken sind arithmetische Mittelwerte erfolgreicher Versuche. Fehlgeschlagene Starts liefern keine gültigen Leistungswerte. TTFT ist die Zeit bis zum ersten Textchunk. Die Tokenzahlen werden mit dem jeweiligen Modelltokenizer aus der vollständigen Rohantwort ermittelt. Decode-Token/s schließen den ersten Textchunk aus; bei nur einem Chunk ist diese Metrik nicht verfügbar. `summary.csv` enthält zusätzlich Token/s einschließlich TTFT.

Bisherige Fehler anderer Konfigurationen und die separaten Hardware-Probeläufe sind nicht in diese Mittelwerte eingemischt. Der Betriebssystem-Dateicache wurde nicht geleert. Bei aktivem Vorladen können Netzwerk- und Datenträgerlast die Messungen beeinflussen.

Details: `answers.jsonl`, `loads.jsonl`, `events.jsonl`, `question_means.json`, `metadata.json` sowie native Modelllogs.

## Richtigkeit der Antworten

Automatische Referenzprüfung und gesonderte redaktionelle Sichtung durch Codex. Noch offene Fälle sind nicht als richtig bestätigt. Technische Generierungsfehler werden separat erfasst.

| Modell | C DE Inhalt / Format | C EN Inhalt / Format | Sachaufgaben DE Punkte | Sachaufgaben EN Punkte | Redaktionell geprüft | Offen |
|---|---|---|---|---|---:|---:|
| DeepSeek-R1-Distill-Qwen-1.5B | 2/18 / 0/18 | 3/18 / 0/18 | 9/63 | 7/63 | 72 | 0 |
| Qwen2.5-Coder-1.5B-Instruct | 15/18 / 15/18 | 18/18 / 18/18 | 51.5/63 | 56/63 | 72 | 0 |
| Qwen2-1.5B-Instruct | 12/18 / 12/18 | 15/18 / 15/18 | 49.5/63 | 54/63 | 72 | 0 |
| Qwen2-VL-2B-Instruct | 9/18 / 6/18 | 15/18 / 12/18 | 43.5/63 | 51/63 | 72 | 0 |
| Qwen2.5-1.5B-Instruct | 12/18 / 11/18 | 11/18 / 8/18 | 37.5/63 | 41/63 | 72 | 0 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 11/18 / 11/18 | 6/18 / 6/18 | 35.5/63 | 27.5/63 | 72 | 0 |
| Llama3.2-1B-Instruct | 6/18 / 4/18 | 9/18 / 9/18 | 30/63 | 33/63 | 72 | 0 |
| Qwen3-1.7B-Instruct | 18/18 / 15/18 | 18/18 / 18/18 | 58.5/63 | 57/63 | 72 | 0 |
| Qwen3-VL-2B-Instruct | 15/18 / 13/18 | 15/18 / 15/18 | 41/63 | 45/63 | 72 | 0 |
| gemma-4-E2B-it | 18/18 / 18/18 | 18/18 / 18/18 | 57/63 | 63/63 | 72 | 0 |

C: sechs kontrollierte Aufgaben je Sprache und Durchlauf. Inhalt und Format werden separat bewertet. Sachaufgaben: 21 objektive Aufgaben pro Sprache und Durchlauf; La Paz allein erhält 0,5 Punkte, Kalenderdatum und Wochentag jeweils 0,5. Kreativtexte, Wetterantworten und Aussagen über nicht ausgeführte Geräteaktionen werden redaktionell nach dokumentierten Kriterien geprüft und nicht in die objektive Trefferquote gemischt. Einzelurteile und Begründungen stehen in `answer_checks.jsonl`; offene Antworten in `review_queue.json`.
