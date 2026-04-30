from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agialpha_helios2.core import run_experiment, external_replay, scaling_run, audit_run, adapters_run


class Helios2Tests(unittest.TestCase):
    def test_helios2_run_generates_docket(self):
        with TemporaryDirectory() as d:
            out = Path(d) / "out"
            docs = Path(d) / "docs"
            summary = run_experiment(out, docs=docs)
            self.assertEqual(summary["B6_beats_B5_count"], summary["transfer_task_count"])
            self.assertEqual(summary["safety_incidents"], 0)
            self.assertTrue((out / "helios-002-evidence-docket" / "00_manifest.json").exists())
            self.assertTrue((docs / "helios-002" / "index.html").exists())

    def test_helios2_external_replay_and_auxiliary_runs(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            run_experiment(root / "source")
            replay = external_replay(root / "replay", source=root / "source")
            scaling = scaling_run(root / "scaling")
            audit = audit_run(root / "audit", source=root / "source")
            adapters = adapters_run(root / "adapters")
            self.assertTrue(replay["clean_ci_replay_pass"])
            self.assertEqual(scaling["claim_level"], "L6-CI-proxy")
            self.assertEqual(audit["audit_status"], "pass")
            self.assertGreaterEqual(len(adapters["adapters"]), 5)


if __name__ == "__main__":
    unittest.main()
