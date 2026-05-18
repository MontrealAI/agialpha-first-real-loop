from __future__ import annotations
import json
from pathlib import Path

BOUNDARIES={
  "claim_boundary":"local bounded public evidence; proof-gated recursive experiment engine; human-reviewed promotion required",
  "token_boundary":"$AGIALPHA utility-only accounting; no wallet/custody/payment/KYC/AML/trading",
  "regulated_boundary":"regulated-domain firewall enabled; blocked_human_review_required for regulated tasks",
  "human_review_required":True,
  "no_auto_merge":True,
  "autonomous_persistence_allowed":False,
}

def atomic_write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write('\n')
    tmp.replace(path)
