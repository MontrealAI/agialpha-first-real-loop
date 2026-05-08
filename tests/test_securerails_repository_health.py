import tempfile, pathlib, unittest
from secure_rails.repository_health import build_repository_health
class T(unittest.TestCase):
  def test_health(self):
    with tempfile.TemporaryDirectory() as d:
      p=pathlib.Path(d); (p/'docs').mkdir(); (p/'docs/WORKFLOW_CATALOG.md').write_text('x'); (p/'.github/workflows').mkdir(parents=True); (p/'.github/workflows/secure-rails-compliance-guard.yml').write_text('x')
      rec=build_repository_health(str(p),str(p/'h.json'))
      self.assertEqual(rec['checks']['workflow_catalog_documented'],'pass')
