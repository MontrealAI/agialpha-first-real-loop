import unittest
from agialpha_evidence_hub.validate import validate_manifest

class TestNoOverclaim(unittest.TestCase):
    def test_rejects(self):
        with self.assertRaises(ValueError):
            validate_manifest({'schema_version':'agialpha.evidence_run.v1','experiment_slug':'x','workflow_name':'wf','run_id':'1','run_url':'u','claim_boundary':'achieved AGI','metrics':{}})
    def test_allows_negated(self):
        validate_manifest({'schema_version':'agialpha.evidence_run.v1','experiment_slug':'x','workflow_name':'wf','run_id':'1','run_url':'u','claim_boundary':'does not claim achieved AGI','metrics':{}})

if __name__=='__main__': unittest.main()
