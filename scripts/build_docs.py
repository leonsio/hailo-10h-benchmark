#!/usr/bin/env python3
"""Generate bilingual reports from immutable measurements and v1.4 checks."""
import csv
import hashlib
import json
from pathlib import Path
from statistics import mean

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'benchmarks/catalog55/results'
DOCS=ROOT/'docs'
MAIN=['runtime54-zoo54','runtime54-prefetch','runtime55-zoo54','runtime55-zoo55']

def js(p,default=None):
    return json.loads(p.read_text()) if p.exists() else (default if default is not None else {})
def rows(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
def avg(vals):
    vals=[x for x in vals if x is not None];return mean(vals) if vals else None
def fmt(x): return '—' if x is None else f'{x:.2f}'
def gib(x): return fmt(x/2**30) if x is not None else '—'
def link(target,page):
    import os
    return Path(os.path.relpath(target,page.parent)).as_posix()
def aggregate(p,repeat=None):
    meta=js(p/'metadata.json');raw=rows(p/'answers.jsonl');loads=rows(p/'loads.jsonl');checks=rows(p/'answer_checks.jsonl');events=rows(p/'events.jsonl');sizes={x['model']:x for x in js(p/'model_sizes.json',[])}
    if repeat:
        raw=[r for r in raw if r['repeat']==repeat];loads=[r for r in loads if r['repeat']==repeat];checks=[r for r in checks if r['repeat']==repeat]
    result=[]
    for model in meta.get('models',[]):
        a=[r for r in raw if r['model']==model and r.get('status')=='ok'];l=[r for r in loads if r['model']==model and r.get('load_s') is not None];c=[r for r in checks if r['model']==model];o=[r for r in c if r.get('objective') and r.get('content_score') is not None and not r.get('needs_review')];q=[r for r in c if not r.get('objective') and 'manual_review' in r]
        errors=[str(r.get('error',r.get('event'))) for r in events if r.get('model')==model and r.get('event') in ('error','timeout','worker_exit') and r.get('returncode',1)!=0]
        result.append(dict(model=model,answers=len(a),loads=len(l),load=avg([r['load_s'] for r in l]),ttft_de=avg([r.get('ttft_s') for r in a if r['language']=='de']),ttft_en=avg([r.get('ttft_s') for r in a if r['language']=='en']),tps=avg([r.get('decode_tokens_per_s') for r in a]),file=sizes.get(model,{}).get('artifact_bytes'),ram=avg([r.get('hailo_ram_loaded_bytes') for r in l]),rss=avg([r.get('host_rss_loaded_bytes') for r in l]),points=sum(r['content_score'] for r in o),scored=len(o),editorial_points=sum(r.get('quality_score',float(bool(r.get('quality_pass')))) for r in q),editorial_n=len(q),pending=sum(bool(r.get('needs_review')) for r in c),errors=errors,status='ok' if a else 'error',graded=bool(c)))
    return result

def table(data,en=False):
    out=['| Model | Answers | Loads | Load s | TTFT DE / EN s | Decode token/s | File GiB | Hailo RAM GiB | Host RSS GiB | Objective points | Editorial points | Pending |' if en else '| Modell | Antworten | Ladungen | Laden s | TTFT DE / EN s | Decode Token/s | Datei GiB | Hailo-RAM GiB | Host-RSS GiB | Objektive Punkte | Redaktionelle Punkte | Offen |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for r in data:
        out.append('| '+' | '.join([r['model'],str(r['answers']),str(r['loads']),fmt(r['load']),fmt(r['ttft_de'])+' / '+fmt(r['ttft_en']),fmt(r['tps']),gib(r['file']),gib(r['ram']),gib(r['rss']),f"{r['points']:g}/{r['scored']}" if r['scored'] else '—',f"{r['editorial_points']:g}/{r['editorial_n']}" if r['editorial_n'] else '—',str(r['pending']) if r['graded'] else '—'])+' |')
    return out

def run_pages():
    inventory=[]
    for p in sorted(BASE.iterdir()):
        if not (p/'metadata.json').exists():continue
        meta=js(p/'metadata.json');data=aggregate(p)
        main=p.name in MAIN
        inventory.append(dict(name=p.name,main=main,metadata=meta,models=data))
        for en in (False,True):
            lang='en' if en else 'de';page=DOCS/'runs'/p.name/f'README.{lang}.md';page.parent.mkdir(parents=True,exist_ok=True)
            title=('Run' if en else 'Testlauf')+' · '+p.name
            text=[f'# {title}','',f"[Deutsch](README.de.md) · [English](README.en.md) · [{'Overview' if en else 'Gesamtübersicht'}]({link(DOCS/('overview.en.md' if en else 'overview.de.md'),page)})",'',f"Runtime: **{meta.get('runtime','unknown')}** · Zoo: **{meta.get('release','not recorded')}** · Start: {meta.get('started','—')}",'',('Main experiment.' if main else 'Diagnostic, preflight, interrupted or failed attempt. Excluded from headline comparisons. Its original settings may differ and legacy correctness files are not promoted to v1.4.') if en else ('Hauptexperiment.' if main else 'Diagnose-, Vorab-, abgebrochener oder fehlgeschlagener Lauf. Nicht in die Gesamtvergleichswerte eingemischt. Einstellungen können abweichen; alte Bewertungsdateien werden nicht als v1.4 ausgegeben.'),'']
            text+=table(data,en)
            text+=['',('Three means are not controlled cold starts. RAM is measured after loading, not peak inference memory. Missing values are not zeros. Objective and editorial points remain separate; 0 pending does not mean all answers passed.' if en else 'Mittelwerte sind keine kontrollierten Kaltstarts. RAM wird nach dem Laden gemessen, nicht als Inferenzspitze. Fehlende Werte sind keine Nullen. Objektive und redaktionelle Punkte bleiben getrennt; 0 offene Prüfungen bedeutet nicht, dass alle Antworten bestanden haben.'),'']
            if meta.get('integrated_model_measurements'):text += [('Qwen3-4B is included in this experiment: 3 loads and 198 answers. Its measurements were collected later with background prefetch disabled; questions and inference settings match. Source records and the original download failure are retained under provenance/.' if en else 'Qwen3-4B ist in diesen Lauf integriert: 3 Ladungen und 198 Antworten. Die Messungen erfolgten später mit deaktiviertem Vorladen; Fragen und Inferenzparameter stimmen überein. Herkunftsdaten und der ursprüngliche Downloadfehler bleiben unter provenance/ erhalten.'),'']
            errors=[r for r in data if r['errors']]
            if errors:
                text+=[('## Errors' if en else '## Fehler'),'']
                for r in errors:text += [f"- **{r['model']}**: "+'; '.join(dict.fromkeys(r['errors']))]
                text+=['']
            text += [('## Repetitions' if en else '## Wiederholungen'),'']
            for repeat in range(1,meta.get('repeats',3)+1):
                rp=page.parent/f'repeat-{repeat}.{lang}.md'
                text += [f'- [Run {repeat}]({rp.name})' if en else f'- [Durchlauf {repeat}]({rp.name})']
                rp.write_text('\n'.join([f'# {title} · {repeat}','',f'[← {title}]({page.name})','',*table(aggregate(p,repeat),en),'',('Per-repetition measurements; no inferred zeros for missing data.' if en else 'Einzelwerte dieser Wiederholung; fehlende Messungen werden nicht mit Null aufgefüllt.')])+'\n')
            text+=['',('## Original data' if en else '## Originaldaten'),'']
            for f in ('metadata.json','questions.json','answers.jsonl','loads.jsonl','events.jsonl','answer_checks.jsonl','manual_reviews.json','correctness_summary.csv','evaluation_metadata.json','report.md','evaluation_history','provenance'):
                if (p/f).exists():text += [f'- [{f}]({link(p/f,page)})']
            page.write_text('\n'.join(text)+'\n')
    return inventory

def overview(inventory,en=False):
    lang='en' if en else 'de';page=DOCS/f'overview.{lang}.md'
    items={x['name']:x for x in inventory};runs={name:{r['model']:r for r in items[name]['models']} for name in MAIN}
    names=list(runs['runtime55-zoo55'])
    title='Hailo-10H benchmark: overall assessment' if en else 'Hailo-10H-Benchmark: Gesamtbewertung'
    text=[f'# {title}','', '[Deutsch](overview.de.md) · [English](overview.en.md) · [Repository](../README.md)','',('Data: 4 runtime/Zoo combinations; Qwen3-4B is integrated into the final 5.5/5.5 experiment. Raspberry Pi CM5, about 15 GiB host RAM and an 8 GB Hailo-10H. All headline scores use **reference-checks-v1.4**; previous reports/archives may contain superseded scores.' if en else 'Datengrundlage: 4 Kombinationen aus Runtime und Model Zoo; Qwen3-4B ist in den letzten 5.5/5.5-Lauf integriert. Raspberry Pi CM5, etwa 15 GiB Host-RAM und Hailo-10H mit 8 GB. Alle hier dargestellten Hauptbewertungen verwenden **reference-checks-v1.4**; ältere Berichte/Archive können frühere Punktzahlen enthalten.'),'',('## Experiment matrix' if en else '## Versuchsmatrix'),'','| Runtime / firmware / driver | Model Zoo 5.4 | Model Zoo 5.5 |','|---|---|---|',f"| 5.4.0 | [Results](runs/runtime54-zoo54/README.{lang}.md) | [Results](runs/runtime54-prefetch/README.{lang}.md) |",f"| 5.5.0 | [Results](runs/runtime55-zoo54/README.{lang}.md) | [Results](runs/runtime55-zoo55/README.{lang}.md) |",'',('Runtime means the entire updated firmware/runtime/driver stack. These experiments do not isolate the PCIe driver alone.' if en else '„Runtime“ bezeichnet hier die gemeinsam aktualisierten Komponenten Firmware, Runtime, Python-Binding und PCIe-Treiber. Der Effekt des Treibers allein wurde nicht isoliert.'),'',('## Quality across all four combinations' if en else '## Antwortbewertung über alle vier Kombinationen'),'','| Model | RT5.4 / Zoo5.4 | RT5.4 / Zoo5.5 | RT5.5 / Zoo5.4 | RT5.5 / Zoo5.5 |','|---|---:|---:|---:|---:|']
    for model in names:
        vals=[]
        for name in MAIN:
            r=runs[name].get(model);vals.append(f"{r['points']:g}/{r['scored']}" if r and r['scored'] else '—')
        text.append('| '+model+' | '+' | '.join(vals)+' |')
    text+=['',('126 possible objective points per full model run; 72 editorial tasks are assessed separately. Repeated/related questions mean this is not a general benchmark accuracy estimate.' if en else 'Pro vollständigem Modelllauf sind 126 objektive Punkte möglich; 72 redaktionelle Aufgaben werden getrennt bewertet. Ähnliche und wiederholte Fragen machen dies nicht zu einer allgemeinen Modellgenauigkeit.'),'',('## Decode throughput across all four combinations' if en else '## Decode-Durchsatz über alle vier Kombinationen'),'','| Model | RT5.4 / Zoo5.4 | RT5.4 / Zoo5.5 | RT5.5 / Zoo5.4 | RT5.5 / Zoo5.5 |','|---|---:|---:|---:|---:|']
    for model in names:text.append('| '+model+' | '+' | '.join(fmt(runs[name].get(model,{}).get('tps')) for name in MAIN)+' |')
    text+=['',('Token/s, arithmetic means. CPU Gemma uses the same LiteRT artifact in every column; its placement does not make it a Zoo model.' if en else 'Token/s als arithmetische Mittelwerte. CPU-Gemma verwendet in jeder Spalte dasselbe LiteRT-Artefakt; die Zuordnung zu den Läufen macht es nicht zu einem Model-Zoo-Modell.'),'',('## Runtime 5.5 with Zoo 5.5: full picture' if en else '## Runtime 5.5 mit Zoo 5.5: Gesamtbild'),'']+table(list(runs['runtime55-zoo55'].values()),en)
    text+=['',('## Findings' if en else '## Einordnung'),'']
    findings_en=[
        'Updating the stack mainly improves model compatibility and load times. Gemma4-E2B and Qwen3-VL-4B now run, and the completed Qwen3-4B measurements are included in the final 5.5 experiment. Their runtime-5.4 load failures provide no valid model-quality baseline.',
        'For the nine shared native models and CPU reference, all 1,980 matched raw answers of the Zoo-5.5 runs are identical across runtime 5.4/5.5. Quality changes therefore come from the Zoo artifacts or revised scoring, not an observed change in answers caused by the runtime update.',
        'Most shared native models gain only about 1–4% decode throughput with runtime 5.5; CPU reference variability is about 1.5%. Treat these small gains cautiously. Larger load-time reductions include Qwen3-VL-2B (16.03 → 7.96 s), Qwen2-VL-2B (12.31 → 8.10 s), and Qwen2.5-1.5B (8.77 → 5.22 s). OS caches and background downloads were not controlled.',
        'Zoo 5.5 notably improves text-chat objective results for Qwen3-VL-2B compared with Zoo 5.4. The 4B VLM is more careful about absent device access and often writes more coherent short stories, but is slower and does not win every factual task.',
        'Qwen3-1.7B has the highest objective score among the tested Hailo models, but its editorial score is low: correct facts do not imply honest device-state reporting or strong creative responses. Never treat a generated action confirmation as proof that an action ran.',
        'DeepSeek is poorly suited to this 128-output-token short-answer setup: reasoning often consumes the budget. Its low score is not a general assessment of unrestricted reasoning ability.'
    ]
    findings_de=[
        'Das Upgrade verbessert vor allem Modellkompatibilität und Ladezeiten. Gemma4-E2B und Qwen3-VL-4B laufen jetzt; die erfolgreichen Qwen3-4B-Messungen sind in den letzten 5.5-Lauf integriert. Die Ladefehler unter Runtime 5.4 sind keine gültige Grundlage für einen Qualitätsvergleich dieser Modelle.',
        'Bei den neun gemeinsamen nativen Modellen und der CPU-Referenz sind alle 1.980 zugeordneten Rohantworten der Zoo-5.5-Läufe unter Runtime 5.4/5.5 identisch. Qualitätsänderungen entstehen damit durch Katalogartefakte oder geänderte Bewertungsregeln, nicht durch eine beobachtete Antwortänderung infolge des Runtime-Upgrades.',
        'Die meisten gemeinsamen nativen Modelle gewinnen mit Runtime 5.5 nur etwa 1–4 % Decode-Durchsatz; die CPU-Referenz schwankt selbst um etwa 1,5 %. Diese kleinen Gewinne vorsichtig bewerten. Deutlichere Ladezeitverkürzungen: Qwen3-VL-2B (16,03 → 7,96 s), Qwen2-VL-2B (12,31 → 8,10 s) und Qwen2.5-1.5B (8,77 → 5,22 s). Dateicaches und Hintergrunddownloads waren nicht kontrolliert.',
        'Zoo 5.5 verbessert insbesondere die objektiven Textchat-Ergebnisse von Qwen3-VL-2B gegenüber Zoo 5.4. Das 4B-VLM geht mit fehlendem Gerätezugriff vorsichtiger um und schreibt oft kohärentere Kurzgeschichten, ist aber langsamer und gewinnt nicht jede Sachaufgabe.',
        'Qwen3-1.7B erreicht unter den getesteten Hailo-Modellen die höchsten objektiven Punkte, hat aber eine niedrige redaktionelle Bewertung. Richtige Fakten garantieren weder ehrliche Gerätezustände noch gute kreative Antworten. Eine generierte Ausführungsbestätigung ist kein Nachweis einer ausgeführten Aktion.',
        'DeepSeek passt schlecht zum hier verwendeten 128-Token-Kurzantworttest: Der Denktext verbraucht oft das Budget. Die niedrige Bewertung ist keine allgemeine Bewertung unbegrenzt langer Denkaufgaben.'
    ]
    text+=['- '+x for x in (findings_en if en else findings_de)]
    text+=['',('## Gemma4-E2B: CPU and Hailo assessed separately' if en else '## Gemma4-E2B: CPU und Hailo getrennt bewertet'),'']
    g=[runs['runtime55-zoo55'][n] for n in ('gemma-4-E2B-it','Gemma4-E2B-Instruct')]
    text+=table(g,en)
    text+=['',('**CPU/LiteRT:** strongest balanced result here: 108/126 objective points and 66/72 editorial points, about 8.48 token/s. Its first text takes about 1.26 s. Suitable for general text conversation on this CM5 when CPU resources are available. Its calendar mistakes remain; it is not universally correct.' if en else '**CPU/LiteRT:** das ausgewogenste Ergebnis in diesem Test: 108/126 objektive und 66/72 redaktionelle Punkte bei etwa 8,48 Token/s. Erster Text nach etwa 1,26 s. Für allgemeinen Textchat auf diesem CM5 geeignet, wenn CPU-Ressourcen verfügbar sind. Kalenderfehler bleiben; es ist nicht allgemein fehlerfrei.'),'',('**Hailo/native:** earlier first text (about 0.52 s DE / 0.45 s EN), but about 5.67 token/s, 79.5/126 objective and 60/72 editorial points. Several outputs contain residual markers, padding or attached `agma`; recognizable correct answers get 0.25 under the user-defined rubric. The cause is not isolated to tokenizer, conversion or decoder. Investigate these artifacts before relying on this path for exact structured output.' if en else '**Hailo/nativ:** früherer erster Text (etwa 0,52 s DE / 0,45 s EN), aber etwa 5,67 Token/s, 79,5/126 objektive und 60/72 redaktionelle Punkte. Mehrere Ausgaben enthalten Restmarker, Padding oder angehängtes `agma`; erkennbare richtige Antworten erhalten nach Nutzerregel 0,25 Punkte. Ob Tokenizer, Konvertierung oder Decoder die Ursache sind, wurde nicht isoliert. Vor Nutzung für exakte strukturierte Ausgaben sollten diese Artefakte untersucht werden.'),'',('These are different LiteRT and HEF artifacts, not the same bit-identical model on two processors. The LiteRT export uses mixed 2/4/8-bit weights according to its model card; equivalent native quantization was not established. Different chat rendering, sampling implementations and numerical kernels may contribute, but their individual effects were not measured. Identical seed values across backends do not guarantee identical sampling.' if en else 'Es handelt sich um unterschiedliche LiteRT- und HEF-Artefakte, nicht um ein bitgleiches Modell auf zwei Prozessoren. Der LiteRT-Export verwendet laut Modellkarte gemischte 2-/4-/8-Bit-Gewichte; eine gleiche native Quantisierung ist nicht nachgewiesen. Unterschiedliche Chat-Aufbereitung, Sampler und Rechenkerne können beitragen; ihr Einzeleffekt wurde nicht gemessen. Gleiche Seeds garantieren über Backends hinweg keine gleichen Stichproben.'),'','[LiteRT model card](https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm)','',('Host RSS after load (about 0.46 GiB) is not total CPU inference memory: memory mapping and lazy loading make this measurement particularly incomplete. Hailo RAM includes the device baseline. Neither number is a peak or an apples-to-apples total-memory comparison. Power consumption and CPU utilization were not measured.' if en else 'Host-RSS nach dem Laden (etwa 0,46 GiB) ist nicht der gesamte Speicherverbrauch der CPU-Inferenz: Memory-Mapping und verzögertes Laden machen diesen Messpunkt besonders unvollständig. Hailo-RAM enthält die Geräte-Grundbelegung. Keiner der Werte ist ein Spitzenwert oder ein direkt vergleichbarer Gesamtspeicherbedarf. Stromverbrauch und CPU-Auslastung wurden nicht gemessen.'),'',('## Usage recommendations for this system' if en else '## Nutzungsempfehlungen für dieses System'),'']
    recommendations_en=[
        '**Balanced general text chat: Gemma4-E2B with LiteRT on CPU.** Best balance of factual/format and editorial results in this set, with about 8.5 token/s; account for host workload and verify factual answers.',
        '**Hailo factual/structured short answers: Qwen3-1.7B with Zoo 5.5 and runtime 5.5.** Highest Hailo objective score (112.5/126), around 4.77 token/s. Validate JSON and reject invented actions/states; its 9/72 editorial score prevents an unconditional general-chat recommendation.',
        '**Hailo with faster generation: Qwen2.5-Coder-1.5B.** About 8.33 token/s and 98.5/126 objective points. This is a short-answer/JSON result, not a coding benchmark; editorial behavior remains weak (16/72). Qwen2-1.5B gives more balanced editorial behavior (40/72) at similar speed, with lower objective points (90.5/126).',
        '**Hailo conversation with better limitation handling: trial Qwen3-VL-4B.** 105.5/126 objective and 59/72 editorial points; about 2.29 token/s and 6.95 GiB loaded device RAM. Use only if this latency/memory cost is acceptable. Vision quality was not tested.',
        '**Qwen3-VL-2B for lower memory/faster output than 4B, with strong guardrails.** Objective score 107/126 and about 4.88 token/s, but 0/72 editorial points in this catalog make it unsuitable as an unchecked device-control assistant.',
        '**Do not prefer Qwen3-4B just for size.** The final 5.5 run gives 98/126 objective points and 58/72 editorial points, but only about 2.10 token/s. On this workload it does not justify a default switch from smaller choices.',
        '**Gemma on Hailo: investigate output artifacts first.** It starts speaking sooner than the CPU export, but is slower afterwards and scores lower. Prefer the CPU export for current general text chat; no power-efficiency claim is supported.',
        '**Llama and DeepSeek:** Llama is fastest (~10 token/s) but low quality in this catalog (39/126); DeepSeek is constrained by the short output limit. Neither is the default choice for these questions.'
    ]
    recommendations_de=[
        '**Ausgewogener allgemeiner Textchat: Gemma4-E2B mit LiteRT auf CPU.** In diesem Katalog das beste Verhältnis von Sach-/Formatpunkten und redaktionellen Ergebnissen bei etwa 8,5 Token/s. Host-Auslastung berücksichtigen und Fakten weiterhin prüfen.',
        '**Sachliche/strukturierte Kurzantworten auf Hailo: Qwen3-1.7B mit Zoo 5.5 und Runtime 5.5.** Höchste objektive Hailo-Bewertung (112,5/126), etwa 4,77 Token/s. JSON validieren und erfundene Aktionen/Zustände ablehnen; 9/72 redaktionelle Punkte erlauben keine uneingeschränkte Chatempfehlung.',
        '**Hailo mit schneller Generierung: Qwen2.5-Coder-1.5B.** Etwa 8,33 Token/s und 98,5/126 objektive Punkte. Das ist ein Kurzantwort-/JSON-Ergebnis, kein Programmierbenchmark; redaktionell bleibt es schwach (16/72). Qwen2-1.5B ist bei ähnlichem Tempo redaktionell ausgewogener (40/72), hat aber weniger objektive Punkte (90,5/126).',
        '**Hailo-Chat mit besserem Umgang mit fehlenden Zugriffsmöglichkeiten: Qwen3-VL-4B erproben.** 105,5/126 objektive und 59/72 redaktionelle Punkte; etwa 2,29 Token/s und 6,95 GiB belegter Gerätespeicher. Nur sinnvoll, wenn Latenz und Speicherbedarf passen. Bildqualität wurde nicht geprüft.',
        '**Qwen3-VL-2B für weniger Speicher und mehr Tempo als 4B, mit strenger Absicherung.** 107/126 objektive Punkte und etwa 4,88 Token/s; 0/72 redaktionelle Punkte in diesem Katalog sprechen gegen einen ungeprüften Einsatz als Gerätesteuerungsassistent.',
        '**Qwen3-4B nicht allein wegen der Größe bevorzugen.** Der letzte 5.5-Lauf liefert 98/126 objektive und 58/72 redaktionelle Punkte, aber nur etwa 2,10 Token/s. Dieser Test rechtfertigt keinen generellen Wechsel von kleineren Modellen.',
        '**Gemma auf Hailo: zuerst Ausgabeartefakte untersuchen.** Der erste Text kommt früher als beim CPU-Export, die weitere Generierung ist aber langsamer und die Bewertung niedriger. Für aktuellen allgemeinen Textchat den CPU-Export bevorzugen; eine Energieeffizienzempfehlung ist nicht durch Messungen gedeckt.',
        '**Llama und DeepSeek:** Llama ist am schnellsten (~10 Token/s), aber in diesem Katalog schwach (39/126). DeepSeek wird durch die kurze Ausgabelänge eingeschränkt. Für diese Aufgaben sind beide keine Standardempfehlung.'
    ]
    text+=['- '+x for x in (recommendations_en if en else recommendations_de)]
    text+=['',('## Method and limitations' if en else '## Methodik und Grenzen'),'']
    text += [('Each full model: 3 fresh-process loads, 33 questions × 2 languages × 3 = 198 fresh-context requests. Temperature 0.1; seeds 1/2/3; output limit 128; context limit 2048 where configured. No images, actual tools or external weather data. One next artifact may be downloaded in the background; no two Hailo models run simultaneously.' if en else 'Je vollständigem Modell: 3 Ladungen in frischen Prozessen, 33 Fragen × 2 Sprachen × 3 = 198 Anfragen mit frischem Kontext. Temperatur 0,1; Seeds 1/2/3; Ausgabelimit 128; Kontextlimit 2048 soweit konfiguriert. Keine Bilder, echten Tools oder externen Wetterdaten. Das nächste Artefakt kann im Hintergrund geladen werden; nie zwei Hailo-Modelle gleichzeitig.'),'',('User rubric v1.4: recognizable correct answers with corrupted output artifacts = 0.25 points and format 0; extra explanations violate an explicit answer-only restriction and get 0. Without that restriction a correct sentence is allowed. For E05, a clear statement that current weather data is unavailable does not need three sentences. Generic refusals or fabricated weather do not qualify. Normal recognized stop delimiters are stripped without penalty. Raw answers remain unchanged. Objective points and Codex editorial assessments are not combined into a fabricated single accuracy metric.' if en else 'Nutzerregel v1.4: erkennbare richtige Antworten mit beschädigten Ausgabe-Artefakten = 0,25 Punkte und Format 0; zusätzliche Erklärung bei ausdrücklicher Kurzantwortvorgabe = 0. Ohne diese Vorgabe ist ein richtiger Satz erlaubt. Bei E05 entfällt die Drei-Satz-Vorgabe für einen klaren Hinweis auf fehlende aktuelle Wetterdaten. Bloße Ablehnung und erfundenes Wetter zählen nicht als richtige Antwort. Reguläre erkannte Stopmarker werden ohne Abzug entfernt. Rohantworten bleiben unverändert. Objektive Punkte und redaktionelle Codex-Sichtung werden nicht zu einer erfundenen Gesamtgenauigkeit vermischt.'),'',('Only three repeated runs, overlapping questions, uncontrolled thermal/cache/system-load conditions and sequential experiment order. These are descriptive measurements, not confidence-tested rankings. TTFT is first nonempty text chunk; output is re-tokenized, so token/s need not equal internal decoder-token throughput. Download and native imports/device construction are excluded from load time.' if en else 'Nur drei Wiederholungen, ähnliche Fragen, nicht kontrollierte Temperatur-/Cache-/Lastbedingungen und zeitlich aufeinanderfolgende Experimente. Die Werte sind beschreibend, keine statistisch abgesicherten Ranglisten. TTFT ist der erste nichtleere Textchunk; Ausgaben werden nachtokenisiert, daher ist Token/s nicht zwingend der interne Decoder-Durchsatz. Download sowie native Imports/Geräteerzeugung sind von der Ladezeit ausgenommen.'),'',f"[{'Scoring rubric' if en else 'Bewertungsregeln'}](../benchmarks/catalog55/evaluation_rubric.md) · [{'Question catalog' if en else 'Fragenkatalog'}](../benchmarks/catalog55/questions.md) · [{'All run pages' if en else 'Alle Testlaufseiten'}](runs/index.{lang}.md)"]
    page.write_text('\n'.join(text)+'\n')
    return runs

def main():
    DOCS.mkdir(exist_ok=True)
    inventory=run_pages();runs=None
    for en in (False,True):
        lang='en' if en else 'de';runs=overview(inventory,en)
        page=DOCS/'runs'/f'index.{lang}.md'
        text=['# '+('All runs' if en else 'Alle Testläufe'),'']
        for item in inventory:
            text.append(f"- [{item['name']}]({item['name']}/README.{lang}.md)"+(' — main' if item['main'] else ' — diagnostic / historical'))
        page.write_text('\n'.join(text)+'\n')
    flat=[dict(experiment=name,**r) for name,data in runs.items() for r in data.values()]
    (DOCS/'comparison.json').write_text(json.dumps(flat,ensure_ascii=False,indent=2)+'\n')
    with (DOCS/'comparison.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
    print('Run pages:',len(inventory),'experiments; bilingual repeat pages generated.')

if __name__=='__main__':main()
