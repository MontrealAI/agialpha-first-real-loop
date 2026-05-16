import json
import subprocess
import sys
import tempfile
from pathlib import Path


def _build_run() -> Path:
    run_dir = Path(tempfile.mkdtemp())
    subprocess.check_call([
        sys.executable,
        "-m",
        "agialpha_enterprise_pilot",
        "build",
        "--repo-root",
        ".",
        "--out",
        str(run_dir),
        "--workflow-family",
        "software_quality_pack",
        "--customer-mode",
        "synthetic_only",
    ])
    return run_dir


def test_settlement_receipt_has_required_utility_only_wording():
    run_dir = _build_run()
    data = json.loads((run_dir / "09_utility_settlement_receipt.json").read_text())
    text = data["statement"]
    assert "utility-only local accounting receipt" in text
    assert "not payment processing" in text
    assert "not_an_investment_claim" in data and data["not_an_investment_claim"] is True


def test_valuation_support_link_disclaims_valuation_and_roi():
    run_dir = _build_run()
    data = json.loads((run_dir / "14_valuation_support_link.json").read_text())
    text = data["statement"].lower()
    assert "does not assert valuation" in text
    assert "roi" in text
    assert "fair market value" in text
