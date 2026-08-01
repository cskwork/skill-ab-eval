<p align="center"><img src="logo.png" width="120" alt="logo" /></p>

# skill-ab-eval

**Prove what actually works — for any task, in any domain.**

Two questions, one evaluation harness, real evidence:

1. **Skill axis** — does loading a `SKILL.md` change the agent's behavior, or is it
   dead weight in the context window? (`with_skill` vs `without_skill`)
2. **Harness axis** — for *this* task, which CLI agent is best? (`claude` vs
   `codex` vs `gemini` vs `agy` vs an OpenAI-compatible API)

Run them separately or crossed, on a skill's evals or on **an ad-hoc task you
type**. A judge grades every output against your assertions, repeated over trials.
You get a **skill-lift table** and a **harness leaderboard** — not vibes.

```
        one task (a skill's eval, or one you type)
                        │
     matrix: harness × {with_skill, without_skill}     ← each cell = a FRESH context
   claude·codex·gemini·agy·openai   ×   with / without
                        │
                  judge (any harness), × N trials
                        ▼
     skill-lift per harness   +   harness leaderboard
```

It's an agent-native take on
[`agent-skills-eval`](https://github.com/darkrishabh/agent-skills-eval) (same
`evals.json` and with/without model), wired to the multi-CLI delegation pattern of
[`cc-agent-call`](https://github.com/cskwork/cc-agent-call): where cc-agent-call
**routes** work to the best CLI, this **measures** which CLI is best.

## Why

You ship a `SKILL.md` and assume the agent is better. You pick a CLI and assume
it's the right one. The hard part is *proving* either. This is the proof — and
**fresh, isolated context per cell** is the trick: the only variables are the
harness and whether the skill is loaded. Reuse a context and the skill leaks into
the baseline, silently invalidating the result.

## Install

### Claude Code (and `~/.claude/skills` agents)

```bash
git clone https://github.com/cskwork/skill-ab-eval ~/.claude/skills/skill-ab-eval
```

Then `/skill-ab-eval`, or ask *"does my X skill actually do anything?"* /
*"which CLI is best at Y?"* and it triggers.

### As a standalone CLI

```bash
git clone https://github.com/cskwork/skill-ab-eval && cd skill-ab-eval
export PATH="$PWD/bin:$PATH"     # optional
skill-ab-eval runners            # list usable harnesses
```

Needs `bash` + `python3` and at least one of `claude`, `codex`, `gemini`, `agy`,
or `OPENAI_API_KEY`. No pip install — stdlib only.

## Quickstart

```bash
# compare CLIs on a task you give (no skill, any domain)
skill-ab-eval task "Explain async/await to a junior in 5 bullets." \
  --runners claude,codex,gemini --judge claude --trials 2

# does a skill help — and on which harness?
skill-ab-eval task "Write a git commit message for the staged diff." \
  --skill examples/conventional-commit \
  --assert "Subject line is 50 characters or fewer." \
  --assert "Ends with a 'Refs:' footer." \
  --runners claude,codex --judge claude

# a whole evals suite across harnesses
skill-ab-eval run examples/conventional-commit --runners claude,gemini --judge claude
```

Inside Claude Code you can also run the **agent-native** mode (fresh subagents, no
API keys) — see `SKILL.md`.

## What you get

`skill-ab-eval-workspace/<name>/iteration-1/`:

- `report.md` — skill-lift table + harness leaderboard
- `results.json` — every cell, metric, judge, trials
- `<eval-id>/<runner>/<side>/trial-N/{answer.md,judge.json}` — full receipts

```
## Skill lift by harness
| harness | with | without | lift | verdict        |
|---------|------|---------|------|----------------|
| claude  | 1.00 | 0.50    | +0.50| clear positive |
| codex   | 1.00 | 0.62    | +0.38| clear positive |

## Harness leaderboard (with skill)
| rank | harness | score |
|------|---------|-------|
| 1    | claude  | 1.00  |
| 2    | codex   | 1.00  |
```

## Reading the verdict

| lift (pass-rate / score delta) | verdict |
|--------------------------------|---------|
| ≥ +0.20                        | **clear positive** — the skill helps |
| +0.05 … +0.20                  | marginal — directional |
| −0.05 … +0.05                  | **no measurable effect** — dead weight |
| ≤ −0.05                        | **negative** — the skill hurts |

A few trials is *directional*, not statistically significant — raise `--trials`.
"No effect" is a real result: the skill is already-default, never triggers, or too
vague to act on. Per-harness differences are real too — a skill can lift Claude and
do nothing for Codex.

## Runners (the harness axis)

| runner | CLI / API | auth |
|--------|-----------|------|
| `claude` | Claude Code (`claude -p`) | claude login / `ANTHROPIC_API_KEY` |
| `codex` | OpenAI Codex (`codex exec`) | codex login / `OPENAI_API_KEY` |
| `gemini` | Gemini CLI (`gemini -p`) | gemini login |
| `agy` | Antigravity (`agy -p`) | `agy install` + Google sign-in |
| `openai` | OpenAI HTTP API | `OPENAI_API_KEY` |

Add your own harness by dropping a `runners/<name>.sh` (prompt on stdin → text on
stdout). See [`runners/README.md`](runners/README.md) and
[`reference/harnesses.md`](reference/harnesses.md).

## Eval format

`evals/evals.json`, compatible with the
[agentskills.io spec](https://agentskills.io/specification). Assertions are atomic
binary claims — they *are* the score. See
[`reference/eval-schema.md`](reference/eval-schema.md).

## Worked example (real, committed results)

[`examples/conventional-commit`](examples/conventional-commit) enforces non-default
commit rules (≤50-char subject, mandatory `Refs:` footer). Two real runs are
committed under
[`examples/conventional-commit/result/`](examples/conventional-commit/result) — and
they disagree, on purpose:

- **agent-native** (fresh subagents, no global rules): skill shows **+0.29 lift,
  clear positive** — and the harness honestly notes `with_skill` still slipped once.
- **cli-orchestrator** (`claude -p` + `gemini -p`): on claude the skill shows
  **0.00 lift** because the user's global `CLAUDE.md` already mandates the same
  conventions — the "dead weight" signal. gemini returned a non-answer in the
  headless nested setup, which the leaderboard surfaces.

Same skill, two harnesses, opposite verdicts — both correct. "Does my skill work?"
has no answer without naming the harness. See
[`result/README.md`](examples/conventional-commit/result/README.md).

## Relationship to cc-agent-call

[cc-agent-call](https://github.com/cskwork/cc-agent-call) delegates work between
CLIs in production; skill-ab-eval *measures* which CLI to prefer. Same shell-out
pattern (`runners/` mirrors cc-agent-call's adapters), opposite direction. Install
both: evaluate here, route there.

## Credits

Inspired by [`darkrishabh/agent-skills-eval`](https://github.com/darkrishabh/agent-skills-eval)
and the [agentskills.io](https://agentskills.io) standard; harness axis built on
[`cskwork/cc-agent-call`](https://github.com/cskwork/cc-agent-call). MIT licensed.
