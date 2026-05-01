import json
import tempfile
import unittest
from pathlib import Path

from agialpha_evidence_hub.registry import update_registry, load_registry


class TestNoRichEvidenceDowngrade(unittest.TestCase):
    def test_sparse_update_does_not_clobber_rich_metrics(self):
        with tempfile.TemporaryDirectory() as d:
            rich = {
                "run_id": "123",
                "experiment_slug": "cyber-sovereign-002",
                "experiment_name": "Cyber Sovereign 002",
                "workflow_name": "cyber-sovereign-002-autonomous",
                "workflow_file": ".github/workflows/cyber-sovereign-002-autonomous.yml",
                "metrics": {
                    "B6_beats_B5_count": 7,
                    "valid_findings_count": 11,
                    "replay_passes": 3,
                },
                "source": "manifest",
            }
            sparse = {
                "run_id": "123",
                "experiment_slug": "cyber-sovereign-002",
                "experiment_name": "Cyber Sovereign 002",
                "workflow_name": "cyber-sovereign-002-autonomous",
                "workflow_file": ".github/workflows/cyber-sovereign-002-autonomous.yml",
                "metrics": {
                    "B6_beats_B5_count": "unavailable",
                },
                "source": "historical_backfill",
            }
            update_registry(d, rich)
            update_registry(d, sparse)
            reg = load_registry(d)
            run = next(r for r in reg["runs"] if r["run_id"] == "123")
            self.assertEqual(run["metrics"]["B6_beats_B5_count"], 7)
            self.assertEqual(run["metrics"]["valid_findings_count"], 11)
            self.assertEqual(run["metrics"]["replay_passes"], 3)


if __name__ == "__main__":
    unittest.main()
