import tempfile
import unittest
from pathlib import Path

from agialpha_evidence_hub.build import build_site


class T(unittest.TestCase):
    def test_experiment_pages_include_claim_boundary_and_run_table(self):
        with tempfile.TemporaryDirectory() as out:
            build_site('evidence_registry', out)
            exp_dir = Path(out, 'experiments')
            pages = [p for p in exp_dir.glob('*/index.html') if p.parent.name != 'index.html']
            self.assertTrue(pages, 'expected at least one generated experiment page')
            sample = pages[0].read_text()
            self.assertIn('claim boundary:', sample)
            self.assertIn('Back to hub', sample)
            self.assertIn('<table>', sample)


if __name__ == '__main__':
    unittest.main()
