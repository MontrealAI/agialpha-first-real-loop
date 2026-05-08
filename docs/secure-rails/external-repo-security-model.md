# SecureRails External Repository Security Model

External PRs are untrusted input. SecureRails processes PR context as data, not executable instructions.

- no untrusted PR code execution
- no secrets required
- least-privilege read-only permissions
- no write permissions by default
- no auto-merge
- no `pull_request_target` analysis
- no external target scanning
- no exploit execution
- no secret printing
- artifacts are advisory only
- human review required

SecureRails outputs are not cybersecurity-certification.
SecureRails outputs are not legal approval.
SecureRails outputs are not autonomous merge authorization.

$AGIALPHA remains utility-only accounting inside bounded defensive workflows.
