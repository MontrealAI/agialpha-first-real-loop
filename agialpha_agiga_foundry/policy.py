import json
from pathlib import Path
CLAIM_BOUNDARY = "No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not."
def load_policy(repo_root):
    return json.loads((Path(repo_root)/"config/agiga_foundry_policy.json").read_text())
