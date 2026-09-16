# TTP Benchmark Dashboard

Interactive comparison of 10 TTP methods (CoCo+, SAVI, RWS, CoCo, CS2SA*, CS2SA,
MA2B, S5, MATLS, and MMAILS) across the CatA/B/C instance set. The page
(`index.html`) reads its data from `data.json`, which is generated from the
Excel workbook by `scripts/xlsx_to_json.py`.

## One-time setup

1. **Create a new GitHub repository** (public — GitHub Pages on a free
   personal account only serves public repos) and push everything in this
   folder to it:
   ```bash
   git init
   git add .
   git commit -m "Initial dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```

2. **Allow the workflow to push commits.** In the repo:
   `Settings → Actions → General → Workflow permissions` → select
   **"Read and write permissions"** → Save.
   (Without this, the auto-update Action can regenerate `data.json` but
   won't be able to commit it back.)

3. **Turn on GitHub Pages.**
   `Settings → Pages → Build and deployment → Source: Deploy from a branch`
   → Branch: `main`, folder `/ (root)` → Save.
   After a minute your dashboard is live at:
   ```
   https://<your-username>.github.io/<repo-name>/
   ```
   That's the link to share with your student.

## Updating the results

Whenever you have a new version of the workbook:

1. Replace the `.xlsx` file in the repo (keep the same filename, or update
   the filename reference — the workflow just picks up the first `*.xlsx`
   file it finds in the repo root) and push:
   ```bash
   git add ttp_literature_catABC_results_updated.xlsx
   git commit -m "Update results"
   git push
   ```
2. That push triggers the **"Update dashboard data"** GitHub Action, which
   re-runs `scripts/xlsx_to_json.py` and commits the refreshed `data.json`.
3. GitHub Pages redeploys automatically. Refresh the dashboard URL (hard
   refresh / clear cache if you don't see the change right away) and the
   new numbers are there — no manual export or re-upload step needed.

You can also trigger the update manually from the **Actions** tab →
"Update dashboard data" → **Run workflow**, e.g. if you only changed a
formula/value in the workbook without renaming anything.

## If you add or rename a method column

`scripts/xlsx_to_json.py` reads method names straight from row 2 of the
sheet and treats the **last populated method column** as "yours" (it
appends " (Ours)" so the dashboard highlights it in gold). If you add new
literature baselines, insert their columns *before* your own column so it
stays last — no code changes needed either in the script or in
`index.html`, which reads the method list from `data.json` at runtime.

## Local preview

You can't just double-click `index.html` (browsers block `fetch()` on
`file://` URLs). Serve the folder locally instead:
```bash
python3 -m http.server 8000
```
then open `http://localhost:8000/`.

## Files

| File | Purpose |
|---|---|
| `index.html` | The dashboard itself (no external dependencies) |
| `data.json` | Generated data consumed by the dashboard |
| `*.xlsx` | Source workbook |
| `scripts/xlsx_to_json.py` | Converts the workbook to `data.json` |
| `.github/workflows/update-data.yml` | Auto-regenerates `data.json` on push |
