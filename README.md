# Hailo-10H LLM/VLM benchmark

**[Gesamtbewertung und Empfehlungen auf Deutsch](docs/overview.de.md)** · **[Overall assessment and recommendations in English](docs/overview.en.md)**

Reproducible text-chat measurements on a Raspberry Pi CM5 with an 8 GB Hailo-10H: runtime/firmware/PCIe-driver **5.4.0 and 5.5.0**, each tested against **Model Zoo 5.4 and 5.5**. Gemma4-E2B on LiteRT/CPU is reported separately from the native Hailo export.

## Ergebnisse / Results

| Runtime stack | Zoo 5.4 | Zoo 5.5 |
|---|---|---|
| 5.4.0 | [DE](docs/runs/runtime54-zoo54/README.de.md) / [EN](docs/runs/runtime54-zoo54/README.en.md) | [DE](docs/runs/runtime54-prefetch/README.de.md) / [EN](docs/runs/runtime54-prefetch/README.en.md) |
| 5.5.0 | [DE](docs/runs/runtime55-zoo54/README.de.md) / [EN](docs/runs/runtime55-zoo54/README.en.md) | [DE](docs/runs/runtime55-zoo55/README.de.md) / [EN](docs/runs/runtime55-zoo55/README.en.md) |

**Qwen3-4B is included in the final runtime 5.5 / Zoo 5.5 experiment**, including its three repetitions and all 198 answers. Original measurement provenance is retained inside that experiment.

- [Alle Testläufe einschließlich Vorabtests / all experiment pages](docs/runs/index.de.md), [English index](docs/runs/index.en.md). Each experiment also links to its individual repetitions.
- [Machine-readable comparison CSV](docs/comparison.csv), [JSON](docs/comparison.json).
- [Raw measurements, answers, logs, scoring histories and original archives](benchmarks/catalog55/results/).
- [Bilingual questions](benchmarks/catalog55/questions.md), [JSON](benchmarks/catalog55/questions.json), [scoring rubric](benchmarks/catalog55/evaluation_rubric.md).

**Latest scoring: `reference-checks-v1.4`.** Corrupted output with a recognizable correct answer gets **0.25 points and format 0**; an explanatory sentence gets **0** when only the answer was requested, and may get **1** when no such restriction exists. **E05 exception:** a clear statement that current weather data is unavailable is correct regardless of sentence count; generic refusals and fabricated weather do not qualify. Known normal stop delimiters are removed without penalty. Older immutable archives contain the scoring version recorded at their creation. Current overview/run pages use the latest v1.4 main-run assessments. Editorial judgments are Codex assessments, not a human panel or a second independent model.

## Kurzbewertung / Main takeaways

- **Gemma4-E2B on CPU/LiteRT** is the most balanced general text-chat option in this question set; native Hailo Gemma begins responding sooner but generates more slowly and has output artifacts.
- **Qwen3-1.7B on Hailo** leads objective short-answer points; its weak editorial/device-state behavior requires strong validation.
- **Qwen2.5-Coder-1.5B** offers faster Hailo generation with useful short-answer/JSON results. No coding-task quality was tested.
- **Qwen3-VL-4B** handles missing device access better than 2B in this catalog, at substantially higher memory use and latency. All VLM tests are **text-only**.

See the bilingual overviews for exact scores, limitations, Gemma CPU/Hailo separation and model-specific recommendations. These measurements do not establish image quality, power efficiency, true tool execution or general benchmark accuracy.

## Reproduce

Use a compatible Linux ARM64 Hailo-10H host, matching HailoRT native library, driver, firmware and vendor Python binding. The recorded host used Python 3.13, HailoRT 5.4/5.5, LiteRT-LM 0.17.1, Jinja2 3.1.6 and PyYAML 6.0.2. Install HailoRT from vendor packages; `requirements.txt` deliberately does not install or upgrade device firmware/driver.

```bash
python3 -m venv .venv --system-site-packages
.venv/bin/python -m pip install -r requirements.txt
# Optional CPU reference, in a compatible environment:
.venv/bin/python -m pip install litert-lm==0.17.1
# Stop any service owning the Hailo before running, e.g.:
sudo systemctl stop hailo-10h-services
# Every new measurement run needs its own result directory:
.venv/bin/python benchmarks/catalog55/run.py --release v5.5.0 \
  --repeats 3 --max-tokens 128 \
  --output benchmarks/catalog55/results/my-runtime55-zoo55
# To select the older Zoo artifacts on the SAME installed runtime:
.venv/bin/python benchmarks/catalog55/run.py --release v5.4.0 \
  --repeats 3 --max-tokens 128 \
  --output benchmarks/catalog55/results/my-runtime55-zoo54
```

The scripts do not upgrade the runtime. Keep at least 10 GB free and allow current/next artifact overlap. Artifact downloads are reused for three repetitions and deleted afterwards. `--local-model` preserves a pre-existing file. Seeds 1/2/3, temperature 0.1, 128 output tokens and fresh context are used; these are not controlled cold-cache runs. Default host request timeout is 300 seconds; inactivity timeout is 600 seconds.

```bash
# Offline checks; no model download or Hailo inference:
.venv/bin/python -m unittest discover -s benchmarks/catalog55 -p 'test_*.py'
# Re-score an existing main run (manual editorial judgments remain explicit):
.venv/bin/python benchmarks/catalog55/evaluate.py benchmarks/catalog55/results/runtime55-zoo55
.venv/bin/python benchmarks/catalog55/report.py benchmarks/catalog55/results/runtime55-zoo55
# Rebuild the published bilingual pages and comparison CSV/JSON:
.venv/bin/python scripts/build_docs.py
# Optional local read-only status page, manual refresh only:
.venv/bin/python benchmarks/catalog55/status_server.py --host 127.0.0.1 --port 8090
```

[Detailed original runner documentation](benchmarks/catalog55/README.md) · [Provenance and packaging changes](PROVENANCE.json) · [SHA256 manifest](MANIFEST.sha256)

All result data, raw answers and historical archives are retained. Model weights, LiteRT compiled caches, process-ID files and temporary downloads are excluded. The runner's prompt-rendering function was extracted unchanged from [hailo-10h-services](https://github.com/leonsio/hailo-10h-services), so the published benchmark can run without importing the entire service. Original archived snapshots retain their original imports and paths. Licensed under [Apache-2.0](LICENSE); model artifacts retain their upstream licenses.
