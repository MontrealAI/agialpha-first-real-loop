import subprocess, unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_page_contains_boundary(self):
        subprocess.run(['python','-m','secure_rails','render','--registry','secure_rails_registry','--out','docs/secure-rails/generated'], check=True)
        txt=Path('docs/secure-rails/generated/index.html').read_text()
        self.assertIn('SecureRails Work Vaults', txt)
        self.assertIn('claim boundary', txt.lower())
