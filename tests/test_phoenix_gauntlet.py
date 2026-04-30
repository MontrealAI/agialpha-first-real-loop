import json, tempfile, unittest
from pathlib import Path
from agialpha_phoenix_gauntlet.core import run_gauntlet, validate_site, detect_overclaims_text

class Args:
    run_id = 'test-run'
    commit = 'local'
    branch = 'test'
    actor = 'tester'
    workflow = 'test-workflow'

class PhoenixGauntletTests(unittest.TestCase):
    def test_overclaim_detector_allows_negation(self):
        self.assertFalse(detect_overclaims_text('This does not claim achieved AGI or empirical SOTA.'))
        self.assertTrue(detect_overclaims_text('This achieved AGI and empirical SOTA.'))

    def test_run_gauntlet_builds_docket_and_site(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / 'repo'
            repo.mkdir()
            (repo/'.github'/'workflows').mkdir(parents=True)
            (repo/'.github'/'workflows'/'helios-001-autonomous.yml').write_text('name: AGI ALPHA HELIOS-001 / Autonomous\n', encoding='utf-8')
            (repo/'docs'/'helios-001').mkdir(parents=True)
            (repo/'docs'/'helios-001'/'index.html').write_text('<h1>AGI ALPHA HELIOS 001</h1><p>Claim boundary: does not claim achieved AGI.</p>', encoding='utf-8')
            out = Path(td) / 'out'
            site = Path(td) / 'site'
            run_gauntlet(repo, out, site, Path('phoenix_challenge_packs'), Args())
            self.assertTrue((out/'00_manifest.json').exists())
            self.assertTrue((out/'SCOREBOARD.html').exists())
            self.assertTrue((site/'index.html').exists())
            self.assertTrue((site/'helios-001'/'index.html').exists())
            v = validate_site(site)
            self.assertTrue(v['pass'], v)
            m = json.loads((out/'00_manifest.json').read_text())
            self.assertGreaterEqual(m['B6_beats_B5_count'], 1)
            self.assertEqual(m['hard_safety_total'], 0)

if __name__ == '__main__':
    unittest.main()
