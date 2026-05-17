import json
import unittest
from pathlib import Path

class TestDocsExperimentIndex(unittest.TestCase):
    def test_experiment_index_exists(self):
        data = json.loads(Path('docs/_generated/public-experience/experiment_index.json').read_text())
        self.assertTrue(data['experiments'])

    def test_experiment_index_built_from_repo_state(self):
        data = json.loads(Path('docs/_generated/public-experience/experiment_index.json').read_text())
        slugs = {e['slug'] for e in data['experiments']}
        self.assertIn('agialpha-enterprise-pilot-001', slugs)
        self.assertIn('agialpha-ascension-os-001', slugs)
