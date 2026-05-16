import json
from pathlib import Path
INDEX=['registry.json','latest.json','pilots.json','pilot_intakes.json','regulated_boundary_triage.json','customer_attestations.json','job_packs.json','proofbundles.json','evidence_dockets.json','work_vaults.json','settlement_receipts.json','customer_reviews.json','external_replay_packets.json','commercial_readiness_scorecards.json','pilot_outcomes.json','valuation_support_links.json','missing_evidence.json']
def ensure_registry(base):
 base.mkdir(parents=True,exist_ok=True); (base/'runs').mkdir(exist_ok=True)
 for n in INDEX:
  p=base/n
  if not p.exists(): p.write_text('{}\n' if n=='latest.json' else '[]\n', encoding='utf-8')
 if not (base/'CHANGELOG.md').exists(): (base/'CHANGELOG.md').write_text('# Enterprise Pilot Registry\n', encoding='utf-8')
def append_json(path,row):
 data=json.loads(path.read_text()); data.append(row); path.write_text(json.dumps(data,indent=2)+'\n')
