import unittest, subprocess, sys

class TestPagesArch(unittest.TestCase):
    def test_arch(self):
        subprocess.check_call([sys.executable,'scripts/check_pages_architecture.py'])

if __name__=='__main__': unittest.main()
