from pathlib import Path
forbidden=['actions/deploy-pages','actions/upload-pages-artifact','github-pages-deploy-action','peaceiris/actions-gh-pages','jamesives/github-pages-deploy-action']
allowed='evidence-hub-publish.yml'
viol=[]
for p in Path('.github/workflows').glob('*.yml'):
    t=p.read_text().lower()
    for f in forbidden:
        if f in t and p.name!=allowed:
            viol.append((p.name,f))
if viol:
    raise SystemExit('forbidden pages deploy references: '+str(viol))
if 'actions/deploy-pages' not in Path('.github/workflows',allowed).read_text().lower():
    raise SystemExit('central publisher missing deploy-pages')
print('ok')
