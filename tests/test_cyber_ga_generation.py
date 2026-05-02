import unittest
from pathlib import Path
import json
from agialpha_cyber_ga_sovereign.lifecycle import run_lifecycle

class T(unittest.TestCase):
    def test_generate(self):
        out=Path('cyber-ga-sovereign-runs/test-unit')
        run_lifecycle(Path('.'),1,16,6,3,out)
        self.assertTrue((out/'cyber-ga-sovereign-evidence-docket/evidence-run-manifest.json').exists())

    def test_cycles_honored(self):
        out=Path('cyber-ga-sovereign-runs/test-cycles')
        run_lifecycle(Path('.'),2,4,2,3,out)
        metrics=json.loads((out/'cyber-ga-sovereign-evidence-docket/28_summary_tables/scoreboard.json').read_text())['metrics']
        self.assertEqual(metrics['cycles_executed'],2)
        self.assertEqual(metrics['candidate_defensive_niches_generated'],8)

    def test_autonomous_custom_out(self):
        import subprocess, sys
        out='cyber-ga-sovereign-runs/custom-auto'
        subprocess.run([sys.executable,'-m','agialpha_cyber_ga_sovereign','autonomous','--out',out,'--cycles','1','--candidate-niches','2','--evaluate-niches','1','--local-variants-per-niche','1'],check=True)
        self.assertTrue((Path(out)/'cyber-ga-sovereign-evidence-docket/evidence-run-manifest.json').exists())

    def test_autonomous_manifest_provenance(self):
        import subprocess, sys, json
        out='cyber-ga-sovereign-runs/custom-auto-manifest'
        subprocess.run([sys.executable,'-m','agialpha_cyber_ga_sovereign','autonomous','--out',out],check=True)
        manifest=json.loads((Path(out)/'cyber-ga-sovereign-evidence-docket/evidence-run-manifest.json').read_text())
        self.assertIn('Autonomous', manifest['workflow_name'])
        self.assertTrue(manifest['workflow_file'].endswith('cyber-ga-sovereign-001-autonomous.yml'))

    def test_repo_root_recorded(self):
        import json
        out=Path('cyber-ga-sovereign-runs/repo-root-test')
        run_lifecycle(Path('.'),1,2,1,1,out)
        manifest=json.loads((out/'cyber-ga-sovereign-evidence-docket/evidence-run-manifest.json').read_text())
        self.assertIn('repo_root', manifest)

    def test_policy_pr_requires_evidence(self):
        import subprocess, sys
        proc=subprocess.run([sys.executable,'-m','agialpha_cyber_ga_sovereign','policy-pr','--docket','cyber-ga-sovereign-runs/missing-policy-docket'],check=False)
        self.assertNotEqual(proc.returncode,0)
