# Hailo-10H benchmark: overall assessment

[Deutsch](overview.de.md) · [English](overview.en.md) · [Repository](../README.md)

Data: 4 runtime/Zoo combinations; Qwen3-4B is integrated into the final 5.5/5.5 experiment. Raspberry Pi CM5, about 15 GiB host RAM and an 8 GB Hailo-10H. All headline scores use **reference-checks-v1.3**; previous reports/archives may contain superseded scores.

## Experiment matrix

| Runtime / firmware / driver | Model Zoo 5.4 | Model Zoo 5.5 |
|---|---|---|
| 5.4.0 | [Results](runs/runtime54-zoo54/README.en.md) | [Results](runs/runtime54-prefetch/README.en.md) |
| 5.5.0 | [Results](runs/runtime55-zoo54/README.en.md) | [Results](runs/runtime55-zoo55/README.en.md) |

Runtime means the entire updated firmware/runtime/driver stack. These experiments do not isolate the PCIe driver alone.

## Quality across all four combinations

| Model | RT5.4 / Zoo5.4 | RT5.4 / Zoo5.5 | RT5.5 / Zoo5.4 | RT5.5 / Zoo5.5 |
|---|---:|---:|---:|---:|
| Qwen3-4B-Instruct-2507 | — | — | — | 98/126 |
| Gemma4-E2B-Instruct | — | — | — | 79.5/126 |
| Qwen3-VL-4B-Instruct | — | — | — | 105.5/126 |
| DeepSeek-R1-Distill-Qwen-1.5B | 10.25/126 | 10.25/126 | 10.25/126 | 10.25/126 |
| Qwen2.5-Coder-1.5B-Instruct | 98.5/126 | 98.5/126 | 98.5/126 | 98.5/126 |
| Qwen2-1.5B-Instruct | 90.5/126 | 90.5/126 | 90.5/126 | 90.5/126 |
| Qwen2-VL-2B-Instruct | 64.5/126 | 84/126 | 64.5/126 | 84/126 |
| Qwen2.5-1.5B-Instruct | 72.5/126 | 72.5/126 | 72.5/126 | 72.5/126 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 63/126 | 68.5/126 | 63/126 | 68.5/126 |
| Llama3.2-1B-Instruct | 39/126 | 39/126 | 39/126 | 39/126 |
| Qwen3-1.7B-Instruct | 112.5/126 | 112.5/126 | 112.5/126 | 112.5/126 |
| Qwen3-VL-2B-Instruct | 77/126 | 107/126 | 77/126 | 107/126 |
| gemma-4-E2B-it | 108/126 | 108/126 | 108/126 | 108/126 |

126 possible objective points per full model run; 72 editorial tasks are assessed separately. Repeated/related questions mean this is not a general benchmark accuracy estimate.

## Decode throughput across all four combinations

| Model | RT5.4 / Zoo5.4 | RT5.4 / Zoo5.5 | RT5.5 / Zoo5.4 | RT5.5 / Zoo5.5 |
|---|---:|---:|---:|---:|
| Qwen3-4B-Instruct-2507 | — | — | — | 2.10 |
| Gemma4-E2B-Instruct | — | — | — | 5.67 |
| Qwen3-VL-4B-Instruct | — | — | — | 2.29 |
| DeepSeek-R1-Distill-Qwen-1.5B | 7.54 | 7.43 | 7.84 | 7.70 |
| Qwen2.5-Coder-1.5B-Instruct | 8.07 | 8.05 | 8.30 | 8.33 |
| Qwen2-1.5B-Instruct | 8.09 | 8.07 | 8.32 | 8.32 |
| Qwen2-VL-2B-Instruct | 7.01 | 7.55 | 7.20 | 7.75 |
| Qwen2.5-1.5B-Instruct | 7.12 | 7.16 | 7.37 | 7.40 |
| Qwen2-1.5B-Instruct-Function-Calling-v1 | 6.72 | 6.77 | 6.86 | 7.01 |
| Llama3.2-1B-Instruct | 9.98 | 9.90 | 10.11 | 10.09 |
| Qwen3-1.7B-Instruct | 4.77 | 4.71 | 4.85 | 4.77 |
| Qwen3-VL-2B-Instruct | 4.70 | 4.81 | 4.77 | 4.88 |
| gemma-4-E2B-it | 8.42 | 8.36 | 8.37 | 8.48 |

Token/s, arithmetic means. CPU Gemma uses the same LiteRT artifact in every column; its placement does not make it a Zoo model.

## Runtime 5.5 with Zoo 5.5: full picture

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

## Findings

- Updating the stack mainly improves model compatibility and load times. Gemma4-E2B and Qwen3-VL-4B now run, and the completed Qwen3-4B measurements are included in the final 5.5 experiment. Their runtime-5.4 load failures provide no valid model-quality baseline.
- For the nine shared native models and CPU reference, all 1,980 matched raw answers of the Zoo-5.5 runs are identical across runtime 5.4/5.5. Quality changes therefore come from the Zoo artifacts or revised scoring, not an observed change in answers caused by the runtime update.
- Most shared native models gain only about 1–4% decode throughput with runtime 5.5; CPU reference variability is about 1.5%. Treat these small gains cautiously. Larger load-time reductions include Qwen3-VL-2B (16.03 → 7.96 s), Qwen2-VL-2B (12.31 → 8.10 s), and Qwen2.5-1.5B (8.77 → 5.22 s). OS caches and background downloads were not controlled.
- Zoo 5.5 notably improves text-chat objective results for Qwen3-VL-2B compared with Zoo 5.4. The 4B VLM is more careful about absent device access and often writes more coherent short stories, but is slower and does not win every factual task.
- Qwen3-1.7B has the highest objective score among the tested Hailo models, but its editorial score is low: correct facts do not imply honest device-state reporting or strong creative responses. Never treat a generated action confirmation as proof that an action ran.
- DeepSeek is poorly suited to this 128-output-token short-answer setup: reasoning often consumes the budget. Its low score is not a general assessment of unrestricted reasoning ability.

