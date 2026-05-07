import unittest
from secure_rails_pr_guard.workflow_permissions import review_workflows
class T(unittest.TestCase):
  def test_workflow_risk(self): self.assertTrue(review_workflows("tests/fixtures/securerails_pr_guard/workflow_permission_pr")["risks"])
