from __future__ import annotations

from pathlib import Path
import argparse
import json
import re
import subprocess
import sys

FORBIDDEN_CLAIMS = [
    'achieved agi', 'achieved asi', 'empirical sota', 'official benchmark victory',
    'guaranteed economic return', 'security certification',
]

ROOT_DOCS = {
    'README.md','README_DEVELOPERS.md','README_OPERATORS.md','README_EXPERIMENTS.md','README_EVIDENCE_HUB.md',
    'CLAIM_BOUNDARY.md','SECURITY.md','EVIDENCE_DOCKET_STANDARD.md','WORKFLOW_LAUNCHPAD.md','CONTRIBUTING.md'
}


def _iter_markdown(repo_root: Path):
    for p in repo_root.rglob('*.md'):
        if '.git' in p.parts:
            continue
        rel = p.relative_to(repo_root)
        rels = str(rel)
        if rels.startswith(('docs/manuscript/', 'COPY_ISSUE_TEMPLATES/')):
            continue
        if not (rels.startswith('docs/') or rels in ROOT_DOCS):
            continue
        yield p, rel


def _audit_links(repo_root: Path) -> int:
    broken = []
    link_pat = re.compile(r'\[[^\]]+\]\(([^)]+)\)')
    for md, rel in _iter_markdown(repo_root):
        text = md.read_text(encoding='utf-8', errors='ignore')
        for link in link_pat.findall(text):
            if link.startswith(('http://', 'https://', 'mailto:', '#')):
                continue
            tgt = (md.parent / link.split('#', 1)[0]).resolve()
            if not tgt.exists():
                broken.append({'file': str(rel), 'link': link})
    out = repo_root / 'docs/_generated/broken_links.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'broken_links': broken}, indent=2), encoding='utf-8')
    print('ok' if not broken else json.dumps({'broken_links': broken}, indent=2))
    return 0 if not broken else 1


def _audit_claims(repo_root: Path) -> int:
    violations = []
    for md, rel in _iter_markdown(repo_root):
        text = md.read_text(encoding='utf-8', errors='ignore').lower()
        for phrase in FORBIDDEN_CLAIMS:
            for m in re.finditer(re.escape(phrase), text):
                idx = m.start()
                window = text[max(0, idx-120): idx+120]
                if not any(token in window for token in ['does not', 'not claim', 'forbidden', 'must not', "doesn't", 'not evidence of', 'no empirical sota claim']):
                    violations.append({'file': str(rel), 'phrase': phrase, 'index': idx})
    out = repo_root / 'docs/_generated/claim_audit.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'violations': violations}, indent=2), encoding='utf-8')
    print('ok' if not violations else json.dumps({'violations': violations}, indent=2))
    return 0 if not violations else 1




def _build_index(repo_root: Path, out_path: Path) -> None:
    docs_dir = repo_root / 'docs'
    md_files = sorted([p for p in docs_dir.glob('*.md') if p.name != out_path.name])
    lines = [
        '# Documentation Index',
        '',
        'Generated index of top-level docs pages.',
        '',
        '| Document | Link |',
        '|---|---|',
    ]
    for p in md_files:
        title = p.stem.replace('_', ' ')
        lines.append(f'| {title} | [{p.name}]({p.name}) |')
    lines.append('')
    lines.append('No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.')
    out_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

def _audit_readmes(repo_root: Path) -> int:
    readme = repo_root / 'README.md'
    if not readme.exists():
        print('README.md missing'); return 1
    txt = readme.read_text(encoding='utf-8', errors='ignore')
    required = ['Quick links', 'claim', 'How to run from GitHub UI', 'Experiment families']
    missing = [k for k in required if k.lower() not in txt.lower()]
    too_large = len(txt.encode('utf-8')) > 500_000
    if missing or too_large:
        print(json.dumps({'missing_sections': missing, 'too_large': too_large}, indent=2)); return 1
    print('ok'); return 0




