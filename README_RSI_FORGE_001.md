# RSI-FORGE-001 — Source-Code Recursive Self-Improvement of the Evidence Kernel

## Purpose

RSI-FORGE-001 is an obvious, concrete Recursive Self-Improvement experiment.

It does not merely simulate better scores. It evolves a real Python Evidence Kernel. Each cycle:

1. reads the current accepted kernel;
2. generates source-code mutation candidates;
3. executes each candidate on Evidence Docket tasks;
4. compares candidates against baselines;
5. accepts one improved kernel;
6. writes the accepted kernel source file and diff;
7. appends the candidate to an RSI state archive;
8. emits an ECI ledger entry;
9. computes a state hash;
10. triggers Move-37 dossier packaging when novelty and advantage are high;
11. uses the accepted source code as the parent for the next cycle.

The proof is visible in:

```text
03_kernel_lineage/
  accepted_kernel_v0.py
  accepted_kernel_v1.py
  ...
  diff_v0_to_v1.patch
  diff_v1_to_v2.patch
  lineage.json
```

## What makes this stronger

The previous evidence lineages showed local compounding. RSI-FORGE-001 makes the RSI mechanism direct:

```text
source code → evidence execution → accepted kernel → archive state → new source code
```

The central comparison is:

```text
B5 = RSI without archive reuse
B6 = full RSI with accepted kernel archive reuse
B7 = B6 + replay + dossier gate
```

The experiment passes locally only if:

- B6 beats B5 on held-out tasks;
- final kernel improves over the seed kernel;
- replay passes;
- falsification audit passes;
- vNext transfer passes;
- state hashes persist;
- ECI entries prove execution;
- Move-37 dossiers are emitted when triggered;
- hard safety counters remain zero.

## Claim boundary

This is bounded, repo-owned, CI/proxy evidence. It does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, real-world certification, guaranteed economic return, or civilization-scale capability.

## Local run

```bash
python -m agialpha_rsi_forge_001 run --out runs/rsi-forge-001/local --cycles 6 --seed 1001
python -m agialpha_rsi_forge_001 replay --docket runs/rsi-forge-001/local
python -m agialpha_rsi_forge_001 audit --docket runs/rsi-forge-001/local
python -m agialpha_rsi_forge_001 vnext --docket runs/rsi-forge-001/local
```

Open:

```text
runs/rsi-forge-001/local/scoreboard.html
```

## GitHub Actions

Upload the workflow files in `COPY_WORKFLOWS_TO_.github_workflows/`, then run:

1. **AGI ALPHA RSI-FORGE-001 / Autonomous Source-Code RSI**
2. **AGI ALPHA RSI-FORGE-001 / Independent Replay**
3. **AGI ALPHA RSI-FORGE-001 / Falsification Audit**
4. **AGI ALPHA RSI-FORGE-001 / vNext Transfer**
5. Optional: **AGI ALPHA RSI-FORGE-001 / Safe PR Proposal**

The safe PR workflow opens a human-review PR with the accepted kernel and summary. It does not auto-merge.
