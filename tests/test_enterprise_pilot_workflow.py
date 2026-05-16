from pathlib import Path
def test_workflow_exists():
 assert Path('.github/workflows/agialpha-enterprise-pilot-001.yml').exists()
