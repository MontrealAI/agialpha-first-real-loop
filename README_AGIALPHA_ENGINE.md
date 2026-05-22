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
