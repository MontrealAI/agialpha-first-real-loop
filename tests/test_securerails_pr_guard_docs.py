import unittest
from pathlib import Path
class T(unittest.TestCase):
  def test_docs(self): self.assertTrue(Path("docs/secure-rails/agentic-pr-guard.md").exists())
