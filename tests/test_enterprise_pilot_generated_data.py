import os
import subprocess
import sys
import tempfile


def test_build_data_exports_pilot_outcomes():
    run_dir = tempfile.mkdtemp()
    out_dir = tempfile.mkdtemp()
    reg_dir = tempfile.mkdtemp()
    subprocess.check_call([
        sys.executable, "-m", "agialpha_enterprise_pilot", "build",
        "--repo-root", ".", "--out", run_dir,
        "--workflow-family", "software_quality_pack",
        "--customer-mode", "synthetic_only",
        "--registry", reg_dir,
    ])
    subprocess.check_call([
        sys.executable, "-m", "agialpha_enterprise_pilot", "build-data",
        "--registry", reg_dir, "--out", out_dir,
    ])
    assert os.path.exists(os.path.join(out_dir, "pilot_outcomes.json"))
