# Modellkatalog 5.5: isolierter Chat-Benchmark

`questions.md` und `questions.json` enthalten die 33 Aufgaben aus
`doc/model-benchmark-evaluation.md` auf Deutsch und Englisch. `build_questions.py`
erzeugt diese Dateien reproduzierbar aus der historischen Dokumentation.
Die englischen Originale E10–E14 bleiben unverändert erhalten. E15 hat absichtlich
einen Tippfehler. C06 verlangt in beiden Sprachfassungen eine deutsche Übersetzung.
Die HA-Aufgaben sind reine Texttests ohne Werkzeuge und ohne Geräteausführung.

Start im Repository:

```bash
sudo systemctl stop hailo-10h-services
/opt/hailo-10h-services/venv/bin/python benchmarks/catalog55/run.py
```

Der Lauf prüft den Dienststatus, sichtbare Gerätenutzer und mindestens 10 GB
freien Datenträgerspeicher. Er ändert weder installierte Runtime noch Firmware.
Katalog-Release ist v5.5.0, die tatsächlich verwendete Runtime/Firmware wird in
`metadata.json` protokolliert. Auf Runtime 5.4 können 5.5-Artefakte inkompatibel
sein. Fehler werden aufgezeichnet und niemals als gültige Messungen behandelt.
Gemma heißt im offiziellen 5.5-Katalog **Gemma4-E2B-Instruct**; ein
Gemma3-E2B-Modell ist dort nicht aufgeführt. Beide Qwen3-4B-Modelle benötigen
8 GB DRAM auf dem Hailo; der Host-RAM ersetzt diesen nicht.

Alle 12 vollständigen LLM/VLM-Chatmodelle mit 5.5-Download im Projektkatalog
werden nacheinander geprüft. Whisper, Embeddings, Detektoren und reine
Bildencoder sind keine Chatmodelle. Danach folgt Gemma4-E2B über LiteRT/CPU.
VLMs erhalten Text ohne Bild, damit die Chatqualität mit denselben Aufgaben
verglichen wird. Dies ist kein Test der Bildverarbeitung.

Jedes Modell wird dreimal in jeweils einem neuen Prozess geladen. Jeder Prozess
stellt 66 Anfragen (33 × DE/EN), jeweils mit leerem KV-Kontext bzw. neuer
LiteRT-Konversation. `temperature=0.1`, Seeds 1/2/3 und höchstens 128
Ausgabetokens gelten für alle Modelle. Es gibt keinen ungemessenen Warmup.
Die erste Anfrage nach dem Laden ist daher im Ergebnis enthalten. Der
Systemprompt ist in `run.py` dokumentiert und verlangt eine Antwort in der
jeweiligen Testsprache. Die Ergebnisse reproduzieren nicht den alten 32-Token-Test.

Gemessen werden:

- Ladezeit vom nativen Modellkonstruktor bis zur Rückkehr; ohne Download,
  Python-Importe oder VDevice-Erzeugung. Der Betriebssystem-Dateicache wird nicht
  geleert; dies sind drei frische Modellladungen, keine garantierten kalten I/O-Ladungen.
- TTFT bis zum ersten nichtleeren Textchunk, einschließlich Kontextinitialisierung.
  Die Streaming-API liefert Textchunks, keine verlässlichen einzelnen Tokenereignisse.
- Token/s über die gesamte Anfrage einschließlich TTFT (`tokens_per_s`).
- Zusätzlich Decode-Token/s nach dem ersten Textchunk (`decode_tokens_per_s`),
  soweit mehrere Chunks vorliegen. Die Tokenzahl stammt aus dem jeweiligen
  Modelltokenizer durch erneutes Tokenisieren der Ausgabe, nicht aus der Chunkzahl.
  Re-Tokenisierung kann von der internen Anzahl generierter Tokens abweichen.

`answers.jsonl` enthält vollständige Antworten, Zeiten und Fehler.
`loads.jsonl` enthält Ladezeiten. `events.jsonl` enthält Download-URL, SHA256,
Prozessstatus und Löschungen. `summary.csv/json` enthält arithmetische Mittelwerte
je Modell/Sprache; `question_means.json` enthält Mittelwerte je Frage/Sprache über
die erfolgreichen Wiederholungen. Erfolgszahlen müssen für einen vollständigen
Vergleich geprüft werden. Native Fehler stehen auch in `<model>-<repeat>.log`.

