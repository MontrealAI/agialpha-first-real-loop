# High-Risk Use Case Denial Policy

SecureRails must reject or escalate deployments that attempt to use it for high-risk decisions about people or safety-critical controls.

## Deny by default

- Biometric identification or categorization.
- Emotion recognition.
- Social scoring.
- Employment decisions.
- Credit or insurance eligibility.
- Education admissions or grading.
- Law enforcement, migration, asylum, border control, or justice decisions.
- Medical diagnosis or treatment decisions.
- Critical-infrastructure safety control.

## Allowed with review

SecureRails may support defensive software evidence for organizations operating in these sectors, provided it does not make high-risk decisions itself and deployment is reviewed by counsel and customer governance.

## Escalation

If a customer tries to use SecureRails for a high-risk decision system:

1. stop deployment;
2. classify intended purpose;
3. notify legal and compliance owner;
4. complete AI Act triage and DPIA;
5. require written approval before any production use.

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
