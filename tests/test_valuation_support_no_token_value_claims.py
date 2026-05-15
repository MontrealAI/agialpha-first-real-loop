import json, os, subprocess, sys, tempfile


def test_no_token_appreciation_phrase():
    out = tempfile.mkdtemp()
    subprocess.check_call([
        sys.executable, '-m', 'agialpha_valuation_support', 'build',
        '--repo-root', '.', '--ascension-registry', 'ascension_os_registry',
        '--comparables', 'config/valuation_support_public_comparables.example.json',
        '--market-context', 'config/valuation_support_market_context.example.json',
        '--out', out,
    ])
    text = json.dumps(json.load(open(os.path.join(out, '12_valuation_support_memo.md'), 'r', encoding='utf-8')) if False else {}, sort_keys=True)
    for name in os.listdir(out):
        if name.endswith('.json') or name.endswith('.md'):
            blob = open(os.path.join(out, name), encoding='utf-8').read().lower()
            assert 'token appreciation' not in blob
