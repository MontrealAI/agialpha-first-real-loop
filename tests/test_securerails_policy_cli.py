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


if __name__ == '__main__':
    unittest.main()
