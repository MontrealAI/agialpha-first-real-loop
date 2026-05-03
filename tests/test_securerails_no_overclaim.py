import pathlib,unittest
class T(unittest.TestCase):
    def test_claim_boundary(self):
        txt=pathlib.Path('docs/secure-rails/work-vaults-mark-sovereigns.md').read_text()
        self.assertIn('No Evidence Docket, no empirical SOTA claim',txt)
