import json, subprocess, tempfile, unittest
from pathlib import Path
SCRIPT=['python','scripts/secure_rails_work_vault_check.py']
class T(unittest.TestCase):
    def run_check(self,obj):
        with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False) as f:
            json.dump(obj,f);p=f.name
        return subprocess.run(SCRIPT+[p],capture_output=True,text=True)
    def test_examples_validate(self):
        for p in ['work-vault-example.json','mark-allocation-example.json','sovereign-example.json','vault-settlement-example.json']:
            r=subprocess.run(SCRIPT+[f'docs/secure-rails/templates/{p}'],capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stdout+r.stderr)
    def test_unsafe_flags_fail(self):
        base=json.loads(Path('docs/secure-rails/templates/work-vault-example.json').read_text())
        for key,val in [('auto_merge_allowed',True),('human_review_required',False),('external_target_scanning_allowed',True),('exploit_execution_allowed',True),('profiling_natural_persons_allowed',True),('automated_decisions_about_natural_persons_allowed',True),('critical_infrastructure_safety_component_reliance_allowed',True)]:
            obj=json.loads(json.dumps(base));obj['scope'][key]=val
            self.assertNotEqual(self.run_check(obj).returncode,0)
