import unittest, tempfile
from pathlib import Path
from agialpha_evidence_hub.linkcheck import linkcheck
class T(unittest.TestCase):
    def test_links(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'index.html').write_text('<a href="/">x</a>')
            linkcheck(d)
if __name__=='__main__': unittest.main()
