BOUNDARY='SecureRails is AI-agent security governance and proof-bound defensive remediation. It is not autonomous cybersecurity certification, not offensive cyber, not a high-risk decision system by intended purpose, not a GPAI model provider by default, and not an investment product.'
DOCTRINE='No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.'

def review_claims(texts):
    violations=[]
    bad=['guaranteed security','certified secure','investment return','dividends','yield']
    for p,t in texts.items():
        low=t.lower()
        for b in bad:
            if b in low: violations.append({'file':p,'term':b})
    return {'violations':violations,'claim_boundary':BOUNDARY,'doctrine':DOCTRINE}
