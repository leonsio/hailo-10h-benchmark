#!/usr/bin/env python3
"""Write a compact German report from benchmark raw records and native logs."""
import argparse
import json
import csv
import statistics
import time
from run import aggregate_summary
from pathlib import Path
import re

def model_memory_rows(metadata,loads,events):
    rows=[]
    for model in metadata['models']:
        samples=[r for r in loads if r['model']==model]
        sizes=[e['bytes'] for e in events if e.get('model')==model and e.get('event') in ('downloaded','cached_download','existing_artifact') and 'bytes' in e]
        sizes += [r['artifact_bytes'] for r in samples if 'artifact_bytes' in r]
        row=dict(model=model,artifact_bytes=sizes[-1] if sizes else None)
        for key in ('hailo_ram_before_bytes','hailo_ram_loaded_bytes','hailo_ram_delta_bytes','host_rss_before_bytes','host_rss_loaded_bytes','host_rss_delta_bytes'):
            values=[r[key] for r in samples if r.get(key) is not None]
            row[key+'_mean']=statistics.mean(values) if values else None
            row[key+'_samples']=len(values)
        rows.append(row)
    return rows


def render(output):
    metadata=json.loads((output/'metadata.json').read_text())
    events=[json.loads(s) for s in (output/'events.jsonl').read_text().splitlines()] if (output/'events.jsonl').exists() else []
    loads=[json.loads(line) for line in (output/'loads.jsonl').read_text().splitlines()] if (output/'loads.jsonl').exists() else []
    answers=[json.loads(line) for line in (output/'answers.jsonl').read_text().splitlines()] if (output/'answers.jsonl').exists() else []
    summary=aggregate_summary(answers,loads,events,metadata['models'])
    (output/'live_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    if summary:
        with (output/'live_summary.csv').open('w') as handle:
            writer=csv.DictWriter(handle,fieldnames=list(summary[0]))
            writer.writeheader(); writer.writerows(summary)
    memory_rows=model_memory_rows(metadata,loads,events)
    memory={row['model']:row for row in memory_rows}
    (output/'model_sizes.json').write_text(json.dumps(memory_rows,ensure_ascii=False,indent=2)+'\n')
    with (output/'model_sizes.csv').open('w') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(memory_rows[0]) if memory_rows else ['model'])
        writer.writeheader(); writer.writerows(memory_rows)
    completed={e['model'] for e in events if e.get('event') in ('artifact_deleted','existing_artifact_preserved')}
    pairs={(s['model'],s['language']):s for s in summary}
    fmt=lambda v:'—' if v is None else f'{v:.2f}'
    gib=lambda value:fmt(value/(1024**3)) if value is not None else '—'
    lines=['# Ergebnisse des Chat-Benchmarks','',f"Aktualisiert: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}.",f"Status: {'abgeschlossen' if set(metadata['models'])<=completed else 'Zwischenstand'}. Start: {metadata['started']}.",f"Runtime: `{metadata['runtime']}`. Modellartefakte: `{metadata['release']}`.",f"Drei Wiederholungen je Modell; maximal {metadata['max_tokens']} Ausgabetokens. Hintergrunddownload: {'aktiviert' if metadata.get('prefetch') else 'deaktiviert'}.",'','| Modell | Datei GiB | Hailo-RAM GiB | Host-RSS GiB | Ladungen | Antworten | Ladezeit s | TTFT DE s | TTFT EN s | Decode DE Token/s | Decode EN Token/s | Status |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
    for model in metadata['models']:
        de=pairs.get((model,'de'),{})
        en=pairs.get((model,'en'),{})
        status='abgeschlossen' if model in completed else 'ausstehend'
        current=[row for row in answers if row['model']==model]
        if model not in completed and current:
            repeat=max(row['repeat'] for row in current)
            count=sum(row['repeat']==repeat for row in current)
            question_count=len(json.loads((output/'questions.json').read_text())['questions'])*2
            status=f"Durchlauf {repeat}/{metadata['repeats']}: {count}/{question_count} Antworten"
        elif model not in completed and any(e.get('model')==model and e.get('event') in ('downloaded','cached_download','existing_artifact') for e in events):
            status='Datei bereit; noch keine Antworten'
        errors=[]
        for log in sorted(output.glob(model+'-*.log')):
            matches=re.findall(r'HAILO_[A-Z_]+(?:\(\d+\))?',log.read_text(errors='replace'))
            errors+=matches
        if errors:
            status=', '.join(sorted(set(errors)))
        if any(e.get('model')==model and e.get('event')=='timeout' for e in events): status+='; Skript-Timeout'
        for e in events:
            if e.get('model')==model and e.get('event')=='error': status=e.get('error','Fehler').replace('|','/')
        lines.append('| '+' | '.join([model,gib(memory[model]['artifact_bytes']),gib(memory[model]['hailo_ram_loaded_bytes_mean']),gib(memory[model]['host_rss_loaded_bytes_mean']),str(de.get('successful_loads',0)),str(de.get('successful_answers',0)+en.get('successful_answers',0)),fmt(de.get('load_s_mean')),fmt(de.get('ttft_s_mean')),fmt(en.get('ttft_s_mean')),fmt(de.get('decode_tokens_per_s_mean')),fmt(en.get('decode_tokens_per_s_mean')),status])+' |')
    lines+=['','Die laufende Tabelle wird direkt aus den Einzelmessungen aktualisiert; Mittelwerte noch laufender Modelle sind vorläufig. `live_summary.csv/json` enthalten denselben aktuellen Stand. Erfolgreiche Antworten in der Leistungstabelle bedeuten technischen Erfolg. Die separate Richtigkeitsauswertung folgt weiter unten, soweit sie bereits vorliegt.','','**Speicher:** Datei ist die tatsächliche Artefaktgröße, auch nach deren Löschung aus dem Testcache. Hailo-RAM ist die gesamte Gerätebelegung unmittelbar nach erfolgreichem Laden einschließlich Firmware/Linux. Host-RSS ist der residente Arbeitsspeicher des Worker-Prozesses einschließlich Runtime; beim CPU-Modell enthält er das geladene Modell. Beide RAM-Spalten zeigen Mittelwerte der vorhandenen Messungen. Es sind keine Spitzenwerte während der Inferenz. Zusätzlicher Verbrauch gegenüber dem Ausgangswert und die Zahl der RAM-Messungen stehen in `model_sizes.csv/json`. Frühere, nicht erfasste RAM-Werte und fehlgeschlagene Ladungen bleiben leer (—); sie werden nicht als null gewertet. 1 GiB = 1.073.741.824 Bytes.','','Ladezeiten und Antwortmetriken sind arithmetische Mittelwerte erfolgreicher Versuche. Fehlgeschlagene Starts liefern keine gültigen Leistungswerte. TTFT ist die Zeit bis zum ersten Textchunk. Die Tokenzahlen werden mit dem jeweiligen Modelltokenizer aus der vollständigen Rohantwort ermittelt. Decode-Token/s schließen den ersten Textchunk aus; bei nur einem Chunk ist diese Metrik nicht verfügbar. `summary.csv` enthält zusätzlich Token/s einschließlich TTFT.','', 'Bisherige Fehler anderer Konfigurationen und die separaten Hardware-Probeläufe sind nicht in diese Mittelwerte eingemischt. Der Betriebssystem-Dateicache wurde nicht geleert. Bei aktivem Vorladen können Netzwerk- und Datenträgerlast die Messungen beeinflussen.','', 'Details: `answers.jsonl`, `loads.jsonl`, `events.jsonl`, `question_means.json`, `metadata.json` sowie native Modelllogs.']
    if (output/'correctness_summary.json').exists():
        quality=json.loads((output/'correctness_summary.json').read_text())
        qa={(row['model'],row['language']):row for row in quality}
        lines += ['', '## Richtigkeit der Antworten', '', 'Automatische Referenzprüfung und gesonderte redaktionelle Sichtung durch Codex. Noch offene Fälle sind nicht als richtig bestätigt. Technische Generierungsfehler werden separat erfasst.', '', '| Modell | C DE Punkte / Format | C EN Punkte / Format | Sachaufgaben DE Punkte | Sachaufgaben EN Punkte | Redaktionell geprüft | Offen |', '|---|---|---|---|---|---:|---:|']
        for model in metadata['models']:
            de=qa.get((model,'de'),{}); en=qa.get((model,'en'),{})
            def controlled(row):
                n=row.get('controlled_total',0)
                return f"{row.get('controlled_points',row.get('controlled_content_correct',0))}/{n} / {row.get('controlled_format_correct',0)}/{n}" if n else '—'
            def objective(row):
                n=row.get('objective_scored',0)
                return f"{row.get('objective_points',0):g}/{n}" if n else '—'
            reviewed=de.get('manual_reviewed',0)+en.get('manual_reviewed',0)
            pending=de.get('review_pending',0)+en.get('review_pending',0)
            lines.append('| '+' | '.join([model,controlled(de),controlled(en),objective(de),objective(en),str(reviewed),str(pending)])+' |')
        lines += ['', 'C: sechs kontrollierte Aufgaben je Sprache und Durchlauf. Ausgabevorgaben gehen in die Punkte ein: erkennbare richtige Antwort mit Ausgabeartefakten 0,25 Punkte und Format 0; zusätzliche Erklärung bei ausdrücklich verlangter Kurzantwort 0 Punkte. Ohne Einschränkung sind Erklärungen zulässig. Bekannte reguläre Stopmarkierungen werden weiterhin entfernt. Sachaufgaben: 21 objektive Aufgaben pro Sprache und Durchlauf; La Paz allein erhält 0,5 Punkte, Kalenderdatum und Wochentag jeweils 0,5. Kreativtexte, Wetterantworten und Aussagen über nicht ausgeführte Geräteaktionen werden redaktionell nach dokumentierten Kriterien geprüft und nicht in die objektive Trefferquote gemischt. Einzelurteile und Begründungen stehen in `answer_checks.jsonl`; offene Antworten in `review_queue.json`.']
    (output/'report.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    render(parser.parse_args().output)
