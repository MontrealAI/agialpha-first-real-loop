from pathlib import Path

def validate_security_txt_template(path: Path) -> tuple[bool,list[str]]:
    txt=path.read_text(encoding='utf-8')
    req=['Contact:','Policy:','Preferred-Languages:','Canonical:','Expires:']
    errs=[f'missing {r}' for r in req if r not in txt]
    if 'production_contact_configured": true' in txt and 'example.invalid' in txt:
        errs.append('invalid production contact')
    return (not errs, errs)
