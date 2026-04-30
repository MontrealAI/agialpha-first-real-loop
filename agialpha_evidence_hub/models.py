from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class RunRecord:
    data: Dict[str, Any]

@dataclass
class Registry:
    runs: List[Dict[str, Any]] = field(default_factory=list)
    experiments: List[Dict[str, Any]] = field(default_factory=list)
    workflows: List[Dict[str, Any]] = field(default_factory=list)
