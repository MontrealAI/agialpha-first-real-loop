import json
import unittest
from pathlib import Path


class TestDocsExperienceIndex(unittest.TestCase):
    def _load(self):
        return json.loads(Path('docs/_generated/public-experience/experience_index.json').read_text())

    def test_experience_index_contains_major_experiences(self):
        data = self._load()
        ids = {e['experience_id'] for e in data['experiences']}
        self.assertIn('secure-rails', ids)
        self.assertIn('enterprise-pilot', ids)

    def test_self_improvement_source_doc_correct(self):
        data = self._load()
        item = next(e for e in data['experiences'] if e['experience_id'] == 'self-improvement-gauntlet')
        self.assertIn('docs/self-improvement-gauntlet/README.md', item['source_docs'])

    def test_workflow_launchpad_has_existing_workflow_link(self):
        data = self._load()
        item = next(e for e in data['experiences'] if e['experience_id'] == 'workflow-launchpad')
        self.assertTrue(item['workflow_files'])

    def test_complete_entries_have_workflows(self):
        data = self._load()
        for entry in data['experiences']:
            if entry['status'] == 'complete':
                self.assertTrue(entry['workflow_files'])


if __name__ == '__main__':
    unittest.main()
