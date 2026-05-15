import json
import os
import subprocess
import sys
import tempfile


def test_build_honors_ascension_registry_argument_in_evidence_inventory():
    out = tempfile.mkdtemp(prefix='val-asc-reg-')
    custom_registry = 'ascension_os_registry'
    subprocess.check_call([
        sys.executable, '-m', 'agialpha_valuation_support', 'build',
        '--repo-root', '.',
        '--ascension-registry', custom_registry,
        '--comparables', 'config/valuation_support_public_comparables.example.json',
        '--market-context', 'config/valuation_support_market_context.example.json',
        '--out', out,
    ])
    inventory = json.load(open(os.path.join(out, '03_agialpha_evidence_inventory.json'), 'r', encoding='utf-8'))
    row = next(i for i in inventory['items'] if i['artifact_type'] == 'ascension_os_registry')
    assert row['path'] == custom_registry
