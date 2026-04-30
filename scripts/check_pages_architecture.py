from pathlib import Path
import sys
n=[]
for p in Path('.github/workflows').glob('*.yml'):
    t=p.read_text()
    if 'actions/deploy-pages@' in t:
        n.append(p.name)
if n != ['evidence-hub-publish.yml']:
    print('deploy-pages must only exist in evidence-hub-publish.yml; found:',n)
    sys.exit(1)
print('ok')
