import json,unittest
class T(unittest.TestCase):
 def test_schema(self): self.assertEqual(json.load(open('config/rsi_governance_kernel.json'))['schema_version'],'agialpha.rsi_governance_kernel.v1')

if __name__=="__main__": unittest.main()
