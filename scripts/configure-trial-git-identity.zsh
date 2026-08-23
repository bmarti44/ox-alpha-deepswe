#!/usr/bin/env zsh
set -euo pipefail

JOB_DIR=${1:?usage: configure-trial-git-identity.zsh JOB_DIR [PIER_PID]}
JOB_DIR=${JOB_DIR:A}
PIER_PID=${2:-}

configure_running_trials() {
  local container_id mount_sources

  for container_id in $(docker ps \
      --filter label=com.docker.compose.service=main \
      --format '{{.ID}}' 2>/dev/null); do
    mount_sources=$(docker inspect "$container_id" 2>/dev/null | jq -r '
      .[0].Mounts[]
      | select(.Destination | startswith("/logs/"))
      | .Source
    ' 2>/dev/null || true)

    # Limit changes to containers whose /logs mounts belong to this Pier job.
    [[ "$mount_sources" == *"$JOB_DIR/"* ]] || continue

    docker exec "$container_id" sh -lc '
      git -C /app config user.name >/dev/null 2>&1 ||
        git -C /app config user.name "DeepSWE Agent"
      git -C /app config user.email >/dev/null 2>&1 ||
        git -C /app config user.email "deepswe-agent@localhost"
    ' >/dev/null 2>&1 || true
  done
}

if [[ -z "$PIER_PID" ]]; then
  configure_running_trials
  exit 0
fi

while kill -0 "$PIER_PID" 2>/dev/null; do
  configure_running_trials
  sleep 2
done
