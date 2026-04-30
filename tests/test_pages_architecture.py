import unittest, subprocess
class T(unittest.TestCase):
    def test_architecture(self):
        subprocess.check_call(['python','scripts/check_pages_architecture.py'])
if __name__=='__main__': unittest.main()