Downloads liegen ausschließlich im Ergebnisverzeichnis und werden nach den drei
Durchläufen im `finally`-Block entfernt. Vorhandene Servicemodelle werden nicht
verändert. Ein neuer Lauf braucht ein neues Ergebnisverzeichnis. Der Dienst bleibt
nach Abschluss gestoppt. Ein harter Abbruch (`SIGKILL`, Stromausfall) kann einen
Download zurücklassen; in diesem Fall nur das betroffene `downloads`-Verzeichnis
im Ergebnisordner entfernen.

Optionen: `--mode cpu|hailo|all`, `--models Name1,Name2`, `--repeats 3`,
`--limit 1` für einen Smoke-Test, `--output <neues Verzeichnis>`.

Quellen:
- https://github.com/hailo-ai/hailo_model_zoo_genai/blob/v5.5.0/docs/MODELS.rst
- https://github.com/hailo-ai/hailo_model_zoo_genai/blob/v5.5.0/docs/CHANGELOG.rst

Der Elternprozess beendet einen Worker, wenn 600 Sekunden ohne neue Ladezeit
oder Antwort vergehen (`--stall-timeout`). Zusätzlich gilt eine Obergrenze von
vier Stunden pro Wiederholung (`--timeout`). Ein Timeout ist ein fehlgeschlagener
Versuch, keine gemessene Ladezeit. Andere Modelle werden danach weiter geprüft.

Pro Modell liegt der Download ausdrücklich **vor** der Schleife der drei
Wiederholungen. Die drei Ladungen verwenden dieselbe heruntergeladene Datei.
Der separate Smoke-Test ist ein eigenständiger Testlauf und wird nicht in die
Mittelwerte des vollständigen Laufs eingerechnet. Die äußere Stillstandsgrenze im
Skript ist unabhängig von nativen HailoRT-Timeouts; HailoRT 5.4 meldete beim ersten
Gemma4-Start nach etwa 122 Sekunden `HAILO_TIMEOUT`.

## Vorabprüfung mit installiertem Servicemodell

```bash
/opt/hailo-10h-services/venv/bin/python benchmarks/catalog55/run.py \
  --models Qwen3-VL-2B-Instruct \
  --local-model /usr/local/hailo/resources/models/hailo10h/Qwen3-VL-2B-Instruct.hef \
  --limit 6 --repeats 3 --max-tokens 32 \
  --output benchmarks/catalog55/results/known-service-model
```

`--local-model` überspringt den Download vollständig. Die Quelldatei wird nie
vom Skript gelöscht. Genau ein Modell muss über `--models` ausgewählt werden.
Dieser separate Lauf verwendet das vorhandene Service-Artefakt; dessen Release
wird nicht als 5.5 ausgegeben. Der SHA256-Hash wird aufgezeichnet.

Mit `--download-cache <Pfad>` können vollständig abgeschlossene Testdownloads
nach einem unterbrochenen Lauf wiederverwendet werden. Dafür müssen URL, Größe
und SHA256 mit einer zuvor gespeicherten `.receipt.json` übereinstimmen. Dieser
Cache muss innerhalb von `benchmarks/catalog55/results` liegen. Die Testdatei und
ihr Beleg werden nach den drei Durchläufen entfernt. Vorhandene Servicemodelle
werden ausschließlich mit `--local-model` eingebunden und bleiben erhalten.

## Gemma-Einstellungen und Vorladen

Das Gerät besitzt etwa 8 GB Modulspeicher (Monitor: 7221 MB nutzbar). Der native
API-Standard `optimize_memory_on_device=False` wird verwendet. Die Option
`--optimize-memory` aktiviert die von Hailo für bestimmte Modelle auf 4-GB-Geräten
benötigte Host-Tokenisierung. Der Probelauf mit dem vorhandenen Servicemodell
funktionierte sowohl mit als auch ohne diese Option. Die bisherigen drei
Gemma-Fehler unter HailoRT 5.4 mit aktivierter Option bleiben in
`results/runtime54-validated` getrennt von späteren Konfigurationen.

Der Host-Request-Timeout wird über `HAILO_REQUEST_TIMEOUT_SECONDS=300` gesetzt
(`--native-timeout`). Das ist im HailoRT-5.4-Quellcode dokumentiert:
https://github.com/hailo-ai/hailort/blob/v5.4.0/hailort/hrpc/client.cpp
Die äußere Grenze ohne Lade-/Antwortfortschritt beträgt 600 Sekunden.
Ein separater interner Geräte-Timeout kann trotzdem früher eintreten.
Gemma4 ist laut offiziellem Katalog erst mit der 5.5-Generation unterstützt;
ein Parameter ersetzt keine fehlende Unterstützung in Firmware/Runtime 5.4.

