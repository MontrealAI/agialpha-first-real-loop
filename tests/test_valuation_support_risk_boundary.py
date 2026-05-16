import json
import os
import subprocess
import sys
import tempfile


MAJOR_OUTPUTS = [
    "00_manifest.json",
    "01_category_valuation_signal.json",
    "02_public_comparables.json",
    "03_agialpha_evidence_inventory.json",
    "04_implementation_side_comparison.json",
    "05_implementation_equivalence_score.json",
    "06_market_equivalence_sensitivity.json",
    "07_commercial_readiness.json",
    "08_moat_assessment.json",
    "09_risk_boundary.json",
    "10_missing_evidence.json",
]


def test_risk_boundary_present_in_major_outputs():
    out = tempfile.mkdtemp()
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "agialpha_valuation_support",
            "build",
            "--repo-root",
            ".",
            "--ascension-registry",
            "ascension_os_registry",
            "--comparables",
            "config/valuation_support_public_comparables.example.json",
            "--market-context",
            "config/valuation_support_market_context.example.json",
            "--out",
            out,
        ]
    )
    for rel_path in MAJOR_OUTPUTS:
        payload = json.load(open(os.path.join(out, rel_path), "r", encoding="utf-8"))
        assert payload.get("claim_boundary")
        assert payload.get("not_an_investment_claim") is True
