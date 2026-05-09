import json,unittest,tempfile
from pathlib import Path
from secure_rails.connector_registry import update_registry,build_connector_data
class T(unittest.TestCase):
  def test_registry(self):
    with tempfile.TemporaryDirectory() as td:
      r=Path(td)/'r';
      p=Path(td)/'i.json';p.write_text(json.dumps({'schema_version':'securerails.customer_installation.v1','installation_id':'../../escape'}));update_registry(p,r)
      files=list((r/'installations').glob('*.json'));self.assertEqual(len(files),1);self.assertNotIn('..',files[0].name)
      p2=Path(td)/'i2.json';p2.write_text(json.dumps({'schema_version':'securerails.customer_installation.v1'}));update_registry(p2,r)
      self.assertEqual(len(list((r/'installations').glob('*.json'))),2)
      o=Path(td)/'o';build_connector_data(r,o);self.assertTrue((o/'summary.json').exists())
  def test_unknown_schema_rejected(self):
    with tempfile.TemporaryDirectory() as td:
      r=Path(td)/'r'; p=Path(td)/'u.json'; p.write_text(json.dumps({'schema_version':'nope'}))
      with self.assertRaises(ValueError): update_registry(p,r)
