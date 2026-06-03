import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class TestAgialphaSkillNetworkGeneratedData(unittest.TestCase):
    def test_generated_data_contains_required_public_json_and_secondary_raw_links(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run = root / "run"
            registry = root / "registry"
            generated = root / "generated"

            subprocess.check_call([
                "python", "-m", "agialpha_engine", "network-compounding-run",
                "--repo-root", ".",
                "--registry", str(registry),
                "--out", str(run),
                "--jobs", "5",
                "--target-agents", "3",
                "--heldout-tasks", "5",
                "--seed", "123",
            ])
            subprocess.check_call(["python", "-m", "agialpha_engine", "network-compounding-replay", "--run", str(run)])
            subprocess.check_call(["python", "-m", "agialpha_engine", "network-compounding-falsification-audit", "--run", str(run)])
            subprocess.check_call([
                "python", "-m", "agialpha_engine", "network-compounding-build-data",
                "--registry", str(registry),
                "--out", str(generated),
            ])

            required = {
                "latest.json",
                "agents.json",
                "skill_packages.json",
                "rejected_skill_candidates.json",
                "failure_learning_packages.json",
                "skill_imports.json",
                "network_skill_metrics.json",
                "b6_vs_b5.json",
                "claim_gate.json",
                "lineage_graph.json",
                "work_vault_receipts.json",
                "summary.json",
            }
            self.assertTrue(required.issubset({p.name for p in generated.glob("*.json")}))

            summary = json.loads((generated / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["hero"], "AGI ALPHA Skill Network")
            self.assertEqual(summary["claim_gate_status"], "supported_local_bounded")
            self.assertTrue(summary["raw_json_secondary"])
            self.assertIn("summary.json", summary["raw_json_links"])
            self.assertIn("Every Job makes an AI Agent smarter.", summary["operating_thesis"])
            self.assertIn("Exponential compounding is a strategic target", summary["exponential_compounding_status"])

            b6_vs_b5 = json.loads((generated / "b6_vs_b5.json").read_text(encoding="utf-8"))
            metrics = json.loads((generated / "network_skill_metrics.json").read_text(encoding="utf-8"))
            self.assertEqual(
                b6_vs_b5["network_skill_propagation_lift"],
                metrics["network_skill_propagation_lift"],
            )
            self.assertTrue(b6_vs_b5["computed_from_raw_logs"])
            self.assertTrue(b6_vs_b5["raw_task_result_ids"])


if __name__ == "__main__":
    unittest.main()
