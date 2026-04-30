# External challenge packs

External reviewers can add JSON challenge packs here through a PR.
The benchmark gauntlet will include any `*.json` files in this directory when it runs.

A challenge pack should contain:

```json
{
  "pack_id": "reviewer-001",
  "reviewer": "name or organization",
  "tasks": [
    {
      "task_id": "reviewer-task-001",
      "family": "external reviewer challenge",
      "capability": "docs.claim_boundary",
      "prompt": "Task description",
      "acceptance": {"required_phrases": ["Evidence Docket"]},
      "risk_tier": "ALLOW"
    }
  ]
}
```

Allowed capability schemas include:

- `software.patch`
- `replay.integrity`
- `data.group_metric`
- `policy.allowed_actions`
- `api.openapi_consistency`
- `docs.claim_boundary`
- `node.telemetry`
- `evidence.proofbundle`
- `security.redaction`

The experiment is defensive and repo-owned. Do not add external target scanning, exploit execution, secret disclosure, malware generation, social engineering, or automatic merge tasks.
