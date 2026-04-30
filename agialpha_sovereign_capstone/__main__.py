import os
import sys
from .core import main

code = main()
sys.stdout.flush()
sys.stderr.flush()
os._exit(code)
