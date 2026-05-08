# Artifact Attestations

This integration can attempt GitHub Artifact Attestation when workflow permissions allow `id-token: write`, `attestations: write`, and `artifact-metadata: write`.

If unavailable (local run, unsupported action, permission constraints), SecureRails records `attestation.status=unavailable` and emits local provenance records.

OpenSSF Scorecard is an advisory repository security-health signal and does not certify SecureRails.