Nach der ersten erfolgreichen Ladung eines Modells startet **genau ein**
Hintergrundthread den Download des nächsten Modells. Der Download einschließlich
SHA256-Prüfung kann sich mit Inferenz und späteren Wiederholungen überschneiden.
Die Metadaten und `prefetch_started`-Ereignisse halten das fest. Es laufen niemals
zwei native Modelle gleichzeitig. Maximal das aktuelle und das nächste Artefakt
liegen im Testcache. Bei fehlgeschlagenen Modellladungen wird das nächste Modell
anschließend regulär vorbereitet. `--no-prefetch` deaktiviert die Überlappung.

Die Ergebnisse mit Vorladen sind Messungen unter dieser zusätzlichen
Netzwerk-/I/O-Last. Sie werden nicht mit den separaten Vorabtests vermischt.

Prüfung von Überschneidung, Download-Wiederverwendung und Schutz vorhandener
Servicedateien (ohne Zugriff auf den Hailo):

```bash
/opt/hailo-10h-services/venv/bin/python benchmarks/catalog55/test_runner.py
```

## Gerätebelegung vor jeder Modellladung

Jeder Worker prüft vor dem Öffnen seines VDevice erneut den Dienststatus,
Gerätenutzer und die Leistungsstatistik des Hailo. Der lesende Prozess
`hailortcli monitor` darf offen bleiben. Andere sichtbare Gerätenutzer blockieren
die Ladung. Außerdem wird auf weniger als 15 % RAM-Belegung des Hailo und unter
0,5 % NNC-Auslastung gewartet. Damit bleibt der Firmware-/Linux-Grundverbrauch
zulässig; große zurückgebliebene Modelle blockieren den nächsten Start. Dies ist
eine Belegungsprüfung und keine vollständige Modellauflistung des Geräts.

Die Prüfungen stehen als `waiting_for_idle_device` und `device_idle_verified`
in `events.jsonl` und liegen außerhalb der gemessenen Modellladezeit. Unbekannte
Statistikwerte oder ein aktiver Dienst werden als Fehler behandelt. Die Prüfung
wurde während des laufenden Tests ergänzt; frühere Wiederholungen erhalten
rückwirkend keinen solchen Verifikationseintrag.

`--resume --output <vorhandener Ergebnisordner>` setzt einen unterbrochenen Lauf
bei identischer Konfiguration fort, überspringt abgeschlossene Modelle und
setzt Teil-Downloads fort. Ein unabhängiger Hintergrundstart schreibt nach
`runner.log`; seine PID steht in `runner.pid`.

## Modellgröße und RAM

Die Ergebnistabelle enthält `Datei GiB`, `Hailo-RAM GiB` und `Host-RSS GiB`.
Die Dateigröße stammt aus dem tatsächlichen Download bzw. der lokalen Datei
und bleibt auch nach dem Löschen des Testartefakts verfügbar.

Ab der Ergänzung dieser Messung erfassen neue Worker nach dem Laden:

- residente Host-Prozessgröße (RSS) vor und nach dem Modellkonstruktor;
- bei Hailo-Modellen Geräte-RAM vor und nach der Modellladung;
- Differenzen gegenüber dem jeweiligen Ausgangswert.

Die RAM-Abfrage liegt außerhalb der gemessenen Ladezeit und vor der ersten
Chat-Anfrage. Sie ist keine Spitzenmessung während der Generierung. Der Hailo-
Gesamtwert enthält Firmware/Linux; Host-RSS enthält Python und die Runtime.
`model_sizes.csv/json` enthalten Bytewerte, Mittelwerte und die Anzahl vorhandener
RAM-Messungen. Nicht erfasste frühere Ladungen und fehlgeschlagene Starts liefern
keinen RAM-Wert und werden nicht als null in die Mittelwerte eingerechnet.
Eine bereits laufende Wiederholung wird dafür nicht unterbrochen.

