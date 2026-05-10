import tempfile,unittest
from pathlib import Path
from secure_rails.canary_runner import run_canary
from secure_rails.canary_replay import replay
from secure_rails.canary_report import build_report
class T(unittest.TestCase):
    def test_report(self):
        out=Path(tempfile.mkdtemp())/'o'; run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),out); replay(out,out/'04_replay_report.json')
        rep=build_report(out,out/'05_canary_report.json'); self.assertEqual(rep['fixtures_passed'],7)
