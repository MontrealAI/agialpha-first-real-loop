import tempfile
import unittest
from pathlib import Path
from agialpha_ascension_os import core


class TestValuationSupport(unittest.TestCase):
    def test_no_valuation_assertion(self):
        with tempfile.TemporaryDirectory() as td:
            run = Path(td) / "run"
            reg = Path(td) / "registry"
            core.run_cycle(Path('.'), run, reg)
            text = (run / "valuation_support_dossier.json").read_text(encoding="utf-8").lower()
            self.assertIn("does not assert a valuation", text)
            self.assertNotIn("asserts a valuation", text)
            self.assertNotIn("guaranteed valuation", text)


if __name__ == '__main__':
    unittest.main()
