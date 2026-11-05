# Run · runtime54-zoo54

[Deutsch](README.de.md) · [English](README.en.md) · [Overview](../../overview.en.md)

Runtime: **HailoRT-CLI version 5.4.0** · Zoo: **v5.4.0** · Start: 2026-11-04T19:03:16+0100

Main experiment.

| Model | Answers | Loads | Load s | TTFT DE / EN s | Decode token/s | File GiB | Hailo RAM GiB | Host RSS GiB | Objective points | Editorial points | Pending |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DeepSeek-R1-Distill-Qwen-1.5B | 198 | 3 | 5.13 | 1.78 / 1.49 | 7.54 | 2.13 | 2.77 | 0.08 | 10.25/126 | 0/72 | 0 |
| Qwen2.5-Coder-1.5B-Instruct | 198 | 3 | 3.91 | 0.64 / 0.33 | 8.07 | 1.56 | 2.25 | 0.08 | 98.5/126 | 16/72 | 0 |
| Qwen2-1.5B-Instruct | 198 | 3 | 5.51 | 0.64 / 0.33 | 8.09 | 1.59 | 2.31 | 0.08 | 90.5/126 | 38/72 | 0 |
| Qwen2-VL-2B-Instruct | 198 | 3 | 12.80 | 0.69 / 0.35 | 7.01 | 3.03 | 3.80 | 0.08 | 64.5/126 | 33/72 | 0 |
| Qwen2.5-1.5B-Instruct | 198 | 3 | 11.56 | 0.74 / 0.38 | 7.12 | 2.30 | 2.94 | 0.08 | 72.5/126 | 31/72 | 0 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 198 | 3 | 9.97 | 0.81 / 0.41 | 6.72 | 3.17 | 3.91 | 0.10 | 63/126 | 7/72 | 0 |
| Llama3.2-1B-Instruct | 198 | 3 | 3.65 | 0.68 / 0.40 | 9.98 | 1.31 | 1.93 | 0.07 | 39/126 | 21/72 | 0 |
| Qwen3-1.7B-Instruct | 198 | 3 | 9.38 | 1.26 / 0.64 | 4.77 | 2.68 | 3.48 | 0.08 | 112.5/126 | 9/72 | 0 |
| Qwen3-VL-2B-Instruct | 198 | 3 | 15.65 | 1.26 / 0.64 | 4.70 | 2.97 | 3.86 | 0.08 | 77/126 | 1/72 | 0 |
| gemma-4-E2B-it | 198 | 3 | 3.21 | 1.32 / 1.27 | 8.42 | 2.41 | — | 0.46 | 108/126 | 66/72 | 0 |

Three means are not controlled cold starts. RAM is measured after loading, not peak inference memory. Missing values are not zeros. Objective and editorial points remain separate; 0 pending does not mean all answers passed.

## Repetitions

- [Run 1](repeat-1.en.md)
- [Run 2](repeat-2.en.md)
- [Run 3](repeat-3.en.md)

## Original data

- [metadata.json](../../../benchmarks/catalog55/results/runtime54-zoo54/metadata.json)
- [questions.json](../../../benchmarks/catalog55/results/runtime54-zoo54/questions.json)
- [answers.jsonl](../../../benchmarks/catalog55/results/runtime54-zoo54/answers.jsonl)
- [loads.jsonl](../../../benchmarks/catalog55/results/runtime54-zoo54/loads.jsonl)
- [events.jsonl](../../../benchmarks/catalog55/results/runtime54-zoo54/events.jsonl)
- [answer_checks.jsonl](../../../benchmarks/catalog55/results/runtime54-zoo54/answer_checks.jsonl)
- [manual_reviews.json](../../../benchmarks/catalog55/results/runtime54-zoo54/manual_reviews.json)
- [correctness_summary.csv](../../../benchmarks/catalog55/results/runtime54-zoo54/correctness_summary.csv)
- [evaluation_metadata.json](../../../benchmarks/catalog55/results/runtime54-zoo54/evaluation_metadata.json)
- [report.md](../../../benchmarks/catalog55/results/runtime54-zoo54/report.md)
- [evaluation_history](../../../benchmarks/catalog55/results/runtime54-zoo54/evaluation_history)
