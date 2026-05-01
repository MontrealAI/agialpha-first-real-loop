# AGI ALPHA ASCENSION-001

## Governed Recursive Self-Improvement of the Evidence Institution

ASCENSION-001 is a bounded, repo-owned, CI/proxy experiment designed to test the central RSI compounding question:

> Can a replayable, validator-gated RSI loop improve the institution that produces future evidence?

The experiment does not ask whether an agent can solve one task. It asks whether AGI ALPHA can create a reusable evidence capability archive, use that archive to improve the next cycle, pass replay, preserve state integrity, and outperform a no-reuse RSI baseline on held-out transfer tasks.

## What makes this experiment different

ASCENSION-001 tests successful compounding directly:

```text
repo scan
→ deterministic RSI state
→ baseline ladder B0-B7
→ proof bundles
→ replay logs
→ ECI ledger
→ capability archive v0 → v1 → v2 → v3
→ held-out transfer
→ Move-37 dossier gate
→ external reviewer kit
```

The decisive comparison is:

```text
B5 = AGI ALPHA RSI without archive reuse
B6 = full AGI ALPHA RSI with capability archive reuse
B7 = B6 + independent replay + dossier gate
```

The experiment passes locally only if B6 beats B5, held-out transfer is positive, replay passes, drift sentinel passes, hard safety counters remain zero, and every high-novelty result is dossier-gated.

## Claim boundary

This experiment does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, real-world certification, guaranteed economic return, or civilization-scale capability. It is a bounded, repo-owned, CI/proxy Evidence Docket experiment testing whether governed RSI state, replay, baselines, and capability archives can improve future verified work.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

## GitHub web UI run guide

1. Upload the files from this package into the repository.
2. Go to **Actions**.
3. Click **AGI ALPHA ASCENSION-001 / Autonomous RSI Compounding**.
4. Click **Run workflow**.
5. Leave the defaults:
   - cycles = `3`
   - task_count = `9`
   - seed = `1001`
6. Wait for the green check.
7. Open the run.
8. Download the artifact named `ascension-001-<run-id>`.
9. Open the HTML scoreboard inside:
   - `docs/ascension-001/index.html`
10. Then run:
   - **AGI ALPHA ASCENSION-001 / Independent Replay**
   - **AGI ALPHA ASCENSION-001 / Falsification Audit**
   - **AGI ALPHA ASCENSION-001 / vNext Transfer**

## What to look for

A successful run shows:

- B6 beats B5 on all tasks.
- Held-out transfer tasks pass.
- Replay passes.
- Drift sentinel passes.
- ECI ledger exists.
- Move-37 dossiers exist when novelty is high.
- `EvidenceCompilerCapabilityArchive-v3` exists after the default run.
- Safety incidents = 0.
- Policy violations = 0.
- Root hash is present.
- External reviewer kit is present.

## Local run

```bash
python -m unittest discover -s tests -p "test_ascension_001.py"
python -m agialpha_ascension_001 run --repo-root . --out runs/ascension-001/local --cycles 3 --task-count 9 --seed 1001
python -m agialpha_ascension_001 replay --docket runs/ascension-001/local/ascension-001-evidence-docket
python -m agialpha_ascension_001 audit --docket runs/ascension-001/local/ascension-001-evidence-docket
```

## Files produced

```text
ascension-001-evidence-docket/
  00_manifest.json
  01_claims_matrix/
  02_environment/
  03_state_hashes/
  03_task_manifests/
  04_baselines/
  06_proof_bundles/
  07_replay_logs/
  08_cost_ledgers/
  09_safety_ledgers/
  09_eci_ledger/
  10_validator_reports/
  11_safe_patch_proposal/
  12_move37_dossiers/
  13_capability_archive/
  14_falsification_audit/
  15_external_reviewer_kit/
  16_summary_tables/
  REPLAY_INSTRUCTIONS.md
```

## Why this matters

The paper defines AGI Alpha RSI as a deterministic governance control plane: exploration is allowed, outcome authority is mechanical, promotion requires evidence, compounding requires persistence, and autonomy requires authority. ASCENSION-001 turns that doctrine into a runnable CI experiment.
