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
        manifests_before=json.loads((run/'01_agents/agent_skill_manifests_before.json').read_text())['manifests']
        assert all(not mm.get('imported_skills') for mm in manifests_before)
        manifests=json.loads((run/'05_skill_import/agent_skill_manifests_after_import.json').read_text())['manifests']
        imported_agents=[mm for mm in manifests if mm.get('imported_skills')]
        assert len(imported_agents) >= 3
        assert 'network_skill_propagation_lift' in m


def test_validate_fails_on_failed_replay_or_falsification():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        (run/'11_replay/replay_report.json').write_text(json.dumps({'replay_pass': False, 'replay_passes': 0}))
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)], capture_output=True, text=True)
        assert proc.returncode != 0
        assert 'replay did not pass' in (proc.stderr + proc.stdout)


def test_run_fails_cleanly_for_zero_heldout_tasks():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','0','--seed','123'], capture_output=True, text=True)
        assert proc.returncode != 0
        assert 'heldout_tasks must be >= 1' in (proc.stderr + proc.stdout)


def test_validate_fails_on_inconsistent_replay_fields():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        (run/'11_replay/replay_report.json').write_text(json.dumps({'replay_pass': False, 'replay_passes': 1}))
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)], capture_output=True, text=True)
        assert proc.returncode != 0
        assert 'replay report inconsistent' in (proc.stderr + proc.stdout)
