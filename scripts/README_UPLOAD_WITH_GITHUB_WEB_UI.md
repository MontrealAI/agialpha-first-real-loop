# Upload RSI-FORGE-002 using GitHub web UI

1. Unzip the package on your computer.
2. Open `https://github.com/MontrealAI/agialpha-first-real-loop`.
3. Click **Add file** -> **Upload files**.
4. Drag these folders/files into the upload area:
   - `rsi_forge_002/`
   - `.github/workflows/rsi-forge-002-autonomous.yml`
   - `.github/workflows/rsi-forge-002-independent-replay.yml`
   - `.github/workflows/rsi-forge-002-falsification-audit.yml`
   - `.github/ISSUE_TEMPLATE/rsi-forge-002-external-review.md`
   - `config/`
   - `data/`
   - `schemas/`
   - `tests/`
   - `README_RSI_FORGE_002.md`
5. Commit message: `Add RSI-FORGE-002 governed recursive self-improvement experiment`.
6. Click **Commit changes**.
7. Go to **Actions**.
8. Select **AGI ALPHA RSI-FORGE-002 / Autonomous**.
9. Click **Run workflow**.
10. Use defaults and click the green **Run workflow** button.

After the run turns green, open the artifact and review the generated PR.
