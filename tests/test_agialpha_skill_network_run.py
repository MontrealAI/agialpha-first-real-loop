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


def test_validate_fails_when_claim_gate_not_supported():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','2','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)], capture_output=True, text=True)
        assert proc.returncode != 0
        assert 'claim gate not supported_local_bounded' in (proc.stderr + proc.stdout)


def test_replay_fails_on_tampered_lift():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        metrics=json.loads((run/'07_metrics/network_skill_metrics.json').read_text())
        metrics['network_skill_propagation_lift']=round(float(metrics['network_skill_propagation_lift'])+0.123,6)
        (run/'07_metrics/network_skill_metrics.json').write_text(json.dumps(metrics))
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        replay=json.loads((run/'11_replay/replay_report.json').read_text())
        assert replay['replay_pass'] is False
        assert replay['replay_passes'] == 0


def test_validate_fails_without_replay_and_falsification_execution():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)], capture_output=True, text=True)
        assert proc.returncode != 0
        assert 'replay did not pass' in (proc.stderr + proc.stdout)


def test_validate_requires_boolean_falsification_pass():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        (run/'12_falsification/falsification_audit.json').write_text(json.dumps({'falsification_pass':'false'}))
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)], capture_output=True, text=True)
        assert proc.returncode != 0
        assert 'falsification_pass must be boolean' in (proc.stderr + proc.stdout)


def test_validate_rejects_tampered_claim_gate_status():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','2','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        gate=json.loads((run/'13_claim_gate/network_compounding_claim_gate.json').read_text())
        gate['claim_gate_status']='supported_local_bounded'
        (run/'13_claim_gate/network_compounding_claim_gate.json').write_text(json.dumps(gate))
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)], capture_output=True, text=True)
        assert proc.returncode != 0
        assert ('claim gate status mismatch' in (proc.stderr + proc.stdout)) or ('claim gate not supported_local_bounded' in (proc.stderr + proc.stdout))


def test_replay_fails_on_tampered_canonical_comparison_lift():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        comparison=json.loads((run/'06_heldout_reuse_tests/comparison.json').read_text())
        comparison['NetworkSkillPropagationLift']=round(float(comparison['NetworkSkillPropagationLift'])+0.5,6)
        (run/'06_heldout_reuse_tests/comparison.json').write_text(json.dumps(comparison))
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        replay=json.loads((run/'11_replay/replay_report.json').read_text())
        assert replay['replay_pass'] is False
        assert replay['replay_passes'] == 0


def test_validate_requires_three_distinct_import_targets():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        imports_doc=json.loads((run/'05_skill_import/skill_import_events.json').read_text())
        for idx, ev in enumerate(imports_doc['skill_import_events']):
            ev['target_agent_id']='agent-2'
            ev['import_id']=f"dup-{idx}"
        (run/'05_skill_import/skill_import_events.json').write_text(json.dumps(imports_doc))
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)], capture_output=True, text=True)
        assert proc.returncode != 0
        assert ('claim gate status mismatch' in (proc.stderr + proc.stdout)) or ('claim gate not supported_local_bounded' in (proc.stderr + proc.stdout))


def test_registry_lineage_contains_all_accepted_skills():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        accepted=json.loads((run/'03_skill_extraction/accepted_skill_packages.json').read_text())['accepted_skill_packages']
        edges=json.loads((reg/'lineage_graph.json').read_text())['edges']
        accepted_pairs={(a['source_job_id'],a['skill_id']) for a in accepted}
        edge_pairs={(e['from'],e['to']) for e in edges}
        assert accepted_pairs == edge_pairs


def test_run_claim_gate_starts_not_supported_until_verification():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        gate=json.loads((run/'13_claim_gate/network_compounding_claim_gate.json').read_text())
        metrics=json.loads((run/'07_metrics/network_skill_metrics.json').read_text())
        assert gate['claim_gate_status'] == 'not_supported'
        assert metrics['replay_pass_rate'] == 'pending'
        assert metrics['falsification_pass'] == 'pending'


def test_replay_fails_on_tampered_absolute_scores():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        comp=json.loads((run/'06_heldout_reuse_tests/comparison.json').read_text())
        comp['D_no_shared_skill']=round(float(comp['D_no_shared_skill'])+0.2,6)
        comp['D_shared_skill_network']=round(float(comp['D_shared_skill_network'])+0.2,6)
        comp['NetworkSkillPropagationLift']=round(comp['D_shared_skill_network']-comp['D_no_shared_skill'],6)
        (run/'06_heldout_reuse_tests/comparison.json').write_text(json.dumps(comp))
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        replay=json.loads((run/'11_replay/replay_report.json').read_text())
        assert replay['replay_pass'] is False

