import unittest

from agialpha_engine.skill_extractor import classify_job, extract_learning_from_job


class TestSkillExtractor(unittest.TestCase):
    def test_skill_extractor_routes_every_job_to_reusable_learning(self):
        job = {"job_id": "job-001", "agent_id": "agent-source", "task_family": "ProofBundle completeness repair"}
        raw = {"task_result_id": "raw-001", "agent_id": "agent-source", "passed": True, "failure_reason": ""}
        accepted = extract_learning_from_job(job, raw, 0)
        rejected = extract_learning_from_job({**job, "job_id": "job-002"}, {**raw, "task_result_id": "raw-002"}, 1)
        failure = extract_learning_from_job({**job, "job_id": "job-003"}, {**raw, "task_result_id": "raw-003", "passed": False, "failure_reason": "validator failed"}, 2)

        self.assertEqual([classify_job(i) for i in range(3)], ["accepted", "rejected", "failure"])
        self.assertEqual(accepted["record"]["raw_task_result_ids"], ["raw-001"])
        self.assertIs(rejected["record"]["quarantined"], True)
        self.assertEqual(failure["record"]["learning_type"], "failure_warning")
        self.assertTrue(all(item["record"]["autonomous_persistence_allowed"] is False for item in [accepted, rejected, failure]))
