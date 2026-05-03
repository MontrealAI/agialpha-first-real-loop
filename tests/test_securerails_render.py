import pathlib,unittest
class T(unittest.TestCase):
    def test_render_contains_boundary(self):
        txt=pathlib.Path('docs/secure-rails/work-vaults-demo/README.md').read_text()
        self.assertIn('No Evidence Docket, no empirical SOTA claim',txt)
