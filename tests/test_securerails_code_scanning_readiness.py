import unittest
from secure_rails.code_scanning import code_scanning_readiness
class T(unittest.TestCase):
    def test_record(self):
        d=code_scanning_readiness('.')
        self.assertIn(d['status'],['ready','not_ready','not_applicable','not_reported'])
