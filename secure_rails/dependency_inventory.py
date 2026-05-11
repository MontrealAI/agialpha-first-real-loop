from __future__ import annotations
import json, re
from pathlib import Path
from datetime import datetime, timezone

LOCK_EXPECTATIONS = {
    'requirements.txt': [],
    'pyproject.toml': ['poetry.lock'],
    'package.json': ['package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'],
    'go.mod': ['go.sum'],
    'Cargo.toml': ['Cargo.lock'],
    'Gemfile': ['Gemfile.lock'],
    'build.gradle': ['gradle.lockfile'],
    'pom.xml': [],
}

CLAIM_BOUNDARY = 'This inventory is advisory metadata and not a vulnerability certification.'

def _dep(name, version, ecosystem, source_file, source_type, confidence='medium'):
    return {
        'name': name, 'version': version, 'ecosystem': ecosystem,
        'source_file': source_file, 'source_type': source_type, 'confidence': confidence,
    }

def collect_dependency_inventory(repo_root: str | Path, repository: str = '') -> dict:
    root = Path(repo_root)
    deps, sources, warnings = [], [], []
    for req in root.rglob('requirements.txt'):
        sources.append(str(req.relative_to(root)))
        for line in req.read_text(encoding='utf-8', errors='ignore').splitlines():
            line=line.strip()
            if not line or line.startswith('#'): continue
            name, version = (line.split('==',1)+[''])[:2] if '==' in line else (line,'')
            deps.append(_dep(name.strip(), version.strip(), 'python', str(req.relative_to(root)), 'manifest', 'high'))
    for pj in root.rglob('package.json'):
        sources.append(str(pj.relative_to(root)))
        try:
            data=json.loads(pj.read_text())
            for sec in ('dependencies','devDependencies'):
                for n,v in (data.get(sec) or {}).items():
                    deps.append(_dep(n,str(v),'npm',str(pj.relative_to(root)),'manifest','high'))
        except Exception:
            warnings.append(f'failed_to_parse:{pj.relative_to(root)}')
    for wf in (root/'.github'/'workflows').glob('*.yml') if (root/'.github'/'workflows').exists() else []:
        sources.append(str(wf.relative_to(root)))
        for line in wf.read_text(encoding='utf-8', errors='ignore').splitlines():
            m=re.search(r'uses:\s*([^@\s]+)@([^\s]+)', line)
            if m:
                deps.append(_dep(m.group(1), m.group(2), 'github_actions', str(wf.relative_to(root)), 'workflow', 'high'))
    for docker in root.rglob('Dockerfile'):
        sources.append(str(docker.relative_to(root)))
        for line in docker.read_text(encoding='utf-8', errors='ignore').splitlines():
            if line.strip().upper().startswith('FROM '):
                image=line.split()[1]
                name, version = (image.split(':',1)+['latest'])[:2]
                deps.append(_dep(name,version,'docker',str(docker.relative_to(root)),'dockerfile','medium'))

    lock_present_paths = set()
    for pat in ['poetry.lock','package-lock.json','yarn.lock','pnpm-lock.yaml','go.sum','Cargo.lock','Gemfile.lock','gradle.lockfile']:
        for p in root.rglob(pat):
            lock_present_paths.add(str(p.relative_to(root)))
    lock_present = sorted({Path(p).name for p in lock_present_paths})
    lock_missing=[]
    for manifest, locks in LOCK_EXPECTATIONS.items():
        for manifest_path in root.rglob(manifest):
            parent = manifest_path.parent
            if locks and not any((parent / lock).exists() for lock in locks):
                for lock in locks:
                    lock_missing.append(str((parent / lock).relative_to(root)))
    return {
        'schema_version':'securerails.dependency_inventory.v1',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'repository': repository,
        'commit_sha':'',
        'sources':sorted(set(sources)),
        'dependencies':deps,
        'lockfiles_present':sorted(set(lock_present)),
        'lockfiles_missing':sorted(set(lock_missing)),
        'warnings':warnings,
        'claim_boundary': CLAIM_BOUNDARY,
    }

def write_inventory(repo_root: str | Path, out: str | Path, repository: str = '') -> dict:
    payload = collect_dependency_inventory(repo_root, repository)
    Path(out).write_text(json.dumps(payload, indent=2), encoding='utf-8')
    return payload
