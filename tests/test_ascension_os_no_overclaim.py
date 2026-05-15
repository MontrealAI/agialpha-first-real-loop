import json
import tempfile
import unittest
from pathlib import Path

from agialpha_ascension_os import core


class TestNoOverclaim(unittest.TestCase):
    def test_run_outputs_no_forbidden_claims(self):
        with tempfile.TemporaryDirectory() as td:
            run = Path(td) / "run"
            reg = Path(td) / "registry"
            core.run_cycle(Path('.'), run, reg)
            forbidden = [
                "achieved agi",
                "achieved asi",
                "achieved superintelligence",
                "official benchmark victory",
                "certified safe",
                "cybersecurity certification",
                "eu ai act exempt",
                "legally approved worldwide",
                "guaranteed economic return",
                "guaranteed wealth",
                "recursive beaten",
            ]
            for p in run.rglob('*'):
                if p.suffix.lower() not in {'.json', '.md'}:
                    continue
                text = p.read_text(encoding='utf-8').lower()
                for bad in forbidden:
                    self.assertNotIn(bad, text, f"found '{bad}' in {p}")
                self.assertNotIn("empirical sota claim achieved", text, f"found empirical sota overclaim in {p}")


if __name__ == '__main__':
    unittest.main()
