import json, os, subprocess, sys, tempfile


def test_moat_assessment_exists():
    out = tempfile.mkdtemp()
    subprocess.check_call([
        sys.executable, '-m', 'agialpha_valuation_support', 'build',
        '--repo-root', '.', '--ascension-registry', 'ascension_os_registry',
        '--comparables', 'config/valuation_support_public_comparables.example.json',
        '--market-context', 'config/valuation_support_market_context.example.json',
        '--out', out,
    ])
    data = json.load(open(os.path.join(out, '08_moat_assessment.json'), encoding='utf-8'))
    assert 'evidence_moat' in data
