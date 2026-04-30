from dataclasses import dataclass, asdict
from typing import Any, Dict

@dataclass
class EvidenceRun:
    data: Dict[str, Any]
    def to_dict(self):
        return dict(self.data)
