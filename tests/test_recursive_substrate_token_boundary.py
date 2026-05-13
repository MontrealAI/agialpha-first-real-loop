import json, pathlib, subprocess, unittest

class TestRecursiveSubstrate(unittest.TestCase):
    def test_cli(self):
        subprocess.check_call(["python","-m","agialpha_recursive_substrate","discover","--repo-root",".","--registry","recursive_substrate_registry"])
        subprocess.check_call(["python","-m","agialpha_recursive_substrate","run-cycle","--repo-root",".","--registry","recursive_substrate_registry","--out","/tmp/recursive-substrate-test","--candidate-seeds","16","--evaluate-seeds","6"])
        self.assertTrue(pathlib.Path('/tmp/recursive-substrate-test/14_reports/recursive_substrate_report.json').exists())

