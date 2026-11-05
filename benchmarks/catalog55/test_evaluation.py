import tempfile
from pathlib import Path
import unittest
import json
from evaluate import check,evaluate,apply_scoring_policy
from suite import archive_results

class EvaluationTests(unittest.TestCase):
    def row(self,q,text,lang='de'):
        return dict(question=q,answer=text,language=lang,status='ok',output_tokens=10,model='test',repeat=1,category='controlled' if q.startswith('C') else 'exploratory')
    def test_numeric_content_and_format_separate(self):
        r=check(self.row('C03','17 × 6 = 102<|im_end|>'))
        self.assertEqual(r['semantic_score'],1)
        self.assertEqual(r['content_score'],0)
        self.assertFalse(r['format_pass'])
        self.assertEqual(check(self.row('C03','108'))['content_score'],0)
        for text in ('4.0.', '2+2 equals 4.', 'The answer is 4.0.'):
            r=check(self.row('C01',text,'en'))
            self.assertEqual(r['semantic_score'],1)
            self.assertEqual(r['content_score'],0)
            self.assertFalse(r['format_pass'])
        self.assertEqual(check(self.row('C01','4.1'))['content_score'],0)
    def test_json_explanation_and_fences_fail_format_only(self):
        r=check(self.row('E08','```json\n{"name":"Max","alter":30}\n```'))
        self.assertEqual(r['semantic_score'],1)
        self.assertEqual(r['content_score'],0)
        self.assertFalse(r['format_pass'])
        self.assertEqual(check(self.row('E08','{"name":"Max","age":30}'))['content_score'],0)
    def test_user_partial_credit_for_output_artifacts(self):
        for q,text in [('C02','Parisagma<turn|>'),('E03','Parisagma<turn|>'),('C01','4<pad>'),('C03','102<turn|>'),('E08','```<pad>\n{"name":"Max","alter":30}\n```<eos>')]:
            r=check(self.row(q,text))
            self.assertEqual(r['content_score'],.25,(q,text,r))
            self.assertFalse(r['format_pass'])
        for text in ['Londonagma<turn|>','agma<turn|>','Paris ist nicht die Hauptstadt<pad>']:
            r=check(self.row('C02',text))
            self.assertNotEqual(r['content_score'],.25)
        r=check(self.row('C02','Paris<|im_end|>'))
        self.assertEqual(r['content_score'],1)
        self.assertTrue(r['format_pass'])
    def test_user_strictness_depends_on_actual_question(self):
        strict=check(self.row('C02','Die Hauptstadt ist Paris.'))
        self.assertEqual(strict['semantic_score'],1)
        self.assertEqual(strict['content_score'],0)
        free=check(self.row('E03','Die Hauptstadt ist Paris.'))
        self.assertEqual(free['content_score'],1)
        self.assertIsNone(free['format_pass'])
        row=self.row('C02','Die Hauptstadt ist Paris.')
        row['prompt']='Was ist die Hauptstadt von Frankreich?'
        self.assertEqual(check(row)['content_score'],1)
        self.assertEqual(check(self.row('E15','2+2 equals 4.','en'))['content_score'],1)

    def test_editorial_overrides_cannot_bypass_new_policy(self):
        row=self.row('C02','Die Hauptstadt ist Paris.')
        result=check(row)
        result.update(content_score=1,semantic_score=1)
        self.assertEqual(apply_scoring_policy(row,result)['content_score'],0)
        row=self.row('H02','I cannot directly control devices<pad>.','en')
        result=check(row);result['quality_pass']=True
        result=apply_scoring_policy(row,result)
        self.assertEqual(result['quality_score'],.25)
        self.assertFalse(result['quality_pass'])
        self.assertFalse(result['format_pass'])

    def test_calendar_and_partial_credit(self):
        self.assertEqual(check(self.row('E09','Montag, 28. Februar 2028.'))['content_score'],1)
        self.assertEqual(check(self.row('E10','Tuesday, February 28, 2028.','en'))['content_score'],.5)
        self.assertEqual(check(self.row('E09','Donnerstag, 31.2.2028.'))['content_score'],0)
        self.assertEqual(check(self.row('E10','March 1, 2028 was a Monday. Therefore, the day before yesterday was Tuesday, March 1, 2028.','en'))['content_score'],0)
        self.assertEqual(check(self.row('E09','Heute ist Mittwoch. Vorgestern war **Montag, 28. Februar 2028**.'))['content_score'],1)
        self.assertTrue(check(self.row('E09','Montag oder Dienstag, 28. Februar 2028.'))['needs_review'])
    def test_capital_not_just_substring_or_negated(self):
        self.assertEqual(check(self.row('E04','Sucreti'))['content_score'],0)
        self.assertEqual(check(self.row('E04','La Paz'))['content_score'],.5)
        self.assertIsNone(check(self.row('C02','Paris ist nicht die Hauptstadt.'))['content_score'])
    def test_no_automatic_pass_for_creative_or_action_answer(self):
        self.assertTrue(check(self.row('H01','Erledigt.'))['needs_review'])
        r=check(self.row('E05','Die Sonne scheint. Es ist warm. Es bleibt trocken.'))
        self.assertTrue(r['constraints']['exactly_three_sentences'])
        self.assertIsNone(r['content_score'])
    def test_repeated_count_and_unfinished_reasoning_fail(self):
        self.assertEqual(check(self.row('E07',','.join(str(n) for n in range(1,21))))['content_score'],1)
        self.assertEqual(check(self.row('E07','1 2 3 1 2 3'))['content_score'],0)
        self.assertEqual(check(self.row('C01','<think>2+2=4'))['content_score'],0)
    def test_archive_verified_and_source_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); source=root/'source'; source.mkdir()
            (source/'metadata.json').write_text(json.dumps({'release':'v5.5.0'}))
            (source/'answers.jsonl').write_text('{"answer":"4"}\n')
            result=archive_results(source,root/'archives')
            self.assertTrue(result['verified'])
            self.assertTrue(Path(result['path']).exists())
            self.assertEqual((source/'answers.jsonl').read_text(),'{"answer":"4"}\n')

if __name__=='__main__': unittest.main()
