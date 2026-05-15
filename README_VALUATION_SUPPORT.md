# AGI ALPHA Valuation Support 002

AGI ALPHA valuation support is an implementation-side evidence dossier for valuation-comparable discussion.

It is not a valuation assertion, investment advice, financial advice, securities offering, token-value claim, guarantee of return, or fair-market-value opinion.

## Canonical boundary
AGI ALPHA does not assert a valuation. This dossier organizes implementation-side evidence that may support a valuation-comparable discussion. It is not investment advice, financial advice, a securities offering, a token-value claim, a guarantee of return, or a fair-market-value opinion.

## Local commands
- `python -m agialpha_valuation_support build --repo-root . --ascension-registry ascension_os_registry --comparables config/valuation_support_public_comparables.example.json --market-context config/valuation_support_market_context.example.json --out /tmp/valuation-support-test`
- `python -m agialpha_valuation_support validate --run /tmp/valuation-support-test`
- `python -m agialpha_valuation_support build-data --registry valuation_support_registry --out docs/_generated/valuation-support`
