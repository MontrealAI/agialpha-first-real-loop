import json
import tempfile
from pathlib import Path
from agialpha_enterprise_pilot.core import build, validate, replay, falsification_audit, build_data


def _run():
    td=Path(tempfile.mkdtemp())
    out=td/"run"
    build(Path('.'), out, Path('config/enterprise_pilot_use_cases.example.json'))
    return out

def test_generated_data_exists():
    out=_run()
    build_data(Path("enterprise_pilot_registry"), out/"gen")
    assert (out/"gen"/"summary.json").exists()
