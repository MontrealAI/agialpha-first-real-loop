# AGI ALPHA CYBER-SOVEREIGN-002

**Defensive Capability Compounding for the AGI ALPHA Evidence Infrastructure**

CYBER-SOVEREIGN-002 tests whether `CyberSecurityCapabilityArchive-v0` can be reused to detect, prioritize, package, and safely remediate repo-owned security work better than a no-reuse baseline.

The core comparison is:

```text
B5 = Cyber Sovereign without archive reuse
B6 = Cyber Sovereign with CyberSecurityCapabilityArchive-v0/v1 reuse
```

## Defensive boundary

Allowed:

```text
GitHub Actions permission review
workflow hardening review
secret hygiene with redaction
Evidence Docket integrity checks
security runbook generation
security issue backlog generation
safe patch proposal
claim-boundary audit
external reviewer kit
delayed-outcome sentinel
```

Forbidden:

```text
external target scanning
exploit execution
credential disclosure
malware generation
social engineering
real-world offensive testing
automatic deployment of high-risk changes
printing secret values
```

## Main command

```bash
python -m agialpha_cyber_sovereign2 run --repo . --out runs/cyber-sovereign-002/manual
python -m agialpha_cyber_sovereign2 scoreboard runs/cyber-sovereign-002/manual --out public-site
```

## Workflows

Create these files under `.github/workflows/` from `COPY_WORKFLOWS/`:

```text
cyber-sovereign-002-autonomous.yml
cyber-sovereign-002-external-replay.yml
cyber-sovereign-002-scaling.yml
cyber-sovereign-002-falsification-audit.yml
cyber-sovereign-002-delayed-outcome.yml
cyber-sovereign-002-safe-pr-proposal.yml
```

Run the main workflow first:

```text
Actions → AGI ALPHA Cybersecurity Sovereign 002 / Autonomous → Run workflow
```

Then confirm or manually run:

```text
AGI ALPHA Cybersecurity Sovereign 002 External Replay / L4
AGI ALPHA Cybersecurity Sovereign 002 Scaling / L6 Proxy
AGI ALPHA Cybersecurity Sovereign 002 Falsification Audit
AGI ALPHA Cybersecurity Sovereign 002 Delayed Outcome Sentinel
AGI ALPHA Cybersecurity Sovereign 002 Safe PR Proposal
```

## Claim boundary

CYBER-SOVEREIGN-002 does not claim achieved AGI, ASI, empirical SOTA cybersecurity, offensive cyber capability, real-world security certification, guaranteed security, or safe autonomy. It is a bounded, defensive, repo-owned Evidence Docket experiment.
