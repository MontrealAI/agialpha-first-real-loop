import json,unittest,tempfile
from pathlib import Path
from secure_rails.connector_registry import update_registry,build_connector_data
class T(unittest.TestCase):
  def test_registry(self):
    with tempfile.TemporaryDirectory() as td:
      r=Path(td)/'r';i=Path(td)/'i.json';i.write_text(json.dumps({'schema_version':'securerails.webhook_event.v1','event_id':'e1'}));update_registry(i,r);o=Path(td)/'o';build_connector_data(r,o);self.assertTrue((o/'summary.json').exists())
