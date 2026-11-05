# Testlauf · runtime55-zoo55-qwen4b-persistent

[Deutsch](README.de.md) · [English](README.en.md) · [Gesamtübersicht](../../overview.de.md)

Runtime: **HailoRT-CLI version 5.5.0** · Zoo: **v5.5.0** · Start: 2026-11-05T08:11:08+0100

Hauptexperiment / vollständiger Modellnachtest.

| Modell | Antworten | Ladungen | Laden s | TTFT DE / EN s | Decode Token/s | Datei GiB | Hailo-RAM GiB | Host-RSS GiB | Objektive Punkte | Redaktionelle Punkte | Offen |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen3-4B-Instruct-2507 | 198 | 3 | 18.85 | 3.08 / 1.55 | 2.10 | 5.27 | 6.13 | 0.12 | 98/126 | 58/72 | 0 |

Mittelwerte sind keine kontrollierten Kaltstarts. RAM wird nach dem Laden gemessen, nicht als Inferenzspitze. Fehlende Werte sind keine Nullen. Objektive und redaktionelle Punkte bleiben getrennt; 0 offene Prüfungen bedeutet nicht, dass alle Antworten bestanden haben.

Ergänzender Lauf: HTTP-Teil-Downloads mit Wiederholungen und SHA256-Prüfung; Vorladen deaktiviert. Drei Wiederholungen, 198 Antworten; nicht mit dem fehlgeschlagenen Downloadversuch mitteln.

## Wiederholungen

- [Durchlauf 1](repeat-1.de.md)
- [Durchlauf 2](repeat-2.de.md)
- [Durchlauf 3](repeat-3.de.md)

## Originaldaten

- [metadata.json](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-persistent/metadata.json)
- [questions.json](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-persistent/questions.json)
- [answers.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-persistent/answers.jsonl)
- [loads.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-persistent/loads.jsonl)
- [events.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-persistent/events.jsonl)
- [answer_checks.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-persistent/answer_checks.jsonl)
- [manual_reviews.json](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-persistent/manual_reviews.json)
- [correctness_summary.csv](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-persistent/correctness_summary.csv)
- [evaluation_metadata.json](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-persistent/evaluation_metadata.json)
- [report.md](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-persistent/report.md)
- [evaluation_history](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-persistent/evaluation_history)
