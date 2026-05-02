from dataclasses import dataclass, asdict
SCHEMA_VERSION = "agialpha.agiga.opportunity_intermediate.v1"
@dataclass
class OpportunityIntermediate:
    opportunity_id:str; operator_goal:str; domain:str; pain_point:str; current_bottleneck:str; available_tools:list; constraints:list; risk_envelope:str; proof_goal:str; validator_hint:str; useful_capacity_hypothesis:str; commercial_usefulness_class:str; candidate_capability_package:str; descendant_niche_hint:str; claim_boundary:str; schema_version:str=SCHEMA_VERSION
    def to_dict(self): return asdict(self)
