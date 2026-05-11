import unittest
from secure_rails.secret_scanning_posture import secret_scanning_posture
class T(unittest.TestCase):
    def test_record(self):
        d=secret_scanning_posture('.')
        self.assertEqual(d['schema_version'],'securerails.secret_scanning_posture.v1')
