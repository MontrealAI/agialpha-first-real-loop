import tempfile,unittest
from pathlib import Path
from secure_rails.canary_runner import run_canary
from secure_rails.canary_replay import replay
class T(unittest.TestCase):
    def test_replay(self):
        out=Path(tempfile.mkdtemp())/'o'; run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),out)
        r=replay(out,out/'04_replay_report.json'); self.assertTrue(r['replay_pass'])
