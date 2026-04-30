from pathlib import Path
import re

def linkcheck(site):
    site=Path(site)
    for f in site.rglob('*.html'):
        t=f.read_text()
        for m in re.findall(r"href=['\"]([^'\"]+)['\"]",t):
            if m.startswith('http') or m.startswith('#'): continue
            path=m
            if path.startswith('/agialpha-first-real-loop/'): path=path[len('/agialpha-first-real-loop/'): ]
            p=site / path.lstrip('/')
            if m.endswith('/'): p=p/'index.html'
            if not p.exists():
                raise ValueError(f'broken link {m} in {f}')
