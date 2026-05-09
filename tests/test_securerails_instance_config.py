import unittest
from secure_rails.instance_config import build_instance_config, validate_instance_config

class T(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate_instance_config(build_instance_config('QuebecAI','securerails-pilot-hub','n','pilot','')),[])
    def test_missing_owner(self):
        c=build_instance_config('QuebecAI','repo','n','pilot',''); c.pop('owner'); self.assertTrue(validate_instance_config(c))
    def test_no_auto_merge_false(self):
        c=build_instance_config('QuebecAI','repo','n','pilot',''); c['forbidden_use_acknowledgement']['no_auto_merge']=False; self.assertTrue(validate_instance_config(c))
