import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path


def _run_build(out: str) -> None:
    subprocess.check_call([
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
        "--out",
        out,
    ])


def test_build_data_emits_expected_generated_files_from_non_repo_cwd():
    out = tempfile.mkdtemp()
    gen = tempfile.mkdtemp()
    _run_build(out)
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
    impl = json.load(open(os.path.join(gen, "implementation_comparison.json"), "r", encoding="utf-8"))
    assert impl.get("status") != "not_reported"


def test_build_data_supports_legacy_registry_prefixed_run_ref():
    out = tempfile.mkdtemp()
    gen = tempfile.mkdtemp()
    _run_build(out)
    tmp_registry = Path(tempfile.mkdtemp()) / "valuation_support_registry"
    shutil.copytree("valuation_support_registry", tmp_registry)
    latest_path = tmp_registry / "latest.json"
    latest = json.loads(latest_path.read_text(encoding="utf-8"))
    latest["run_ref"] = f"valuation_support_registry/{latest['run_ref']}"
    latest_path.write_text(json.dumps(latest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    subprocess.check_call([
        sys.executable,
        "-m",
        "agialpha_valuation_support",
        "build-data",
        "--registry",
        str(tmp_registry),
        "--out",
        gen,
    ])
    impl = json.load(open(os.path.join(gen, "implementation_comparison.json"), "r", encoding="utf-8"))
    assert impl.get("status") != "not_reported"
