import json
import subprocess
import tempfile
from pathlib import Path


def test_each_job_produces_reusable_learning_bucket():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / 'run'
        reg = Path(td) / 'reg'
        subprocess.check_call([
            'python','-m','agialpha_engine','network-compounding-run',
            '--repo-root','.','--registry',str(reg),'--out',str(run),
            '--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'
        ])
        accepted = json.loads((run / '03_skill_extraction/accepted_skill_packages.json').read_text())['accepted_skill_packages']
        rejected = json.loads((run / '03_skill_extraction/rejected_skill_candidates.json').read_text())['rejected_skill_candidates']
        failures = json.loads((run / '03_skill_extraction/failure_learning_packages.json').read_text())['failure_learning_packages']
        raw = json.loads((run / '02_jobs/raw_task_results.json').read_text())['raw_task_results']
        produced = {p['source_job_id'] for p in accepted + rejected + failures}
        expected = {r['task_id'] for r in raw}
        assert expected <= produced
        assert failures or rejected or accepted


def test_failure_learning_package_has_boundary_fields_and_raw_ids():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / 'run'
        reg = Path(td) / 'reg'
        subprocess.check_call([
            'python','-m','agialpha_engine','network-compounding-run',
            '--repo-root','.','--registry',str(reg),'--out',str(run),
            '--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'
        ])
        failures = json.loads((run / '03_skill_extraction/failure_learning_packages.json').read_text())['failure_learning_packages']
        if failures:
            row = failures[0]
            assert row['raw_task_result_ids']
            assert row['claim_boundary']
            assert row['token_boundary']
            assert row['regulated_boundary']


def test_failure_learning_helper_emits_required_schema_fields():
    from agialpha_engine.failure_learning import build_failure_learning

    row = build_failure_learning('job-helper', 'tighten replay validator', raw_task_result_ids=['raw-job-helper'])
    assert row['failure_type']
    assert row['reusable_warning']
    assert row['recommended_future_validator']
    assert row['quarantine_required'] is True
    assert row['raw_task_result_ids'] == ['raw-job-helper']
