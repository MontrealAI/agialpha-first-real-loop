from .context import *
def render_scoreboard(run: Path, payload):
 rpt=run/"12_reports"; rpt.mkdir(parents=True,exist_ok=True); write_json(rpt/"scoreboard.json",payload); (rpt/"scoreboard.md").write_text("# Scoreboard\n\n"+json.dumps(payload,indent=2)+"\n",encoding="utf-8")
