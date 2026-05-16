from pathlib import Path
def test_docs_exist():
 assert Path('README_ENTERPRISE_PILOT.md').exists()
 assert Path('docs/enterprise-pilot/operator-guide.md').exists()
