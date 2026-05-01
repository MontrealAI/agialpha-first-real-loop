import unittest
from pathlib import Path

class T(unittest.TestCase):
    def test_modules_exist(self):
        req=["__init__.py","cli.py","kernel.py","discovery_policy.py","claim_policy.py","scoring_policy.py","safety_policy.py","promotion_policy.py","recommendation_policy.py","page_quality_policy.py","registry_policy.py","workflow_policy.py","replay_policy.py","falsification_policy.py","human_review_policy.py"]
        for n in req:
            self.assertTrue((Path("agialpha_governance_kernel")/n).exists())
