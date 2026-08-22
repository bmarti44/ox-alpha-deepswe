#!/usr/bin/env zsh
set -euo pipefail

# Keep Pier's local job metadata private by default.
umask 077

if [[ -z ${OPENCODE_API_KEY:-} ]]; then
  print -u2 'OPENCODE_API_KEY is not present in this shell.'
  print -u2 'Run `source ~/.zshrc` once, then retry.'
  exit 2
fi

SCRIPT_DIR=${0:A:h}
WORKSPACE_DIR=${SCRIPT_DIR:h}
PIER_JOB_NAME=${1:-ox-alpha-opencode-canary-$(date +%Y%m%d-%H%M%S)}

cd "$WORKSPACE_DIR"
exec pier run \
  --config "$WORKSPACE_DIR/pier-opencode-canary.yaml" \
  --job-name "$PIER_JOB_NAME" \
  --yes
