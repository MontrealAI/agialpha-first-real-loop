import unittest, json
from agialpha_rsi_governor.candidates import generate_candidates
class T(unittest.TestCase):
 def test_candidates(self): self.assertEqual(len(generate_candidates(json.load(open('config/rsi_governance_kernel.json')),2)),2)

if __name__=="__main__": unittest.main()
