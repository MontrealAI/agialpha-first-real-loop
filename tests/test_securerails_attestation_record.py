import tempfile, pathlib, unittest
from secure_rails.attestations import build_attestation_record
class T(unittest.TestCase):
  def test_unavailable(self):
    with tempfile.TemporaryDirectory() as d:
      rec=build_attestation_record(str(pathlib.Path(d)/'a.json'),attempt=True,supported=False)
      self.assertEqual(rec['attestation']['status'],'unavailable')
