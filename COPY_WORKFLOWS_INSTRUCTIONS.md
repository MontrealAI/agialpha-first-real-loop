# Uploading OMEGA-AEGIS-001 with the GitHub web UI

## Option A — easiest: upload the folders at repository root

1. Unzip `omega-aegis-001-v0.1.zip` on your computer.
2. Go to `https://github.com/MontrealAI/agialpha-first-real-loop`.
3. Click `Add file` → `Upload files`.
4. Drag these folders/files into the upload box:
   - `omega_aegis_001`
   - `tests`
   - `README_OMEGA_AEGIS_001.md`
5. Commit directly to `main`.

## Option B — upload workflows

GitHub web upload is easiest inside the destination folder.

1. Go to `.github/workflows` in the repository.
2. Click `Add file` → `Upload files`.
3. Drag only these files:
   - `omega-aegis-001-autonomous.yml`
   - `omega-aegis-001-external-replay.yml`
   - `omega-aegis-001-falsification-audit.yml`
   - `omega-aegis-001-vnext-transfer.yml`
4. Commit directly to `main`.

## Option C — upload issue template

1. Go to `.github/ISSUE_TEMPLATE` in the repository.
2. Click `Add file` → `Upload files`.
3. Drag:
   - `omega-aegis-001-external-review.md`
4. Commit directly to `main`.

## Run it

1. Open the `Actions` tab.
2. Select `AGI ALPHA OMEGA-AEGIS-001 / Autonomous`.
3. Click `Run workflow`.
4. Leave defaults enabled.
5. Run.
6. Wait for success.
7. Download the artifact and copy the root hash.
8. Run `AGI ALPHA OMEGA-AEGIS-001 / External Replay` with the root hash.
9. Run the falsification and vNext workflows.

This experiment does not deploy GitHub Pages directly. It writes a `docs/omega-aegis-001` subpage and registry pointer, then attempts to trigger the central Evidence Hub publisher if that workflow exists. This avoids overwriting other experiments.
