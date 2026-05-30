import json, shutil, subprocess, tempfile
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
        agents=json.loads((run/'01_agents/agent_registry.json').read_text())['agents']
        assert all(a.get('role') == a.get('agent_role') for a in agents)
        imp=json.loads((run/'05_skill_import/skill_import_events.json').read_text())['skill_import_events']
        assert len(imp)>=3 and all(i['activation_status']=='inactive' for i in imp)
        assert all(i['import_status']=='imported_inactive_outside_sandbox' for i in imp)
        assert all(i.get('active_outside_sandbox') is False for i in imp)
        assert all(i.get('proofbundle_id') and i.get('evidence_docket_id') for i in imp)
        manifests=json.loads((run/'05_skill_import/agent_skill_manifests_after_import.json').read_text())['manifests']
        assert all(mm.get('activation_status') == 'sandbox_registered_inactive_outside_sandbox' for mm in manifests)
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



def test_build_data_uses_post_replay_falsification_truth():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'; out=Path(td)/'gen'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-build-data','--registry',str(reg),'--out',str(out)])
        metrics=json.loads((out/'network_skill_metrics.json').read_text())
        gate=json.loads((out/'claim_gate.json').read_text())
        assert metrics['replay_pass_rate'] == 1.0
        assert metrics['falsification_pass'] is True
        assert metrics['adversarial_failures_caught'] == 8
        assert gate['claim_gate_status'] == 'supported_local_bounded'


def test_falsification_syncs_adversarial_counter_to_metrics():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        pre_metrics=json.loads((run/'07_metrics/network_skill_metrics.json').read_text())
        assert pre_metrics['adversarial_failures_caught'] == 'not_reported'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        post_metrics=json.loads((run/'07_metrics/network_skill_metrics.json').read_text())
        audit=json.loads((run/'12_falsification/falsification_audit.json').read_text())
        assert post_metrics['adversarial_failures_caught'] == audit['adversarial_failures_caught']
        assert post_metrics['adversarial_failures_caught'] == 8


def test_no_blocked_persistence_attempts_when_none_recorded():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        metrics=json.loads((run/'07_metrics/network_skill_metrics.json').read_text())
        sandbox_records=json.loads((run/'02_jobs/sandbox_records.json').read_text())['sandbox_records']
        assert all(r.get('repo_mutation_allowed') is False for r in sandbox_records)
        assert all(r.get('autonomous_persistence_attempt_blocked') is False for r in sandbox_records)
        assert metrics['autonomous_persistence_attempts_blocked'] == 0


def test_skill_statuses_progress_from_pending_to_pass():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        skills=json.loads((run/'03_skill_extraction/accepted_skill_packages.json').read_text())['accepted_skill_packages']
        assert all(s['replay_status']=='pending' and s['falsification_status']=='pending' for s in skills)
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        skills=json.loads((run/'03_skill_extraction/accepted_skill_packages.json').read_text())['accepted_skill_packages']
        assert all(s['replay_status']=='pass' and s['falsification_status']=='pass' for s in skills)


def test_seed_changes_outputs():
    with tempfile.TemporaryDirectory() as td:
        run1=Path(td)/'run1'; run2=Path(td)/'run2'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run1),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run2),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','999'])
        m1=json.loads((run1/'07_metrics/network_skill_metrics.json').read_text())
        m2=json.loads((run2/'07_metrics/network_skill_metrics.json').read_text())
        assert m1['network_skill_propagation_lift'] != m2['network_skill_propagation_lift']


def test_registry_skill_packages_synced_after_audits():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        reg_skills=json.loads((reg/'skill_packages.json').read_text())['skill_packages']
        assert reg_skills
        assert all(s['replay_status'] == 'pass' and s['falsification_status'] == 'pass' for s in reg_skills)


def test_falsification_requires_boolean_replay_status():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        (run/'11_replay/replay_report.json').write_text(json.dumps({'replay_pass':'false','replay_passes':1}))
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)], capture_output=True, text=True)
        assert proc.returncode != 0
        assert 'replay_pass must be boolean' in (proc.stderr + proc.stdout)


def test_validate_rejects_import_active_outside_sandbox_or_production_activation():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        path=run/'05_skill_import/skill_import_events.json'
        doc=json.loads(path.read_text())
        doc['skill_import_events'][0]['active_outside_sandbox']=True
        doc['skill_import_events'][1]['production_activation_allowed']=True
        path.write_text(json.dumps(doc))
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)], capture_output=True, text=True)
        output=proc.stderr + proc.stdout
        assert proc.returncode != 0
        assert 'active_outside_sandbox must be false' in output
        assert 'production_activation_allowed must be false' in output


