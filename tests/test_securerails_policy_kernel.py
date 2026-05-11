
import unittest
from pathlib import Path
from secure_rails.policy_context import build_context
from secure_rails.policy_kernel import evaluate_context, load_kernel, validate_kernel

K=load_kernel(Path('config/securerails_policy_kernel.json'))
class T(unittest.TestCase):
    def test_kernel(self):
        self.assertEqual(validate_kernel(K),[])
