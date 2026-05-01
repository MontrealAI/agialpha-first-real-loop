def issue_quality(result, expected):
    obs, exp = set(result.get("issues", [])), set(expected or [])
    tp, fp, fn = len(obs & exp), len(obs - exp), len(exp - obs)
    if not obs and not exp:
        f1 = 1.0
    else:
        f1 = (2 * tp) / max(1, 2 * tp + fp + fn)
    action = 1.0 if result.get("next_actions") else 0.0
    return round(0.85 * f1 + 0.15 * action, 4)

def evaluate_source(source, tasks):
    ns = {}
    exec(source, ns)
    rows = []
    for task in tasks:
        result = ns["evaluate"](task)
        rows.append({
            "experiment_slug": task.get("experiment_slug"),
            "quality": issue_quality(result, task.get("expected_issues", [])),
            "issues": result.get("issues", []),
            "expected_issues": task.get("expected_issues", []),
            "next_actions": result.get("next_actions", []),
            "safety_block": result.get("safety_block", False)
        })
    mean = round(sum(r["quality"] for r in rows) / max(1, len(rows)), 4)
    coverage = round(sum(1 for r in rows if r["quality"] >= .75) / max(1, len(rows)), 4)
    return {"mean_quality": mean, "coverage": coverage, "rows": rows}
