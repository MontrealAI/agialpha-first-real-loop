import json
import subprocess
import tempfile
from pathlib import Path


def test_network_compounding_metrics_computed_from_raw_logs_without_fixed_wins():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / "run"
        reg = Path(td) / "reg"

        subprocess.check_call(
            [
                "python",
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
