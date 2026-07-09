---
inclusion: always
---

# Keep SETUP.md in sync with every merge

**Rule:** Whenever a change is prepared for merge (a commit/PR into `main`),
`SETUP.md` MUST be updated in the same change if the change affects anything a
user or operator needs to know to install, configure, run, or deploy the project.

## When SETUP.md must be updated
Update `SETUP.md` if the change touches any of:
- New or changed **commands** (build, install, run, deploy, uninstall).
- New or changed **environment variables** (e.g. `DIYA_API_BASE`, `ADMIN_KEY`,
  `DIYA_DATA_DIR`, `DIYA_PYTHON`, `DIYA_CALIBRATION_SCRIPT`).
- New **pages/endpoints** or user-facing flows (e.g. `/admin`, `/p/<token>`,
  registration/login steps).
- New **columns/inputs** an operator provides (e.g. roster sheet columns).
- **Deployment** changes (Render settings, branch, `.deb` rebuild/reinstall steps,
  Docker preview).
- Anything that changes **how the kiosk, server, or registration site is set up**.

## How to apply it
1. Make the code/feature change.
2. In the **same branch/PR**, add or edit the relevant `SETUP.md` section(s) so the
   instructions match the new behavior. Prefer updating an existing section over
   duplicating; add a new numbered/lettered section only when needed.
3. If a feature requires **two deploys** (e.g. server redeploy + kiosk `.deb`
   rebuild), state both explicitly.
4. If a change is purely internal (refactor, tests, non-user-facing) and needs no
   doc update, that's fine — but say so in the PR description so it's a conscious
   decision, not an omission.

## Related docs
When the change is significant, also consider whether `PROJECT.md` (overview,
version history, branch map) and `FAQ.md` need matching updates — but `SETUP.md`
is the required one per this rule.
