import json, html
from pathlib import Path
from .render import page, CLAIM_BOUNDARY
from .legacy import LEGACY_SLUGS

def _load(base):
    b=Path(base)
    runs=json.loads((b/'runs.json').read_text()) if (b/'runs.json').exists() else []
    exps=json.loads((b/'experiments.json').read_text()) if (b/'experiments.json').exists() else []
    wfs=json.loads((b/'workflows.json').read_text()) if (b/'workflows.json').exists() else []
    catalog_path = b / 'workflow_catalog.json'
    catalog = json.loads(catalog_path.read_text()) if catalog_path.exists() else {'workflows': []}
    if isinstance(catalog, dict):
        catalog_workflows = catalog.get('workflows', [])
    else:
        catalog_workflows = catalog
    if catalog_workflows:
        wfs = catalog_workflows
    return runs,exps,wfs

def build_site(registry='evidence_registry', out='_site'):
    runs,exps,wfs=_load(registry)
    o=Path(out); o.mkdir(parents=True,exist_ok=True)
    for d in ['data','experiments','workflows','runs','artifacts','legacy','external-review','safety','launchpad','falsification','assets','strong-rsi']:
        (o/d).mkdir(exist_ok=True)

    o.joinpath('.nojekyll').write_text('')
    o.joinpath('assets/app.css').write_text(':root{--bg:#f7f9fc;--panel:#fff;--panel-2:#f1f5f9;--text:#0f172a;--muted:#475569;--line:#dbe3ef;--accent:#2563eb;--success:#059669;--warning:#d97706;--danger:#dc2626;--info:#0284c7;--shadow:0 8px 30px rgba(15,23,42,.07);--radius:16px}*{box-sizing:border-box}body{margin:0;font-family:Inter,Arial,sans-serif;background:var(--bg);color:var(--text)}.topnav{display:flex;justify-content:space-between;align-items:center;padding:1rem 2rem;border-bottom:1px solid var(--line);background:var(--panel)}.topnav nav a,.brand{margin-right:1rem;color:var(--accent);text-decoration:none}.container{max-width:1200px;margin:2rem auto;padding:0 1rem}.panel{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:1rem 1.25rem}.hero h1{margin-top:0}table{width:100%;border-collapse:collapse}td,th{border:1px solid var(--line);padding:.45rem;text-align:left}.footer{padding:1rem 2rem;color:var(--muted)}')
    o.joinpath('assets/app.js').write_text('document.querySelectorAll("[data-copy]").forEach(b=>b.onclick=()=>navigator.clipboard?.writeText(b.dataset.copy));')

    by_exp={}
    for r in sorted(runs,key=lambda x:x.get('generated_at',''), reverse=True):
        by_exp.setdefault(r['experiment_slug'],[]).append(r)
    rows=''.join([f"<tr><td>{html.escape(r.get('generated_at',''))}</td><td><a href='/agialpha-first-real-loop/experiments/{r['experiment_slug']}/'>{r['experiment_slug']}</a></td><td>{html.escape(r.get('workflow_name',''))}</td><td>{r.get('status')}</td><td>{r.get('claim_level')}</td><td>{r.get('metrics',{}).get('replay_passes','not_reported')}</td><td>{r.get('metrics',{}).get('baseline_count','not_reported')}</td><td>{r.get('metrics',{}).get('safety_incidents','not_reported')}</td><td>{r.get('external_review',{}).get('status','not_started')}</td><td>{r.get('pr_review',{}).get('status','not_applicable')}</td><td><a href='/agialpha-first-real-loop/runs/{r['run_id']}/'>run page</a></td><td><a href='{r.get('run_url','#')}'>actions</a></td></tr>" for r in runs])
    o.joinpath('index.html').write_text(page('AGI ALPHA Evidence Mission Control',f"<p>Dynamic Evidence Docket registry, workflow launchpad, replay portal, safety ledger, and public scoreboard for AGI ALPHA experiments.</p><p>{CLAIM_BOUNDARY}</p><h3>Recent Runs</h3><table>{rows}</table>"))
    o.joinpath('404.html').write_text(page('Not Found','<a href="/agialpha-first-real-loop/">Back to hub</a>'))
    o.joinpath('experiments/index.html').write_text(page('Experiments',''.join([f"<li><a href='/agialpha-first-real-loop/experiments/{e['slug']}/'>{e['slug']}</a></li>" for e in exps])))
    o.joinpath('workflows/index.html').write_text(page('Workflows',''.join([f"<li><a href='/agialpha-first-real-loop/workflows/{(w.get('slug') or Path(w.get('workflow_file','')).stem)}/'>{w.get('name') or w.get('workflow_name') or Path(w.get('workflow_file','')).name}</a></li>" for w in wfs])))
    o.joinpath('runs/index.html').write_text(page('Runs',''.join([f"<li><a href='/agialpha-first-real-loop/runs/{r['run_id']}/'>{r['run_id']}</a></li>" for r in runs])))
    for s in ['artifacts','external-review','safety','legacy','falsification']:
        o.joinpath(s,'index.html').write_text(page(s.title(),'<a href="/agialpha-first-real-loop/">Back</a>'))

    launch_rows=''.join([f"<tr><td>{w.get('name') or w.get('workflow_name') or Path(w.get('workflow_file','')).name}</td><td>{w.get('workflow_file')}</td><td><a href='https://github.com/MontrealAI/agialpha-first-real-loop/actions/workflows/{Path(w.get('workflow_file','')).name}'>{w.get('workflow_file')}</a></td><td><code>{w.get('gh_command') or 'workflow_dispatch not enabled'}</code></td></tr>" for w in wfs])
    o.joinpath('launchpad/index.html').write_text(page('Workflow Launchpad', f"<p>Click the button, then click Run workflow on GitHub.</p><table>{launch_rows}</table>"))
    strong_rsi_source = Path('strong-rsi/index.html')
    if strong_rsi_source.exists():
        o.joinpath('strong-rsi/index.html').write_text(
            strong_rsi_source.read_text(encoding='utf-8'),
            encoding='utf-8',
        )

    for exp,runs_exp in by_exp.items():
        ep=o/'experiments'/exp; (ep/'runs').mkdir(parents=True,exist_ok=True)
        latest=runs_exp[0]
        run_rows=''.join([f"<tr><td>{r['run_id']}</td><td>{r.get('status')}</td><td><a href='{r.get('run_url','#')}'>actions</a></td></tr>" for r in runs_exp])
        ep.joinpath('index.html').write_text(page(exp,f"<div>claim boundary: {html.escape(latest.get('claim_boundary','missing'))}</div><div>latest status: {latest.get('status')}</div><div>safety incidents: {latest.get('metrics',{}).get('safety_incidents','not_reported')}</div><table>{run_rows}</table><a href='/agialpha-first-real-loop/'>Back to hub</a>"))
    custom_experiment_source = Path('experiments/rsi-governor-001/index.html')
    if custom_experiment_source.exists() and 'rsi-governor-001' not in by_exp:
        exp_dir = o / 'experiments' / 'rsi-governor-001'
        exp_dir.mkdir(parents=True, exist_ok=True)
        exp_dir.joinpath('index.html').write_text(
            custom_experiment_source.read_text(encoding='utf-8'),
            encoding='utf-8',
        )

    for r in runs:
        rp=o/'runs'/r['run_id']; rp.mkdir(parents=True,exist_ok=True)
        rp.joinpath('manifest.json').write_text(json.dumps(r,indent=2))
        rp.joinpath('index.html').write_text(page(r['run_id'],f"<a href='{r.get('run_url','#')}'>GitHub Actions run</a><div>workflow: {r.get('workflow_name')}</div><div>claim boundary: {r.get('claim_boundary')}</div><a href='/agialpha-first-real-loop/experiments/{r.get('experiment_slug')}/'>Experiment</a>"))
        exp_rp=o/'experiments'/r['experiment_slug']/'runs'/r['run_id']; exp_rp.mkdir(parents=True,exist_ok=True)
        exp_rp.joinpath('index.html').write_text(rp.joinpath('index.html').read_text())
        exp_rp.joinpath('manifest.json').write_text(json.dumps(r,indent=2))

    for slug in LEGACY_SLUGS:
        lp=o/slug; lp.mkdir(exist_ok=True)
        target=f"/agialpha-first-real-loop/experiments/{slug}/" if slug in by_exp else '/agialpha-first-real-loop/'
        msg='backfill required' if slug not in by_exp else 'legacy route mapped'
        lp.joinpath('index.html').write_text(page(slug,f"<meta http-equiv='refresh' content='0; url={target}'/><p>{msg}</p><a href='{target}'>Canonical page</a>"))

    o.joinpath('data/runs.json').write_text(json.dumps(runs,indent=2))
    o.joinpath('data/experiments.json').write_text(json.dumps(exps,indent=2))
    o.joinpath('data/workflows.json').write_text(json.dumps(wfs,indent=2))
    o.joinpath('data/latest.json').write_text(json.dumps(runs[0] if runs else {},indent=2))
    o.joinpath('data/safety.json').write_text(json.dumps({'runs':len(runs)},indent=2))
    o.joinpath('data/external_review.json').write_text(json.dumps({'runs':len(runs)},indent=2))
    o.joinpath('data/workflow_catalog.json').write_text(json.dumps({'workflows':wfs},indent=2))
