import unittest, tempfile, subprocess, sys, json
from pathlib import Path

class T(unittest.TestCase):
    def test_cmd(self):
        with tempfile.TemporaryDirectory() as td:
            subprocess.check_call([sys.executable,'-m','agialpha_ascension_scorecard','build-scorecard','--repo-root','.','--out',td])
            subprocess.check_call([sys.executable,'-m','agialpha_ascension_scorecard','run-open-rsi-eval','--repo-root','.','--out',td,'--task-count','16'])
            subprocess.check_call([sys.executable,'-m','agialpha_ascension_scorecard','evaluate-archive-reuse','--repo-root','.','--run',td])
            subprocess.check_call([sys.executable,'-m','agialpha_ascension_scorecard','value-to-capacity','--run',td])
            subprocess.check_call([sys.executable,'-m','agialpha_ascension_scorecard','replay','--run',td])
            subprocess.check_call([sys.executable,'-m','agialpha_ascension_scorecard','falsification-audit','--run',td])
            subprocess.check_call([sys.executable,'-m','agialpha_ascension_scorecard','validate','--run',td])
            self.assertTrue((Path(td)/'02_open_rsi_eval/open_rsi_eval.json').exists())
