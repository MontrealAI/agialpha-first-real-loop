import subprocess
import tempfile
import unittest
from pathlib import Path


class T(unittest.TestCase):
    def test_evaluate_repo_fails_on_reject_decision(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / 'repo'
            out = Path(td) / 'out'
            repo.mkdir()
            (repo / 'bad.md').write_text('achieved agi', encoding='utf-8')
            proc = subprocess.run(['python', '-m', 'secure_rails', 'policy', 'evaluate-repo', '--repo-root', str(repo), '--out', str(out)])
            self.assertNotEqual(proc.returncode, 0)

    def test_evaluate_repo_removes_stale_decision_files(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / 'repo'
            out = Path(td) / 'out'
            repo.mkdir()
            out.mkdir()
            (out / 'decision_9999.json').write_text('{"stale": true}', encoding='utf-8')
            (repo / 'safe.md').write_text('does not claim achieved agi', encoding='utf-8')
            proc = subprocess.run(['python', '-m', 'secure_rails', 'policy', 'evaluate-repo', '--repo-root', str(repo), '--out', str(out)])
            self.assertEqual(proc.returncode, 0)
            self.assertFalse((out / 'decision_9999.json').exists())


if __name__ == '__main__':
    unittest.main()
