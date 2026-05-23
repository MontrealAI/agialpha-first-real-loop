# AGI ALPHA ENGINE

This repository includes bounded AGI ALPHA engine experiments, including ENGINE-003 for **Networked Skill Compounding**.

## Engine-003 quickstart

```bash
python -m agialpha_engine network-compounding-run \
  --repo-root . \
  --registry agialpha_skill_network_registry \
  --out /tmp/agialpha-skill-network-test \
  --jobs 5 \
  --target-agents 3 \
  --heldout-tasks 5 \
  --seed 123
python -m agialpha_engine network-compounding-replay --run /tmp/agialpha-skill-network-test
python -m agialpha_engine network-compounding-falsification-audit --run /tmp/agialpha-skill-network-test
python -m agialpha_engine network-compounding-validate --run /tmp/agialpha-skill-network-test
```

## Boundary doctrine

- No Evidence Docket, no empirical SOTA claim.
- Autonomous evidence production is allowed; autonomous claim promotion is not.
- Human review is required for activation outside sandbox.

## ENGINE-003 claim status wording

- Supported local bounded wording (only when the claim gate passes):  
  `AGI ALPHA demonstrated that one agent’s proof-bound job produced a validated Skill Package that other agents imported and used to improve held-out adjacent work against no-shared-skill baselines.`
- Exponential wording boundary (default unless multi-cycle evidence supports it):  
  `Exponential compounding is a strategic target. Current evidence reports local bounded network skill propagation only.`
