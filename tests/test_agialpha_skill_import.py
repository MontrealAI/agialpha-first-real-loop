import unittest

from agialpha_engine.agent_registry import build_agent_registry
from agialpha_engine.agent_skill_manifest import build_manifest, import_skill_into_manifest
from agialpha_engine.skill_import import build_skill_import_event


class TestSkillImport(unittest.TestCase):
    def test_skill_import_event_and_manifest_keep_skill_inactive(self):
        agent = build_agent_registry(1, seed=123)[0]
        event = build_skill_import_event(
            skill_id="skill-001", source_agent_id="agent-source", target_agent_id=agent["agent_id"],
            proofbundle_id="pb-001", evidence_docket_id="ed-001", seed=123
        )
        manifest = import_skill_into_manifest(build_manifest(agent), event["skill_id"], proofbundle_id=event["proofbundle_id"], evidence_docket_id=event["evidence_docket_id"])
        self.assertEqual(event["import_status"], "imported")
        self.assertEqual(event["activation_status"], "inactive")
        self.assertIs(event["production_activation_allowed"], False)
        self.assertEqual(manifest["imported_skills"], ["skill-001"])
        self.assertIs(manifest["production_activation_allowed"], False)

    def test_skill_import_without_evidence_is_quarantined(self):
        event = build_skill_import_event(skill_id="skill-002", source_agent_id="agent-source", target_agent_id="agent-target", proofbundle_id="", evidence_docket_id="", seed=1)
        self.assertEqual(event["import_status"], "quarantined_missing_evidence")
        self.assertIs(event["poisoned_skill_quarantined"], True)

    def test_skill_import_treats_pending_evidence_as_missing(self):
        agent = build_agent_registry(1, seed=123)[0]
        event = build_skill_import_event(
            skill_id="skill-pending", source_agent_id="agent-source", target_agent_id=agent["agent_id"],
            proofbundle_id="pending", evidence_docket_id="pending", seed=123
        )
        manifest = import_skill_into_manifest(
            build_manifest(agent), event["skill_id"],
            proofbundle_id=event["proofbundle_id"], evidence_docket_id=event["evidence_docket_id"]
        )
        self.assertEqual(event["import_status"], "quarantined_missing_evidence")
        self.assertIs(event["poisoned_skill_quarantined"], True)
        self.assertNotIn("skill-pending", manifest["imported_skills"])
        self.assertIn("skill-pending", manifest["quarantined_skills"])

