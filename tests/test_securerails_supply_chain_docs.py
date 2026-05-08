import pathlib, unittest
class T(unittest.TestCase):
  def test_docs(self):
    self.assertTrue(pathlib.Path('docs/secure-rails/supply-chain-provenance.md').exists())
