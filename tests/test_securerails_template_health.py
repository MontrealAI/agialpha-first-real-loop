import unittest, tempfile, json
from pathlib import Path
from secure_rails.template_health import write_template_health
class T(unittest.TestCase):
    def test_health_json(self):
        with tempfile.TemporaryDirectory() as d:
            o=Path(d)/'h.json'; h=write_template_health(Path('.'),'x/y',o); self.assertTrue(o.exists()); self.assertIn(h['status'],('pass','fail','warning'))
