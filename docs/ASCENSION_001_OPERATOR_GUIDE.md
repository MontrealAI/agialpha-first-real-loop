# Non-Technical Operator Guide — ASCENSION-001

## Goal

Run the strongest current AGI ALPHA RSI compounding experiment from the GitHub web UI.

## Best first run

Use this workflow:

**AGI ALPHA ASCENSION-001 / Autonomous RSI Compounding**

Keep all defaults. Click **Run workflow**.

## After it finishes

Open the run and confirm:

- green checkmark;
- artifact exists;
- artifact name starts with `ascension-001-`;
- no safety failure;
- no replay failure.

## Then run the second workflow

Run:

**AGI ALPHA ASCENSION-001 / Independent Replay**

Leave `source_run_id` blank for a clean fresh replay, or enter the run id from the first workflow to replay that artifact.

## Then run the third workflow

Run:

**AGI ALPHA ASCENSION-001 / Falsification Audit**

This checks that the result is not overclaiming and that safety counters are zero.

## Then run vNext

Run:

**AGI ALPHA ASCENSION-001 / vNext Transfer**

This makes the compounding claim stronger because it asks the archive to help with a harder future task.

## What result should impress you

The impressive result is not a single score. It is the chain:

```text
B6 > B5
held-out transfer positive
replay passes
state hashes persist
archive version increases
Move-37 dossiers appear when novelty is high
safety counters stay zero
external reviewer kit is ready
```

## Claim boundary

This experiment does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, real-world certification, guaranteed economic return, or civilization-scale capability. It is a bounded, repo-owned, CI/proxy Evidence Docket experiment testing whether governed RSI state, replay, baselines, and capability archives can improve future verified work.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
