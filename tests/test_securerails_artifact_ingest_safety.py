import tempfile, zipfile, unittest
from pathlib import Path
from secure_rails.artifact_ingest import ingest_artifact
class T(unittest.TestCase):
    def test_zip_slip(self):
        with tempfile.TemporaryDirectory() as td:
            z=Path(td)/'a.zip'
            with zipfile.ZipFile(z,'w') as f:f.writestr('../x.txt','oops')
            r=ingest_artifact(z)
            self.assertIn('zip_slip', r['quarantine_reasons'])
