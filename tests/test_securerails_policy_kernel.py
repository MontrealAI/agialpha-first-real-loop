import unittest
from secure_rails.policy_kernel import evaluate_file, load_kernel, validate_kernel

class T(unittest.TestCase):
    def test_kernel(self):
        k=load_kernel('config/securerails_policy_kernel.json')
        self.assertEqual([], validate_kernel(k))
        self.assertNotEqual('allow', k['default_decision'])
        self.assertTrue(k['human_review_required'])
        self.assertFalse(k['auto_merge_allowed'])

if __name__=='__main__': unittest.main()


class TPath(unittest.TestCase):
    def test_evaluate_file_default_kernel_path_independent_of_cwd(self):
        import os
        from pathlib import Path
        cwd = os.getcwd()
        try:
            os.chdir('/tmp')
            decision = evaluate_file(str(Path(cwd) / 'tests/fixtures/securerails_policy/valid_work_vault.json'))
            self.assertIn('decision', decision)
        finally:
            os.chdir(cwd)
