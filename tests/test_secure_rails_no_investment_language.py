import subprocess, unittest
class T(unittest.TestCase):
    def test_token_boundary(self):
        subprocess.run(['python','-m','secure_rails','check-token-boundary','--repo-root','.'], check=True)
