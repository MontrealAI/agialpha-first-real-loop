import re
from pathlib import Path

DOCS = [
    'docs/START_HERE.md','docs/OPERATOR_QUICKSTART.md','docs/WORKFLOW_LAUNCHPAD.md','docs/WORKFLOW_CATALOG.md','docs/secure-rails/README.md'
]

def test_key_docs_links_resolve():
    for d in DOCS:
        t = Path(d).read_text(encoding='utf-8')
        for link in re.findall(r'\]\(([^)#]+)', t):
            if link.startswith('http') or link.startswith('mailto:'):
                continue
            p = (Path(d).parent / link).resolve()
            assert p.exists(), f'{d} -> {link}'
