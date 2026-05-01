"""Falsification audit helpers for RSI-GOVERNOR-001."""

from pathlib import Path


def falsification_report(docket: str | Path) -> dict:
    d = Path(docket)
    checks = {
        "manifest_present": (d / "00_manifest.json").exists(),
        "heldout_results_present": (d / "07_evaluation_results/heldout_results.json").exists(),
        "promotion_dossier_present": (d / "13_promotion_dossier/promotion_dossier.md").exists(),
    }
    return {"docket": str(d), "checks": checks, "falsification_pass": all(checks.values())}
