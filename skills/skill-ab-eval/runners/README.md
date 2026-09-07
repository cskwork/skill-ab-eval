# Runner adapters

A **runner** is one way to send a prompt to a model/CLI harness and get text back.
This is the harness axis: the same eval is run through several runners so you can
compare which CLI does the task best — with or without a skill loaded.

## Contract

Each adapter is a tiny shell script:

```
prompt in $PROMPT env  ->  the model's answer text on STDOUT
```

Nothing else on stdout (send logs/reasoning to stderr or /dev/null). Exit non-zero
on failure. That's the whole interface — it composes with any CLI. The orchestrator
reads the adapter and runs it with `bash -c`, so the prompt arrives as `$PROMPT`
(no temp files, and no path-mangling on Windows git-bash).

**Security:** always pass `$PROMPT` as a quoted argument to the target CLI
(`some-cli "$PROMPT"`). Never `eval "$PROMPT"`, never `bash -c "$PROMPT"`, and never
put it inside command substitution (`` `...$PROMPT...` `` / `$(...$PROMPT...)`) — the
prompt is untrusted text and those forms would execute it as shell code.

## Built-in adapters

| runner   | CLI         | invocation         | auth |
|----------|-------------|--------------------|------|
| `claude` | Claude Code | `claude -p`        | `claude` login / `ANTHROPIC_API_KEY` |
| `codex`  | OpenAI Codex| `codex exec`       | `codex login` / `OPENAI_API_KEY` |
| `gemini` | Gemini CLI  | `gemini -p`        | `gemini` login |
| `agy`    | Antigravity | `agy -p`           | `agy install` + Google sign-in |
| `openai` | HTTP API    | built-in (urllib)  | `OPENAI_API_KEY` |

`openai` is implemented inside `scripts/run_eval.py` (no shell adapter needed) so
it works without a separate `curl`/`jq`. Every other runner is a shell adapter
here, mirroring the delegation style of
[cc-agent-call](https://github.com/cskwork/cc-agent-call).

## Add your own harness

Drop `runners/<name>.sh` following the contract, then pass `--runners <name>`.
Example for a hypothetical `kiro`:

```bash
#!/usr/bin/env bash
set -euo pipefail
kiro-cli chat "$PROMPT" 2>/dev/null
```

The orchestrator auto-discovers any `runners/*.sh` plus the built-in `openai`.

## Notes

- Adapters require `bash` (git-bash/WSL on Windows) and the target CLI to be on
  `PATH`. The orchestrator runs `bash -c "<adapter contents>"` with `$PROMPT` set.
- These CLIs are *agentic* — for plain text tasks they just answer, but they may
  print framing. The judge grades the text regardless; keep prompts self-contained.
- A "skill" is loaded by prepending its `SKILL.md` body to the prompt (uniform
  across every harness), which is the faithful, portable way to inject skill context.
