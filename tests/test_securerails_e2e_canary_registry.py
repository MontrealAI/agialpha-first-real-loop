import tempfile,unittest
from pathlib import Path
from secure_rails.canary_runner import run_canary
from secure_rails.canary_replay import replay
from secure_rails.canary_report import build_report
from secure_rails.canary_registry import update_registry, build_data
class T(unittest.TestCase):
  def test_registry(self):
    out=Path(tempfile.mkdtemp())/'o'; reg=Path(tempfile.mkdtemp())/'r'; data=Path(tempfile.mkdtemp())/'d'
    run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),out); replay(out,out/'04_replay_report.json'); build_report(out,out/'05_canary_report.json')
    update_registry(out,reg); build_data(reg,data); self.assertTrue((data/'latest.json').exists())


  def test_registry_appends_runs(self):
    out=Path(tempfile.mkdtemp())/'o'; reg=Path(tempfile.mkdtemp())/'r'
    m1=run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),out)
    from time import sleep; sleep(1)
    out2=Path(tempfile.mkdtemp())/'o2'; m2=run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),out2)
    update_registry(out,reg); update_registry(out2,reg)
    import json
    runs=json.loads((reg/'registry.json').read_text())['runs']
    self.assertGreaterEqual(len(runs),2)
