import unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_page_chain(self):
        t=Path('docs/cybersecurity-sovereign/index.html').read_text(encoding='utf-8')
        self.assertIn('α-AGI Insight', t)
        self.assertIn('No Evidence Docket, no empirical SOTA claim', t)
