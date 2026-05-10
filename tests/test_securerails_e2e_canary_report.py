import tempfile,unittest
from pathlib import Path
from secure_rails.canary_runner import run_canary
from secure_rails.canary_replay import replay
from secure_rails.canary_report import build_report
class T(unittest.TestCase):
    def test_report(self):
        out=Path(tempfile.mkdtemp())/'o'; run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),out); replay(out,out/'04_replay_report.json')
        rep=build_report(out,out/'05_canary_report.json'); self.assertEqual(rep['fixtures_passed'],7)

    def test_failed_and_partial_counts_derived_from_summary(self):
        out=Path(tempfile.mkdtemp())/'o'
        run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),out)
        summary_path = out / '01_fixture_summary.json'
        summary = __import__('json').loads(summary_path.read_text())
        summary[0]['status'] = 'fail'
        summary[1]['status'] = 'partial'
        summary_path.write_text(__import__('json').dumps(summary))
        replay(out,out/'04_replay_report.json')
        rep=build_report(out,out/'05_canary_report.json')
        self.assertEqual(rep['fixtures_failed'],1)
        self.assertEqual(rep['fixtures_partial'],1)

    def test_expected_recommendations_matched_is_computed(self):
        out=Path(tempfile.mkdtemp())/'o'
        run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),out)
        summary_path = out / '01_fixture_summary.json'
        summary = __import__('json').loads(summary_path.read_text())
        summary[0]['actual_recommendation'] = 'mismatch'
        summary_path.write_text(__import__('json').dumps(summary))
        replay(out,out/'04_replay_report.json')
        rep=build_report(out,out/'05_canary_report.json')
        self.assertEqual(rep['expected_recommendations_matched'],6)
