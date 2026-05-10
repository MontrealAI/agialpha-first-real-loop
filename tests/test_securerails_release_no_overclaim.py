import unittest
from secure_rails.release_manifest import validate_manifest
class T(unittest.TestCase):
  def test_forbidden(self):
    ok,_=validate_manifest({'release_version':'1','release_channel':'rc','claim_boundary':'certified'}); self.assertFalse(ok)
