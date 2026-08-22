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
  local result_path trial_dir trial_name normalized_name image_name

  [[ -d "$JOB_DIR" ]] || return 0

  for result_path in "$JOB_DIR"/*/result.json(N); do
    jq -e '.finished_at != null' "$result_path" >/dev/null 2>&1 || continue
    trial_dir=${result_path:h}
    trial_name=${trial_dir:t}
    normalized_name=${trial_name:l}

    for image_name in \
      "${normalized_name}-main" \
      "${normalized_name}-pier-egress-proxy" \
      "${normalized_name}__verifier__trial-main"; do
      if docker image inspect "$image_name" >/dev/null 2>&1; then
        docker image rm "$image_name" >/dev/null 2>&1 || true
      fi
    done
  done

  find "$JOB_DIR" -type d -exec chmod 700 {} +
  find "$JOB_DIR" -type f -exec chmod 600 {} +
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
