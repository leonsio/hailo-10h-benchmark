# Testlauf · runtime55-zoo55-qwen4b-retry

[Deutsch](README.de.md) · [English](README.en.md) · [Gesamtübersicht](../../overview.de.md)

Runtime: **HailoRT-CLI version 5.5.0** · Zoo: **v5.5.0** · Start: 2026-11-05T07:48:17+0100

Diagnose-, Vorab-, abgebrochener oder fehlgeschlagener Lauf. Nicht in die Gesamtvergleichswerte eingemischt. Einstellungen können abweichen; alte Bewertungsdateien werden nicht als v1.3 ausgegeben.

| Modell | Antworten | Ladungen | Laden s | TTFT DE / EN s | Decode Token/s | Datei GiB | Hailo-RAM GiB | Host-RSS GiB | Objektive Punkte | Redaktionelle Punkte | Offen |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen3-4B-Instruct-2507 | 0 | 0 | — | — / — | — | — | — | — | — | — | — |

Mittelwerte sind keine kontrollierten Kaltstarts. RAM wird nach dem Laden gemessen, nicht als Inferenzspitze. Fehlende Werte sind keine Nullen. Objektive und redaktionelle Punkte bleiben getrennt; 0 offene Prüfungen bedeutet nicht, dass alle Antworten bestanden haben.

## Fehler

- **Qwen3-4B-Instruct-2507**: RuntimeError('download exit 18')

## Wiederholungen

- [Durchlauf 1](repeat-1.de.md)
- [Durchlauf 2](repeat-2.de.md)
- [Durchlauf 3](repeat-3.de.md)

## Originaldaten

- [metadata.json](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-retry/metadata.json)
- [questions.json](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-retry/questions.json)
- [events.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-retry/events.jsonl)
- [answer_checks.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-retry/answer_checks.jsonl)
- [manual_reviews.json](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-retry/manual_reviews.json)
- [correctness_summary.csv](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-retry/correctness_summary.csv)
- [evaluation_metadata.json](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-retry/evaluation_metadata.json)
- [report.md](../../../benchmarks/catalog55/results/runtime55-zoo55-qwen4b-retry/report.md)
