from .context import *


def init_registry(reg: Path):
    reg.mkdir(parents=True, exist_ok=True)
    files = [
        "registry.json",
        "latest.json",
        "runs.json",
        "candidates.json",
        "heldout_tasks.json",
        "evaluations.json",
        "promotion_queue.json",
        "rejected_candidates.json",
    ]
    for f in files:
        write_json(reg / f, {"claim_boundary": CLAIM_BOUNDARY, "items": []})
    for i in ["by_run", "by_candidate", "by_status", "by_decision"]:
        write_json(reg / f"indexes/{i}.json", {"claim_boundary": CLAIM_BOUNDARY, "index": {}})
    (reg / "CHANGELOG.md").write_text("# Recursive Gauntlet Registry Changelog\n", encoding="utf-8")
