import json
from pathlib import Path
from .registry import load_registry
FOOT='No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.'
BANNER='This hub records bounded Evidence Docket experiments. It does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, real-world certification, guaranteed economic return, or civilization-scale capability. Stronger claims require independent replay, official public benchmarks, cost/safety review, delayed outcomes, and external audit.'
LEG=['helios-001','helios-002','helios-003','helios-004','cyber-sovereign-001','cyber-sovereign-002','cyber-sovereign-003','benchmark-gauntlet-001','omega-gauntlet-001']

def build_site(registry,out):
    d=load_registry(registry); out=Path(out); out.mkdir(parents=True,exist_ok=True)
    runs=sorted(d['runs'], key=lambda r:r.get('generated_at',''), reverse=True)
    (out/'data').mkdir(exist_ok=True)
    for k,v in [('runs',runs),('experiments',d['experiments']),('workflows',d['workflows']),('latest',runs[0] if runs else {})]:
        (out/'data'/f'{k}.json').write_text(json.dumps(v,indent=2))
    rows=''.join([f"<tr><td><a href='/agialpha-first-real-loop/runs/{r['run_id']}/'>{r['run_id']}</a></td><td>{r.get('experiment_slug')}</td><td>{r.get('status')}</td></tr>" for r in runs])
    (out/'index.html').write_text(f"<h1>AGI ALPHA Evidence Hub</h1><p>{BANNER}</p><table>{rows}</table><footer>{FOOT}</footer>")
    (out/'404.html').write_text('Not found')
    for base in ['experiments','workflows','runs','artifacts','legacy']:(out/base).mkdir(exist_ok=True)
    (out/'experiments'/'index.html').write_text('experiments')
    for e in d['experiments']:
        slug=e['experiment_slug']; p=out/'experiments'/slug/'runs'; p.mkdir(parents=True,exist_ok=True)
        (out/'experiments'/slug/'index.html').write_text(f"<h1>{slug}</h1><div>{e.get('claim_boundary','pending')}</div><footer>{FOOT}</footer>")
    for r in runs:
        p=out/'runs'/r['run_id']; p.mkdir(parents=True,exist_ok=True)
        (p/'manifest.json').write_text(json.dumps(r,indent=2))
        (p/'index.html').write_text(f"<a href='{r.get('run_url','#')}'>run</a><div>{r.get('claim_boundary')}</div><footer>{FOOT}</footer>")
    for l in LEG:
        p=out/l; p.mkdir(exist_ok=True)
        (p/'index.html').write_text(f"<meta http-equiv='refresh' content='0; url=/agialpha-first-real-loop/experiments/{l}/'>")
