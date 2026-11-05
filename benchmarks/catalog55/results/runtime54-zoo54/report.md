# Ergebnisse des Chat-Benchmarks

Aktualisiert: 2026-11-05 10:13:03 CET.
Status: abgeschlossen. Start: 2026-11-04T19:03:16+0100.
Runtime: `HailoRT-CLI version 5.4.0`. Modellartefakte: `v5.4.0`.
Drei Wiederholungen je Modell; maximal 128 Ausgabetokens. Hintergrunddownload: aktiviert.

| Modell | Datei GiB | Hailo-RAM GiB | Host-RSS GiB | Ladungen | Antworten | Ladezeit s | TTFT DE s | TTFT EN s | Decode DE Token/s | Decode EN Token/s | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| DeepSeek-R1-Distill-Qwen-1.5B | 2.13 | 2.77 | 0.08 | 3 | 198 | 5.13 | 1.78 | 1.49 | 7.54 | 7.54 | abgeschlossen |
| Qwen2.5-Coder-1.5B-Instruct | 1.56 | 2.25 | 0.08 | 3 | 198 | 3.91 | 0.64 | 0.33 | 8.07 | 8.08 | abgeschlossen |
| Qwen2-1.5B-Instruct | 1.59 | 2.31 | 0.08 | 3 | 198 | 5.51 | 0.64 | 0.33 | 8.09 | 8.09 | abgeschlossen |
| Qwen2-VL-2B-Instruct | 3.03 | 3.80 | 0.08 | 3 | 198 | 12.80 | 0.69 | 0.35 | 6.99 | 7.03 | abgeschlossen |
| Qwen2.5-1.5B-Instruct | 2.30 | 2.94 | 0.08 | 3 | 198 | 11.56 | 0.74 | 0.38 | 7.12 | 7.12 | abgeschlossen |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 3.17 | 3.91 | 0.10 | 3 | 198 | 9.97 | 0.81 | 0.41 | 6.70 | 6.73 | abgeschlossen |
| Llama3.2-1B-Instruct | 1.31 | 1.93 | 0.07 | 3 | 198 | 3.65 | 0.68 | 0.40 | 10.00 | 9.97 | abgeschlossen |
| Qwen3-1.7B-Instruct | 2.68 | 3.48 | 0.08 | 3 | 198 | 9.38 | 1.26 | 0.64 | 4.77 | 4.76 | abgeschlossen |
| Qwen3-VL-2B-Instruct | 2.97 | 3.86 | 0.08 | 3 | 198 | 15.65 | 1.26 | 0.64 | 4.70 | 4.70 | abgeschlossen |
| gemma-4-E2B-it | 2.41 | — | 0.46 | 3 | 198 | 3.21 | 1.32 | 1.27 | 8.42 | 8.42 | abgeschlossen |

Die laufende Tabelle wird direkt aus den Einzelmessungen aktualisiert; Mittelwerte noch laufender Modelle sind vorläufig. `live_summary.csv/json` enthalten denselben aktuellen Stand. Erfolgreiche Antworten in der Leistungstabelle bedeuten technischen Erfolg. Die separate Richtigkeitsauswertung folgt weiter unten, soweit sie bereits vorliegt.

**Speicher:** Datei ist die tatsächliche Artefaktgröße, auch nach deren Löschung aus dem Testcache. Hailo-RAM ist die gesamte Gerätebelegung unmittelbar nach erfolgreichem Laden einschließlich Firmware/Linux. Host-RSS ist der residente Arbeitsspeicher des Worker-Prozesses einschließlich Runtime; beim CPU-Modell enthält er das geladene Modell. Beide RAM-Spalten zeigen Mittelwerte der vorhandenen Messungen. Es sind keine Spitzenwerte während der Inferenz. Zusätzlicher Verbrauch gegenüber dem Ausgangswert und die Zahl der RAM-Messungen stehen in `model_sizes.csv/json`. Frühere, nicht erfasste RAM-Werte und fehlgeschlagene Ladungen bleiben leer (—); sie werden nicht als null gewertet. 1 GiB = 1.073.741.824 Bytes.

