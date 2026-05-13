import json
from pathlib import Path
import shutil
import unittest
from secure_rails.review_ledger import update_ledger
from secure_rails.review_render import build_data

class T(unittest.TestCase):
    def test_pending_reviews_not_negative(self):
        reg=Path('tests/tmp_review_registry_render')
        out=Path('tests/tmp_review_render_out')
        if reg.exists(): shutil.rmtree(reg)
        if out.exists(): shutil.rmtree(out)
        update_ledger(Path('tests/fixtures/securerails_human_review/valid_request.json'), reg)
        update_ledger(Path('tests/fixtures/securerails_human_review/valid_decision_accept.json'), reg)
        # add second decision to create decision count > request count
        d=json.loads(Path('tests/fixtures/securerails_human_review/valid_decision_accept.json').read_text())
        d['decision_id']='sr-review-decision-2026-0002'
        p=Path('tests/tmp_decision_2.json'); p.write_text(json.dumps(d), encoding='utf-8')
        update_ledger(p, reg)
        build_data(reg, out)
        summary=json.loads((out/'summary.json').read_text())
        self.assertGreaterEqual(summary['pending_reviews'], 0)
    def test_pending_reviews_uses_request_ids(self):
        reg=Path('tests/tmp_review_registry_render_ids')
        out=Path('tests/tmp_review_render_out_ids')
        if reg.exists(): shutil.rmtree(reg)
        if out.exists(): shutil.rmtree(out)
        # request 1 and request 2
        r1=json.loads(Path('tests/fixtures/securerails_human_review/valid_request.json').read_text())
        r2=json.loads(Path('tests/fixtures/securerails_human_review/valid_request.json').read_text())
        r2['review_request_id']='sr-review-request-2026-0002'
        p1=Path('tests/tmp_request_1.json'); p1.write_text(json.dumps(r1), encoding='utf-8')
        p2=Path('tests/tmp_request_2.json'); p2.write_text(json.dumps(r2), encoding='utf-8')
        update_ledger(p1, reg)
        update_ledger(p2, reg)
        # two decisions both for request 1
        d1=json.loads(Path('tests/fixtures/securerails_human_review/valid_decision_accept.json').read_text())
        d2=json.loads(Path('tests/fixtures/securerails_human_review/valid_decision_accept.json').read_text())
        d2['decision_id']='sr-review-decision-2026-0002'
        pd1=Path('tests/tmp_decision_a.json'); pd1.write_text(json.dumps(d1), encoding='utf-8')
        pd2=Path('tests/tmp_decision_b.json'); pd2.write_text(json.dumps(d2), encoding='utf-8')
        update_ledger(pd1, reg)
        update_ledger(pd2, reg)
        build_data(reg, out)
        summary=json.loads((out/'summary.json').read_text())
        self.assertEqual(summary['pending_reviews'], 1)
