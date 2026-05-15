import json, os, subprocess, sys, tempfile
from pathlib import Path


def test_build_data_emits_expected_generated_files_from_non_repo_cwd():
    out = tempfile.mkdtemp()
    gen = tempfile.mkdtemp()
    subprocess.check_call([sys.executable, "-m", "agialpha_valuation_support", "build", "--repo-root", ".", "--ascension-registry", "ascension_os_registry", "--comparables", "config/valuation_support_public_comparables.example.json", "--out", out])
    latest = json.load(open("valuation_support_registry/latest.json", "r", encoding="utf-8"))
    assert latest["run_ref"].startswith("runs/")
    outside_cwd = tempfile.mkdtemp()
    env = dict(os.environ)
    env["PYTHONPATH"] = str(Path(".").resolve())
    subprocess.check_call([
        sys.executable,
        "-m",
        "agialpha_valuation_support",
        "build-data",
        "--registry",
        str(Path("valuation_support_registry").resolve()),
        "--out",
        gen,
    ], cwd=outside_cwd, env=env)
    for name in ["latest.json", "summary.json", "implementation_comparison.json", "valuation_support_scorecard.json", "market_equivalence_sensitivity.json", "commercial_readiness.json", "moat_assessment.json", "risk_boundary.json"]:
        assert os.path.exists(os.path.join(gen, name))
    impl = json.load(open(os.path.join(gen, "implementation_comparison.json"), "r", encoding="utf-8"))
    assert impl.get("status") != "not_reported"
