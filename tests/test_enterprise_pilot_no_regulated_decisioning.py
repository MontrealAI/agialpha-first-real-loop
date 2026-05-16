import json
import subprocess
import sys
import tempfile
from pathlib import Path


def test_regulated_domain_fixture_is_blocked_and_human_review_required():
    run_dir = Path(tempfile.mkdtemp())
    subprocess.check_call([
        sys.executable, "-m", "agialpha_enterprise_pilot", "build",
        "--repo-root", ".", "--out", str(run_dir),
        "--workflow-family", "software_quality_pack", "--customer-mode", "synthetic_only",
        "--intended-use", "credit underwriting decision for applicants",
    ])
    triage = json.loads((run_dir / "02_regulated_boundary_triage.json").read_text())
    assert triage["regulated_boundary_result"] == "regulated_boundary_blocked"
    assert triage["human_review_required"] is True
    assert triage["decision_output"] == "documentation_only"
