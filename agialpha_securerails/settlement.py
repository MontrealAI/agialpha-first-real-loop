import json,os
from .claim_boundary import CLAIM_BOUNDARY
def make_settlement(out_dir,vault):
 o={"schema_version":"1.0.0","settlement_id":"settlement-demo-001","vault_id":vault["vault_id"],"utility_asset":"$AGIALPHA","settlement_type":"utility-accounting-only","status":"recorded","alpha_work_units":100,"validator_fee":20,"replay_fee":10,"safety_review_fee":10,"human_review_fee":20,"unused_refund":40,"slashing_event":False,"evidence_docket_id":"evidence-docket-demo-001","proofbundle_id":"proofbundle-demo-001","human_review_status":"required","claim_boundary":CLAIM_BOUNDARY,"notice":"This settlement receipt records utility accounting for validated protocol work. It is not equity, debt, yield, dividend, ownership, profit right, guaranteed appreciation, or investment return."}
 json.dump(o,open(os.path.join(out_dir,'settlement-receipt.json'),'w'),indent=2);return o
