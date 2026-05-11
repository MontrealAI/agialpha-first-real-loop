
from __future__ import annotations
import json, re
from pathlib import Path

ALLOWED_CHANNELS={"rc","stable","internal","pilot"}
CLAIM_BOUNDARY_DEFAULT="SecureRails release artifacts are installable governance and evidence tooling. This release does not certify security, does not claim empirical SOTA, and does not authorize autonomous remediation."
FORBIDDEN=["certified","certification","slsa certified","openssf certified","investment return","token appreciation","yield","dividends","profit rights","ownership rights"]


def build_manifest(release_version:str, release_channel:str, repo:str, commit_sha:str, branch:str, included_components:list[str], excluded_components:list[str]):
    rid=f"securerails-{release_version}"
    return {
      "schema_version":"securerails.release_manifest.v1",
      "release_id":rid,
      "release_version":release_version,
      "release_channel":release_channel,
      "generated_at":__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat().replace('+00:00','Z'),
      "repository":repo,
      "commit_sha":commit_sha,
      "branch":branch,
      "release_scope":["SecureRails Compliance Guard","SecureRails Work Vaults","MARK allocations","Sovereigns","Agentic PR Guard","Customer pilot intake","GitHub App connector","Supply-chain provenance"],
      "included_components":included_components,
      "excluded_components":excluded_components,
      "artifact_manifest_path":"artifact_manifest.json",
      "checksums_path":"CHECKSUMS.sha256",
      "release_notes_path":"RELEASE_NOTES.md",
      "marketplace_readiness_path":"marketplace_readiness.json",
      "customer_install_bundle_path":"CUSTOMER_INSTALL.md",
      "claim_boundary":CLAIM_BOUNDARY_DEFAULT
    }

def validate_manifest(obj:dict)->tuple[bool,list[str]]:
    errs=[]
    if not obj.get('release_version'): errs.append('release_version missing')
    if obj.get('release_channel') not in ALLOWED_CHANNELS: errs.append('invalid release_channel')
    if not obj.get('claim_boundary'): errs.append('claim_boundary missing')
    txt=json.dumps(obj).lower()
    for t in FORBIDDEN:
      if t in txt: errs.append(f'forbidden claim term: {t}')
    return (len(errs)==0,errs)
