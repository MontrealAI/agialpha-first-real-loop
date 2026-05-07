import subprocess, unittest
import tempfile
import json
from pathlib import Path
class T(unittest.TestCase):
    def test_page_contains_boundary(self):
        subprocess.run(['python','-m','secure_rails','render','--registry','secure_rails_registry','--out','docs/secure-rails/generated'], check=True)
        txt=Path('docs/secure-rails/generated/index.html').read_text()
        self.assertIn('SecureRails Work Vaults', txt)
        self.assertIn('claim boundary', txt.lower())

    def test_render_uses_selected_registry(self):
        with tempfile.TemporaryDirectory() as td:
            reg = Path(td) / 'registry'
            (reg / 'work_vaults').mkdir(parents=True)
            (reg / 'mark_allocations').mkdir(parents=True)
            (reg / 'sovereigns').mkdir(parents=True)
            (reg / 'settlements').mkdir(parents=True)
            (reg / 'work_vaults' / 'a.json').write_text('{"status":"vault_opened"}')
            for part in ('mark_allocations','sovereigns','settlements'):
                (reg / part / 'x.json').write_text('{}')
            subprocess.run(['python','-m','secure_rails','discover','--repo-root','.','--registry',str(reg)], check=True)
            out = Path(td) / 'html'
            subprocess.run(['python','-m','secure_rails','render','--registry',str(reg),'--out',str(out)], check=True)
            data = json.loads((out / '_data' / 'summary.json').read_text())
            expected = len(list((reg / 'work_vaults').glob('*.json')))
            self.assertEqual(data['work_vault_count'], expected)
