import unittest
from pathlib import Path
from agialpha_docs.cli import _audit_links

class TestDocsLinks(unittest.TestCase):
    def test_links_audit_passes_repo_scope(self):
        self.assertEqual(_audit_links(Path('.').resolve()), 0)

if __name__ == '__main__':
    unittest.main()
