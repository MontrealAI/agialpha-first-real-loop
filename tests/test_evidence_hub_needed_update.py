import tempfile
import unittest
from pathlib import Path

from agialpha_evidence_hub.needed_update import needed_update


class T(unittest.TestCase):
    def test_needed_update_detects_file_change_then_stabilizes(self):
        with tempfile.TemporaryDirectory() as repo, tempfile.TemporaryDirectory() as registry:
            workflow = Path(repo) / '.github' / 'workflows'
            workflow.mkdir(parents=True)
            tracked = workflow / 'alpha.yml'
            tracked.write_text('name: alpha\n')

            first = needed_update(registry=registry, repo_root=repo)
            self.assertTrue(first['needed'])
            self.assertIn('.github/workflows/alpha.yml', first['changed_files'])

            second = needed_update(registry=registry, repo_root=repo)
            self.assertFalse(second['needed'])

            tracked.write_text('name: alpha\non:\n  workflow_dispatch:\n')
            third = needed_update(registry=registry, repo_root=repo)
            self.assertTrue(third['needed'])


if __name__ == '__main__':
    unittest.main()