## Gemma4-E2B: CPU and Hailo assessed separately

| Model | Answers | Loads | Load s | TTFT DE / EN s | Decode token/s | File GiB | Hailo RAM GiB | Host RSS GiB | Objective points | Editorial points | Pending |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemma-4-E2B-it | 198 | 3 | 2.74 | 1.26 / 1.25 | 8.48 | 2.41 | — | 0.46 | 108/126 | 66/72 | 0 |
| Gemma4-E2B-Instruct | 198 | 3 | 13.48 | 0.52 / 0.45 | 5.67 | 3.11 | 3.78 | 0.08 | 79.5/126 | 59.25/72 | 0 |

**CPU/LiteRT:** strongest balanced result here: 108/126 objective points and 66/72 editorial points, about 8.48 token/s. Its first text takes about 1.26 s. Suitable for general text conversation on this CM5 when CPU resources are available. Its calendar mistakes remain; it is not universally correct.

**Hailo/native:** earlier first text (about 0.52 s DE / 0.45 s EN), but about 5.67 token/s, 79.5/126 objective and 59.25/72 editorial points. Several outputs contain residual markers, padding or attached `agma`; recognizable correct answers get 0.25 under the user-defined rubric. The cause is not isolated to tokenizer, conversion or decoder. Investigate these artifacts before relying on this path for exact structured output.

These are different LiteRT and HEF artifacts, not the same bit-identical model on two processors. The LiteRT export uses mixed 2/4/8-bit weights according to its model card; equivalent native quantization was not established. Different chat rendering, sampling implementations and numerical kernels may contribute, but their individual effects were not measured. Identical seed values across backends do not guarantee identical sampling.

[LiteRT model card](https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm)

Host RSS after load (about 0.46 GiB) is not total CPU inference memory: memory mapping and lazy loading make this measurement particularly incomplete. Hailo RAM includes the device baseline. Neither number is a peak or an apples-to-apples total-memory comparison. Power consumption and CPU utilization were not measured.

## Usage recommendations for this system

- **Balanced general text chat: Gemma4-E2B with LiteRT on CPU.** Best balance of factual/format and editorial results in this set, with about 8.5 token/s; account for host workload and verify factual answers.
- **Hailo factual/structured short answers: Qwen3-1.7B with Zoo 5.5 and runtime 5.5.** Highest Hailo objective score (112.5/126), around 4.77 token/s. Validate JSON and reject invented actions/states; its 9/72 editorial score prevents an unconditional general-chat recommendation.
- **Hailo with faster generation: Qwen2.5-Coder-1.5B.** About 8.33 token/s and 98.5/126 objective points. This is a short-answer/JSON result, not a coding benchmark; editorial behavior remains weak (16/72). Qwen2-1.5B gives more balanced editorial behavior (38/72) at similar speed, with lower objective points (90.5/126).
- **Hailo conversation with better limitation handling: trial Qwen3-VL-4B.** 105.5/126 objective and 59/72 editorial points; about 2.29 token/s and 6.95 GiB loaded device RAM. Use only if this latency/memory cost is acceptable. Vision quality was not tested.
- **Qwen3-VL-2B for lower memory/faster output than 4B, with strong guardrails.** Objective score 107/126 and about 4.88 token/s, but 0/72 editorial points in this catalog make it unsuitable as an unchecked device-control assistant.
- **Do not prefer Qwen3-4B just for size.** The final 5.5 run gives 98/126 objective points and 58/72 editorial points, but only about 2.10 token/s. On this workload it does not justify a default switch from smaller choices.
- **Gemma on Hailo: investigate output artifacts first.** It starts speaking sooner than the CPU export, but is slower afterwards and scores lower. Prefer the CPU export for current general text chat; no power-efficiency claim is supported.
- **Llama and DeepSeek:** Llama is fastest (~10 token/s) but low quality in this catalog (39/126); DeepSeek is constrained by the short output limit. Neither is the default choice for these questions.

## Method and limitations

Each full model: 3 fresh-process loads, 33 questions × 2 languages × 3 = 198 fresh-context requests. Temperature 0.1; seeds 1/2/3; output limit 128; context limit 2048 where configured. No images, actual tools or external weather data. One next artifact may be downloaded in the background; no two Hailo models run simultaneously.

User rubric v1.3: recognizable correct answers with corrupted output artifacts = 0.25 points and format 0; extra explanations violate an explicit answer-only restriction and get 0. Without that restriction a correct sentence is allowed. Normal recognized stop delimiters are stripped without penalty. Raw answers remain unchanged. Objective points and Codex editorial assessments are not combined into a fabricated single accuracy metric.

Only three repeated runs, overlapping questions, uncontrolled thermal/cache/system-load conditions and sequential experiment order. These are descriptive measurements, not confidence-tested rankings. TTFT is first nonempty text chunk; output is re-tokenized, so token/s need not equal internal decoder-token throughput. Download and native imports/device construction are excluded from load time.

[Scoring rubric](../benchmarks/catalog55/evaluation_rubric.md) · [Question catalog](../benchmarks/catalog55/questions.md) · [All run pages](runs/index.en.md)
