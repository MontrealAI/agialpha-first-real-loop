# AGI ALPHA Valuation Support 002

AGI ALPHA VALUATION-SUPPORT-002 is a deterministic, implementation-side evidence dossier for valuation-comparable discussion.

## What this is
- A **public implementation evidence organizer** built from repository-local artifacts and manually provided public comparables.
- A **diligence artifact**: evidence inventory, implementation-side comparison, readiness tiering, market-equivalence scenario math, commercial-readiness, moat signals, and risk boundaries.
- A **missing-evidence-honest** system: absent data is shown as `not_reported`, `pending`, `unavailable`, or `skipped_with_reason`.

## What this is not
- Not a valuation assertion.
- Not investment advice, financial advice, securities advice, legal advice, or tax advice.
- Not a token-value claim, return guarantee, fair-market-value opinion, or fundraising recommendation.

## Canonical boundary (required)
AGI ALPHA does not assert a valuation. This dossier organizes implementation-side evidence that may support a valuation-comparable discussion. It is not investment advice, financial advice, a securities offering, a token-value claim, a guarantee of return, or a fair-market-value opinion.

Any comparison to private self-improving-AI labs is limited to public implementation-side evidence available in this repository and manually entered public comparables. Missing external data is shown as not_reported.

AGI ALPHA’s long-horizon superintelligence / Kardashev / value-to-energy framing is a strategic direction, not a present achievement claim. Near-term valuation support must be based only on verified work, replay, Evidence Dockets, ProofBundles, Work Vaults, enterprise workflow evidence, customer-reviewed dockets if available, commercial-readiness evidence, and governance integrity.

## Why implementation-side evidence matters
Valuation-comparable discussion is only defensible when grounded in reproducible implementation evidence (runs, replay, audits, dockets, proofs, governance checks), not narrative claims.

## Public comparable handling
- The fixture `config/valuation_support_public_comparables.example.json` contains manually entered comparable data.
- The default sample includes a **reported category valuation comparable** dated **2026-05-13** with source links and caveats.
- If fixture fields are absent, outputs explicitly render `not_reported`; they are never converted to zeros.

## Readiness tiers and hard caps
Current implementation emits T2–T6 readiness tiers with hard caps (for example: no replay report caps readiness at T2; no ProofBundle caps at T3; no customer-reviewed dockets caps at T6).

## Local deterministic commands
- `python -m agialpha_valuation_support build --repo-root . --ascension-registry ascension_os_registry --comparables config/valuation_support_public_comparables.example.json --market-context config/valuation_support_market_context.example.json --out /tmp/valuation-support-test`
- `python -m agialpha_valuation_support validate --run /tmp/valuation-support-test`
- `python -m agialpha_valuation_support build-data --registry valuation_support_registry --out docs/_generated/valuation-support`
- `python -m agialpha_valuation_support summarize --run /tmp/valuation-support-test --out /tmp/valuation-support-test/12_valuation_support_memo.md`

## Output locations
- Run outputs are written to the explicit `--out` directory passed to `build` (for example `/tmp/valuation-support-test`).
- A registry copy is written to `valuation_support_registry/runs/<run_id>/`.
- Registry (append-only history): `valuation_support_registry/`
- UI-consumable generated data: `docs/_generated/valuation-support/`
