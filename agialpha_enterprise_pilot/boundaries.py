from __future__ import annotations
BOUNDARY_CLAIM="No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not."
TOKEN_BOUNDARY="$AGIALPHA is utility-only accounting; not equity, debt, yield, ROI, or token value evidence."
REG_BOUNDARY="Not legal, medical, HR, credit, insurance, investment, payment, custody, KYC/AML, or regulated decisioning."
CUSTOMER_DATA_BOUNDARY="Synthetic or customer-approved redacted inputs only; no raw PII or secrets."
def boundary_fields():
    return {"claim_boundary":BOUNDARY_CLAIM,"token_boundary":TOKEN_BOUNDARY,"regulated_boundary":REG_BOUNDARY,"customer_data_boundary":CUSTOMER_DATA_BOUNDARY,"human_review_required":True,"autonomous_persistence_allowed":False,"no_auto_merge":True,"not_an_investment_claim":True}
