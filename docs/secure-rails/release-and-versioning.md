# SecureRails Release and Versioning

Production users should pin reusable workflow/action references to a release tag (`v1`, `v1.0.0`) or commit SHA. `main` is for demos only.

Use immutable releases when available. Include provenance/attestation artifacts where supported. Do not claim certification unless independently verified and documented.

## Release checklist
1. tests pass
2. SecureRails Compliance Guard passes
3. docs-audit passes
4. PR Guard demo passes
5. supply-chain provenance workflow passes if present
6. artifact manifest generated
7. release notes include claim boundary
8. immutable release considered
9. customer template updated
10. version tag created
