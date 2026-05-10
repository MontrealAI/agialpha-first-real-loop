import unittest
from secure_rails.release_manifest import build_manifest, validate_manifest
class T(unittest.TestCase):
  def test_ok(self):
    m=build_manifest('0.1.0-rc1','rc','r','c','b',[],[]);ok,_=validate_manifest(m);self.assertTrue(ok)
  def test_bad_channel(self):
    m=build_manifest('0.1.0-rc1','bad','r','c','b',[],[]);ok,_=validate_manifest(m);self.assertFalse(ok)
