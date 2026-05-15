import json, os, subprocess, sys, tempfile


def test_valuation_support_build_cli_outputs_manifest_and_boundary_text():
    run_dir = tempfile.mkdtemp()
    out = tempfile.mkdtemp()
    subprocess.check_call([sys.executable, "-m", "agialpha_ascension_os", "run-cycle", "--repo-root", ".", "--registry", "ascension_os_registry", "--out", run_dir])
    subprocess.check_call([sys.executable, "-m", "agialpha_valuation_support", "build", "--repo-root", ".", "--ascension-registry", "ascension_os_registry", "--comparables", "config/valuation_support_public_comparables.example.json", "--out", out])
    manifest = json.load(open(os.path.join(out, "00_manifest.json"), "r", encoding="utf-8"))
    assert manifest["human_review_required"] is True
    assert "does not assert a valuation" in manifest["statement"].lower()
