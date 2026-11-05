# Testlauf · runtime54-prefetch

[Deutsch](README.de.md) · [English](README.en.md) · [Gesamtübersicht](../../overview.de.md)

Runtime: **HailoRT-CLI version 5.4.0** · Zoo: **v5.5.0** · Start: 2026-11-04T14:57:48+0100

Hauptexperiment.

| Modell | Antworten | Ladungen | Laden s | TTFT DE / EN s | Decode Token/s | Datei GiB | Hailo-RAM GiB | Host-RSS GiB | Objektive Punkte | Redaktionelle Punkte | Offen |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen3-4B-Instruct-2507 | 0 | 0 | — | — / — | — | 5.27 | — | — | — | — | — |
| Gemma4-E2B-Instruct | 0 | 0 | — | — / — | — | 3.11 | — | — | — | — | — |
| Qwen3-VL-4B-Instruct | 0 | 0 | — | — / — | — | 6.08 | — | — | — | — | — |
| DeepSeek-R1-Distill-Qwen-1.5B | 198 | 3 | 5.36 | 1.78 / 1.49 | 7.43 | 2.10 | 2.62 | 0.08 | 10.25/126 | 0/72 | 0 |
| Qwen2.5-Coder-1.5B-Instruct | 198 | 3 | 3.92 | 0.64 / 0.33 | 8.05 | 1.55 | 2.13 | 0.07 | 98.5/126 | 16/72 | 0 |
| Qwen2-1.5B-Instruct | 198 | 3 | 4.12 | 0.64 / 0.33 | 8.07 | 1.54 | 2.11 | 0.08 | 90.5/126 | 40/72 | 0 |
| Qwen2-VL-2B-Instruct | 198 | 3 | 12.31 | 0.56 / 0.28 | 7.55 | 2.91 | 3.59 | 0.08 | 84/126 | 33/72 | 0 |
| Qwen2.5-1.5B-Instruct | 198 | 3 | 8.77 | 0.74 / 0.38 | 7.16 | 2.32 | 2.90 | 0.08 | 72.5/126 | 31/72 | 0 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 198 | 3 | 6.72 | 0.81 / 0.41 | 6.77 | 2.43 | 3.10 | 0.10 | 68.5/126 | 7/72 | 0 |
| Llama3.2-1B-Instruct | 198 | 3 | 3.61 | 0.68 / 0.40 | 9.90 | 1.26 | 1.82 | 0.07 | 39/126 | 24/72 | 0 |
| Qwen3-1.7B-Instruct | 198 | 3 | 7.99 | 1.26 / 0.64 | 4.71 | 2.75 | 3.52 | 0.08 | 112.5/126 | 9/72 | 0 |
| Qwen3-VL-2B-Instruct | 198 | 3 | 16.03 | 1.27 / 0.64 | 4.81 | 2.97 | 3.85 | 0.08 | 107/126 | 0/72 | 0 |
| gemma-4-E2B-it | 198 | 3 | 2.92 | 1.30 / 1.27 | 8.36 | 2.41 | — | 0.46 | 108/126 | 66/72 | 0 |

Mittelwerte sind keine kontrollierten Kaltstarts. RAM wird nach dem Laden gemessen, nicht als Inferenzspitze. Fehlende Werte sind keine Nullen. Objektive und redaktionelle Punkte bleiben getrennt; 0 offene Prüfungen bedeutet nicht, dass alle Antworten bestanden haben.

## Fehler

- **Qwen3-4B-Instruct-2507**: worker_exit
- **Gemma4-E2B-Instruct**: worker_exit
- **Qwen3-VL-4B-Instruct**: worker_exit

## Wiederholungen

- [Durchlauf 1](repeat-1.de.md)
- [Durchlauf 2](repeat-2.de.md)
- [Durchlauf 3](repeat-3.de.md)

## Originaldaten

- [metadata.json](../../../benchmarks/catalog55/results/runtime54-prefetch/metadata.json)
- [questions.json](../../../benchmarks/catalog55/results/runtime54-prefetch/questions.json)
- [answers.jsonl](../../../benchmarks/catalog55/results/runtime54-prefetch/answers.jsonl)
- [loads.jsonl](../../../benchmarks/catalog55/results/runtime54-prefetch/loads.jsonl)
- [events.jsonl](../../../benchmarks/catalog55/results/runtime54-prefetch/events.jsonl)
- [answer_checks.jsonl](../../../benchmarks/catalog55/results/runtime54-prefetch/answer_checks.jsonl)
- [manual_reviews.json](../../../benchmarks/catalog55/results/runtime54-prefetch/manual_reviews.json)
- [correctness_summary.csv](../../../benchmarks/catalog55/results/runtime54-prefetch/correctness_summary.csv)
- [evaluation_metadata.json](../../../benchmarks/catalog55/results/runtime54-prefetch/evaluation_metadata.json)
- [report.md](../../../benchmarks/catalog55/results/runtime54-prefetch/report.md)
- [evaluation_history](../../../benchmarks/catalog55/results/runtime54-prefetch/evaluation_history)
