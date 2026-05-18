import json
import subprocess
import sys
from pathlib import Path


def run_cmd(*args):
    subprocess.check_call([sys.executable, "-m", "agialpha_engine", *args])


def make_run(tmp_path: Path) -> Path:
    out = tmp_path / "engine002"
    run_cmd("run-proof", "--repo-root", ".", "--out", str(out), "--mandate-pairs", "3", "--seed", "1337")
    return out


def read_json(path: Path):
    return json.loads(path.read_text())
