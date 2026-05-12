import subprocess
import tempfile
import unittest
from pathlib import Path


class T(unittest.TestCase):
    def test_evaluate_repo_fails_on_blocking_decisions(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / 'repo'
            out = Path(td) / 'out'
            repo.mkdir()
            (repo / 'bad.md').write_text('We achieved AGI and provide guaranteed security.', encoding='utf-8')
            proc = subprocess.run(['python', '-m', 'secure_rails', 'policy', 'evaluate-repo', '--repo-root', str(repo), '--out', str(out)], capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('blocking_policy_decisions=', proc.stdout + proc.stderr)


if __name__ == '__main__':
    unittest.main()
