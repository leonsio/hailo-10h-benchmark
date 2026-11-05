#!/usr/bin/env python3
"""Versioned reference checks plus an explicit queue for editorial review.

No external model service, and no changes to measured raw answers.
"""
import argparse
import collections
import csv
from decimal import Decimal
from datetime import date,timedelta
import hashlib
import json
from pathlib import Path
import re
import unicodedata

VERSION='reference-checks-v1.2'
NUMERIC={'C01':4,'C03':102,'C05':23,'E01':4,'E02':5,'E11':4,'E15':4,'E16':4}
CONTROLLED={f'C{i:02}' for i in range(1,7)}
MANUAL={'E05','E06'}|{f'H{i:02}' for i in range(1,11)}
GIB=1024**3

def atomic_json(path,value):
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    tmp.replace(path)

def read_records(path):
    if not path.exists(): return []
    lines=path.read_text().splitlines(keepends=True)
    result=[]
    for index,line in enumerate(lines):
        try: result.append(json.loads(line))
        except json.JSONDecodeError:
            if index==len(lines)-1 and not line.endswith('\n'): break
            raise
    return result

def clean_answer(raw):
    text=unicodedata.normalize('NFKC',raw)
    text=re.sub(r'<\|[^>]*?\|>|<｜[^>]*?｜>|</?(?:bos|eos|end_of_turn)>','',text)
    if '<think>' in text:
        if '</think>' not in text: return '',True
        text=text.rsplit('</think>',1)[1]
    return text.strip(),False

def group_key(qid,language,text):
    return hashlib.sha256((qid+'\0'+language+'\0'+text).encode()).hexdigest()

def response_key(row):
    return hashlib.sha256(json.dumps([row.get(k) for k in ('model','repeat','question','language','answer')],ensure_ascii=False).encode()).hexdigest()

def word_count(text):
    return len(re.findall(r"\b\w+(?:[-’']\w+)*\b",text))

def calendar_result(text):
    """Evaluate the stated answer, not a weekday in the restated input."""
    text=re.sub(r'[*_`]', '', text)
    markers=list(re.finditer(r'\b(?:therefore|daher|somit|vorgestern|the day before yesterday)\b',text,re.I))
    if markers: text=text[markers[-1].end():]
    weekdays=re.findall(r'\b(?:Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b',text,re.I)
    weekday=bool(weekdays and weekdays[-1].casefold() in ('montag','monday'))
    month_words=['january januar jan','february februar feb','march märz maerz mar mär','april apr','may mai','june juni jun','july juli jul','august aug','september sep sept','october oktober oct okt','november nov','december dezember dec dez']
    months={word:index for index,words in enumerate(month_words,1) for word in words.split()}
    names='(?:'+'|'.join(sorted(months,key=len,reverse=True))+')'
    matches=[]
    patterns=[
        (r'\b(\d{4})[-/](\d{1,2})[-/](\d{1,2})\b','ymd'),
        (r'\b(\d{1,2})[./](\d{1,2})[./](\d{4})\b','dmy'),
        (r'\b(\d{1,2})\.?\s+('+names+r')\.?\s*,?\s*(\d{4})\b','dnmy'),
        (r'\b('+names+r')\.?\s+(\d{1,2})(?:st|nd|rd|th)?\s*,?\s*(\d{4})\b','nmdy')]
    for pattern,kind in patterns:
        for match in re.finditer(pattern,text,re.I):
            a,b,c=match.groups()
            try:
                if kind=='ymd': value=date(int(a),int(b),int(c))
                elif kind=='dmy': value=date(int(c),int(b),int(a))
                elif kind=='dnmy': value=date(int(c),months[b.casefold()],int(a))
                else: value=date(int(c),months[a.casefold()],int(b))
            except ValueError: value=None
            matches.append((match.start(),value))
    matches.sort(key=lambda item:item[0])
    dated=bool(matches and matches[-1][1]==date(2028,2,28))
    ambiguous=len({w.casefold() for w in weekdays})>1 or len({v for _,v in matches})>1
    return (int(weekday)+int(dated))/2,ambiguous


