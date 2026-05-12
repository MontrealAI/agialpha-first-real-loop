import json
from pathlib import Path

def build_data(registry, out):
    r=Path(registry); o=Path(out); o.mkdir(parents=True, exist_ok=True)
    decisions=json.loads((r/"registry.json").read_text()).get("decisions", []) if (r/"registry.json").exists() else []
    latest=decisions[-1] if decisions else {}
    summary={"total":len(decisions),"allow":0,"warn":0,"escalate":0,"reject":0,"quarantine":0,"human_review_required":len(decisions)}
    by_domain={}
    for d in decisions:
        summary[d["decision"]]=summary.get(d["decision"],0)+1
        by_domain[d["context_type"]]=by_domain.get(d["context_type"],0)+1
    (o/"latest.json").write_text(json.dumps(latest, indent=2))
    (o/"decisions.json").write_text(json.dumps(decisions, indent=2))
    (o/"summary.json").write_text(json.dumps(summary, indent=2))
    (o/"by_domain.json").write_text(json.dumps(by_domain, indent=2))
