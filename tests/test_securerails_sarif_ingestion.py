import unittest
from secure_rails.sarif import sarif_ingestion_readiness
class T(unittest.TestCase):
    def test_record(self):
        d=sarif_ingestion_readiness('.')
        self.assertFalse(d['upload_attempted'])
