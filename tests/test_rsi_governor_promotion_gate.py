import unittest
from agialpha_rsi_governor.promotion import promotion_gate

class T(unittest.TestCase):
    def test_minimum_delta_enforced(self):
        self.assertFalse(promotion_gate(0.149, 'E3_REPLAYED'))
        self.assertTrue(promotion_gate(0.15, 'E3_REPLAYED'))

if __name__ == '__main__':
    unittest.main()
