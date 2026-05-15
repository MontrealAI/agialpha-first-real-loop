import unittest
from agialpha_ascension_os.core import _regulated_triage


class TestRegulatedBoundary(unittest.TestCase):
    def test_regulated_fixture_blocked(self):
        triage = _regulated_triage("x", {"financial_advice": True})
        self.assertIn(triage["allowed_mode"], ["documentation_only", "blocked_human_review_required"])


if __name__ == '__main__':
    unittest.main()
