import json
import subprocess
import tempfile
import sys
import unittest
from pathlib import Path


def test_network_compounding_metrics_computed_from_raw_logs_without_fixed_wins():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / "run"
        reg = Path(td) / "reg"

        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "agialpha_engine",
                "network-compounding-run",
                "--repo-root",
                ".",
                "--registry",
                str(reg),
                "--out",
                str(run),
                "--jobs",
                "5",
                "--target-agents",
                "3",
                "--heldout-tasks",
                "5",
                "--seed",
                "123",
            ]
        )

        metrics = json.loads((run / "07_metrics/network_skill_metrics.json").read_text())
        comparison = json.loads((run / "06_heldout_reuse_tests/comparison.json").read_text())
        raw_b5 = json.loads((run / "06_heldout_reuse_tests/B5_no_shared_skill.json").read_text())["results"]
        raw_b6 = json.loads((run / "06_heldout_reuse_tests/B6_shared_skill_network.json").read_text())["results"]

        def d_metric(rows):
            return sum(
                row["success_score"]
                * row["validator_pass"]
                * row["replay_pass"]
                * row["proofbundle"]
                * row["docket"]
                / max(1, row["cost_risk_proxy"])
                for row in rows
            ) / len(rows)

        d5 = round(d_metric(raw_b5), 6)
        d6 = round(d_metric(raw_b6), 6)
        lift = round(d6 - d5, 6)

        assert comparison["D_no_shared_skill"] == d5
        assert comparison["D_shared_skill_network"] == d6
        assert comparison["NetworkSkillPropagationLift"] == lift

        assert metrics["B6_shared_skill_advantage_delta"] == lift
        assert metrics["network_skill_propagation_lift"] == lift
        assert metrics["B6_shared_skill_beats_B5_no_shared_skill"] == (d6 > d5)

        assert isinstance(metrics["hard_coded_metric_count"], int)
        assert isinstance(metrics["fake_zero_metric_count"], int)
        assert metrics["hard_coded_metric_count"] >= metrics["fake_zero_metric_count"] >= 0


class NetworkCompoundingNoFixedMetricRegressionTest(unittest.TestCase):
    def test_cli_does_not_reintroduce_fixed_b6_or_vrci_metrics(self):
        """Regression guard for ENGINE-003: no literal B6 win or fixed vRCI shortcuts."""
        cli_text = Path("agialpha_engine/cli.py").read_text(encoding="utf-8")
        network_text = Path("agialpha_engine/network_compounding.py").read_text(encoding="utf-8")
        combined = cli_text + "\n" + network_text
        forbidden_snippets = [
            "baseline_B6_beats_B5=True",
            "baseline_B6_beats_B5 = True",
            "'baseline_B6_beats_B5': True",
            '"baseline_B6_beats_B5": True',
            "vRCI=5",
            "vRCI = 5",
            "'vRCI': 5",
            '"vRCI": 5',
            "'vRCI_value': 5",
            '"vRCI_value": 5',
            "B6_shared_skill_beats_B5_no_shared_skill=True",
            "B6_shared_skill_beats_B5_no_shared_skill = True",
        ]
        for snippet in forbidden_snippets:
            self.assertNotIn(snippet, combined)
        self.assertIn("B6_shared_skill_beats_B5_no_shared_skill", network_text)
        self.assertIn("D_shared_skill_network", network_text)
        self.assertIn("D_no_shared_skill", network_text)
