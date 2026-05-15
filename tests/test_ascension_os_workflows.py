import unittest
from pathlib import Path


class TestAscensionWorkflow(unittest.TestCase):
    def test_workflow_no_pages_or_automerge(self):
        text = Path('.github/workflows/agialpha-ascension-os-001.yml').read_text(encoding='utf-8').lower()
        self.assertNotIn('pages', text)
        self.assertNotIn('auto-merge', text)


if __name__ == '__main__':
    unittest.main()
