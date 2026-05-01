import unittest
from agialpha_rsi_governor.promotion import promotion_gate
class T(unittest.TestCase):
 def test_gate(self): self.assertTrue(promotion_gate(0.1,'E3_REPLAYED'))

if __name__=="__main__": unittest.main()
