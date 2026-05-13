import json
import pathlib
import subprocess
import unittest


class TestRecursiveSubstrateAutomatedScientificMethod(unittest.TestCase):
    def test_scientific_method_artifacts_exist(self):
        out_dir = pathlib.Path('/tmp/recursive-substrate-test/ai_improves_ai')
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
