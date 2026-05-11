import unittest
import tempfile
from pathlib import Path
from secure_rails.code_scanning import code_scanning_readiness
class T(unittest.TestCase):
    def test_record(self):
        d=code_scanning_readiness('.')
        self.assertIn(d['status'],['ready','not_ready','not_applicable','not_reported'])

    def test_detects_yaml_codeql_workflow(self):
        with tempfile.TemporaryDirectory() as td:
            wf = Path(td) / '.github' / 'workflows'
            wf.mkdir(parents=True)
            (wf / 'codeql.yaml').write_text('name: codeql', encoding='utf-8')
            (Path(td) / 'main.py').write_text('print(1)', encoding='utf-8')
            d = code_scanning_readiness(td)
            self.assertTrue(d['workflow_present'])
