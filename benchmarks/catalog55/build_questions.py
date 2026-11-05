"""Extract original historical prompts and pair them with explicit translations."""
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
EN = [
'What is 2 + 2? Answer with the number only.',
'What is the capital of France? Answer with the city name only.',
'What is 17 times 6? Answer with the number only.',
'Which day of the week comes after Monday? Answer with the weekday only.',
'Which number is greater: 17 or 23? Answer with the number only.',
'Translate the English word house into German. Answer with one word only.',
'Calculate 2+2 and output only the answer',
'Calculate 2+3 and output only the answer',
'What is the capital of France?',
'What is the capital of Bolivia',
'Write exactly three sentences about the weather today.',
'Tell a very short, funny story about a cat named Miau (at most 50 words).',
'Count from 1 to 20.',
"Give me a JSON object with the keys 'name' (value: 'Max') and 'alter' (value: 30). No explanation around it.",
'Today is March 1, 2028. What day of the week and date was the day before yesterday?',
'Today is March 1, 2028. What day of the week and date was the day before yesterday?',
'Calculate 2+2 and just give the answer.',
'What is the capital of France?',
'What is the capital of Bolivia?',
'Count from 1 to 20.',
'Calclate 2+2',
'Add 2+2 .give only the result',
"Give me a JSON object with the keys 'name' (value: 'Max') and 'alter' (value: 30). No explanation around it. Output only one answer",
'Set the living room light to 70 percent.',
'Turn on the kitchen light.',
'Turn off the bedside lamp.',
'Set the living room light to red.',
'Set the bedroom temperature to 19.5 degrees.',
'Set the attic roller shutter to 40 percent.',
'Close the roller shutter.',
'Start Deebot mini.',
'Turn on the coffee machine.',
'How warm is it in the living room?',
]
DE = {
'E10': 'Heute ist der 1. März 2028. Welcher Wochentag und welches Datum waren vorgestern?',
'E11': 'Berechne 2+2 und gib nur die Antwort aus.',
'E12': 'Was ist die Hauptstadt von Frankreich?',
'E13': 'Was ist die Hauptstadt von Bolivien?',
'E14': 'Zähle von 1 bis 20.',
}
source = (ROOT/'doc/model-benchmark-evaluation.md').read_text().split('## Vollständige Fragenübersicht und Testsprache', 1)[1].split('### Einfluss der deutschen Fragestellung', 1)[0]
rows = re.findall(r'^\| ([CEH]\d\d) \| (.*?) \|', source, re.M)
assert len(rows) == len(EN) == 33
questions = []
for (qid, original), en in zip(rows, EN):
    questions.append(dict(id=qid, category={'C':'controlled','E':'exploratory','H':'intent'}[qid[0]], de=DE.get(qid,original), en=en, original=original, original_language='en' if qid in DE else 'de', note='Preserves typo; English typo is an analogous translation.' if qid=='E15' else 'Translation into German is intentional in both languages.' if qid=='C06' else 'No weather data or device tools supplied.' if qid=='E05' or qid.startswith('H') else ''))
payload = dict(schema_version=1, source='doc/model-benchmark-evaluation.md', questions=questions)
HERE = Path(__file__).resolve().parent
(HERE/'questions.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
lines=['# Fragenkatalog DE / EN','', '33 historische Aufgaben, jeweils in beiden Sprachen. Sprachvarianten und Wiederholungen bleiben anhand ihrer Original-ID erkennbar. C06 prüft in beiden Sprachen die Übersetzung ins Deutsche. E15 enthält absichtlich einen Tippfehler. Wetterdaten und Gerätewerkzeuge werden nicht bereitgestellt. HA-Fragen prüfen ausschließlich Textantworten; es werden keine Geräte geschaltet. VLMs erhalten dieselben Textfragen ohne Bilder.','', '| ID | Deutsch | English |','|---|---|---|']
lines += [f"| {q['id']} | {q['de']} | {q['en']} |" for q in questions]
(HERE/'questions.md').write_text('\n'.join(lines)+'\n')
