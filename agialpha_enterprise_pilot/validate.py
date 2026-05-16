import json
from pathlib import Path
def validate_run(run):
 required=['01_pilot_intake.json','02_regulated_boundary_triage.json','03_customer_use_attestation.json','04_enterprise_job_pack.json','05_validator_plan.json','06_proofbundle.json','08_work_vault.json','09_utility_settlement_receipt.json','10_customer_review_record.json','11_external_replay_packet.json','12_commercial_readiness_scorecard.json','14_valuation_support_link.json','15_missing_evidence.json']
 for f in required:
  if not (run/f).exists(): raise SystemExit(f'missing {f}')
 j=json.loads((run/'09_utility_settlement_receipt.json').read_text())
 if 'utility-only local accounting receipt' not in j.get('notice',''): raise SystemExit('bad notice')
