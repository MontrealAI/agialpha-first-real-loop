import unittest
from pathlib import Path
from agialpha_docs.cli import _audit_claims

class TestNoOverclaim(unittest.TestCase):
    def test_claim_audit_passes_repo_scope(self):
        self.assertEqual(_audit_claims(Path('.').resolve()), 0)

if __name__ == '__main__':
    unittest.main()
