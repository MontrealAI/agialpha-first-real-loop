# Trust Center Control Matrix

Readiness mapping only (not certification): NIST CSF 2.0, NIST AI RMF, SOC 2 readiness, ISO/IEC 27001 readiness, ISO/IEC 42001 readiness.

| ID | Name | Status | Evidence | Claim boundary |
|---|---|---|---|---|
| SEC-001 | Claim-boundary enforcement | implemented | scripts/secure_rails_claim_boundary_check.py | advisory only |
| SEC-002 | No-auto-merge enforcement | implemented | scripts/secure_rails_no_automerge_check.py | advisory only |
| SEC-003 | Safety ledger hard counters | implemented | docs/secure-rails/templates/safety-ledger-example.json | advisory only |
| SEC-004 | Redaction policy | partially implemented | secure_rails/redaction_guard.py | advisory only |
| SEC-005 | Work Vault validation | implemented | scripts/secure_rails_work_vault_check.py | advisory only |
| SEC-006 | MARK allocation record | implemented | secure_rails_registry/mark_allocations | advisory only |
| SEC-007 | Sovereign assignment record | implemented | secure_rails_registry/sovereigns | advisory only |
| SEC-008 | ProofBundle generation | implemented | docs/PROOFBUNDLES.md | advisory only |
| SEC-009 | Evidence Docket generation | implemented | docs/EVIDENCE_DOCKET_STANDARD.md | advisory only |
| SEC-010 | Vulnerability disclosure policy | implemented | docs/secure-rails/vulnerability-disclosure-policy.md | advisory only |
| SEC-011 | Incident response runbook | implemented | docs/secure-rails/incident-response-runbook.md | advisory only |
| SEC-012 | Security advisory process | implemented | docs/secure-rails/security-advisory-process.md | advisory only |
| SEC-013 | Supply-chain provenance | implemented | docs/secure-rails/supply-chain-provenance.md | advisory only |
| SEC-014 | Customer pilot intake controls | implemented | docs/secure-rails/customer-pilot-intake.md | advisory only |
| SEC-015 | GitHub App least-privilege connector | implemented | docs/secure-rails/github-app-connector.md | advisory only |
| SEC-016 | Template bootstrap health check | implemented | .github/workflows/securerails-template-health-check-001.yml | advisory only |
| SEC-017 | $AGIALPHA utility-only boundary | implemented | docs/secure-rails/token-utility-policy.md | advisory only |
| SEC-018 | EU AI Act excluded-use posture | implemented | docs/secure-rails/eu-ai-act-positioning.md | advisory only |
| SEC-019 | Human review gate | implemented | config/securerails_required_checks.json | advisory only |
| SEC-020 | Evidence Mission Control publication guard | implemented | .github/workflows/evidence-hub-publish.yml | advisory only |
