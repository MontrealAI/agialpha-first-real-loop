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


def _json_file(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def _as_list(doc, *keys):
    if isinstance(doc, list):
        return doc
    if not isinstance(doc, dict):
        return []
    for key in keys:
        value = doc.get(key)
        if isinstance(value, list):
            return value
    return []


def _metric_card(label, value):
    return f"<div class='metric'><div class='label'>{html.escape(label)}</div><div class='value'>{html.escape(str(value))}</div></div>"


def _render_skill_network_page(repo_root: Path, out_root: Path):
    data_root = repo_root / 'docs' / '_generated' / 'agialpha-skill-network'
    metrics = _json_file(data_root / 'network_skill_metrics.json', {})
    claim_gate = _json_file(data_root / 'claim_gate.json', {})
    skills_doc = _json_file(data_root / 'skill_packages.json', {})
    agents_doc = _json_file(data_root / 'agents.json', {})
    imports_doc = _json_file(data_root / 'skill_imports.json', {})
    manifests_doc = _json_file(data_root / 'agents.json', {})
    failures_doc = _json_file(data_root / 'failure_learning_packages.json', {})
    rejected_doc = _json_file(data_root / 'rejected_skill_candidates.json', {})
    receipts_doc = _json_file(data_root / 'work_vault_receipts.json', {})
    b6_doc = _json_file(data_root / 'b6_vs_b5.json', {})
    lineage_doc = _json_file(data_root / 'lineage_graph.json', {})

    skills = _as_list(skills_doc, 'skill_packages', 'accepted_skill_packages')
    agents = _as_list(agents_doc, 'agents')
    imports = _as_list(imports_doc, 'skill_imports', 'skill_import_events')
    manifests = _as_list(_json_file(data_root / 'agent_skill_manifests.json', {}), 'manifests', 'agent_skill_manifests')
    failures = _as_list(failures_doc, 'failure_learning_packages')
    rejected = _as_list(rejected_doc, 'rejected_skill_candidates')
    receipts = _as_list(receipts_doc, 'receipts')
    skill_imports_by_skill = {}
    for item in imports:
        skill_imports_by_skill.setdefault(item.get('skill_id', 'unknown'), []).append(item.get('target_agent_id', 'not_reported'))

    status_fields = [
        ('jobs run', metrics.get('jobs_run', 'not_reported')),
        ('accepted Skill Packages', metrics.get('accepted_skill_packages', 'not_reported')),
        ('rejected Skill Candidates', metrics.get('rejected_skill_candidates', 'not_reported')),
        ('Failure Learning Packages', metrics.get('failure_learning_packages', 'not_reported')),
        ('skills published', metrics.get('skills_published_to_vault', 'not_reported')),
        ('agents registered', metrics.get('agents_registered', len(agents) if agents else 'not_reported')),
        ('skill imports', metrics.get('skill_import_events', len(imports) if imports else 'not_reported')),
        ('target agents improved', metrics.get('target_agents_improved_on_heldout', 'not_reported')),
        ('held-out tasks evaluated', metrics.get('heldout_tasks_evaluated', 'not_reported')),
        ('B6 beats B5', metrics.get('B6_shared_skill_beats_B5_no_shared_skill', 'not_reported')),
        ('NetworkSkillPropagationLift', metrics.get('network_skill_propagation_lift', 'not_reported')),
        ('CompoundingExponentProxy', metrics.get('compounding_exponent_proxy', 'not_supported')),
        ('exponential compounding supported', metrics.get('exponential_compounding_supported', False)),
        ('replay status', metrics.get('replay_pass_rate', 'not_reported')),
        ('falsification status', metrics.get('falsification_pass', 'not_reported')),
        ('hard safety counters', metrics.get('critical_safety_incidents', 'not_reported')),
    ]
    cards = ''.join(_metric_card(label, value) for label, value in status_fields)

    skill_rows = ''.join(
        '<tr>'
        f"<td>{html.escape(str(skill.get('skill_id', 'not_reported')))}</td>"
        f"<td>{html.escape(str(skill.get('source_job_id', 'not_reported')))}</td>"
        f"<td>{html.escape(str(skill.get('source_agent_id', 'not_reported')))}</td>"
        f"<td>{html.escape(str(skill.get('skill_type', 'not_reported')))}</td>"
        f"<td>{html.escape(str(skill.get('proofbundle_id', 'not_reported')))}</td>"
        f"<td>{html.escape(str(skill.get('evidence_docket_id', 'not_reported')))}</td>"
        f"<td>{html.escape(', '.join(str(x) for x in skill_imports_by_skill.get(skill.get('skill_id'), [])) or 'not_reported')}</td>"
        f"<td>{html.escape(str(metrics.get('network_skill_propagation_lift', 'not_reported')))}</td>"
        f"<td>{html.escape(str(skill.get('allowed_import_scope', 'sandbox_only')))}</td>"
        f"<td>{html.escape(str(skill.get('human_review_status', 'pending')))}</td>"
        '</tr>'
        for skill in skills
    ) or "<tr><td colspan='10'>No accepted Skill Packages reported.</td></tr>"

    manifest_rows = ''.join(
        '<tr>'
        f"<td>{html.escape(str(m.get('agent_id', 'not_reported')))}</td>"
        f"<td>{html.escape(str(m.get('agent_role', 'not_reported')))}</td>"
        f"<td>{html.escape(', '.join(str(x) for x in m.get('imported_skills', [])) or 'none')}</td>"
        f"<td>{html.escape(str(m.get('skill_import_policy', {}).get('auto_activate_allowed', False)))}</td>"
        '</tr>'
        for m in manifests
    ) or "<tr><td colspan='4'>No Agent Skill Manifests reported.</td></tr>"

    failure_items = ''.join(f"<li>{html.escape(str(f.get('failure_learning_id', f.get('candidate_id', 'not_reported'))))}: {html.escape(str(f.get('failure_summary', f.get('rejection_reason', 'preserved for review'))))}</li>" for f in failures + rejected)
    receipt_rows = ''.join(
        '<tr>'
        f"<td>{html.escape(str(r.get('receipt_id', 'not_reported')))}</td>"
        f"<td>{html.escape(str(r.get('skill_id', 'not_reported')))}</td>"
        f"<td>{html.escape(str(r.get('wallet_used', 'not_reported')))}</td>"
        f"<td>{html.escape(str(r.get('custody_used', 'not_reported')))}</td>"
        f"<td>{html.escape(str(r.get('payment_executed', 'not_reported')))}</td>"
        f"<td>{html.escape(str(r.get('token_price_used', 'not_reported')))}</td>"
        '</tr>'
        for r in receipts
    ) or "<tr><td colspan='6'>No utility receipts reported.</td></tr>"

    raw_links = ''.join(
        f"<li><a href='/agialpha-first-real-loop/data/agialpha-skill-network/{name}'>{name}</a></li>"
        for name in [
            'latest.json','agents.json','skill_packages.json','rejected_skill_candidates.json',
            'failure_learning_packages.json','skill_imports.json','network_skill_metrics.json',
            'b6_vs_b5.json','claim_gate.json','lineage_graph.json','work_vault_receipts.json','summary.json'
        ]
    )
    proof_chain = 'AGI Job → Skill Package / Rejected Skill / Failure Learning → ProofBundle → Evidence Docket → Network Skill Vault → Agent Skill Manifest → Held-out Reuse Test → B6 vs B5 → NetworkSkillPropagationLift → Claim Gate → Human Review'
    workflow_buttons = """
      <p class='actions'>
        <a class='btn' href='https://github.com/MontrealAI/agialpha-first-real-loop/actions/workflows/agialpha-engine-003-network-compounding.yml'>Run Network Compounding</a>
        <a class='btn secondary' href='https://github.com/MontrealAI/agialpha-first-real-loop/actions/workflows/agialpha-engine-003-network-replay.yml'>Replay</a>
        <a class='btn secondary' href='https://github.com/MontrealAI/agialpha-first-real-loop/actions/workflows/agialpha-engine-003-network-falsification-audit.yml'>Falsification Audit</a>
        <a class='btn secondary' href='https://github.com/MontrealAI/agialpha-first-real-loop/actions/workflows/agialpha-engine-003-network-claim-gate.yml'>Claim Gate</a>
      </p>
    """
    body = f"""
      <p class='kicker'>AGI ALPHA Skill Network</p>
      <h2>Operating thesis</h2>
      <p><strong>Every Job makes an AI Agent smarter.</strong><br />Every new skill can be instantly shared across the network.<br />One Agent learns, all Agents level up.</p>
      <p class='warning'>Instant sharing means sandboxed registration/importability. Production activation requires validators and human review. Exponential compounding is a strategic target unless the exponential claim gate passes.</p>
      <h2>Proof chain</h2><p>{html.escape(proof_chain)}</p>
      <h2>Claim gate</h2><p><strong>Claim gate status:</strong> {html.escape(str(claim_gate.get('claim_gate_status', 'not_supported')))}</p><p>{html.escape(str(claim_gate.get('supported_wording', 'Networked skill compounding claim not yet supported.')))}</p>
      <h2>Exponential compounding status</h2><p>{html.escape(str(claim_gate.get('exponential_compounding_status', 'Exponential compounding is a strategic target. Current evidence reports local bounded network skill propagation only.')))}</p>
      <h2>Status cards</h2><div class='metric-grid'>{cards}</div>
      <h2>Skill propagation graph</h2><pre>{html.escape(json.dumps(lineage_doc.get('edges', []), indent=2))}</pre>
      <h2>Skill table</h2><table><tr><th>skill</th><th>source job</th><th>source agent</th><th>skill type</th><th>ProofBundle</th><th>Evidence Docket</th><th>imported by</th><th>held-out lift</th><th>activation status</th><th>human review</th></tr>{skill_rows}</table>
      <h2>Agent Skill Manifest panel</h2><table><tr><th>agent</th><th>role</th><th>imported skills</th><th>auto activate</th></tr>{manifest_rows}</table>
      <h2>B6 vs B5 comparison</h2><pre>{html.escape(json.dumps({'D_no_shared_skill': b6_doc.get('D_no_shared_skill', metrics.get('D_no_shared_skill_B5', 'not_reported')), 'D_shared_skill_network': b6_doc.get('D_shared_skill_network', metrics.get('D_shared_skill_network_B6', 'not_reported')), 'NetworkSkillPropagationLift': b6_doc.get('NetworkSkillPropagationLift', metrics.get('network_skill_propagation_lift', 'not_reported'))}, indent=2))}</pre>
      <h2>Failure learning panel</h2><ul>{failure_items or '<li>No rejected or failure-learning packages reported.</li>'}</ul>
      <h2>Work Vault / $AGIALPHA utility accounting</h2><p>$AGIALPHA remains utility-only accounting.</p><table><tr><th>receipt</th><th>skill</th><th>wallet</th><th>custody</th><th>payment</th><th>token price</th></tr>{receipt_rows}</table>
      <h2>Safety and boundaries</h2><p><strong>claim boundary:</strong> {html.escape(str(metrics.get('claim_boundary', CLAIM_BOUNDARY)))}</p><p><strong>token boundary:</strong> {html.escape(str(metrics.get('token_boundary', 'Utility-only; no wallet, custody, payment, trading, KYC/AML, token price, token value, token appreciation, ROI, yield, or investment return.')))}</p><p><strong>regulated boundary:</strong> {html.escape(str(metrics.get('regulated_boundary', 'Regulated-domain decisioning is blocked and requires documentation-only human review.')))}</p>
      <h2>Workflows</h2>{workflow_buttons}
      <h2>Raw JSON links</h2><p>Raw JSON is secondary to the proof-chain UI.</p><ul>{raw_links}</ul><p><a href='/agialpha-first-real-loop/'>Back to hub</a></p>
    """
    page_html = page('AGI ALPHA Skill Network', body)
    route = out_root / 'agialpha-skill-network'
    route.mkdir(parents=True, exist_ok=True)
    route.joinpath('index.html').write_text(page_html, encoding='utf-8')
    exp_route = out_root / 'experiments' / 'agialpha-engine-003'
    exp_route.mkdir(parents=True, exist_ok=True)
    exp_route.joinpath('index.html').write_text(page_html, encoding='utf-8')
    data_out = out_root / 'data' / 'agialpha-skill-network'
    data_out.mkdir(parents=True, exist_ok=True)
    if data_root.exists():
        for src in data_root.glob('*.json'):
            (data_out / src.name).write_text(src.read_text(encoding='utf-8'), encoding='utf-8')

def build_site(registry='evidence_registry', out='_site'):
    runs,exps,wfs=_load(registry)
    repo_root = Path(__file__).resolve().parent.parent
    o=Path(out); o.mkdir(parents=True,exist_ok=True)
    for d in ['data','experiments','workflows','runs','artifacts','legacy','external-review','safety','launchpad','falsification','assets','strong-rsi','secure-rails','agialpha-skill-network']:
        (o/d).mkdir(exist_ok=True)

    o.joinpath('.nojekyll').write_text('')
    o.joinpath('assets/app.css').write_text(':root{--bg:#f7f9fc;--panel:#fff;--panel-2:#f1f5f9;--text:#0f172a;--muted:#475569;--line:#dbe3ef;--accent:#2563eb;--success:#059669;--warning:#d97706;--danger:#dc2626;--info:#0284c7;--shadow:0 8px 30px rgba(15,23,42,.07);--radius:16px}*{box-sizing:border-box}body{margin:0;font-family:Inter,Arial,sans-serif;background:var(--bg);color:var(--text)}.topnav{display:flex;justify-content:space-between;align-items:center;padding:1rem 2rem;border-bottom:1px solid var(--line);background:var(--panel)}.topnav nav a,.brand{margin-right:1rem;color:var(--accent);text-decoration:none}.container{max-width:1200px;margin:2rem auto;padding:0 1rem}.panel{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:1rem 1.25rem}.hero h1{margin-top:0}table{width:100%;border-collapse:collapse}td,th{border:1px solid var(--line);padding:.45rem;text-align:left}.footer{padding:1rem 2rem;color:var(--muted)}.metric-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;margin:1rem 0}.metric{background:var(--panel-2);border:1px solid var(--line);border-radius:12px;padding:.8rem}.metric .label{text-transform:uppercase;color:var(--muted);font-size:.72rem;letter-spacing:.06em}.metric .value{font-size:1.35rem;font-weight:800;margin-top:.25rem}.warning{border-left:4px solid var(--warning);background:#fff7ed;padding:.75rem 1rem}.actions{display:flex;flex-wrap:wrap;gap:.75rem}.btn{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;border-radius:999px;padding:.65rem .9rem;font-weight:700}.btn.secondary{background:#fff;color:var(--accent);border:1px solid var(--line)}pre{white-space:pre-wrap;background:#0f172a;color:#e2e8f0;padding:1rem;border-radius:12px;overflow:auto}')
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
    sr = repo_root / 'docs' / 'secure-rails' / 'generated' / 'index.html'
    if sr.exists():
        o.joinpath('secure-rails/index.html').write_text(sr.read_text(encoding='utf-8'), encoding='utf-8')
    else:
        o.joinpath('secure-rails/index.html').write_text(page('SecureRails Work Vaults','<p>Unavailable</p>'))
    for s in ['artifacts','external-review','safety','legacy','falsification']:
        o.joinpath(s,'index.html').write_text(page(s.title(),'<a href="/agialpha-first-real-loop/">Back</a>'))

    launch_rows=''.join([f"<tr><td>{w.get('name') or w.get('workflow_name') or Path(w.get('workflow_file','')).name}</td><td>{w.get('workflow_file')}</td><td><a href='https://github.com/MontrealAI/agialpha-first-real-loop/actions/workflows/{Path(w.get('workflow_file','')).name}'>{w.get('workflow_file')}</a></td><td><code>{w.get('gh_command') or 'workflow_dispatch not enabled'}</code></td></tr>" for w in wfs])
    o.joinpath('launchpad/index.html').write_text(page('Workflow Launchpad', f"<p>Click the button, then click Run workflow on GitHub.</p><table>{launch_rows}</table>"))
    strong_rsi_source = repo_root / 'strong-rsi' / 'index.html'
    if strong_rsi_source.exists():
        o.joinpath('strong-rsi/index.html').write_text(
            strong_rsi_source.read_text(encoding='utf-8'),
            encoding='utf-8',
        )

    for exp,runs_exp in by_exp.items():
        ep=o/'experiments'/exp; (ep/'runs').mkdir(parents=True,exist_ok=True)
        latest=runs_exp[0]
        run_rows=''.join([f"<tr><td>{r['run_id']}</td><td>{r.get('status')}</td><td><a href='{r.get('run_url','#')}'>actions</a></td></tr>" for r in runs_exp])
        extra = ""
        if exp == 'rsi-governor-001':
            extra = "<p><a href='/agialpha-first-real-loop/strong-rsi/'>Open Strong RSI control room</a></p>"
        ep.joinpath('index.html').write_text(page(exp,f"<div>claim boundary: {html.escape(latest.get('claim_boundary','missing'))}</div><div>latest status: {latest.get('status')}</div><div>safety incidents: {latest.get('metrics',{}).get('safety_incidents','not_reported')}</div><table>{run_rows}</table>{extra}<a href='/agialpha-first-real-loop/'>Back to hub</a>"))
    custom_experiment_source = repo_root / 'experiments' / 'rsi-governor-001' / 'index.html'

    _render_skill_network_page(repo_root, o)

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
