import json
from pathlib import Path
from .render import page

def build_site(registry='evidence_registry/registry', out='_site'):
    r=Path(registry); o=Path(out); o.mkdir(parents=True,exist_ok=True)
    runs=json.loads((r/'runs.json').read_text()) if (r/'runs.json').exists() else []
    exps={}
    for run in runs: exps.setdefault(run['experiment_slug'],[]).append(run)
    recent=''.join([f"<tr><td><a href='runs/{x['run_id']}/'>{x['run_id']}</a></td><td>{x['experiment_slug']}</td><td>{x['status']}</td></tr>" for x in runs])
    (o/'index.html').write_text(page('AGI ALPHA Evidence Hub',"<p>This hub records bounded Evidence Docket experiments. It does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, real-world certification, guaranteed economic return, or civilization-scale capability.</p><table><tr><th>Run</th><th>Experiment</th><th>Status</th></tr>"+recent+"</table>"))
    (o/'404.html').write_text(page('Not found',''))
    for d in ['data','experiments','runs','workflows','artifacts','legacy']: (o/d).mkdir(exist_ok=True)
    (o/'data/runs.json').write_text(json.dumps(runs,indent=2))
    for slug,sruns in exps.items():
        ep=o/'experiments'/slug; (ep/'runs').mkdir(parents=True,exist_ok=True)
        rows=''.join([f"<tr><td><a href='/agialpha-first-real-loop/runs/{r['run_id']}/'>{r['run_id']}</a></td><td>{r['status']}</td></tr>" for r in sruns])
        (ep/'index.html').write_text(page(slug,f"<div>claim_boundary: {sruns[0].get('claim_boundary')}</div><table>{rows}</table>"))
    for run in runs:
        rp=o/'runs'/run['run_id']; rp.mkdir(parents=True,exist_ok=True)
        (rp/'manifest.json').write_text(json.dumps(run,indent=2))
        (rp/'index.html').write_text(page(run['run_id'],f"<a href='{run.get('run_url','#')}'>workflow run</a>"))
    for slug in ['helios-001','helios-002','helios-003','helios-004','cyber-sovereign-001','cyber-sovereign-002','cyber-sovereign-003','benchmark-gauntlet-001','omega-gauntlet-001']:
        lp=o/slug; lp.mkdir(exist_ok=True)
        (lp/'index.html').write_text(page(slug,f"<meta http-equiv='refresh' content='0; url=/agialpha-first-real-loop/experiments/{slug}/'/>"))
