import json
import pathlib
import unittest


class T(unittest.TestCase):
    def test_sorted(self):
        runs_path = pathlib.Path("evidence_registry/runs.json")
        if runs_path.exists():
            with runs_path.open("r", encoding="utf-8") as handle:
                runs = json.load(handle)
        else:
            runs = []
        self.assertEqual(
            runs,
            sorted(runs, key=lambda x: x.get("generated_at", ""), reverse=True),
        )


if __name__ == "__main__":
    unittest.main()
