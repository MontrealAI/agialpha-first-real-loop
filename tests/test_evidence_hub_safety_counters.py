import unittest
from agialpha_evidence_hub.validate import validate_manifest
class T(unittest.TestCase):
    def test_security_requires_counters(self):
        with self.assertRaises(ValueError):
            validate_manifest({'schema_version':'agialpha.evidence_run.v1','experiment_slug':'cyber-sovereign-001','workflow_name':'wf','run_id':'1','run_url':'u','claim_boundary':'does not claim','metrics':{}})
if __name__=='__main__': unittest.main()
