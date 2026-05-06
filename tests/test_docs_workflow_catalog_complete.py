import re
from pathlib import Path

def test_all_workflows_documented_and_guard_detail_present():
    cat = Path('docs/WORKFLOW_CATALOG.md').read_text(encoding='utf-8')
    documented = set(re.findall(r'`([^`]+\.ya?ml)`', cat))
    actual = {p.name for p in Path('.github/workflows').glob('*.yml')} | {p.name for p in Path('.github/workflows').glob('*.yaml')}
    assert not (actual-documented)
    assert 'secure-rails-compliance-guard.yml' in cat
    assert 'does not certify security or provide legal approval' in cat.lower()
