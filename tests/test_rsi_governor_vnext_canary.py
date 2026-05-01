import unittest,subprocess
class T(unittest.TestCase):
    def test_cli(self):
        p=subprocess.run(["python","-m","agialpha_rsi_governor","vnext-canary","--repo-root",".","--out","rsi-governor-runs/test-vnext"],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
