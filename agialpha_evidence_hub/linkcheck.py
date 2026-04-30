from pathlib import Path

def linkcheck(site):
    if not (Path(site)/'index.html').exists(): raise ValueError('missing index')
