import json
from pathlib import Path

RULE_FILES = [
    "securerails_policy_rules_claims.json",
    "securerails_policy_rules_safety.json",
    "securerails_policy_rules_eu_ai_act.json",
    "securerails_policy_rules_token_utility.json",
    "securerails_policy_rules_work_vault.json",
    "securerails_policy_rules_mark_allocation.json",
    "securerails_policy_rules_sovereign.json",
    "securerails_policy_rules_github_app.json",
    "securerails_policy_rules_release.json",
    "securerails_policy_rules_trust_center.json",
    "securerails_policy_rules_repo_security.json",
]

def load_rules(config_dir: str | None = None):
    if config_dir is None:
        base = Path(__file__).resolve().parent.parent / "config"
    else:
        base = Path(config_dir)
    rules = []
    for name in RULE_FILES:
        p = base / name
        if p.exists():
            rules.extend(json.loads(p.read_text()).get("rules", []))
    return rules
