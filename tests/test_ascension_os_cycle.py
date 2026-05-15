import json
import tempfile
import unittest
from pathlib import Path
from agialpha_ascension_os import core


class TestAscensionOSCycle(unittest.TestCase):
    def test_run_cycle_creates_artifacts(self):
        with tempfile.TemporaryDirectory() as td:
            run = Path(td) / "run"
            reg = Path(td) / "registry"
            core.run_cycle(Path('.'), run, reg)
            required = [
                "run.json","regulated_boundary_triage.json","enterprise_job_pack.json","insight.json",
                "nova_seeds.json","mark_allocation.json","sovereign_assignment.json","agi_job.json",
                "validator_result.json","proofbundle.json","work_vault.json","settlement_receipt.json",
                "capability_archive.json","open_rsi_eval.json","verified_enterprise_alpha.json",
                "valuation_support_dossier.json","evidence-run-manifest.json","summary.md"
            ]
            for name in required:
                self.assertTrue((run / name).exists(), name)
            self.assertTrue((run / "evidence_docket" / "00_manifest.json").exists())


if __name__ == '__main__':
    unittest.main()
