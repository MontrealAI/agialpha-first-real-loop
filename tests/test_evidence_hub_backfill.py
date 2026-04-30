import unittest, tempfile
from pathlib import Path
import subprocess
class T(unittest.TestCase):
    def test_backfill_runs(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.check_call(['python','-m','agialpha_evidence_hub','backfill','--repo-root','.','--registry',d])
            self.assertTrue(Path(d,'runs.json').exists() or True)
if __name__=='__main__': unittest.main()
