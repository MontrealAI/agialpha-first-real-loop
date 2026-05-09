import unittest, tempfile
from pathlib import Path
from secure_rails.template_bootstrap import init, validate
class T(unittest.TestCase):
    def test_init_validate(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'cfg.json'; init(Path('.'),'QuebecAI','securerails-pilot-hub','name','pilot','',p); self.assertEqual(validate(p),[])
