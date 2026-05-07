import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class T(unittest.TestCase):
    def test_discovery_and_summary(self):
        subprocess.run(['python','-m','secure_rails','discover','--repo-root','.','--registry','secure_rails_registry'], check=True)
        subprocess.run(['python','-m','secure_rails','build-data','--registry','secure_rails_registry','--out','docs/_generated/secure-rails'], check=True)
        s=json.loads(Path('docs/_generated/secure-rails/summary.json').read_text())
        self.assertIn('work_vault_count', s)
        self.assertIn('claim_boundary', s)

    def test_discover_bootstraps_indexes_directory(self):
        with tempfile.TemporaryDirectory() as td:
            reg = Path(td) / 'new_registry'
            subprocess.run(['python','-m','secure_rails','discover','--repo-root','.','--registry',str(reg)], check=True)
            self.assertTrue((reg / 'indexes' / 'by_status.json').exists())

    def test_by_sovereign_uses_outer_sovereign_id(self):
        subprocess.run(['python','-m','secure_rails','discover','--repo-root','.','--registry','secure_rails_registry'], check=True)
        by_sovereign = json.loads(Path('secure_rails_registry/indexes/by_sovereign.json').read_text())
        self.assertIn('workflow-permission-sovereign', by_sovereign)
        self.assertGreater(len(by_sovereign['workflow-permission-sovereign']), 0)
