import unittest
import json
from pathlib import Path
from engine import Retriever
from evaluate import evaluate

class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.r = Retriever(json.loads((Path(__file__).parent/'data/runbooks.json').read_text()))
    def test_known_query_cites_actual_source(self):
        a = self.r.answer('Kubernetes EKS pod deployment image failure')
        self.assertEqual(a['status'],'supported')
        self.assertEqual(a['sources'][0]['id'],'RB-006')
        self.assertEqual(a['answer'],a['sources'][0]['text'])
    def test_unknown_query_abstains(self):
        a = self.r.answer('astronomy nebula telescope')
        self.assertEqual(a['status'],'insufficient_evidence')
        self.assertEqual(a['sources'],[])
    def test_empty_query(self):
        self.assertEqual(self.r.answer('')['status'],'insufficient_evidence')
    def test_scores_and_ranking(self):
        hits = self.r.search('power supply fault')
        self.assertEqual(hits[0]['id'],'RB-002')
        self.assertTrue(all(0<=h['score']<=1.0001 for h in hits))
    def test_synthetic_evaluation(self):
        e = evaluate()
        self.assertEqual(e['cases'],20)
        self.assertGreaterEqual(e['top1_accuracy'],.9)

if __name__=='__main__':
    unittest.main()
