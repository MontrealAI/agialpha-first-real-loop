from pathlib import Path
from .canary_fixtures import list_fixtures
from .canary_runner import run_canary
from .canary_replay import replay
from .canary_report import build_report
from .canary_registry import update_registry, build_data
from .canary_render import render

def validate(input_dir: Path):
    required=['00_manifest.json','01_fixture_summary.json']
    missing=[f for f in required if not (input_dir/f).exists()]
    if missing: raise SystemExit(f"missing: {missing}")

def list_fixtures_cmd(fixtures: Path):
    for f in list_fixtures(fixtures): print(f)
