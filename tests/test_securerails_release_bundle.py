import unittest, tempfile
from pathlib import Path
from secure_rails.release_train import build
from secure_rails.release_validate import validate_bundle
class T(unittest.TestCase):
  def test_bundle(self):
    with tempfile.TemporaryDirectory() as d:
      out=Path(d)/'x'; build(Path('.'),'0.1.0-rc1','rc',out)
      self.assertTrue((out/'CHECKSUMS.sha256').exists())
      self.assertIn('artifact_manifest.json', (out/'CHECKSUMS.sha256').read_text())
      validate_bundle(out)

  def test_validate_fails_missing_required(self):
    with tempfile.TemporaryDirectory() as d:
      out=Path(d)/'x'; build(Path('.'),'0.1.0-rc1','rc',out)
      (out/'RELEASE_NOTES.md').unlink()
      with self.assertRaises(ValueError):
        validate_bundle(out)
