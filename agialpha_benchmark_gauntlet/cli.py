from __future__ import annotations

import sys
from .core import main_cli


def main() -> int:
    return main_cli(sys.argv[1:])
