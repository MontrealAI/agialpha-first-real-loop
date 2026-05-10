import tempfile
import unittest
from pathlib import Path

from secure_rails.release_train import build
from secure_rails.release_validate import validate_bundle


class T(unittest.TestCase):
    def test_validate_bundle_fails_missing_checksum(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'bundle'
            build(Path('.').resolve(), '0.1.0-rc1', 'rc', out)
            (out / 'CHECKSUMS.sha256').unlink()
            with self.assertRaises(ValueError):
                validate_bundle(out)

    def test_validate_bundle_fails_checksum_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'bundle'
            build(Path('.').resolve(), '0.1.0-rc1', 'rc', out)
            (out / 'RELEASE_NOTES.md').write_text('tampered', encoding='utf-8')
            with self.assertRaises(ValueError):
                validate_bundle(out)

    def test_validate_bundle_fails_if_artifact_not_checksumed(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'bundle'
            build(Path('.').resolve(), '0.1.0-rc1', 'rc', out)
            checks = (out / 'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines()
            checks = [ln for ln in checks if 'RELEASE_NOTES.md' not in ln]
            (out / 'CHECKSUMS.sha256').write_text('\n'.join(checks) + '\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                validate_bundle(out)
