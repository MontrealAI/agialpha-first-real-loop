import json, subprocess, tempfile
from pathlib import Path

def test_network_run_end_to_end():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'; out=Path(td)/'gen'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-build-data','--registry',str(reg),'--out',str(out)])
        m=json.loads((run/'07_metrics/network_skill_metrics.json').read_text())
        assert m['jobs_run']>=3 and m['accepted_skill_packages']>=1
        acc=json.loads((run/'03_skill_extraction/accepted_skill_packages.json').read_text())['accepted_skill_packages'][0]
        assert acc['raw_task_result_ids'] and acc['proofbundle_id'] and acc['evidence_docket_id']
        imp=json.loads((run/'05_skill_import/skill_import_events.json').read_text())['skill_import_events']
        assert len(imp)>=3 and all(i['activation_status']=='inactive' for i in imp)
        assert 'network_skill_propagation_lift' in m
