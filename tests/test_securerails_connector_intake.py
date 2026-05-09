import json,unittest
from secure_rails.connector_intake import validate_installation_record
class T(unittest.TestCase):
  def test_installation(self):
    d=json.loads(open('docs/secure-rails/templates/customer-installation-example.json').read());self.assertTrue(validate_installation_record(d)[0])
