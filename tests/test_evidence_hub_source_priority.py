import unittest

from agialpha_evidence_hub.source_priority import rank


class T(unittest.TestCase):
    def test_manifest_beats_historical_backfill(self):
        self.assertGreater(rank('manifest'), rank('historical_backfill'))

    def test_unknown_source_is_lowest(self):
        self.assertEqual(rank('unknown_source'), 0)


if __name__ == '__main__':
    unittest.main()
