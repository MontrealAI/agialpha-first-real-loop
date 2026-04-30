---
name: BENCHMARK-GAUNTLET-001 external challenge pack
description: Propose external challenge tasks for the Benchmark Gauntlet.
title: "External challenge pack: BENCHMARK-GAUNTLET-001 / <reviewer-id>"
labels: ["benchmark-gauntlet", "challenge-pack", "external-review"]
---

## Claim boundary

Challenge packs are repo-owned, defensive, and schema-bound. They must not include external target scanning, exploit execution, credential disclosure, malware generation, social engineering, automatic merge, or real-world certification claims.

## How to submit

Open a pull request adding a JSON file under:

```text
external_challenge_packs/<reviewer-id>/challenge_pack.json
```

Use the schema in `external_challenge_packs/README.md`.

## Checklist

- [ ] Tasks are repo-owned and safe.
- [ ] Tasks use supported capability schemas.
- [ ] No external target scanning.
- [ ] No exploit execution.
- [ ] No secrets included.
- [ ] No malware / social engineering.
- [ ] No automatic merge request.
- [ ] Claim boundary preserved.

