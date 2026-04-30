from pathlib import Path
required = [
    'agialpha_phoenix_gauntlet/__main__.py',
    'agialpha_phoenix_gauntlet/core.py',
    'tests/test_phoenix_gauntlet.py',
    'phoenix_challenge_packs/default_review_challenge.json',
    'COPY_WORKFLOWS/phoenix-hub-001-autonomous.yml'
]
missing = [p for p in required if not Path(p).exists()]
if missing:
    raise SystemExit('Missing files: ' + ', '.join(missing))
print('PHOENIX-HUB-001 package files present.')
