#!/usr/bin/env bash
# Runner adapter: OpenAI Codex CLI. Contract: prompt in $PROMPT env -> answer text on STDOUT.
# codex exec runs non-interactively; reasoning -> stderr, final message -> stdout.
set -euo pipefail
codex exec --skip-git-repo-check "$PROMPT" 2>/dev/null
