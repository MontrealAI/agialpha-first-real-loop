import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _env_with_repo(repo: Path):
    env = dict(os.environ)
    env['PYTHONPATH'] = str(repo) + (':' + env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
    return env


def _run_build(repo_root: Path, out_dir: Path, registry_name: str):
    subprocess.check_call([
        sys.executable, '-m', 'agialpha_enterprise_pilot', 'build',
        '--repo-root', str(repo_root), '--out', str(out_dir),
        '--workflow-family', 'software_quality_pack', '--customer-mode', 'synthetic_only',
        '--registry', registry_name,
    ], env=_env_with_repo(repo_root))


def test_repeated_builds_get_unique_registry_run_ids():
    repo = Path('.').resolve()
    out = Path(tempfile.mkdtemp())
    registry_name = f"_tmp_enterprise_pilot_registry_{next(tempfile._get_candidate_names())}"
    try:
        _run_build(repo, out, registry_name)
        _run_build(repo, out, registry_name)
        runs_dir = repo / registry_name / 'runs'
        run_ids = sorted([p.name for p in runs_dir.iterdir() if p.is_dir() and p.name.startswith('enterprise-pilot-')])
        assert len(run_ids) >= 2
        assert run_ids[-1] != run_ids[-2]
    finally:
        shutil.rmtree(repo / registry_name, ignore_errors=True)


def test_registry_written_under_repo_root_not_cwd():
    repo = Path('.').resolve()
    out = Path(tempfile.mkdtemp())
    external_cwd = Path(tempfile.mkdtemp())
    registry_name = f"_tmp_enterprise_pilot_registry_{next(tempfile._get_candidate_names())}"
    try:
        subprocess.check_call([
            sys.executable, '-m', 'agialpha_enterprise_pilot', 'build',
            '--repo-root', str(repo), '--out', str(out),
            '--workflow-family', 'software_quality_pack', '--customer-mode', 'synthetic_only',
            '--registry', registry_name,
        ], cwd=external_cwd, env=_env_with_repo(repo))
        assert (repo / registry_name / 'latest.json').exists()
        assert not (external_cwd / registry_name / 'latest.json').exists()
    finally:
        shutil.rmtree(repo / registry_name, ignore_errors=True)
