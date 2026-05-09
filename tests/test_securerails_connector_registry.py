import json,unittest,tempfile
from pathlib import Path
from secure_rails.connector_registry import update_registry,build_connector_data
class T(unittest.TestCase):
  def test_registry(self):
    with tempfile.TemporaryDirectory() as td:
      r=Path(td)/'r';
      for i in range(2):
        p=Path(td)/f'i{i}.json';p.write_text(json.dumps({'schema_version':'unknown'}));update_registry(p,r)
      files=list((r/'installations').glob('*.json'));self.assertEqual(len(files),2)
      o=Path(td)/'o';build_connector_data(r,o);self.assertTrue((o/'summary.json').exists())
