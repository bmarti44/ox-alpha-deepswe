#!/usr/bin/env zsh
set -euo pipefail

# Keep Pier metadata and model trajectories private.
umask 077

if [[ -z ${OPENCODE_API_KEY:-} ]]; then
  print -u2 'OPENCODE_API_KEY is not present in this shell.'
  print -u2 'Run `source ~/.zshrc` once, then retry.'
  exit 2
fi

SCRIPT_DIR=${0:A:h}
WORKSPACE_DIR=${SCRIPT_DIR:h}
CONFIG_PATH=${WORKSPACE_DIR}/pier-opencode-full-suite.yaml
PIER_JOB_NAME=${1:-ox-alpha-opencode-full-$(date +%Y%m%d-%H%M%S)}
JOB_DIR=${WORKSPACE_DIR}/benchmark-results/${PIER_JOB_NAME}

cd "$WORKSPACE_DIR"

"$SCRIPT_DIR/verify-pier-secret-transport.py"

task_count=$(find "$WORKSPACE_DIR/deep-swe/tasks" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
if [[ "$task_count" != 113 ]]; then
  print -u2 "Expected 113 DeepSWE tasks, found ${task_count}."
  exit 3
fi

cleanup_completed_trial_images() {
  "$SCRIPT_DIR/cleanup-completed-trial-images.zsh" "$JOB_DIR"
}

print "Starting all ${task_count} DeepSWE tasks as job ${PIER_JOB_NAME}."

pier run \
  --config "$CONFIG_PATH" \
  --job-name "$PIER_JOB_NAME" \
  --n-concurrent 1 \
  --max-retries 1 \
  --yes &
pier_pid=$!

# Keep macOS awake for this multi-day job. The guard exits with Pier.
sleep_guard_pid=''
if command -v caffeinate >/dev/null 2>&1; then
  caffeinate -dimsu -w "$pier_pid" &
  sleep_guard_pid=$!
fi

while kill -0 "$pier_pid" 2>/dev/null; do
  cleanup_completed_trial_images
  sleep 30
done

set +e
wait "$pier_pid"
pier_status=$?
set -e

cleanup_completed_trial_images

if [[ -n "$sleep_guard_pid" ]]; then
  wait "$sleep_guard_pid" 2>/dev/null || true
fi

exit "$pier_status"
