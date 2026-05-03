import pathlib,unittest
class T(unittest.TestCase):
    def test_no_investment_lang(self):
        txt=pathlib.Path('docs/secure-rails/work-vaults-mark-sovereigns.md').read_text().lower()
        self.assertNotIn('guaranteed investment return',txt)