def test_validate_allows_safe_quarantined_non_import_event():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        path=run/'05_skill_import/skill_import_events.json'
        doc=json.loads(path.read_text())
        doc['skill_import_events'].append({
            'schema_version':'agialpha.skill_import.v1',
            'import_id':'import-quarantined-safe',
            'skill_id':'skill-poisoned',
            'target_agent_id':'agent-2',
            'import_status':'quarantined_missing_evidence',
            'activation_status':'quarantined',
            'active_outside_sandbox':False,
            'production_activation_allowed':False,
            'proofbundle_id':'unavailable',
            'evidence_docket_id':'unavailable',
            'claim_boundary':'local bounded public evidence; proof-gated recursive experiment engine; human-reviewed promotion required',
            'token_boundary':'$AGIALPHA utility-only accounting; no wallet/custody/payment/KYC/AML/trading',
            'regulated_boundary':'regulated-domain firewall enabled; blocked_human_review_required for regulated tasks',
            'human_review_required':True,
            'autonomous_persistence_allowed':False,
            'no_auto_merge':True,
        })
        path.write_text(json.dumps(doc))
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)])
        gate=json.loads((run/'13_claim_gate/network_compounding_claim_gate.json').read_text())
        assert gate['checks']['imported_skills_inactive_outside_sandbox'] is True
        assert gate['claim_gate_status'] == 'supported_local_bounded'


def test_validate_rejects_unsafe_quarantined_import_event():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        path=run/'05_skill_import/skill_import_events.json'
        doc=json.loads(path.read_text())
        doc['skill_import_events'].append({
            'schema_version':'agialpha.skill_import.v1',
            'import_id':'import-quarantined-unsafe',
            'skill_id':'skill-poisoned',
            'target_agent_id':'agent-2',
            'import_status':'quarantined_missing_evidence',
            'activation_status':'active',
            'active_outside_sandbox':True,
            'production_activation_allowed':True,
            'proofbundle_id':'unavailable',
            'evidence_docket_id':'unavailable',
            'claim_boundary':'local bounded public evidence; proof-gated recursive experiment engine; human-reviewed promotion required',
            'token_boundary':'$AGIALPHA utility-only accounting; no wallet/custody/payment/KYC/AML/trading',
            'regulated_boundary':'regulated-domain firewall enabled; blocked_human_review_required for regulated tasks',
            'human_review_required':True,
            'autonomous_persistence_allowed':False,
            'no_auto_merge':True,
        })
        path.write_text(json.dumps(doc))
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)], capture_output=True, text=True)
        output=proc.stderr + proc.stdout
        assert proc.returncode != 0
        assert 'activation_status must be inactive or quarantined for non-imported skill events' in output
        assert 'active_outside_sandbox must be false' in output
        assert 'production_activation_allowed must be false' in output


def test_validate_fails_when_network_skill_vault_missing():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        shutil.rmtree(run/'04_network_skill_vault')
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)], capture_output=True, text=True)
        assert proc.returncode != 0
        assert 'network skill vault publication evidence invalid' in (proc.stderr + proc.stdout)


def test_validate_fails_when_accepted_skill_missing_from_vault():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        vault_path=run/'04_network_skill_vault/network_skill_vault.json'
        vault=json.loads(vault_path.read_text())
        vault['skill_packages']=vault['skill_packages'][:1]
        vault_path.write_text(json.dumps(vault, sort_keys=True))
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)], capture_output=True, text=True)
        assert proc.returncode != 0
        assert 'accepted skills missing from network skill vault' in (proc.stderr + proc.stdout)


def test_validate_fails_when_vault_contains_unaccepted_skill():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        vault_path=run/'04_network_skill_vault/network_skill_vault.json'
        vault=json.loads(vault_path.read_text())
        extra=dict(vault['skill_packages'][0])
        extra['skill_id']='skill-unaccepted-corrupt'
        vault['skill_packages'].append(extra)
        vault_path.write_text(json.dumps(vault, sort_keys=True))
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)], capture_output=True, text=True)
        assert proc.returncode != 0
        assert 'unaccepted skills present in network skill vault' in (proc.stderr + proc.stdout)


def test_validate_fails_when_publication_events_contain_unaccepted_skill():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        publication_path=run/'04_network_skill_vault/skill_publication_events.json'
        publication=json.loads(publication_path.read_text())
        publication['events'].append({'skill_id':'skill-unaccepted-corrupt'})
        publication_path.write_text(json.dumps(publication, sort_keys=True))
        proc=subprocess.run(['python','-m','agialpha_engine','network-compounding-validate','--run',str(run)], capture_output=True, text=True)
        assert proc.returncode != 0
        assert 'unaccepted skills present in skill publication events' in (proc.stderr + proc.stdout)


def test_registry_run_preserves_proofbundles_and_evidence_dockets():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'; reg=Path(td)/'reg'
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-run','--repo-root','.','--registry',str(reg),'--out',str(run),'--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        registry_run=reg/'runs'/run.name
        proof_index=registry_run/'14_proofbundles/index.json'
        docket_index=registry_run/'15_evidence_dockets/index.json'
        assert proof_index.exists()
        assert docket_index.exists()
        proofbundles=json.loads(proof_index.read_text())['proofbundles']
        dockets=json.loads(docket_index.read_text())['evidence_dockets']
        assert proofbundles and dockets
        assert all((registry_run/'14_proofbundles'/f"{pb['proofbundle_id']}.json").exists() for pb in proofbundles)
        assert all((registry_run/'15_evidence_dockets'/f"{d['evidence_docket_id']}.json").exists() for d in dockets)
