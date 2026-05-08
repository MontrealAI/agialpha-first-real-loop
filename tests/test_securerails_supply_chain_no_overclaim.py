import pathlib, unittest
class T(unittest.TestCase):
  def test_no_certified(self):
    bad=['supply-chain certified','SLSA certified','OpenSSF certified','guaranteed security']
    text='\n'.join(pathlib.Path('docs/secure-rails').glob('*.md') and [p.read_text().lower() for p in pathlib.Path('docs/secure-rails').glob('*.md')])
    for b in bad: self.assertNotIn(b,text)
