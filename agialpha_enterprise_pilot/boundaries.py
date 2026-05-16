CLAIM_BOUNDARY='No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.'
TOKEN_BOUNDARY='$AGIALPHA is utility-only accounting only.'
REGULATED_BOUNDARY='No regulated decisioning; block legal/medical/hr/credit/insurance/kyc/aml/banking/brokerage/custody/payment.'
EXCLUDED_USES=['HR / worker evaluation','profiling of individuals','automated decisions about natural persons','credit / lending','insurance','medical use','legal advice','financial or investment advice','KYC/AML','banking / brokerage / custody','critical infrastructure control','energy or utility market participation','offensive cyber','cybersecurity certification','autonomous procurement','binding contract execution']
def envelope():
 return {'claim_boundary':CLAIM_BOUNDARY,'token_boundary':TOKEN_BOUNDARY,'regulated_boundary':REGULATED_BOUNDARY,'customer_data_boundary':'synthetic_or_customer_approved_redacted_only','human_review_required':True,'autonomous_persistence_allowed':False,'no_auto_merge':True,'not_an_investment_claim':True}
