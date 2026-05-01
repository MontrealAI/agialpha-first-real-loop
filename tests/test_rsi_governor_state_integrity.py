import json,unittest
class T(unittest.TestCase):
 def test_state(self): self.assertIn('state_hash_chain',json.load(open('rsi_state/governance_kernel_state.json')))

if __name__=="__main__": unittest.main()
