import json
import subprocess
import tempfile
from pathlib import Path


def _run_full(run: Path, reg: Path, jobs: int = 5):
    subprocess.check_call([
        'python','-m','agialpha_engine','network-compounding-run',
        '--repo-root','.','--registry',str(reg),'--out',str(run),
        '--jobs',str(jobs),'--target-agents','3','--heldout-tasks','5','--seed','123'
    ])


def test_claim_gate_not_supported_before_replay_and_falsification():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / 'run'
        reg = Path(td) / 'reg'
        _run_full(run, reg)
        gate = json.loads((run / '13_claim_gate/network_compounding_claim_gate.json').read_text())
        assert gate['claim_gate_status'] == 'not_supported'


def test_claim_gate_supported_after_replay_and_falsification():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / 'run'
        reg = Path(td) / 'reg'
        _run_full(run, reg)
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)])
        gate = json.loads((run / '13_claim_gate/network_compounding_claim_gate.json').read_text())
        assert gate['claim_gate_status'] == 'supported_local_bounded'
        assert gate['human_review_required'] is True
