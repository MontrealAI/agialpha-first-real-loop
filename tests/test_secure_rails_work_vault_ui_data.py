import unittest, subprocess
from pathlib import Path
class T(unittest.TestCase):
    def test_ui_files_generated(self):
        subprocess.run(['python','-m','secure_rails','build-data','--registry','secure_rails_registry','--out','docs/_generated/secure-rails'], check=True)
        for n in ['work_vaults.json','mark_allocations.json','sovereigns.json','settlements.json','summary.json']:
            self.assertTrue((Path('docs/_generated/secure-rails')/n).exists())
