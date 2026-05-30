import unittest

from agialpha_engine.skill_extractor import extract_job_learning, extract_many_job_learnings


def _raw(job_id="job-1", *, passed=True):
    return {
        "schema_version": "agialpha.engine.raw_task_result.v1",
        "task_result_id": f"raw-{job_id}",
        "raw_task_result_id": f"raw-{job_id}",
        "task_id": job_id,
        "candidate_id": f"cand-{job_id}",
        "agent_id": "agent-1",
        "passed": passed,
        "validator_results": [{"validator_id": "v1", "pass": passed}],
        "raw_scores": {"score": 0.7 if passed else 0.2},
    }


class SkillExtractorSemanticTests(unittest.TestCase):
    def test_extract_job_learning_accepts_only_proof_bound_passing_jobs(self):
        result = extract_job_learning(
            _raw(),
            force_outcome="accepted",
            proofbundle_id="pb-skill-1",
            evidence_docket_id="ed-skill-1",
        )

        self.assertEqual(result["outcome"], "accepted")
        artifact = result["artifact"]
        self.assertEqual(artifact["schema_version"], "agialpha.skill_package.v1")
        self.assertEqual(artifact["raw_task_result_ids"], ["raw-job-1"])
        self.assertEqual(artifact["proofbundle_id"], "pb-skill-1")
        self.assertEqual(artifact["evidence_docket_id"], "ed-skill-1")
        self.assertIs(artifact["activation_policy"]["auto_activate_allowed"], False)

    def test_extract_job_learning_preserves_missing_evidence_as_rejected_candidate(self):
        result = extract_job_learning(_raw("job-2"), force_outcome="accepted")

        self.assertEqual(result["outcome"], "rejected")
        artifact = result["artifact"]
        self.assertEqual(artifact["schema_version"], "agialpha.rejected_skill_candidate.v1")
        self.assertEqual(artifact["raw_task_result_ids"], ["raw-job-2"])
        self.assertIs(artifact["quarantine_required"], True)

    def test_extract_job_learning_preserves_failed_jobs_as_failure_learning(self):
        result = extract_job_learning(_raw("job-3", passed=False), force_outcome="accepted")

        self.assertEqual(result["outcome"], "failure")
        artifact = result["artifact"]
        self.assertEqual(artifact["schema_version"], "agialpha.failure_learning_package.v1")
        self.assertEqual(artifact["raw_task_result_ids"], ["raw-job-3"])
        self.assertIs(artifact["quarantine_required"], True)

    def test_extract_many_job_learnings_never_drops_a_job(self):
        report = extract_many_job_learnings([_raw("job-1"), _raw("job-2"), _raw("job-3", passed=False)])
        produced = {
            row["source_job_id"]
            for bucket in ("accepted_skill_packages", "rejected_skill_candidates", "failure_learning_packages")
            for row in report[bucket]
        }

        self.assertEqual(produced, {"job-1", "job-2", "job-3"})
        self.assertIs(report["every_job_produced_reusable_learning"], True)
        self.assertIs(report["human_review_required"], True)
        self.assertIs(report["autonomous_persistence_allowed"], False)


if __name__ == "__main__":
    unittest.main()
