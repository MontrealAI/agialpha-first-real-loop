import tempfile, json, unittest
from pathlib import Path
from secure_rails.canary_runner import run_canary

class T(unittest.TestCase):
    def test_run(self):
        out=Path(tempfile.mkdtemp())/'out'
        m=run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),out)
        self.assertEqual(m['fixture_count'],7)
        self.assertTrue((out/'02_runs/safe_docs_customer_repo/work_vault.json').exists())
