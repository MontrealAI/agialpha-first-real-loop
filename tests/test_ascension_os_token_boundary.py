import unittest
from agialpha_ascension_os.core import bfields


class TestTokenBoundary(unittest.TestCase):
    def test_utility_only(self):
        self.assertIn("utility-only", bfields()["token_boundary"])


if __name__ == '__main__':
    unittest.main()
