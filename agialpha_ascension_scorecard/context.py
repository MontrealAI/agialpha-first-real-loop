
from dataclasses import dataclass
from pathlib import Path
@dataclass
class AscensionContext:
    repo_root: Path
    run_dir: Path
