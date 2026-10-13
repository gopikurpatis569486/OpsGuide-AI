import json
from pathlib import Path
from engine import Retriever

CASES = [
 ('CPU overheating and fan alarm', 'RB-001'),
 ('PSU power supply redundancy lost', 'RB-002'),
 ('Network switch port link down', 'RB-003'),
 ('Linux filesystem disk space full', 'RB-004'),
 ('IAM access denied permission', 'RB-005'),
 ('Kubernetes EKS pod deployment image failure', 'RB-006'),
 ('Liquid cooling leak flow alarm', 'RB-007'),
 ('Decommission drive erase report disposal', 'RB-008'),
 ('REST API HTTP timeout integration failure', 'RB-009'),
 ('Incident ticket SLA handover escalation', 'RB-010'),
 ('Fan status and airflow obstructions', 'RB-001'),
 ('Power feeds and failed supply identifier', 'RB-002'),
 ('Cable labels and patch-panel mapping', 'RB-003'),
 ('Application log growth retention filesystem', 'RB-004'),
 ('Explicit deny role policies least privilege', 'RB-005'),
 ('Container readiness probes registry permissions', 'RB-006'),
 ('Coolant pressure leak notify facilities', 'RB-007'),
 ('Chain of custody storage media retirement', 'RB-008'),
 ('Endpoint response code correlation identifier', 'RB-009'),
 ('Assign owner overdue incidents shift handover', 'RB-010'),
]

def evaluate():
    r = Retriever(json.loads((Path(__file__).parent/'data/runbooks.json').read_text()))
    rows = []
    for question, expected in CASES:
        hits = r.search(question)
        rows.append({'question':question,'expected':expected,'actual':hits[0]['id'] if hits else None,'top1_correct':bool(hits and hits[0]['id']==expected),'top3_correct':expected in [h['id'] for h in hits]})
    return {'dataset':'20 synthetic queries authored from the same demo runbooks; not an independent benchmark','cases':len(rows), 'top1_accuracy':sum(x['top1_correct'] for x in rows)/len(rows), 'recall_at_3':sum(x['top3_correct'] for x in rows)/len(rows), 'results':rows}

if __name__ == '__main__':
    print(json.dumps(evaluate(), indent=2))
