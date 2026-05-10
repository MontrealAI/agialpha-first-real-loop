import unittest
from pathlib import Path

class T(unittest.TestCase):
  def test_release_workflows_present(self):
    t=Path('.github/workflows/securerails-release-candidate-001.yml').read_text(); self.assertIn('workflow_dispatch',t)

  def test_validate_workflow_tracks_marketplace_files(self):
    t=Path('.github/workflows/securerails-release-validate-001.yml').read_text()
    self.assertIn('schemas/securerails_marketplace_readiness.schema.json', t)
    self.assertIn('schemas/securerails_export_plan.schema.json', t)
    self.assertIn('config/securerails_marketplace_readiness_policy.json', t)
