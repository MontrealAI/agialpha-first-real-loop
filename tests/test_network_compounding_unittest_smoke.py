import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestNetworkCompoundingUnittestSmoke(unittest.TestCase):
    def test_run_replay_falsification_validate(self):
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix='agialpha-engine003-smoke-') as td:
            run_dir = Path(td) / 'run'
            registry = Path(td) / 'registry'
            cmds = [
                [
                    sys.executable, '-m', 'agialpha_engine', 'network-compounding-run',
                    '--repo-root', str(repo_root), '--registry', str(registry), '--out', str(run_dir),
                    '--jobs', '5', '--target-agents', '3', '--heldout-tasks', '5', '--seed', '123'
                ],
                [sys.executable, '-m', 'agialpha_engine', 'network-compounding-replay', '--run', str(run_dir)],
                [sys.executable, '-m', 'agialpha_engine', 'network-compounding-falsification-audit', '--run', str(run_dir)],
                [sys.executable, '-m', 'agialpha_engine', 'network-compounding-validate', '--run', str(run_dir)],
            ]
            for cmd in cmds:
                subprocess.run(cmd, cwd=repo_root, check=True)


if __name__ == '__main__':
    unittest.main()
