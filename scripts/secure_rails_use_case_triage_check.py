#!/usr/bin/env python3
"""Validate a SecureRails deployment intake for default allowed posture."""
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('docs/secure-rails/templates/deployment-intake-example.json')
obj=json.loads(p.read_text(encoding='utf-8'))
blocked_flags=[
    'uses_for_hr_or_worker_management','uses_for_profiling_natural_persons',
    'uses_as_critical_infrastructure_safety_component','uses_for_biometric_decisions',
    'uses_for_education_decisions','uses_for_credit_or_essential_services','uses_for_law_enforcement',
    'uses_for_migration_or_border','uses_for_justice_or_legal_decisions','external_target_scanning',
    'exploit_execution','malware_generation','social_engineering','raw_secret_output',
    'provides_gpai_model','claims_certification_or_guarantee'
]
fail=[]
if not obj.get('repo_owned_scope'):
    fail.append('repo_owned_scope must be true for default posture')
if not obj.get('human_review_required'):
    fail.append('human_review_required must be true')
if obj.get('automerge_enabled'):
    fail.append('automerge_enabled must be false')
for k in blocked_flags:
    if obj.get(k) is True:
        fail.append(f'{k} requires blocked_or_escalate or counsel review')
if obj.get('decision') == 'allowed_default' and fail:
    print('SecureRails use-case triage check FAILED')
    for x in fail: print('-', x)
    sys.exit(1)
print('SecureRails use-case triage check passed')
