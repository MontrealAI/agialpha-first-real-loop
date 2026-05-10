import tempfile
import unittest
from pathlib import Path
from secure_rails.marketplace_readiness import assess

class T(unittest.TestCase):
  def test_needed(self):
    d=assess(Path('.')); self.assertTrue(d['marketplace_dedicated_repo_needed']); self.assertFalse(d['marketplace_publication_allowed_now'])

  def test_fail_without_root_action(self):
    with tempfile.TemporaryDirectory() as td:
      root = Path(td)
      (root / '.github/workflows').mkdir(parents=True, exist_ok=True)
      (root / '.github/workflows/demo.yml').write_text('name: demo\n', encoding='utf-8')
      d = assess(root)
      self.assertEqual(d['monorepo_action_ready'], 'fail')
