import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from agialpha_engine.network_compounding import IMPORTED_SKILL_IMPORT_STATUSES


def _run_network(seed: int = 123):
    td = tempfile.TemporaryDirectory()
    root = Path(td.name)
    run = root / "run"
    reg = root / "reg"
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
            str(seed),
        ]
    )
    return td, run


class NetworkB6VsB5SemanticTest(unittest.TestCase):
    def test_b6_vs_b5_scores_are_derived_from_raw_skill_evidence_not_literal_win_flags(self):
        td, run = _run_network()
        try:
            raw = json.loads((run / "02_jobs/raw_task_results.json").read_text())["raw_task_results"]
            accepted = json.loads(
                (run / "03_skill_extraction/accepted_skill_packages.json").read_text()
            )["accepted_skill_packages"]
            imports = json.loads(
                (run / "05_skill_import/skill_import_events.json").read_text()
            )["skill_import_events"]
            b5 = json.loads(
                (run / "06_heldout_reuse_tests/B5_no_shared_skill.json").read_text()
            )["results"]
            b6 = json.loads(
                (run / "06_heldout_reuse_tests/B6_shared_skill_network.json").read_text()
            )["results"]
            comparison = json.loads((run / "06_heldout_reuse_tests/comparison.json").read_text())

            accepted_raw_ids = {raw_id for skill in accepted for raw_id in skill["raw_task_result_ids"]}
            accepted_raw_scores = [
                float(row["raw_scores"]["score"])
                for row in raw
                if row["raw_task_result_id"] in accepted_raw_ids
            ]
            source_skill_quality = sum(accepted_raw_scores) / len(accepted_raw_scores)
            imported_target_agents = {
                event["target_agent_id"]
                for event in imports
                if event["import_status"] in IMPORTED_SKILL_IMPORT_STATUSES
            }
            import_coverage = len(imported_target_agents) / 3
            validator_coverage = sum(1 for row in raw if row["passed"] is True) / len(raw)
            reusable_skill_signal = max(0.0, source_skill_quality - 0.5) * import_coverage * validator_coverage

            self.assertTrue(accepted_raw_ids)
            self.assertGreater(reusable_skill_signal, 0)
            for i, (control, treatment) in enumerate(zip(b5, b6)):
                task_transfer_factor = 0.20 + (0.03 * ((i + 123) % 5))
                expected_delta = round(reusable_skill_signal * task_transfer_factor, 3)
                self.assertEqual(
                    treatment["reuse_delta_source"],
                    "accepted_raw_skill_scores_x_import_coverage_x_validator_coverage",
                )
                self.assertEqual(treatment["raw_task_result_ids"], sorted(accepted_raw_ids))
                self.assertAlmostEqual(
                    treatment["measured_reuse_delta"],
                    reusable_skill_signal * task_transfer_factor,
                    places=6,
                )
                self.assertIn(
                    round(treatment["success_score"] - control["success_score"], 3),
                    {expected_delta, round(expected_delta + 0.001, 3), round(expected_delta - 0.001, 3)},
                )

            self.assertGreater(comparison["D_shared_skill_network"], comparison["D_no_shared_skill"])
            self.assertEqual(
                comparison["NetworkSkillPropagationLift"],
                round(comparison["D_shared_skill_network"] - comparison["D_no_shared_skill"], 6),
            )
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
