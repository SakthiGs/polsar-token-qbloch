# Public-release licensing and security audit — 18 November 2026

**Repository:** `SakthiGs/polsar-token-qbloch`  
**Decision:** Remain PRIVATE. This audit is a release-readiness check, **not** legal clearance or authorization to publish.

## 1. Scope and verified security facts

- Inspected the current default branch tree: **43 tracked blobs**, plus directory entries; no raw model-weight, image, archive or paper-PDF files.
- Enumerated all **26 reachable commit snapshots** through the GitHub Git tree API on 18 November 2026. No tracked files in those trees had the reviewed dataset/image/checkpoint/archive/key extensions, including `.pt`, `.pth`, `.npz`, `.npy`, `.tif`, `.tiff`, `.jpg`, `.png`, `.pdf`, `.zip`, `.h5`, `.parquet`, `.pem`, `.key`, `.p12`, `.pfx`.
- The Git refs returned by GitHub consist of **`refs/heads/main` only**, with no tag refs at audit time.
- Full-checkout GitHub Actions run [44365128038](https://github.com/SakthiGs/polsar-token-qbloch/actions/runs/44365128038) on head `609a39d` completed successfully: scanner processed **82 reachable Git blob objects** and found no configured GitHub/Google/AWS/OpenAI/Slack key patterns, private-key header or private Colab Drive path; **13 unit tests** and a **synthetic canonical-notebook run** passed.
- The scanner was extended to fail on sensitive **historical filenames** across reachable commits, including filenames subsequently deleted. GitHub Actions [44366594829](https://github.com/SakthiGs/polsar-token-qbloch/actions/runs/44366594829) on `c0d2c65` **passed**, including the new scanner and its regression tests. See `scripts/scan_git_history.py` and `tests/test_release_history_path.py`.
- `.gitignore` excludes common secrets, local environments, original raw imagery, model weights and caches. `results/summary/grid_per_seed_metrics.csv` contains model/seed aggregate metrics, not the original full-pol image arrays or individual candidate predictions.

### Security gaps remaining

- Pattern and filename scans are **not** a professional high-entropy secret scan. Run Gitleaks (or equivalent) over every reachable ref with a manually reviewed report before publicity. Also inspect for potentially personal metadata and embedded notebook/output content.
- Verify GitHub Dependabot, secret scanning/push protection and code scanning settings; these settings were **not confirmed** by the connected metadata endpoint.
- Perform dependency vulnerability audit against the **resolved install versions**, not just the broad ranges in `requirements.txt` and `requirements-full.txt`.
- Human review is still required to confirm none of the source files contain third-party code copied without appropriate licensing or sensitive unpublished material. An automated signature scan cannot determine copyright ownership.
- No developer secrets should ever be uploaded to an issue/commit/PR to request audit assistance. If any valid secret is discovered, **revoke/rotate it first**, then assess history cleanup according to GitHub's official procedure: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository.

## 2. Source-code licensing and legal provenance

**Finding: NOT CLEARED. No `LICENSE` file, no chosen code license, and no documented coauthor/IP-owner approval.**

| Component | Evidence | Release determination |
|---|---|---|
| Author-written EXP37 notebooks and scripts | Original source in repo; copyright/ownership approvals not documented | Confirm owners, coauthor consent, employer/university obligations, and all external code attribution before selecting a license |
| FPSD images, TIFF/COCO labels, feature caches | Upstream https://github.com/Yanhui-Struggle/FPSD publicly distributes resources, but no express blanket redistribution LICENSE was identified in its inspected root | Keep original data and derivatives out of this repo; link users to upstream; obtain explicit redistribution permission if needed |
| PauliYOLOv8n / Ultralytics | Optional `requirements-full.txt` installs `ultralytics`; original detector weights are excluded | Ultralytics states AGPL-3.0 vs Enterprise terms. Determine whether and how the integrated workflow triggers obligations before selecting a project license or distributing trained models: https://www.ultralytics.com/license |
| Python scientific ecosystem | Dependencies are specified as version ranges, no vendor source included in repo | Review resolved transitive licenses and notices for intended distributions; do not imply a fully audited dependency SBOM |
| Manuscript Figures 1–3 | Repository provides an independently authored Mermaid technical equivalent, not a redistributed PDF figure | Figure rights/publisher policy should be checked if the actual published graphics or publisher PDF are later added |

A code-only artifact can be released separately from FPSD, but code-only visibility is **not itself an exemption** from AGPL or other obligations. Independent legal review may be appropriate if upstream licensing is ambiguous. In particular, do **not** assume MIT or Apache-2.0 automatically covers the complete detector-dependent pipeline.

## 3. Evidence and scientific boundaries

- This repository documents the classically simulated QBloch branch, 18 shared rotation angles, 12-dimensional readout, 8+12 token fusion, and candidate-level verifier evidence.
- The CI synthetic notebook run **does not** rerun the full authorized FPSD data pipeline or reconstruct the original 80 model checkpoints.
- `CITATION.cff` should be updated with **publisher-confirmed** bibliographic information/DOI when available; do not invent the DOI.
- The manuscript includes a code-availability URL; external readers will not be able to access it until the repository is made public.

## 4. Publication decision checklist

- [x] Review all reachable commit-tree filenames for raw imagery/weights/sensitive extensions (26 snapshots).
- [x] Confirm prior CI pattern scan of 82 reachable blob objects passed.
- [x] Confirm no `LICENSE` has been invented or added without owner authorization.
- [x] Keep repository PRIVATE and avoid uploading original dataset, model weights or submitted manuscript PDF.
- [x] Confirm post-enhancement CI passed on commit `c0d2c65` (run 44366594829).
- [ ] Independently run a specialist secrets/entropy scanner and review all alerts.
- [ ] Inspect GitHub advanced security/dependency alert settings and perform version-resolved dependency/SBOM review.
- [ ] Author/coauthor/institutional IP approvals for distributing the source.
- [ ] Decide an enforceable and compatible license strategy for the code and the optional Ultralytics integration; **only then** add an approved LICENSE and notices.
- [ ] Verify dataset and figure redistribution rights for any future assets.
- [ ] Confirm DOI/proceedings details and release tag once available.
- [ ] Obtain explicit final approval before changing repository visibility to PUBLIC.

**Result:** technical screening strengthened and documented, but **public software release remains blocked by the ownership/license decision and a fuller secret/dependency audit**.
