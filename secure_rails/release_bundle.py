from pathlib import Path
import json, hashlib, shutil
from .release_notes import render_notes
from .marketplace_readiness import write_reports

def _sha(p: Path) -> str:
    h = hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

def build_bundle(repo_root: Path, out: Path, manifest: dict):
    out.mkdir(parents=True, exist_ok=True)
    (out / 'release_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    (out / 'CLAIM_BOUNDARY.md').write_text(manifest['claim_boundary'] + '\n', encoding='utf-8')
    (out / 'RELEASE_NOTES.md').write_text(render_notes(manifest), encoding='utf-8')
    (out / 'CUSTOMER_INSTALL.md').write_text((repo_root / 'docs/secure-rails/customer-install-bundle.md').read_text(encoding='utf-8'), encoding='utf-8')
    write_reports(repo_root, out / 'MARKETPLACE_READINESS.md', out / 'marketplace_readiness.json')
    (out / 'EXPORT_PLAN.md').write_text('Future dedicated repository: MontrealAI/securerails-pr-guard-action with root action.yml and no workflow files.\n', encoding='utf-8')
    cust = out / 'customer'; cust.mkdir(exist_ok=True)
    for f in ['customer-securerails-pr-guard.yml', 'customer-pilot-intake-example.json', 'deployment-intake-example.json', 'safety-ledger-example.json']:
        shutil.copy2(repo_root / f'docs/secure-rails/templates/{f}', cust / f)
    docs = out / 'docs'; docs.mkdir(exist_ok=True)
    for f in ['installable-action.md', 'reusable-workflow.md', 'customer-pilot-installation.md', 'work-vaults-mark-sovereigns.md', 'token-utility-policy.md', 'external-repo-security-model.md']:
        shutil.copy2(repo_root / f'docs/secure-rails/{f}', docs / f)
    (docs / 'quickstart.md').write_text('See release docs and CUSTOMER_INSTALL.md\n', encoding='utf-8')
    wf = out / 'workflow'; wf.mkdir(exist_ok=True)
    for f in ['securerails-pr-guard-reusable.yml', 'securerails-agentic-pr-guard-001.yml']:
        src = repo_root / f'.github/workflows/{f}'
        (wf / f).write_text(src.read_text(encoding='utf-8') if src.exists() else 'not_available\n', encoding='utf-8')
    act = out / 'action'; act.mkdir(exist_ok=True)
    for n, s in [('action.yml', repo_root / '.github/actions/securerails-pr-guard/action.yml'), ('README.md', repo_root / '.github/actions/securerails-pr-guard/README.md')]:
        (act / n).write_text(s.read_text(encoding='utf-8') if s.exists() else 'not_available\n', encoding='utf-8')
    files = [p for p in out.rglob('*') if p.is_file() and p.name != 'CHECKSUMS.sha256']
    (out / 'CHECKSUMS.sha256').write_text('\n'.join(f"{_sha(p)}  {p.relative_to(out)}" for p in sorted(files)), encoding='utf-8')
    (out / 'artifact_manifest.json').write_text(json.dumps({'artifacts': [str(p.relative_to(out)) for p in sorted(files)]}, indent=2), encoding='utf-8')
