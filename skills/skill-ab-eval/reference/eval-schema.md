# Eval schema (`evals/evals.json`)

Compatible with the [agentskills.io specification](https://agentskills.io/specification).
A skill is evaluable when its directory contains both `SKILL.md` and
`evals/evals.json`.

## Top level

| field        | type   | required | meaning |
|--------------|--------|----------|---------|
| `skill_name` | string | yes      | Must match the target skill's `name`. |
| `evals`      | array  | yes      | One or more eval objects (below). |

## Eval object

| field             | type     | required | meaning |
|-------------------|----------|----------|---------|
| `id`              | string   | yes      | Stable slug, unique within the file. Used in artifact paths. |
| `name`            | string   | no       | Human label. |
| `prompt`          | string   | yes      | The task given to BOTH runners. Keep it neutral. |
| `files`           | string[] | no       | Paths relative to the skill dir, inlined into the prompt. |
| `expected_output` | string   | yes      | Prose description of a good answer, shown to the judge. |
| `assertions`      | string[] | yes      | Atomic, binary, independently checkable claims. These are the score. |

## Authoring rules

- **Neutral prompts.** Do not restate the skill's rules in the prompt. If the
  prompt already tells the model to "use a Refs: footer," both sides pass and you
  measure nothing. Describe the task; let the skill supply the how.
- **Binary assertions.** Each assertion is one checkable fact.
  - Bad: `"The commit message is high quality."`
  - Good: `"The subject line is 50 characters or fewer."`
- **2–5 assertions per eval.** Enough to capture the skill's promises, few enough
  to grade reliably.
- **3–6 evals per skill.** Cover the distinct behaviors the skill claims.
- **`expected_output` is for the judge,** not the runners. Runners never see it.

## Scoring

For each (eval, side, trial) the judge returns pass/fail per assertion. The
**assertion pass rate** for a side = passed assertions / total assertions across
all trials. The skill's effect on an eval is:

```
lift = with_skill_pass_rate − without_skill_pass_rate
```

See the verdict table in the top-level `SKILL.md`.

## Minimal example

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": "core-behavior",
      "name": "core behavior",
      "prompt": "<a neutral task this skill should improve>",
      "expected_output": "<what a good answer contains>",
      "assertions": [
        "<binary claim 1>",
        "<binary claim 2>"
      ]
    }
  ]
}
```
