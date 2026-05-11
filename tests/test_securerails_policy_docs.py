import unittest, pathlib
class T(unittest.TestCase):
  def test_docs(self): self.assertTrue(pathlib.Path("docs/secure-rails/policy-kernel.md").exists())
