import unittest
from agialpha_rsi_governor.evaluator import eval_kernel
class T(unittest.TestCase):
 def test_delta(self): self.assertGreater(eval_kernel({},[1],False)['d_governance'], eval_kernel({},[1],True)['d_governance'])

if __name__=="__main__": unittest.main()
