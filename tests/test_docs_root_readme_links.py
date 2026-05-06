import re
from pathlib import Path

def test_root_readme_relative_links_exist():
    text = Path('README.md').read_text(encoding='utf-8')
    links = re.findall(r'\]\(([^)]+)\)', text)
    for link in links:
        if link.startswith('http'):
            continue
        assert Path(link).exists(), link
