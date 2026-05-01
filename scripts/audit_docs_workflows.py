#!/usr/bin/env python3
from pathlib import Path
import re, json
root=Path('.')
wf=sorted(p.name for p in (root/'.github/workflows').glob('*.yml'))
cat=(root/'docs/WORKFLOW_CATALOG.md').read_text() if (root/'docs/WORKFLOW_CATALOG.md').exists() else ''
docd=sorted(set(re.findall(r'`([^`]+\.yml)`',cat)))
print('undocumented_workflows=',[w for w in wf if w not in docd])
print('missing_workflow_files=',[d for d in docd if d not in wf])
print('ok_pages_only_central=', all(('evidence-hub-publish.yml'==w or 'pages' not in (root/'.github/workflows'/w).read_text().lower()) for w in wf))
