import unittest
from secure_rails.repository_dispatch_bridge import build_dispatch_from_webhook_event,validate_dispatch_payload
class T(unittest.TestCase):
  def test_dispatch(self):
    event={'event_id':'1','event_type':'workflow_run','repository':{'full_name':'org/secret-tools'},'workflow_run':{'run_id':1,'conclusion':'success'},'security':{'signature_verified':True}}
    d=build_dispatch_from_webhook_event(event);self.assertTrue(validate_dispatch_payload(d)[0])
  def test_unverified_rejected(self):
    with self.assertRaises(ValueError):
      build_dispatch_from_webhook_event({'event_id':'1','event_type':'workflow_run','workflow_run':{'run_id':1,'conclusion':'success'},'security':{'signature_verified':False}})
  def test_non_workflow_event_rejected(self):
    with self.assertRaises(ValueError):
      build_dispatch_from_webhook_event({'event_id':'1','event_type':'pull_request','security':{'signature_verified':True}})
