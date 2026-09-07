# conventional-commit — committed eval results

Two real runs of `skill-ab-eval` against the `conventional-commit` skill, kept as
receipts. Both are genuine model outputs graded by a real judge — nothing staged.
Together they show the same skill measuring **very differently depending on the
harness's ambient context**, which is exactly the point of the tool.

## 1. `agent-native/` — fresh-context subagents (skill axis)

Each cell ran in a fresh Claude subagent (Task/Agent tool), so the baseline did
**not** inherit any global commit conventions. The skill shows a clear lift:

| eval        | with | without | lift  |
|-------------|------|---------|-------|
| feat-rate-limit | 1.00 | 0.75 | +0.25 |
| fix-npe         | 0.67 | 0.33 | +0.33 |
| **overall**     | **0.86** | **0.57** | **+0.29 → clear positive** |

The harness was honest: `with_skill` still slipped once (used `feat` instead of
`fix` on the bugfix), so the win is real but not perfect. See
[`agent-native/report.md`](agent-native/report.md).

## 2. `cli-orchestrator/` — live multi-CLI run (skill axis × harness axis)

`scripts/run_eval.py` driving real CLIs (`claude -p`, `gemini -p`), judged by
`claude`, one trial:

| harness | with | without | lift  | verdict             |
|---------|------|---------|-------|---------------------|
| claude  | 1.00 | 1.00    | +0.00 | no measurable effect |
| gemini  | 0.00 | 0.00    | +0.00 | no measurable effect |

Read honestly:

- **claude lift = 0** is a *finding, not a failure*. `claude -p` loaded the user's
  global `CLAUDE.md`, which already mandates Conventional Commits + a ticket
  footer — so the baseline was already as good as the skill. The skill is
  **redundant on this harness**: its content is already-default behavior. That's
  precisely the "dead weight in the context window" signal skill-ab-eval exists to
  catch.
- **gemini = 0 on both sides** is an *integration artifact*: in this headless,
  nested environment `gemini -p` returned a greeting ("I'm ready. Please provide
  your instructions.") instead of answering. The leaderboard surfaces that this
  harness couldn't do the task **in this setup** — useful to know, but not a fair
  benchmark of Gemini's true ability. On a clean shell the gemini adapter answers
  normally. See the raw `answer.md` files to verify.

See [`cli-orchestrator/iteration-1/report.md`](cli-orchestrator/iteration-1/report.md).

## Takeaway

Same skill, two harnesses, opposite verdicts — both correct. The skill genuinely
helps a model with no commit conventions loaded (+0.29), and genuinely adds nothing
to a model that already has them (0.00). "Does my skill work?" has no answer
without naming the harness and its ambient context. That's the measurement
skill-ab-eval makes cheap.
