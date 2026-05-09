import unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_no_overclaim(self):
        txt='\n'.join(Path(p).read_text(errors='ignore') for p in ['docs/secure-rails/template-bootstrap.md','docs/secure-rails/quebecai-template-setup.md'])
        for bad in ['EU AI Act exempt','certified secure','achieved AGI','achieved ASI']:
            self.assertNotIn(bad, txt)
