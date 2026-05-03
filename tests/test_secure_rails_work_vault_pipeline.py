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


    def test_default_created_at_is_stable(self):
        payload = {
            "vault_id": "vault-x",
            "defensive_scope": "scope",
            "job_type": "defensive_validation",
            "mark_units": 1,
            "sovereign_id": "sovereign-x",
            "reviewers": ["r1"],
            "status": "completed",
            "decision": "safe_remediation",
            "reviewed_by": "r1",
        }
        with tempfile.TemporaryDirectory() as td:
            inp = Path(td) / "in.json"
            out = Path(td) / "out.json"
            inp.write_text(json.dumps(payload), encoding="utf-8")
            subprocess.run([
                "python", "scripts/secure_rails_work_vault_pipeline.py",
                "--input", str(inp), "--output", str(out),
            ], check=True)
            data = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(data["work_vault"]["created_at"], "1970-01-01T00:00:00+00:00")

    def test_rejects_invalid_enums(self):
        payload = {
            "vault_id": "vault-x",
            "defensive_scope": "scope",
            "job_type": "oops",
            "mark_units": 1,
            "sovereign_id": "sovereign-x",
            "reviewers": ["r1"],
            "status": "running",
            "decision": "auto",
            "reviewed_by": "r1",
        }
        with tempfile.TemporaryDirectory() as td:
            inp = Path(td) / "in.json"
            out = Path(td) / "out.json"
            inp.write_text(json.dumps(payload), encoding="utf-8")
            res = subprocess.run([
                "python", "scripts/secure_rails_work_vault_pipeline.py",
                "--input", str(inp), "--output", str(out),
            ], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)

    def test_rejects_negative_mark_units(self):
        payload = {
            "vault_id": "vault-x",
            "defensive_scope": "scope",
            "job_type": "defensive_validation",
            "mark_units": -3,
            "sovereign_id": "sovereign-x",
            "reviewers": ["r1"],
            "status": "completed",
            "decision": "safe_remediation",
            "reviewed_by": "r1",
        }
        with tempfile.TemporaryDirectory() as td:
            inp = Path(td) / "in.json"
            out = Path(td) / "out.json"
            inp.write_text(json.dumps(payload), encoding="utf-8")
            res = subprocess.run([
                "python", "scripts/secure_rails_work_vault_pipeline.py",
                "--input", str(inp), "--output", str(out),
            ], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)

    def test_rejects_boolean_mark_units(self):
        payload = {
            "vault_id": "vault-x",
            "defensive_scope": "scope",
            "job_type": "defensive_validation",
            "mark_units": True,
            "sovereign_id": "sovereign-x",
            "reviewers": ["r1"],
            "status": "completed",
            "decision": "safe_remediation",
            "reviewed_by": "r1",
        }
        with tempfile.TemporaryDirectory() as td:
            inp = Path(td) / "in.json"
            out = Path(td) / "out.json"
            inp.write_text(json.dumps(payload), encoding="utf-8")
            res = subprocess.run([
                "python", "scripts/secure_rails_work_vault_pipeline.py",
                "--input", str(inp), "--output", str(out),
            ], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)

    def test_rejects_invalid_created_at(self):
        payload = {
            "vault_id": "vault-x",
            "defensive_scope": "scope",
            "job_type": "defensive_validation",
            "mark_units": 1,
            "sovereign_id": "sovereign-x",
            "reviewers": ["r1"],
            "status": "completed",
            "decision": "safe_remediation",
            "reviewed_by": "r1",
            "created_at": "yesterday",
        }
        with tempfile.TemporaryDirectory() as td:
            inp = Path(td) / "in.json"
            out = Path(td) / "out.json"
            inp.write_text(json.dumps(payload), encoding="utf-8")
            res = subprocess.run([
                "python", "scripts/secure_rails_work_vault_pipeline.py",
                "--input", str(inp), "--output", str(out),
            ], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)

    def test_rejects_created_at_without_timezone(self):
        payload = {
            "vault_id": "vault-x",
            "defensive_scope": "scope",
            "job_type": "defensive_validation",
            "mark_units": 1,
            "sovereign_id": "sovereign-x",
            "reviewers": ["r1"],
            "status": "completed",
            "decision": "safe_remediation",
            "reviewed_by": "r1",
            "created_at": "2026-05-03T00:00:00",
        }
        with tempfile.TemporaryDirectory() as td:
            inp = Path(td) / "in.json"
            out = Path(td) / "out.json"
            inp.write_text(json.dumps(payload), encoding="utf-8")
            res = subprocess.run([
                "python", "scripts/secure_rails_work_vault_pipeline.py",
                "--input", str(inp), "--output", str(out),
            ], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)

    def test_rejects_empty_or_non_string_reviewers(self):
        base = {
            "vault_id": "vault-x",
            "defensive_scope": "scope",
            "job_type": "defensive_validation",
            "mark_units": 1,
            "sovereign_id": "sovereign-x",
            "status": "completed",
            "decision": "safe_remediation",
            "reviewed_by": "r1",
        }
        bad_payloads = [
            {**base, "reviewers": []},
            {**base, "reviewers": [123]},
            {**base, "reviewers": [""]},
        ]
        with tempfile.TemporaryDirectory() as td:
            for i, payload in enumerate(bad_payloads):
                inp = Path(td) / f"in_{i}.json"
                out = Path(td) / f"out_{i}.json"
                inp.write_text(json.dumps(payload), encoding="utf-8")
                res = subprocess.run([
                    "python", "scripts/secure_rails_work_vault_pipeline.py",
                    "--input", str(inp), "--output", str(out),
                ], capture_output=True, text=True)
                self.assertNotEqual(res.returncode, 0)


if __name__ == "__main__":
    unittest.main()
