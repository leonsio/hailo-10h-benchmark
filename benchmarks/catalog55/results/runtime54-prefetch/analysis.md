> Historischer Analysebericht: Die Punkte wurden inzwischen nach Nutzerregel v1.3 neu berechnet. Aktuelle Werte stehen in report.md und im Vergleichsbericht.

# Auswertung Model Zoo 5.5 auf HailoRT 5.4

Der technische Lauf ist abgeschlossen: neun Hailo-Modelle und die CPU-Referenz erzeugten jeweils 198 Antworten (drei Wiederholungen, 33 Fragen auf Deutsch und Englisch). Drei weitere Hailo-Modelle scheiterten beim Laden.

| Modell | Objektive Punkte | Offene Prüfungen |
|---|---:|---:|
| Qwen3-4B-Instruct-2507 | 0/0 | 0 |
| Gemma4-E2B-Instruct | 0/0 | 0 |
| Qwen3-VL-4B-Instruct | 0/0 | 0 |
| DeepSeek-R1-Distill-Qwen-1.5B | 16/126 (12.7 %) | 0 |
| Qwen2.5-Coder-1.5B-Instruct | 105.5/126 (83.7 %) | 0 |
| Qwen2-1.5B-Instruct | 103.5/126 (82.1 %) | 0 |
| Qwen2-VL-2B-Instruct | 93/126 (73.8 %) | 0 |
| Qwen2.5-1.5B-Instruct | 75.5/126 (59.9 %) | 0 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 71.5/126 (56.7 %) | 0 |
| Llama3.2-1B-Instruct | 63/126 (50.0 %) | 0 |
| Qwen3-1.7B-Instruct | 115.5/126 (91.7 %) | 0 |
| Qwen3-VL-2B-Instruct | 110/126 (87.3 %) | 57 |
| gemma-4-E2B-it | 120/123 (97.6 %) | 75 |

Gemma4-E2B auf CPU erreicht bisher 120/123 bewertete Punkte; drei objektive Antworten und 72 redaktionelle Prüfungen sind offen. Dies ist noch keine endgültige Trefferquote. Alle 36 kontrollierten Antworten waren in Inhalt und Format korrekt. Die CPU-Referenz erreicht 8,29–8,43 Decode-Token/s, TTFT 1,27–1,30 s und 2,92 s mittlere Ladezeit. Der gemessene RSS nach dem Laden (0,46 GiB) ist kein Spitzenverbrauch während der Inferenz.

Qwen3-1.7B liefert unter den Hailo-Modellen die höchsten objektiven Punkte (91,7 %), benötigt aber etwa 4,7 Token/s. Qwen2.5-Coder und Qwen2 bieten mit etwa 8 Token/s und 83,7 beziehungsweise 82,1 % einen guten Kompromiss in diesem Fragenkatalog. Qwen3-VL-2B erreicht 87,3 %, lädt aber im Mittel 16,03 s. Llama ist mit etwa 9,9 Token/s am schnellsten, erreicht jedoch nur 50 % objektive Punkte.

Hohe Sachpunkte bedeuten keine zuverlässige Gerätesteuerung: Qwen3-1.7B bestand nur 9 von 72 redaktionellen Aufgaben. Mehrere Modelle erfinden Wetterdaten oder bestätigen Geräteaktionen ohne tatsächlich angebundene Werkzeuge. Für den Service müssen Zustände und ausgeführte Aktionen durch reale Werkzeuge bestätigt werden.

DeepSeek schneidet unter dem Limit von 128 Ausgabetokens schlecht ab (12,7 %); häufig wird der Denktext vor einer abschließenden Antwort abgeschnitten. Diese Einstellung begrenzt die Aussage über seine allgemeine Fähigkeit.

Qwen3-4B und Qwen3-VL-4B scheiterten mit HAILO_RESOURCE_EXHAUSTED(81), Gemma4 auf Hailo mit HAILO_TIMEOUT(4). Hieraus ergibt sich keine Bewertung der Antwortqualität. Die Kombination aus Zoo-5.5-Artefakten und HailoRT 5.4 ist keine bestätigte 5.5-Referenzkonfiguration; nach dem vorgesehenen Runtime-Upgrade sind Wiederholungen erforderlich.

Der Fragenkatalog enthält ähnliche Aufgaben und korrelierte Wiederholungen; Punkte umfassen Teilgutschriften. VLM wurden ausschließlich im Textchat getestet. Kleine Punktunterschiede sind kein statistisch abgesicherter Modellvergleich.

Der Vergleich mit Zoo 5.4 wurde am 04.11.2026 um 19:03 CET automatisch gestartet. Gleiche Fragen, drei Wiederholungen, neuer Kontext je Frage, 128 Ausgabetokens, gleiche Messgrößen und Hintergrunddownload. Neun Hailo-Modelle und die CPU-Referenz werden geprüft; die Auswertung wird laufend aktualisiert und nach Abschluss separat archiviert.

Das ursprüngliche Archiv mit SHA256-Prüfung bleibt unverändert; dieser ergänzende Analysebericht ist separat gespeichert.
