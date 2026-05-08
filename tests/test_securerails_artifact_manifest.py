import json, tempfile, pathlib, unittest
from secure_rails.artifact_manifest import build_manifest
class T(unittest.TestCase):
  def test_manifest(self):
    with tempfile.TemporaryDirectory() as d:
      p=pathlib.Path(d); (p/'docs/secure-rails').mkdir(parents=True); (p/'docs/secure-rails/a.md').write_text('x')
      m=build_manifest(str(p),str(p/'out'))
      self.assertTrue(m['artifacts'])
      self.assertIn('not_found',m)
