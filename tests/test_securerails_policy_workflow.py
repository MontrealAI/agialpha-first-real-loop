import unittest, pathlib
class T(unittest.TestCase):
  def test_workflow(self): self.assertTrue(pathlib.Path(".github/workflows/securerails-policy-kernel-001.yml").exists())
