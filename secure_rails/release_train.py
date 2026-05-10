
from pathlib import Path
import subprocess
from .release_manifest import build_manifest
from .release_bundle import build_bundle
from .release_validate import validate_bundle
from .marketplace_readiness import write_reports
from .release_render import render_notes_file

def git(cmd, repo_root: Path):
  try:
    return subprocess.check_output(cmd, text=True, cwd=str(repo_root), stderr=subprocess.DEVNULL).strip()
  except Exception:
    return "unknown"

def infer_repository(repo_root: Path) -> str:
  remote = git(['git', 'remote', 'get-url', 'origin'], repo_root)
  if remote != 'unknown':
    trimmed = remote.strip().removesuffix('.git')
    if trimmed.startswith('git@github.com:'):
      return trimmed.split(':', 1)[1]
    if 'github.com/' in trimmed:
      return trimmed.split('github.com/', 1)[1]
  return f"unknown/{repo_root.resolve().name}"

def build(repo_root:Path, release_version:str, release_channel:str, out:Path):
  manifest=build_manifest(
    release_version,
    release_channel,
    infer_repository(repo_root),
    git(['git','rev-parse','HEAD'], repo_root),
    git(['git','rev-parse','--abbrev-ref','HEAD'], repo_root),
    ["release_train_001"],
    [],
  )
  build_bundle(repo_root,out,manifest)

def validate(inp:Path): validate_bundle(inp)

def marketplace(repo_root:Path,out:Path): write_reports(repo_root,out,out.with_suffix('.json'))

def render_notes(inp:Path,out:Path): render_notes_file(inp,out)
