import unittest

from agialpha_engine.agent_registry import build_agent_registry
from agialpha_engine.agent_skill_manifest import create_agent_skill_manifest, import_skill_into_manifest
from agialpha_engine.skill_import import create_skill_import_event
from agialpha_engine.skill_vault import publish_skill_packages_to_vault
from agialpha_engine.skill_extractor import extract_learning_from_raw_result


class SkillNetworkHelperTests(unittest.TestCase):
    def test_agent_registry_and_manifest_helpers_are_sandbox_bounded(self):
        registry = build_agent_registry(run_id="run-1", roles=["Reviewer Agent", "Validator Agent", "Operator Agent"], seed=123)
        self.assertEqual(len(registry["agents"]), 3)
        self.assertTrue(all(agent["production_activation_allowed"] is False for agent in registry["agents"]))

        manifest = create_agent_skill_manifest(agent_id=registry["agents"][0]["agent_id"])
        updated = import_skill_into_manifest(manifest, "skill-1", "import-1")
        self.assertIs(updated["production_activation_allowed"], False)
        self.assertEqual(updated["imported_skills"][0]["activation_status"], "inactive")
        self.assertIs(updated["imported_skills"][0]["outside_sandbox_activation_allowed"], False)

    def test_skill_vault_and_import_helpers_require_evidence_artifacts(self):
        package = {
            "skill_id": "skill-1",
            "source_job_id": "job-1",
            "source_agent_id": "agent-1",
            "proofbundle_id": "pb-1",
            "evidence_docket_id": "docket-1",
        }
        vault = publish_skill_packages_to_vault(run_id="run-1", skill_packages=[package])
        self.assertIs(vault["skill_packages"][0]["published"], True)
        self.assertEqual(vault["skill_packages"][0]["activation_status"], "inactive_outside_sandbox")

        accepted_import = create_skill_import_event(run_id="run-1", skill_package=package, target_agent_id="agent-2", seed=124)
        self.assertEqual(accepted_import["import_status"], "accepted")
        self.assertIs(accepted_import["outside_sandbox_activation_allowed"], False)

        quarantined_import = create_skill_import_event(
            run_id="run-1", skill_package={"skill_id": "skill-without-proof"}, target_agent_id="agent-2", seed=124
        )
        self.assertEqual(quarantined_import["import_status"], "quarantined")
        self.assertIn("missing ProofBundle", quarantined_import["quarantine_reason"])

    def test_skill_extractor_preserves_every_job_as_reusable_learning(self):
        raw = {"task_id": "job-1", "task_result_id": "raw-1", "passed": True}
        accepted = extract_learning_from_raw_result(raw, 0)
        rejected = extract_learning_from_raw_result(raw, 1)
        failure = extract_learning_from_raw_result({**raw, "failure_reason": "validator_failed"}, 2)
        self.assertEqual(accepted["learning_type"], "accepted_skill_package")
        self.assertEqual(rejected["learning_type"], "rejected_skill_candidate")
        self.assertEqual(failure["learning_type"], "failure_learning_package")
        self.assertTrue(all(row["raw_task_result_id"] == "raw-1" for row in [accepted, rejected, failure]))


if __name__ == "__main__":
    unittest.main()
