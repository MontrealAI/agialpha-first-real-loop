import unittest
from secure_rails_pr_guard.sovereign import assign_sovereign
class T(unittest.TestCase):
    def test_sov(self): self.assertIn("primary",assign_sovereign({}, {"risks":[]}, [], {}, {"findings":[]}))
