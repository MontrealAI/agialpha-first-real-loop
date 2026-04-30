import unittest
from agialpha_evidence_hub.validate import validate_manifest, default_manifest

class TestNoOverclaim(unittest.TestCase):
    def test_reject_unsafe(self):
        m=default_manifest('x')
        m['source']='manifest'; m['run_url']='http://x'; m['workflow_name']='wf'; m['claim_boundary']='achieved AGI'
        with self.assertRaises(ValueError):
            validate_manifest(m)

    def test_allow_negative(self):
        m=default_manifest('x')
        m['source']='manifest'; m['run_url']='http://x'; m['workflow_name']='wf'; m['claim_boundary']='does not claim achieved AGI'
        validate_manifest(m)

if __name__=='__main__':
    unittest.main()
