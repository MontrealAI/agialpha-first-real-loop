import json, subprocess, unittest
from pathlib import Path

class T(unittest.TestCase):
    def test_discovery_and_summary(self):
        subprocess.run(['python','-m','secure_rails','discover','--repo-root','.','--registry','secure_rails_registry'], check=True)
        subprocess.run(['python','-m','secure_rails','build-data','--registry','secure_rails_registry','--out','docs/_generated/secure-rails'], check=True)
        s=json.loads(Path('docs/_generated/secure-rails/summary.json').read_text())
        self.assertIn('work_vault_count', s)
        self.assertIn('claim_boundary', s)


    def test_discover_bootstraps_indexes_dir(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            reg = Path(td) / 'registry'
            subprocess.run(['python','-m','secure_rails','discover','--repo-root','.','--registry',str(reg)], check=True)
            self.assertTrue((reg / 'indexes' / 'by_status.json').exists())

    def test_by_sovereign_maps_assigned_vaults(self):
        subprocess.run(['python','-m','secure_rails','discover','--repo-root','.','--registry','secure_rails_registry'], check=True)
        by=json.loads(Path('secure_rails_registry/indexes/by_sovereign.json').read_text())
        self.assertIn('workflow-permission-sovereign', by)
        self.assertIn('sr-vault-2026-0001', by['workflow-permission-sovereign'])
