import json
import tempfile
from pathlib import Path
from agialpha_enterprise_pilot.core import build, validate, replay, falsification_audit, build_data


def _run():
    td=Path(tempfile.mkdtemp())
    out=td/"run"
    build(Path('.'), out, Path('config/enterprise_pilot_use_cases.example.json'))
    return out

def test_validate_passes():
    out=_run(); validate(out)
