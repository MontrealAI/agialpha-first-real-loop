import json
import subprocess
import sys
import tempfile
from pathlib import Path


def _run_full(run: Path, reg: Path, jobs: int = 5):
    subprocess.check_call([
        sys.executable,'-m','agialpha_engine','network-compounding-run',
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
        subprocess.check_call([sys.executable,'-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call([sys.executable,'-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        subprocess.check_call([sys.executable,'-m','agialpha_engine','network-compounding-validate','--run',str(run)])
        gate = json.loads((run / '13_claim_gate/network_compounding_claim_gate.json').read_text())
        assert gate['claim_gate_status'] == 'supported_local_bounded'
        assert gate['human_review_required'] is True


def test_validate_catches_missing_accepted_skill_evidence_docket():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / 'run'
        reg = Path(td) / 'reg'
        _run_full(run, reg)
        subprocess.check_call([sys.executable,'-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call([sys.executable,'-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        accepted = json.loads((run / '03_skill_extraction/accepted_skill_packages.json').read_text())['accepted_skill_packages']
        missing_docket_id = accepted[0]['evidence_docket_id']
        (run / '15_evidence_dockets' / f'{missing_docket_id}.json').unlink()
        completed = subprocess.run(
            [sys.executable,'-m','agialpha_engine','network-compounding-validate','--run',str(run)],
            text=True,
            capture_output=True,
        )
        assert completed.returncode != 0
        assert 'evidence docket integrity errors' in completed.stderr


def test_validate_report_records_evidence_docket_integrity_pass():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / 'run'
        reg = Path(td) / 'reg'
        _run_full(run, reg)
        subprocess.check_call([sys.executable,'-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call([sys.executable,'-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        subprocess.check_call([sys.executable,'-m','agialpha_engine','network-compounding-validate','--run',str(run)])
        validate_report = json.loads((run / 'validate.json').read_text())
        assert validate_report['validation_pass'] is True
        assert validate_report['proofbundle_integrity_pass'] is True
        assert validate_report['evidence_docket_integrity_pass'] is True
