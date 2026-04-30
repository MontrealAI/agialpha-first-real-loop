import tempfile, unittest
from pathlib import Path
from agialpha_l4_l7.core import run_all, replay, falsify
class L4L7Tests(unittest.TestCase):
    def test_run_replay_falsify(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); src=root/'evidence-docket'; src.mkdir(); (src/'10_decision_memo.md').write_text('claim boundary not empirical SOTA independent replay required'); (src/'09_treatment_control_comparison.json').write_text('{"reuse_lift_percent":66.67}')
            out=root/'out'; docs=root/'docs'; s=run_all(src,out,docs,[1,2],[1,2],root); self.assertEqual(s['safety_incidents'],0); self.assertTrue((docs/'index.html').exists())
            rr=replay(out,root/'replay'); self.assertGreaterEqual(rr['pass_count'],1)
            fr=falsify(out,root/'audit'); self.assertIn(fr['audit_status'],['pass','review_required'])
if __name__=='__main__': unittest.main()
