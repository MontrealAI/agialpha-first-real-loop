from pathlib import Path

def test_secure_rails_docs_exist():
    assert Path('docs/secure-rails/README.md').exists()
    assert Path('docs/secure-rails/work-vaults-mark-sovereigns.md').exists()
    assert Path('docs/secure-rails/templates/README.md').exists()
