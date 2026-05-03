# Critical Infrastructure Safety-Component Boundary

## Policy

SecureRails is not designed or marketed as a safety component of critical infrastructure. It is an advisory governance and evidence-support layer for repo-owned defensive software work.

## Default rule

SecureRails outputs require independent human and technical validation before production use. They must not directly control or materially determine the safe operation of road traffic, water, gas, heating, electricity, medical devices, industrial systems, financial critical operations, or similar safety-critical infrastructure.

## Allowed

- Reviewing repository workflows used by a regulated customer.
- Producing advisory findings.
- Producing Evidence Dockets and ProofBundles.
- Preparing safe PR proposals for human review.
- Supporting audit and governance evidence.

## Not allowed by default

- Direct control of critical infrastructure.
- Automated safety decisions.
- Reliance as the sole safety validation layer.
- Deployment as a legally required safety component.
- Use without independent validation in safety-critical production systems.

## Escalation

If a customer wants to use SecureRails in a safety-critical context, the deployment must be marked `blocked_or_escalate` until counsel and security leadership complete a separate classification and risk assessment.

## Customer clause

> Customer will not use SecureRails as a critical-infrastructure safety component or as the sole basis for safety-critical operational decisions. SecureRails outputs are advisory and require independent validation before production use.

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
