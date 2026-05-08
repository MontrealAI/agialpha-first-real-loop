import json
import tempfile
import unittest
from pathlib import Path

from secure_rails.external_repo import sync_external_repos
from secure_rails.pilot_intake import ingest_intake


class T(unittest.TestCase):
    def test_artifact_sync_generates_ingestable_records(self):
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            cfg = tdp / 'repos.json'
            cfg.write_text(json.dumps({
                'repos': [
                    {'provider': 'github', 'owner': 'example-org', 'name': 'example-repo', 'allow_artifact_api': True}
                ]
            }), encoding='utf-8')
            registry = tdp / 'registry'
            records = sync_external_repos(cfg, limit=5)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]['source']['ingestion_method'], 'artifact_api')

            intake = tdp / 'intake.json'
            intake.write_text(json.dumps(records[0]), encoding='utf-8')
            out = ingest_intake(intake, registry)
            self.assertEqual(out['status'], 'validated')
            db = json.loads((registry / 'registry.json').read_text(encoding='utf-8'))
            self.assertEqual(len(db['records']), 1)
