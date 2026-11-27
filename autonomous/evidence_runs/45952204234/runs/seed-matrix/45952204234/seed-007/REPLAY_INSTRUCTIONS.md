# Replay instructions

From the repository root, run:

```bash
python -m agialpha_first_loop.run --out runs/coldchain-energy-loop-001-replay
python -m unittest discover -s tests
```

Compare the generated `00_manifest.json` hash with the expected fields. The timestamp may differ; the deterministic content and pass/fail conditions should match.
