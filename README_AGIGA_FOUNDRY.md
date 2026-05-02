# AGI-GA-FOUNDRY-001

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

AGI-GA Foundry implements global opportunity generation, co-design, local evolution, proof gates, archives, and descendant generation for proof-bound work niches.

Includes OpportunityIntermediates, validators, Evidence Dockets, QD archive, CapabilityArchive, replay, falsification, and workflow commands.

Run:
- `python -m agialpha_agiga_foundry lifecycle --repo-root . --cycles 1 --candidate-niches 16 --evaluate-niches 6 --local-variants-per-niche 3 --out agiga-foundry-runs/test`
- `python -m agialpha_agiga_foundry replay --docket agiga-foundry-runs/test/agiga-foundry-evidence-docket`
- `python -m agialpha_agiga_foundry falsification-audit --docket agiga-foundry-runs/test/agiga-foundry-evidence-docket`
