# SecureRails Quick Start Upload Guide

## Browser upload

1. Download and unzip this package.
2. Open the repository: `https://github.com/MontrealAI/agialpha-first-real-loop`.
3. Create a new branch named:

```text
securerails-worldwide-deployment-v2-1
```

4. Click **Add file → Upload files**.
5. Drag the **contents** of the unzipped package into the repository root.
6. Do **not** replace the existing root `README.md`. Instead, open `README_SECURE_RAILS_SNIPPET_FOR_ROOT_README.md` and paste that section into the existing README.
7. Commit with:

```text
Add SecureRails worldwide deployment package v2.1
```

8. Open a Pull Request into `main`.
9. Confirm that this workflow passes:

```text
SecureRails Compliance Guard
```

10. Review the package manually before merge.

## Command-line upload

```bash
git clone https://github.com/MontrealAI/agialpha-first-real-loop.git
cd agialpha-first-real-loop
git checkout -b securerails-worldwide-deployment-v2-1

unzip /path/to/securerails_worldwide_deployment_package_v2_1_FINAL.zip -d /tmp/securerails_v2_1
rsync -av /tmp/securerails_v2_1/ ./

python scripts/secure_rails_claim_boundary_check.py .
python scripts/secure_rails_safety_ledger_check.py docs/secure-rails/templates/safety-ledger-example.json
python scripts/secure_rails_no_automerge_check.py .
python scripts/secure_rails_use_case_triage_check.py docs/secure-rails/templates/deployment-intake-example.json

git add .
git commit -m "Add SecureRails worldwide deployment package v2.1"
git push origin securerails-worldwide-deployment-v2-1
```

Then open a Pull Request in GitHub.

## Where files go

Upload these paths to the repository root:

```text
README_SECURERAILS_WORLDWIDE_DEPLOYMENT.md
SECURERAILS_QUICK_START_UPLOAD_GUIDE.md
SECURERAILS_WORLDWIDE_LAUNCH_CHECKLIST.md
README_SECURE_RAILS_SNIPPET_FOR_ROOT_README.md
docs/secure-rails/
config/
schemas/
scripts/
.github/workflows/secure-rails-compliance-guard.yml
.github/ISSUE_TEMPLATE/secure-rails-compliance-review.yml
.github/PULL_REQUEST_TEMPLATE/secure-rails-safe-remediation.md
```

## What not to do

- Do not deploy this directly to production without legal and security review.
- Do not enable auto-merge.
- Do not use SecureRails for employee performance evaluation.
- Do not use SecureRails as a safety component for critical infrastructure without reclassification.
- Do not describe SecureRails as cybersecurity certification.
- Do not describe `$AGIALPHA` as yield, dividends, ownership, profit rights, or investment upside.
