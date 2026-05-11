
import unittest
from pathlib import Path
from secure_rails.policy_context import build_context
from secure_rails.policy_kernel import evaluate_context
class T(unittest.TestCase):
    def test_claims(self):
        d=evaluate_context(build_context(Path('tests/fixtures/securerails_policy/forbidden_positive_overclaim.md'),'auto'),{})
        self.assertEqual(d['decision'],'reject')
