import hashlib,re

def scan_text(path,text):
    findings=[]
    for i,l in enumerate(text.splitlines(),1):
        if re.search(r'(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|secret\s*=)',l,re.I):
            h=hashlib.sha256(('securerails-salt'+l).encode()).hexdigest()[:16]
            findings.append({'file':path,'line':i,'finding_type':'secret_like','salted_hash':h,'redacted_preview':'[REDACTED]','claim_boundary':'SecureRails is AI-agent security governance and proof-bound defensive remediation.'})
    return findings
