from pathlib import Path
import re
REQ=["01_pilot_intake.json","02_regulated_boundary_triage.json","03_customer_use_attestation.json","04_enterprise_job_pack.json","05_validator_plan.json","06_proofbundle.json","07_evidence_docket.json","08_work_vault.json","09_utility_settlement_receipt.json","10_customer_review_record.json","11_external_replay_packet.json","12_commercial_readiness_scorecard.json","14_valuation_support_link.json","15_missing_evidence.json"]
FORB=[r"buy / sell / hold",r"token appreciation"]
def validate_run(run:Path):
 run=Path(run)
 m=[f for f in REQ if not (run/f).exists()]
 if m: raise SystemExit("missing artifacts: "+", ".join(m))
 txt="\n".join(p.read_text(encoding="utf-8").lower() for p in run.iterdir() if p.suffix in {".json",".md"})
 for pat in FORB:
  if re.search(pat,txt): raise SystemExit(f"forbidden language: {pat}")
