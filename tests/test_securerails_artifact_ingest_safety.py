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

    def test_zip_binary_quarantine(self):
        with tempfile.TemporaryDirectory() as td:
            z=Path(td)/'b.zip'
            with zipfile.ZipFile(z,'w') as f:f.writestr('a.bin',b'\x00\x01')
            r=ingest_artifact(z)
            self.assertIn('unsupported_binary', r['quarantine_reasons'])


    def test_zip_openai_project_key_quarantine(self):
        with tempfile.TemporaryDirectory() as td:
            z=Path(td)/'c.zip'
            with zipfile.ZipFile(z,'w') as f:f.writestr('a.txt','OPENAI_API_KEY=sk-proj-AbCdEf_1234567890')
            r=ingest_artifact(z)
            self.assertIn('secret_like_content', r['quarantine_reasons'])

    def test_zip_pkcs8_key_quarantine(self):
        with tempfile.TemporaryDirectory() as td:
            z=Path(td)/'d.zip'
            with zipfile.ZipFile(z,'w') as f:f.writestr('a.txt','-----BEGIN PRIVATE KEY-----\nabc')
            r=ingest_artifact(z)
            self.assertIn('secret_like_content', r['quarantine_reasons'])
