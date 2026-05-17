from pathlib import Path
import json

def test_workflow_index_exists():
    data=json.loads(Path('docs/_generated/public-experience/workflow_index.json').read_text())
    assert len(data['workflows']) > 0
