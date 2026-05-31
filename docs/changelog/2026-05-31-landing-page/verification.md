# Verification — adversarial re-run + QA

Verifier read-scope: claims.md + code only (no plan rationale). Builder (Designer)
!= Verifier. All commands re-run by a fresh adversarial context; QA measured with
real Chrome (puppeteer-core mobile emulation) and WCAG luminance math.

## Per-claim verdicts
claim S1: GREEN — run-to-prove "ALL CHECKS PASS" + "JS OK" (exit 0). Re-run after both
  QA fix rounds: still ALL PASS, inline JS `node --check` OK. One h1, lang set, all
  landmarks, both axes, verbatim install line, both result tables (+0.50/+0.38),
  github CTA href, prefers-reduced-motion + responsive media queries, aria-live,
  zero em-dash, zero en-dash, zero emoji, target=_blank(7)==rel=noopener(7).
claim S2: GREEN — `test -f docs/.nojekyll` -> NOJEKYLL_OK (exit 0).

## QA (black-box, running page)
Rendered docs/index.html in headless Chrome via puppeteer-core with true mobile
emulation (isMobile, deviceScaleFactor 2) at 360/768/1280px. Final full-page
evidence committed under `qa/` (m-after2-360.png mobile, m-after2-1280.png desktop;
intermediate/baseline renders were left uncommitted to keep the repo lean).

- Horizontal overflow (document.scrollWidth vs clientWidth):
  - 360px: 360 == 360 -> 0px overflow (was 588 vs 360 = 228px before the fix)
  - 768px: 768 == 768 -> 0px
  - 1280px: 1280 == 1280 -> 0px
  No section content clipped; hero heading wraps, axis tags wrap, data tables and
  code blocks scroll within their own blocks (visually confirmed on the 360 + 1280
  full-page captures).
- WCAG AA contrast (computed from the file's color tokens, worst-case background):
  text-primary 14.09:1, text-secondary 5.64:1, text-muted 4.84:1, accent 9.18:1 —
  all >= 4.5:1 AA. (text-muted was 2.35:1 before the fix; raised to #808c99.)
- Reduced motion: `@media (prefers-reduced-motion: reduce)` disables animation +
  forces `.reveal` visible. Present (code-verified).
- Keyboard a11y: `:focus-visible` outline rule present; copy buttons are real
  `<button>`s with an `aria-live` status region.
- Single `<h1>` at every width (puppeteer: h1=1 on 360/768/1280).

Two QA-fail rewinds to Build were performed and re-verified (logged in README):
1. 228px mobile horizontal overflow — root cause CSS grid `min-width:auto` trap on
   `.install-grid` items holding `white-space:pre` code blocks. Fixed with
   `min-width:0` on grid children + `overflow-wrap:break-word` + tables made
   `display:block; overflow-x:auto`. Re-verified: 0 overflow at 360/768/1280.
2. `--text-muted` AA contrast failure (2.35-2.72:1) on 19 text usages incl. table
   headers, footer links, copy button. Fixed `#4d5a66` -> `#808c99`. Re-verified:
   4.84:1 worst case, AA pass.

## Coverage
Acceptance criteria (brief.md) mapped to evidence:
- AC1 single self-contained well-formed HTML5, one h1, lang: S1 parse + h1=1 — GREEN
- AC2 both axes in hero: with_skill/without_skill + 5 harness tags in hero — GREEN
- AC3 install + quickstart match README (verbatim): S1 string checks — GREEN
- AC4 skill-lift table + leaderboard, real numbers: S1 (+0.50/+0.38, ranks) — GREEN
- AC5 primary CTA href + rel=noopener on every target=_blank: S1 (7==7) — GREEN
- AC6 responsive 360..1280, no horizontal overflow: QA puppeteer 0px all — GREEN
- AC7 a11y (landmarks, one h1, AA contrast, focus-visible, reduced-motion): QA — GREEN
- AC8 no emoji, no em-dash: S1 raw-byte scan — GREEN
- AC9 pure static, no build, no runtime framework: S1 (no script src) — GREEN
- AC10 docs/.nojekyll present: S2 — GREEN
Priority Rules (domain checklist) checked: one message + one primary action, show-not-tell
(real tables/commands), static performance, accessible-by-default, mobile-first, brand
voice (no slop/emoji/em-dash), every claim links to proof (repo/examples/spec), progressive
disclosure fold order, minimal dependencies (Google Fonts optional w/ fallback chain),
credit + MIT visible — all GREEN.

Not covered:
- Live clipboard write in a real secure context (HTTPS/localhost) — JS is syntactically
  valid and follows the standard navigator.clipboard + aria-live pattern, but no automated
  test exercises the actual copy. Low risk.
- Cross-browser rendering on non-Chromium engines (Safari/Firefox) — only Chrome (Blink)
  was rendered. The page uses standard, widely-supported CSS/JS. Low risk.
- Google Fonts offline-failure appearance — confirmed via the font-family fallback chain in
  CSS, not via an actual network-blocked render. Low risk (system fallback fonts declared).
- Full Lighthouse/axe automated audit not run — replaced by measured WCAG contrast +
  structural landmark/focus/reduced-motion checks. Medium-to-low residual risk.

Regression tests: none — verify-only run for a new, additive static page; no pre-existing
failing test was fixed. The repo's own CI-equivalent suite is re-run at the delivery gate
(python tests/validate_evals.py + py_compile scripts/run_eval.py + bash -n on runners/*.sh
and bin/skill-ab-eval) to confirm the additive docs/ change breaks nothing.

verdict: GREEN
