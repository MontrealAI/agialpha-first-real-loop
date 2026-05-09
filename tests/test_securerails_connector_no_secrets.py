import json
import unittest


class T(unittest.TestCase):
    def test_no_secret_perm(self):
        with open('config/securerails_github_app_permissions.json', encoding='utf-8') as f:
            d = json.load(f)
        self.assertEqual(d['default_permissions']['secrets'], 'none')
