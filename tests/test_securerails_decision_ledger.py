import json
from pathlib import Path
import unittest
import shutil
from secure_rails.review_ledger import update_ledger, validate_ledger
class T(unittest.TestCase):
  def test_history(self):
    reg=Path('tests/tmp_review_registry');
    if reg.exists(): shutil.rmtree(reg)
    update_ledger(Path('tests/fixtures/securerails_human_review/valid_request.json'), reg)
    update_ledger(Path('tests/fixtures/securerails_human_review/valid_decision_accept.json'), reg)
    entries=json.loads((reg/'registry.json').read_text())['entries']; self.assertGreaterEqual(len(entries),2)
  def test_gate_requires_existing_decision(self):
    reg=Path('tests/tmp_review_registry_missing_decision');
    if reg.exists(): shutil.rmtree(reg)
    update_ledger(Path('tests/fixtures/securerails_human_review/valid_request.json'), reg)
    with self.assertRaises(ValueError):
      update_ledger(Path('tests/fixtures/securerails_human_review/valid_promotion_gate_pass.json'), reg)
  def test_rejects_unsafe_ids(self):
    reg=Path('tests/tmp_review_registry_unsafe');
    if reg.exists(): shutil.rmtree(reg)
    bad=json.loads(Path('tests/fixtures/securerails_human_review/valid_request.json').read_text())
    bad['review_request_id'] = '../escape'
    tmp=Path('tests/fixtures/securerails_human_review/tmp_bad_request.json')
    tmp.write_text(json.dumps(bad), encoding='utf-8')
    with self.assertRaises(ValueError):
      update_ledger(tmp, reg)
    tmp.unlink()
  def test_gate_cross_checks_source_decision(self):
    reg=Path('tests/tmp_review_registry_crosscheck');
    if reg.exists(): shutil.rmtree(reg)
    update_ledger(Path('tests/fixtures/securerails_human_review/valid_request.json'), reg)
    update_ledger(Path('tests/fixtures/securerails_human_review/valid_decision_accept.json'), reg)
    gate=json.loads(Path('tests/fixtures/securerails_human_review/valid_promotion_gate_pass.json').read_text())
    gate['required_conditions']['hard_safety_counters_zero'] = False
    tmp=Path('tests/fixtures/securerails_human_review/tmp_bad_gate.json')
    tmp.write_text(json.dumps(gate), encoding='utf-8')
    with self.assertRaises(ValueError):
      update_ledger(tmp, reg)
    tmp.unlink()
  def test_validate_ledger_detects_bad_entries(self):
    reg=Path('tests/tmp_review_registry_validate');
    if reg.exists(): shutil.rmtree(reg)
    update_ledger(Path('tests/fixtures/securerails_human_review/valid_request.json'), reg)
    broken=json.loads((reg/'registry.json').read_text())
    broken['entries'].append({'id':'x','kind':'request','path':'requests/missing.json','updated_at':'now'})
    (reg/'registry.json').write_text(json.dumps(broken), encoding='utf-8')
    errs = validate_ledger(reg)
    self.assertTrue(any('missing file' in e for e in errs))
