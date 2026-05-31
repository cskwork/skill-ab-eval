# Plan — skill-ab-eval GitHub Pages landing page (FROZEN)

Frozen on 2026-05-31. Build implements this; it does not redesign it.

## UI/UX overlay (taste-skill v2 authority)

**Design Read (one line):** Evidence over vibes — a precise, terminal-inspired
technical landing where real result tables and real commands do the selling, not
adjectives.

**Three dials (frozen with the plan):**
- `DESIGN_VARIANCE`: medium-high. Anti-generic, anti-default. A distinctive
  terminal / IDE aesthetic, not a stock SaaS template. Still legible and credible
  to skeptical developers.
- `MOTION_INTENSITY`: low. Subtle on-scroll reveals and hover affordances only;
  fully disabled under `prefers-reduced-motion`. Developers distrust flashy.
- `VISUAL_DENSITY`: medium-high. Technical audience expects density: show the real
  matrix, real tables, real commands. Not a sparse one-claim-per-screen page.

**Design system vs aesthetic:** a small custom token system (CSS custom properties
for color, type scale, spacing, radius) realizing a dark terminal/evidence
aesthetic — near-black canvas, one saturated accent reserved for CTAs and the
positive verdict, monospace for code/data, a clean sans for prose. Light theme is
an optional `prefers-color-scheme` add-on, not required for MVP.

Anti-slop hard rules carried into Build: no emojis, no em-dashes in copy, no
lorem/placeholder, no div-mockups standing in for real content. The matrix diagram
and tables are real CSS/SVG/HTML content, not images of content.

## Architecture
- **Stack:** pure static. One self-contained file `docs/index.html` with an inline
  `<style>` and a small inline `<script>` (copy-to-clipboard + optional scroll
  reveal). No build step, no framework, no runtime npm/CDN JS dependency.
- **Fonts:** system/monospace stack by default; an optional Google Fonts `<link>`
  for a display/mono face is allowed only if the page still renders readably when
  the link fails (graceful fallback in the font-family chain).
- **Favicon:** inline SVG data URI (keeps the page single-file, zero extra request).
- **Deploy:** GitHub Pages, source = `main` branch `/docs` folder. `docs/.nojekyll`
  disables Jekyll so the raw HTML serves verbatim. Site URL once enabled:
  `https://cskwork.github.io/skill-ab-eval/`.
- **No backend, no analytics, no service worker** (per non-goals).

## Contracts

**File layout (this run writes only these):**
- `docs/index.html` — the landing page (single file).
- `docs/.nojekyll` — empty marker.
- `docs/changelog/2026-05-31-landing-page/` — this run's vault (already present).

**Content sections, in fold order (progressive disclosure):**
1. Header / sticky nav: wordmark + anchor links + GitHub link.
2. Hero: H1 "Prove what actually works", one-sentence subhead, the **two axes**
   (skill axis: with_skill vs without_skill; harness axis: which CLI is best),
   dual CTA (primary = GitHub repo, secondary = jump to Quickstart).
3. How it works: the matrix diagram (one task -> harness x {with,without} -> fresh
   context per cell -> judge x N trials -> skill-lift + leaderboard), rendered as
   styled HTML/SVG.
4. What you get: the **skill-lift-by-harness table** and the **harness leaderboard**
   using the real README example numbers, plus the workspace artifact tree.
5. Install + Quickstart: copy-paste blocks, verbatim-consistent with README
   (Claude Code skill install + standalone CLI + at least one `skill-ab-eval task`).
6. Runners table: claude / codex / gemini / agy / openai with auth notes.
7. Reading the verdict: the lift -> verdict thresholds table.
8. Worked example: the conventional-commit two-harness opposite-verdict story,
   linking to `examples/conventional-commit/result/`.
9. Footer: credits (inspired by agent-skills-eval, harness axis on cc-agent-call),
   agentskills.io spec link, MIT license, author cskwork, repo link.

**Accessibility contract:** exactly one `<h1>`; `header`/`nav`/`main`/`footer`
landmarks; body text contrast >= 4.5:1; visible `:focus-visible` style on every
interactive element; copy buttons keyboard-operable with an `aria-live` status;
`@media (prefers-reduced-motion: reduce)` removes non-essential animation.

**Content-accuracy contract:** install command, quickstart commands, runners table,
verdict thresholds, and the two result tables are consistent with `README.md` and
`SKILL.md` (no invented numbers, no contradicting flags).

**Deploy contract:** after the owner sets Pages source to main `/docs`, the site
serves `docs/index.html` at the project Pages URL; `.nojekyll` present.

## Slice plan (each independently testable)

| Slice | What | Files | Acceptance check (run-to-prove) |
|---|---|---|---|
| **S1** | Single-file landing page: semantic structure + all 9 content sections + token-based design system + responsive (360/768/1280) + a11y + reduced-motion + copy-to-clipboard | `docs/index.html` | Parses as well-formed HTML5 with exactly one `<h1>` and a `lang` attribute (HTML parser, exit 0); grep confirms presence of both axis terms, the `git clone ... ~/.claude/skills/skill-ab-eval` install line, the `github.com/cskwork/skill-ab-eval` href, both result tables (skill-lift + leaderboard), a `prefers-reduced-motion` media query, and a responsive `max-width`/`@media` query; grep confirms ZERO emoji and ZERO em-dash (—) in the file |
| **S2** | Deploy scaffolding | `docs/.nojekyll` | `test -f docs/.nojekyll` exits 0 |

