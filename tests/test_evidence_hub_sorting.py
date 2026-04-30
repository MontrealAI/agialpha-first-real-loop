import unittest, json
class T(unittest.TestCase):
    def test_sorted(self):
        runs=json.load(open('evidence_registry/runs.json')) if __import__('pathlib').Path('evidence_registry/runs.json').exists() else []
        self.assertEqual(runs, sorted(runs,key=lambda x:x.get('generated_at',''), reverse=True))
if __name__=='__main__': unittest.main()
