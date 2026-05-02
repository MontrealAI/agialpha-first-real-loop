"""Lifecycle orchestration helpers for RSI-GOVERNOR-001."""

from __future__ import annotations

from pathlib import Path

from .cli import run, replay, falsification_audit


def run_pre_review(repo_root: str, out: str, candidate_count: int) -> None:
    run(repo_root, out, candidate_count)
    docket = Path(out) / "rsi-governor-evidence-docket"
    replay(str(docket))
    falsification_audit(str(docket))


def run_post_merge(repo_root: str, out: str) -> None:
    # Placeholder: delayed outcome + vNext canary handled by dedicated workflows.
    Path(out).mkdir(parents=True, exist_ok=True)
