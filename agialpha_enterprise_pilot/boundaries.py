CLAIM_BOUNDARY = "No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not."
TOKEN_BOUNDARY = "$AGIALPHA is utility-only accounting and not investment, securities, or token-value evidence."
REGULATED_BOUNDARY = "Not legal, medical, HR, credit, insurance, KYC/AML, banking, brokerage, custody, payment, or regulated decisioning."
CUSTOMER_DATA_BOUNDARY = "synthetic_only or customer_approved_redacted only; no raw PII."
def boundary_fields():
    return {"claim_boundary": CLAIM_BOUNDARY, "token_boundary": TOKEN_BOUNDARY, "regulated_boundary": REGULATED_BOUNDARY, "customer_data_boundary": CUSTOMER_DATA_BOUNDARY, "human_review_required": True, "autonomous_persistence_allowed": False, "no_auto_merge": True, "not_an_investment_claim": True}
