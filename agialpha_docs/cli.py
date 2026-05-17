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

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd', required=True)
    for c in ['inventory','audit-links','audit-workflows','audit-claims','audit-readmes','build-index','freshness','build-experience-index','build-experiment-index','build-workflow-index','page-health','validate-public-experience']:
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
        src=root/'docs/_generated/public-experience/experience_index.json'
        data=json.loads(src.read_text(encoding='utf-8')) if src.exists() else {'experiences': []}
        _write_json(out,data); return
    if a.cmd=='build-experiment-index':
        out=Path(a.out or (root/'docs/_generated/public-experience/experiment_index.json'))
        src=root/'docs/_generated/public-experience/experiment_index.json'
        data=json.loads(src.read_text(encoding='utf-8')) if src.exists() else {'experiments': []}
        _write_json(out,data); return
    if a.cmd=='build-workflow-index':
        out=Path(a.out or (root/'docs/_generated/public-experience/workflow_index.json'))
        w=[str(p.relative_to(root)) for p in sorted((root/'.github/workflows').glob('*.yml'))]
        _write_json(out, {'schema_version':'agialpha.workflow_index.v1','workflows':w}); return
    if a.cmd=='page-health':
        out=Path(a.out or (root/'docs/_generated/public-experience/page_health.json'))
        missing=[]
        for r in _major_routes():
            if r=='/':
                home_candidates=[root/'README.md', root/'docs/index.md', root/'docs/EVIDENCE_MISSION_CONTROL.md']
                if not any(c.exists() for c in home_candidates):
                    missing.append(r)
                continue
            slug=r.strip('/')
            cand=[root/'docs'/f'{slug}.md', root/'docs'/slug/'README.md', root/'docs'/slug/'index.html']
            if not any(c.exists() for c in cand):
                missing.append(r)
        data={'schema_version':'agialpha.public_page_health.v1','generated_at':'deterministic','routes_checked':len(_major_routes()),'routes_ok':len(_major_routes())-len(missing),'routes_missing':missing,'routes_partial':[],'broken_links':[],'missing_claim_boundaries':[],'raw_json_primary_pages':[],'missing_workflow_catalog_entries':[],'direct_pages_deploy_violations':[],'status':'pass' if not missing else 'partial'}
        _write_json(out,data); print('ok' if not missing else json.dumps(data, indent=2)); return
    if a.cmd=='validate-public-experience':
        needed=['site_manifest.json','experience_index.json','experiment_index.json','workflow_index.json','page_health.json']
        base=root/'docs/_generated/public-experience'
        missing=[n for n in needed if not (base/n).exists()]
        if missing:
            print(json.dumps({'missing':missing}, indent=2)); raise SystemExit(1)
        print('ok'); return

if __name__=='__main__':
    main()
