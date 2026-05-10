import tempfile
import unittest
from pathlib import Path

from secure_rails.release_train import build
from secure_rails.release_validate import validate_bundle


class T(unittest.TestCase):
    def test_missing_checksums_fails(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'bundle'
            build(Path('.').resolve(), '0.1.0-rc1', 'rc', out)
            (out / 'CHECKSUMS.sha256').unlink()
            with self.assertRaises(ValueError):
                validate_bundle(out)

    def test_tampered_artifact_manifest_fails(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'bundle'
            build(Path('.').resolve(), '0.1.0-rc1', 'rc', out)
            (out / 'artifact_manifest.json').write_text('{"artifacts": ["release_manifest.json", "fake.txt"]}', encoding='utf-8')
            with self.assertRaises(ValueError):
                validate_bundle(out)
