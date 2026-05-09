
from __future__ import annotations
import json
from pathlib import Path
ALLOWED_INSTANCE_TYPES = {'pilot','customer','internal','canonical','demo'}
REQUIRED_FORBIDDEN_USE_ACKS = (
    'no_hr_worker_evaluation',
    'no_profiling_natural_persons',
    'no_automated_decisions_about_natural_persons',
    'no_critical_infrastructure_safety_component_reliance',
    'no_offensive_cyber',
    'no_auto_merge',
    'no_investment_product_framing',
)

def build_instance_config(owner:str, repository:str, instance_name:str, instance_type:str, pages_url:str='') -> dict:
    if instance_type not in ALLOWED_INSTANCE_TYPES:
        raise ValueError('invalid instance_type')
    full = f"{owner}/{repository}"
    return {
      'schema_version':'securerails.instance_config.v1','instance_id':f"{owner.lower()}-{repository}".replace('_','-'),'instance_name':instance_name,
      'owner':owner,'repository':repository,'full_repository':full,'source_template':'MontrealAI/agialpha-first-real-loop','instance_type':instance_type,
      'visibility':'unknown','public_pages_url':pages_url,'evidence_mission_control_url':pages_url,
      'secure_rails':{'enabled':True,'compliance_guard_required':True,'work_vaults_enabled':True,'agentic_pr_guard_enabled':False,'customer_pilot_intake_enabled':False,'github_app_connector_enabled':False},
      'claim_boundary':'SecureRails is AI-agent security governance and proof-bound defensive remediation. This instance does not certify security, does not perform offensive cyber activity, and does not make autonomous decisions about natural persons.',
      'forbidden_use_acknowledgement':{'no_hr_worker_evaluation':True,'no_profiling_natural_persons':True,'no_automated_decisions_about_natural_persons':True,'no_critical_infrastructure_safety_component_reliance':True,'no_offensive_cyber':True,'no_auto_merge':True,'no_investment_product_framing':True},
      'token_boundary':{'agialpha_utility_only':True,'no_yield':True,'no_dividends':True,'no_ownership':True,'no_profit_rights':True,'no_guaranteed_appreciation':True}
    }

def validate_instance_config(cfg:dict)->list[str]:
    errs=[]
    for k in ('owner','repository','full_repository','claim_boundary'):
        if not cfg.get(k): errs.append(f'missing {k}')
    if cfg.get('instance_type') not in ALLOWED_INSTANCE_TYPES: errs.append('invalid instance_type')
    fua = cfg.get('forbidden_use_acknowledgement',{})
    for key in REQUIRED_FORBIDDEN_USE_ACKS:
        if fua.get(key) is not True:
            errs.append(f'{key} must be true')
    tb=cfg.get('token_boundary',{})
    for k in ('agialpha_utility_only','no_yield','no_dividends','no_ownership','no_profit_rights','no_guaranteed_appreciation'):
        if tb.get(k) is not True: errs.append(f'{k} must be true')
    return errs

def load_and_validate(path:Path)->list[str]:
    return validate_instance_config(json.loads(path.read_text(encoding='utf-8')))
