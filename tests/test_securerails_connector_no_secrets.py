import json,unittest
class T(unittest.TestCase):
  def test_no_secret_perm(self):
    d=json.loads(open('config/securerails_github_app_permissions.json').read());self.assertEqual(d['default_permissions']['secrets'],'none')
