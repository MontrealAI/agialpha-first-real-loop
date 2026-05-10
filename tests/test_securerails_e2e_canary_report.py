import tempfile,unittest
from pathlib import Path
from secure_rails.canary_runner import run_canary
from secure_rails.canary_replay import replay
from secure_rails.canary_report import build_report
class T(unittest.TestCase):
    def test_report(self):
        out=Path(tempfile.mkdtemp())/'o'; run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),out); replay(out,out/'04_replay_report.json')
        rep=build_report(out,out/'05_canary_report.json'); self.assertEqual(rep['fixtures_passed'],7)


    def test_report_counts_failed_partial(self):
        out=Path(tempfile.mkdtemp())/'o'; run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),out)
        import json
        fx=json.loads((out/'01_fixture_summary.json').read_text())
        fx[0]['status']='fail'; fx[1]['status']='partial'
        (out/'01_fixture_summary.json').write_text(json.dumps(fx))
        replay(out,out/'04_replay_report.json')
        rep=build_report(out,out/'05_canary_report.json')
        self.assertEqual(rep['fixtures_failed'],1)
        self.assertEqual(rep['fixtures_partial'],1)
