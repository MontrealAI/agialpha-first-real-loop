from pathlib import Path


def test_docs_exist():
    required = [
        'docs/valuation-support/README.md',
        'docs/valuation-support/implementation-side-comparison.md',
        'docs/valuation-support/category-valuation-signal.md',
        'docs/valuation-support/market-equivalence-sensitivity.md',
        'docs/valuation-support/commercial-readiness.md',
        'docs/valuation-support/moat-assessment.md',
        'docs/valuation-support/investor-diligence-index.md',
        'docs/valuation-support/not-an-investment-claim.md',
        'docs/valuation-support/regulated-boundary.md',
        'docs/valuation-support/missing-evidence.md',
    ]
    for p in required:
        assert Path(p).exists(), p
