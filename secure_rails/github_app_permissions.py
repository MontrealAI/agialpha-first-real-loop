
import json
from pathlib import Path

DEFAULT_READ_ONLY = {
  "contents": "read", "metadata": "read", "pull_requests": "read", "actions": "read",
  "checks": "read", "issues": "none", "secrets": "none", "workflows": "none",
  "administration": "none", "deployments": "none", "statuses": "read"
}
OPTIONAL_MODES = {"pr_comment_mode", "issue_creation_mode", "check_run_mode"}


def validate_permission_matrix(data: dict) -> tuple[bool, list[str]]:
    errs = []
    perms = data.get('default_permissions', data)
    modes = set(data.get('optional_modes_enabled', []))
    if not modes.issubset(OPTIONAL_MODES):
        errs.append('unknown optional mode')
    forbidden = {
        'contents': {'write'}, 'workflows': {'write'}, 'administration': {'read', 'write'},
        'secrets': {'read', 'write'}, 'deployments': {'write'}
    }
    for k, bad in forbidden.items():
        if perms.get(k) in bad: errs.append(f'forbidden default permission: {k}={perms.get(k)}')
    if perms.get('pull_requests') == 'write' and 'pr_comment_mode' not in modes: errs.append('pull_requests write requires pr_comment_mode')
    if perms.get('issues') == 'write' and 'issue_creation_mode' not in modes: errs.append('issues write requires issue_creation_mode')
    if perms.get('checks') == 'write' and 'check_run_mode' not in modes: errs.append('checks write requires check_run_mode')
    return (len(errs) == 0, errs)


def validate_permissions_file(path: Path) -> tuple[bool, list[str]]:
    return validate_permission_matrix(json.loads(path.read_text(encoding='utf-8')))
