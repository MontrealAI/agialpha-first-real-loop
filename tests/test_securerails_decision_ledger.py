import json
from pathlib import Path
import unittest
import shutil
from secure_rails.review_ledger import update_ledger
class T(unittest.TestCase):
  def test_history(self):
    reg=Path('tests/tmp_review_registry');
    if reg.exists(): shutil.rmtree(reg)
    update_ledger(Path('tests/fixtures/securerails_human_review/valid_request.json'), reg)
    update_ledger(Path('tests/fixtures/securerails_human_review/valid_decision_accept.json'), reg)
    entries=json.loads((reg/'registry.json').read_text())['entries']; self.assertGreaterEqual(len(entries),2)
