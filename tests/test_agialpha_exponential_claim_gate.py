import json
import subprocess
import tempfile
from pathlib import Path


def test_exponential_compounding_defaults_to_strategic_target_without_multi_cycle_evidence():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / 'run'
        reg = Path(td) / 'reg'
        subprocess.check_call([
            'python','-m','agialpha_engine','network-compounding-run',
            '--repo-root','.','--registry',str(reg),'--out',str(run),
            '--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'
        ])
        metrics = json.loads((run / '07_metrics/network_skill_metrics.json').read_text())
        assert metrics['exponential_compounding_supported'] is False
        assert 'strategic target' in metrics['exponential_compounding_status']
