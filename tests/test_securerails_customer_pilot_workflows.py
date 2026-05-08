import unittest
from pathlib import Path
import tempfile
import json
import subprocess

class T(unittest.TestCase):
    def test_dispatch_path_uses_event_payload(self):
        t = Path('.github/workflows/securerails-customer-pilot-intake-001.yml').read_text()
        self.assertIn('dispatch-ingest --payload "$GITHUB_EVENT_PATH"', t)

    def test_artifact_sync_command_records_ingestion(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = Path(td) / 'repos.json'
            reg = Path(td) / 'registry'
            cfg.write_text(json.dumps({
                'repos': [{'provider': 'github', 'owner': 'example-org', 'name': 'example-repo', 'allow_artifact_api': False}]
            }), encoding='utf-8')
            subprocess.run([
                'python', '-m', 'secure_rails', 'customer-pilots', 'artifact-sync',
                '--config', str(cfg), '--registry', str(reg), '--limit', '1'
            ], check=True)
            db = json.loads((reg / 'registry.json').read_text(encoding='utf-8'))
            self.assertGreaterEqual(len(db.get('records', [])), 1)
