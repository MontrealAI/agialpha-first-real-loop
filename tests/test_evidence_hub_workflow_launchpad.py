import json
import subprocess
import unittest


class TestEvidenceHubWorkflowLaunchpad(unittest.TestCase):
    def test_workflow_catalog_generates_gh_commands(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as td:
            registry = Path(td) / 'registry'
            subprocess.run([
                'python','-m','agialpha_evidence_hub','workflow-catalog','--repo-root','.', '--registry', str(registry)
            ], check=True)
            data = json.loads((registry / 'workflow_catalog.json').read_text())
            self.assertTrue(data['workflows'])
            self.assertTrue(any(w['has_workflow_dispatch'] for w in data['workflows']))
            self.assertTrue(any((w.get('gh_command') or '').startswith('gh workflow run') for w in data['workflows']))

if __name__ == '__main__':
    unittest.main()
