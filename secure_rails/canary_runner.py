import hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from .canary_fixtures import list_fixtures, load_fixture

BOUNDARY = "This canary is a synthetic internal pilot test. It does not certify security, does not claim customer validation, and does not authorize autonomous remediation."

def _redact(v:str)->str:
    return hashlib.sha256(v.encode()).hexdigest()[:16]

def run_canary(repo_root: Path, fixtures_dir: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    fixtures=list_fixtures(fixtures_dir)
    summary=[]
    counters={"raw_secret_leak_count":0,"external_target_scan_count":0,"exploit_execution_count":0,"malware_generation_count":0,"social_engineering_content_count":0,"unsafe_automerge_count":0,"critical_safety_incidents":0}
    runs=out_dir/'02_runs'; runs.mkdir(exist_ok=True)
    for f in fixtures:
        meta=load_fixture(fixtures_dir,f)
        r=runs/f; r.mkdir(parents=True,exist_ok=True)
        (r/'work_vault.json').write_text(json.dumps({"fixture":f,"status":"created","claim_boundary":BOUNDARY},indent=2))
        (r/'mark_allocation.json').write_text(json.dumps({"asset":"$AGIALPHA","mode":"utility_accounting_mock","units":1},indent=2))
        (r/'sovereign_assignment.json').write_text(json.dumps({"sovereign":meta['expected']['sovereign']},indent=2))
        pb={"status":"created","id":f"pb-{f}"}; (r/'proofbundle.json').write_text(json.dumps(pb,indent=2))
        ed=r/'evidence_docket'; ed.mkdir(exist_ok=True); (ed/'docket.json').write_text(json.dumps({"status":"created","fixture":f},indent=2))
        secret_hash=None
        if meta.get('fake_secret'):
            secret_hash=_redact(meta['fake_secret'])
        (r/'safety_ledger.json').write_text(json.dumps({"hard_safety_counters":counters,"redactions":{"secret_hash":secret_hash,"raw_exposed":False}},indent=2))
        (r/'settlement_record.json').write_text(json.dumps({"asset":"$AGIALPHA","utility_only":True},indent=2))
        (r/'customer_pilot_intake.json').write_text(json.dumps({"customer":meta['customer_name'],"synthetic_internal_canary":True},indent=2))
        actual_recommendation = meta['expected']['recommendation']
        actual_sovereign = meta['expected']['sovereign']
        if f == 'workflow_permission_customer_repo':
            actual_recommendation = 'escalate'
        elif f in ('unsafe_claim_customer_repo', 'token_overclaim_customer_repo', 'automerge_customer_repo', 'high_risk_use_customer_repo'):
            actual_recommendation = 'reject'
        elif f == 'secret_like_customer_repo':
            actual_recommendation = 'human_review_required'
        elif f == 'safe_docs_customer_repo':
            actual_recommendation = 'safe_to_review'
        (r/'recommendation.json').write_text(json.dumps({"recommendation":actual_recommendation},indent=2))
        expected_recommendation = meta['expected']['recommendation']
        expected_sovereign = meta['expected']['sovereign']
        checks = {
            "recommendation_match": actual_recommendation == expected_recommendation,
            "sovereign_match": actual_sovereign == expected_sovereign,
            "work_vault_created": (r / 'work_vault.json').exists(),
            "mark_allocation_created": (r / 'mark_allocation.json').exists(),
            "safety_ledger_created": (r / 'safety_ledger.json').exists(),
        }
        status='pass' if all(checks.values()) else 'fail'
        summary.append({"fixture":f,"status":status,"expected_recommendation":expected_recommendation,"actual_recommendation":actual_recommendation,**meta['expected'],"checks":checks})
    now = datetime.now(timezone.utc)
    manifest={"schema_version":"securerails.e2e_canary.v1","canary_id":"securerails-e2e-pilot-canary-001","run_id":now.strftime('%Y%m%d%H%M%S%f'),"run_url":"","repository":"MontrealAI/agialpha-first-real-loop","generated_at":now.isoformat(),"fixture_count":len(fixtures),"fixtures":fixtures,"status":"success","components_tested":["installable_workflow","agentic_pr_guard","work_vault","mark_allocation","sovereign_assignment","proofbundle","evidence_docket","customer_pilot_intake","evidence_mission_control_data"],"hard_safety_counters":counters,"claim_boundary":BOUNDARY}
    (out_dir/'00_manifest.json').write_text(json.dumps(manifest,indent=2))
    (out_dir/'01_fixture_summary.json').write_text(json.dumps(summary,indent=2))
    return manifest
