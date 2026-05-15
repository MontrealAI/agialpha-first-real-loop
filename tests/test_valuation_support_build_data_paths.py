import json
import os
import subprocess
import sys
import tempfile


def test_build_data_resolves_run_ref_relative_to_registry_parent():
    run_out = tempfile.mkdtemp(prefix='val-run-')
    subprocess.check_call([
        sys.executable, '-m', 'agialpha_valuation_support', 'build',
        '--repo-root', '.',
        '--ascension-registry', 'ascension_os_registry',
        '--comparables', 'config/valuation_support_public_comparables.example.json',
        '--market-context', 'config/valuation_support_market_context.example.json',
        '--out', run_out,
    ])
    out = tempfile.mkdtemp(prefix='val-gen-')
    subprocess.check_call([
        sys.executable, '-m', 'agialpha_valuation_support', 'build-data',
        '--registry', 'valuation_support_registry',
        '--out', out,
    ])
    data = json.load(open(os.path.join(out, 'public_comparables.json'), 'r', encoding='utf-8'))
    assert 'comparables' in data
    assert data.get('not_reported') is None
