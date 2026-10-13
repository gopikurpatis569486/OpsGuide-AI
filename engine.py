"""Dependency-free TF-IDF retrieval with source-grounded extractive responses."""
import math
import re
from collections import Counter

STOP = set('a an the is are to of and for in on with what how do i my it can does'.split())

def tokens(text):
    return [x for x in re.findall(r'[a-z0-9]+', text.lower()) if x not in STOP]

class Retriever:
    def __init__(self, documents):
        self.documents = documents
        self.counts = [Counter(tokens(d['title'] + ' ' + ' '.join(d['tags']) + ' ' + d['text'])) for d in documents]
        df = Counter(term for count in self.counts for term in count)
        self.idf = {term: math.log((1 + len(documents)) / (1 + n)) + 1 for term, n in df.items()}
        self.vectors = [self.vector(c) for c in self.counts]

    def vector(self, count):
        v = {t: (1 + math.log(n)) * self.idf[t] for t, n in count.items() if t in self.idf}
        norm = math.sqrt(sum(x*x for x in v.values())) or 1
        return {t: x/norm for t, x in v.items()}

    def search(self, query, limit=3):
        q = self.vector(Counter(tokens(query)))
        ranked = []
        for d, v in zip(self.documents, self.vectors):
            score = sum(w*v.get(t, 0) for t, w in q.items())
            if score > 0:
                ranked.append({**d, 'score':round(score, 4)})
        return sorted(ranked, key=lambda x: (-x['score'], x['id']))[:limit]

    def answer(self, query):
        hits = self.search(query)
        # This is an evidence threshold, not a calibrated confidence probability.
        if not hits or hits[0]['score'] < 0.16:
            return {'status':'insufficient_evidence','answer':'No sufficiently relevant runbook was found. Escalate to a qualified owner with diagnostic evidence.', 'sources':[], 'mode':'extractive'}
        return {'status':'supported','answer':hits[0]['text'], 'sources':hits, 'mode':'extractive'}
