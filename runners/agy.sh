#!/usr/bin/env bash
# Runner adapter: Google Antigravity CLI (agy). Contract: prompt in $PROMPT env -> answer text on STDOUT.
set -euo pipefail
agy -p "$PROMPT" 2>/dev/null
