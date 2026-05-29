import unittest
from pathlib import Path

REQUIRED_DOCS = [
    "README_AGIALPHA_SKILL_NETWORK.md",
    "docs/agialpha-skill-network/README.md",
    "docs/agialpha-skill-network/every-job-teaches.md",
    "docs/agialpha-skill-network/network-skill-vault.md",
    "docs/agialpha-skill-network/agent-skill-manifests.md",
    "docs/agialpha-skill-network/skill-packages.md",
    "docs/agialpha-skill-network/failure-learning-packages.md",
    "docs/agialpha-skill-network/b6-vs-b5-shared-skill.md",
    "docs/agialpha-skill-network/network-skill-propagation-lift.md",
    "docs/agialpha-skill-network/compounding-claim-gate.md",
    "docs/agialpha-skill-network/exponential-compounding-boundary.md",
    "docs/agialpha-skill-network/work-vaults-and-agialpha.md",
    "docs/agialpha-skill-network/replay-and-falsification.md",
    "docs/agialpha-skill-network/human-review-gate.md",
    "docs/agialpha-skill-network/claim-boundary.md",
    "docs/agialpha-skill-network/token-boundary.md",
    "docs/agialpha-skill-network/regulated-boundary.md",
    "docs/agialpha-skill-network/operator-guide.md",
    "docs/agialpha-skill-network/reviewer-guide.md",
]


class TestAgialphaSkillNetworkDocs(unittest.TestCase):
    def test_skill_network_docs_exist_and_state_boundaries(self):
        for doc in REQUIRED_DOCS:
            self.assertTrue(Path(doc).exists(), doc)

        readme = Path("README_AGIALPHA_SKILL_NETWORK.md").read_text(encoding="utf-8")
        self.assertIn("Every Job makes an AI Agent smarter", readme)
        self.assertIn("Instant sharing means sandboxed registration", readme)
        self.assertIn("Production activation requires validators and human review", readme)
        self.assertIn("Exponential compounding is a strategic target", readme)
        self.assertIn("$AGIALPHA remains utility-only", readme)

    def test_workflow_catalog_mentions_engine_003(self):
        catalog = Path("docs/WORKFLOW_CATALOG.md").read_text(encoding="utf-8")
        self.assertIn("AGI ALPHA Engine 003 / Networked Skill Compounding", catalog)
        self.assertIn("agialpha-engine-003-network-compounding.yml", catalog)


if __name__ == "__main__":
    unittest.main()
