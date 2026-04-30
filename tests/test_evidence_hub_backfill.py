import unittest, tempfile, json
from pathlib import Path
from agialpha_evidence_hub.backfill import backfill

class TestBackfill(unittest.TestCase):
    def test_backfill_writes_runs(self):
        with tempfile.TemporaryDirectory() as d:
            backfill('.', d)
            self.assertTrue((Path(d)/'runs.json').exists())

if __name__=='__main__': unittest.main()
