import json
import tempfile
import unittest
from pathlib import Path

from secure_rails.release_train import build


class T(unittest.TestCase):
    def test_manifest_git_metadata_from_repo_root(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'x'
            build(Path('.').resolve(), '0.1.0-rc1', 'rc', out)
            manifest = json.loads((out / 'release_manifest.json').read_text(encoding='utf-8'))
            self.assertNotEqual(manifest.get('commit_sha'), 'unknown')
            self.assertNotEqual(manifest.get('branch'), 'unknown')
