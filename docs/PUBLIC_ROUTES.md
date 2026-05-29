# Public Routes

Evidence Mission Control is the central public publisher. Non-publisher workflows must not deploy GitHub Pages directly.

| route | label | backing data | boundary |
|---|---|---|---|
| `/` | Evidence Mission Control | `evidence_registry/` | No Evidence Docket, no empirical SOTA claim. |
| `/agialpha-skill-network/` | Skill Network | `docs/_generated/agialpha-skill-network/` | Local bounded network skill propagation only unless claim gates pass. |
| `/experiments/agialpha-engine-003/` | AGI ALPHA Engine 003 | `docs/_generated/agialpha-skill-network/` | Instant sharing means sandboxed registration/importability; production activation requires validators and human review. |

Footer doctrine: **No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.**
