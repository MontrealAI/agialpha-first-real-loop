# SecureRails External Repository Security Model

External repository PRs are untrusted input. SecureRails parses PR data as data and does not execute PR code.

- no secrets required
- least privilege read-only permissions
- no write permissions by default
- no auto-merge
- no `pull_request_target` analysis
- no external target scanning
- no exploit execution
- no secret printing
- artifacts are advisory
- human review required

SecureRails outputs are not cybersecurity-certification, not legal approval, and not autonomous merge authorization.
SecureRails is AI-agent security governance and proof-bound defensive remediation, not offensive cyber, and not an investment product.
