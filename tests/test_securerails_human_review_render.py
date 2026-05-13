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
