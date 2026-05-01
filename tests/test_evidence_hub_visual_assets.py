import subprocess
import unittest


class TestEvidenceHubVisualAssets(unittest.TestCase):
    def test_visual_assets_exist_after_build(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / 'site'
            subprocess.run(['python','-m','agialpha_evidence_hub','build','--registry','evidence_registry','--out',str(out)], check=True)
            self.assertTrue((out / 'assets' / 'app.css').exists())
            self.assertTrue((out / 'assets' / 'app.js').exists())
            root = (out / 'index.html').read_text()
            self.assertIn('/agialpha-first-real-loop/assets/app.css', root)
            self.assertIn('class="mission-control"', root)
            self.assertIn('class="panel hero"', root)
            self.assertIn('class="topnav"', root)
            self.assertNotIn('<body><h1>', root)
            self.assertTrue((out / '.nojekyll').exists())

if __name__ == '__main__':
    unittest.main()
