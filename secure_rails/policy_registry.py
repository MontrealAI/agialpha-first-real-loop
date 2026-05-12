import json
from pathlib import Path

def write_decision_log(decisions_dir, registry_dir):
    r = Path(registry_dir); r.mkdir(parents=True, exist_ok=True)
    dpaths = sorted(Path(decisions_dir).glob("*.json"))
    decisions = [json.loads(p.read_text()) for p in dpaths]
    (r / "registry.json").write_text(json.dumps({"decisions": decisions}, indent=2))
    latest = decisions[-1] if decisions else {}
    (r / "latest.json").write_text(json.dumps(latest, indent=2))
    by_decision = {}
    by_severity = {}
    by_domain = {}
    for d in decisions:
        by_decision[d["decision"]] = by_decision.get(d["decision"],0)+1
        by_severity[d["severity"]] = by_severity.get(d["severity"],0)+1
        by_domain[d["context_type"]] = by_domain.get(d["context_type"],0)+1
    idx = r / "indexes"; idx.mkdir(exist_ok=True)
    (idx/"by_decision.json").write_text(json.dumps(by_decision, indent=2))
    (idx/"by_severity.json").write_text(json.dumps(by_severity, indent=2))
    (idx/"by_domain.json").write_text(json.dumps(by_domain, indent=2))
