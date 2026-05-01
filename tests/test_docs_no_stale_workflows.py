import re
import unittest
from pathlib import Path

class TestNoStaleWorkflows(unittest.TestCase):
    def test_every_workflow_documented(self):
        wf_dir = Path('.github/workflows')
        wf = {p.name for p in wf_dir.glob('*.yml')} | {p.name for p in wf_dir.glob('*.yaml')}
        catalog = Path('docs/WORKFLOW_CATALOG.md').read_text(encoding='utf-8')
        documented = set(re.findall(r'`([^`]+\.ya?ml)`', catalog))
        self.assertFalse(wf - documented, f'Undocumented workflows: {sorted(wf-documented)}')
        self.assertFalse(documented - wf, f'Missing workflow files: {sorted(documented-wf)}')

if __name__ == '__main__':
    unittest.main()
