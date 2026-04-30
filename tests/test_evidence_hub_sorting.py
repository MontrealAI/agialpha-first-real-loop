import json

def test_sorting_desc():
    runs=json.load(open('evidence_registry/registry/runs.json'))
    assert runs==sorted(runs,key=lambda x:x.get('generated_at',''),reverse=True)
