import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class T(unittest.TestCase):
    def test_replay_exits_nonzero_on_failed_fixture(self):
        out = Path(tempfile.mkdtemp()) / 'out'
        subprocess.run([
            'python','-m','secure_rails','e2e-canary','run','--repo-root','.','--fixtures','tests/fixtures/securerails_e2e_canary','--out',str(out)
        ], check=True)
        summary_path = out / '01_fixture_summary.json'
        summary = json.loads(summary_path.read_text())
        summary[0]['status'] = 'fail'
        summary_path.write_text(json.dumps(summary), encoding='utf-8')
        proc = subprocess.run([
            'python','-m','secure_rails','e2e-canary','replay','--input',str(out),'--out',str(out/'04_replay_report.json')
        ])
        self.assertNotEqual(proc.returncode, 0)

    def test_run_manifest_failure_when_fixture_mismatch(self):
        temp_fix = Path(tempfile.mkdtemp()) / 'fixtures'
        shutil.copytree('tests/fixtures/securerails_e2e_canary', temp_fix)
        fx = temp_fix / 'safe_docs_customer_repo' / 'fixture.json'
        data = json.loads(fx.read_text())
        data['expected']['recommendation'] = 'reject'
        fx.write_text(json.dumps(data), encoding='utf-8')
        out = Path(tempfile.mkdtemp()) / 'out'
        subprocess.run(['python','-m','secure_rails','e2e-canary','run','--repo-root','.','--fixtures',str(temp_fix),'--out',str(out)], check=True)
        manifest = json.loads((out/'00_manifest.json').read_text())
        self.assertEqual(manifest['status'], 'failure')


if __name__ == '__main__':
    unittest.main()
