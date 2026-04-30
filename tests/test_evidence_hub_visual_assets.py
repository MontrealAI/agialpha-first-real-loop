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

if __name__ == '__main__':
    unittest.main()
