import os, subprocess, sys, tempfile


def test_no_valuation_assertion_phrase():
    out = tempfile.mkdtemp()
    subprocess.check_call([
        sys.executable, '-m', 'agialpha_valuation_support', 'build',
        '--repo-root', '.', '--ascension-registry', 'ascension_os_registry',
        '--comparables', 'config/valuation_support_public_comparables.example.json',
        '--market-context', 'config/valuation_support_market_context.example.json',
        '--out', out,
    ])
    for name in os.listdir(out):
        if name.endswith('.json') or name.endswith('.md'):
            blob = open(os.path.join(out, name), encoding='utf-8').read().lower()
            assert 'agi alpha is worth' not in blob
