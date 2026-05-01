#!/usr/bin/env bash
set -euo pipefail
OUT="${1:-runs/rsi-forge-001/local}"
python -m agialpha_rsi_forge_001 run --out "$OUT" --cycles 6 --seed 1001
python -m agialpha_rsi_forge_001 replay --docket "$OUT"
python -m agialpha_rsi_forge_001 audit --docket "$OUT"
python -m agialpha_rsi_forge_001 vnext --docket "$OUT"
echo "RSI-FORGE-001 complete: $OUT/scoreboard.html"
