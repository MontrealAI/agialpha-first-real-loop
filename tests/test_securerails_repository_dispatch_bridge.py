import unittest
from secure_rails.repository_dispatch_bridge import build_dispatch_from_webhook_event,validate_dispatch_payload
class T(unittest.TestCase):
  def test_dispatch(self):
    d=build_dispatch_from_webhook_event({'event_id':'1','repository':{'full_name':'a/b'},'workflow_run':{'run_id':1}});self.assertTrue(validate_dispatch_payload(d)[0])
