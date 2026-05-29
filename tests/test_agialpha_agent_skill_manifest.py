import json
import subprocess
import tempfile
from pathlib import Path

from agialpha_engine.network_skill_metrics import compute_d_metric


def test_agent_manifests_include_required_skill_lists_and_policy():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / 'run'
        reg = Path(td) / 'reg'
        subprocess.check_call([
            'python','-m','agialpha_engine','network-compounding-run',
            '--repo-root','.','--registry',str(reg),'--out',str(run),
            '--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'
        ])
        manifests = json.loads((run / '05_skill_import/agent_skill_manifests_after_import.json').read_text())['manifests']
        assert len(manifests) >= 3
        for m in manifests:
            for key in ['native_skills','imported_skills','quarantined_skills','rejected_skills']:
                assert key in m and isinstance(m[key], list)
            assert m['activation_status'] == 'sandbox_registered_inactive_outside_sandbox'
            assert m['production_activation_allowed'] is False
            assert m['skill_import_policy']
            assert m['claim_boundary'] and m['token_boundary'] and m['regulated_boundary']


def test_imported_skills_are_inactive_outside_sandbox_by_default():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / 'run'
        reg = Path(td) / 'reg'
        subprocess.check_call([
            'python','-m','agialpha_engine','network-compounding-run',
            '--repo-root','.','--registry',str(reg),'--out',str(run),
            '--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'
        ])
        imports = json.loads((run / '05_skill_import/skill_import_events.json').read_text())['skill_import_events']
        assert len(imports) >= 3
        assert all(e['activation_status'] == 'inactive' for e in imports)
        assert all(e['import_status'] == 'imported_inactive_outside_sandbox' for e in imports)
        assert all(e.get('active_outside_sandbox') is False for e in imports)
        assert all(e.get('proofbundle_id') and e.get('evidence_docket_id') for e in imports)
        assert all(e.get('autonomous_persistence_allowed') is False for e in imports)


def test_target_agent_manifests_keep_imports_sandbox_inactive_and_human_review_pending():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / 'run'
        reg = Path(td) / 'reg'
        subprocess.check_call([
            'python', '-m', 'agialpha_engine', 'network-compounding-run',
            '--repo-root', '.', '--registry', str(reg), '--out', str(run),
            '--jobs', '5', '--target-agents', '3', '--heldout-tasks', '5', '--seed', '123'
        ])
        manifests = json.loads((run / '05_skill_import/agent_skill_manifests_after_import.json').read_text())['manifests']
        target_manifests = [m for m in manifests if m['imported_skills']]

        assert len(target_manifests) == 3
        assert all(m['production_activation_allowed'] is False for m in target_manifests)
        assert all(m['human_review_status'] == 'pending' for m in target_manifests)
        assert all(m['activation_status'] == 'sandbox_registered_inactive_outside_sandbox' for m in target_manifests)
        assert all(m['imported_skills'] for m in target_manifests)


def test_network_d_metric_does_not_render_missing_values_as_zero():
    assert compute_d_metric([]) == 'not_reported'
    assert compute_d_metric([{'validator_pass': 1, 'replay_pass': 1, 'proofbundle': 1, 'docket': 1, 'cost_risk_proxy': 1}]) == 'not_reported'

    measured_zero = compute_d_metric([
        {
            'success_score': 0,
            'validator_pass': 1,
            'replay_pass': 1,
            'proofbundle': 1,
            'docket': 1,
            'cost_risk_proxy': 1,
        }
    ])
    assert measured_zero == 0
