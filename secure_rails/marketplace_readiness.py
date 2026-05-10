from pathlib import Path
import json

def assess(repo_root: Path) -> dict:
    root_action = (repo_root / 'action.yml').exists()
    workflows = any((repo_root / '.github/workflows').glob('*.yml'))
    return {
        'schema_version': 'securerails.marketplace_readiness.v1',
        'monorepo_action_ready': 'partial' if workflows else 'pass',
        'reusable_workflow_ready': 'pass' if (repo_root / '.github/workflows/securerails-pr-guard-reusable.yml').exists() else 'partial',
        'marketplace_dedicated_repo_needed': True,
        'root_action_yml_present': root_action,
        'workflow_files_present': workflows,
        'public_repo_required': True,
        'marketplace_publication_allowed_now': False,
        'recommended_next_step': 'export to dedicated action repository'
    }

def write_reports(repo_root: Path, out_md: Path, out_json: Path):
    d = assess(repo_root)
    out_json.write_text(json.dumps(d, indent=2), encoding='utf-8')
    out_md.write_text('# Marketplace-ready export plan\n\nThis repository is a monorepo with workflow files and is **not** directly Marketplace listed. Use reusable workflows here, and export to a dedicated action repository for Marketplace publication.\n', encoding='utf-8')
