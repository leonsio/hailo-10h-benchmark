# Testlauf · runtime55-zoo54

[Deutsch](README.de.md) · [English](README.en.md) · [Gesamtübersicht](../../overview.de.md)

Runtime: **HailoRT-CLI version 5.5.0** · Zoo: **v5.4.0** · Start: 2026-11-05T04:34:02+0100

Hauptexperiment.

| Modell | Antworten | Ladungen | Laden s | TTFT DE / EN s | Decode Token/s | Datei GiB | Hailo-RAM GiB | Host-RSS GiB | Objektive Punkte | Redaktionelle Punkte | Offen |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DeepSeek-R1-Distill-Qwen-1.5B | 198 | 3 | 4.97 | 1.75 / 1.47 | 7.84 | 2.13 | 2.69 | 0.07 | 10.25/126 | 0/72 | 0 |
| Qwen2.5-Coder-1.5B-Instruct | 198 | 3 | 3.78 | 0.63 / 0.32 | 8.30 | 1.56 | 2.18 | 0.07 | 98.5/126 | 16/72 | 0 |
| Qwen2-1.5B-Instruct | 198 | 3 | 3.83 | 0.63 / 0.32 | 8.32 | 1.59 | 2.21 | 0.07 | 90.5/126 | 40/72 | 0 |
| Qwen2-VL-2B-Instruct | 198 | 3 | 8.27 | 0.68 / 0.35 | 7.20 | 3.03 | 3.73 | 0.08 | 64.5/126 | 33/72 | 0 |
| Qwen2.5-1.5B-Instruct | 198 | 3 | 5.18 | 0.73 / 0.37 | 7.37 | 2.30 | 2.88 | 0.07 | 72.5/126 | 31/72 | 0 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 198 | 3 | 8.05 | 0.79 / 0.40 | 6.86 | 3.17 | 3.83 | 0.09 | 63/126 | 7/72 | 0 |
| Llama3.2-1B-Instruct | 198 | 3 | 3.62 | 0.68 / 0.39 | 10.11 | 1.31 | 1.86 | 0.07 | 39/126 | 24/72 | 0 |
| Qwen3-1.7B-Instruct | 198 | 3 | 6.85 | 1.25 / 0.63 | 4.85 | 2.68 | 3.37 | 0.08 | 112.5/126 | 9/72 | 0 |
| Qwen3-VL-2B-Instruct | 198 | 3 | 8.05 | 1.25 / 0.63 | 4.77 | 2.97 | 3.79 | 0.08 | 77/126 | 1/72 | 0 |
| gemma-4-E2B-it | 198 | 3 | 2.61 | 1.28 / 1.27 | 8.37 | 2.41 | — | 0.46 | 108/126 | 66/72 | 0 |

Mittelwerte sind keine kontrollierten Kaltstarts. RAM wird nach dem Laden gemessen, nicht als Inferenzspitze. Fehlende Werte sind keine Nullen. Objektive und redaktionelle Punkte bleiben getrennt; 0 offene Prüfungen bedeutet nicht, dass alle Antworten bestanden haben.

## Wiederholungen

- [Durchlauf 1](repeat-1.de.md)
- [Durchlauf 2](repeat-2.de.md)
- [Durchlauf 3](repeat-3.de.md)

## Originaldaten

- [metadata.json](../../../benchmarks/catalog55/results/runtime55-zoo54/metadata.json)
- [questions.json](../../../benchmarks/catalog55/results/runtime55-zoo54/questions.json)
- [answers.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo54/answers.jsonl)
- [loads.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo54/loads.jsonl)
- [events.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo54/events.jsonl)
- [answer_checks.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo54/answer_checks.jsonl)
- [manual_reviews.json](../../../benchmarks/catalog55/results/runtime55-zoo54/manual_reviews.json)
- [correctness_summary.csv](../../../benchmarks/catalog55/results/runtime55-zoo54/correctness_summary.csv)
- [evaluation_metadata.json](../../../benchmarks/catalog55/results/runtime55-zoo54/evaluation_metadata.json)
- [report.md](../../../benchmarks/catalog55/results/runtime55-zoo54/report.md)
- [evaluation_history](../../../benchmarks/catalog55/results/runtime55-zoo54/evaluation_history)
