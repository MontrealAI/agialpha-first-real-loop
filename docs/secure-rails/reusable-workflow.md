# SecureRails Reusable Workflow

`securerails-pr-guard-reusable.yml` exposes `workflow_call` inputs for mode, strictness, artifact generation toggles, token utility mode, and artifact upload.

- Outputs: `recommendation`, `summary_path`, `evidence_docket_path`, `work_vault_path`
- Artifact: `securerails-pr-guard-output`
- Permissions: `contents: read`, `pull-requests: read`, `actions: read`
- No write permission required.
- No secrets required.

For production callers, pin to a release tag (`v1`) or immutable commit SHA; `main` is demo-only.
