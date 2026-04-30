import unittest, tempfile, json
from pathlib import Path
from agialpha_evidence_hub.discover import discover_to_file

class TestDiscovery(unittest.TestCase):
    def test_discover_file(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'disc.json'
            discover_to_file('.', out)
            data=json.loads(out.read_text())
            self.assertIn('workflows', data)

if __name__=='__main__': unittest.main()
