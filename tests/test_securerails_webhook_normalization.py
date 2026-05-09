import json
import pathlib
import unittest

from secure_rails.github_webhooks import normalize_webhook_payload


class T(unittest.TestCase):
  def test_redact(self):
    n = normalize_webhook_payload({'sender': {'login': 'alice', 'email': 'a@b.com'}}, 'pull_request', 'd')
    self.assertTrue(n['sender']['raw_login_redacted'])
    self.assertNotIn('email', str(n))

  def test_fixture_payload_minimized(self):
    fixture = pathlib.Path(__file__).resolve().parent / 'fixtures' / 'securerails_github_app' / 'webhook_payload.json'
    payload = json.loads(fixture.read_text(encoding='utf-8'))
    n = normalize_webhook_payload(payload, 'pull_request', 'delivery-001')
    self.assertEqual(n['repository']['full_name'], 'MontrealAI/agialpha-first-real-loop')
    self.assertEqual(n['pull_request']['is_fork'], False)
    self.assertNotIn('not-retained@example.test', json.dumps(n))
    self.assertNotIn('full_payload', n)
