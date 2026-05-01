import json
import unittest


class T(unittest.TestCase):
    def test_state(self):
        with open("rsi_state/governance_kernel_state.json", "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        self.assertIn("state_hash_chain", payload)


if __name__ == "__main__":
    unittest.main()
