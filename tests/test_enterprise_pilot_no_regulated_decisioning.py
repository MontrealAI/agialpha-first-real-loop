import json
import subprocess
import sys
import tempfile
from pathlib import Path


def test_regulated_domain_signal_is_blocked_and_human_review_required():
    run_dir = Path(tempfile.mkdtemp())
    subprocess.check_call([
        sys.executable, "-m", "agialpha_enterprise_pilot", "build",
        "--repo-root", ".", "--out", str(run_dir),
        "--workflow-family", "software_quality_pack", "--customer-mode", "synthetic_only",
    ])
    triage = json.loads((run_dir / "02_regulated_boundary_triage.json").read_text())
    assert triage["regulated_boundary_result"] == "passed"
    assert triage["human_review_required"] is True

    # Directly test regulated boundary triage behavior with a regulated-domain input.
    from agialpha_enterprise_pilot.regulated_boundary import triage
    blocked = triage("credit underwriting decision for applicants")
    assert blocked["regulated_boundary_result"] == "blocked"
    assert blocked["regulated_boundary_blocked"] is True
    assert blocked["documentation_only"] is True
    assert blocked["human_review_required"] is True
