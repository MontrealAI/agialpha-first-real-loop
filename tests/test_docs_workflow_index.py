import json
import unittest
from pathlib import Path

class TestDocsWorkflowIndex(unittest.TestCase):
    def test_workflow_index_exists(self):
        data = json.loads(Path('docs/_generated/public-experience/workflow_index.json').read_text())
        self.assertGreater(len(data['workflows']), 0)
