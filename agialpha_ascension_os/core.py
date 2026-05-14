import hashlib, json
from pathlib import Path
BOUNDARY_CLAIM="local bounded public evidence"
BOUNDARY_TOKEN="utility-only $AGIALPHA settlement record"
BOUNDARY_REGULATED="regulated-boundary-safe documentation-only automation"
DISCLAIMER_OPS="This is a directional operational usefulness proxy, not a financial projection, ROI claim, investment claim, token-value claim, legal conclusion, or guaranteed economic result."

def bfields():
    return {
        "claim_boundary": BOUNDARY_CLAIM,
        "token_boundary": BOUNDARY_TOKEN,
        "regulated_boundary": BOUNDARY_REGULATED,
        "human_review_required": True,
        "autonomous_persistence_allowed": False,
        "no_auto_merge": True,
    }

def sid(*parts):
    h=hashlib.sha256("|".join(parts).encode()).hexdigest()[:12]
    return h

def write_json(path,data):
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    tmp=p.with_suffix(p.suffix+".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True)+"\n")
    tmp.replace(p)
