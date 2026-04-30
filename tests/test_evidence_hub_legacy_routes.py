import unittest, tempfile
from pathlib import Path
from agialpha_evidence_hub.build import build_site
class T(unittest.TestCase):
    def test_legacy(self):
        with tempfile.TemporaryDirectory() as d:
            build_site('evidence_registry', d)
            self.assertTrue((Path(d)/'helios-001/index.html').exists())
if __name__=='__main__': unittest.main()
