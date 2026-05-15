import json, subprocess, sys, tempfile, os

def test_arr_math_not_reported_comparable_path():
    out = tempfile.mkdtemp()
    subprocess.check_call([
        sys.executable, '-m', 'agialpha_valuation_support', 'build',
        '--repo-root', '.',
        '--ascension-registry', 'ascension_os_registry',
        '--comparables', 'config/valuation_support_public_comparables.example.json',
        '--market-context', 'config/valuation_support_market_context.example.json',
        '--out', out,
    ])
    d = json.load(open(os.path.join(out, '06_market_equivalence_sensitivity.json'), encoding='utf-8'))
    assert d['required_arr_by_multiple']['10'] == 'not_reported'
    assert d['required_arr_by_multiple']['20'] == 'not_reported'
    assert d['required_arr_by_multiple']['30'] == 'not_reported'
    assert d['required_arr_by_multiple']['50'] == 'not_reported'
