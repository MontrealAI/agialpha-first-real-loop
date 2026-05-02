import json
from pathlib import Path
def audit(d):
    s=json.loads((Path(d)/"22_summary_tables/scoreboard.json").read_text())
    p=[]
    if "B6_advantage_delta_vs_B5" not in s: p.append("missing baseline delta")
    out={"pass":len(p)==0,"problems":p}
    (Path(d)/"14_falsification_audit/falsification_report.json").write_text(json.dumps(out,indent=2))
    return out
