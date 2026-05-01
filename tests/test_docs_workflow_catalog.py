import re
import unittest
from pathlib import Path

class TestWorkflowCatalog(unittest.TestCase):
    def test_catalog_has_required_columns(self):
        text = Path('docs/WORKFLOW_CATALOG.md').read_text(encoding='utf-8')
        self.assertIn('| Workflow file |', text)
        self.assertIn('Pages publisher?', text)

    def test_catalog_maps_to_workflow_files(self):
        catalog = Path('docs/WORKFLOW_CATALOG.md').read_text(encoding='utf-8')
        documented = set(re.findall(r'`([^`]+\.ya?ml)`', catalog))
        workflow_dir = Path('.github/workflows')
        actual = {p.name for p in workflow_dir.glob('*.yml')} | {p.name for p in workflow_dir.glob('*.yaml')}
        self.assertFalse(actual - documented, f'Undocumented workflows: {sorted(actual-documented)}')
        self.assertFalse(documented - actual, f'Missing workflow files: {sorted(documented-actual)}')

if __name__ == '__main__':
    unittest.main()
