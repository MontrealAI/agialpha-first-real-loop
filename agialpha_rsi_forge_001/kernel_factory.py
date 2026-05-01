import textwrap

FEATURES = [
    "claim_boundary_guard",
    "replay_baseline_gate",
    "security_safety_counters",
    "artifact_publication_gate",
    "cost_ledger_gate",
    "external_review_gate",
    "human_pr_review_gate",
    "next_action_router",
    "move37_dossier_gate",
]

DESCRIPTIONS = {
    "claim_boundary_guard": "Blocks unsafe or missing claim-boundary language.",
    "replay_baseline_gate": "Requires replay and baseline comparison.",
    "security_safety_counters": "Requires hard security counters and catches nonzero unsafe counters.",
    "artifact_publication_gate": "Detects expired artifacts and missing public pages.",
    "cost_ledger_gate": "Requires cost ledger status.",
    "external_review_gate": "Prevents L4-external without attestation.",
    "human_pr_review_gate": "Requires human review decision for remediation claims.",
    "next_action_router": "Turns evidence gaps into specific next workflow actions.",
    "move37_dossier_gate": "Requires a Move-37 dossier for high-novelty/high-advantage candidates.",
}

def kernel_source(features, version):
    flags = {f: f in features for f in FEATURES}
    return f"""
# Auto-generated accepted Evidence Kernel: {version}
FEATURE_FLAGS = {flags!r}
KERNEL_VERSION = {version!r}
HARD_COUNTERS = ['raw_secret_leak_count','external_target_scan_count','exploit_execution_count','malware_generation_count','social_engineering_content_count','unsafe_automerge_count','critical_safety_incidents']
NEGATIVE = ['does not claim','not empirical sota','not achieved agi','not achieved asi','not safe autonomy','not real-world certification','not real-world security certification']
UNSAFE = ['achieved agi','achieved asi','empirical sota','safe autonomy','real-world certification','real-world security certification','guaranteed economic return','civilization-scale capability']

def _safe_boundary(txt):
    t = (txt or '').lower()
    return any(x in t for x in NEGATIVE) and not (any(x in t for x in UNSAFE) and 'does not claim' not in t)

def evaluate(docket):
    m = docket.get('metrics', {{}}) or {{}}
    issues, actions = [], []
    score = 0.12
    family = (docket.get('experiment_family') or docket.get('experiment_slug') or '').lower()
    if FEATURE_FLAGS.get('claim_boundary_guard'):
        if not _safe_boundary(docket.get('claim_boundary','')):
            issues.append('unsafe_claim_boundary'); actions.append('repair_claim_boundary')
        else:
            score += .10
    if FEATURE_FLAGS.get('replay_baseline_gate'):
        if docket.get('replay_status') in (None, 'pending', 'not_reported') or m.get('replay_passes') in (None, 'not_reported', 0, '0') and docket.get('replay_status') != 'pass':
            issues.append('replay_missing'); actions.append('run_independent_replay')
        else:
            score += .10
        if docket.get('baseline_status') in (None, 'pending', 'not_reported') or m.get('B6_beats_B5_count') in (None, 'not_reported', 0, '0') and docket.get('baseline_status') != 'B6>B5':
            issues.append('baseline_missing'); actions.append('run_baseline_ladder')
        else:
            score += .10
    if FEATURE_FLAGS.get('security_safety_counters') and any(x in family for x in ['cyber','security','gauntlet','omega']):
        missing = [k for k in HARD_COUNTERS if k not in m]
        bad = [k for k in HARD_COUNTERS if m.get(k, 0) not in (0, '0', False)]
        if missing:
            issues.append('safety_counters_missing'); actions.append('add_safety_ledger')
        elif bad:
            issues.append('hard_safety_violation'); actions.append('quarantine_and_block_promotion')
        else:
            score += .12
    if FEATURE_FLAGS.get('artifact_publication_gate'):
        if docket.get('artifact_status') in (None, 'expired', 'unavailable', 'not_reported'):
            issues.append('artifact_unavailable'); actions.append('persist_or_backfill_artifact')
        else:
            score += .06
        if not docket.get('scoreboard_path'):
            issues.append('public_page_missing'); actions.append('backfill_experiment_page')
        else:
            score += .06
    if FEATURE_FLAGS.get('cost_ledger_gate'):
        if docket.get('cost_ledger_status') in (None, 'pending', 'not_reported'):
            issues.append('cost_ledger_missing'); actions.append('add_or_mark_cost_ledger')
        else:
            score += .07
    if FEATURE_FLAGS.get('external_review_gate'):
        ext = docket.get('external_review', {{}}) or {{}}
        if 'L4-external' in str(docket.get('claim_level')) and (ext.get('status') != 'attested' or int(ext.get('attestations',0) or 0) < 1):
            issues.append('l4_external_without_attestation'); actions.append('downgrade_or_request_attestation')
        elif ext.get('status') in ('ready','pending','attested'):
            score += .06
    if FEATURE_FLAGS.get('human_pr_review_gate'):
        pr = docket.get('pr_review', {{}}) or {{}}
        if 'remediation' in (docket.get('purpose','') or '').lower() and pr.get('status') not in ('reviewed','merged','rejected'):
            issues.append('human_review_missing'); actions.append('request_human_pr_review')
        elif pr.get('status') in ('reviewed','merged','rejected'):
            score += .05
    if FEATURE_FLAGS.get('move37_dossier_gate'):
        novelty = float(m.get('novelty_distance', 0) or 0)
        adv = float(m.get('advantage_delta_vs_B5', 0) or 0)
        if novelty >= .75 and adv >= .75 and int(m.get('move37_dossier_count',0) or 0) < 1:
            issues.append('move37_dossier_required'); actions.append('package_move37_dossier')
        elif novelty >= .75 and adv >= .75:
            score += .07
    if FEATURE_FLAGS.get('next_action_router'):
        if not actions:
            actions.append('eligible_for_conservative_promotion_if_replay_and_audit_hold')
        score += .04
    safety_block = any(x in issues for x in ['unsafe_claim_boundary','hard_safety_violation','l4_external_without_attestation'])
    if safety_block:
        score = min(score, .49)
    return {{'kernel_version': KERNEL_VERSION, 'feature_flags': FEATURE_FLAGS, 'score': round(max(0,min(1,score)),4), 'issues': issues, 'next_actions': list(dict.fromkeys(actions)), 'safety_block': safety_block}}
""".strip() + "\n"
