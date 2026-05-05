# Troubleshooting

Use this pattern for each failure: **symptom → likely cause → fix → what not to do**.

- Undocumented workflow → new `.github/workflows/*` not in catalog → update `docs/WORKFLOW_CATALOG.md` → do not bypass docs-audit.
- Missing script → workflow references nonexistent file → restore path or update workflow → do not disable failing steps.
- Docs claim failure / token language flagged → overclaim wording → rewrite conservatively per `docs/CLAIM_BOUNDARIES.md` → do not weaken boundaries.
- Claim-audit false positive → boundary negation wording pattern mismatch → rephrase with explicit “not” scope → do not remove boundary text.
- Missing safety ledger counter → schema/output omission → add ledger field + tests → do not ship partial docket.
- Broken link → moved/renamed docs → fix links, rerun link audit → do not leave stale pointers.
- Artifact not found / replay failed / falsification failed → run config mismatch or missing upload → inspect logs, rerun with corrected inputs → do not promote claims.
- Pages not updated / Mission Control not published → publisher workflow failed/perms issue → check `evidence-hub-publish` and Pages settings → do not do direct Pages deploy from random workflow.
- no-auto-merge or use-case triage failed → policy guard triggered → resolve policy issue and re-run → do not force merge.
- Actions permission warning / Node.js deprecation warning → workflow runtime drift → update permissions/action versions → do not ignore repeated warnings.
