# Harness axis — comparing CLI agents

`skill-ab-eval` evaluates along two independent axes:

1. **Skill axis** — does loading a `SKILL.md` change behavior? (`with_skill` vs `without_skill`)
2. **Harness axis** — which CLI agent does the task best? (`claude` vs `codex` vs `gemini` vs `agy` vs `openai`)

Run them together and you answer questions like: *"This skill lifts Claude Code a
lot but does nothing for Codex"* or *"For this domain, gemini beats everyone even
without the skill."*

## Why per-harness skill lift matters

A skill is not universally good or bad — its lift depends on the host model's
defaults. A convention the base model already follows shows ~0 lift; a convention
it ignores shows large lift. Measuring per harness tells you *where* the skill
earns its context budget.

## The harnesses

| runner   | CLI / API        | strengths (per cc-agent-call)                         |
|----------|------------------|-------------------------------------------------------|
| `claude` | Claude Code      | code editing, planning, large-context analysis        |
| `codex`  | OpenAI Codex CLI | image gen, `codex review`, tight shell loop           |
| `gemini` | Gemini CLI       | Google-grounded reasoning, long context               |
| `agy`    | Antigravity      | Google Search grounding, scientific DBs               |
| `openai` | OpenAI HTTP API  | deterministic, cheap, key-based (CI-friendly)         |

This mirrors [cc-agent-call](https://github.com/cskwork/cc-agent-call), which
delegates work between these same CLIs. Where cc-agent-call *routes* to the best
harness, skill-ab-eval *measures* which harness is best — for your task, with your
skill.

## Relationship to cc-agent-call

- cc-agent-call: "from inside Claude Code, hand this off to Codex/agy/kiro/..."
  (production delegation).
- skill-ab-eval: "run this task through all of them and grade the results"
  (evaluation). The runner adapters in `../runners/` are the same shell-out
  pattern cc-agent-call uses, repurposed as measurable, comparable cells.

You can install cc-agent-call's delegation skills and skill-ab-eval side by side:
use skill-ab-eval to decide *which* harness a cc-agent-call skill should prefer.

## CLI usage

```bash
# which harnesses are usable right now?
skill-ab-eval runners

# ad-hoc task, no skill — pure harness comparison on a task you give
skill-ab-eval task "Explain async/await to a junior, in 5 bullet points." \
  --runners claude,codex,gemini --judge claude --trials 2

# ad-hoc task WITH a skill — skill lift x harness, in one shot
skill-ab-eval task "Write a git commit message for the staged diff." \
  --skill examples/conventional-commit \
  --assert "Subject line is 50 characters or fewer." \
  --assert "Ends with a 'Refs:' footer." \
  --runners claude,codex --judge claude

# a full evals suite across harnesses
skill-ab-eval run examples/conventional-commit --runners claude,gemini --judge claude
```

Output: a `skill-ab-eval-workspace/<name>/iteration-1/` with per-cell artifacts,
`results.json`, and a `report.md` containing the skill-lift table and the harness
leaderboard.

## Judge choice

Any runner can judge. Defaults to `claude`. For neutrality, prefer a judge that
isn't one of the harnesses under test when you can — or accept the small home-field
bias and report it. The judge grades each answer independently against the
assertions, so it scales to many harnesses without pairwise blowup.
