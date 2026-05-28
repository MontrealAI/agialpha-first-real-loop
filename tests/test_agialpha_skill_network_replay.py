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
