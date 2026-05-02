import unittest, tempfile, json
from pathlib import Path
from agialpha_agiga_foundry.replay import replay_docket

class T(unittest.TestCase):
    def test_replay_requires_solved_niches(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"22_summary_tables"; p.mkdir(parents=True)
            (p/"scoreboard.json").write_text(json.dumps({"solved_niches":0}))
            (Path(td)/"13_replay_logs").mkdir(parents=True)
            out=replay_docket(td)
            self.assertFalse(out["replay_pass"])

if __name__=='__main__':
    unittest.main()