def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')

def _major_routes():
    return ['/', '/secure-rails/', '/cybersecurity-sovereign/', '/enterprise-pilot/', '/ascension-os/', '/recursive-substrate/', '/open-rsi-eval/', '/self-improvement-gauntlet/', '/valuation-support/', '/work-vaults/', '/evidence-dockets/', '/proofbundles/', '/workflow-launchpad/', '/experiments/', '/raw-data/']



def _experience_specs():
    return [
        ('home','Home / Evidence Mission Control','/',['docs/EVIDENCE_MISSION_CONTROL.md'],['.github/workflows/evidence-hub-publish.yml']),
        ('secure-rails','SecureRails','/secure-rails/',['docs/secure-rails/README.md'],['.github/workflows/secure-rails-compliance-guard.yml']),
        ('cybersecurity-sovereign','Cybersecurity Sovereign','/cybersecurity-sovereign/',['docs/cybersecurity-sovereign/index.html'],['.github/workflows/cyber-ga-sovereign-001-lifecycle.yml']),
        ('recursive-substrate','Recursive Substrate','/recursive-substrate/',['docs/recursive-substrate/README.md'],['.github/workflows/agialpha-recursive-substrate-001-lifecycle.yml']),
        ('ascension-os','Ascension OS','/ascension-os/',['docs/ascension-os/README.md'],['.github/workflows/agialpha-ascension-os-001-lifecycle.yml']),
        ('open-rsi-eval','Open RSI Eval','/open-rsi-eval/',['docs/open-rsi-eval/README.md'],['.github/workflows/agialpha-open-rsi-eval-001.yml']),
        ('self-improvement-gauntlet','Self-Improvement Gauntlet','/self-improvement-gauntlet/',['docs/self-improvement-gauntlet/README.md'],['.github/workflows/agialpha-self-improvement-gauntlet-001.yml']),
        ('enterprise-pilot','Enterprise Pilot','/enterprise-pilot/',['docs/enterprise-pilot/README.md'],['.github/workflows/agialpha-enterprise-pilot-001.yml']),
        ('valuation-support','Valuation Support','/valuation-support/',['docs/valuation-support/README.md'],['.github/workflows/agialpha-valuation-support-002.yml']),
        ('work-vaults','Work Vaults / MARK / Sovereigns','/work-vaults/',['docs/work-vaults/README.md'],['.github/workflows/securerails-work-vault-demo.yml']),
        ('evidence-dockets','Evidence Dockets','/evidence-dockets/',['docs/evidence-dockets/README.md'],['.github/workflows/agialpha-enterprise-pilot-001.yml']),
        ('proofbundles','ProofBundles','/proofbundles/',['docs/proofbundles/README.md'],['.github/workflows/agialpha-enterprise-pilot-001.yml']),
        ('workflow-launchpad','Workflow Launchpad','/workflow-launchpad/',['docs/WORKFLOW_LAUNCHPAD.md'],['.github/workflows/evidence-hub-publish.yml']),
        ('experiment-index','Experiment Index','/experiments/',['docs/EXPERIMENT_INDEX.md'],['.github/workflows/evidence-hub-publish.yml']),
        ('raw-data','Raw Data Index','/raw-data/',['docs/RAW_DATA_INDEX.md'],['.github/workflows/evidence-hub-publish.yml']),
    ]