Ladezeiten und Antwortmetriken sind arithmetische Mittelwerte erfolgreicher Versuche. Fehlgeschlagene Starts liefern keine gültigen Leistungswerte. TTFT ist die Zeit bis zum ersten Textchunk. Die Tokenzahlen werden mit dem jeweiligen Modelltokenizer aus der vollständigen Rohantwort ermittelt. Decode-Token/s schließen den ersten Textchunk aus; bei nur einem Chunk ist diese Metrik nicht verfügbar. `summary.csv` enthält zusätzlich Token/s einschließlich TTFT.

Bisherige Fehler anderer Konfigurationen und die separaten Hardware-Probeläufe sind nicht in diese Mittelwerte eingemischt. Der Betriebssystem-Dateicache wurde nicht geleert. Bei aktivem Vorladen können Netzwerk- und Datenträgerlast die Messungen beeinflussen.

Details: `answers.jsonl`, `loads.jsonl`, `events.jsonl`, `question_means.json`, `metadata.json` sowie native Modelllogs.

## Richtigkeit der Antworten

Automatische Referenzprüfung und gesonderte redaktionelle Sichtung durch Codex. E05: Bei einem klaren Hinweis auf fehlende Wetterdaten entfällt die Drei-Satz-Vorgabe (v1.4). Noch offene Fälle sind nicht als richtig bestätigt. Technische Generierungsfehler werden separat erfasst.

| Modell | C DE Punkte / Format | C EN Punkte / Format | Sachaufgaben DE Punkte | Sachaufgaben EN Punkte | Redaktionell geprüft | Offen |
|---|---|---|---|---|---:|---:|
| DeepSeek-R1-Distill-Qwen-1.5B | 0/18 / 0/18 | 0.25/18 / 0/18 | 6/63 | 4.25/63 | 72 | 0 |
| Qwen2.5-Coder-1.5B-Instruct | 15.0/18 / 15/18 | 18.0/18 / 18/18 | 48.5/63 | 50/63 | 72 | 0 |
| Qwen2-1.5B-Instruct | 12.0/18 / 12/18 | 15.0/18 / 15/18 | 45.5/63 | 45/63 | 72 | 0 |
| Qwen2-VL-2B-Instruct | 6.0/18 / 6/18 | 12.0/18 / 12/18 | 31.5/63 | 33/63 | 72 | 0 |
| Qwen2.5-1.5B-Instruct | 11.0/18 / 11/18 | 8.0/18 / 8/18 | 36.5/63 | 36/63 | 72 | 0 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 11.0/18 / 11/18 | 6.0/18 / 6/18 | 35.5/63 | 27.5/63 | 72 | 0 |
| Llama3.2-1B-Instruct | 4.0/18 / 4/18 | 9.0/18 / 9/18 | 13/63 | 26/63 | 72 | 0 |
| Qwen3-1.7B-Instruct | 15.0/18 / 15/18 | 18.0/18 / 18/18 | 55.5/63 | 57/63 | 72 | 0 |
| Qwen3-VL-2B-Instruct | 13.0/18 / 13/18 | 15.0/18 / 15/18 | 38/63 | 39/63 | 72 | 0 |
| gemma-4-E2B-it | 18.0/18 / 18/18 | 18.0/18 / 18/18 | 51/63 | 57/63 | 72 | 0 |

C: sechs kontrollierte Aufgaben je Sprache und Durchlauf. Ausgabevorgaben gehen in die Punkte ein: erkennbare richtige Antwort mit Ausgabeartefakten 0,25 Punkte und Format 0; zusätzliche Erklärung bei ausdrücklich verlangter Kurzantwort 0 Punkte. Ohne Einschränkung sind Erklärungen zulässig. Bekannte reguläre Stopmarkierungen werden weiterhin entfernt. Sachaufgaben: 21 objektive Aufgaben pro Sprache und Durchlauf; La Paz allein erhält 0,5 Punkte, Kalenderdatum und Wochentag jeweils 0,5. Kreativtexte, Wetterantworten und Aussagen über nicht ausgeführte Geräteaktionen werden redaktionell nach dokumentierten Kriterien geprüft und nicht in die objektive Trefferquote gemischt. Einzelurteile und Begründungen stehen in `answer_checks.jsonl`; offene Antworten in `review_queue.json`.
