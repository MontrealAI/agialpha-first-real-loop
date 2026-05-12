import unittest
from secure_rails.policy_kernel import load_kernel, validate_kernel

class T(unittest.TestCase):
    def test_kernel(self):
        k=load_kernel('config/securerails_policy_kernel.json')
        self.assertEqual([], validate_kernel(k))
        self.assertNotEqual('allow', k['default_decision'])
        self.assertTrue(k['human_review_required'])
        self.assertFalse(k['auto_merge_allowed'])

if __name__=='__main__': unittest.main()
