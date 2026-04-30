from pathlib import Path

def linkcheck(site):
    s=Path(site)
    required=['index.html','404.html','experiments/index.html','runs/index.html','legacy/index.html']
    for f in required:
        if not (s/f).exists(): raise ValueError(f'missing {f}')
