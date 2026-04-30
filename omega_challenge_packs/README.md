# OMEGA-GAUNTLET-001 external challenge packs

External reviewers may add a folder such as:

```text
omega_challenge_packs/reviewer-001/challenge_pack.json
```

Minimal schema:

```json
{
  "reviewer": "reviewer-001",
  "claim_boundary_reviewed": true,
  "tasks": [
    {
      "id": "reviewer-claim-boundary-task-001",
      "family": "external reviewer claim-boundary regression",
      "difficulty": 5,
      "required_capability": "claim"
    }
  ]
}
```

Allowed `required_capability` values: `hub`, `claim`, `workflow`, `json`, `python`, `proof`, `redact`, `policy`, `microbatch`, `external_replay`, `delayed`, `archive`.

Do not include secrets, exploit instructions, external target scanning instructions, malware content, or social engineering content.
