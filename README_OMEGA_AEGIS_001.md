# AGI ALPHA OMEGA-AEGIS-001

## Adversarial Evidence Immunity Gauntlet

OMEGA-AEGIS-001 is a bounded, repo-owned, synthetic adversarial evidence experiment. It tests whether AGI ALPHA can detect forged, corrupted, overclaimed, or unsafe Evidence Dockets before claim promotion.

The purpose is not to prove empirical SOTA. The purpose is to harden AGI ALPHA's evidence institution.

## What it proves if it passes

Local claim only:

> Under deterministic CI conditions, the archive-aware B6 validator catches the generated synthetic adversarial evidence attacks with zero false accepts, produces a replayable Evidence Docket, and preserves hard safety invariants.

It does **not** claim AGI, ASI, SOTA, safe autonomy, real-world certification, external validation, or civilization-scale capability.

## Why this is important

AGI ALPHA's paper states that empirical claims require Evidence Dockets, baselines, ProofBundles, replay logs, safety/cost ledgers, validator reports, delayed outcomes, and independent reproduction. The next failure mode is forged evidence. OMEGA-AEGIS-001 attacks the evidence layer itself.

## Files

Upload these folders/files into the repository:

```text
omega_aegis_001/
tests/test_omega_aegis_001.py
.github/workflows/omega-aegis-001-autonomous.yml
.github/workflows/omega-aegis-001-external-replay.yml
.github/workflows/omega-aegis-001-falsification-audit.yml
.github/workflows/omega-aegis-001-vnext-transfer.yml
.github/ISSUE_TEMPLATE/omega-aegis-001-external-review.md
README_OMEGA_AEGIS_001.md
```

## Run order

1. Run `AGI ALPHA OMEGA-AEGIS-001 / Autonomous`.
2. Open the generated artifact.
3. Run `AGI ALPHA OMEGA-AEGIS-001 / External Replay` with the root hash from the artifact.
4. Run `AGI ALPHA OMEGA-AEGIS-001 / Falsification Audit`.
5. Run `AGI ALPHA OMEGA-AEGIS-001 / vNext Transfer`.
6. Open an external-review issue using the included template.

## GitHub UI instructions

1. Go to `https://github.com/MontrealAI/agialpha-first-real-loop`.
2. Open the `Actions` tab.
3. Select `AGI ALPHA OMEGA-AEGIS-001 / Autonomous`.
4. Click `Run workflow`.
5. Leave both checkboxes enabled unless you want artifact-only mode.
6. Click the green `Run workflow` button.
7. Wait for the green checkmark.
8. Open the completed run.
9. Download the `omega-aegis-001-<run-id>` artifact.
10. Copy the `root_hash` from `evidence-run-manifest.json`.
11. Run `AGI ALPHA OMEGA-AEGIS-001 / External Replay` and paste the root hash.

## Safety boundary

This experiment is defensive and synthetic only. It does not scan external targets, execute exploits, generate malware, disclose secrets, or auto-merge patches.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
