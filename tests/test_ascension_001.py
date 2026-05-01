
import json
import pathlib
import tempfile
import unittest

from agialpha_ascension_001.core import run_experiment, replay, audit

class Ascension001Tests(unittest.TestCase):
    def test_run_replay_audit(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td) / "repo"
            root.mkdir()
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "sample.yml").write_text("name: sample\non: workflow_dispatch\njobs:\n  x:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo ok\n")
            (root / "docs" / "helios-001").mkdir(parents=True)
            (root / "docs" / "helios-001" / "index.html").write_text("<html><body>Claim boundary: this does not claim achieved AGI or empirical SOTA.</body></html>")
            out = pathlib.Path(td) / "out"
            manifest = run_experiment(root, out, cycles=2, task_count=4)
            docket = out / "ascension-001-evidence-docket"
            self.assertTrue((docket / "00_manifest.json").exists())
            self.assertEqual(manifest["summary"]["B6_beats_B5_count"], manifest["summary"]["task_count"])
            self.assertEqual(replay(docket)["replay_status"], "pass")
            self.assertEqual(audit(docket)["audit_status"], "pass")

if __name__ == "__main__":
    unittest.main()
