# Run — GitHub Pages landing page for skill-ab-eval

Objective: "make landing page for this repo skill host in github pages"
Mode: GREENFIELD (new user-facing site) + UI/UX overlay (taste-skill v2 authority).
Target repo: cskwork/skill-ab-eval (this folder's repo).
Date: 2026-05-31.

## Decisions & narrative (audit log)
- Mode detected GREENFIELD; deliverable ships visual look-and-feel, so the UI/UX
  overlay is loaded (Design Read + dials at Plan, Designer at Build, taste
  Pre-Flight at QA).
- Ambiguity resolved up front: "this repo" was undefined (cwd is not a git repo).
  Asked one clarifying question; user selected `cskwork/skill-ab-eval`.
- Deploy mechanism chosen: GitHub Pages from `main` branch `/docs` folder. Reason:
  the page is a single static file with no build step, so `/docs` is the simplest,
  most transparent source. `docs/.nojekyll` disables Jekyll so the raw HTML serves
  as-is. The vault for this run lives under `docs/changelog/...`; it is harmless if
  publicly served (markdown, unlinked) and is the intended browsable changelog.
- One-time human/owner action required at Deliver: set repo Settings → Pages →
  Source = "Deploy from a branch", branch `main`, folder `/docs`. `gh` is
  authenticated as `cskwork` with push, so this can optionally be enabled via the
  Pages API on explicit confirmation (outward-facing action).

## Priority Rules (advisory — landing page / dev-tool frontend domain)
1. One hero message, one primary action. Clarity beats cleverness.
2. Show, do not tell. Real result tables and real commands, never adjectives.
3. Performance is UX. Static, no heavy framework, fast first paint.
4. Accessible by default. Semantic HTML, AA contrast, keyboard, reduced-motion.
5. Mobile-first responsive. No horizontal scroll at 360px.
6. Hold the brand voice. Terminal/evidence aesthetic, no slop, no emojis, no em-dashes.
7. Every claim links to proof: repo, examples, the agentskills spec.
8. Progressive disclosure. Fold order: what -> why -> how -> install -> details.
9. Minimal dependencies. Single file, no build, GitHub Pages friendly.
10. Credit and license visible. MIT, inspirations (agent-skills-eval), author.

## Skips logged
- Heavy market research skipped at Validate: additive page for an existing tool on
  explicit owner request; demand is stated, downside near zero. GO recorded.

## Phase log
- Intake: brief.md written with 10 machine-checkable acceptance criteria. DONE.
- Validate: Decision: GO recorded; validate-gate.sh exit 0. DONE.
- Plan: plan.md frozen (Design Read + 3 dials + Architecture + Contracts + slices); plan_hash recorded. DONE.
- Human Feedback: two briefs written; human approved Build; Pages-enable = gh API (owner choice); human-feedback-gate.mjs exit 0. DONE.
- Build: Designer produced docs/index.html (single self-contained file) + docs/.nojekyll. DONE.
- Verify (adversarial): both claims GREEN, 11 acceptance targets evidenced. DONE.
- QA (taste pre-flight): found + fixed two defects via Build rewinds, re-verified:
  - REWIND 1 (build cycle 1): 228px horizontal overflow at true 360px mobile (puppeteer-core,
    isMobile, dsf 2). Root cause: CSS grid `min-width:auto` trap on `.install-grid` items holding
    `white-space:pre` code blocks. Fix: `min-width:0` on grid children + `overflow-wrap:break-word`
    + tables `display:block;overflow-x:auto`. Re-verified 0 overflow at 360/768/1280.
  - REWIND 2 (in build cycle 1): `--text-muted #4d5a66` failed WCAG AA (2.35-2.72:1) across 19 text
    usages. Fix: `#808c99` (4.84-5.60:1, AA pass), hierarchy preserved.
  Note: headless Chrome `--screenshot` lays out a 360px window at ~482px (no mobile emulation),
  which initially masked the bug; puppeteer-core device emulation gave true-360 ground truth.
- Committee (architect + security + code-reviewer, parallel):
  - architect: APPROVE. security-reviewer: APPROVE. code-reviewer: CHANGES (2 HIGH a11y + WCAG-A skip-link).
  - REWIND 3 (build cycle 2): fixed copy-button aria-label restore, `role="group"` on `.hero-axes`,
    added skip-to-content link (WCAG 2.4.1 A), removed misleading `role="img"` from `.matrix-flow`,
    moved the `aria-live` region to top of `<main>`. Re-verified: S1 all pass, 0 overflow retained.
  - Accepted (non-blocking, logged): Google Fonts has no SRI (GitHub Pages header constraint; security
    APPROVE); no `og:image` (needs a raster asset; brief marked optional); `!important` on `.nav-github`
    + scattered inline styles (cosmetic); result numbers are illustrative and carry an in-page note;
    `--positive` shares the accent hue (intentional); mobile nav hides section anchors (scroll still works).
- Deliver: DONE.
  - plan_hash matched; delivery-gate.sh exit 0 (artifacts + GREEN + completeness contract + GO +
    repo CI-equivalent suite green: validate_evals.py / py_compile / bash -n).
  - committee: architect APPROVE, security APPROVE, code-reviewer APPROVE (after the a11y rewind).
  - committed f5c212f, pushed to origin/main (user-approved direct push).
  - GitHub Pages enabled via gh API (source main /docs); build status "built", HTTPS enforced.
  - Live: https://cskwork.github.io/skill-ab-eval/ (HTTP 200, title verified).
  - Repo About: homepage + description updated to include the Pages link (user request).

## Post-delivery enhancements (user-approved follow-up)
- Open Graph social card: added `docs/og.png` (1200x630, rendered from
  `og-card.html` via puppeteer to match the site aesthetic) + og:image / og:url /
  og:type / twitter:card=summary_large_image / twitter:image meta in index.html.
  Fixes the previously-blank social unfurl (the LOW finding from code review).
- Removed the three unnecessary `!important` on `.nav-github` (cascade unchanged;
  `.nav-github` already out-specifies `.nav-links a`).
- CSP meta intentionally NOT added: the page is inline-CSS+JS, so a meaningful CSP
  would require `'unsafe-inline'` for both style-src and script-src, giving little
  real protection while risking breakage. Google Fonts SRI remains a GitHub Pages
  header constraint (security review APPROVE). Left as accepted.
