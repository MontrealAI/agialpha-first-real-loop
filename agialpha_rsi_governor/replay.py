"""Replay helpers for RSI-GOVERNOR-001."""

from pathlib import Path


def replay_docket(docket: str | Path) -> dict:
    d = Path(docket)
    replay_pass = (d / "00_manifest.json").exists() and (d / "07_evaluation_results/heldout_results.json").exists()
    return {"docket": str(d), "replay_pass": replay_pass}
