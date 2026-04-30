import unittest, tempfile
from pathlib import Path
from agialpha_evidence_hub.build import build_site
class T(unittest.TestCase):
    def test_build(self):
        with tempfile.TemporaryDirectory() as d:
            build_site('evidence_registry', d)
            self.assertTrue((Path(d)/'index.html').exists())
            self.assertTrue((Path(d)/'data/runs.json').exists())
if __name__=='__main__': unittest.main()
