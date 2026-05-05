# Evidence Guide

## Core evidence objects
- **Evidence Docket**: structured claim context + artifacts + boundaries.
- **ProofBundle**: machine-verifiable bundle of run outputs.
- **Validator report**: pass/fail/pending checks and notes.
- **Replay log**: replay attempt metadata and outcome.
- **Safety ledger**: boundary counters, risk annotations, and interventions.
- **Cost ledger**: utility accounting for run resources.
- **Artifact manifest**: explicit artifact list and locations.

## Integrity and claim control
- Use root hashes and manifest integrity checks where provided.
- Track local evidence vs external evidence separately.
- Classify outcomes as pending / pass / fail.
- **Rule**: No Evidence Docket, no empirical SOTA claim.

## Baseline ladder (B0–B7)
- B0-B4: pre-claim, exploratory, or local checks.
- B5: stronger local evidence with replay + boundary checks.
- B6: adds broader validation and harder falsification expectations.
- B7: highest internal bar before any externalized claim language.

## External review and delayed outcomes
- External review can confirm or challenge local claims.
- Delayed outcomes prevent premature promotion.
