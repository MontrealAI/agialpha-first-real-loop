import json
import unittest

from secure_rails.github_app_permissions import validate_permission_matrix


class T(unittest.TestCase):
    def test_default_ok(self):
        with open('config/securerails_github_app_permissions.json', encoding='utf-8') as f:
            d = json.load(f)
        self.assertTrue(validate_permission_matrix(d)[0])

    def test_secrets_forbidden(self):
        d = {'default_permissions': {'secrets': 'read'}}
        self.assertFalse(validate_permission_matrix(d)[0])

    def test_unknown_scope_rejected(self):
        d = {'default_permissions': {'metadata': 'read', 'members': 'write'}}
        ok, errs = validate_permission_matrix(d)
        self.assertFalse(ok)
        self.assertTrue(any('unknown permission scope' in e for e in errs))
