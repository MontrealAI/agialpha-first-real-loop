import tempfile, pathlib, json, unittest
from secure_rails.provenance import build_provenance
class T(unittest.TestCase):
  def test_provenance(self):
    with tempfile.TemporaryDirectory() as d:
      p=pathlib.Path(d); mf=p/'m.json'; mf.write_text('{}')
      out=p/'p.json'; rec=build_provenance('.',str(mf),str(out))
      self.assertIn('artifact_manifest_sha256',rec)
