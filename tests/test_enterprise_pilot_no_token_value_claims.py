import json
import subprocess
import sys
import tempfile
from pathlib import Path


def test_no_token_value_or_appreciation_claims_in_core_artifacts():
    run_dir = Path(tempfile.mkdtemp())
    subprocess.check_call([
        sys.executable, "-m", "agialpha_enterprise_pilot", "build",
        "--repo-root", ".", "--out", str(run_dir),
        "--workflow-family", "software_quality_pack", "--customer-mode", "synthetic_only",
    ])
    files = [
        "01_pilot_intake.json",
        "09_utility_settlement_receipt.json",
        "14_valuation_support_link.json",
    ]
    for name in files:
        payload = json.loads((run_dir / name).read_text())
        text = json.dumps(payload).lower()
        assert "token appreciation" not in text
        assert "securities value" not in text
        assert "guaranteed appreciation" not in text