Slice-size note (logged exception): a single-file landing page legitimately exceeds
the ~500-line slice guideline because keeping CSS/JS inline is the simplest,
no-build, GitHub-Pages-friendly form (Priority Rule 9). The page stays one cohesive
purpose, so the cohesion-over-line-count house rule governs. Estimated ~450-650
lines for `index.html`.

## Regression / no-break contract
This run adds files under `docs/` only and changes no existing code. The repo's own
CI-equivalent suite must still pass at Deliver:
`python tests/validate_evals.py && python -m py_compile scripts/run_eval.py && for f in runners/*.sh bin/skill-ab-eval; do bash -n "$f"; done`

## Human Feedback

### Plain-language brief
I want to add a one-page website for the skill-ab-eval project so that anyone who
hears about it can open a clean page, instantly understand what the tool does, and
decide to try it. The page lives inside the project under a `docs` folder and is
published for free with GitHub Pages, so there is no server to run and nothing to
maintain. It will explain the two things the tool proves (does a skill actually
help the AI, and which AI command-line tool is best for a task), show the real
result tables the tool produces, and give the exact copy-and-paste commands to
install and run it. It changes none of the existing program code; it only adds the
new page. After it is committed, you flip one switch in the repository settings to
turn the page on.

### Technical brief
The deliverable is a single self-contained file, `docs/index.html`, with its CSS
and a tiny bit of JavaScript written inline, plus an empty `docs/.nojekyll` marker
file. No build tools, no frameworks, no external libraries are required, which is
what makes it safe and trivial to host on GitHub Pages straight from the `/docs`
folder of the `main` branch.

- Touch points: new files only — `docs/index.html`, `docs/.nojekyll`. The run's
  notes live in `docs/changelog/2026-05-31-landing-page/`. No edits to `scripts/`,
  `runners/`, `bin/`, `SKILL.md`, or `README.md`.
- Content sections (in order): sticky nav, hero with the two axes and a call to
  action, a how-it-works matrix diagram, the skill-lift table and harness
  leaderboard, install plus quickstart command blocks, the runners table, the
  verdict-reading table, the worked example, and a footer with credits and license.
  All commands and numbers are copied to match `README.md`, so the page never
  states anything the project does not actually do.
- Design: a dark, terminal-inspired look built on CSS variables (a small set of
  color/spacing/type tokens). Subtle motion only, and it turns off automatically
  for visitors who prefer reduced motion. The page is responsive from a 360px phone
  up to a wide desktop, uses semantic landmark tags, meets WCAG AA text contrast,
  and keeps every button keyboard-accessible.
- How I will prove it: an HTML parser confirms the file is well-formed with one
  `<h1>`; text searches confirm the required commands, links, both tables, the
  reduced-motion rule, and the responsive rule are present, and that there are no
  emojis or em-dashes. The project's existing test/lint commands are re-run to
  confirm nothing else broke. A fresh reviewer re-runs all of these from a clean
  checkout, and a design pre-flight checks accessibility and reduced-motion.
- Deploy step (yours, one time): repository Settings -> Pages -> Source = "Deploy
  from a branch" -> branch `main`, folder `/docs`. Because the `gh` CLI is signed in
  as `cskwork` with push access, I can optionally enable this for you via the GitHub
  Pages API, but only if you explicitly say so (it is an outward-facing change).
- Risks: very low. The page is additive and static. The only real failure mode is a
  content drift between the page and the README, which the accuracy checks above
  guard against. Publishing makes the page publicly visible at the `*.github.io`
  URL; the vault changelog under `docs/` would also be publicly reachable (harmless
  markdown, unlinked from the page).

### Terms
- GitHub Pages: GitHub's free static-website hosting that serves files straight from
  a branch/folder of a repository, with no server to run.
- `.nojekyll`: an empty marker file that tells GitHub Pages to skip its Jekyll
  processing step and serve the raw HTML exactly as written.
- Skill axis (with_skill vs without_skill): comparing the AI's output when a
  `SKILL.md` is loaded against when it is not, to measure whether the skill helps.
- Harness axis: comparing different AI command-line tools (claude, codex, gemini,
  agy, openai) on the same task to see which performs best.
- Skill lift: the difference in pass rate or score between the with-skill and
  without-skill runs; positive lift means the skill helped.
- WCAG AA contrast: an accessibility standard requiring text to have at least a
  4.5:1 brightness contrast against its background so it is readable.
- `prefers-reduced-motion`: a browser/OS setting that lets a visitor ask sites to
  minimize animation; the page honors it by disabling non-essential motion.

### Approval request
Approve Build, request changes, or stop. No file under the source tree (outside this
vault) will be written until you approve.
