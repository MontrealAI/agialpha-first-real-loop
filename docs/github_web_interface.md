# Super-friendly GitHub web setup

This guide uses the GitHub website, not the command line.

## A. Create the repository

1. Sign in to GitHub.
2. Click the **+** icon in the top-right corner.
3. Click **New repository**.
4. Repository name: `agialpha-first-real-loop`.
5. Description: `Replayable Nova-Seed → MARK → Mini Sovereign → AGI Jobs → Evidence Docket → vNext loop`.
6. Choose **Public** or **Private**.
7. Select **Add a README file** only if you want GitHub to initialize the repo. If you initialize it, you will overwrite or update that README after uploading these files.
8. Click **Create repository**.

## B. Upload the files using the web interface

1. Download and unzip `agialpha-first-real-loop.zip`.
2. Open the unzipped folder on your computer.
3. In GitHub, open your new repository.
4. Click **Add file** → **Upload files**.
5. Drag the **contents** of the unzipped folder into the upload area. Do not drag the zip file itself.
6. GitHub may limit browser uploads to 100 files at a time and 25 MiB per file. This repository is small; if upload fails, upload the folders in batches.
7. Commit message: `Add AGI ALPHA First Real Loop`.
8. Click **Commit changes**.

Official GitHub documentation says the web upload flow is **Add file → Upload files**, and that you can drag and drop files or folders into the browser. GitHub also documents browser upload limits, including the 25 MiB per-file web limit and the 100-files-at-a-time limit.

## C. Run the loop from GitHub Actions

1. After the upload, click the **Actions** tab.
2. If GitHub asks whether to enable workflows, click **I understand my workflows, go ahead and enable them**.
3. Click **Replay First Real Loop**.
4. Click **Run workflow**.
5. Wait for the green checkmark.
6. Open the completed workflow run.
7. Download the artifact named `evidence-docket-ci-loop`.

That artifact is the replayed Evidence Docket.

## D. Run locally if you prefer

```bash
python -m agialpha_first_loop.run
python -m unittest discover -s tests
```

## E. Replace demo review with real review

For external proof, edit:

```text
data/mark_review_card.json
data/reviewer_decisions_seed001.json
```

Use a real reviewer name or reviewer ID, rerun the loop, and publish the resulting Evidence Docket.
