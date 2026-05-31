#!/usr/bin/env bash
# Runner adapter: Claude Code. Contract: prompt in $PROMPT env -> answer text on STDOUT.
set -euo pipefail
claude -p "$PROMPT" 2>/dev/null
