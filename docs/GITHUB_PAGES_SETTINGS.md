# GitHub Pages Settings (Evidence Hub)

## Required settings

1. **Settings → Pages**
   - **Source:** GitHub Actions

2. **Settings → Environments → github-pages**
   - Allow deployments from the default/protected branch policy used by the repository.
   - Do not require impossible manual approvals for the bot if autonomous publication is expected.
   - Keep deployment source constrained to trusted branch executions (main).

## Why

The publisher workflow now has strict main-branch deploy guards. PR and feature branches build/validate only and cannot deploy Pages.
