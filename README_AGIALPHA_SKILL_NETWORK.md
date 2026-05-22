# AGI ALPHA Skill Network (ENGINE-003)

AGI ALPHA ENGINE-003 implements a deterministic, local, replayable **Networked Skill Compounding Engine**.

## Operating thesis

Every Job makes an AI Agent smarter.  
Every new skill can be instantly shared across the network.  
One Agent learns, all Agents level up.

### Boundary on “instant sharing”

“Instant sharing” means **sandboxed registration and importability** through the Network Skill Vault. It does **not** mean production activation without validators and human review.

## Canonical doctrine

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

## Claim gate statuses

- Claim gate status: supported_local_bounded.
- Claim gate status: not_supported. Networked skill compounding claim not yet supported.
- Exponential compounding is a strategic target. Current evidence reports local bounded network skill propagation only.

## What this does not claim

This experiment does **not** claim achieved AGI, ASI, superintelligence, empirical SOTA, official benchmark victory, certification, legal exemption, safe autonomy, token value, token appreciation, or investment return.

## Quickstart

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
python -m agialpha_engine network-compounding-build-data \
  --registry agialpha_skill_network_registry \
  --out docs/_generated/agialpha-skill-network
```
