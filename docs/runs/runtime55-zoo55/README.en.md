# Run · runtime55-zoo55

[Deutsch](README.de.md) · [English](README.en.md) · [Overview](../../overview.en.md)

Runtime: **HailoRT-CLI version 5.5.0** · Zoo: **v5.5.0** · Start: 2026-11-05T00:14:57+0100

Main experiment.

| Model | Answers | Loads | Load s | TTFT DE / EN s | Decode token/s | File GiB | Hailo RAM GiB | Host RSS GiB | Objective points | Editorial points | Pending |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen3-4B-Instruct-2507 | 198 | 3 | 18.85 | 3.08 / 1.55 | 2.10 | 5.27 | 6.13 | 0.12 | 98/126 | 58/72 | 0 |
| Gemma4-E2B-Instruct | 198 | 3 | 13.48 | 0.52 / 0.45 | 5.67 | 3.11 | 3.78 | 0.08 | 79.5/126 | 59.25/72 | 0 |
| Qwen3-VL-4B-Instruct | 198 | 3 | 22.87 | 3.28 / 1.65 | 2.29 | 6.08 | 6.95 | 0.12 | 105.5/126 | 59/72 | 0 |
| DeepSeek-R1-Distill-Qwen-1.5B | 198 | 3 | 5.72 | 1.74 / 1.46 | 7.70 | 2.10 | 2.49 | 0.07 | 10.25/126 | 0/72 | 0 |
| Qwen2.5-Coder-1.5B-Instruct | 198 | 3 | 3.84 | 0.63 / 0.32 | 8.33 | 1.55 | 2.02 | 0.07 | 98.5/126 | 16/72 | 0 |
| Qwen2-1.5B-Instruct | 198 | 3 | 3.94 | 0.63 / 0.32 | 8.32 | 1.54 | 2.02 | 0.07 | 90.5/126 | 38/72 | 0 |
| Qwen2-VL-2B-Instruct | 198 | 3 | 8.10 | 0.55 / 0.28 | 7.75 | 2.91 | 3.50 | 0.08 | 84/126 | 30/72 | 0 |
| Qwen2.5-1.5B-Instruct | 198 | 3 | 5.22 | 0.73 / 0.37 | 7.40 | 2.32 | 2.81 | 0.07 | 72.5/126 | 31/72 | 0 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 198 | 3 | 6.56 | 0.80 / 0.40 | 7.01 | 2.43 | 3.02 | 0.09 | 68.5/126 | 7/72 | 0 |
| Llama3.2-1B-Instruct | 198 | 3 | 3.60 | 0.67 / 0.39 | 10.09 | 1.26 | 1.74 | 0.07 | 39/126 | 21/72 | 0 |
| Qwen3-1.7B-Instruct | 198 | 3 | 7.02 | 1.25 / 0.63 | 4.77 | 2.75 | 3.40 | 0.08 | 112.5/126 | 9/72 | 0 |
| Qwen3-VL-2B-Instruct | 198 | 3 | 7.96 | 1.26 / 0.64 | 4.88 | 2.97 | 3.75 | 0.08 | 107/126 | 0/72 | 0 |
| gemma-4-E2B-it | 198 | 3 | 2.74 | 1.26 / 1.25 | 8.48 | 2.41 | — | 0.46 | 108/126 | 66/72 | 0 |

Three means are not controlled cold starts. RAM is measured after loading, not peak inference memory. Missing values are not zeros. Objective and editorial points remain separate; 0 pending does not mean all answers passed.

Qwen3-4B is included in this experiment: 3 loads and 198 answers. Its measurements were collected later with background prefetch disabled; questions and inference settings match. Source records and the original download failure are retained under provenance/.

## Repetitions

- [Run 1](repeat-1.en.md)
- [Run 2](repeat-2.en.md)
- [Run 3](repeat-3.en.md)

## Original data

- [metadata.json](../../../benchmarks/catalog55/results/runtime55-zoo55/metadata.json)
- [questions.json](../../../benchmarks/catalog55/results/runtime55-zoo55/questions.json)
- [answers.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo55/answers.jsonl)
- [loads.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo55/loads.jsonl)
- [events.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo55/events.jsonl)
- [answer_checks.jsonl](../../../benchmarks/catalog55/results/runtime55-zoo55/answer_checks.jsonl)
- [manual_reviews.json](../../../benchmarks/catalog55/results/runtime55-zoo55/manual_reviews.json)
- [correctness_summary.csv](../../../benchmarks/catalog55/results/runtime55-zoo55/correctness_summary.csv)
- [evaluation_metadata.json](../../../benchmarks/catalog55/results/runtime55-zoo55/evaluation_metadata.json)
- [report.md](../../../benchmarks/catalog55/results/runtime55-zoo55/report.md)
- [evaluation_history](../../../benchmarks/catalog55/results/runtime55-zoo55/evaluation_history)
- [provenance](../../../benchmarks/catalog55/results/runtime55-zoo55/provenance)