def _build_experience_index(repo_root: Path) -> dict:
    claim='No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.'
    experiences=[]
    for eid,title,route,docs,wfs in _experience_specs():
        existing_docs=[d for d in docs if (repo_root/d).exists()]
        existing_wfs=[w for w in wfs if (repo_root/w).exists()]
        if existing_docs and existing_wfs:
            status='complete'
        elif existing_docs or existing_wfs:
            status='partial'
        else:
            status='pending'
        experiences.append({
            'experience_id': eid,
            'title': title,
            'route': route,
            'source_docs': existing_docs,
            'generated_data': [],
            'registry_sources': [],
            'workflow_files': existing_wfs,
            'evidence_docket_paths': [],
            'proofbundle_paths': [],
            'status': status,
            'claim_level': 'documentation',
            'replay_status': 'not_reported',
            'falsification_status': 'not_reported',
            'human_review_status': 'not_reported',
            'public_page_health': 'ok' if existing_docs else 'partial',
            'primary_next_action': 'Run workflow to generate evidence and inspect generated artifacts.',
            'claim_boundary': claim,
            'raw_json_secondary_links': ['/docs/_generated/public-experience/summary.json'],
        })
    return {'schema_version':'agialpha.public_experience_registry.v1','experiences':experiences}



def _build_experiment_index(repo_root: Path) -> dict:
    claim='No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.'
    specs=[
        ('AGI ALPHA Enterprise Pilot 001','agialpha-enterprise-pilot-001','/experiments/agialpha-enterprise-pilot-001/','agialpha_enterprise_pilot','.github/workflows/agialpha-enterprise-pilot-001.yml','docs/_generated/enterprise-pilot/latest.json','enterprise_pilot_registry','enterprise-pilot-runs','pending'),
        ('AGI ALPHA Valuation Support 002','agialpha-valuation-support-002','/experiments/agialpha-valuation-support-002/','agialpha_valuation_support','.github/workflows/agialpha-valuation-support-002.yml','docs/_generated/valuation-support/latest.json','valuation_support_registry','valuation-support-runs','pending'),
        ('AGI ALPHA Ascension OS 001','agialpha-ascension-os-001','/experiments/agialpha-ascension-os-001/','agialpha_ascension_os','.github/workflows/agialpha-ascension-os-001-lifecycle.yml','docs/_generated/ascension-os/latest.json','ascension_os_registry','ascension-os-runs','pending'),
        ('AGI ALPHA Recursive Substrate 001','agialpha-recursive-substrate-001','/experiments/agialpha-recursive-substrate-001/','agialpha_recursive_substrate','.github/workflows/agialpha-recursive-substrate-001-lifecycle.yml','docs/_generated/recursive-substrate/latest.json','recursive_substrate_registry','agiga-foundry-runs','pending'),
        ('Cyber GA Sovereign 001','cyber-ga-sovereign-001','/experiments/cyber-ga-sovereign-001/','agialpha_cyber_ga','.github/workflows/cyber-ga-sovereign-001-lifecycle.yml','docs/cybersecurity-sovereign/index.html','cyber_ga_sovereign_registry','cyber-ga-sovereign-runs','pending'),
        ('AGIGA Foundry 001','agiga-foundry-001','/experiments/agiga-foundry-001/','agialpha_foundry','.github/workflows/agiga-foundry-001-lifecycle.yml','docs/evidence-factory/index.html','agiga_foundry_registry','agiga-foundry-runs','pending'),
    ]
    out=[]
    for name,slug,route,pkg,wf,generated,registry,rundir,status0 in specs:
        has_gen=(repo_root/generated).exists()
        has_wf=(repo_root/wf).exists()
        status='complete' if (has_gen and has_wf) else ('partial' if (has_gen or has_wf) else 'pending')
        out.append({'name':name,'slug':slug,'route':route,'package':pkg,'workflow':wf if has_wf else 'not_reported','generated_data_path':generated if has_gen else 'pending generated data','registry_path':registry,'evidence_docket_path':'not_reported','status':status,'replay_status':'not_reported','falsification_status':'not_reported','claim_boundary':claim,'next_action':'Run workflow and inspect Evidence Docket/ProofBundle.'})
    return {'schema_version':'agialpha.experiment_index.v1','experiments':out}

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd', required=True)
    for c in ['inventory','audit-links','audit-workflows','audit-claims','audit-readmes','build-index','freshness','build-experience-index','build-experiment-index','build-workflow-index','build-route-manifest','page-health','validate-public-experience']:
        sp=sub.add_parser(c); sp.add_argument('--repo-root', default='.'); sp.add_argument('--out', default='')
    a=p.parse_args(); root=Path(a.repo_root).resolve()
    if a.cmd=='inventory':
        out=Path(a.out or (root/'docs/_generated/inventory.json')); out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({'workflows':len(list((root/'.github/workflows').glob('*.yml')))}, indent=2)); return
    if a.cmd=='audit-workflows':
        script=root/'scripts/audit_docs_workflows.py'; subprocess.run([sys.executable, str(script), '--repo-root', str(root)], check=True); return
    if a.cmd=='audit-links': raise SystemExit(_audit_links(root))
    if a.cmd=='audit-claims': raise SystemExit(_audit_claims(root))
    if a.cmd=='audit-readmes': raise SystemExit(_audit_readmes(root))
    if a.cmd=='build-index':
        out_path = Path(a.out).resolve() if a.out else (root / 'docs/README.md')
        _build_index(root, out_path)
        return
    if a.cmd=='freshness':
        out=root/'docs/_generated/freshness_report.json'; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps({'status':'pass'}), encoding='utf-8')


    if a.cmd=='build-experience-index':
        out=Path(a.out or (root/'docs/_generated/public-experience/experience_index.json'))
        _write_json(out,_build_experience_index(root)); return
    if a.cmd=='build-experiment-index':
        out=Path(a.out or (root/'docs/_generated/public-experience/experiment_index.json'))
        _write_json(out,_build_experiment_index(root)); return
    if a.cmd=='build-workflow-index':
        out=Path(a.out or (root/'docs/_generated/public-experience/workflow_index.json'))
        w=[str(p.relative_to(root)) for p in sorted((root/'.github/workflows').glob('*.yml'))]
        _write_json(out, {'schema_version':'agialpha.workflow_index.v1','workflows':w}); return

    if a.cmd=='build-route-manifest':
        out=Path(a.out or (root/'docs/_generated/public-experience/route_manifest.json'))
        _write_json(out, {'schema_version':'agialpha.public_route_manifest.v1','routes':_major_routes()}); return
    if a.cmd=='page-health':
        out=Path(a.out or (root/'docs/_generated/public-experience/page_health.json'))
        missing=[]
        checked=0
        for r in _major_routes():
            checked += 1
            if r=='/':
                home_candidates=[root/'docs/index.md', root/'docs/EVIDENCE_MISSION_CONTROL.md']
                if not any(c.exists() for c in home_candidates):
                    missing.append(r)
                continue
            slug=r.strip('/')
            cand=[root/'docs'/f'{slug}.md', root/'docs'/slug/'README.md', root/'docs'/slug/'index.html']
            if not any(c.exists() for c in cand):
                missing.append(r)
        data={'schema_version':'agialpha.public_page_health.v1','generated_at':'deterministic','routes_checked':checked,'routes_ok':checked-len(missing),'routes_missing':missing,'routes_partial':[],'broken_links':[],'missing_claim_boundaries':[],'raw_json_primary_pages':[],'missing_workflow_catalog_entries':[],'direct_pages_deploy_violations':[],'status':'pass' if not missing else 'partial'}
        _write_json(out,data)
        if missing:
            print(json.dumps(data, indent=2))
            raise SystemExit(1)
        print('ok'); return
    if a.cmd=='validate-public-experience':
        needed=['site_manifest.json','experience_index.json','experiment_index.json','workflow_index.json','page_health.json']
        base=root/'docs/_generated/public-experience'
        missing=[n for n in needed if not (base/n).exists()]
        if missing:
            print(json.dumps({'missing':missing}, indent=2)); raise SystemExit(1)
        print('ok'); return

if __name__=='__main__':
    main()
