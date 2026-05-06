from pathlib import Path

def test_glossary_exists():
    p = Path('docs/GLOSSARY.md')
    assert p.exists()
    t = p.read_text(encoding='utf-8').lower()
    for term in ['evidence mission control','securerails','proofbundle','evidence docket','rsi governor']:
        assert term in t
