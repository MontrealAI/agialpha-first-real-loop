import unittest

from agialpha_engine.skill_package import create_skill_package, evidence_id_present


class SkillPackageSchemaTests(unittest.TestCase):
    def test_create_skill_package_keeps_audit_status_pending_with_real_evidence_ids(self):
        package = create_skill_package(
            skill_id="skill-1",
            source_job_id="job-1",
            source_agent_id="agent-1",
            skill_payload={"template": "safe_replay_template"},
            validated_on_task_ids=["job-1"],
            raw_task_result_ids=["raw-job-1"],
            proofbundle_id="pb-skill-1",
            evidence_docket_id="ed-skill-1",
        )

        self.assertIs(package["proofbundle_id_present"], True)
        self.assertIs(package["evidence_docket_id_present"], True)
        self.assertEqual(package["replay_status"], "pending")
        self.assertEqual(package["falsification_status"], "pending")
        self.assertIs(package["activation_policy"]["replay_required"], True)
        self.assertIs(package["activation_policy"]["falsification_required"], True)

    def test_create_skill_package_allows_explicit_post_audit_pass_statuses(self):
        package = create_skill_package(
            skill_id="skill-1",
            source_job_id="job-1",
            source_agent_id="agent-1",
            proofbundle_id="pb-skill-1",
            evidence_docket_id="ed-skill-1",
            replay_status="pass",
            falsification_status="pass",
        )

        self.assertEqual(package["replay_status"], "pass")
        self.assertEqual(package["falsification_status"], "pass")

    def test_create_skill_package_rejects_unknown_audit_status(self):
        with self.assertRaisesRegex(ValueError, "replay_status must be one of"):
            create_skill_package(
                skill_id="skill-1",
                source_job_id="job-1",
                source_agent_id="agent-1",
                replay_status="passed_by_id",
            )

    def test_evidence_id_present_treats_placeholders_as_absent(self):
        self.assertIs(evidence_id_present("pb-skill-1"), True)
        self.assertIs(evidence_id_present(" pending "), False)
        self.assertIs(evidence_id_present(None), False)


if __name__ == "__main__":
    unittest.main()
