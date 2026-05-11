
import unittest
from pathlib import Path
from secure_rails.policy_context import build_context
from secure_rails.policy_kernel import evaluate_context
class T(unittest.TestCase):
    def test_github_app(self):
        d=evaluate_context(build_context(Path('tests/fixtures/securerails_policy/invalid_github_app_permissions.json'),'auto'),{})
        self.assertEqual(d['decision'],'allow')
