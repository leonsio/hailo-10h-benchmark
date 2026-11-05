# Run · runtime55-zoo55-qwen4b-persistent

[Deutsch](README.de.md) · [English](README.en.md) · [Overview](../../overview.en.md)

Runtime: **HailoRT-CLI version 5.5.0** · Zoo: **v5.5.0** · Start: 2026-11-05T08:11:08+0100

Main experiment / supplemental full-model retry.

| Model | Answers | Loads | Load s | TTFT DE / EN s | Decode token/s | File GiB | Hailo RAM GiB | Host RSS GiB | Objective points | Editorial points | Pending |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen3-4B-Instruct-2507 | 198 | 3 | 18.85 | 3.08 / 1.55 | 2.10 | 5.27 | 6.13 | 0.12 | 98/126 | 58/72 | 0 |

Three means are not controlled cold starts. RAM is measured after loading, not peak inference memory. Missing values are not zeros. Objective and editorial points remain separate; 0 pending does not mean all answers passed.

Supplemental run: HTTP range retries and verified SHA256 download; prefetch disabled. Three repeats, 198 answers; never average its results with the failed download attempt.

## Repetitions

- [Run 1](repeat-1.en.md)
- [Run 2](repeat-2.en.md)
- [Run 3](repeat-3.en.md)

## Original data

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
