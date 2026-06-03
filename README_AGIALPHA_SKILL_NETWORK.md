# AGI ALPHA Skill Network (ENGINE-003)

AGI ALPHA ENGINE-003 implements a deterministic, local, replayable **Networked Skill Compounding Engine**.

## Operating thesis

Every Job makes an AI Agent smarter.  
Every new skill can be instantly shared across the network.  
One Agent learns, all Agents level up.

### Boundary on “instant sharing”

“Instant sharing” means **sandboxed registration and importability** through the Network Skill Vault. It does **not** mean production activation without validators and human review.

Instant sharing means sandboxed registration and importability. Production activation requires validators and human review. Exponential compounding is a strategic target unless the exponential claim gate passes.

## Canonical doctrine

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

## Claim gate statuses

- Claim gate status: supported_local_bounded.
- Claim gate status: not_supported. Networked skill compounding claim not yet supported.
- Exponential compounding is a strategic target. Current evidence reports local bounded network skill propagation only. Measured exponential wording requires at least three raw-log-backed cycles with superlinear lift, replay and falsification passing, metrics from raw logs, and a complete reported zero-valued hard-safety ledger; missing safety counters or sentinel raw IDs keep the strategic-target caveat in force.

## What this does not claim

This experiment does **not** claim achieved AGI, ASI, superintelligence, empirical SOTA, official benchmark victory, certification, legal exemption, safe autonomy, token value, token appreciation, or investment return.

$AGIALPHA remains utility-only. Work Vault records are synthetic local utility-accounting receipts only; no wallet, custody, payment, trading, KYC/AML, token price, token value, ROI, yield, or investment return is implemented or claimed.

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

## Workflow publication boundary

ENGINE-003 workflows must never deploy GitHub Pages directly; they only emit artifacts and can signal a central Evidence Mission Control publisher when repository convention supports it.

