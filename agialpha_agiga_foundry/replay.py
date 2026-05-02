import json
from pathlib import Path
def replay_docket(d):
    s=json.loads((Path(d)/"22_summary_tables/scoreboard.json").read_text())
    solved=s.get("solved_niches",0)
    out={"replay_pass": solved > 0, "solved_niches": solved}
    (Path(d)/"13_replay_logs/replay_report.json").write_text(json.dumps(out,indent=2))
    return out
