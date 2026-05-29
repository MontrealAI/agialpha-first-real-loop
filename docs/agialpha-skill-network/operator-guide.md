# Operator Guide

Run the deterministic local chain:

```bash
python -m agialpha_engine network-compounding-run --repo-root . --registry agialpha_skill_network_registry --out /tmp/agialpha-skill-network-test --jobs 5 --target-agents 3 --heldout-tasks 5 --seed 123
python -m agialpha_engine network-compounding-replay --run /tmp/agialpha-skill-network-test
python -m agialpha_engine network-compounding-falsification-audit --run /tmp/agialpha-skill-network-test
python -m agialpha_engine network-compounding-validate --run /tmp/agialpha-skill-network-test
python -m agialpha_engine network-compounding-build-data --registry agialpha_skill_network_registry --out docs/_generated/agialpha-skill-network
```

Do not treat a successful run as production activation. Review ProofBundles, Evidence Dockets, replay, falsification, and boundary ledgers before any further action.
