import unittest
from secure_rails_pr_guard.work_vault import build_work_vault
class T(unittest.TestCase):
    def test_vault(self): self.assertEqual(build_work_vault({"pull_request":{"number":1}})["vault_type"],"proof_bound_pr_review")
