import os, subprocess, tempfile, pathlib, unittest

class T(unittest.TestCase):
    def test_verify_webhook_requires_secret_env(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'p.json'; p.write_text('{}')
            env=os.environ.copy(); env.pop('SECURERAILS_WEBHOOK_SECRET', None)
            proc=subprocess.run(['python','-m','secure_rails','github-app','verify-webhook','--secret-env','SECURERAILS_WEBHOOK_SECRET','--payload-file',str(p),'--signature','sha256=abc'], env=env)
            self.assertNotEqual(proc.returncode,0)
