import json,unittest,tempfile
from pathlib import Path
from secure_rails.connector_registry import update_registry,build_connector_data
class T(unittest.TestCase):
  def test_registry(self):
    with tempfile.TemporaryDirectory() as td:
      r=Path(td)/'r';i=Path(td)/'i.json';i.write_text(json.dumps({'schema_version':'securerails.webhook_event.v1','event_id':'e1'}));update_registry(i,r);o=Path(td)/'o';build_connector_data(r,o);self.assertTrue((o/'summary.json').exists())
  def test_missing_id_does_not_overwrite(self):
    with tempfile.TemporaryDirectory() as td:
      r=Path(td)/'r'
      i1=Path(td)/'i1.json'; i1.write_text(json.dumps({'schema_version':'securerails.webhook_event.v1'}))
      i2=Path(td)/'i2.json'; i2.write_text(json.dumps({'schema_version':'securerails.webhook_event.v1'}))
      update_registry(i1,r); update_registry(i2,r)
      self.assertEqual(len(list((r/'events').glob('*.json'))), 2)
