import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class GovernanceKernel:
    policy: dict
    @classmethod
    def load(cls, path:str|Path):
        return cls(json.loads(Path(path).read_text()))
    def require_human_review(self)->bool:
        return self.policy.get("human_review_required", True)
