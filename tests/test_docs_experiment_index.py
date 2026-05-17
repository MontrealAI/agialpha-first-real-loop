from pathlib import Path
import json

def test_experiment_index_exists():
    data=json.loads(Path('docs/_generated/public-experience/experiment_index.json').read_text())
    assert data['experiments']
