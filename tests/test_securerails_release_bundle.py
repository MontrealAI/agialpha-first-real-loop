import json
import tempfile
import unittest
from pathlib import Path

from secure_rails.release_train import build


class T(unittest.TestCase):
    def test_bundle_checksums_include_artifact_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'x'
            build(Path('.'), '0.1.0-rc1', 'rc', out)
            checksums = (out / 'CHECKSUMS.sha256').read_text(encoding='utf-8')
            self.assertIn('artifact_manifest.json', checksums)
            manifest = json.loads((out / 'artifact_manifest.json').read_text(encoding='utf-8'))
            self.assertIn('release_manifest.json', manifest['artifacts'])
