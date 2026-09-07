#!/usr/bin/env bash
# Runner adapter: Google Gemini CLI. Contract: prompt in $PROMPT env -> answer text on STDOUT.
set -euo pipefail
gemini -p "$PROMPT" 2>/dev/null
