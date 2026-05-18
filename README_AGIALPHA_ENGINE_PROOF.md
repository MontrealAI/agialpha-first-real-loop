# AGI ALPHA Engine 002: Measured Recursive Machine Labor Proof

AGI ALPHA ENGINE-002 is a deterministic, local proof pilot for measured recursive machine labor. It tests whether Mandate A machine-generated work creates a frozen reusable capability that improves held-out adjacent Mandate B performance against a shadow-control baseline under equal constraints.

The stronger claim is supported only when treatment beats shadow control with computed metrics and all gates pass: capability freeze, held-out leakage, replay, falsification, ProofBundle, Evidence Docket, semantic negative tests, adversarial docket, safety counters, token boundary, regulated boundary, no auto-merge, and human-review promotion gate.

This is not achieved AGI, ASI, superintelligence, empirical SOTA, an official benchmark victory, security/legal/compliance certification, safe-autonomy certification, investment advice, token value, ROI, yield, or external validation. `$AGIALPHA` remains utility-only accounting.

## Run locally

```bash
python -m agialpha_engine run-proof --repo-root . --out agialpha-engine-proof-runs/test --mandate-pairs 3 --seed 1337
python -m agialpha_engine replay-proof --run agialpha-engine-proof-runs/test
python -m agialpha_engine falsification-audit-proof --run agialpha-engine-proof-runs/test
python -m agialpha_engine validate-proof --run agialpha-engine-proof-runs/test
python -m agialpha_engine build-proof-data --run agialpha-engine-proof-runs/test --out docs/_generated/agialpha-engine-proof
python -m agialpha_engine render-proof --run agialpha-engine-proof-runs/test --out docs/agialpha-engine-proof/generated
```

If any gate fails, the public status must be: `This run does not support the stronger recursive-improvement claim.`
