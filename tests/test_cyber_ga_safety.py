import unittest
from pathlib import Path
import subprocess, sys, json
from agialpha_cyber_ga_sovereign.lifecycle import run_lifecycle

class T(unittest.TestCase):
    def test_safe_pr_fails_without_docket(self):
        p=subprocess.run([sys.executable,'-m','agialpha_cyber_ga_sovereign','safe-pr','--docket','cyber-ga-sovereign-runs/missing-safepr'],capture_output=True)
        self.assertNotEqual(p.returncode,0)

    def test_safe_pr_requires_and_uses_docket(self):
        out=Path('cyber-ga-sovereign-runs/safepr-ok')
        run_lifecycle(Path('.'),1,2,1,1,out)
        subprocess.run([sys.executable,'-m','agialpha_cyber_ga_sovereign','safe-pr','--docket',str(out/'cyber-ga-sovereign-evidence-docket')],check=True)
        report=json.loads((out/'cyber-ga-sovereign-evidence-docket/safe_pr.json').read_text())
        self.assertEqual(report['status'],'pending_human_review')
