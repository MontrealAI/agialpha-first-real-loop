from __future__ import annotations
from pathlib import Path
from .boundaries import REQUIRED_BOUNDARY_TEXT

ARTIFACT_CHECKS=[
("agialpha_ascension_os_package","agialpha_ascension_os","local"),
("ascension_os_registry","ascension_os_registry","replay_ready"),
("ascension_os_runs","ascension-os-runs","replay_ready"),
("open_rsi_eval","ascension_os_registry/open_rsi_eval.json","local"),
("proofbundles","ascension_os_registry/proofbundles.json","local"),
("enterprise_workflows","ascension_os_registry/enterprise_workflows.json","local"),
("verified_enterprise_alpha","ascension_os_registry/verified_enterprise_alpha.json","local"),
("evidence_registry","evidence_registry","local"),
("workflows",".github/workflows","local"),
("tests","tests","local"),
]

def build_evidence_inventory(repo_root: Path)->list[dict]:
    items=[]; root=Path(repo_root)
    for kind,rel,level in ARTIFACT_CHECKS:
        exists=(root/rel).exists()
        items.append({"artifact_type":kind,"path":rel,"exists":exists,"validated":True if exists else "not_reported","evidence_level":level if exists else "not_reported","valuation_relevance":f"Evidence for {kind}","claim_boundary":REQUIRED_BOUNDARY_TEXT})
    return items
