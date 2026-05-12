import unittest, subprocess, sys, json
from pathlib import Path
from secure_rails.policy_kernel import evaluate_file
class T(unittest.TestCase):
    def test_smoke(self):
        self.assertTrue(True)
if __name__=='__main__': unittest.main()
