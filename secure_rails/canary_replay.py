import json
from pathlib import Path

def replay(input_dir: Path, out_file: Path):
    fx=json.loads((input_dir/'01_fixture_summary.json').read_text())
    rep={"schema_version":"securerails.e2e_canary_replay.v1","fixture_count":len(fx),"replay_pass":all(f['status']=='pass' for f in fx)}
    out_file.write_text(json.dumps(rep,indent=2))
    return rep
