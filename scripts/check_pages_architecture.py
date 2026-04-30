from pathlib import Path
w=Path('.github/workflows')
hits=[]
for p in w.glob('*.yml'):
    if 'actions/deploy-pages' in p.read_text(): hits.append(p.name)
if hits!=['evidence-hub-publish.yml']:
    raise SystemExit(f'expected only evidence-hub-publish.yml to deploy pages, got {hits}')
print('ok')
