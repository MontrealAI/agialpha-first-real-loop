from pathlib import Path

def test_public_site_guide_exists():
    assert Path('docs/PUBLIC_SITE_GUIDE.md').exists()
