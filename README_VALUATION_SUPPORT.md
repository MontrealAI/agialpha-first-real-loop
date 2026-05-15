# AGI ALPHA Valuation Support 002

This dossier is implementation-side valuation support evidence.

It is **not** a valuation assertion, investment advice, financial advice, token-value claim, securities offering, ROI guarantee, or fair-market-value opinion.

It uses public implementation evidence, replayability, governance checks, and missing-evidence honesty.

## Local run

```bash
python -m agialpha_valuation_support build --repo-root . --ascension-registry ascension_os_registry --comparables config/valuation_support_public_comparables.example.json --market-context config/valuation_support_market_context.example.json --out /tmp/valuation-support-test
python -m agialpha_valuation_support validate --run /tmp/valuation-support-test
python -m agialpha_valuation_support build-data --registry valuation_support_registry --out docs/_generated/valuation-support
```
