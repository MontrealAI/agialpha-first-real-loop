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
    p=Path('tests/tmp_bad_request.json'); p.write_text(json.dumps(bad), encoding='utf-8')
    with self.assertRaises(ValueError):
      update_ledger(p, reg)
  def test_gate_decision_cross_check(self):
    reg=Path('tests/tmp_review_registry_mismatch');
    if reg.exists(): shutil.rmtree(reg)
    update_ledger(Path('tests/fixtures/securerails_human_review/valid_request.json'), reg)
    bad_dec=json.loads(Path('tests/fixtures/securerails_human_review/valid_decision_accept.json').read_text())
    bad_dec['promotion']['promotion_allowed'] = False
    bad_dec['hard_safety_counters']['critical_safety_incidents'] = 1
    p_dec=Path('tests/tmp_bad_decision.json'); p_dec.write_text(json.dumps(bad_dec), encoding='utf-8')
    update_ledger(p_dec, reg)
    with self.assertRaises(ValueError):
      update_ledger(Path('tests/fixtures/securerails_human_review/valid_promotion_gate_pass.json'), reg)
  def test_validate_ledger_detects_missing_file(self):
    reg=Path('tests/tmp_review_registry_validate');
    if reg.exists(): shutil.rmtree(reg)
    update_ledger(Path('tests/fixtures/securerails_human_review/valid_request.json'), reg)
    data=json.loads((reg/'registry.json').read_text())
    data['entries'].append({'id':'x','kind':'request','path':'requests/missing.json','updated_at':'2026-05-12T00:00:00Z'})
    (reg/'registry.json').write_text(json.dumps(data), encoding='utf-8')
    errs=validate_ledger(reg)
    self.assertTrue(any('missing file' in e for e in errs))
  def test_missing_id_rejected(self):
    reg=Path('tests/tmp_review_registry_missing_id');
    if reg.exists(): shutil.rmtree(reg)
    req=json.loads(Path('tests/fixtures/securerails_human_review/valid_request.json').read_text())
    req.pop('review_request_id', None)
    p=Path('tests/tmp_missing_id_request.json'); p.write_text(json.dumps(req), encoding='utf-8')
    with self.assertRaises(ValueError):
      update_ledger(p, reg)
