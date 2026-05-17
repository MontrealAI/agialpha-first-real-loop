import json
import unittest
from pathlib import Path

class TestDocsExperienceIndex(unittest.TestCase):
    def test_experience_index_contains_major_experiences(self):
        p = Path('docs/_generated/public-experience/experience_index.json')
        data = json.loads(p.read_text())
        ids = {e['experience_id'] for e in data['experiences']}
        self.assertIn('secure-rails', ids)
        self.assertIn('enterprise-pilot', ids)

    def test_self_improvement_source_doc_correct(self):
        data = json.loads(Path('docs/_generated/public-experience/experience_index.json').read_text())
        item = next(e for e in data['experiences'] if e['experience_id'] == 'self-improvement-gauntlet')
        self.assertIn('docs/self-improvement-gauntlet/README.md', item['source_docs'])

    def test_workflow_launchpad_has_existing_workflow_link(self):
        data = json.loads(Path('docs/_generated/public-experience/experience_index.json').read_text())
        item = next(e for e in data['experiences'] if e['experience_id'] == 'workflow-launchpad')
        self.assertTrue(item['workflow_files'])

    def test_complete_entries_have_workflows(self):
        data = json.loads(Path('docs/_generated/public-experience/experience_index.json').read_text())
        for e in data['experiences']:
            if e['status'] == 'complete':
                self.assertTrue(e['workflow_files'])
