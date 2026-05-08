# SecureRails Release and Versioning

Production users should pin reusable workflow/action references to release tags or commit SHAs. `main` is demo-only.

Recommended tags: `v1.0.0`, `v1`.
Prefer immutable releases where supported.
Release provenance/attestation should be attached where supported.
Do not claim certification unless independently verified and documented.

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
