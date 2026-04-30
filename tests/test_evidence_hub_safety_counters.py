import unittest
from agialpha_evidence_hub.validate import validate_manifest, default_manifest

class TestSafetyCounters(unittest.TestCase):
    def test_required_present(self):
        m=default_manifest('cyber-sovereign-001'); m['source']='manifest'; m['run_url']='http://x'; m['workflow_name']='wf'
        validate_manifest(m)

if __name__=='__main__': unittest.main()
