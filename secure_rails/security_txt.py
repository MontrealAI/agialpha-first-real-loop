from pathlib import Path

def validate_security_txt_template(path: Path) -> tuple[bool,list[str]]:
    txt=path.read_text(encoding='utf-8')
    req=['Contact:','Policy:','Preferred-Languages:','Canonical:','Expires:']
    errs=[f'missing {r}' for r in req if r not in txt]
    contact_lines = [line.split(':', 1)[1].strip() for line in txt.splitlines() if line.startswith('Contact:')]
    if not contact_lines:
        errs.append('missing Contact value')
    is_template = path.name.endswith('.template')
    for contact in contact_lines:
        if 'example.invalid' in contact and not is_template:
            errs.append('placeholder security contact is not valid for production routing')
    return (not errs, errs)
