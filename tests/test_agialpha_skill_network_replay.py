import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


def _h(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_proofbundles_rehash_to_final_replay_and_falsification_artifacts():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / "run"
        reg = Path(td) / "reg"
        subprocess.check_call([
            "python", "-m", "agialpha_engine", "network-compounding-run",
            "--repo-root", ".", "--registry", str(reg), "--out", str(run),
            "--jobs", "5", "--target-agents", "3", "--heldout-tasks", "5", "--seed", "123",
        ])
        subprocess.check_call(["python", "-m", "agialpha_engine", "network-compounding-replay", "--run", str(run)])
        subprocess.check_call(["python", "-m", "agialpha_engine", "network-compounding-falsification-audit", "--run", str(run)])
        subprocess.check_call(["python", "-m", "agialpha_engine", "network-compounding-validate", "--run", str(run)])

        replay = _read(run / "11_replay" / "replay_report.json")
        audit = _read(run / "12_falsification" / "falsification_audit.json")
        gate = _read(run / "13_claim_gate" / "network_compounding_claim_gate.json")
        run_bundles = _read(run / "14_proofbundles" / "index.json")["proofbundles"]
        registry_bundles = _read(reg / "proofbundles.json")["proofbundles"]

        assert run_bundles
        assert len(run_bundles) == len(registry_bundles)
        for bundle in run_bundles + registry_bundles:
            assert bundle["complete"] is True
            assert bundle["replay_report_hash"] == _h(replay)
            assert bundle["falsification_audit_hash"] == _h(audit)
            assert bundle["claim_gate_hash"] == _h(gate)
            body = {k: v for k, v in bundle.items() if k != "proofbundle_hash"}
            assert bundle["proofbundle_hash"] == _h(body)


def test_initial_proofbundle_hashes_persisted_comparison_artifact():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / "run"
        reg = Path(td) / "reg"
        subprocess.check_call([
            "python", "-m", "agialpha_engine", "network-compounding-run",
            "--repo-root", ".", "--registry", str(reg), "--out", str(run),
            "--jobs", "5", "--target-agents", "3", "--heldout-tasks", "5", "--seed", "123",
        ])

        persisted_comparison = _read(run / "06_heldout_reuse_tests" / "comparison.json")
        run_bundles = _read(run / "14_proofbundles" / "index.json")["proofbundles"]
        registry_bundles = _read(reg / "proofbundles.json")["proofbundles"]

        assert run_bundles
        for bundle in run_bundles + registry_bundles:
            assert bundle["complete"] is True
            assert bundle["b6_vs_b5_comparison_hash"] == _h(persisted_comparison)


def test_validate_rejects_tampered_standalone_proofbundle_file():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / "run"
        reg = Path(td) / "reg"
        subprocess.check_call([
            "python", "-m", "agialpha_engine", "network-compounding-run",
            "--repo-root", ".", "--registry", str(reg), "--out", str(run),
            "--jobs", "5", "--target-agents", "3", "--heldout-tasks", "5", "--seed", "123",
        ])
        subprocess.check_call(["python", "-m", "agialpha_engine", "network-compounding-replay", "--run", str(run)])
        subprocess.check_call(["python", "-m", "agialpha_engine", "network-compounding-falsification-audit", "--run", str(run)])

        index = _read(run / "14_proofbundles" / "index.json")
        proofbundle_id = index["proofbundles"][0]["proofbundle_id"]
        standalone_path = run / "14_proofbundles" / f"{proofbundle_id}.json"
        standalone = _read(standalone_path)
        standalone["complete"] = False
        standalone_path.write_text(json.dumps(standalone), encoding="utf-8")

        proc = subprocess.run(
            ["python", "-m", "agialpha_engine", "network-compounding-validate", "--run", str(run)],
            capture_output=True,
            text=True,
        )
        assert proc.returncode != 0
        assert "standalone proofbundle file mismatch" in (proc.stderr + proc.stdout)


def test_validate_rejects_stale_source_job_hash_after_source_job_tamper():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / "run"
        reg = Path(td) / "reg"
        subprocess.check_call([
            "python", "-m", "agialpha_engine", "network-compounding-run",
            "--repo-root", ".", "--registry", str(reg), "--out", str(run),
            "--jobs", "5", "--target-agents", "3", "--heldout-tasks", "5", "--seed", "123",
        ])
        subprocess.check_call(["python", "-m", "agialpha_engine", "network-compounding-replay", "--run", str(run)])
        subprocess.check_call(["python", "-m", "agialpha_engine", "network-compounding-falsification-audit", "--run", str(run)])

        source_jobs_path = run / "02_jobs" / "source_jobs.json"
        source_jobs = _read(source_jobs_path)
        source_jobs["jobs"][0]["score"] = round(float(source_jobs["jobs"][0]["score"]) + 0.001, 3)
        source_jobs_path.write_text(json.dumps(source_jobs), encoding="utf-8")

        proc = subprocess.run(
            ["python", "-m", "agialpha_engine", "network-compounding-validate", "--run", str(run)],
            capture_output=True,
            text=True,
        )
        assert proc.returncode != 0
        assert "does not match current run artifacts" in (proc.stderr + proc.stdout)


def test_validate_rejects_missing_declared_raw_task_result_id():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / "run"
        reg = Path(td) / "reg"
        subprocess.check_call([
            "python", "-m", "agialpha_engine", "network-compounding-run",
            "--repo-root", ".", "--registry", str(reg), "--out", str(run),
            "--jobs", "5", "--target-agents", "3", "--heldout-tasks", "5", "--seed", "123",
        ])
        subprocess.check_call(["python", "-m", "agialpha_engine", "network-compounding-replay", "--run", str(run)])
        subprocess.check_call(["python", "-m", "agialpha_engine", "network-compounding-falsification-audit", "--run", str(run)])

        accepted_path = run / "03_skill_extraction" / "accepted_skill_packages.json"
        accepted_doc = _read(accepted_path)
        accepted_doc["accepted_skill_packages"][0]["raw_task_result_ids"].append("raw-missing-evidence")
        accepted_path.write_text(json.dumps(accepted_doc), encoding="utf-8")

        proc = subprocess.run(
            ["python", "-m", "agialpha_engine", "network-compounding-validate", "--run", str(run)],
            capture_output=True,
            text=True,
        )
        assert proc.returncode != 0
        assert "does not match current run artifacts" in (proc.stderr + proc.stdout)
