---
name: RSI-FORGE-002 external review
description: External replay and review checklist for RSI-FORGE-002
title: "RSI-FORGE-002 external review: <run-id>"
labels: ["external-review", "rsi", "evidence-docket"]
---

## Source run

Run ID:

Actions URL:

Artifact name:

## Review checklist

- [ ] Clean checkout completed
- [ ] Source artifact downloaded
- [ ] `python -m rsi_forge_002 replay --docket <path>` passes
- [ ] Evidence Docket files present
- [ ] B5/B6 comparison inspected
- [ ] vNext transfer inspected
- [ ] State hash continuity inspected
- [ ] ECI ledger inspected
- [ ] Move-37 dossier inspected if present
- [ ] Safety counters inspected
- [ ] Claim boundary present
- [ ] No empirical SOTA / AGI / ASI claim promoted

## Verdict

- [ ] Replay passed
- [ ] Replay failed
- [ ] Needs changes

Notes:
