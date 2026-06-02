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

    def test_nonzero_hard_safety_counter_fails(self):
        obj=json.loads(Path('docs/secure-rails/templates/work-vault-example.json').read_text())
        obj['hard_safety_counters']['exploit_execution_count']=1
        self.assertNotEqual(self.run_check(obj).returncode,0)

    def test_mark_validators_required_must_be_array(self):
        obj=json.loads(Path('docs/secure-rails/templates/mark-allocation-example.json').read_text())
        obj['validators_required']='claim_boundary_validator'
        self.assertNotEqual(self.run_check(obj).returncode,0)

    def test_boolean_hard_safety_counter_fails(self):
        obj=json.loads(Path('docs/secure-rails/templates/work-vault-example.json').read_text())
        obj['hard_safety_counters']['exploit_execution_count']=False
        self.assertNotEqual(self.run_check(obj).returncode,0)

    def test_non_object_json_fails_cleanly(self):
        with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False) as f:
            f.write('[1,2,3]'); p=f.name
        r=subprocess.run(SCRIPT+[p],capture_output=True,text=True)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('INVALID:',r.stdout)

    def test_sovereign_validators_must_be_array(self):
        obj=json.loads(Path('docs/secure-rails/templates/sovereign-example.json').read_text())
        obj['validators']='workflow_permission_validator'
        self.assertNotEqual(self.run_check(obj).returncode,0)

    def test_scope_must_be_object(self):
        obj=json.loads(Path('docs/secure-rails/templates/work-vault-example.json').read_text())
        obj['scope']=[]
        r=self.run_check(obj)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('INVALID:',r.stdout)

    def test_mark_required_ids_enforced(self):
        base=json.loads(Path('docs/secure-rails/templates/mark-allocation-example.json').read_text())
        for field in ['allocation_id','vault_id','opportunity_id']:
            obj=json.loads(json.dumps(base))
            obj.pop(field,None)
            self.assertNotEqual(self.run_check(obj).returncode,0)

    def test_negated_clause_does_not_clear_later_positive_forbidden_claim(self):
        obj=json.loads(Path('docs/secure-rails/templates/work-vault-example.json').read_text())
        obj['claim_boundary']='No token appreciation; grants equity to holders'
        r=self.run_check(obj)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('forbidden token language: equity',r.stdout)

    def test_unrelated_comma_negation_does_not_clear_positive_forbidden_claim(self):
        obj=json.loads(Path('docs/secure-rails/templates/work-vault-example.json').read_text())
        obj['claim_boundary']='No wallet, grants equity to holders'
        r=self.run_check(obj)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('forbidden token language: equity',r.stdout)

    def test_not_only_positive_construction_does_not_negate_forbidden_claims(self):
        obj=json.loads(Path('docs/secure-rails/templates/work-vault-example.json').read_text())
        obj['claim_boundary']='This work offers not only equity but also dividend rights to holders.'
        r=self.run_check(obj)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('forbidden token language: equity',r.stdout)

    def test_plural_forbidden_terms_are_rejected(self):
        obj=json.loads(Path('docs/secure-rails/templates/work-vault-example.json').read_text())
        obj['claim_boundary']='This work pays dividends to holders.'
        r=self.run_check(obj)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('forbidden token language: dividend',r.stdout)

    def test_multiword_not_only_positive_construction_does_not_negate_claims(self):
        obj=json.loads(Path('docs/secure-rails/templates/work-vault-example.json').read_text())
        obj['claim_boundary']='This work does not only grant equity; it also pays dividends to holders.'
        r=self.run_check(obj)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('forbidden token language: equity',r.stdout)

    def test_direct_verb_negation_can_clear_forbidden_term(self):
        obj=json.loads(Path('docs/secure-rails/templates/work-vault-example.json').read_text())
        obj['claim_boundary']='Utility-only accounting does not grant equity to holders'
        r=self.run_check(obj)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)

    def test_utility_only_negated_receipt_note_passes_forbidden_text_check(self):
        obj={
            'schema_version':'agialpha.skill_network.work_vault_receipt.v1',
            'receipt_id':'receipt-test',
            'skill_id':'skill-test',
            'source_job_id':'job-test',
            'source_agent_id':'agent-test',
            'receipt_note':'Synthetic local utility receipt only. No wallet, custody, payment, trading, KYC/AML, money transmission, securities functionality, token price, token value, token appreciation, or investment return.',
            'wallet_used':False,
            'custody_used':False,
            'payment_executed':False,
            'token_price_used':False,
            'investment_claim_made':False,
            'human_review_required':True,
            'autonomous_persistence_allowed':False,
            'no_auto_merge':True,
            'claim_boundary':'local bounded public evidence'
        }
        r=self.run_check(obj)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
