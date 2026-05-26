import json
import subprocess
import tempfile
from pathlib import Path


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
        assert all(e.get('autonomous_persistence_allowed') is False for e in imports)
