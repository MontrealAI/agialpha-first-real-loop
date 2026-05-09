# webhook-security.md

SecureRails GitHub App connector blueprint. Uses least-privilege GitHub App permissions and avoids broad classic PATs except temporary demo fallback. Human review required. No certification claim.

## Local webhook simulator

For local tests, generate a fake payload and matching signature:

```bash
python scripts/secure_rails_webhook_simulator.py --out tests/fixtures/securerails_github_app/webhook_payload.simulated.json
```

This simulator uses demo-only fake values and must not be used with production secrets.
