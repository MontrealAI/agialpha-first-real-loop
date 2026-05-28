import json
from pathlib import Path
from types import SimpleNamespace

from agialpha_engine.network_compounding import (
    _h,
    falsification_network_compounding,
    replay_network_compounding,
    run_network_compounding,
    validate_network_compounding,
)


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _args(**kwargs):
    return SimpleNamespace(**kwargs)


def test_proofbundles_rebuilt_against_final_replay_falsification_and_gate(tmp_path):
    run_dir = tmp_path / "run"
    registry_dir = tmp_path / "registry"
    run_network_compounding(
        _args(
            repo_root=".",
            registry=str(registry_dir),
            out=str(run_dir),
            jobs=5,
            target_agents=3,
            heldout_tasks=5,
            seed=123,
        )
    )
    replay_network_compounding(_args(run=str(run_dir)))
    falsification_network_compounding(_args(run=str(run_dir)))
    validate_network_compounding(_args(run=str(run_dir)))

    replay = _read(run_dir / "11_replay" / "replay_report.json")
    falsification = _read(run_dir / "12_falsification" / "falsification_audit.json")
    gate = _read(run_dir / "13_claim_gate" / "network_compounding_claim_gate.json")
    local_proofbundles = _read(run_dir / "14_proofbundles" / "index.json")["proofbundles"]
    registry_proofbundles = _read(registry_dir / "proofbundles.json")["proofbundles"]

    assert local_proofbundles
    assert local_proofbundles == registry_proofbundles
    for proofbundle in local_proofbundles:
        assert proofbundle["replay_report_hash"] == _h(replay)
        assert proofbundle["falsification_audit_hash"] == _h(falsification)
        assert proofbundle["claim_gate_hash"] == _h(gate)
        assert proofbundle["proofbundle_hash"] == _h(
            {k: v for k, v in proofbundle.items() if k != "proofbundle_hash"}
        )
        assert proofbundle["complete"] is True
