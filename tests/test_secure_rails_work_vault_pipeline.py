import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class TestSecureRailsWorkVaultPipeline(unittest.TestCase):
    def test_generates_claim_boundary_and_utility_only_receipt(self):
        fixture = Path("sample_outputs/secure_rails_work_vault/sample_input.json")
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out.json"
            subprocess.run([
                "python",
                "scripts/secure_rails_work_vault_pipeline.py",
                "--input",
                str(fixture),
                "--output",
                str(out),
            ], check=True)
            data = json.loads(out.read_text())
        self.assertEqual(data["schema_version"], "agialpha.securerails.work_vault_record.v1")
        self.assertEqual(
            data["evidence_docket"]["claim_boundary_statement"],
            "No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.",
        )
        self.assertEqual(data["utility_settlement"]["mode"], "$AGIALPHA_UTILITY_ONLY")
        self.assertFalse(data["utility_settlement"]["real_transfer"])

    def test_deterministic_replay_for_identical_input(self):
        fixture = Path("sample_outputs/secure_rails_work_vault/sample_input.json")
        with tempfile.TemporaryDirectory() as td:
            out1 = Path(td) / "out1.json"
            out2 = Path(td) / "out2.json"
            cmd = [
                "python",
                "scripts/secure_rails_work_vault_pipeline.py",
                "--input",
                str(fixture),
            ]
            subprocess.run(cmd + ["--output", str(out1)], check=True)
            subprocess.run(cmd + ["--output", str(out2)], check=True)
            self.assertEqual(out1.read_text(), out2.read_text())



if __name__ == "__main__":
    unittest.main()
