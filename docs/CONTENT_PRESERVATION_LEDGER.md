# Content Preservation Ledger


| original file | changed file | change type | rationale | content preserved? | claim boundary preserved? | tests run? |
|---|---|---|---|---|---|---|
| `README.md` | `README.md` | restructure + expansion | 30-second orientation, quickstart, boundary clarity | yes | yes | yes |
| multiple existing docs | new index/guide files in `docs/` | additive wrappers | provide operator/reviewer/contributor entrypoints without removing legacy material | yes | yes | yes |

| README.md | README.md | update | Clarified SecureRails boundary wording and added repository/documentation index links for faster onboarding. | yes | yes | claim-boundary check, docs audits, unittest suite |
| docs/START_HERE.md | docs/START_HERE.md | update | Added role-specific callouts for operators/reviewers/contributors without changing doctrine. | yes | yes | claim-boundary check, docs audits, unittest suite |
| docs/WORKFLOW_CATALOG.md | docs/WORKFLOW_CATALOG.md | update | Added catalog schema guidance and fixed operator guide link to OPERATOR_QUICKSTART. | yes | yes | audit-workflows, unittest suite |

| README.md | README.md | clarity update | Add HELIOS to root positioning sentence and quick link index for operator discoverability. | yes | yes | `python -m unittest discover -s tests`; `python -m agialpha_docs audit-readmes --repo-root .` |
