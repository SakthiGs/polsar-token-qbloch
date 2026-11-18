# Repository security and history inspection — updated 18 November 2026

**Repo:** `SakthiGs/polsar-token-qbloch`. **Status: PRIVATE**. See [complete publication licensing and security checklist](PUBLIC_RELEASE_AUDIT_2026-11-18.md).

## Completed inspections

- Enumerated all **26 commits** reachable from the main branch in the GitHub commit listing, and independently fetched all **26 recursive commit trees**. No tree was truncated.
- The current head tree has **43 tracked blobs**; no historical tree contained a file with the reviewed imagery/weights/cache/archive/PDF/credential-key extensions, including `.jpg`, `.png`, `.tif`, `.npz`, `.pt`, `.pdf`, `.zip`, `.pem`.
- GitHub's refs listing contained only `refs/heads/main` and no tag refs on 18 November.
- A complete checkout in GitHub Actions run [44365128038](https://github.com/SakthiGs/polsar-token-qbloch/actions/runs/44365128038) scanned **82 reachable blob objects** for the configured token/key/private-path regex patterns; no matches or oversized skipped blobs. That run also passed **13 scientific/portability unit tests** and the canonical notebook's synthetic smoke test.
- The historical filename scan was strengthened on 18 November 2026 in `scripts/scan_git_history.py`. [CI run 44366594829](https://github.com/SakthiGs/polsar-token-qbloch/actions/runs/44366594829) passed after adding the new sensitive-path regression tests.
- The publicly disclosed content is research architecture, aggregate summary metrics and anonymized hash/provenance records, **not** original FPSD imagery or trained detector weights.

## Remaining security work

The baseline is a custom signature/filename scanner, **not** an independent high-entropy scanner such as Gitleaks. Conduct a specialist scan and human review for secrets, private paths, personal information and copied/proprietary source before going public. Repository GitHub Advanced Security, Dependabot and code-scanning alert settings have not been verified by a suitable connected endpoint.

If real credentials are discovered, **rotate/revoke immediately** before any history rewrite. See https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository.

**Conclusion:** Basic historical artifact/credential screening PASSED. Complete public-release clearance is **not** granted; code ownership, third-party licenses and broader security review remain open.
