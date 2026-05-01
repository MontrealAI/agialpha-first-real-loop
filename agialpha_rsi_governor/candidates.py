import copy


def _bump(value, delta=0.02, cap=0.3):
    return min(cap, round(float(value) + delta, 4))


def generate_candidates(kernel, n):
    out = []
    for i in range(1, n + 1):
        c = copy.deepcopy(kernel)
        c["candidate_id"] = f"candidate-{i:03d}"
        c["kernel_version"] = f"0.1.{i}"
        c["rollback_note"] = "restore baseline"
        c["claim_boundary_impact"] = "none"
        c["safety_impact"] = "none"

        if i % 2 == 1:
            c["mutation_rationale"] = "raise page completeness emphasis"
            c["changed_fields"] = ["scoring_weights.page_completeness"]
            c["scoring_weights"]["page_completeness"] = _bump(
                kernel["scoring_weights"].get("page_completeness", 0.18)
            )
            c["expected_benefit"] = "improved completeness"
            c["expected_risk"] = "false positives"
        else:
            c["mutation_rationale"] = "raise replay readiness emphasis"
            c["changed_fields"] = ["scoring_weights.replayability"]
            c["scoring_weights"]["replayability"] = _bump(
                kernel["scoring_weights"].get("replayability", 0.14), delta=0.04
            )
            c["expected_benefit"] = "improved replay recommendation quality"
            c["expected_risk"] = "reduced sensitivity to shallow pages"
        out.append(c)
    return out
