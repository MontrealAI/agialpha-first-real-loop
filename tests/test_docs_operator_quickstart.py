from pathlib import Path

def test_operator_quickstart_exists():
    p = Path('docs/OPERATOR_QUICKSTART.md')
    assert p.exists()
    t = p.read_text(encoding='utf-8').lower()
    for sec in ['run an experiment','replay evidence','check securerails','inspect an evidence docket']:
        assert sec in t
