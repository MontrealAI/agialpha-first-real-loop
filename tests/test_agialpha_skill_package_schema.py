import unittest

from agialpha_engine.skill_package import SKILL_TYPES, build_skill_package, has_required_evidence


class TestSkillPackageSchema(unittest.TestCase):
    def test_skill_package_requires_raw_logs_and_allowed_type(self):
        self.assertIn("capability_package", SKILL_TYPES)
        package = build_skill_package(
            source_job_id="job-001",
            source_agent_id="agent-source",
            skill_type="capability_package",
            skill_payload={"sandbox_only": True},
            raw_task_result_ids=["raw-001"],
            proofbundle_id="pb-001",
            evidence_docket_id="ed-001",
        )
        self.assertEqual(package["schema_version"], "agialpha.engine.skill_package.v1")
        self.assertEqual(package["allowed_import_scope"], "sandbox_only")
        self.assertEqual(package["activation_policy"], "inactive_outside_sandbox_until_human_review")
        self.assertIs(has_required_evidence(package), True)

        with self.assertRaises(ValueError):
            build_skill_package(source_job_id="job", source_agent_id="agent", skill_type="bad", skill_payload={}, raw_task_result_ids=["raw"])
        with self.assertRaises(ValueError):
            build_skill_package(source_job_id="job", source_agent_id="agent", skill_type="capability_package", skill_payload={}, raw_task_result_ids=[])
