#!/usr/bin/env zsh
set -euo pipefail

umask 077

SCRIPT_DIR=${0:A:h}
WORKSPACE_DIR=${SCRIPT_DIR:h}
JOB_NAME=${1:-ox-alpha-opencode-full-20260822}
JOB_DIR=${WORKSPACE_DIR}/benchmark-results/${JOB_NAME}
INTERVAL_SECONDS=${BENCHMARK_STATUS_INTERVAL_SECONDS:-1800}

cd "$WORKSPACE_DIR"

if [[ ! -f "$JOB_DIR/result.json" ]]; then
  print -u2 "Missing Pier result: $JOB_DIR/result.json"
  exit 2
fi

publish_status() {
  local trial_result trial_dir completed_count

  "$SCRIPT_DIR/update-readme-status.py" "$JOB_DIR"

  git add README.md "$JOB_DIR/result.json" "$JOB_DIR/config.json" \
    "$JOB_DIR/lock.json" "$JOB_DIR/job.log"

  for trial_result in "$JOB_DIR"/*/result.json(N); do
    jq -e '.finished_at != null' "$trial_result" >/dev/null 2>&1 || continue
    trial_dir=${trial_result:h}
    git add "$trial_dir"
  done

  if git diff --cached --quiet; then
    return 0
  fi

  gitleaks git --staged --no-banner --redact --no-color
  completed_count=$(jq -r '.stats.n_completed_trials' "$JOB_DIR/result.json")
  git commit -m "chore: update benchmark status (${completed_count}/113)"
  git push origin main
}

while true; do
  publish_status
  if jq -e '.finished_at != null' "$JOB_DIR/result.json" >/dev/null; then
    break
  fi
  sleep "$INTERVAL_SECONDS"
done