def check(row):
    q=row['question']; lang=row['language']
    text,unfinished=clean_answer(row.get('answer',''))
    norm=text.strip(' \t\r\n.!。').casefold()
    result=dict(question=q,language=lang,clean_answer=text,objective=q not in MANUAL,content_score=None,format_pass=None,needs_review=False,reason='',reference=None,flags=[])
    if unfinished: result['flags'].append('unclosed_thinking_block')
    if row.get('output_tokens',0)>=128: result['flags'].append('possibly_output_limited')
    if row.get('status')!='ok':
        return dict(result,reason='Generation failed; excluded from answer accuracy',technical_error=True)
    if q in NUMERIC:
        expected=NUMERIC[q]
        result['reference']=str(expected)
        exact=norm==str(expected)
        numbers=re.findall(r'(?<!\w)-?\d+(?:[.,]\d+)?(?!\w)',text)
        explicit=bool(re.search(r'(?:=|equals|answer(?: is)?|result(?: is)?|antwort(?: ist)?|ergebnis(?: ist)?)\s*[:=]?\s*'+str(expected)+r'\s*[.!]?$',text,re.I))
        content=exact or (len(text)<120 and ((len(numbers)==1 and Decimal(numbers[0].replace(',','.'))==expected) or explicit) and not re.search(r'\b(?:not|nicht|kein)\b',text,re.I))
        result.update(content_score=float(content),format_pass=exact if q in CONTROLLED or q in ('E01','E02','E11','E16') else None,reason='Final numeric answer checked; incidental mentions in long reasoning do not count')
    elif q in ('C02','E03','E12'):
        result['reference']='Paris'
        present=bool(re.search(r'\bParis\b',text,re.I))
        uncertain=present and (bool(re.search(r'\b(?:Berlin|London|Madrid|Rome|Rom)\b',text,re.I)) or bool(re.search(r'\b(?:nicht|not|kein|keine)\b',text,re.I)))
        result.update(content_score=None if uncertain else float(present),format_pass=norm=='paris' if q=='C02' else None,needs_review=uncertain,reason='Paris required; ambiguous or contradictory phrasing sent to review')
    elif q=='C04':
        expected='Dienstag' if lang=='de' else 'Tuesday'
        present=bool(re.search(r'\b'+('Dienstags?' if lang=='de' else 'Tuesday')+r'\b',text,re.I))
        result.update(reference=expected,content_score=float(present and len(text)<120 and not re.search(r'\b(?:nicht|not|statt|instead)\b',text,re.I)),format_pass=norm==expected.casefold(),reason='Weekday checked; grammatical variant Dienstags is content-correct but not the exact requested name')
    elif q=='C06':
        result.update(reference='Haus',content_score=float(bool(re.search(r'\bHaus\b',text,re.I)) and len(text)<120 and not re.search(r'\b(?:nicht|not|kein)\b',text,re.I)),format_pass=norm=='haus',reason='German translation required in both prompt languages; case-insensitive')
    elif q in ('E04','E13'):
        sucre=bool(re.search(r'\bSucre\b',text,re.I)); paz=bool(re.search(r'\bLa\s+Paz\b',text,re.I))
        result.update(reference='Sucre (constitutional capital); La Paz is the seat of government',content_score=1.0 if sucre else .5 if paz else 0.0,reason='La Paz alone gets partial credit; constitutional capital is Sucre')
    elif q in ('E07','E14'):
        numbers=[int(n) for n in re.findall(r'(?<!\w)\d+(?!\w)',text)]
        if not numbers:
            words=('eins zwei drei vier fünf sechs sieben acht neun zehn elf zwölf dreizehn vierzehn fünfzehn sechzehn siebzehn achtzehn neunzehn zwanzig' if lang=='de' else 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty').split()
            lookup={v:i for i,v in enumerate(words,1)}
            numbers=[lookup[w] for w in re.findall(r'\b\w+\b',text.casefold()) if w in lookup]
        result.update(reference=list(range(1,21)),content_score=float(numbers==list(range(1,21))),reason='All numbers 1 through 20 required exactly once and in order')
    elif q in ('E08','E17'):
        expected={'name':'Max','alter':30}
        start=text.find('{'); obj=None; suffix=''
        if start>=0:
            try: obj,end=json.JSONDecoder().raw_decode(text[start:]); suffix=text[start+end:]
            except json.JSONDecodeError: pass
        result.update(reference=expected,content_score=float(type(obj) is dict and obj==expected),format_pass=bool(type(obj) is dict and obj==expected and start==0 and not suffix.strip()),reason='JSON values and exact keys checked; code fences/explanations fail format independently')
    elif q in ('E09','E10'):
        expected=date(2028,3,1)-timedelta(days=2)
        assert expected.isoformat()=='2028-02-28' and expected.weekday()==0
        score,ambiguous=calendar_result(text)
        result.update(reference='Monday / Montag, 2028-02-28',content_score=None if ambiguous else score,needs_review=ambiguous,reason='Final answer segment checked; ambiguous conflicting weekdays/dates require editorial review')
    elif q in MANUAL:
        constraints={}
        if q=='E05':
            sentences=[s for s in re.split(r'(?<=[.!?])\s+',text.strip()) if re.search(r'\w',s)]
            constraints=dict(sentence_count=len(sentences),exactly_three_sentences=len(sentences)==3)
            result['reference']='Exactly three sentences; no invented current weather without supplied weather data'
        elif q=='E06':
            constraints=dict(word_count=word_count(text),within_50_words=word_count(text)<=50,mentions_miau=bool(re.search(r'\bMiau\b',text,re.I)))
            result['reference']='Coherent very short funny cat story about Miau; maximum 50 words'
        else:
            result['reference']='No tools/state data supplied: do not claim device actions or invent current room temperature'
        result.update(needs_review=True,reason='Editorial review required; automatic structural checks are not a factual correctness verdict',constraints=constraints)
    else:
        result.update(needs_review=True,reason='No evaluator rule')
    return result


def evaluate(output):
    metadata=json.loads((output/'metadata.json').read_text())
    rows=read_records(output/'answers.jsonl')
    overrides=json.loads((output/'manual_reviews.json').read_text()) if (output/'manual_reviews.json').exists() else {}
    checked=[]; groups={}
    for row in rows:
        result=check(row)
        text=result.pop('clean_answer')
        key=group_key(row['question'],row['language'],text)
        result.update(answer_id=response_key(row),group_id=key,model=row['model'],repeat=row['repeat'],category=row['category'],technical_error=row['status']!='ok',evaluator_version=VERSION)
        if key in overrides and not result['technical_error']:
            override=overrides[key]
            result.update(manual_review=override,needs_review=False)
            if result['objective'] and 'content_score' in override: result['content_score']=override['content_score']
            if not result['objective']: result['quality_pass']=override.get('quality_pass')
        checked.append(result)
        if result['needs_review']:
            group=groups.setdefault(key,dict(group_id=key,question=row['question'],language=row['language'],answer=text,reference=result['reference'],constraints=result.get('constraints'),occurrences=[]))
            group['occurrences'].append(dict(model=row['model'],repeat=row['repeat']))
    summaries=[]
    for model in metadata['models']:
        for lang in ('de','en'):
            subset=[r for r in checked if r['model']==model and r['language']==lang and not r['technical_error']]
            controlled=[r for r in subset if r['question'] in CONTROLLED]
            objective=[r for r in subset if r['objective'] and r['content_score'] is not None]
            reviewed=[r for r in subset if not r['objective'] and 'manual_review' in r]
            summaries.append(dict(model=model,language=lang,answers=len(subset),controlled_content_correct=sum(r.get('content_score')==1 for r in controlled),controlled_total=len(controlled),controlled_review_pending=sum(r['needs_review'] for r in controlled),controlled_format_correct=sum(r.get('format_pass') is True for r in controlled),objective_fully_correct=sum(r['content_score']==1 for r in objective),objective_partial=sum(0<r['content_score']<1 for r in objective),objective_incorrect=sum(r['content_score']==0 for r in objective),objective_scored=len(objective),objective_points=sum(r['content_score'] for r in objective),manual_reviewed=len(reviewed),manual_pending=sum(r['needs_review'] for r in subset if not r['objective']),manual_quality_pass=sum(r.get('quality_pass') is True for r in reviewed),review_pending=sum(r['needs_review'] for r in subset),technical_errors=sum(r['technical_error'] for r in checked if r['model']==model and r['language']==lang)))
    atomic_json(output/'correctness_summary.json',summaries)
    with (output/'correctness_summary.csv').open('w') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(summaries[0]) if summaries else ['model'])
        writer.writeheader(); writer.writerows(summaries)
    tmp=output/'answer_checks.jsonl.tmp'
    tmp.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in checked))
    tmp.replace(output/'answer_checks.jsonl')
    atomic_json(output/'review_queue.json',list(groups.values()))
    atomic_json(output/'evaluation_metadata.json',dict(version=VERSION,evaluator_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),manual_reviews_sha256=hashlib.sha256((output/'manual_reviews.json').read_bytes()).hexdigest() if (output/'manual_reviews.json').exists() else None,answer_count=len(rows),raw_answers_sha256=hashlib.sha256((output/'answers.jsonl').read_bytes()).hexdigest() if (output/'answers.jsonl').exists() else None,controlled_scoring='Content and exact requested format reported separately',partial_credit='Bolivia: La Paz alone 0.5; calendar: weekday/date each 0.5',subjective_scoring='Codex/editorial review is separate from objective accuracy; structural checks alone do not establish quality',reference_date='2028-03-01 minus two days = Monday 2028-02-28'))
    return summaries

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    evaluate(args.output)
