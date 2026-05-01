import unittest, json
from agialpha_rsi_governor.candidates import generate_candidates
class T(unittest.TestCase):
 def test_candidates(self):
  with open('config/rsi_governance_kernel.json') as f:
   candidates=generate_candidates(json.load(f),2)
  self.assertEqual(len(candidates),2)
  self.assertNotEqual(
   candidates[0]['scoring_weights']['replayability'],
   candidates[1]['scoring_weights']['replayability']
  )
  self.assertNotEqual(candidates[0]['changed_fields'], candidates[1]['changed_fields'])

if __name__=="__main__": unittest.main()
