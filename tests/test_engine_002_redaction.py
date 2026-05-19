import unittest
from secure_rails.redaction_guard import find_secret_like

class TestRedaction002(unittest.TestCase):
    def test_detects_github_token_without_leak(self):
        token='ghp_'+'A'*24
        f=find_secret_like('x='+token)
        self.assertTrue(f)
        self.assertNotIn(token,str(f))

    def test_detects_openai_project_key(self):
        key='sk-proj-AbCdEf_1234567890'
        f=find_secret_like('OPENAI_API_KEY='+key)
        self.assertTrue(any(x['type']=='openai_key' for x in f))

    def test_detects_pkcs8_headers(self):
        f=find_secret_like('-----BEGIN PRIVATE KEY-----\nabc\n-----END PRIVATE KEY-----')
        self.assertTrue(any(x['type']=='private_key_header' for x in f))
