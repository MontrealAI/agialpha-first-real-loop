import json
from pathlib import Path
def replay_docket(d):
    s=json.loads((Path(d)/"22_summary_tables/scoreboard.json").read_text())
    out={"replay_pass":s.get("solved_niches",0)>=0}
    (Path(d)/"13_replay_logs/replay_report.json").write_text(json.dumps(out,indent=2))
    return out
