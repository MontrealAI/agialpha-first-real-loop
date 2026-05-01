import json
import unittest


class T(unittest.TestCase):
    def test_schema(self):
        with open("config/rsi_governance_kernel.json", "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        self.assertEqual(payload["schema_version"], "agialpha.rsi_governance_kernel.v1")


if __name__ == "__main__":
    unittest.main()
