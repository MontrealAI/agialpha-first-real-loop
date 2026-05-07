import json
from pathlib import Path

def render_summary(inp,out):
    i=Path(inp)
    m=json.loads((i/'00_manifest.json').read_text())
    Path(out).write_text(f"# SecureRails Agentic PR Guard 001\n\nRecommendation: **{m['decision']['recommendation']}**\n\nHuman review required: **{m['human_review_required']}**\n\n{m['claim_boundary']}\n")
