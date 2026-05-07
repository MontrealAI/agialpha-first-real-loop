import unittest
from secure_rails_pr_guard.mark import allocate_mark
class T(unittest.TestCase):
    def test_mark(self): self.assertIn(allocate_mark({"workflow_files":[]},{"risks":[]},{"violations":[]},{"findings":[]})["risk_tier"],["low","medium","high","critical"])