Die lesbare Tabelle und `live_summary.csv/json` werden aus allen bereits
vollständig geschriebenen Einzelmessungen berechnet, einschließlich laufender
Wiederholungen. Die Mittelwerte eines noch laufenden Modells sind vorläufig.
Die Statusspalte zeigt den Durchlauf und dessen Antwortfortschritt. Der Zeitpunkt
der letzten Aktualisierung steht im Bericht. Der Hintergrund-Reporter aktualisiert
alle fünf Sekunden; er unterbricht die Modelltests nicht. `summary.csv/json` des
Elternprozesses wird weiterhin nach abgeschlossenen Wiederholungen geschrieben.
Die inhaltliche Richtigkeit wird getrennt durch Referenzprüfungen und dokumentierte redaktionelle Sichtung bewertet.

## Testmatrix und automatische Folge

`test_matrix.json` beschreibt vier Experimente mit demselben Fragenkatalog und
denselben Sampling-/Kontexteinstellungen:

| HailoRT/Firmware | Zoo-Artefakte | Ausführung |
|---|---|---|
| 5.4.0 | v5.5.0 | aktueller Lauf |
| 5.4.0 | v5.4.0 | automatisch nach verifiziertem Archiv des ersten Laufs |
| 5.5.0 | v5.4.0 | erst nach dem späteren Upgrade durch den Benutzer |
| 5.5.0 | v5.5.0 | erst nach dem späteren Upgrade durch den Benutzer |

Zoo 5.4 liefert neun vollständige native Chatmodelle, Zoo 5.5 zwölf. Nur
Modelle mit einem Download für die gewählte Version werden ausgewählt.
Der identische LiteRT/Gemma4-CPU-Vergleich ist unabhängig vom Zoo-Release
und wird am Ende beider Läufe wiederholt. `--release v5.4.0|v5.5.0` ändert
nur die Modellquelle, niemals HailoRT oder Firmware.

`suite.py` läuft unabhängig von der Sitzung, wertet neue Antworten laufend aus
und schreibt den aktuellen Stand nach `results/suite_status.json`. Nach Ende des
ersten Prozesses prüft es, dass alle geplanten Modelle bearbeitet wurden. Es
sichert Ergebnisse, Rohantworten, Logs, Metadaten, Fragenkatalog und Skripte in
`results/archives/*.tar.gz`. Jedes Archiv besitzt ein internes SHA256-Manifest
und eine externe SHA256-Datei. Vor Freigabe werden sämtliche Archivdateien
gegen das Manifest geprüft; Archiv und Prüfsummendatei sind danach schreibgeschützt.
Die ursprünglichen Ergebnisse bleiben erhalten. Modelldownloads werden nicht
archiviert. Die zweite Testserie beginnt erst nach erfolgreicher Archivprüfung
und erneuter Prüfung auf Runtime **und** Firmware 5.4.0. Anschließend wird auch
die zweite Serie gesichert. Der Dienst bleibt gestoppt.

Der aktive Folgelauf braucht keinen weiteren manuellen Start. Eine unterbrochene
Serie blockiert die Folge und wird in `suite_status.json` als `needs_attention`
markiert; unvollständige Daten werden nicht als abgeschlossene Testserie behandelt.
Die HailoRT-5.5-Experimente sind nur geplant und werden nicht automatisch gestartet.

## Prüfung der Antworten

`evaluate.py` verändert keine Rohantworten und verwendet keinen externen
Modellservice. Es schreibt `answer_checks.jsonl`, `correctness_summary.csv/json`,
`evaluation_metadata.json` und eine offene Prüfliste `review_queue.json`.
Die Regeln stehen in `evaluation_rubric.md`; die Auswerterversion und SHA256
von Auswerterskript, Rohantworten und redaktioneller Urteilsdatei werden erfasst.
`manual_reviews.json` enthält begründete redaktionelle Urteile von Codex, keine
behauptete menschliche Begutachtung. Gleichlautende Antworten auf dieselbe
Frage in derselben Sprache teilen ein Urteil. Bereits geprüfte identische
Antworten dürfen im Folgelauf wiederverwendet werden. Neue Antworten bleiben
bis zur Sichtung als offen erkennbar.

Die Ergebnistabelle enthält einen eigenen Richtigkeitsabschnitt. Objektive
Referenzpunkte, verlangtes Antwortformat und qualitative Sichtung sind getrennt.
Nicht abgeschlossene Wiederholungen liefern ausdrücklich vorläufige Werte.
Die automatisch vorgeschlagenen Regeln ersetzen keine universelle semantische
Bewertung beliebiger Texte; zweifelhafte Fälle landen in der Prüfliste.
