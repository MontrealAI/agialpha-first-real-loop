#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _workflow_files(repo_root: Path) -> list[Path]:
    wf_dir = repo_root / '.github' / 'workflows'
    return sorted(list(wf_dir.glob('*.yml')) + list(wf_dir.glob('*.yaml')))


def main() -> int:
    parser = argparse.ArgumentParser(description='Audit workflow docs coverage and Pages boundary.')
    parser.add_argument('--repo-root', default='.')
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()

    wf_paths = _workflow_files(root)
    wf_names = [p.name for p in wf_paths]

    catalog = (root / 'docs' / 'WORKFLOW_CATALOG.md').read_text(encoding='utf-8')
    documented = sorted(set(re.findall(r'`([^`]+\.ya?ml)`', catalog)))

    undocumented = sorted([w for w in wf_names if w not in documented])
    missing_files = sorted([d for d in documented if d not in wf_names])

    violations: list[str] = []
    for wf in wf_paths:
        text = wf.read_text(encoding='utf-8').lower()
        if 'actions/deploy-pages' in text and wf.name != 'evidence-hub-publish.yml':
            violations.append(wf.name)

    print('undocumented_workflows=', undocumented)
    print('missing_workflow_files=', missing_files)
    print('noncentral_pages_publishers=', violations)

    if undocumented or missing_files or violations:
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
