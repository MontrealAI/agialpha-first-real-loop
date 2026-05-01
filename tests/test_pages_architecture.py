import unittest
from pathlib import Path


class TestPagesArchitecture(unittest.TestCase):
    def test_central_publisher_contains_pages_actions(self):
        wf = Path('.github/workflows/evidence-hub-publish.yml').read_text(encoding='utf-8').lower()
        self.assertIn('actions/upload-pages-artifact', wf)
        self.assertIn('actions/deploy-pages', wf)

    def test_only_central_workflow_deploys_pages(self):
        central = 'evidence-hub-publish.yml'
        for p in Path('.github/workflows').glob('*.yml'):
            text = p.read_text(encoding='utf-8').lower()
            if p.name == central:
                continue
            self.assertNotIn('actions/upload-pages-artifact', text)
            self.assertNotIn('actions/deploy-pages', text)


if __name__ == '__main__':
    unittest.main()
