import os
import subprocess
import sys
import tempfile
from pathlib import Path


def _env_with_repo(repo: Path):
    env = dict(os.environ)
    env['PYTHONPATH'] = str(repo) + (':' + env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
    return env


def _run_build(repo_root: Path, out_dir: Path):
    subprocess.check_call([
        sys.executable, '-m', 'agialpha_enterprise_pilot', 'build',
        '--repo-root', str(repo_root), '--out', str(out_dir),
        '--workflow-family', 'software_quality_pack', '--customer-mode', 'synthetic_only',
        '--registry', 'enterprise_pilot_registry',
    ], env=_env_with_repo(repo_root))


def test_repeated_builds_get_unique_registry_run_ids():
    repo = Path('.').resolve()
    out = Path(tempfile.mkdtemp())
    _run_build(repo, out)
    _run_build(repo, out)
    runs_dir = repo / 'enterprise_pilot_registry' / 'runs'
    run_ids = sorted([p.name for p in runs_dir.iterdir() if p.is_dir() and p.name.startswith('enterprise-pilot-')])
    assert len(run_ids) >= 2
    assert run_ids[-1] != run_ids[-2]


def test_registry_written_under_repo_root_not_cwd():
    repo = Path('.').resolve()
    out = Path(tempfile.mkdtemp())
    external_cwd = Path(tempfile.mkdtemp())
    subprocess.check_call([
        sys.executable, '-m', 'agialpha_enterprise_pilot', 'build',
        '--repo-root', str(repo), '--out', str(out),
        '--workflow-family', 'software_quality_pack', '--customer-mode', 'synthetic_only',
        '--registry', 'enterprise_pilot_registry',
    ], cwd=external_cwd, env=_env_with_repo(repo))
    assert (repo / 'enterprise_pilot_registry' / 'latest.json').exists()
    assert not (external_cwd / 'enterprise_pilot_registry' / 'latest.json').exists()
