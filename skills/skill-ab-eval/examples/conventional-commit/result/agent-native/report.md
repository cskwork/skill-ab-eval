# skill-ab-eval report: conventional-commit (agent-native mode)

- mode: agent-native — each cell ran in a **fresh Claude subagent** (Task/Agent tool)
- judge: claude, blind (neutral labels, randomized order), independent grading
- trials: 1 per side | metric: assertion pass rate

## Skill lift

| eval            | with_skill | without_skill | lift  | verdict        |
|-----------------|------------|---------------|-------|----------------|
| feat-rate-limit | 1.00 (4/4) | 0.75 (3/4)    | +0.25 | clear positive |
| fix-npe         | 0.67 (2/3) | 0.33 (1/3)    | +0.33 | clear positive |
| **overall**     | **0.86 (6/7)** | **0.57 (4/7)** | **+0.29** | **clear positive** |

## What the harness caught

- **without_skill** missed the house rules the base model doesn't guess: it wrote
  `Refs PROJ-481` (no colon) on feat-rate-limit, and a 67-char subject with a bare
  `PROJ-512` (no `Refs:` footer) on fix-npe.
- **with_skill** fixed those — but was **not perfect**: on fix-npe it used type
  `feat` instead of `fix`, failing one assertion. The tool reports the real lift,
  not a rigged win.

## Caveats (honest)

- One trial per side → directional, not significant. Raise trials for confidence.
- The "baseline" here is a fresh subagent that did **not** inherit the user's
  global commit conventions, so the skill had room to show lift. Compare with the
  CLI-orchestrator run, where `claude -p` loaded the user's global rules and the
  same skill showed **no** lift — baseline depends on the harness's ambient context.
