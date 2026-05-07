# Content Preservation Ledger


| original file | changed file | change type | rationale | content preserved? | claim boundary preserved? | tests run? |
|---|---|---|---|---|---|---|
| `README.md` | `README.md` | restructure + expansion | 30-second orientation, quickstart, boundary clarity | yes | yes | yes |
| multiple existing docs | new index/guide files in `docs/` | additive wrappers | provide operator/reviewer/contributor entrypoints without removing legacy material | yes | yes | yes |

| README.md | README.md | update | Clarified SecureRails boundary wording and added repository/documentation index links for faster onboarding. | yes | yes | claim-boundary check, docs audits, unittest suite |
| docs/START_HERE.md | docs/START_HERE.md | update | Added role-specific callouts for operators/reviewers/contributors without changing doctrine. | yes | yes | claim-boundary check, docs audits, unittest suite |
| docs/WORKFLOW_CATALOG.md | docs/WORKFLOW_CATALOG.md | update | Added catalog schema guidance and fixed operator guide link to OPERATOR_QUICKSTART. | yes | yes | audit-workflows, unittest suite |
| `README.md` | `README.md` | boundary wording normalization | Align SecureRails boundary phrasing with compliance language while keeping scope unchanged. | yes | yes | secure_rails_claim_boundary_check, agialpha_docs audits |
| `docs/START_HERE.md` | `docs/START_HERE.md` | usability polish | Converted role-path references to relative Markdown links for faster operator/reviewer onboarding. | yes | yes | agialpha_docs audit-links, unittest docs tests |
