import json, subprocess, unittest
from pathlib import Path

class T(unittest.TestCase):
    def test_discovery_and_summary(self):
        subprocess.run(['python','-m','secure_rails','discover','--repo-root','.','--registry','secure_rails_registry'], check=True)
        subprocess.run(['python','-m','secure_rails','build-data','--registry','secure_rails_registry','--out','docs/_generated/secure-rails'], check=True)
        s=json.loads(Path('docs/_generated/secure-rails/summary.json').read_text())
        self.assertIn('work_vault_count', s)
        self.assertIn('claim_boundary', s)
