# Brief — skill-ab-eval GitHub Pages landing page

## Goal
A single static landing page, served by GitHub Pages, that makes a developer
landing from GitHub/Reddit/HN understand in under 30 seconds what skill-ab-eval
is, why it matters, and how to try it — then click through to the repo. The page
sells the core idea: prove what actually works (skill axis + harness axis) with
real evidence, not vibes.

## Audience
- Developers building Claude Code `SKILL.md` skills who need to prove a skill
  earns its context-window cost.
- Engineers choosing between CLI agents (claude / codex / gemini / agy / openai)
  for a task or domain.
- Open-source browsers who arrived from a README link, a post, or search and
  decide in seconds whether to star, install, or bounce.

## Acceptance criteria (machine-checkable)
1. `docs/index.html` exists, is a single self-contained file (inline CSS + inline
   JS only), and is well-formed HTML5 (`<!DOCTYPE html>`, one `<html lang>`, one
   `<title>`, balanced tags — verified by an HTML parser exit 0).
2. The two axes (skill axis = with_skill vs without_skill; harness axis = which
   CLI is best) are both explained in the first screen / hero region of the page.
3. The page includes copy-paste-accurate install and quickstart commands that
   match `README.md` (the `git clone ... ~/.claude/skills/skill-ab-eval` install
   and at least one `skill-ab-eval task ...` quickstart).
4. The page renders the skill-lift table and the harness leaderboard (the real
   example numbers from `README.md`).
5. The primary call-to-action links to `https://github.com/cskwork/skill-ab-eval`;
   every external `<a target="_blank">` carries `rel="noopener"` (or `noreferrer`).
6. Responsive from 360px to ≥1280px wide with no horizontal overflow at any
   breakpoint (checked at 360 / 768 / 1280).
7. Accessible: semantic landmarks (`header`/`main`/`footer`/`nav`), exactly one
   `<h1>`, body-text color contrast ≥ WCAG AA (4.5:1), all interactive elements
   keyboard-focusable with a visible focus style, and a `prefers-reduced-motion`
   fallback that disables non-essential animation.
8. No emojis anywhere in the page; no em-dash (—) characters in the page copy
   (house rule + taste-skill anti-slop rule).
9. Pure static: no build step, no runtime framework, no external JS dependency
   required to render the page (a self-hosted or system font stack is fine; an
   optional Google Fonts `<link>` is allowed but the page must still render
   readably if it fails).
10. `docs/.nojekyll` exists so GitHub Pages serves the static file as-is without
    Jekyll processing.

## Non-goals
- No backend, no analytics pipeline, no form/email capture, no service worker.
- No multi-page documentation site or blog; one page only.
- No change to the CLI, the Python orchestrator, the runners, or the skill itself.
- No custom domain / DNS work; default `*.github.io` URL is the target.
- No CI/CD change beyond what is strictly needed to serve the page.

## Validation
Demand evidence (lightweight — this is an additive page for an existing
open-source tool the owner explicitly asked to promote, not a net-new product):

- **Explicit pull**: the repo owner (cskwork) directly requested this landing
  page for this repo. Demand is stated, not speculative.
- **Gap**: the repo currently ships only a `README.md`; there is no rendered
  landing surface to link from posts, talks, or the agentskills ecosystem.
- **Discoverability value**: a focused landing page is the standard, low-risk way
  open-source dev tools convert a visitor into an install/star; the asset is
  reusable across every future share (Reddit, HN, conference slides).
- **Downside**: near zero. The page is additive (new `docs/` only), changes no
  existing code, and requires only a one-time GitHub Pages source toggle.

MVP scope = one static page covering: hero (both axes), how-it-works matrix,
what-you-get (real tables), install + quickstart, runners table, verdict guide,
worked example, footer (credits/license/links). Anything beyond one page is a
non-goal for this run.

Decision: GO
