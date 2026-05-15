import json, os, subprocess, sys, tempfile


def test_commercial_readiness_exists_and_scored():
    out = tempfile.mkdtemp()
    subprocess.check_call([
        sys.executable, '-m', 'agialpha_valuation_support', 'build',
        '--repo-root', '.', '--ascension-registry', 'ascension_os_registry',
        '--comparables', 'config/valuation_support_public_comparables.example.json',
        '--market-context', 'config/valuation_support_market_context.example.json',
        '--out', out,
    ])
    data = json.load(open(os.path.join(out, '07_commercial_readiness.json'), encoding='utf-8'))
    assert 'score' in data
    assert data['score'] != 'not_reported'
