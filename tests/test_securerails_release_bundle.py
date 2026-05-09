import unittest, tempfile
from pathlib import Path
from secure_rails.release_train import build
class T(unittest.TestCase):
  def test_bundle(self):
    with tempfile.TemporaryDirectory() as d:
      out=Path(d)/'x'; build(Path('.'),'0.1.0-rc1','rc',out)
      self.assertTrue((out/'CHECKSUMS.sha256').exists())
