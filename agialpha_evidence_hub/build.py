import json, html
from pathlib import Path
from .render import page, CLAIM
from .legacy import LEGACY_SLUGS

def build_site(registry='evidence_registry', out='_site'):
    r=Path(registry); o=Path(out); o.mkdir(parents=True,exist_ok=True)
    runs=json.loads((r/'runs.json').read_text()) if (r/'runs.json').exists() else []
    runs=sorted(runs,key=lambda x:x.get('generated_at',''),reverse=True)
    exps={}
    for run in runs: exps.setdefault(run['experiment_slug'],[]).append(run)
    for d in ['data','experiments','runs','workflows','artifacts','legacy','external-review','safety']: (o/d).mkdir(exist_ok=True)
    # data files
    for name,content in [('runs.json',runs),('experiments.json',sorted(exps.keys())),('workflows.json',sorted({x.get('workflow_name','') for x in runs})),('latest.json',runs[0] if runs else {}),('safety.json',[{x['run_id']:x.get('metrics',{})} for x in runs]),('external_review.json',[x.get('external_review',{}) for x in runs])]:
        (o/'data'/name).write_text(json.dumps(content,indent=2))
    rows=''.join([f"<tr><td>{html.escape(x.get('generated_at',''))}</td><td><a href='experiments/{x['experiment_slug']}/'>{html.escape(x['experiment_slug'])}</a></td><td>{html.escape(x.get('workflow_name',''))}</td><td>{html.escape(x.get('status',''))}</td><td>{html.escape(x.get('claim_level',''))}</td><td>{html.escape(str(x.get('metrics',{}).get('replay_passes','not_reported')))}</td><td>{html.escape(str(x.get('metrics',{}).get('baseline_count','not_reported')))}</td><td>{html.escape(str(x.get('metrics',{}).get('safety_incidents','not_reported')))}</td><td>{html.escape(str(x.get('external_review',{}).get('status','not_started')))}</td><td>{html.escape(str(x.get('pr_review',{}).get('status','not_applicable')))}</td><td><a href='runs/{x['run_id']}/'>run</a></td><td><a href='{html.escape(x.get('run_url','#'))}'>actions</a></td></tr>" for x in runs])
    body=f"<h2>Unified Evidence Docket registry for AGI ALPHA workflows, experiments, replay, baselines, safety ledgers, and external review.</h2><p>{html.escape(CLAIM)}</p><h3>Recent Runs</h3><table><tr><th>generated_at</th><th>experiment</th><th>workflow</th><th>status</th><th>claim_level</th><th>replay</th><th>baselines</th><th>safety incidents</th><th>external review</th><th>PR review</th><th>run page</th><th>GitHub Actions run</th></tr>{rows}</table>"
    (o/'index.html').write_text(page('AGI ALPHA Evidence Hub',body))
    (o/'404.html').write_text(page('Not found',"<a href='/agialpha-first-real-loop/'>Back to hub</a>"))
    (o/'experiments/index.html').write_text(page('Experiments',''.join([f"<div><a href='/agialpha-first-real-loop/experiments/{s}/'>{s}</a></div>" for s in sorted(exps)])))
    (o/'runs/index.html').write_text(page('Runs',''.join([f"<div><a href='/agialpha-first-real-loop/runs/{x['run_id']}/'>{x['run_id']}</a></div>" for x in runs])))
    (o/'workflows/index.html').write_text(page('Workflows',''.join([f"<div>{w}</div>" for w in sorted({x.get('workflow_name','') for x in runs})])))
    (o/'artifacts/index.html').write_text(page('Artifacts','artifact links are listed on run pages'))
    (o/'external-review/index.html').write_text(page('External Review','summary in run pages'))
    (o/'safety/index.html').write_text(page('Safety','safety counters in run pages'))
    (o/'legacy/index.html').write_text(page('Legacy Routes','legacy routes redirect to experiments'))
    for slug,sruns in exps.items():
        sruns=sorted(sruns,key=lambda x:x.get('generated_at',''),reverse=True); latest=sruns[0]
        ep=o/'experiments'/slug; (ep/'runs').mkdir(parents=True,exist_ok=True)
        metrics=''.join([f"<tr><td>{k}</td><td>{html.escape(str(v))}</td></tr>" for k,v in latest.get('metrics',{}).items()])
        run_rows=''.join([f"<tr><td>{x['run_id']}</td><td>{x.get('status')}</td><td><a href='/agialpha-first-real-loop/runs/{x['run_id']}/'>open</a></td></tr>" for x in sruns])
        ep_body=f"<p>claim boundary: {html.escape(latest.get('claim_boundary','unavailable'))}</p><h3>Latest metrics</h3><table>{metrics}</table><h3>All runs</h3><table>{run_rows}</table><p><a href='/agialpha-first-real-loop/'>Back to hub</a></p>"
        (ep/'index.html').write_text(page(slug,ep_body)); (ep/'runs/index.html').write_text(page(f'{slug} runs',run_rows))
        for x in sruns:
            rp=ep/'runs'/x['run_id']; rp.mkdir(parents=True,exist_ok=True)
            (rp/'manifest.json').write_text(json.dumps(x,indent=2)); (rp/'index.html').write_text(page(x['run_id'],f"<a href='{x.get('run_url','#')}'>Actions Run</a>"))
    for run in runs:
        rp=o/'runs'/run['run_id']; rp.mkdir(parents=True,exist_ok=True)
        (rp/'manifest.json').write_text(json.dumps(run,indent=2))
        (rp/'index.html').write_text(page(run['run_id'],f"<p>experiment: <a href='/agialpha-first-real-loop/experiments/{run['experiment_slug']}/'>{run['experiment_slug']}</a></p><p>workflow:{run.get('workflow_name')}</p><p><a href='{run.get('run_url','#')}'>GitHub Actions run</a></p><p>claim boundary: {html.escape(run.get('claim_boundary',''))}</p><p><a href='/agialpha-first-real-loop/'>Back to hub</a></p>"))
    for slug in LEGACY_SLUGS:
        lp=o/slug; lp.mkdir(exist_ok=True)
        target=f"/agialpha-first-real-loop/experiments/{slug}/" if slug in exps else '/agialpha-first-real-loop/legacy/'
        msg='backfill required' if slug not in exps else 'canonical experiment page'
        (lp/'index.html').write_text(page(slug,f"<meta http-equiv='refresh' content='0; url={target}'/><p>{msg}</p><p>{html.escape(CLAIM)}</p><a href='/agialpha-first-real-loop/'>Back to hub</a>"))
