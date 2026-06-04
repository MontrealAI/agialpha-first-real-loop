import unittest
from pathlib import Path

from agialpha_engine.render import render_skill_network_summary


class SkillNetworkRenderTest(unittest.TestCase):
    def test_summary_renders_caveat_proof_chain_and_footer(self):
        text = render_skill_network_summary(
            {
                "jobs_run": 5,
                "accepted_skill_packages": 1,
                "network_skill_propagation_lift": 0.1,
                "exponential_compounding_supported": False,
                "raw_secret_leak_count": 0,
                "unsafe_automerge_count": 0,
            },
            {"claim_gate_status": "supported_local_bounded"},
        )
        self.assertIn("Every Job makes an AI Agent smarter.", text)
        self.assertIn("Instant sharing means sandboxed registration and importability", text)
        self.assertIn("AGI Job → Skill Package / Rejected Skill / Failure Learning", text)
        self.assertIn("NetworkSkillPropagationLift", text)
        self.assertIn("Exponential compounding is a strategic target", text)
        self.assertIn("No Evidence Docket, no empirical SOTA claim", text)
        self.assertIn("unsafe_automerge_count: 0", text)
        self.assertNotIn("empirical SOTA claim supported", text)


    def test_public_skill_network_route_exists_with_required_nav_and_caveat(self):
        page = Path("agialpha-skill-network/index.html")
        self.assertTrue(page.exists())
        text = page.read_text(encoding="utf-8")
        self.assertIn("Skill Network", text)
        self.assertIn("Every Job makes an AI Agent smarter.", text)
        self.assertIn("Instant sharing means sandboxed registration and importability", text)
        self.assertIn("AGI Job</span><span>Skill Package / Rejected Skill / Failure Learning", text)
        self.assertIn("NetworkSkillPropagationLift", text)
        self.assertIn("No Evidence Docket, no empirical SOTA claim", text)


if __name__ == "__main__":
    unittest.main()
