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

  def test_registry_preserves_prior_runs(self):
    out1=Path(tempfile.mkdtemp())/'o1'
    out2=Path(tempfile.mkdtemp())/'o2'
    reg=Path(tempfile.mkdtemp())/'r'
    run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),out1)
    run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),out2)
    update_registry(out1,reg)
    update_registry(out2,reg)
    runs=__import__('json').loads((reg/'registry.json').read_text())['runs']
    self.assertGreaterEqual(len(runs),2)
    by_status=__import__('json').loads((reg/'indexes/by_status.json').read_text())
    self.assertGreaterEqual(len(by_status.get('success',[])),2)
    by_safety=__import__('json').loads((reg/'indexes/by_safety_status.json').read_text())
    self.assertGreaterEqual(len(by_safety.get('safe',[])),2)

  def test_latest_json_tracks_newest_generated_at(self):
    reg=Path(tempfile.mkdtemp())/'r'
    older=Path(tempfile.mkdtemp())/'old'; newer=Path(tempfile.mkdtemp())/'new'
    run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),older)
    run_canary(Path('.'),Path('tests/fixtures/securerails_e2e_canary'),newer)
    old_manifest=__import__('json').loads((older/'00_manifest.json').read_text())
    new_manifest=__import__('json').loads((newer/'00_manifest.json').read_text())
    if old_manifest['generated_at'] > new_manifest['generated_at']:
      old_manifest, new_manifest = new_manifest, old_manifest
      (older/'00_manifest.json').write_text(__import__('json').dumps(old_manifest))
      (newer/'00_manifest.json').write_text(__import__('json').dumps(new_manifest))
    update_registry(newer,reg)
    update_registry(older,reg)
    latest=__import__('json').loads((reg/'latest.json').read_text())
    self.assertEqual(latest['generated_at'], new_manifest['generated_at'])
