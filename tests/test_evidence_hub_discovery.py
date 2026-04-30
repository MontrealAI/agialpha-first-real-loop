import unittest
from agialpha_evidence_hub.discover import discover
class T(unittest.TestCase):
    def test_discover(self):
        d=discover('.')
        self.assertIn('discovered_files', d)
if __name__=='__main__': unittest.main()
