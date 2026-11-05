"""Compare completed Zoo artifact runs on the same runtime; preserve raw results."""
import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results' / 'comparison-runtime54'
DIRS = [ROOT / 'results' / n for n in ('runtime54-zoo54', 'runtime54-prefetch')]

def read(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]

def key(r):
    return r['model'], r['repeat'], r['question'], r['language']

def main():
    OUT.mkdir(exist_ok=True)
    data = []
    provenance = {}
    for p in DIRS:
        meta = json.loads((p/'metadata.json').read_text())
        answers = read(p/'answers.jsonl')
        checks = read(p/'answer_checks.jsonl')
        assert len({key(r) for r in answers}) == len(answers), 'Duplicate measurements'
        assert all(r['status'] == 'ok' for r in answers), 'Inspect technical errors'
        data.append(dict(meta=meta, answers=answers, checks={key(r):r for r in checks},
                         loads=read(p/'loads.jsonl'), sizes={r['model']:r for r in json.loads((p/'model_sizes.json').read_text())}))
        provenance[p.name] = {f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in ('metadata.json','answers.jsonl','loads.jsonl','answer_checks.jsonl')}
    a,b=data
    for field in ('runtime','questions_sha256','repeats','max_tokens','temperature','context_tokens','prefetch','optimize_memory_on_device'):
        assert a['meta'][field] == b['meta'][field], f'Incompatible {field}'
    models = [m for m in a['meta']['models'] if m in b['meta']['models']]
    result=[]; changes=[]
    for m in models:
        row={'model':m}
        aa=[{key(r):r for r in d['answers'] if r['model']==m} for d in data]
        assert len(aa[0]) == len(aa[1]) == 198
        same=sum(aa[0][k]['answer']==aa[1][k]['answer'] for k in aa[0])
        row['identical_raw_answers']=same
        for label,d in zip(('54','55'),data):
            ars=[r for r in d['answers'] if r['model']==m]
            loads=[r['load_s'] for r in d['loads'] if r['model']==m and 'load_s' in r]
            assert len(loads)==3
            row[f'load_{label}']=mean(loads)
            row[f'load_range_{label}']=[min(loads),max(loads)]
            for lang in ('de','en'):
                for metric in ('ttft_s','decode_tokens_per_s'):
                    row[f'{metric}_{lang}_{label}']=mean(r[metric] for r in ars if r['language']==lang and r.get(metric) is not None)
            row[f'decode_{label}']=mean(r['decode_tokens_per_s'] for r in ars if r.get('decode_tokens_per_s') is not None)
            row[f'decode_repeat_means_{label}']=[mean(r['decode_tokens_per_s'] for r in ars if r['repeat']==rep and r.get('decode_tokens_per_s') is not None) for rep in (1,2,3)]
            for field in ('artifact_bytes','hailo_ram_loaded_bytes_mean','hailo_ram_delta_bytes_mean','host_rss_loaded_bytes_mean'):
                row[f'{field}_{label}']=d['sizes'][m][field]
            checks=[r for r in d['checks'].values() if r['model']==m]
            objective=[r for r in checks if r['objective'] and r.get('content_score') is not None and not r.get('needs_review')]
            row[f'objective_points_{label}']=sum(r['content_score'] for r in objective)
            row[f'objective_scored_{label}']=len(objective)
            row[f'review_pending_{label}']=sum(bool(r.get('needs_review')) for r in checks)
        pairs=[(a['checks'][k],b['checks'][k]) for k in aa[0] if a['checks'][k]['objective'] and all(d['checks'][k].get('content_score') is not None and not d['checks'][k].get('needs_review') for d in data)]
        row['paired_objective_n']=len(pairs)
        for label,i in (('54',0),('55',1)):
            row[f'paired_objective_points_{label}']=sum(pair[i]['content_score'] for pair in pairs)
        for x,y in pairs:
            if x['content_score']!=y['content_score']:
                changes.append(dict(model=m,repeat=x['repeat'],question=x['question'],language=x['language'],score54=x['content_score'],score55=y['content_score'],answer54=aa[0][key(x)]['answer'],answer55=aa[1][key(y)]['answer']))
        row['decode_change_percent']=100*(row['decode_55']/row['decode_54']-1)
        row['load_change_percent']=100*(row['load_55']/row['load_54']-1)
        result.append(row)
    (OUT/'comparison.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    with (OUT/'comparison.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(result[0]));writer.writeheader();writer.writerows(result)
    (OUT/'changed_objective_answers.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False)+'\n')
    (OUT/'provenance.json').write_text(json.dumps(dict(created=datetime.now().astimezone().isoformat(),sources=provenance),indent=2)+'\n')
    lines=['# Vergleich Model Zoo 5.4 und 5.5 auf HailoRT 5.4','',f'Erstellt: {datetime.now().astimezone().isoformat()}. Beide technischen Läufe sind abgeschlossen und separat archiviert. Dieser Bericht ergänzt die Archive, ohne sie zu verändern.','', '## Geschwindigkeit und Laden','', 'Mittelwerte von jeweils 198 Antworten und drei Ladungen. Positive Änderung bei Token/s bedeutet schneller mit Zoo 5.5; negative Änderung bei Ladezeit bedeutet kürzer.','', '| Modell | Token/s 5.4 | Token/s 5.5 | Änderung | Laden 5.4 s | Laden 5.5 s | Änderung |','|---|---:|---:|---:|---:|---:|---:|']
    for r in result:
        lines.append(f"| {r['model']} | {r['decode_54']:.2f} | {r['decode_55']:.2f} | {r['decode_change_percent']:+.1f} % | {r['load_54']:.2f} | {r['load_55']:.2f} | {r['load_change_percent']:+.1f} % |")
    lines+=['','## Speicher','', 'Gesamte Hailo-Belegung unmittelbar nach Laden; keine Inferenzspitzen. GiB = 2^30 Bytes. CPU-RSS ist ebenfalls nur der Messpunkt nach dem Laden. Delta gegenüber Ausgangsbelegung steht zusätzlich in comparison.json.','', '| Modell | Datei GiB 5.4 → 5.5 | Hailo-RAM GiB 5.4 → 5.5 |','|---|---:|---:|']
    for r in result:
        fmt=lambda field,label: '—' if r[f'{field}_{label}'] is None else f"{r[f'{field}_{label}']/2**30:.2f}"
        lines.append(f"| {r['model']} | {fmt('artifact_bytes','54')} → {fmt('artifact_bytes','55')} | {fmt('hailo_ram_loaded_bytes_mean','54')} → {fmt('hailo_ram_loaded_bytes_mean','55')} |")
    lines+=['','## Antwortqualität','', 'Der direkte Vergleich verwendet ausschließlich dieselben objektiven Aufgaben, die in beiden Läufen bereits bewertet sind. Dadurch verzerren offene Fälle nicht den Nenner. Punkte enthalten Teilgutschriften. Identische Rohantworten beziehen sich auf gleiche Frage, Sprache und Wiederholung.','', '| Modell | Gemeinsame Aufgaben | Punkte 5.4 | Punkte 5.5 | Gleiche Rohantworten /198 | Offene Prüfungen 5.4 / 5.5 |','|---|---:|---:|---:|---:|---:|']
    for r in result:
        lines.append(f"| {r['model']} | {r['paired_objective_n']} | {r['paired_objective_points_54']:g} | {r['paired_objective_points_55']:g} | {r['identical_raw_answers']} | {r['review_pending_54']} / {r['review_pending_55']} |")
    lines+=['','## Einordnung','', 'Der stärkste Geschwindigkeitsgewinn liegt bei Qwen2-VL-2B: rund 8 % mehr Decode-Token/s und rund 19 % kürzere TTFT in beiden Sprachen. Zugleich steigen die objektiven Punkte von 94,5 auf 99 von 126. Qwen3-VL-2B verbessert seine objektiven Punkte deutlich von 86 auf 110 von 126, während der Durchsatz nur rund 2 % steigt; die Ladezeit steigt leicht. Beide Ergebnisse betreffen Textchat, nicht Bildverstehen.','','Die Function-Calling-Variante benötigt mit Zoo 5.5 erheblich weniger Datei- und Gerätespeicher und lädt schneller. Die objektiven Aufgaben verbessern sich im gemeinsamen bewerteten Teil. Das ist kein Nachweis zuverlässiger Werkzeugaufrufe: Es wurden keine echten Tool-Schemata und Geräteaktionen getestet, und redaktionelle Prüfungen sind teilweise offen.','','Bei DeepSeek, Coder, Qwen2, Qwen2.5, Llama und Qwen3 bleiben die objektiven Punktzahlen gleich. Geschwindigkeit ändert sich meist um weniger als 2 %. Diese kleinen Abweichungen werden angesichts der CPU-Referenz und fehlender randomisierter Laufreihenfolge nicht als belastbare Verbesserungen gewertet. Qwen2 und Qwen2.5 laden mit Zoo 5.5 deutlich schneller.','','Die Gemma4-CPU-Referenz verwendet in beiden Durchgängen dasselbe Artefakt und ist kein Zoo-Versionsvergleich. Ihre Schwankungen liefern einen Hinweis auf Messvariabilität: rund 1 % beim Durchsatz und rund 9 % bei der Ladezeit. Bei sechs gemeinsamen Hailo-Modellen und der CPU-Referenz sind sämtliche 198 Rohantworten je Modell sogar wortgleich. Unterschiede bestehen bei Qwen2-VL, Qwen3-VL und Function-Calling. Bei der CPU-Referenz liegen die einzelnen Ladezeiten zwischen etwa 0,41 und 8,80 Sekunden; der Mittelwert verdeckt hier starke Cache-/Initialisierungseffekte.','','Drei neue Zoo-5.5-Hailo-Modelle (Qwen3-4B, Qwen3-VL-4B, Gemma4-E2B) scheiterten beim Laden. Sie besitzen keine Zoo-5.4-Vergleichszeile und werden nicht in Qualitäts- oder Geschwindigkeitsranglisten eingerechnet.','','## Grenzen und Reproduzierbarkeit','', 'Beide Läufe nutzen HailoRT/Firmware 5.4.0, denselben Fragen-Hash, drei Wiederholungen, Temperatur 0,1, 128 Ausgabetokens und neuen Kontext je Frage. Diese Metadaten wurden automatisch auf Übereinstimmung geprüft. Unterschiede können Modellgewichte, Kompilierung und Artefaktkonfiguration betreffen; die Ursache ist aus diesen Messungen nicht isolierbar.','','Die Modelle wurden zeitlich nacheinander und nicht in zufällig wechselnder Reihenfolge getestet. Dateicache wurde nicht geleert; Hintergrunddownloads können Last erzeugen. Ladezeiten sind deshalb keine kontrollierten Kaltstarts. Drei Wiederholungen und ähnliche Fragen erlauben keine abgesicherte allgemeine Rangfolge. TTFT ist der erste Textchunk; Token/s basieren auf nachträglicher Tokenisierung. DeepSeek wird durch das kurze Ausgabelimit stark eingeschränkt.','','Die Referenzprüfung wurde auf Version 1.2 aktualisiert: numerisch gleichwertige Dezimalantworten und englisches „equals“ werden inhaltlich anerkannt, das strenge Antwortformat wird separat geprüft. Die alten Bewertungen bleiben in evaluation_history und den ursprünglichen Archiven erhalten. Deshalb ändern sich einige absolute Punktzahlen gegenüber früheren Statusmeldungen. Die automatische Referenzprüfung ist regelbasiert; offene und redaktionelle Fälle sind nicht automatisch richtig. Ein vollständiger semantischer Qualitätsvergleich steht für Teile der VLM-, Function-Calling- und CPU-Antworten noch aus. Ausgewählte Antwortänderungen stehen unverändert in changed_objective_answers.json. Originalquellen sind über SHA256 in provenance.json referenziert. Nach einem HailoRT-5.5-Upgrade müssen beide Katalogversionen erneut getestet werden.']
    (OUT/'report.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
