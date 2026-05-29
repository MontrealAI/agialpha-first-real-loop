import unittest
from pathlib import Path

from agialpha_evidence_hub.build import build_site


class TestAgialphaSkillNetworkPublicPage(unittest.TestCase):
    def test_skill_network_public_page_is_polished_and_route_backed(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "site"
            build_site("evidence_registry", out)

            skill_page = out / "agialpha-skill-network" / "index.html"
            experiment_page = out / "experiments" / "agialpha-engine-003" / "index.html"
            raw_data = out / "data" / "agialpha-skill-network" / "network_skill_metrics.json"

            self.assertTrue(skill_page.exists())
            self.assertTrue(experiment_page.exists())
            self.assertTrue(raw_data.exists())

            html = skill_page.read_text(encoding="utf-8")
            for expected in [
                "AGI ALPHA Skill Network",
                "Every Job makes an AI Agent smarter",
                "Every new skill can be instantly shared across the network",
                "One Agent learns, all Agents level up",
                "Instant sharing means sandboxed registration/importability",
                "Proof chain",
                "Claim gate",
                "Exponential compounding is a strategic target",
                "Skill propagation graph",
                "Work Vault / $AGIALPHA utility accounting",
                "Raw JSON is secondary",
                "No Evidence Docket, no empirical SOTA claim",
            ]:
                self.assertIn(expected, html)

    def test_mission_control_nav_links_skill_network(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "site"
            build_site("evidence_registry", out)
            index = (out / "index.html").read_text(encoding="utf-8")
            self.assertIn("Skill Network", index)
            self.assertIn("/agialpha-first-real-loop/agialpha-skill-network/", index)


if __name__ == "__main__":
    unittest.main()
