from pathlib import Path

def validate_security_txt_template(path: Path) -> tuple[bool,list[str]]:
    txt=path.read_text(encoding='utf-8')
    lines = txt.splitlines()
    fields = {}
    for line in lines:
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        fields.setdefault(key.strip().lower(), []).append(value.strip())
    req=['contact','policy','preferred-languages','canonical','expires']
    errs=[f'missing {r}:' for r in req if r not in fields]
    contact_lines = fields.get('contact', [])
    if not contact_lines:
        errs.append('missing Contact value')
    is_template = path.name.endswith('.template')
    for contact in contact_lines:
        if 'example.invalid' in contact and not is_template:
            errs.append('placeholder security contact is not valid for production routing')
    return (not errs, errs)
