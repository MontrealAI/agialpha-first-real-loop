from pathlib import Path

def test_business_positioning_text_present():
    txt=Path('docs/ascension-os/business-positioning.md').read_text()
    assert 'not “we claim superintelligence.”' in txt
