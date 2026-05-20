import json
import subprocess
import sys
from pathlib import Path


def test_run_recursive_proof_propagates_sizing_flags(tmp_path: Path):
    run_dir = tmp_path / "run"
    cmd = [sys.executable, "-m", "agialpha_engine", "run-recursive-proof", "--repo-root", ".", "--out", str(run_dir), "--cycles", "5", "--train-tasks", "20", "--heldout-tasks", "7", "--variants-per-task", "4", "--seed", "42"]
    subprocess.run(cmd, check=True)
    manifest = json.loads((run_dir / "00_manifest.json").read_text())
    assert manifest["cycles"] == 5
    assert manifest["train_tasks"] == 20
    assert manifest["heldout_tasks"] == 7
    assert manifest["variants_per_task"] == 4


def test_child_mandates_overrides_heldout_for_backward_compat(tmp_path: Path):
    run_dir = tmp_path / "run2"
    cmd = [sys.executable, "-m", "agialpha_engine", "run-recursive-proof", "--repo-root", ".", "--out", str(run_dir), "--heldout-tasks", "9", "--child-mandates", "2", "--seed", "42"]
    subprocess.run(cmd, check=True)
    pairs = json.loads((run_dir / "02_mandate_pairs" / "mandate_pairs.json").read_text())
    assert len(pairs["mandate_pairs"]) == 2
