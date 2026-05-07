from __future__ import annotations
from pathlib import Path
FORBIDDEN=['equity','debt','yield','dividend','ownership','profit right','passive income','guaranteed return','investment return','token appreciation','financial product','claim on revenue','claim on assets']

def check_token_boundary(repo_root: Path) -> bool:
    paths=list((repo_root/'docs'/'secure-rails').rglob('*.md'))+list((repo_root/'docs'/'secure-rails').rglob('*.json'))
    ok=True
    for p in paths:
        t=p.read_text(encoding='utf-8', errors='ignore').lower()
        if '$agialpha' in t:
            for f in FORBIDDEN:
                if f in t:
                    print(f'forbidden token/investment term {f} in {p}')
                    ok=False
    return ok
