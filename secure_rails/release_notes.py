
def render_notes(manifest:dict)->str:
    return f"""# SecureRails Release Notes

## Release version
{manifest['release_version']}

## Release channel
{manifest['release_channel']}

## What is included
- Release manifest, checksums, artifact manifest, customer install bundle, Marketplace-ready export plan.

## What is not included
- Marketplace publication, autonomous certification, offensive cyber capabilities.

## Installation
See CUSTOMER_INSTALL.md and docs/.

## Required permissions
Read-only by default (`contents: read`, `actions: read`, `pull-requests: read` where needed).

## Artifacts
CHECKSUMS.sha256, artifact_manifest.json, release_manifest.json, marketplace_readiness.json.

## Known limitations
Monorepo is not a direct Marketplace action repository.

## Claim boundary
{manifest['claim_boundary']}

## Security posture
Defensive governance and proof-bound remediation only.

## $AGIALPHA utility boundary
$AGIALPHA remains utility-only and not an investment product.

## Human review requirement
Human review is required before promotion or publish actions.

## No auto-merge
No auto-merge behavior is enabled by this release train.

## No certification claim
No security, SLSA, or OpenSSF certification claim is made.

## Checks run
SecureRails Compliance Guard, docs audits, release validation tests.

## Links to docs
- docs/secure-rails/release-train.md
- docs/secure-rails/marketplace-readiness.md
"""
