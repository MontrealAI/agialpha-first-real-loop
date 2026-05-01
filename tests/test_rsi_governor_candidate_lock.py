import unittest,json
from pathlib import Path
class T(unittest.TestCase):
    def test_lock_then_heldout_declared(self):
        m=json.loads(Path("config/rsi_governance_kernel.json").read_text())
        self.assertTrue(m["promotion"]["require_heldout"])
