"""Compatibility wrapper for vNext canary execution."""

from __future__ import annotations

from pathlib import Path

from .canary import default_canary_report


def run_vnext_canary(repo_root: str | Path = ".") -> dict:
    """Return deterministic vNext canary report for compatibility callers."""
    _ = Path(repo_root)
    return default_canary_report()


__all__ = ["run_vnext_canary"]
