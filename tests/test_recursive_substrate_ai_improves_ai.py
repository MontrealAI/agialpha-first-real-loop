import json
import pathlib
import subprocess
import unittest


class TestRecursiveSubstrateAiImprovesAi(unittest.TestCase):
    def test_ai_improves_ai_outputs_lock_before_heldout(self):
        out_dir = pathlib.Path('/tmp/recursive-substrate-test/ai_improves_ai')
        subprocess.check_call([
            'python', '-m', 'agialpha_recursive_substrate', 'ai-improves-ai',
            '--repo-root', '.', '--registry', 'recursive_substrate_registry',
            '--out', str(out_dir), '--candidate-mechanisms', '6', '--heldout-fixtures', '8'
        ])
        lock_path = out_dir / 'candidate_lock.json'
        heldout_path = out_dir / 'heldout_fixtures.json'
        self.assertTrue(lock_path.exists())
        self.assertTrue(heldout_path.exists())

        lock = json.loads(lock_path.read_text(encoding='utf-8'))
        heldout = json.loads(heldout_path.read_text(encoding='utf-8'))
        self.assertIn('locked_at', lock)
        self.assertIsInstance(heldout, list)
        self.assertGreater(len(heldout), 0)
        self.assertTrue(all(item.get('generated_after_lock') for item in heldout))


if __name__ == '__main__':
    unittest.main()
