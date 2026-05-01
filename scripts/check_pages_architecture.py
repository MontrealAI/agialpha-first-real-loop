from pathlib import Path
import re

FORBIDDEN_REFS = [
    'actions/deploy-pages',
    'actions/upload-pages-artifact',
    'github-pages-deploy-action',
    'peaceiris/actions-gh-pages',
    'jamesives/github-pages-deploy-action',
]
FORBIDDEN_CMD_PATTERNS = [
    r'\bgit\s+push\s+.*\bgh-pages\b',
    r'\bgh-pages\b',
    r'\bmkdocs\s+gh-deploy\b',
]
ALLOWED = 'evidence-hub-publish.yml'


def main() -> None:
    violations = []
    for workflow in Path('.github/workflows').glob('*.yml'):
        text = workflow.read_text(encoding='utf-8').lower()
        if workflow.name == ALLOWED:
            continue
        for ref in FORBIDDEN_REFS:
            if ref in text:
                violations.append((workflow.name, ref))
        for cmd_pattern in FORBIDDEN_CMD_PATTERNS:
            if re.search(cmd_pattern, text):
                violations.append((workflow.name, f'cmd:{cmd_pattern}'))

    if violations:
        raise SystemExit(f'forbidden pages deploy references: {violations}')

    central_text = Path('.github/workflows', ALLOWED).read_text(encoding='utf-8').lower()
    for required in ('actions/deploy-pages', 'actions/upload-pages-artifact'):
        if required not in central_text:
            raise SystemExit(f'central publisher missing {required}')

    print('ok')


if __name__ == '__main__':
    main()
