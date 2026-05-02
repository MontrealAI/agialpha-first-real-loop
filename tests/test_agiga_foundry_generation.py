import unittest, tempfile
from agialpha_agiga_foundry.lifecycle import run_lifecycle

class T(unittest.TestCase):
    def test_cycles_affect_generation_count(self):
        with tempfile.TemporaryDirectory() as td:
            run_lifecycle('.',2,4,2,1,td)
            import json
            from pathlib import Path
            score=json.loads((Path(td)/'agiga-foundry-evidence-docket/22_summary_tables/scoreboard.json').read_text())
            self.assertEqual(score['candidate_niches_generated'],8)
            self.assertEqual(score['candidate_niches_evaluated'],4)

if __name__=='__main__':
    unittest.main()
