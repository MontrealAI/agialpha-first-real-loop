import pathlib
import shutil
import subprocess
import tempfile
import unittest


class TestRecursiveSubstrateAutomatedScientificMethod(unittest.TestCase):
    def test_scientific_method_artifacts_exist(self):
        temp_root = pathlib.Path(tempfile.mkdtemp(prefix='recursive-substrate-scimethod-'))
        self.addCleanup(lambda: shutil.rmtree(temp_root, ignore_errors=True))
        out_dir = temp_root / 'ai_improves_ai'
        subprocess.check_call([
            'python', '-m', 'agialpha_recursive_substrate', 'ai-improves-ai',
            '--repo-root', '.', '--registry', 'recursive_substrate_registry',
            '--out', str(out_dir), '--candidate-mechanisms', '4', '--heldout-fixtures', '5'
        ])
        for rel in [
            'scientific_method_report.json',
            'replay_report.json',
            'falsification_audit.json',
            'promotion_dossier.md',
            'safe_pr_plan.json',
        ]:
            self.assertTrue((out_dir / rel).exists(), rel)


if __name__ == '__main__':
    unittest.main()
