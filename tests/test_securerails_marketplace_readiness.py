import unittest
from pathlib import Path
from secure_rails.marketplace_readiness import assess
class T(unittest.TestCase):
  def test_needed(self):
    d=assess(Path('.')); self.assertTrue(d['marketplace_dedicated_repo_needed']); self.assertFalse(d['marketplace_publication_allowed_now'])
