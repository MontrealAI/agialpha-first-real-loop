import unittest

from agialpha_engine.skill_package import build_skill_package
from agialpha_engine.skill_vault import publish_to_vault


class TestSkillVault(unittest.TestCase):
    def test_skill_vault_publishes_only_proof_bound_skills(self):
        good = build_skill_package(
            source_job_id="job-001", source_agent_id="agent-source", skill_type="capability_package",
            skill_payload={"sandbox_only": True}, raw_task_result_ids=["raw-001"], proofbundle_id="pb-001", evidence_docket_id="ed-001"
        )
        missing = build_skill_package(
            source_job_id="job-002", source_agent_id="agent-source", skill_type="capability_package",
            skill_payload={"sandbox_only": True}, raw_task_result_ids=["raw-002"]
        )
        vault = publish_to_vault([good, missing])
        self.assertIs(vault["append_only"], True)
        self.assertEqual(vault["skills_published_to_vault"], 1)
        self.assertEqual(vault["skill_packages"][0]["activation_status"], "inactive")
        self.assertEqual(vault["rejected_publications"][0]["publication_status"], "rejected_missing_proofbundle_or_evidence_docket")
