import unittest
from agialpha_agiga_foundry.local_evolver import evolve

class T(unittest.TestCase):
    def test_zero_variants_guarded(self):
        out=evolve({"niche_id":"n1"},0)
        self.assertIsNone(out["winner"])
        self.assertEqual(out["error"],"no_local_variants_configured")

if __name__=='__main__':
    unittest.main()
