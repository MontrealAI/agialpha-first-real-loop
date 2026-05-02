import unittest

from agialpha_rsi_governor.adversarial import evaluate_adversarial_tasks
from agialpha_rsi_governor.safe_pr import prepare_safe_pr_plan
from agialpha_rsi_governor.candidate_lock import CandidateLockError, build_candidate_lock_manifest


class TestRsiGovernorHelpers(unittest.TestCase):
    def test_adversarial_task_count_is_single_per_fixture(self):
        kernel = {
            "scoring_weights": {},
            "future_work_recommendation_policy": {},
            "safety_policy": {
                "raw_secret_leak_count": 0,
                "external_target_scan_count": 0,
                "exploit_execution_count": 0,
                "malware_generation_count": 0,
                "social_engineering_content_count": 0,
                "unsafe_automerge_count": 0,
                "critical_safety_incidents": 0,
            },
        }
        tasks = [{"a": 1, "b": 2}, {"x": 3, "y": 4, "z": 5}]
        results = evaluate_adversarial_tasks(kernel, tasks)
        self.assertEqual([r["task_count"] for r in results], [1, 1])


    def test_candidate_lock_fails_on_missing_required_artifacts(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as td:
            candidate = Path(td) / "candidate-001"
            candidate.mkdir()
            (candidate / "candidate_kernel.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(CandidateLockError):
                build_candidate_lock_manifest([candidate])


    def test_prepare_safe_pr_plan_accepts_scoreboard_delta_field(self):
        plan = prepare_safe_pr_plan({"Governance Compounding Advantage": 0.2, "ECI_level": "E3_REPLAYED"})
        self.assertTrue(plan["open_pr"])
        self.assertEqual(plan["promotion_gate"]["delta"], 0.2)

    def test_prepare_safe_pr_plan_uses_boolean_promotion_gate(self):
        plan = prepare_safe_pr_plan({"B6_advantage_delta_vs_B5": 0.2, "ECI_level": "E3_REPLAYED"})
        self.assertTrue(plan["open_pr"])
        self.assertFalse(plan["automerge"])
        self.assertTrue(plan["promotion_gate"]["pass"])


if __name__ == "__main__":
    unittest.main()
