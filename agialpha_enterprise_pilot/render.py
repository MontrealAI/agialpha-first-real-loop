from pathlib import Path
import json
def render_summary(run:Path)->str:
 s=json.loads((Path(run)/"12_commercial_readiness_scorecard.json").read_text())
 return f"# Enterprise Pilot Summary\n\nTier: {s.get('commercial_readiness_tier','not_reported')}\n"
