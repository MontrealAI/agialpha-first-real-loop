---
name: PHOENIX-HUB-001 challenge pack
description: Propose external reviewer challenge tasks for PHOENIX-HUB-001.
title: "PHOENIX-HUB-001 challenge pack: <reviewer-id>"
labels: ["challenge-pack", "phoenix-hub-001", "external-review"]
---

## Challenge pack instructions

Create a JSON file under:

```text
phoenix_challenge_packs/<reviewer-id>/challenge_pack.json
```

Use this template:

```json
{
  "reviewer": "reviewer-id",
  "claim_boundary_reviewed": true,
  "tasks": [
    {
      "id": "reviewer-task-001",
      "family": "dynamic experiment discovery",
      "difficulty": 5,
      "required_capability": "registry"
    }
  ]
}
```

## Safety boundary

Do not include external target scanning, exploit execution, credential disclosure, malware generation, social engineering, or any request to weaken claim boundaries.
